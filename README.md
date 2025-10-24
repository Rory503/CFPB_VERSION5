# 🏛️ CFPB Consumer Complaint Analysis Tool v5.0

**Specialized for FinTech Innovation, Regulatory Compliance, and Consumer Protection Insights**

A comprehensive Python-based analysis tool for the CFPB Consumer Complaint Database, designed for financial technology companies, regulatory professionals, and consumer protection advocates.

## 🎯 Key Features

- **📊 Smart Filtering**: Last 6 months analysis with narrative-only complaints, excluding credit reporting noise
- **🤖 AI Detection**: Identifies AI/algorithmic bias complaints in financial services  
- **🌐 LEP Analysis**: Tracks Limited English Proficiency and Spanish language access issues
- **🚨 Fraud Monitoring**: Detects digital banking fraud and emerging scam patterns
- **🔄 FTC Triangulation**: Cross-validates trends with FTC Consumer Sentinel data
- **📈 Interactive Dashboards**: Beautiful visualizations with complaint links for deep-dive analysis
- **⚡ Automated Reports**: Generates comprehensive markdown reports and structured data exports

## 🚀 Quick Start

### Option 1: GUI Interface (Recommended) 🖥️

1. **Windows**: Double-click `start_gui.bat`
2. **Or run**: `python gui_app.py`
3. **Use the interface to**:
   - View system information and project status
   - Run analysis with one-click execution
   - Monitor progress in real-time
   - View results in organized tabs
   - Export reports with GUI buttons

### Option 2: Command Line Interface 💻

#### 1. Setup

```bash
# Clone or download the project
cd cfpb_version5

# Install dependencies
pip install -r requirements.txt
```

#### 2. Run Analysis

```bash
# Automatic data download and analysis
python real_main_analysis.py
```

**No manual data download needed!** The system automatically:
- Downloads latest CFPB complaint data
- Applies all filters (6 months, narratives only, etc.)
- Excludes credit reporting noise
- Generates comprehensive reports

## 📁 Project Structure

```
cfpb_version5/
├── analysis/
│   ├── cfpb_analyzer.py      # Core data processing engine
│   ├── visualizer.py         # Visualization dashboard generator  
│   └── ftc_triangulator.py   # FTC data cross-validation
├── data/                     # Place CSV files here
├── outputs/                  # Generated reports (.md, .json)
├── visualizations/           # Charts and interactive dashboards
├── main_analysis.py          # Main execution script
├── download_data.py          # Script to download latest complaint data
└── requirements.txt          # Python dependencies
```

## 📊 Analysis Focus Areas

### Core Filters Applied

- **Date Range**: Last 6 months (April 19, 2025 – October 19, 2025)
- **Narrative Required**: Only complaints with consumer stories
- **Credit Exclusion**: Removes noisy credit reporting categories
- **Company Focus**: Excludes credit agencies (Equifax, Experian, TransUnion)

### Special Category Detection

**🤖 AI & Algorithmic Complaints**
- Keywords: AI, algorithm, automated decision, chatbot, model, bias
- Use Case: Identify algorithmic bias in lending, unfair automated decisions

**🌐 LEP/Spanish Language Issues**  
- Keywords: Spanish, translation, language barrier, interpreter, bilingual
- Use Case: Track language access gaps in financial services

**🚨 Fraud & Digital Banking**
- Keywords: fraud, scam, Zelle, digital wallet, phishing, unauthorized
- Use Case: Monitor emerging digital fraud patterns and security gaps

## �️ GUI Features

### 📊 System Overview Tab
- Real-time project status and file structure
- Data source verification
- Analysis specifications summary
- Quick access to CFPB website and project folders

### 🔥 Run Analysis Tab  
- One-click analysis execution
- Real-time progress monitoring
- Live analysis logs and output
- Configurable options (FTC triangulation, Excel export)

### 📈 View Results Tab
- Interactive results summary
- Quick access to generated reports
- One-click report opening (Markdown, Excel)
- Detailed findings browser

### ⚙️ Settings & Export Tab
- File location management
- Analysis parameters display
- Export options and report generation
- Direct folder access buttons

## �📈 Generated Outputs

### Reports
- **`cfpb_real_analysis_report.md`** - Comprehensive markdown report with clickable complaint links
- **`cfpb_real_analysis.xlsx`** - Excel export with multiple sheets and analysis data
- **`cfpb_ftc_triangulation_report.md`** - FTC cross-validation findings

### Interactive Visualizations
- **`cfpb_analysis_dashboard.html`** - Main interactive dashboard
- **`cfpb_analysis_companies.html`** - Company ranking with drill-down
- **`cfpb_analysis_heatmap.png`** - Product vs Issue category heatmap
- **`cfpb_analysis_special_categories.png`** - AI, LEP, fraud analysis charts
- **`cfpb_analysis_wordcloud.png`** - Consumer narrative word cloud

## 🎯 Use Cases

### For FinTech Companies
- **Product Risk Assessment**: Identify complaint patterns before product launch
- **Competitive Intelligence**: Analyze competitor complaint trends
- **Regulatory Preparation**: Anticipate CFPB enforcement priorities

### For Regulatory Professionals  
- **Trend Monitoring**: Track emerging consumer protection issues
- **Enforcement Targeting**: Identify high-risk companies and practices
- **Policy Development**: Use data to inform regulatory guidance

### For Consumer Advocates
- **Pattern Recognition**: Spot systemic issues across financial services
- **Company Accountability**: Access complaint details with direct links
- **Advocacy Planning**: Use trends to prioritize consumer protection efforts

## 📋 Example Output Preview

```markdown
# CFPB Consumer Complaint Analysis Report

## Executive Summary
| Metric | Value |
|--------|-------|
| **Total Non-Credit Complaints** | 247,856 |
| **Unique Companies** | 3,247 |
| **Avg. Daily Complaints** | 1,348.4 |

## Top Complaint Trends
| Rank | Product Category | Complaints | % of Total |
|------|------------------|------------|------------|
| 1 | Debt collection | 52,341 | 21.1% |
| 2 | Checking or savings account | 38,429 | 15.5% |
| 3 | Credit card or prepaid card | 31,287 | 12.6% |

## Special Categories
- **AI-Related Complaints**: 1,247 (0.5% of total)
- **LEP/Spanish Issues**: 3,891 (1.6% of total)  
- **Fraud/Digital**: 18,234 (7.4% of total)
```

## 🔧 Advanced Usage

### Custom Analysis

```python
from analysis.cfpb_analyzer import CFPBAnalyzer

# Initialize analyzer
analyzer = CFPBAnalyzer()

# Load and filter data
analyzer.load_and_filter_data('data/complaints.csv')

# Get specific product analysis  
debt_trends = analyzer.get_sub_trends('Debt collection')

# Analyze special categories
special = analyzer.analyze_special_categories()
ai_complaints = special['ai_complaints']
```

### Custom Visualizations

```python
from analysis.visualizer import CFPBVisualizer

# Create visualizer
viz = CFPBVisualizer(analyzer)

# Generate custom charts
company_chart = viz.create_company_ranking_chart(companies, top_n=15)
special_chart = viz.create_special_category_charts(special_categories)
```

### FTC Triangulation

```python
from analysis.ftc_triangulator import FTCTriangulator

# Initialize triangulator
triangulator = FTCTriangulator(analyzer)

# Load FTC data
triangulator.load_ftc_data('data/ftc_data.csv')

# Compare trends
comparison = triangulator.compare_trends()
fraud_analysis = triangulator.analyze_fraud_trends()
```

## 🔍 Key Insights Generated

### Regulatory Risk Indicators
- Algorithmic bias patterns in lending decisions
- Language access gaps in mortgage servicing
- Digital fraud vulnerability in payment apps
- Debt collection practice violations

### Market Intelligence
- Competitor complaint volumes and trending issues
- Product category growth/decline patterns  
- Geographic concentration of specific complaints
- Seasonal trends in financial service complaints

### Consumer Protection Priorities
- Emerging scam patterns requiring public awareness
- Systemic issues affecting multiple companies
- Vulnerable population targeting (elderly, LEP, etc.)
- Technology gaps creating consumer harm

## 📞 Support & Enhancement

This tool is designed to be:
- **Extensible**: Add new keyword filters or analysis modules
- **Automated**: Schedule regular analysis runs  
- **Scalable**: Handle growing complaint databases efficiently
- **Customizable**: Adapt filters and outputs for specific needs

### Potential Enhancements
- Real-time CFPB API integration
- Machine learning complaint classification
- Sentiment analysis of consumer narratives
- Geographic mapping of complaint patterns
- Integration with other regulatory databases

## 📄 License & Usage

This tool is designed for legitimate consumer protection, regulatory compliance, and financial industry analysis purposes. Please ensure compliance with:

- CFPB data usage guidelines
- Consumer privacy protection standards  
- Appropriate use of complaint narrative data
- Professional and ethical analysis practices

---

**Built for:** Financial technology professionals, regulatory experts, and consumer protection advocates working to improve financial services through data-driven insights.

**Version:** 5.0 - Optimized for 2025 regulatory environment and emerging FinTech challenges

# CFPB Dashboard

## How to use

1. Clone the repo.
2. Download the latest complaint data from the CFPB site:
   - https://www.consumerfinance.gov/data-research/consumer-complaints/search/
   - Click "Download all complaint data | CSV"
3. Place the CSV file in the `data/` folder as `complaints.csv`.
4. Run the app as usual.

## Optional: Auto-download script
You can also run `python download_data.py` to fetch the latest data automatically (requires internet access).#   C F P D _ N e w 1  
 