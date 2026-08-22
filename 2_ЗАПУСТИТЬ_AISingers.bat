@echo off
chcp 65001 >nul
cd /d "%~dp0"
title AISingers Studio
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0windows\launch.ps1"
set "AIS_EXIT=%ERRORLEVEL%"
if not "%AIS_EXIT%"=="0" (
  echo.
  pause
)
exit /b %AIS_EXIT%
