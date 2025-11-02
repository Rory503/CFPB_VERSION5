@echo off
echo ========================================
echo  Push Fixed Code to GitHub
echo ========================================
echo.
echo This will commit and push your changes to GitHub,
echo which will automatically deploy to Render/Streamlit Cloud!
echo.
echo ========================================
echo.

cd /d "%~dp0"

echo Step 1: Checking git status...
echo.
git status
echo.
echo ========================================
echo.
echo Step 2: Adding all changed files...
git add .
echo Done!
echo.
echo ========================================
echo.
echo Step 3: Committing changes...
git commit -m "MAJOR SIMPLIFICATION: Removed all confusing options - ONE button always downloads fresh CFPB data. Fixed syntax errors. No more Quick/Upload options."
echo.
echo ========================================
echo.
echo Step 4: Pushing to GitHub...
git push origin main
echo.
echo ========================================
echo.
echo  SUCCESS! Changes pushed to GitHub!
echo ========================================
echo.
echo Your changes are now on GitHub.
echo.
echo If you have auto-deploy enabled on Render or Streamlit Cloud:
echo   - They will automatically detect this push
echo   - Redeploy with the new code
echo   - Should be live in 2-5 minutes!
echo.
echo Check your deployment dashboard to monitor progress.
echo.
echo ========================================
pause

