@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AISingers Studio - Diagnostics
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0windows\diagnose.ps1"
set "AIS_EXIT=%ERRORLEVEL%"
echo.
pause
exit /b %AIS_EXIT%
