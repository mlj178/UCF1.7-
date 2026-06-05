#define WIN32_LEAN_AND_MEAN
#include <Windows.h>
#include "core/hook_manager.h"
#include "core/logger.h"
#include "core/config.h"
#include "hook/d3d11_hook.h"
#include "hook/input_hook.h"
#include "il2cpp/il2cpp_api.h"
#include "game/game_manager.h"
#include "game/coord_converter.h"

static volatile bool g_Shutdown = false;

static DWORD WINAPI MainThread(LPVOID param) {
    Sleep(500);

    LOG("Main", "MainThread start");

    if (!HookManager::Initialize()) {
        LOG_ERROR("Main", "Failed to initialize HookManager");
        return 1;
    }

    HMODULE gameAssembly = GetModuleHandleA("GameAssembly.dll");
    if (!gameAssembly) {
        LOG("Main", "GameAssembly.dll not found, retrying...");
        for (int i = 0; i < 10; i++) {
            Sleep(1000);
            gameAssembly = GetModuleHandleA("GameAssembly.dll");
            if (gameAssembly) {
                LOG("Main", "GameAssembly.dll found at 0x%p (retry %d)", gameAssembly, i + 1);
                break;
            }
        }
    }

    if (!gameAssembly) {
        LOG_ERROR("Main", "GameAssembly.dll not found after retries");
        return 1;
    }

    if (!IL2CPP::API::Initialize(gameAssembly)) {
        LOG_ERROR("Main", "Failed to initialize IL2CPP API");
        return 1;
    }

    if (!D3D11Hook::Instance().Initialize()) {
        LOG_ERROR("Main", "Failed to initialize D3D11 Hook");
        return 1;
    }

    if (!GameManager::Instance().Initialize()) {
        LOG_ERROR("Main", "Failed to initialize GameManager");
    }

    if (!CoordConverter::Instance().Initialize()) {
        LOG_ERROR("Main", "Failed to initialize CoordConverter");
    }

    LOG("Main", "Initialization complete");

    while (!g_Shutdown) {
        Sleep(250);
    }

    LOG("Main", "MainThread exit");
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
    case DLL_PROCESS_ATTACH: {
        DisableThreadLibraryCalls(hModule);

        char logPath[MAX_PATH];
        GetModuleFileNameA(hModule, logPath, MAX_PATH);
        char* lastSlash = strrchr(logPath, '\\');
        if (lastSlash) {
            strcpy(lastSlash + 1, "esp_log.txt");
        }

        Logger::Initialize(logPath);
        LOG("Main", "DLL loaded");

        char configPath[MAX_PATH];
        GetModuleFileNameA(hModule, configPath, MAX_PATH);
        lastSlash = strrchr(configPath, '\\');
        if (lastSlash) {
            strcpy(lastSlash + 1, "esp_config.ini");
        }

        g_Config.LoadFromFile(configPath);

        CreateThread(0, 0, MainThread, 0, 0, 0);
        break;
    }
    case DLL_PROCESS_DETACH: {
        g_Shutdown = true;
        Sleep(300);

        LOG("Main", "DLL unloading");

        D3D11Hook::Instance().Shutdown();
        InputHook::Instance().Shutdown();
        HookManager::Shutdown();
        IL2CPP::API::Shutdown();
        Logger::Shutdown();

        break;
    }
    }
    return TRUE;
}
