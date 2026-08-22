@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AISingers Studio - Setup
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0windows\install.ps1"
set "AIS_EXIT=%ERRORLEVEL%"
echo.
pause
exit /b %AIS_EXIT%
