#pragma once
#include <d3d11.h>
#include <dxgi.h>

class D3D11Hook {
public:
    static D3D11Hook& Instance();
    
    bool Initialize();
    void Shutdown();
    
private:
    D3D11Hook() = default;
    ~D3D11Hook() = default;
    
    static HRESULT WINAPI Present_Hook(IDXGISwapChain* pSwapChain, UINT SyncInterval, UINT Flags);
    static HRESULT WINAPI ResizeBuffers_Hook(IDXGISwapChain* pSwapChain, UINT BufferCount, 
                                             UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags);
    
    typedef HRESULT (WINAPI *Present_t)(IDXGISwapChain*, UINT, UINT);
    typedef HRESULT (WINAPI *ResizeBuffers_t)(IDXGISwapChain*, UINT, UINT, UINT, DXGI_FORMAT, UINT);
    
    static Present_t s_OriginalPresent;
    static ResizeBuffers_t s_OriginalResizeBuffers;
    
    static ID3D11Device* s_Device;
    static ID3D11DeviceContext* s_Context;
    static ID3D11RenderTargetView* s_RTV;
    static IDXGISwapChain* s_SwapChain;
    static HWND s_hWnd;
    static bool s_Initialized;
    static bool s_ImGuiInitialized;
    
    static void CreateRenderTarget();
    static void CleanupRenderTarget();
    static bool InitializeImGui();
    static void RenderFrame();
};
