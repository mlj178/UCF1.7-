@echo off
setlocal

echo [*] Building m.dll with MSVC (ImGui + D3D11 Present Hook + ESP)...

cl /LD /MT /O2 /EHsc ^
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
    /I"imgui" /I"esp" ^
    /Fe:m.dll ^
    /link d3d11.lib dxgi.lib user32.lib gdi32.lib

if %ERRORLEVEL% neq 0 (
    echo [FAIL] Compilation failed!
    exit /b 1
)

echo [OK] m.dll built successfully!
exit /b 0
