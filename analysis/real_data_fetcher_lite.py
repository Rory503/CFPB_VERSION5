"""
Lightweight real-data fetcher optimized for small memory instances.
Uses the CFPB Socrata API for a rolling window and supports Lite mode
that omits long narratives. Falls back to ZIP only when the API path
is unavailable.
"""

import os
import io
from datetime import datetime, timedelta
import requests
import pandas as pd


class RealDataFetcher:
    def __init__(self):
        # Configure rolling window (months)
        try:
            months = int(os.environ.get("MONTHS_WINDOW", "4"))
        except ValueError:
            months = 4
        months = max(1, min(months, 12))
        self.end_date = datetime.now()
        self.start_date = self.end_date - timedelta(days=30 * months)

        # Lite mode: exclude long narratives to reduce memory
        self.lite_mode = str(os.environ.get("LITE_MODE", "0")).lower() in ("1", "true", "yes")
        self.include_narratives = not self.lite_mode

        # Exclusions (credit reporting)
        self.credit_exclusions = [
            "Credit reporting, credit repair services, or other personal consumer reports",
            "Credit reporting",
            "Credit repair services",
            "Other personal consumer reports",
        ]

        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)

    def _fetch_api(self):
        endpoint = "https://data.consumerfinance.gov/resource/s6ew-h6mp.csv"
        where = (
            f"date_received between '{self.start_date:%Y-%m-%d}' and '{self.end_date:%Y-%m-%d}'"
        )
        if self.include_narratives:
            where += " AND consumer_complaint_narrative IS NOT NULL"
        if self.credit_exclusions:
            not_in = ",".join([f"'{c}'" for c in self.credit_exclusions])
            where += f" AND product NOT IN({not_in})"

        select_cols = [
            "complaint_id",
            "date_received",
            "date_sent_to_company",
            "product",
            "issue",
            "company",
            "state",
        ]
        if self.include_narratives:
            select_cols.append("consumer_complaint_narrative")

        headers = {"Accept": "text/csv"}
        token = os.environ.get("SOCRATA_APP_TOKEN")
        if token:
            headers["X-App-Token"] = token

        batch = 25000
        offset = 0
        frames = []
        total = 0

        while True:
            params = {
                "$select": ",".join(select_cols),
                "$where": where,
                "$order": "date_received DESC",
                "$limit": batch,
                "$offset": offset,
            }
            r = requests.get(endpoint, params=params, headers=headers, timeout=90)
            r.raise_for_status()
            if not r.text.strip():
                break
            chunk = pd.read_csv(io.StringIO(r.text))
            if chunk.empty:
                break
            frames.append(chunk)
            total += len(chunk)
            if len(chunk) < batch:
                break
            offset += batch

        if not frames:
            return None

        df = pd.concat(frames, ignore_index=True)
        df.rename(
            columns={
                "complaint_id": "Complaint ID",
                "date_received": "Date received",
                "date_sent_to_company": "Date sent to company",
                "product": "Product",
                "issue": "Issue",
                "company": "Company",
                "state": "State",
                "consumer_complaint_narrative": "Consumer complaint narrative",
            },
            inplace=True,
        )
        df["Date received"] = pd.to_datetime(df["Date received"]) 
        df["Date sent to company"] = pd.to_datetime(df["Date sent to company"], errors="coerce") 
        for col in ["Product", "Issue", "Company", "State"]:
            if col in df.columns:
                df[col] = df[col].astype("category")
        # Cache a filtered file for quick re-use
        try:
            df.to_csv(os.path.join(self.data_dir, "complaints_filtered.csv"), index=False)
        except Exception:
            pass
        return df

    def load_and_filter_data(self):
        print(
            f"Loading CFPB data (lite={self.lite_mode}) for window: {self.start_date:%Y-%m-%d} to {self.end_date:%Y-%m-%d}"
        )
        # Try cached filtered file first - but only if it's recent (not from old hardcoded dates)
        cache = os.path.join(self.data_dir, "complaints_filtered.csv")
        if os.path.exists(cache):
            try:
                # Check cache age - ignore if older than 1 day to avoid stale data
                cache_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(cache))
                if cache_age.days < 1:
                    df = pd.read_csv(cache, low_memory=False)
                    df["Date received"] = pd.to_datetime(df["Date received"]) 
                    df["Date sent to company"] = pd.to_datetime(df["Date sent to company"], errors="coerce") 
                    # Also check if data is in current date range
                    if len(df) > 0:
                        max_date = df["Date received"].max()
                        if max_date.date() >= self.start_date.date():
                            return df
            except Exception:
                pass

        # API fast path
        try:
            print("Attempting API fetch...")
            df = self._fetch_api()
            if df is not None:
                print(f"API fetch successful: {len(df)} records")
                return df
            else:
                print("API returned None")
        except Exception as e:
            print(f"API path failed: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

        # Fallback: let the legacy fetcher handle ZIP if really needed
        # Import lazily to avoid pulling heavy deps here
        try:
            print("Attempting legacy ZIP fallback...")
            from .real_data_fetcher import CFPBRealDataFetcher as Legacy

            legacy = Legacy()
            result = legacy.load_and_filter_data()
            if result is not None:
                print(f"Legacy ZIP fallback successful: {len(result)} records")
            else:
                print("Legacy ZIP fallback returned None")
            return result
        except Exception as e:
            print(f"Legacy ZIP path failed: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            return None

    # The following helpers mirror the original fetcher API
    def get_top_trends(self, df, top_n=10):
        if df is None or len(df) == 0:
            return None
        top_products = df["Product"].value_counts().head(top_n)
        top_issues = df["Issue"].value_counts().head(top_n)
        combos = (
            df.groupby(["Product", "Issue"]).size().reset_index(name="Count").sort_values("Count", ascending=False).head(top_n)
        )
        return {"top_products": top_products, "top_issues": top_issues, "product_issue_combinations": combos}

    def get_sub_trends(self, df, product, top_n=5):
        if df is None or len(df) == 0:
            return None
        sub = df[df["Product"] == product]
        if sub.empty:
            return None
        counts = sub["Issue"].value_counts().head(top_n)
        details = {}
        for issue in counts.index:
            sample = sub[sub["Issue"] == issue][
                [
                    "Complaint ID",
                    "Consumer complaint narrative",
                    "Company",
                    "State",
                    "Date received",
                ]
            ].head(3)
            details[issue] = {
                "count": counts[issue],
                "percentage": (counts[issue] / len(sub)) * 100,
                "sample_complaints": sample.to_dict("records"),
            }
        return details

    def get_top_companies(self, df, top_n=10):
        if df is None or len(df) == 0:
            return None
        credit_agencies = [
            "EQUIFAX, INC.",
            "Experian Information Solutions Inc.",
            "TRANSUNION INTERMEDIATE HOLDINGS, INC.",
            "TransUnion Intermediate Holdings, Inc.",
            "EXPERIAN INFORMATION SOLUTIONS INC.",
            "Equifax Information Services LLC",
            "EXPERIAN",
            "EQUIFAX",
        ]
        base = df[~df["Company"].isin(credit_agencies)]
        top = base["Company"].value_counts().head(top_n)
        out = {}
        for company in top.index:
            cdf = base[base["Company"] == company]
            out[company] = {
                "total_complaints": top[company],
                "top_issues": cdf["Issue"].value_counts().head(5).to_dict(),
                "sample_complaints": cdf[[
                    "Complaint ID",
                    "Consumer complaint narrative",
                    "Issue",
                    "Product",
                    "Date received",
                ]].head(5).to_dict("records"),
            }
        return out

    def generate_complaint_links(self, complaint_ids):
        base = "https://www.consumerfinance.gov/data-research/consumer-complaints/search/detail/"
        return [f"{base}{cid}" for cid in complaint_ids]

    def export_analysis_data(self, df, output_path):
        if df is None or len(df) == 0:
            return
        summary = {
            "total_complaints": len(df),
            "date_range": f"{self.start_date:%Y-%m-%d} to {self.end_date:%Y-%m-%d}",
            "unique_companies": df["Company"].nunique(),
            "unique_products": df["Product"].nunique(),
            "unique_states": df["State"].nunique(),
            "data_exported": datetime.now().isoformat(),
        }
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            pd.DataFrame([summary]).to_excel(writer, sheet_name="Summary", index=False)
            df.head(10000).to_excel(writer, sheet_name="Filtered_Data", index=False)
            tp = df["Product"].value_counts().head(20)
            pd.DataFrame({"Product": tp.index, "Count": tp.values}).to_excel(writer, sheet_name="Top_Products", index=False)
