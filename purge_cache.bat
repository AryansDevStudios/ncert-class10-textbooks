@echo off
title Purge NCERT CDN Cache
echo ====================================================
echo      NCERT PDF - Purge jsDelivr Global CDN Cache
echo ====================================================
echo.
cd /d "%~dp0"

python purge_cache.py %*

echo.
pause
