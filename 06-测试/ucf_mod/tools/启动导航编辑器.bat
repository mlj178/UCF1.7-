@echo off
setlocal
chcp 936 >nul 2>nul
title UCF 导航编辑器（浏览器版）
cd /d "%~dp0"
set "QS="
echo %* | find /i "-q" >nul 2>nul && set "QS=1"
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe")
if not defined PY (if exist "C:\Python312\python.exe" set "PY=C:\Python312\python.exe")
if not defined PY goto nopython

echo ================================================================
echo  导航编辑器   编辑的是 ② 开发版 navdata\dev
echo ================================================================

rem 三版：native（只读备份）/ dev（开发，编辑器编这一版）/ deploy（游戏目录）
set "UCF_PROFILE=dev"

if exist "..\geo\web" goto serve
echo [1/2] 第一次运行：生成 3D 地形网格（要 numpy；失败也能进编辑器，只是 3D 没地形）
%PY% geo2web.py
:serve
echo [2/2] 启动本地服务，浏览器会自动打开编辑器…
echo        （关掉这个窗口 = 停止服务；编辑结果写进 ..\navdata\dev\nav）
echo.
%PY% -u navserver.py %*
set "RC=%ERRORLEVEL%"
echo.
if "%RC%"=="0" goto bye
echo [已退出] navserver 退出码 %RC%（端口被占用等情况会看到这行）
echo          日志文件：..\navdata\_logs\navdata.log
:bye
echo 服务已停止。
call :wait
exit /b %RC%

echo.
echo [失败] 没找到 Python 3。请装 Python 3.10+（安装时勾 Add python.exe to PATH）。
echo        或用记事本打开这个 bat，把 PY 改成你自己的 python.exe 完整路径。
echo.
call :wait
exit /b 1

:wait
if not defined QS pause
exit /b 0
