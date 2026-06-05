#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <d3d11.h>
#include <dxgi.h>
#include <stdio.h>

#include "imgui/imgui.h"
#include "imgui/imgui_impl_dx11.h"
#include "imgui/imgui_impl_win32.h"

#include "esp/esp_config.h"
#include "esp/il2cpp_bridge.h"
#include "esp/game_manager.h"
#include "esp/transform_helper.h"
#include "esp/coord_converter.h"
#include "esp/esp_renderer.h"

extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

typedef HRESULT(__stdcall* PresentFn)(IDXGISwapChain*, UINT, UINT);
static PresentFn g_RealPresent   = NULL;
static DWORD     g_PresentAddress = 0;
static int       g_HookLen        = 0;
static BYTE      g_SavedBytes[16] = {0};
static BYTE*     g_Trampoline     = NULL;

static ID3D11Device*           g_pDevice  = NULL;
static ID3D11DeviceContext*    g_pContext = NULL;
static ID3D11RenderTargetView* g_pRTV    = NULL;
static WNDPROC                 g_OrigWndProc = NULL;
static HWND                    g_hWnd    = NULL;

static volatile bool g_ImGuiInit = false;
static volatile bool g_Shutdown  = false;
static volatile LONG g_FrameCount = 0;
static volatile bool g_ESPInitialized = false;
static volatile bool g_ESPInitAttempted = false;

static char  g_LogPath[MAX_PATH] = {0};
static CRITICAL_SECTION g_LogCS;

extern "C" void dbg(const char* fmt, ...) {
    char buf[512];
    va_list va;
    va_start(va, fmt);
    wvsprintfA(buf, fmt, va);
    va_end(va);

    if (g_LogPath[0]) {
        EnterCriticalSection(&g_LogCS);
        FILE* f = fopen(g_LogPath, "a");
        if (f) {
            SYSTEMTIME st;
            GetLocalTime(&st);
            fprintf(f, "[%02d:%02d:%02d.%03d] [ESP] %s\n",
                st.wHour, st.wMinute, st.wSecond, st.wMilliseconds, buf);
            fflush(f);
            fclose(f);
        }
        LeaveCriticalSection(&g_LogCS);
    }
    OutputDebugStringA("[ESP] ");
    OutputDebugStringA(buf);
    OutputDebugStringA("\r\n");
}

static int x86_len(BYTE* code) {
    BYTE op = code[0];

    if (op == 0x66 || op == 0x67 || op == 0xF0 || op == 0xF2 || op == 0xF3 ||
        op == 0x26 || op == 0x2E || op == 0x36 || op == 0x3E ||
        op == 0x64 || op == 0x65) {
        int n = x86_len(code + 1);
        return (n > 0) ? 1 + n : 2;
    }

    if (op >= 0x50 && op <= 0x5F) return 1;
    if (op >= 0x40 && op <= 0x4F) return 1;
    if (op == 0x90 || op == 0xF8 || op == 0xF9 || op == 0xFA ||
        op == 0xFB || op == 0xFC || op == 0xFD) return 1;
    if (op == 0xC3 || op == 0xCB || op == 0xCF) return 1;
    if (op == 0xCC) return 1;
    if (op == 0x9C || op == 0x9D || op == 0x60 || op == 0x61 || op == 0xC9) return 1;
    if (op == 0x98 || op == 0x99) return 1;
    if (op == 0x9E || op == 0x9F) return 1;
    if (op >= 0x91 && op <= 0x97) return 1;

    if (op == 0x6A) return 2;
    if (op == 0x68) return 5;

    if (op == 0xE8 || op == 0xE9) return 5;
    if (op == 0xEB) return 2;
    if (op >= 0x70 && op <= 0x7F) return 2;

    if (op >= 0xB8 && op <= 0xBF) return 5;

    if (op == 0x0F) {
        BYTE op2 = code[1];
        if (op2 >= 0x80 && op2 <= 0x8F) return 6;
        if (op2 >= 0x90 && op2 <= 0x9F) return 3;
        if (op2 == 0xBE || op2 == 0xB6 || op2 == 0xBF || op2 == 0xB7) return 3;
        return 3;
    }

    int modrm = code[1];
    int mod = (modrm >> 6) & 3;
    int rm = modrm & 7;

    if (op == 0x83) return 3;
    if (op == 0x81) return 6;
    if (op == 0x80) return 3;
    if (op == 0xC7) return 6;
    if (op == 0xC6) return 3;

    if (op == 0x8B || op == 0x89 || op == 0x85 || op == 0x33 ||
        op == 0x3B || op == 0x03 || op == 0x2B || op == 0x0B ||
        op == 0x23 || op == 0x39 || op == 0x8D) {
        if (mod == 0x03) return 2;
        if (mod == 0x00 && rm == 0x05) return 6;
        if (mod == 0x00 && rm == 0x04) {
            BYTE sib = code[2];
            if ((sib & 7) == 0x05) return 6;
            return 3;
        }
        if (mod == 0x01) return 3;
        if (mod == 0x02) return 6;
        return 2;
    }

    if (op == 0xFF) return 2;

    return 1;
}

static bool InstallHook(void* targetFunc, void* detourFunc, int* outHookLen) {
    BYTE* target = (BYTE*)targetFunc;

    int hookLen = 0;
    while (hookLen < 5) {
        int n = x86_len(target + hookLen);
        if (n <= 0 || n > 15) {
            dbg("InstallHook: bad insn at +%d (0x%02X)", hookLen, target[hookLen]);
            return false;
        }
        hookLen += n;
    }
    *outHookLen = hookLen;

    dbg("Hook target=0x%p  len=%d  prologue=%02X%02X%02X%02X%02X%02X%02X%02X",
        target, hookLen,
        target[0], target[1], target[2], target[3],
        target[4], target[5], target[6], target[7]);

    memcpy(g_SavedBytes, target, hookLen);

    DWORD oldProt;
    if (!VirtualProtect(target, hookLen, PAGE_EXECUTE_READWRITE, &oldProt)) {
        dbg("InstallHook: VirtualProtect FAIL %d", GetLastError());
        return false;
    }

    target[0] = 0xE9;
    DWORD rel = (DWORD)detourFunc - (DWORD)target - 5;
    memcpy(target + 1, &rel, 4);
    for (int i = 5; i < hookLen; i++)
        target[i] = 0x90;

    DWORD old2;
    VirtualProtect(target, hookLen, oldProt, &old2);

    int trampSize = hookLen + 5;
    g_Trampoline = (BYTE*)VirtualAlloc(NULL, trampSize, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!g_Trampoline) {
        dbg("InstallHook: trampoline alloc FAIL %d", GetLastError());
        VirtualProtect(target, hookLen, PAGE_EXECUTE_READWRITE, &old2);
        memcpy(target, g_SavedBytes, hookLen);
        VirtualProtect(target, hookLen, old2, &old2);
        return false;
    }

    memcpy(g_Trampoline, g_SavedBytes, hookLen);
    g_Trampoline[hookLen] = 0xE9;
    DWORD jmpBack = ((DWORD)target + hookLen) - (DWORD)(g_Trampoline + hookLen + 5);
    memcpy(g_Trampoline + hookLen + 1, &jmpBack, 4);

    g_RealPresent    = (PresentFn)g_Trampoline;
    g_PresentAddress = (DWORD)target;

    FlushInstructionCache(GetCurrentProcess(), g_Trampoline, trampSize);
    FlushInstructionCache(GetCurrentProcess(), target, hookLen);

    dbg("Hook OK  trampoline=0x%p", g_Trampoline);
    return true;
}

static void RestoreHook() {
    if (!g_PresentAddress) return;
    BYTE* target = (BYTE*)g_PresentAddress;
    DWORD old;
    VirtualProtect(target, g_HookLen, PAGE_EXECUTE_READWRITE, &old);
    memcpy(target, g_SavedBytes, g_HookLen);
    VirtualProtect(target, g_HookLen, old, &old);
    dbg("Hook restored");
    g_PresentAddress = 0;
}

static LRESULT __stdcall WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    if (ImGui_ImplWin32_WndProcHandler(hWnd, uMsg, wParam, lParam))
        return true;
    return CallWindowProc(g_OrigWndProc, hWnd, uMsg, wParam, lParam);
}

static volatile int g_PresentStage = 0;

static HRESULT __stdcall hkPresent(IDXGISwapChain* pSwap, UINT sync, UINT flags) {
    g_PresentStage = 1;

    if (g_Shutdown) {
        g_PresentStage = 0;
        return g_RealPresent(pSwap, sync, flags);
    }

    if (!g_ImGuiInit) {
        g_PresentStage = 10;
        dbg("First Present! swap=0x%p", pSwap);

        g_PresentStage = 11;
        ID3D11Device* pDev = NULL;
        HRESULT hr = pSwap->GetDevice(__uuidof(ID3D11Device), (void**)&pDev);
        dbg("GetDevice hr=0x%08X dev=0x%p", hr, pDev);

        if (SUCCEEDED(hr) && pDev) {
            g_pDevice = pDev;
            g_PresentStage = 12;

            g_pDevice->GetImmediateContext(&g_pContext);
            dbg("Context=0x%p", g_pContext);

            if (g_pContext) {
                g_PresentStage = 13;

                DXGI_SWAP_CHAIN_DESC sd;
                pSwap->GetDesc(&sd);
                g_hWnd = sd.OutputWindow;
                dbg("OutputWindow=0x%p", g_hWnd);

                g_PresentStage = 14;
                ID3D11Texture2D* pBackBuffer = NULL;
                hr = pSwap->GetBuffer(0, __uuidof(ID3D11Texture2D), (LPVOID*)&pBackBuffer);
                dbg("GetBuffer hr=0x%08X bb=0x%p", hr, pBackBuffer);

                if (SUCCEEDED(hr) && pBackBuffer) {
                    g_PresentStage = 15;
                    hr = g_pDevice->CreateRenderTargetView(pBackBuffer, NULL, &g_pRTV);
                    dbg("CreateRTV hr=0x%08X rtv=0x%p", hr, g_pRTV);
                    pBackBuffer->Release();
                }

                if (g_pRTV) {
                    g_PresentStage = 16;
                    
                    DXGI_SWAP_CHAIN_DESC sd;
                    pSwap->GetDesc(&sd);
                    float width = (float)sd.BufferDesc.Width;
                    float height = (float)sd.BufferDesc.Height;
                    
                    UINT numVps = 1;
                    D3D11_VIEWPORT vp;
                    g_pContext->RSGetViewports(&numVps, &vp);
                    
                    if (vp.Width > 0 && vp.Height > 0) {
                        width = vp.Width;
                        height = vp.Height;
                    }
                    
                    dbg("Viewport: num=%u w=%.0f h=%.0f x=%.0f y=%.0f (swapchain: %ux%u)", 
                        numVps, width, height, vp.TopLeftX, vp.TopLeftY, 
                        sd.BufferDesc.Width, sd.BufferDesc.Height);

                    g_PresentStage = 20;
                    ImGui::CreateContext();
                    ImGuiIO& io = ImGui::GetIO();
                    io.ConfigFlags = ImGuiConfigFlags_NoMouseCursorChange;
                    io.IniFilename = NULL;
                    io.DisplaySize = ImVec2(width, height);
                    io.Fonts->AddFontDefault();

                    ImGui_ImplWin32_Init(g_hWnd);
                    ImGui_ImplDX11_Init(g_pDevice, g_pContext);

                    g_OrigWndProc = (WNDPROC)SetWindowLongPtr(g_hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);

                    g_ImGuiInit = true;
                    dbg("=== ImGui INIT COMPLETE ===");
                } else {
                    dbg("No RTV, cannot init ImGui");
                }
            } else {
                dbg("GetImmediateContext returned NULL!");
            }
        } else {
            dbg("GetDevice FAILED hr=0x%08X", hr);
        }
    }

    if (g_ImGuiInit) {
        g_PresentStage = 60;

        ImGui_ImplDX11_NewFrame();
        ImGui_ImplWin32_NewFrame();
        ImGui::NewFrame();
        
        if (g_ESPInitialized) {
            ESPRenderer::Render();
        }

        ImGui::SetNextWindowPos(ImVec2(10, 10), ImGuiCond_FirstUseEver);
        ImGui::SetNextWindowSize(ImVec2(300, 200), ImGuiCond_FirstUseEver);
        ImGui::Begin("ESP Demo", NULL, ImGuiWindowFlags_NoCollapse);
        {
            ImGui::Checkbox("Enable ESP", &ESPRenderer::s_Enabled);
            ImGui::Separator();
            ImGui::Text("ImGui D3D11 Hook - Working!");
            ImGui::Separator();
            ImGui::Text("Frame: %d", (int)g_FrameCount);
            ImGui::Text("ESP Init: %s", g_ESPInitialized ? "YES" : "NO");
            ImGui::Text("Stage: %d", (int)g_PresentStage);
            ImGui::Text("Device: 0x%p", g_pDevice);
            ImGui::Text("Context: 0x%p", g_pContext);
        }
        ImGui::End();

        ImDrawList* bg = ImGui::GetBackgroundDrawList();
        bg->AddRect(ImVec2(100, 100), ImVec2(400, 350), IM_COL32(0, 255, 0, 255), 0, 0, 2.0f);
        bg->AddText(ImVec2(110, 110), IM_COL32(0, 255, 0, 255), "ESP Box Demo");

        ImGui::Render();
        g_pContext->OMSetRenderTargets(1, &g_pRTV, NULL);
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        LONG fc = InterlockedIncrement(&g_FrameCount);
        if (fc % 60 == 1) {
            dbg("Frame #%d  OK", fc);
        }
    }

    g_PresentStage = 50;
    HRESULT ret = g_RealPresent(pSwap, sync, flags);

    g_PresentStage = 0;
    return ret;
}

static bool InitD3D11AndHook() {
    WNDCLASSEXA wc = {};
    wc.cbSize        = sizeof(wc);
    wc.lpfnWndProc   = DefWindowProcA;
    wc.lpszClassName = "EspDummyClass";
    wc.hInstance     = GetModuleHandleA(0);
    RegisterClassExA(&wc);

    HWND hWnd = CreateWindowExA(0, "EspDummyClass", "", WS_OVERLAPPED,
        0, 0, 100, 100, 0, 0, wc.hInstance, 0);
    if (!hWnd) { dbg("CreateWindow FAIL err=%d", GetLastError()); return false; }
    dbg("DummyWindow=0x%p", hWnd);

    DXGI_SWAP_CHAIN_DESC sd = {};
    sd.BufferDesc.Width = 100;
    sd.BufferDesc.Height = 100;
    sd.BufferDesc.RefreshRate.Numerator = 60;
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;
    sd.SampleDesc.Count = 1;
    sd.SampleDesc.Quality = 0;
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;
    sd.BufferCount = 1;
    sd.OutputWindow = hWnd;
    sd.Windowed = TRUE;
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;

    D3D_FEATURE_LEVEL flvls[] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    D3D_FEATURE_LEVEL gotFl = D3D_FEATURE_LEVEL_10_0;
    ID3D11Device* pDev = NULL;
    ID3D11DeviceContext* pCtx = NULL;
    IDXGISwapChain* pSwap = NULL;

    HRESULT hr = D3D11CreateDeviceAndSwapChain(
        NULL, D3D_DRIVER_TYPE_HARDWARE, NULL, 0,
        flvls, 2, D3D11_SDK_VERSION,
        &sd, &pSwap, &pDev, &gotFl, &pCtx);

    if (FAILED(hr)) {
        dbg("D3D11CreateDeviceAndSwapChain FAIL 0x%08X", hr);
        DestroyWindow(hWnd);
        return false;
    }

    dbg("DeviceAndSwapChain OK dev=%p ctx=%p swap=%p fl=0x%x", pDev, pCtx, pSwap, gotFl);

    void** swapVt = *(void***)pSwap;
    void* pPresent = swapVt[8];
    dbg("Present vtable[8]=0x%p", pPresent);

    bool ok = InstallHook(pPresent, (void*)hkPresent, &g_HookLen);

    pSwap->Release();
    pDev->Release();
    pCtx->Release();
    DestroyWindow(hWnd);

    if (!ok) {
        dbg("InstallHook FAIL");
        return false;
    }

    return true;
}

static DWORD WINAPI MainThread(LPVOID) {
    Sleep(500);
    dbg("MainThread start");

    if (!InitD3D11AndHook()) {
        dbg("FATAL: InitD3D11AndHook failed");
        return 1;
    }

    dbg("Hook active. Waiting for game frames...");
    
    Sleep(3000);
    
    if (!g_ESPInitialized && !g_ESPInitAttempted) {
        g_ESPInitAttempted = true;
        dbg("[ESP] Starting initialization...");
        
        HMODULE gameAsm = GetModuleHandleA("GameAssembly.dll");
        if (gameAsm) {
            dbg("[ESP] GameAssembly.dll found at 0x%p", gameAsm);
            
            bool initOK = false;
            if (IL2CPPBridge::Initialize(gameAsm)) {
                if (GameManager::Initialize()) {
                    if (TransformHelper::Initialize()) {
                        if (CoordConverter::Initialize()) {
                            initOK = true;
                        }
                    }
                }
            }
            
            if (initOK) {
                g_ESPInitialized = true;
                dbg("=== ESP System Initialized ===");
            } else {
                dbg("[ESP] Initialization failed");
            }
        } else {
            dbg("[ESP] GameAssembly.dll not found, retrying...");
            for (int i = 0; i < 10; i++) {
                Sleep(1000);
                gameAsm = GetModuleHandleA("GameAssembly.dll");
                if (gameAsm) {
                    dbg("[ESP] GameAssembly.dll found at 0x%p (retry %d)", gameAsm, i+1);
                    if (IL2CPPBridge::Initialize(gameAsm)) {
                        if (GameManager::Initialize()) {
                            if (TransformHelper::Initialize()) {
                                if (CoordConverter::Initialize()) {
                                    g_ESPInitialized = true;
                                    dbg("=== ESP System Initialized ===");
                                    break;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    while (!g_Shutdown) {
        Sleep(250);
    }
    dbg("MainThread exit");
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hMod, DWORD reason, LPVOID) {
    switch (reason) {
    case DLL_PROCESS_ATTACH:
        DisableThreadLibraryCalls(hMod);
        {
            char dllPath[MAX_PATH];
            GetModuleFileNameA(hMod, dllPath, MAX_PATH);
            char* lastSlash = strrchr(dllPath, '\\');
            if (lastSlash) *(lastSlash + 1) = 0;
            wsprintfA(g_LogPath, "%sesp_log.txt", dllPath);
        }
        InitializeCriticalSection(&g_LogCS);
        dbg("DLL loaded  log=%s", g_LogPath);
        CreateThread(0, 0, MainThread, 0, 0, 0);
        break;

    case DLL_PROCESS_DETACH:
        g_Shutdown = true;
        Sleep(300);

        if (g_ImGuiInit) {
            RestoreHook();
            ImGui_ImplDX11_Shutdown();
            ImGui_ImplWin32_Shutdown();
            ImGui::DestroyContext();
            if (g_hWnd && g_OrigWndProc)
                SetWindowLongPtr(g_hWnd, GWLP_WNDPROC, (LONG_PTR)g_OrigWndProc);
        } else {
            RestoreHook();
        }

        if (g_pRTV) { g_pRTV->Release(); g_pRTV = NULL; }
        if (g_pContext) { g_pContext->Release(); g_pContext = NULL; }
        if (g_pDevice) { g_pDevice->Release(); g_pDevice = NULL; }
        if (g_Trampoline) VirtualFree(g_Trampoline, 0, MEM_RELEASE);

        dbg("DLL unloaded cleanly");
        DeleteCriticalSection(&g_LogCS);
        break;
    }
    return TRUE;
}
