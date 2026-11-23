@echo off
title UCF 控制台
cd /d "%~dp0"

set "PYW="
where pythonw >nul 2>nul && set "PYW=pythonw"
if not defined PYW (where py >nul 2>nul && set "PYW=py -3w")
if not defined PYW (if exist "%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe" set "PYW=%LOCALAPPDATA%\Programs\Python\Python312\pythonw.exe")
if not defined PYW (if exist "C:\Python312\pythonw.exe" set "PYW=C:\Python312\pythonw.exe")
if not defined PYW goto nopython

start "" %PYW% "控制台.pyw"
exit /b 0

:nopython
echo 找不到 Python 3。
echo 请安装 Python 3.10 或更高版本（安装时勾选 Add python.exe to PATH），
echo 或者用记事本打开这个 bat，把 PYW 改成你自己的 pythonw.exe 路径。
pause
exit /b 1
