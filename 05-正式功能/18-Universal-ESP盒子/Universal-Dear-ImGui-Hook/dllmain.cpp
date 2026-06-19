#include "stdafx.h"
#include "esp/named_pipe_server.h"
#include "esp/game_manager.h"
#include <atomic>

namespace mousehooks { void Init(); void Remove(); }

static std::atomic<bool> s_uninjecting{false};

// Utility helpers for backend initialization checks
using IsInitFn = bool (*)();

static bool WaitForInitialization(IsInitFn fn, int attempts = 50, int sleepMs = 100)
{
    for (int i = 0; i < attempts; ++i)
    {
        if (fn())
            return true;
        Sleep(sleepMs);
    }
    return false;
}

static bool TryInitBackend(globals::Backend backend)
{
    switch (backend)
    {
    case globals::Backend::DX12:
        if (GetModuleHandleA("d3d12.dll") || GetModuleHandleA("dxgi.dll"))
        {
            DebugLog("[DllMain] Attempting DX12 initialization.\n");
            hooks::Init();
            if (WaitForInitialization(d3d12hook::IsInitialized))
            {
                DebugLog("[DllMain] DX12 initialization succeeded.\n");
                globals::activeBackend = globals::Backend::DX12;
                return true;
            }
            DebugLog("[DllMain] DX12 initialization failed, falling back.\n");
            d3d12hook::release();
        }
        break;
    case globals::Backend::DX11:
        if (GetModuleHandleA("d3d11.dll"))
        {
            DebugLog("[DllMain] Attempting DX11 initialization.\n");
            hooks_dx11::Init();
            if (WaitForInitialization(hooks_dx11::IsInitialized))
            {
                DebugLog("[DllMain] DX11 initialization succeeded.\n");
                globals::activeBackend = globals::Backend::DX11;
                return true;
            }
            DebugLog("[DllMain] DX11 initialization failed, falling back.\n");
            hooks_dx11::release();
        }
        break;
    case globals::Backend::DX10:
        if (GetModuleHandleA("d3d10.dll"))
        {
            DebugLog("[DllMain] Attempting DX10 initialization.\n");
            hooks_dx10::Init();
            if (WaitForInitialization(hooks_dx10::IsInitialized))
            {
                DebugLog("[DllMain] DX10 initialization succeeded.\n");
                globals::activeBackend = globals::Backend::DX10;
                return true;
            }
            DebugLog("[DllMain] DX10 initialization failed, falling back.\n");
            hooks_dx10::release();
        }
        break;
    case globals::Backend::DX9:
        if (GetModuleHandleA("d3d9.dll"))
        {
            DebugLog("[DllMain] Attempting DX9 initialization.\n");
            d3d9hook::Init();
            if (WaitForInitialization(d3d9hook::IsInitialized))
            {
                DebugLog("[DllMain] DX9 initialization succeeded.\n");
                globals::activeBackend = globals::Backend::DX9;
                return true;
            }
            DebugLog("[DllMain] DX9 initialization failed, falling back.\n");
            d3d9hook::release();
        }
        break;
    default:
        break;
    }
    return false;
}

static bool TryInitializeFrom(globals::Backend start)
{
    const globals::Backend order[] = {
        globals::Backend::DX12,
        globals::Backend::DX11,
        globals::Backend::DX10,
        globals::Backend::DX9
    };
    int idx = 0;
    for (; idx < 4; ++idx)
    {
        if (order[idx] == start)
            break;
    }
    for (; idx < 4; ++idx)
    {
        if (TryInitBackend(order[idx]))
            return true;
    }
    DebugLog("[DllMain] All backend initialization attempts failed.\n");
    return false;
}

// Pointers to original LoadLibrary functions
using LoadLibraryA_t = HMODULE(WINAPI*)(LPCSTR);
using LoadLibraryW_t = HMODULE(WINAPI*)(LPCWSTR);
static LoadLibraryA_t oLoadLibraryA = nullptr;
static LoadLibraryW_t oLoadLibraryW = nullptr;

// Helper: check loaded module name and initialize hooks if needed
static int GetBackendPriority(globals::Backend backend)
{
    switch (backend)
    {
    case globals::Backend::DX12:   return 4;
    case globals::Backend::DX11:   return 3;
    case globals::Backend::DX10:   return 2;
    case globals::Backend::DX9:    return 1;
    default:                       return 0;
    }
}

static void InitForModule(const char* name)
{
    if (!name || s_uninjecting)
        return;

    const char* base = strrchr(name, '\\');
    base = base ? base + 1 : name;

    globals::Backend detected = globals::Backend::None;
    if (_stricmp(base, "d3d12.dll") == 0 || _stricmp(base, "dxgi.dll") == 0) {
        detected = globals::Backend::DX12;
    }
    else if (_stricmp(base, "d3d11.dll") == 0) {
        detected = globals::Backend::DX11;
    }
    else if (_stricmp(base, "d3d10.dll") == 0) {
        detected = globals::Backend::DX10;
    }
    else if (_stricmp(base, "d3d9.dll") == 0) {
        detected = globals::Backend::DX9;
    }
    else {
        return;
    }

    if (globals::preferredBackend != globals::Backend::None && detected != globals::preferredBackend)
        return;

    if (GetBackendPriority(detected) <= GetBackendPriority(globals::activeBackend))
        return;

    switch (globals::activeBackend)
    {
    case globals::Backend::DX9:    d3d9hook::release(); break;
    case globals::Backend::DX10:   hooks_dx10::release(); break;
    case globals::Backend::DX11:   hooks_dx11::release(); break;
    case globals::Backend::DX12:   d3d12hook::release(); break;
    default: break;
    }

    globals::activeBackend = globals::Backend::None;
    if (globals::preferredBackend != globals::Backend::None)
        TryInitBackend(globals::preferredBackend);
    else
        TryInitializeFrom(detected);
}

// Hooked LoadLibraryA
static HMODULE WINAPI hookLoadLibraryA(LPCSTR lpLibFileName)
{
    HMODULE mod = oLoadLibraryA(lpLibFileName);
    if (mod)
        InitForModule(lpLibFileName);
    return mod;
}

// Hooked LoadLibraryW
static HMODULE WINAPI hookLoadLibraryW(LPCWSTR lpLibFileName)
{
    HMODULE mod = oLoadLibraryW(lpLibFileName);
    if (mod && lpLibFileName)
    {
        char name[MAX_PATH];
        WideCharToMultiByte(CP_ACP, 0, lpLibFileName, -1, name, MAX_PATH, nullptr, nullptr);
        InitForModule(name);
    }
    return mod;
}

// Thread routine that performs cleanup and unloads the DLL
static DWORD WINAPI UninjectThread(LPVOID)
{
    DebugLog("[DllMain] Uninject thread starting.\n");

    // Stop named pipe server first to prevent thread from accessing freed code
    NamedPipeServer::Stop();

    MH_DisableHook(MH_ALL_HOOKS);

    // Let callbacks that entered before MH_DisableHook return before shared
    // state and critical sections are destroyed.
    Sleep(100);

    switch (globals::activeBackend)
    {
    case globals::Backend::DX9:
        d3d9hook::release();
        break;
    case globals::Backend::DX10:
        hooks_dx10::release();
        break;
    case globals::Backend::DX11:
        hooks_dx11::release();
        break;
    case globals::Backend::DX12:
        d3d12hook::release();
        break;
    default:
        break;
    }

    // mousehooks::Remove(); // mousehooks::Init() is intentionally inactive.
    globals::activeBackend = globals::Backend::None;

    // Remove all hooks, then uninitialize MinHook.
    MH_RemoveHook(MH_ALL_HOOKS);
    MH_Uninitialize();

    // Cleanup ESP game manager resources after hooks can no longer enter.
    esp::GameManager::Cleanup();

    DebugLog("[DllMain] Unloading module and exiting thread.\n");
    FreeLibraryAndExitThread(globals::mainModule, 0);
    return 0; // not reached
}

// Public helper to begin uninjecting the DLL
void Uninject()
{
    bool expected = false;
    if (!s_uninjecting.compare_exchange_strong(expected, true))
        return;

    // Wait for current frame to complete before starting cleanup
    // This ensures the Present hook (which called Uninject) has returned
    // before we start disabling hooks and releasing resources
    Sleep(50);  // ~3 frames at 60fps

    HANDLE hThread = CreateThread(nullptr, 0, UninjectThread, nullptr, 0, nullptr);
    if (hThread) {
        CloseHandle(hThread);
    } else {
        s_uninjecting = false;
    }
}

// Thread entry: initialize MinHook and start hook setup
static DWORD WINAPI onAttach(LPVOID lpParameter)
{
    DebugLog("[DllMain] onAttach starting.\n");

    // Initialize MinHook
    {
        MH_STATUS mhStatus = MH_Initialize();
        if (mhStatus != MH_OK) {
            DebugLog("[DllMain] MinHook initialization failed: %s\n",
                MH_StatusToString(mhStatus));
            return 1;
        }
        DebugLog("[DllMain] MinHook initialized.\n");
    }

    // Detect loaded rendering backends and initialize hooks accordingly
    if (globals::preferredBackend != globals::Backend::None)
        TryInitBackend(globals::preferredBackend);
    else
        TryInitializeFrom(globals::Backend::DX12);

    // Hook LoadLibraryA/W to catch backends loaded after injection
    HMODULE k32 = GetModuleHandleA("kernel32.dll");
    if (k32) {
        LPVOID addrA = GetProcAddress(k32, "LoadLibraryA");
        LPVOID addrW = GetProcAddress(k32, "LoadLibraryW");
        if (addrA) {
            MH_CreateHook(addrA, reinterpret_cast<LPVOID>(hookLoadLibraryA), reinterpret_cast<LPVOID*>(&oLoadLibraryA));
            MH_EnableHook(addrA);
            DebugLog("[DllMain] Hooked LoadLibraryA@%p\n", addrA);
        }
        if (addrW) {
            MH_CreateHook(addrW, reinterpret_cast<LPVOID>(hookLoadLibraryW), reinterpret_cast<LPVOID*>(&oLoadLibraryW));
            MH_EnableHook(addrW);
            DebugLog("[DllMain] Hooked LoadLibraryW@%p\n", addrW);
        }
    }

    // The in-game ImGui menu is not used by the release ESP path, so do not
    // hook SetCursorPos/ClipCursor. Box drawing does not require mouse hooks.
    // mousehooks::Init();

    // Start named pipe server after all initialization is done
    // This ensures the pipe server thread won't interfere with hook setup
    NamedPipeServer::Start();

    DebugLog("[DllMain] Hook initialization completed.\n");
    return 0;
}

BOOL WINAPI DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH:
    {
        // Early diagnostic: verify DllMain is called before anything else
        // Build path next to the DLL
        // DISABLED: 日志输出已注释
        /*
        wchar_t wDiagPath[MAX_PATH] = {0};
        HMODULE hDiagMod = NULL;
        GetModuleHandleExW(
            GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
            GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
            (LPCWSTR)DllMain,
            &hDiagMod);
        if (hDiagMod && GetModuleFileNameW(hDiagMod, wDiagPath, MAX_PATH)) {
            wchar_t* lastSlash = wcsrchr(wDiagPath, L'\\');
            if (lastSlash) {
                wcscpy_s(lastSlash + 1, MAX_PATH - (lastSlash + 1 - wDiagPath), L"esp_dllmain_test.txt");
            } else {
                wcscpy_s(wDiagPath, MAX_PATH, L"esp_dllmain_test.txt");
            }
        } else {
            GetTempPathW(MAX_PATH, wDiagPath);
            wcscat_s(wDiagPath, MAX_PATH, L"esp_dllmain_test.txt");
        }
        HANDLE hDiag = CreateFileW(wDiagPath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, 0, NULL);
        if (hDiag != INVALID_HANDLE_VALUE) {
            DWORD written;
            const char* diagMsg = "DllMain DLL_PROCESS_ATTACH reached\n";
            WriteFile(hDiag, diagMsg, (DWORD)strlen(diagMsg), &written, NULL);
            CloseHandle(hDiag);
        }
        */
        DebugLog("[DllMain] DLL_PROCESS_ATTACH: hModule=%p\n", hModule);
        globals::mainModule = hModule;
        // Create a thread for hook setup to avoid blocking loading
        {
            HANDLE thread = CreateThread(
                nullptr, 0,
                onAttach,
                nullptr,
                0,
                nullptr
            );
            if (thread) CloseHandle(thread);
            else DebugLog("[DllMain] Failed to create hook thread: %d\n", GetLastError());
        }
        break;
    }

    case DLL_PROCESS_DETACH:
        if (lpReserved) {
            DebugLog("[DllMain] Process exiting; skipping explicit detach cleanup.\n");
            break;
        }
        if (s_uninjecting) {
            DebugLog("[DllMain] DLL_PROCESS_DETACH after explicit cleanup.\n");
            break;
        }
        DebugLog("[DllMain] DLL_PROCESS_DETACH. Releasing hooks and uninitializing MinHook.\n");
        // Stop named pipe server
        NamedPipeServer::Stop();
        MH_DisableHook(MH_ALL_HOOKS);
        Sleep(100);
        switch (globals::activeBackend) {
        case globals::Backend::DX9:
            d3d9hook::release();
            break;
        case globals::Backend::DX10:
            hooks_dx10::release();
            break;
        case globals::Backend::DX11:
            hooks_dx11::release();
            break;
        case globals::Backend::DX12:
            d3d12hook::release();
            break;
        default:
            break;
        }
        // mousehooks::Remove(); // mousehooks::Init() is intentionally inactive.
        MH_RemoveHook(MH_ALL_HOOKS);
        MH_Uninitialize();
        esp::GameManager::Cleanup();
        break;
    }
    return TRUE;
}
