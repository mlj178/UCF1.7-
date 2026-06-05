#include "d3d11_hook.h"
#include "../core/hook_manager.h"
#include "../core/logger.h"
#include "../core/config.h"
#include "../imgui/imgui.h"
#include "../imgui/imgui_impl_dx11.h"
#include "../imgui/imgui_impl_win32.h"
#include "../render/esp_renderer.h"
#include "../render/menu.h"
#include <Windows.h>

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

D3D11Hook::Present_t D3D11Hook::s_OriginalPresent = nullptr;
D3D11Hook::ResizeBuffers_t D3D11Hook::s_OriginalResizeBuffers = nullptr;
ID3D11Device* D3D11Hook::s_Device = nullptr;
ID3D11DeviceContext* D3D11Hook::s_Context = nullptr;
ID3D11RenderTargetView* D3D11Hook::s_RTV = nullptr;
IDXGISwapChain* D3D11Hook::s_SwapChain = nullptr;
HWND D3D11Hook::s_hWnd = nullptr;
bool D3D11Hook::s_Initialized = false;
bool D3D11Hook::s_ImGuiInitialized = false;

D3D11Hook& D3D11Hook::Instance() {
    static D3D11Hook instance;
    return instance;
}

bool D3D11Hook::Initialize() {
    if (s_Initialized) {
        return true;
    }
    
    WNDCLASSEX wc = {0};
    wc.cbSize = sizeof(WNDCLASSEX);
    wc.style = CS_CLASSDC;
    wc.lpfnWndProc = DefWindowProc;
    wc.hInstance = GetModuleHandle(NULL);
    wc.lpszClassName = "D3D11HookTemp";
    RegisterClassEx(&wc);
    
    HWND hWnd = CreateWindow(wc.lpszClassName, "", WS_OVERLAPPEDWINDOW,
                             0, 0, 100, 100, NULL, NULL, wc.hInstance, NULL);
    
    if (!hWnd) {
        LOG_ERROR("D3D11Hook", "Failed to create temp window");
        UnregisterClass(wc.lpszClassName, wc.hInstance);
        return false;
    }
    
    DXGI_SWAP_CHAIN_DESC scDesc = {0};
    scDesc.BufferCount = 2;
    scDesc.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    scDesc.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    scDesc.OutputWindow = hWnd;
    scDesc.SampleDesc.Count = 1;
    scDesc.Windowed = TRUE;
    scDesc.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;
    
    ID3D11Device* pDevice = nullptr;
    ID3D11DeviceContext* pContext = nullptr;
    IDXGISwapChain* pSwapChain = nullptr;
    
    D3D_FEATURE_LEVEL featureLevel = D3D_FEATURE_LEVEL_11_0;
    
    HRESULT hr = D3D11CreateDeviceAndSwapChain(NULL, D3D_DRIVER_TYPE_NULL, NULL, 
                                               0, &featureLevel, 1, D3D11_SDK_VERSION, 
                                               &scDesc, &pSwapChain, &pDevice, NULL, &pContext);
    
    if (FAILED(hr)) {
        LOG_ERROR("D3D11Hook", "NULL driver failed (0x%08X), trying HARDWARE...", hr);
        hr = D3D11CreateDeviceAndSwapChain(NULL, D3D_DRIVER_TYPE_HARDWARE, NULL, 
                                           0, &featureLevel, 1, D3D11_SDK_VERSION, 
                                           &scDesc, &pSwapChain, &pDevice, NULL, &pContext);
    }
    
    if (FAILED(hr)) {
        LOG_ERROR("D3D11Hook", "D3D11CreateDeviceAndSwapChain failed: 0x%08X", hr);
        DestroyWindow(hWnd);
        UnregisterClass(wc.lpszClassName, wc.hInstance);
        return false;
    }
    
    void** pSwapChainVTable = *(void***)pSwapChain;
    void* pPresent = pSwapChainVTable[8];
    void* pResizeBuffers = pSwapChainVTable[13];
    
    LOG("D3D11Hook", "Present address: 0x%p", pPresent);
    LOG("D3D11Hook", "ResizeBuffers address: 0x%p", pResizeBuffers);
    
    if (!HookManager::CreateHook(pPresent, (void*)Present_Hook, (void**)&s_OriginalPresent)) {
        LOG_ERROR("D3D11Hook", "Failed to create Present hook");
        pDevice->Release();
        pContext->Release();
        pSwapChain->Release();
        DestroyWindow(hWnd);
        UnregisterClass(wc.lpszClassName, wc.hInstance);
        return false;
    }
    
    if (!HookManager::CreateHook(pResizeBuffers, (void*)ResizeBuffers_Hook, (void**)&s_OriginalResizeBuffers)) {
        LOG_ERROR("D3D11Hook", "Failed to create ResizeBuffers hook");
        pDevice->Release();
        pContext->Release();
        pSwapChain->Release();
        DestroyWindow(hWnd);
        UnregisterClass(wc.lpszClassName, wc.hInstance);
        return false;
    }
    
    if (!HookManager::EnableHook(pPresent)) {
        LOG_ERROR("D3D11Hook", "Failed to enable Present hook");
        pDevice->Release();
        pContext->Release();
        pSwapChain->Release();
        DestroyWindow(hWnd);
        UnregisterClass(wc.lpszClassName, wc.hInstance);
        return false;
    }
    
    if (!HookManager::EnableHook(pResizeBuffers)) {
        LOG_ERROR("D3D11Hook", "Failed to enable ResizeBuffers hook");
        pDevice->Release();
        pContext->Release();
        pSwapChain->Release();
        DestroyWindow(hWnd);
        UnregisterClass(wc.lpszClassName, wc.hInstance);
        return false;
    }
    
    pDevice->Release();
    pContext->Release();
    pSwapChain->Release();
    DestroyWindow(hWnd);
    UnregisterClass(wc.lpszClassName, wc.hInstance);
    
    s_Initialized = true;
    LOG("D3D11Hook", "Initialized successfully");
    return true;
}

void D3D11Hook::Shutdown() {
    if (!s_Initialized) {
        return;
    }
    
    if (s_RTV) {
        s_RTV->Release();
        s_RTV = nullptr;
    }
    
    if (s_ImGuiInitialized) {
        ImGui_ImplDX11_Shutdown();
        ImGui_ImplWin32_Shutdown();
        ImGui::DestroyContext();
        s_ImGuiInitialized = false;
    }
    
    s_Initialized = false;
    LOG("D3D11Hook", "Shutdown complete");
}

void D3D11Hook::CreateRenderTarget() {
    if (!s_SwapChain || !s_Device) {
        return;
    }
    
    ID3D11Texture2D* pBackBuffer = nullptr;
    if (SUCCEEDED(s_SwapChain->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&pBackBuffer))) {
        s_Device->CreateRenderTargetView(pBackBuffer, NULL, &s_RTV);
        pBackBuffer->Release();
    }
}

void D3D11Hook::CleanupRenderTarget() {
    if (s_RTV) {
        s_RTV->Release();
        s_RTV = nullptr;
    }
}

bool D3D11Hook::InitializeImGui() {
    if (s_ImGuiInitialized) {
        return true;
    }
    
    if (!s_Device || !s_Context || !s_SwapChain) {
        return false;
    }
    
    DXGI_SWAP_CHAIN_DESC desc;
    s_SwapChain->GetDesc(&desc);
    s_hWnd = desc.OutputWindow;
    
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
    
    ImGui::StyleColorsDark();
    
    if (!ImGui_ImplWin32_Init(s_hWnd)) {
        LOG_ERROR("D3D11Hook", "Failed to initialize ImGui Win32");
        return false;
    }
    
    if (!ImGui_ImplDX11_Init(s_Device, s_Context)) {
        LOG_ERROR("D3D11Hook", "Failed to initialize ImGui DX11");
        return false;
    }
    
    s_ImGuiInitialized = true;
    LOG("D3D11Hook", "ImGui initialized");
    return true;
}

void D3D11Hook::RenderFrame() {
    if (!s_ImGuiInitialized) {
        return;
    }
    
    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();
    
    if (Menu::Instance().IsOpen()) {
        Menu::Instance().Render();
    }
    
    if (g_Config.enabled) {
        ESPRenderer::Instance().Render();
    }
    
    ImGui::Render();
    s_Context->OMSetRenderTargets(1, &s_RTV, NULL);
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
}

HRESULT WINAPI D3D11Hook::Present_Hook(IDXGISwapChain* pSwapChain, UINT SyncInterval, UINT Flags) {
    if (!s_Device) {
        s_SwapChain = pSwapChain;
        if (SUCCEEDED(pSwapChain->GetDevice(__uuidof(ID3D11Device), (void**)&s_Device))) {
            s_Device->GetImmediateContext(&s_Context);
            CreateRenderTarget();
            InitializeImGui();
        }
    }
    
    if (GetAsyncKeyState(g_Config.openMenuKey) & 1) {
        Menu::Instance().Toggle();
    }
    
    if (GetAsyncKeyState(g_Config.toggleESPKey) & 1) {
        g_Config.enabled = !g_Config.enabled;
    }
    
    RenderFrame();
    
    return s_OriginalPresent(pSwapChain, SyncInterval, Flags);
}

HRESULT WINAPI D3D11Hook::ResizeBuffers_Hook(IDXGISwapChain* pSwapChain, UINT BufferCount, 
                                             UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags) {
    CleanupRenderTarget();
    
    HRESULT hr = s_OriginalResizeBuffers(pSwapChain, BufferCount, Width, Height, NewFormat, SwapChainFlags);
    
    if (SUCCEEDED(hr)) {
        s_SwapChain = pSwapChain;
        CreateRenderTarget();
        
        if (s_ImGuiInitialized) {
            ImGuiIO& io = ImGui::GetIO();
            io.DisplaySize = ImVec2((float)Width, (float)Height);
        }
    }
    
    return hr;
}
