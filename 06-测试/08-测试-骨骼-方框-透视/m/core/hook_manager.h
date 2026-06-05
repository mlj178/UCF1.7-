#pragma once
#include <Windows.h>

namespace HookManager {
    bool Initialize();
    void Shutdown();
    
    bool CreateHook(void* target, void* detour, void** original);
    bool EnableHook(void* target);
    bool DisableHook(void* target);
    bool RemoveHook(void* target);
    void EnableAllHooks();
    void DisableAllHooks();
}
