#include "hook_manager.h"
#include "../minhook/MinHook.h"
#include <stdio.h>

namespace HookManager {
    static bool s_Initialized = false;
    
    bool Initialize() {
        if (s_Initialized) {
            return true;
        }
        
        if (MH_Initialize() != MH_OK) {
            return false;
        }
        
        s_Initialized = true;
        return true;
    }
    
    void Shutdown() {
        if (!s_Initialized) {
            return;
        }
        
        MH_Uninitialize();
        s_Initialized = false;
    }
    
    bool CreateHook(void* target, void* detour, void** original) {
        if (!s_Initialized) {
            return false;
        }
        
        if (MH_CreateHook(target, detour, original) != MH_OK) {
            return false;
        }
        
        return true;
    }
    
    bool EnableHook(void* target) {
        if (!s_Initialized) {
            return false;
        }
        
        if (MH_EnableHook(target) != MH_OK) {
            return false;
        }
        
        return true;
    }
    
    bool DisableHook(void* target) {
        if (!s_Initialized) {
            return false;
        }
        
        if (MH_DisableHook(target) != MH_OK) {
            return false;
        }
        
        return true;
    }
    
    bool RemoveHook(void* target) {
        if (!s_Initialized) {
            return false;
        }
        
        if (MH_RemoveHook(target) != MH_OK) {
            return false;
        }
        
        return true;
    }
    
    void EnableAllHooks() {
        if (!s_Initialized) {
            return;
        }
        
        MH_EnableHook(MH_ALL_HOOKS);
    }
    
    void DisableAllHooks() {
        if (!s_Initialized) {
            return;
        }
        
        MH_DisableHook(MH_ALL_HOOKS);
    }
}
