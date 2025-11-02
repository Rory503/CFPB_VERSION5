@echo off
echo ========================================
echo  RESTARTING CFPB Analysis Dashboard
echo ========================================
echo.
echo Step 1: Stopping any running Streamlit processes...
taskkill /F /IM streamlit.exe 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq streamlit*" 2>nul
timeout /t 2 /nobreak >nul
echo Done!
echo.
echo Step 2: Starting fresh Streamlit app...
echo.
echo The dashboard will open in your browser in a few seconds...
echo.
echo ========================================
echo  Dashboard is loading...
echo  Press Ctrl+C to stop the server
echo ========================================
echo.
streamlit run web_dashboard.py
pause

