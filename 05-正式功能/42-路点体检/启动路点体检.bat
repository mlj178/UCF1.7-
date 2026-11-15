@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 goto nopython

python "AAAAA-waypoint_probe_ui.py"
if errorlevel 1 goto failed
exit /b 0

:nopython
echo.
echo [ERROR] python.exe not found in PATH.
echo Install Python 3 and: pip install customtkinter frida psutil
pause
exit /b 1

:failed
echo.
echo [ERROR] launch failed - see the message above.
pause
exit /b 1
