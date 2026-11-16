@echo off
title UCF 导航编辑器（浏览器版）
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe")
if not defined PY (if exist "C:\Python312\python.exe" set "PY=C:\Python312\python.exe")
if not defined PY goto nopython

if not exist "..\geo\web" (
  echo [1/2] 第一次运行：生成 3D 地形网格（要 numpy，失败也能进编辑器，只是 3D 没有地形）
  %PY% geo2web.py
)

echo [2/2] 启动本地服务，浏览器会自动打开编辑器…
%PY% -u navserver.py %*

echo.
echo 服务已停止（关掉这个窗口即可）。
pause
exit /b 0

:nopython
echo 找不到 Python 3。
echo 请安装 Python 3.10 或更高版本，安装时勾选 Add python.exe to PATH；
echo 或者用记事本打开这个 bat，把 PY 改成你自己的 python.exe 路径。
pause
exit /b 1
