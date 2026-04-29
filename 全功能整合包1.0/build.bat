@echo off
chcp 65001 >nul
echo ========================================
echo 游戏修改器控制台 - 打包工具
echo ========================================
echo.

echo [1/3] 安装依赖...
pip install customtkinter frida psutil pyinstaller

echo.
echo [2/3] 开始打包...
pyinstaller --onefile --windowed ^
  --name "游戏修改器控制台" ^
  --icon=NONE ^
  --add-data "game_modifier.py;." ^
  --hidden-import=customtkinter ^
  --hidden-import=frida ^
  --hidden-import=psutil ^
  game_modifier.py

echo.
echo [3/3] 打包完成！
echo 输出目录: dist\游戏修改器控制台.exe
echo.
pause
