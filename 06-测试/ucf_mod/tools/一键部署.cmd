@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

rem UCF mod one-click deploy
rem   double-click  : pick UnityCrossFire.exe in a dialog
rem   drag-drop exe : deploy to that game folder

set "PY=python"
where %PY% >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python not found in PATH.
  echo         Install Python 3.10+ or run deploy_mod.py manually.
  pause
  exit /b 1
)

if "%~1"=="" goto pick
"%PY%" "deploy_mod.py" --game-exe "%~1" %2 %3 %4 %5 %6
goto done

:pick
"%PY%" "deploy_mod.py" --pick

:done
set RC=%ERRORLEVEL%
echo.
echo [exit code: %RC%]
pause
exit /b %RC%
