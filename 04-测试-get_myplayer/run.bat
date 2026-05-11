@echo off
chcp 65001 >nul
title 获取玩家对象地址

echo ========================================
echo   获取玩家对象地址 - 启动器
echo ========================================
echo.

cd /d "%~dp0"

echo [*] 启动 Python UI...
python launcher.py

pause
