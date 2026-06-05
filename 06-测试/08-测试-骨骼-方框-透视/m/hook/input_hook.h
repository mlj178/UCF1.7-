#pragma once
#include <Windows.h>

class InputHook {
public:
    static InputHook& Instance();
    
    bool Initialize(HWND hWnd);
    void Shutdown();
    
private:
    InputHook() = default;
    ~InputHook() = default;
    
    static WNDPROC s_OriginalWndProc;
    static HWND s_hWnd;
    
    static LRESULT WINAPI WndProc_Hook(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
};
