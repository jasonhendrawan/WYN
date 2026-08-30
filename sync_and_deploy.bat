@echo off
title WYN - Sync Google Drive & Deploy
cd /d "%~dp0"

echo =======================================================
echo    WYN - Automated Google Drive Sync ^& Deploy
echo =======================================================
echo.

echo [1/2] Scanning Google Drive for new folders/photos...
python scripts/sync_gdrive.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Sync script failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/2] Deploying to Cloudflare Pages...
call npx --yes wrangler pages deploy dist --project-name jhcwch
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Deployment failed!
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo =======================================================
echo    SUCCESS! Site updated live at https://jhcwch.pages.dev
echo =======================================================
echo.
pause
