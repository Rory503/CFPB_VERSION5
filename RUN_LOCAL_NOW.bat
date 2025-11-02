@echo off
COLOR 0A
cls
echo.
echo  ============================================================
echo                 RUNNING LOCAL VERSION
echo  ============================================================
echo.
echo  This will use YOUR local data files (453,624 complaints)
echo  NOT the cloud version!
echo.
echo  ============================================================
echo.
echo  Stopping any old processes...
taskkill /F /IM streamlit.exe 2>nul
timeout /t 2 /nobreak >nul

echo  Starting local dashboard...
echo.
echo  ============================================================
echo   IMPORTANT: Use this URL in your browser:
echo   
echo   http://localhost:8501
echo   
echo   NOT the cfpb-consumer-complaints-dashboard.onrender.com URL!
echo  ============================================================
echo.
echo  Keep this window open!
echo.

cd /d "%~dp0"
streamlit run web_dashboard.py --server.port 8501

pause

