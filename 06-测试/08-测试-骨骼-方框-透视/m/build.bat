@echo off
setlocal

set "GPP=D:\Program Files\mingw32\bin\g++.exe"
if not exist "%GPP%" (
    echo [ERROR] MinGW g++ not found at %GPP%
    exit /b 1
)

echo [*] Building m.dll (MinHook + ImGui + D3D11 Hook + IL2CPP + ESP)...
echo [*] Using compiler: %GPP%

"%GPP%" -m32 -O2 -shared -static-libgcc -static-libstdc++ -o m.dll ^
    m.cpp ^
    core/hook_manager.cpp ^
    core/logger.cpp ^
    core/config.cpp ^
    hook/d3d11_hook.cpp ^
    hook/input_hook.cpp ^
    il2cpp/il2cpp_api.cpp ^
    game/player.cpp ^
    game/game_manager.cpp ^
    game/coord_converter.cpp ^
    render/esp_renderer.cpp ^
    render/menu.cpp ^
    imgui/imgui.cpp ^
    imgui/imgui_draw.cpp ^
    imgui/imgui_tables.cpp ^
    imgui/imgui_widgets.cpp ^
    imgui/imgui_demo.cpp ^
    imgui/imgui_impl_dx11.cpp ^
    imgui/imgui_impl_win32.cpp ^
    minhook/hook.c ^
    minhook/trampoline.c ^
    minhook/buffer.c ^
    minhook/hde32.c ^
    -Icore -Ihook -Iil2cpp -Igame -Irender -Iimgui -Iminhook ^
    -ld3d11 -ldxgi -ld3dcompiler -luser32 -lkernel32 -lgdi32 -limm32 -ldwmapi

if %ERRORLEVEL% neq 0 (
    echo [FAIL] Compilation failed!
    exit /b 1
)

echo [OK] m.dll built successfully!
dir m.dll
exit /b 0
