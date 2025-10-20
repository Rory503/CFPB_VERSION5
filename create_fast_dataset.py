"""
Fast CFPB Data Loader - Pre-filtered Real Data
Creates a smaller file with ONLY the data we need for faster loading
"""

import pandas as pd
from datetime import datetime, timedelta
import os

def create_fast_dataset():
    """Create pre-filtered dataset with real CFPB data matching your requirements"""
    
    print("🏛️  Creating Fast CFPB Dataset")
    print("============================")
    
    # Load the full dataset
    data_file = "data/complaints.csv"
    if not os.path.exists(data_file):
        print("❌ Main data file not found")
        return False
    
    print("📊 Loading full CFPB data...")
    df = pd.read_csv(data_file, low_memory=False)
    print(f"✅ Loaded {len(df):,} total complaints")
    
    # Apply your exact filters
    print("🔍 Applying filters...")
    
    # 1. Last 6 months filter
    cutoff_date = datetime.now() - timedelta(days=180)
    cutoff_str = cutoff_date.strftime('%Y-%m-%d')
    df['Date received'] = pd.to_datetime(df['Date received'])
    df_recent = df[df['Date received'] >= cutoff_str]
    print(f"📅 Last 6 months: {len(df_recent):,} complaints")
    
    # 2. Only complaints with narratives (consumers)
    df_narratives = df_recent[df_recent['Consumer complaint narrative'].notna()]
    print(f"📝 With narratives: {len(df_narratives):,} complaints")
    
    # 3. Exclude credit reporting
    credit_products = ['Credit reporting, credit repair services, or other personal consumer reports']
    df_filtered = df_narratives[~df_narratives['Product'].isin(credit_products)]
    print(f"🚫 Excluding credit reporting: {len(df_filtered):,} complaints")
    
    # Save the pre-filtered dataset
    output_file = "data/complaints_filtered.csv"
    df_filtered.to_csv(output_file, index=False)
    print(f"💾 Saved filtered dataset to: {output_file}")
    print(f"📊 Final dataset: {len(df_filtered):,} real CFPB complaints")
    
    return True

if __name__ == "__main__":
    create_fast_dataset()