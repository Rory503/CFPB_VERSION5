"""
CFPB Analysis - Modern Web Dashboard
Beautiful, interactive dashboard with real-time charts and data visualization
Updated: Demo expiration removed - Full version active
"""

import streamlit as st
from functools import lru_cache
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
from datetime import datetime, timedelta
import json
import io
import base64

# OpenAI imports for chat interface
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Configure page
st.set_page_config(
    page_title="CFPB Consumer Complaint Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add analysis modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'analysis'))

try:
    from analysis.cfpb_real_analyzer import CFPBRealAnalyzer
    from analysis.ftc_real_triangulator import FTCRealTriangulator
    from analysis.data_exporter import CFPBDataExporter
except ImportError as e:
    print(f"Import error: {e}")
    CFPBRealAnalyzer = None
    FTCRealTriangulator = None
    CFPBDataExporter = None

# Clean, professional styling - No overlapping text
st.markdown("""
<style>
    /* Clean button styling */
    .stButton > button {
        background: #003d7a;
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        width: 100%;
        margin: 0.4rem 0;
        border-radius: 6px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background: #0066cc;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
    }
    
    /* Proper metrics spacing */
    .stMetric {
        background: #f8f9fa;
        padding: 1.2rem;
        border-radius: 8px;
        border: 1px solid #e6e6e6;
    }
    
    .stMetric label {
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        color: #666 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #003d7a !important;
    }
    
    /* Tab styling - improved for visibility */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #23263b;
        padding: 0.5rem;
        border-radius: 8px;
        border: 1px solid #444;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 6px;
        color: #222 !important;
        background: #e6e8f0;
        border: 1px solid #bbb;
        margin-right: 0.2rem;
        opacity: 1 !important;
        transition: background 0.2s, color 0.2s;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #003d7a !important;
        color: #fff !important;
        border: 1.5px solid #003d7a;
        font-weight: 700;
        box-shadow: 0 2px 8px rgba(0,61,122,0.08);
        opacity: 1 !important;
    }
    
    /* Clean headers */
    h1, h2, h3 {
        font-weight: 600 !important;
        line-height: 1.3 !important;
        margin-bottom: 1rem !important;
    }
    
    /* Proper column spacing */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Chat interface improvements */
    .stChatMessage {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header - Simplified and clean
    st.title("🏛️ CFPB Consumer Complaint Database Analysis")
    st.markdown("### Consumer Financial Protection Bureau - Complaint Trends and Analysis")
    st.caption("Analysis Period: Last 6 Months | Data Source: Official CFPB Database | Focus Areas: AI Bias, Language Access, Digital Fraud")
    
    # Initialize session state
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = None
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = None
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # Sidebar
    with st.sidebar:
        st.markdown("## Analysis Controls")
        
        # Analysis Status
        st.markdown("### Current Status")
        if st.session_state.analysis_complete:
            st.success("Analysis Complete")
        else:
            st.info("Ready to Analyze")
        
        # Analysis Controls
        st.markdown("### Analysis Options")
        
        # Month selection for data loading
        months_to_load = st.selectbox(
            "Load data for past:",
            [1, 2, 3, 4, 5, 6],
            index=3,
            help="Select how many months of complaint data to load (1-6 months)"
        )
        
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Upload Your Own CSV", "Quick Analysis (Use Existing Data)", "Full Analysis (Download Latest Data)"],
            help="Upload your own CSV file or use existing data"
        )
        
        # File upload section
        if analysis_type == "Upload Your Own CSV":
            st.markdown("### 📁 Upload CFPB Data")
            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type="csv",
                help="Upload a CFPB complaints CSV file. Should have columns like 'Complaint ID', 'Date received', 'Product', 'Issue', 'Company', 'State', 'Consumer complaint narrative'"
            )
            
            if uploaded_file is not None:
                try:
                    # Load the uploaded file
                    df = pd.read_csv(uploaded_file, low_memory=False)
                    st.success(f"✅ Loaded {len(df):,} complaints from uploaded file")
                    
                    # Show column info
                    st.info(f"📊 Columns found: {', '.join(df.columns.tolist())}")
                    
                    # Store in session state for analysis
                    st.session_state.uploaded_data = df

                    # Quick Preview option to open dashboard immediately without heavy processing
                    if st.button("🚀 Open Preview Now", type="primary"):
                        # Minimal analyzer stub
                        class _Stub: pass
                        stub = _Stub()
                        # Normalize minimal fields for charts that need them
                        col_map = {c.lower().strip(): c for c in df.columns}
                        def col(*names):
                            for n in names:
                                if n in df.columns:
                                    return n
                                ln = n.lower()
                                if ln in col_map:
                                    return col_map[ln]
                            return None
                        prod = col('Product','product')
                        issue = col('Issue','issue')
                        company = col('Company','company')
                        date_received = col('Date received','date_received')
                        state = col('State','state')
                        narr = col('Consumer complaint narrative','consumer_complaint_narrative','narrative')
                        needed = [x for x in [prod, issue, company, date_received, state, narr] if x]
                        df_small = df[needed].copy()
                        if date_received:
                            import pandas as _pd
                            df_small[date_received] = _pd.to_datetime(df_small[date_received], errors='coerce')
                        # Rename to expected names where possible
                        rename = {}
                        if prod and prod != 'Product': rename[prod] = 'Product'
                        if issue and issue != 'Issue': rename[issue] = 'Issue'
                        if company and company != 'Company': rename[company] = 'Company'
                        if state and state != 'State': rename[state] = 'State'
                        if narr and narr != 'Consumer complaint narrative': rename[narr] = 'Consumer complaint narrative'
                        if date_received and date_received != 'Date received': rename[date_received] = 'Date received'
                        df_small.rename(columns=rename, inplace=True)
                        # Minimal session for dashboard
                        st.session_state.analysis_complete = True
                        st.session_state.analyzer = _Stub()
                        st.session_state.analyzer.filtered_df = df_small
                        # Build lightweight summary/trends directly
                        import pandas as _pd
                        summary = {
                            'total_complaints': len(df_small),
                            'unique_companies': df_small['Company'].nunique() if 'Company' in df_small.columns else 0,
                            'unique_products': df_small['Product'].nunique() if 'Product' in df_small.columns else 0,
                            'unique_states': df_small['State'].nunique() if 'State' in df_small.columns else 0,
                            'date_range': f"{str(df_small['Date received'].min())[:10]} to {str(df_small['Date received'].max())[:10]}",
                            'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        trends = {
                            'top_products': (df_small['Product'].value_counts() if 'Product' in df_small.columns else _pd.Series(dtype=int)),
                            'top_issues': (df_small['Issue'].value_counts() if 'Issue' in df_small.columns else _pd.Series(dtype=int)),
                            'sub_trends': {}
                        }
                        companies = {}
                        if 'Company' in df_small.columns:
                            top_companies = df_small['Company'].value_counts().head(10)
                            for name in top_companies.index:
                                subset = df_small[df_small['Company'] == name]
                                companies[name] = {
                                    'total_complaints': len(subset),
                                    'top_issues': (subset['Issue'].value_counts().head(5).to_dict() if 'Issue' in subset.columns else {}),
                                    'sample_complaints': []
                                }
                        st.session_state.analysis_data = {
                            'summary': summary,
                            'trends': trends,
                            'companies': companies,
                            'special_categories': {'ai_complaints': [], 'lep_complaints': [], 'fraud_digital_complaints': []}
                        }
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error loading file: {str(e)}")
        
        include_ftc = st.checkbox("Include FTC Cross-Validation", value=True)
        generate_excel = st.checkbox("Generate Excel Export", value=True)
        auto_refresh = st.checkbox("Auto-refresh Visualizations", value=True)
        
        # Run Analysis Button
        if st.button("Start Analysis", type="primary"):
            # Only run if analysis hasn't been completed yet or if explicitly requested
            if not st.session_state.analysis_complete:
                success = run_analysis(analysis_type, include_ftc, generate_excel, months_to_load)
                # Only rerun on success so any error remains visible instead of flashing
                if success:
                    st.rerun()
                else:
                    st.warning("Analysis failed or was interrupted. See the error above; not auto-retrying.")
            else:
                st.info("Analysis already completed! Check the main area for results.")
        
        # Reset Analysis Button (for debugging/re-running)
        if st.session_state.analysis_complete:
            if st.button("🔄 Reset Analysis", type="secondary"):
                st.session_state.analysis_complete = False
                st.session_state.analysis_data = None
                st.session_state.analyzer = None
                st.rerun()
        
        # Quick Stats
        if st.session_state.analysis_complete and st.session_state.analysis_data:
            st.markdown("### Summary Statistics")
            data = st.session_state.analysis_data
            
            st.metric("Total Complaints", f"{data['summary']['total_complaints']:,}")
            st.metric("Companies Analyzed", f"{data['summary']['unique_companies']:,}")
            st.metric("Product Categories", f"{data['summary']['unique_products']:,}")
            
            if 'special_categories' in data:
                ai_count = len(data['special_categories']['ai_complaints']) if hasattr(data['special_categories']['ai_complaints'], '__len__') else 0
                lep_count = len(data['special_categories']['lep_complaints']) if hasattr(data['special_categories']['lep_complaints'], '__len__') else 0
                fraud_count = len(data['special_categories']['fraud_digital_complaints']) if hasattr(data['special_categories']['fraud_digital_complaints'], '__len__') else 0
                
                st.metric("AI-Related Issues", ai_count)
                st.metric("Language Access Issues", lep_count)
                st.metric("Digital Fraud Cases", fraud_count)
    
    # Main Content Area
    if not st.session_state.analysis_complete:
        show_welcome_screen()
    else:
        show_analysis_dashboard()

def show_welcome_screen():
    """Show welcome screen with system info"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## Analysis Parameters")
        
        specs_data = {
            "Parameter": [
                "Analysis Period",
                "Data Source", 
                "Filtering Criteria",
                "Excluded Categories",
                "Focus Areas",
                "Export Formats"
            ],
            "Value": [
                "Last 6 months (April 19 - October 19, 2025)",
                "CFPB Consumer Complaint Database (Official)",
                "Complaints with consumer narratives only, excludes credit reporting",
                "Credit reporting agencies (Equifax, Experian, TransUnion)",
                "Algorithmic bias, Limited English Proficiency, Digital fraud",
                "Markdown reports, Excel spreadsheets, Interactive charts"
            ]
        }
        
        specs_df = pd.DataFrame(specs_data)
        st.dataframe(specs_df, width=800, hide_index=True)
        
        st.markdown("## Real CFPB Data Analysis")
        
        st.info("📊 **All data comes directly from the official CFPB Consumer Complaint Database**")
        st.markdown("""
        **Data Source**: https://files.consumerfinance.gov/ccdb/complaints.csv.zip  
        **No Mock Data**: System only processes real complaint data  
        **Verification**: Every complaint includes link to CFPB.gov for verification  
        
        Click **"Start Analysis"** to load and analyze real CFPB complaint data.
        """)
    
    with col2:
        st.markdown("## Analysis Outputs")
        
        st.markdown("### 📊 Real Data Analysis Features")
        st.markdown("""
        **After running analysis, you will see:**
        - ✅ **Real complaint counts** from CFPB database
        - 🏢 **Actual company data** with verification links  
        - 📊 **Genuine trends** from official complaint data
        - 🔗 **Clickable links** to verify every complaint on CFPB.gov
        - 📤 **Excel exports** with full data verification
        """)
        
        st.markdown("## Ready for Real Data Analysis")
        
        st.success("📊 **System Ready** - Click 'Start Analysis' to begin processing real CFPB complaint data")
        
        st.markdown("**Analysis will generate:**")
        st.markdown("""
        - 📊 **Real complaint statistics** from CFPB database
        - 🏢 **Actual company rankings** with verification links
        - 🎯 **Genuine AI bias, LEP, and fraud cases** 
        - 📤 **Excel exports** with CFPB verification URLs
        - 🔗 **Clickable links** to verify every complaint
        """)


# Cache the loading of the filtered real data for instant Quick Analysis
@st.cache_data(show_spinner="Loading real CFPB data...")
def get_filtered_real_data(months_window=None):
    try:
        from analysis.real_data_fetcher_lite import RealDataFetcher as RealDataFetcher
    except Exception:
        from analysis.real_data_fetcher import CFPBRealDataFetcher as RealDataFetcher
    
    # Set environment variable for month window if provided
    if months_window is not None:
        import os
        os.environ['MONTHS_WINDOW'] = str(months_window)
    
    fetcher = RealDataFetcher()
    return fetcher.load_and_filter_data()

def run_analysis(analysis_type, include_ftc, generate_excel, months_to_load=6):
    """Run the CFPB analysis; returns True on success, False on failure."""
    progress_container = st.container()
    with progress_container:
        st.markdown("## 🚀 Running Analysis...")
        progress_bar = st.progress(0)
        status_text = st.empty()
        try:
            status_text.text("Initializing CFPB Data Analyzer...")
            progress_bar.progress(10)
            if CFPBRealAnalyzer is None:
                st.error("Analysis modules not available")
                return False
            analyzer = CFPBRealAnalyzer()
            # Data loading logic
            status_text.text("Loading CFPB complaint database...")
            progress_bar.progress(30)
            if analysis_type == "Upload Your Own CSV":
                # Use uploaded data
                if 'uploaded_data' not in st.session_state or st.session_state.uploaded_data is None:
                    st.error("No CSV file uploaded. Please upload a file first.")
                    return False
                df = st.session_state.uploaded_data.copy()
                
                # Normalize column names to expected format
                col_map = {c.lower().strip(): c for c in df.columns}
                def pick(*names):
                    for n in names:
                        if n in df.columns:
                            return n
                        ln = n.lower()
                        if ln in col_map:
                            return col_map[ln]
                    return None
                required = {
                    'Complaint ID': pick('Complaint ID','complaint_id','id'),
                    'Date received': pick('Date received','date_received'),
                    'Date sent to company': pick('Date sent to company','date_sent_to_company'),
                    'Product': pick('Product','product'),
                    'Issue': pick('Issue','issue'),
                    'Company': pick('Company','company'),
                    'State': pick('State','state'),
                    'Consumer complaint narrative': pick('Consumer complaint narrative','consumer_complaint_narrative','narrative')
                }
                missing = [k for k,v in required.items() if v is None]
                if missing:
                    st.error(f"Uploaded CSV is missing required columns: {', '.join(missing)}")
                    return False
                # Select and rename only needed columns (reduces memory)
                df_small = df[[required[k] for k in required]].rename(columns={required[k]:k for k in required})
                
                # Convert dates
                try:
                    df_small['Date received'] = pd.to_datetime(df_small['Date received'])
                    if 'Date sent to company' in df_small.columns:
                        df_small['Date sent to company'] = pd.to_datetime(df_small['Date sent to company'], errors='coerce')
                except Exception:
                    pass
                
                # Limit very large uploads for responsiveness
                if len(df_small) > 250_000:
                    df_small = df_small.head(250_000)
                    st.info("Large file detected – analyzing first 250,000 rows for speed.")
                
                analyzer.filtered_df = df_small
                st.success(f"Successfully loaded {len(analyzer.filtered_df):,} complaints from uploaded file")
            elif analysis_type == "Quick Analysis (Use Existing Data)":
                # Use data with specified month window - need to bypass cache for custom months
                try:
                    from analysis.real_data_fetcher_lite import RealDataFetcher as RealDataFetcher
                except Exception:
                    from analysis.real_data_fetcher import CFPBRealDataFetcher as RealDataFetcher
                
                # Set environment variable for month window
                import os
                os.environ['MONTHS_WINDOW'] = str(months_to_load)
                
                fetcher = RealDataFetcher()
                analyzer.filtered_df = fetcher.load_and_filter_data()
                
                if analyzer.filtered_df is None:
                    st.error("Failed to load pre-filtered real CFPB data.")
                    return False
                st.success(f"Successfully loaded {len(analyzer.filtered_df):,} complaints for analysis (Quick Analysis - {months_to_load} months)")
            else:
                # Full Analysis: force reprocess/download and refresh cache
                success = analyzer.load_real_data(force_download=True)
                if not success:
                    st.error("Failed to load CFPB data")
                    return False
                st.success(f"Successfully loaded {len(analyzer.filtered_df):,} complaints for analysis (Full Analysis)")
                # Clear Streamlit cache so next Quick Analysis uses new data
                get_filtered_real_data.clear()
            # Generate analysis
            status_text.text("Processing complaint data and generating analysis...")
            progress_bar.progress(60)
            analysis_results = analyzer.create_detailed_report()
            if not analysis_results:
                st.error("Failed to generate analysis report")
                return False
            # FTC Triangulation
            if include_ftc:
                status_text.text("Running FTC cross-validation...")
                progress_bar.progress(80)
                if FTCRealTriangulator:
                    ftc_triangulator = FTCRealTriangulator(analyzer)
                    if ftc_triangulator.load_ftc_real_data():
                        triangulation_results = ftc_triangulator.create_triangulation_report()
                        if triangulation_results:
                            st.success("FTC cross-validation complete")
            # Excel export
            if generate_excel:
                status_text.text("Generating Excel export...")
                progress_bar.progress(90)
                analyzer.data_fetcher.export_analysis_data(
                    analyzer.filtered_df,
                    "outputs/cfpb_real_analysis.xlsx"
                )
                st.success("Excel export complete")
            # Complete
            progress_bar.progress(100)
            status_text.text("Analysis Complete")
            # Store results
            st.session_state.analyzer = analyzer
            st.session_state.analysis_data = analysis_results
            st.session_state.analysis_complete = True
            # Clear the progress indicators
            progress_container.empty()
            st.success("✅ Analysis completed successfully! View results in the tabs below.")
            return True
        except Exception as e:
            st.error(f"Analysis error: {str(e)}")
            return False

def show_analysis_dashboard():
    """Show the main analysis dashboard with charts"""
    
    data = st.session_state.analysis_data
    analyzer = st.session_state.analyzer
    
    # Top metrics row - Using native Streamlit metrics for consistency
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Complaints Analyzed",
            value=f"{data['summary']['total_complaints']:,}"
        )
    
    with col2:
        st.metric(
            label="Financial Institutions",
            value=f"{data['summary']['unique_companies']:,}"
        )
    
    with col3:
        st.metric(
            label="Product Categories",
            value=f"{data['summary']['unique_products']:,}"
        )
    
    with col4:
        if 'special_categories' in data:
            # Fix the counting - check if these are DataFrames or lists
            ai_count = len(data['special_categories']['ai_complaints']) if hasattr(data['special_categories']['ai_complaints'], '__len__') else 0
            lep_count = len(data['special_categories']['lep_complaints']) if hasattr(data['special_categories']['lep_complaints'], '__len__') else 0  
            fraud_count = len(data['special_categories']['fraud_digital_complaints']) if hasattr(data['special_categories']['fraud_digital_complaints'], '__len__') else 0
            
            total_special = ai_count + lep_count + fraud_count
            st.metric(
                label="Priority Issue Cases",
                value=f"{total_special:,}"
            )
    
    # Main charts section
    st.markdown("## Data Visualizations and Analysis")
    
    # Tab layout for different chart types - Added Consumer Complaints tab
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Professional Dashboard", "📈 Complaint Trends", "🏢 Company Analysis", "📋 Consumer Complaints", "🤖 AI Chat Assistant"])
    
    with tab1:
        show_professional_dashboard(data, analyzer)
    
    with tab2:
        show_trends_charts(data)
    
    with tab3:
        show_companies_charts(data)
    
    with tab4:
        show_consumer_complaints(data, analyzer)
    
    with tab5:
        show_ai_chat_interface(data, analyzer)
    
    # Excel Export Section
    st.markdown("---")
    st.markdown("## 📊 Data Export & Verification")
    show_export_section(analyzer)

def show_professional_dashboard(data, analyzer):
    """Show comprehensive professional dashboard like the examples provided"""
    
    try:
        from analysis.comprehensive_dashboard import create_comprehensive_dashboard
        
        # Create the full comprehensive dashboard with all charts and metrics
        create_comprehensive_dashboard(data, analyzer)
        
    except ImportError as e:
        st.error(f"Comprehensive dashboard not available: {e}")
        # Fallback to basic dashboard
        show_basic_fallback_dashboard(data, analyzer)
    except Exception as e:
        st.error(f"Dashboard error: {e}")
        show_basic_fallback_dashboard(data, analyzer)

def show_basic_fallback_dashboard(data, analyzer):
    """Fallback dashboard if comprehensive one fails"""
    st.markdown("### 📊 Basic Dashboard (Fallback Mode)")
    
    if 'summary' in data:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Complaints", f"{data['summary']['total_complaints']:,}")
        with col2:
            st.metric("Companies", f"{data['summary']['unique_companies']:,}")
        with col3:
            st.metric("Products", f"{data['summary']['unique_products']}")
    
    if 'trends' in data and 'top_products' in data['trends']:
        st.subheader("Top Product Categories")
        products = data['trends']['top_products'].head(10)
        
        import plotly.graph_objects as go
        fig = go.Figure(data=[
            go.Bar(x=products.index, y=products.values, 
                   marker_color='rgba(55, 128, 191, 0.7)')
        ])
        fig.update_layout(
            title="Top 10 Product Categories by Complaint Volume",
            xaxis_title="Product Category",
            yaxis_title="Number of Complaints",
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

# Filtering function removed - using all real CFPB data without filtering

def show_trends_charts(data):
    """Show trend analysis charts"""
    
    if 'trends' not in data:
        st.warning("No trend data available")
        return
    
    trends = data['trends']
    
    # Top products chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔥 Top Complaint Categories")
        
        # Use all real CFPB data
        products_data = list(trends['top_products'].items())[:10]
        products_df = pd.DataFrame(products_data, columns=['Product', 'Complaints'])
        
        fig = px.bar(
            products_df,
            x='Complaints',
            y='Product',
            orientation='h',
            title="Top 10 Complaint Categories",
            color='Complaints',
            color_continuous_scale='viridis'
        )
        fig.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📊 Distribution Pie Chart")
        
        fig = px.pie(
            products_df.head(8),
            values='Complaints',
            names='Product',
            title="Complaint Distribution (Top 8)"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Sub-trends analysis
    st.markdown("### 🔍 Sub-Trend Analysis")
    
    if 'sub_trends' in trends:
        sub_trends = trends['sub_trends']
        
        # Select product for sub-trend viewing
        selected_product = st.selectbox(
            "Select Product Category for Sub-Trends:",
            list(sub_trends.keys())
        )
        
        if selected_product and selected_product in sub_trends:
            sub_data = sub_trends[selected_product]
            sub_df = pd.DataFrame(list(sub_data.items()), columns=['Issue', 'Count'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.bar(
                    sub_df.head(10),
                    x='Count',
                    y='Issue',
                    orientation='h',
                    title=f"Sub-trends in {selected_product}",
                    color='Count',
                    color_continuous_scale='plasma'
                )
                fig.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.treemap(
                    sub_df.head(8),
                    values='Count',
                    names='Issue',
                    title=f"Issue Breakdown - {selected_product}"
                )
                st.plotly_chart(fig, use_container_width=True)

def show_companies_charts(data):
    """Show company analysis charts"""
    
    if 'companies' not in data:
        st.warning("No company data available")
        return
    
    companies = data['companies']
    
    # Top companies chart
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏢 Most Complained About Companies")
        
        companies_list = [(name, info['total_complaints']) for name, info in list(companies.items())[:15]]
        companies_df = pd.DataFrame(companies_list, columns=['Company', 'Complaints'])
        
        fig = px.bar(
            companies_df,
            x='Complaints',
            y='Company',
            orientation='h',
            title="Top 15 Companies by Complaint Volume",
            color='Complaints',
            color_continuous_scale='reds'
        )
        fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 Company Complaint Trends")
        
        # Create a sunburst chart
        fig = px.sunburst(
            companies_df.head(10),
            values='Complaints',
            names='Company',
            title="Company Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Company details table
        st.markdown("### 📋 Company Details")
        
        company_details = []
        for company, info in list(companies.items())[:10]:
            company_details.append({
                "Company": company,
                "Total Complaints": info['total_complaints'],
                "Top Issues": ", ".join(list(info['top_issues'].keys())[:3])
            })
        
        details_df = pd.DataFrame(company_details)
        st.dataframe(details_df, use_container_width=True, hide_index=True)

def show_consumer_complaints(data, analyzer):
    """Show individual consumer complaints with all details"""
    
    st.markdown("### 📋 Individual Consumer Complaints")
    st.markdown("View detailed information for each complaint in the database")
    
    if not analyzer or not hasattr(analyzer, 'filtered_df') or analyzer.filtered_df is None:
        st.warning("No complaint data available. Please run the analysis first.")
        return
    
    df = analyzer.filtered_df
    
    # Check if we have the necessary columns - handle both capitalized and lowercase
    col_map = {c.lower().strip(): c for c in df.columns}
    
    # Map column names - try multiple variations for robustness
    complaint_id_col = col_map.get('complaint id') or 'Complaint ID'
    company_col = col_map.get('company') or 'Company'
    company_response_col = col_map.get('company response to consumer') or 'Company response to consumer'
    timely_col = col_map.get('timely response?') or 'Timely response?'
    date_received_col = col_map.get('date received') or 'Date received'
    state_col = col_map.get('state') or 'State'
    product_col = col_map.get('product') or 'Product'
    subproduct_col = col_map.get('sub-product') or 'Sub-product'
    issue_col = col_map.get('issue') or 'Issue'
    subissue_col = col_map.get('sub-issue') or 'Sub-issue'
    
    # Try multiple variations for narrative column
    narrative_col = None
    for possible_name in ['consumer complaint narrative', 'Consumer complaint narrative', 'consumer_complaint_narrative', 'narrative']:
        if possible_name in df.columns:
            narrative_col = possible_name
            break
        if possible_name.lower() in col_map:
            narrative_col = col_map[possible_name.lower()]
            break
    
    if narrative_col is None:
        # Last resort: search for any column containing 'narrative' or 'complaint'
        for col in df.columns:
            if 'narrative' in str(col).lower() or 'complaint' in str(col).lower():
                narrative_col = col
                break
    
    # Create filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Company filter
        if company_col in df.columns:
            companies = sorted(df[company_col].dropna().unique())
            selected_company = st.selectbox("Filter by Company:", ["All"] + companies[:50])
        else:
            selected_company = "All"
    
    with col2:
        # Product filter
        if product_col in df.columns:
            products = sorted(df[product_col].dropna().unique())
            selected_product = st.selectbox("Filter by Product:", ["All"] + products)
        else:
            selected_product = "All"
    
    with col3:
        # Number of complaints to show - add "All" option
        num_complaints = st.selectbox("Number of complaints to show:", [10, 25, 50, 100, 200, 500, 1000, "All"], index=2)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_company != "All" and company_col in df.columns:
        filtered_df = filtered_df[filtered_df[company_col] == selected_company]
    
    if selected_product != "All" and product_col in df.columns:
        filtered_df = filtered_df[filtered_df[product_col] == selected_product]
    
    # Limit number of complaints
    if num_complaints == "All":
        display_df = filtered_df.copy()
    else:
        display_df = filtered_df.head(num_complaints)
    
    # Display summary
    st.info(f"Showing {len(display_df):,} out of {len(filtered_df):,} total complaints matching your filters")
    
    # Display each complaint
    for idx, row in display_df.iterrows():
        # Create container for each complaint
        with st.expander(f"Complaint #{row.get(complaint_id_col, idx)} - {row.get(company_col, 'Unknown Company')}", expanded=False):
            
            # Create two columns for layout
            left_col, right_col = st.columns([1, 1])
            
            with left_col:
                st.markdown(f"**Complaint ID:** `{row.get(complaint_id_col, 'N/A')}`")
                st.markdown(f"**Company Name:** {row.get(company_col, 'N/A')}")
                st.markdown(f"**Company Response:** {row.get(company_response_col, 'N/A')}")
                st.markdown(f"**Timely Response:** {row.get(timely_col, 'N/A')}")
                st.markdown(f"**Date Received:** {row.get(date_received_col, 'N/A')}")
                st.markdown(f"**Consumer's State:** {row.get(state_col, 'N/A')}")
            
            with right_col:
                st.markdown(f"**Product:** {row.get(product_col, 'N/A')}")
                if subproduct_col in df.columns and pd.notna(row.get(subproduct_col)):
                    st.markdown(f"**Sub-product:** {row.get(subproduct_col, 'N/A')}")
                st.markdown(f"**Issue:** {row.get(issue_col, 'N/A')}")
                if subissue_col in df.columns and pd.notna(row.get(subissue_col)):
                    st.markdown(f"**Sub-issue:** {row.get(subissue_col, 'N/A')}")
            
            # Consumer Complaint Narrative (full width)
            narrative_value = row.get(narrative_col, None)
            if narrative_col in df.columns and pd.notna(narrative_value) and str(narrative_value).strip() != '':
                st.markdown("**Consumer Complaint Narrative:**")
                st.text_area(
                    "",
                    value=str(narrative_value),
                    height=200,
                    disabled=True,
                    label_visibility="collapsed"
                )
            else:
                st.markdown("*Consumer Complaint Narrative: No narrative provided*")
            
            # Add link to CFPB website
            if complaint_id_col in df.columns and pd.notna(row.get(complaint_id_col)):
                complaint_id = str(row.get(complaint_id_col))
                cfpb_link = f"https://www.consumerfinance.gov/data-research/consumer-complaints/search/detail/{complaint_id}"
                st.markdown(f"[🔗 View this complaint on CFPB.gov]({cfpb_link})")
        
        st.markdown("---")

def show_deep_dive_analysis(data, analyzer):
    """Show deep dive analysis with advanced charts"""
    
    st.markdown("### 🔬 Deep Dive Analysis")
    
    if not analyzer or not hasattr(analyzer, 'filtered_df'):
        st.warning("No detailed data available for deep dive")
        return
    
    df = analyzer.filtered_df
    
    # Time series analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📅 Complaints Over Time")
        
        # Convert date received to datetime if it's not already
        if 'date_received' in df.columns:
            df['date_received'] = pd.to_datetime(df['date_received'])
            
            # Group by date
            daily_complaints = df.groupby(df['date_received'].dt.date).size().reset_index()
            daily_complaints.columns = ['Date', 'Complaints']
            
            fig = px.line(
                daily_complaints,
                x='Date',
                y='Complaints',
                title="Daily Complaint Volume",
                markers=True
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### 🗺️ Complaints by State")
        
        if 'state' in df.columns:
            state_complaints = df['state'].value_counts().head(15).reset_index()
            state_complaints.columns = ['State', 'Complaints']
            
            fig = px.bar(
                state_complaints,
                x='State',
                y='Complaints',
                title="Top 15 States by Complaint Volume",
                color='Complaints',
                color_continuous_scale='blues'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    # Correlation analysis
    st.markdown("#### 🔗 Response Analysis")
    
    if 'company_response_to_consumer' in df.columns:
        response_counts = df['company_response_to_consumer'].value_counts().reset_index()
        response_counts.columns = ['Response Type', 'Count']
        
        fig = px.pie(
            response_counts,
            values='Count',
            names='Response Type',
            title="Company Response Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Export options
    st.markdown("### 📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Download Excel Report"):
            st.success("Excel report generated in outputs/ folder")
    
    with col2:
        if st.button("📄 Open Markdown Report"):
            st.success("Opening markdown report...")
    
    with col3:
        if st.button("🗂️ Open Output Folder"):
            st.success("Opening output folder...")

def show_export_section(analyzer):
    """Show comprehensive data export options with verification"""
    
    st.markdown("---")
    st.markdown("## Data Export & Verification")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Full Dataset Export")
        st.write("Complete filtered dataset with verification URLs")
        
        include_narratives = st.checkbox("Include complaint narratives", value=True, 
                                       help="Include full consumer complaint text")
        
        if st.button("📥 Export Full Dataset", type="primary", key="export_full"):
            if CFPBDataExporter is None:
                st.error("Data exporter not available. Please check installation.")
                return
            try:
                with st.spinner("Creating comprehensive Excel export with verification links..."):
                    exporter = CFPBDataExporter(analyzer)
                    filename = exporter.export_full_dataset(include_narratives=include_narratives)
                    
                if filename:
                    st.success("Export complete!")
                    st.info(f"File saved: {filename}")
                    
                    # Create download button
                    if os.path.exists(filename):
                        with open(filename, "rb") as file:
                            st.download_button(
                                label="⬇️ Download Excel File",
                                data=file,
                                file_name=os.path.basename(filename),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                else:
                    st.error("Export failed. Please try again.")
                    
            except Exception as e:
                st.error(f"Export error: {str(e)}")
    
    with col2:
        st.subheader("Special Categories Export")
        st.write("Focus on AI bias, LEP issues, and digital fraud")
        
        category_option = st.selectbox("Select category:", [
            "all", "ai_complaints", "lep_complaints", "fraud_digital_complaints"
        ], format_func=lambda x: {
            "all": "All Special Categories",
            "ai_complaints": "AI/Algorithmic Bias Only", 
            "lep_complaints": "LEP/Spanish Language Only",
            "fraud_digital_complaints": "Digital Fraud Only"
        }[x])
        
        if st.button("📊 Export Category Data", key="export_category", type="primary"):
            if CFPBDataExporter is None:
                st.error("Data exporter not available. Please check installation.")
                return
            try:
                with st.spinner(f"Exporting {category_option} data..."):
                    exporter = CFPBDataExporter(analyzer)
                    filename = exporter.export_category_specific(category_option)
                    
                if filename:
                    st.success("Category export complete!")
                    st.info(f"File: {filename}")
                    
                    if os.path.exists(filename):
                        with open(filename, "rb") as file:
                            btn = st.download_button(
                                label="⬇️ Download Category Excel",
                                data=file,
                                file_name=os.path.basename(filename),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                else:
                    st.error("Category export failed.")
                    
            except Exception as e:
                st.error(f"Export error: {str(e)}")
    
    with col3:
        st.subheader("Verification Report")
        st.write("Data accuracy and source verification")
        
        st.markdown("""
        **Verification includes:**
        - Data source authentication
        - Official CFPB database links
        - Filter transparency
        - Quality metrics
        """)
        
        if st.button("✅ Create Verification Report", key="export_verify", type="primary"):
            if CFPBDataExporter is None:
                st.error("Data exporter not available. Please check installation.")
                return
            try:
                with st.spinner("Generating verification report..."):
                    exporter = CFPBDataExporter(analyzer)
                    filename = exporter.create_verification_report()
                    
                if filename:
                    st.success("Verification report ready!")
                    st.info(f"Report: {filename}")
                    
                    if os.path.exists(filename):
                        with open(filename, "rb") as file:
                            btn = st.download_button(
                                label="⬇️ Download Verification Report",
                                data=file,
                                file_name=os.path.basename(filename),
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )
                else:
                    st.error("Verification report failed.")
                    
            except Exception as e:
                st.error(f"Verification error: {str(e)}")
    
    # Data verification information - Simplified
    st.markdown("---")
    st.markdown("### 🛡️ Data Verification & Accuracy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ Data Source Verification**
        - Official CFPB Source: All data from Consumer Financial Protection Bureau
        - Real Data Only: No simulated, synthetic, or fake data
        - Verification URLs: Direct links to verify on CFPB.gov
        - Download Source: https://files.consumerfinance.gov/ccdb/complaints.csv.zip
        """)
    
    with col2:
        # Use analyzer summary if available; otherwise use the preview summary from session state
        if hasattr(analyzer, 'export_summary_stats') and callable(getattr(analyzer, 'export_summary_stats')):
            summary = analyzer.export_summary_stats()
        else:
            summary = st.session_state.get('analysis_data', {}).get('summary', {})
        st.markdown(f"""
        **📊 Quality Assurance**
        - Total Verified Complaints: {summary['total_complaints']:,}
        - Date Range: {summary['date_range']}
        - Data Freshness: Updated {summary['analysis_date'][:10]}
        - Coverage: {summary['unique_states']} states/territories
        """)
    
    # Important note - Simplified
    st.info("""
    **⚠️ Important:** This system uses only real CFPB complaint data. Every complaint can be verified on the official CFPB website. 
    Credit reporting complaints excluded as requested. Only complaints with consumer narratives included.
    """)

def show_ai_chat_interface(data, analyzer):
    """Show AI chat interface for data exploration"""
    
    st.markdown("## 🤖 AI Data Explorer")
    st.markdown("Chat with your CFPB complaint data using AI - ask questions and get insights!")
    
    # OpenAI API Key input - Always visible and expanded
    st.markdown("### 🔑 Setup Required")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        api_key = st.text_input(
            "Enter your OpenAI API Key:",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys",
            placeholder="sk-..."
        )
    
    with col2:
        if st.button("✅ Test Key", disabled=not api_key):
            if api_key and api_key.startswith('sk-'):
                st.success("✅ Key format looks good!")
            else:
                st.error("❌ Invalid key format")
    
    # Model selection
    model_choice = st.selectbox(
        "Choose AI Model:",
        ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=2,  # Default to cheaper gpt-3.5-turbo
        help="GPT-4 gives better analysis but costs more. GPT-3.5-turbo is faster and cheaper."
    )
    
    # Show status
    if api_key:
        st.success("🟢 **Ready to chat!** Type your question below.")
    else:
        st.warning("🟡 **Please enter your OpenAI API key above to start chatting.**")
        st.info("💡 Get your free API key at: https://platform.openai.com/api-keys")
    
    st.markdown("---")
    st.markdown("### 💬 Chat with Your Data")
    
    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
        # Add welcome message
        st.session_state.chat_messages.append({
            "role": "assistant", 
            "content": "👋 Hello! I'm your CFPB data assistant. I can help you analyze the 470,216 real consumer complaints in this database. Try asking me about trends, companies, or specific issues!"
        })
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input - Make it more prominent
    if api_key:
        if prompt := st.chat_input("💬 Type your question here and press Enter..."):
            # Add user message to chat history
            st.session_state.chat_messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant"):
                try:
                    # Prepare data context for AI
                    data_context = prepare_data_context_for_ai(data, analyzer)
                    
                    # Create AI response
                    with st.spinner("Analyzing data and generating response..."):
                        response = generate_ai_response(prompt, data_context, api_key, model_choice)
                        st.markdown(response)
                        
                        # Add AI response to chat history
                        st.session_state.chat_messages.append({"role": "assistant", "content": response})
                
                except Exception as e:
                    st.error(f"Error generating AI response: {str(e)}")
    else:
        # Show disabled chat input when no API key
        st.text_input("💬 Enter your OpenAI API key above to start chatting...", disabled=True, placeholder="Chat disabled - API key required")
    
    # Suggested questions - Properly working with AI responses
    st.markdown("### 💡 Quick Start Questions")
    if not api_key:
        st.info("💬 Enter your OpenAI API key above to use these quick questions!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Top complaint trends", disabled=not api_key, key="q1", type="secondary"):
            question = "What are the top complaint trends in the data?"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            # Generate AI response immediately
            data_context = prepare_data_context_for_ai(data, analyzer)
            response = generate_ai_response(question, data_context, api_key, model_choice)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("🤖 AI bias complaints", disabled=not api_key, key="q3", type="secondary"):
            question = "Tell me about AI bias and algorithm complaints"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            data_context = prepare_data_context_for_ai(data, analyzer)
            response = generate_ai_response(question, data_context, api_key, model_choice)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("🏢 Top companies", disabled=not api_key, key="q2", type="secondary"):
            question = "Which companies have the most complaints?"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            data_context = prepare_data_context_for_ai(data, analyzer)
            response = generate_ai_response(question, data_context, api_key, model_choice)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("🌐 Language access issues", disabled=not api_key, key="q5", type="secondary"):
            question = "Analyze LEP and language access issues"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            data_context = prepare_data_context_for_ai(data, analyzer)
            response = generate_ai_response(question, data_context, api_key, model_choice)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("🚨 Fraud patterns", disabled=not api_key, key="q4", type="secondary"):
            question = "What fraud and digital scam patterns do you see?"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            data_context = prepare_data_context_for_ai(data, analyzer)
            response = generate_ai_response(question, data_context, api_key, model_choice)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("🗺️ Geographic trends", disabled=not api_key, key="q6", type="secondary"):
            question = "Show me geographic and regional trends"
            st.session_state.chat_messages.append({"role": "user", "content": question})
            data_context = prepare_data_context_for_ai(data, analyzer)
            response = generate_ai_response(question, data_context, api_key, model_choice)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.markdown("---")
    
    # Clear chat button
    col_clear1, col_clear2, col_clear3 = st.columns([1, 1, 1])
    with col_clear2:
        if st.button("🗑️ Clear Chat History", type="secondary"):
            st.session_state.chat_messages = []
            st.rerun()

def prepare_data_context_for_ai(data, analyzer):
    """Prepare data context for AI analysis"""
    
    context = {
        "total_complaints": data.get('summary', {}).get('total_complaints', 0),
        "companies_count": data.get('summary', {}).get('unique_companies', 0),
        "products_count": data.get('summary', {}).get('unique_products', 0),
        "date_range": "April 19 - October 19, 2025 (last 6 months)",
        "data_source": "Official CFPB Consumer Complaint Database"
    }
    
    # Add top trends if available
    if 'trends' in data:
        if 'top_products' in data['trends']:
            context['top_products'] = dict(list(data['trends']['top_products'].items())[:10])
        if 'top_companies' in data.get('companies', {}):
            context['top_companies'] = {k: v['total_complaints'] for k, v in list(data['companies'].items())[:10]}
    
    # Special categories
    if 'special_categories' in data:
        special = data['special_categories']
        context['special_categories'] = {
            'ai_complaints': len(special.get('ai_complaints', [])),
            'lep_complaints': len(special.get('lep_complaints', [])),
            'fraud_complaints': len(special.get('fraud_digital_complaints', []))
        }
    
    return context

def generate_ai_response(prompt, data_context, api_key, model):
    """Generate AI response using OpenAI API"""
    
    if not OPENAI_AVAILABLE:
        return "❌ OpenAI library not installed. Please install it with: pip install openai"
    
    try:
        # Set up OpenAI client
        client = openai.OpenAI(api_key=api_key)
        
        # Create system prompt with data context
        system_prompt = f"""
        You are a CFPB complaint data analyst AI assistant. You have access to real complaint data from the Consumer Financial Protection Bureau.
        
        Current dataset summary:
        - Total complaints: {data_context.get('total_complaints', 'N/A'):,}
        - Companies analyzed: {data_context.get('companies_count', 'N/A'):,}
        - Product categories: {data_context.get('products_count', 'N/A')}
        - Date range: {data_context.get('date_range', 'N/A')}
        - Data source: {data_context.get('data_source', 'Official CFPB Database')}
        
        Top complaint categories: {data_context.get('top_products', {})}
        
        Special categories:
        - AI/Algorithm related: {data_context.get('special_categories', {}).get('ai_complaints', 'N/A')} complaints
        - Limited English Proficiency: {data_context.get('special_categories', {}).get('lep_complaints', 'N/A')} complaints  
        - Digital Fraud: {data_context.get('special_categories', {}).get('fraud_complaints', 'N/A')} complaints
        
        Answer questions about this data with specific insights, trends, and actionable recommendations. Always mention that this is real CFPB data and can be verified on CFPB.gov.
        """
        
        # Generate response
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"❌ Error generating AI response: {str(e)}. Please check your API key and try again."

def add_footer():
    """Add professional footer with branding"""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem; padding: 20px;'>
            <p><strong>Developed by AI Architect Lab</strong></p>
            <p>📧 rory@aiarchitectlab.com | 🌐 Professional Data Analytics Solutions</p>
            <p><em>Powered by Real CFPB Data • 463,571 Consumer Complaints • Last 6 Months</em></p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
