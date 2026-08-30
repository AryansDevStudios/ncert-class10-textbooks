@echo off
title Deploy NCERT PDF to Firebase
echo ====================================================
echo      Deploying NCERT PDF to Firebase Hosting
echo ====================================================
echo.
cd /d "%~dp0"

echo Running Firebase Deploy...
call firebase deploy --only hosting:ncertbook
if %errorlevel% neq 0 (
    echo.
    echo [!] Authentication needed. Opening browser to login...
    call firebase login
    echo.
    echo [*] Retrying deployment...
    call firebase deploy --only hosting:ncertbook
)

echo.
echo ====================================================
echo Deployment complete!
echo Live URL: https://ncertbook.web.app
echo ====================================================
pause
