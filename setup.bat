@echo off
echo 🏛️  CFPB Consumer Complaint Analysis Tool v5.0 Setup
echo ====================================================
echo.

echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Error installing dependencies. Please check your Python installation.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencies installed successfully!
echo.

echo 📁 Creating necessary directories...
if not exist "data" mkdir data
if not exist "outputs" mkdir outputs  
if not exist "visualizations" mkdir visualizations

echo.
echo 🎭 Running demo to show expected output format...
python demo.py

echo.
echo 📋 Next Steps:
echo ============
echo.
echo 1. Download CFPB complaint data:
echo    Visit: https://www.consumerfinance.gov/data-research/consumer-complaints/#download-the-data
echo    Save as: data\complaints.csv
echo.
echo 2. (Optional) Download FTC Consumer Sentinel data:
echo    Visit: https://www.ftc.gov/exploredata
echo    Save as: data\ftc_data.csv
echo.
echo 3. Run full analysis:
echo    python main_analysis.py
echo.
echo 4. View results:
echo    - Open outputs\cfpb_analysis_report.md for detailed findings
echo    - Open visualizations\cfpb_analysis_dashboard.html for interactive charts
echo.

echo 🎉 Setup complete! Ready for CFPB complaint analysis.
pause