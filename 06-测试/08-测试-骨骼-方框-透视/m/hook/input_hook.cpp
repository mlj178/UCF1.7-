#include "input_hook.h"
#include "../imgui/imgui.h"
#include "../imgui/imgui_impl_win32.h"
#include "../render/menu.h"
#include <Windows.h>

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

WNDPROC InputHook::s_OriginalWndProc = nullptr;
HWND InputHook::s_hWnd = nullptr;

InputHook& InputHook::Instance() {
    static InputHook instance;
    return instance;
}

bool InputHook::Initialize(HWND hWnd) {
    if (!hWnd) {
        return false;
    }
    
    s_hWnd = hWnd;
    s_OriginalWndProc = (WNDPROC)SetWindowLongPtr(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc_Hook);
    
    if (!s_OriginalWndProc) {
        return false;
    }
    
    return true;
}

void InputHook::Shutdown() {
    if (s_hWnd && s_OriginalWndProc) {
        SetWindowLongPtr(s_hWnd, GWLP_WNDPROC, (LONG_PTR)s_OriginalWndProc);
        s_OriginalWndProc = nullptr;
        s_hWnd = nullptr;
    }
}

LRESULT WINAPI InputHook::WndProc_Hook(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam) {
    if (Menu::Instance().IsOpen()) {
        if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam)) {
            return true;
        }
    }
    
    return CallWindowProc(s_OriginalWndProc, hWnd, msg, wParam, lParam);
}
