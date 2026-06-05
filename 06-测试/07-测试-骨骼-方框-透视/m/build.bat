@echo off
setlocal

set "GPP=D:\Program Files\mingw32\bin\g++.exe"
if not exist "%GPP%" (
    echo [ERROR] MinGW g++ not found at %GPP%
    echo [INFO] Searching for g++...
    where g++
    exit /b 1
)

echo [*] Building m.dll (ImGui + D3D11 Present Hook + ESP)...
echo [*] Using compiler: %GPP%

"%GPP%" -m32 -O2 -shared -o m.dll ^
    m.cpp ^
    esp/il2cpp_bridge.cpp ^
    esp/game_manager.cpp ^
    esp/transform_helper.cpp ^
    esp/coord_converter.cpp ^
    esp/esp_renderer.cpp ^
    imgui/imgui.cpp ^
    imgui/imgui_draw.cpp ^
    imgui/imgui_tables.cpp ^
    imgui/imgui_widgets.cpp ^
    imgui/imgui_demo.cpp ^
    imgui/imgui_impl_dx11.cpp ^
    imgui/imgui_impl_win32.cpp ^
    -Iimgui -Iesp ^
    -ld3d11 -ldxgi -ld3dcompiler -luser32 -lkernel32 -lgdi32 -limm32 -ldwmapi

if %ERRORLEVEL% neq 0 (
    echo [FAIL] Compilation failed!
    exit /b 1
)

echo [OK] m.dll built successfully!
dir m.dll
exit /b 0
