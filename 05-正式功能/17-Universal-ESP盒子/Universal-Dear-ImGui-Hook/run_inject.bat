@echo off
title DLL Injector
echo ==========================================
echo   UnityCrossFire DLL Injector
echo ==========================================
echo.
echo Starting injector...
echo.
cd /d "%~dp0"
inject.exe
echo.
echo Press any key to exit...
pause >nul
