@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo   编译 Universal-ImGui-Hook.dll
echo   使用 MinGW (GCC)
echo ==========================================
echo.

REM 设置 MinGW 路径
set MINGW_PATH=D:\Program Files\mingw32
set PATH=%MINGW_PATH%\bin;%PATH%

REM 检查 g++ 是否存在
where g++ >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] g++ not found in PATH
    echo Please install MinGW or update MINGW_PATH in this script
    pause
    exit /b 1
)

echo [OK] Found g++:
g++ --version | findstr /C:"g++"
echo.

REM 设置编译参数
set CXXFLAGS=-std=c++17 -O2 -m32 -shared -fpermissive
set DEFINES=-DUNICODE -D_UNICODE -DIMGUI_IMPL_WIN32_DISABLE_GAMEPAD
set INCLUDES=-I. -Iimgui -Iesp -Iminhook/include

REM 库文件
set LIBS=-ld3d9 -ld3d10 -ld3d11 -ld3d12 -ldxgi -ld3dcompiler_47 -ldwmapi -luser32 -lgdi32 -lpsapi
set MINHOOK_LIB=minhook/lib/libMinHook.a

REM 源文件
set SOURCES=^
    dllmain.cpp ^
    globals.cpp ^
    hooks.cpp ^
    d3d9hook.cpp ^
    d3d10hook.cpp ^
    d3d11hook.cpp ^
    d3d12hook.cpp ^
    inputhooks.cpp ^
    mousehooks.cpp ^
    menu.cpp ^
    imgui/imgui.cpp ^
    imgui/imgui_demo.cpp ^
    imgui/imgui_draw.cpp ^
    imgui/imgui_tables.cpp ^
    imgui/imgui_widgets.cpp ^
    imgui/imgui_impl_dx9.cpp ^
    imgui/imgui_impl_dx10.cpp ^
    imgui/imgui_impl_dx11.cpp ^
    imgui/imgui_impl_dx12.cpp ^
    imgui/imgui_impl_win32.cpp ^
    esp/il2cpp_bridge.cpp ^
    esp/game_manager.cpp ^
    esp/transform_helper.cpp ^
    esp/coord_converter.cpp ^
    esp/esp_renderer.cpp

REM 输出目录
set OUT_DIR=Release
if not exist %OUT_DIR% mkdir %OUT_DIR%

echo [INFO] Compiling...
echo.

REM 编译
g++ %CXXFLAGS% %DEFINES% %INCLUDES% %SOURCES% %MINHOOK_LIB% -o %OUT_DIR%/Universal-ImGui-Hook.dll %LIBS% 2>&1

if %ERRORLEVEL% equ 0 (
    echo.
    echo ==========================================
    echo   [SUCCESS] Build completed!
    echo ==========================================
    echo   Output: %OUT_DIR%\Universal-ImGui-Hook.dll
    for %%F in (%OUT_DIR%\Universal-ImGui-Hook.dll) do echo   Size: %%~zF bytes
    echo ==========================================
) else (
    echo.
    echo ==========================================
    echo   [FAILED] Build failed!
    echo ==========================================
    echo   Please check the error messages above
    echo ==========================================
)

pause
