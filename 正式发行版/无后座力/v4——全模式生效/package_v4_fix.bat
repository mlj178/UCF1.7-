@echo off
chcp 65001 >nul
title Package No Recoil V4 Fix Launcher

echo.
echo ==========================================
echo    Package No Recoil V4 Fix Launcher
echo    (All Modes Support)
echo ==========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Step 1: Checking Python... OK

echo.
echo Step 2: Checking frida-tools...
python -c "import frida" >nul 2>&1
if errorlevel 1 (
    echo Installing frida-tools...
    pip install frida-tools -i https://pypi.tuna.tsinghua.edu.cn/simple
) else (
    echo frida-tools OK
)

echo.
echo Step 3: Installing PyInstaller...
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo Step 4: Packaging...
echo This may take 1-2 minutes...
echo.

pyinstaller --onefile --add-data "no_recoil_v4_fix.js;." --hidden-import=frida.core --name "NoRecoil_V4_Fix" launcher_v4_fix.py

echo.
echo ==========================================
if exist "dist\NoRecoil_V4_Fix.exe" (
    echo SUCCESS - Packaging Complete!
    echo.
    echo Output file: dist\NoRecoil_V4_Fix.exe
    echo.
    echo Instructions:
    echo 1. Send this EXE to your friend
    echo 2. Friend starts the game first
    echo 3. Friend double-clicks NoRecoil_V4_Fix.exe
    echo 4. No Recoil activated!
    echo.
    echo Features:
    echo - All game modes support
    echo - Auto room change detection
    echo - Zero performance impact
    echo - Direct field zeroing
    echo.
    echo Note:
    echo - File size: ~50-60MB (normal, includes Frida)
    echo - No Python/Frida installation needed
    echo - Works on any Windows PC
    echo ==========================================
    pause
    exit /b 0
) else (
    echo ERROR - Packaging failed
    echo Please check error messages above
    echo ==========================================
    pause
    exit /b 1
)
