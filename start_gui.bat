@echo off
title CFPB Analysis Tool - GUI Launcher
echo.
echo 🏛️ CFPB Consumer Complaint Analysis Tool
echo ==================================================
echo Starting GUI interface...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install requirements if needed
if exist requirements.txt (
    echo 📦 Checking dependencies...
    pip install -r requirements.txt >nul 2>&1
)

REM Launch GUI
python gui_app.py

pause