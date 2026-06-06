#include "il2cpp_bridge.h"
#include "../stdafx.h"

namespace esp {

void* IL2CPPBridge::s_GameAssemblyBase = nullptr;
bool IL2CPPBridge::s_Initialized = false;
IL2CPPBridge::SingletonGetFn IL2CPPBridge::s_SingletonGet = nullptr;
void* IL2CPPBridge::s_CachedInstance = nullptr;

static bool ValidateArray(void* arrayPtr, int maxLength) {
    if (!arrayPtr || !IsValidPointer(arrayPtr)) return false;

    int length = -1;
    if (!SafeReadValue<int>((char*)arrayPtr + OffsetConstants::Arr_len, &length)) return false;
    if (length < 0 || length > maxLength) return false;
    if (length > 0) {
        void* first = nullptr;
        if (!SafeReadValue<void*>((char*)arrayPtr + OffsetConstants::Arr_data, &first)) return false;
    }
    return true;
}

static bool ValidateList(void* listPtr, int maxLength) {
    if (!listPtr || !IsValidPointer(listPtr)) return false;

    void* items = nullptr;
    int size = -1;
    if (!SafeReadValue<void*>((char*)listPtr + OffsetConstants::List_items, &items)) return false;
    if (!SafeReadValue<int>((char*)listPtr + OffsetConstants::List_size, &size)) return false;
    if (size < 0 || size > maxLength) return false;
    if (size > 0 && (!items || !ValidateArray(items, maxLength))) return false;
    return true;
}

bool IL2CPPBridge::ValidateGameManagerInstance(void* instance) {
    if (!instance || !IsValidPointer(instance)) return false;

    void* allPlayers = nullptr;
    void* playersBL = nullptr;
    void* playersGR = nullptr;
    if (!SafeReadValue<void*>((char*)instance + OffsetConstants::GM_allPlayers, &allPlayers)) return false;
    if (!SafeReadValue<void*>((char*)instance + OffsetConstants::GM_playersBL, &playersBL)) return false;
    if (!SafeReadValue<void*>((char*)instance + OffsetConstants::GM_playersGR, &playersGR)) return false;

    bool hasValidContainer = false;
    if (allPlayers) hasValidContainer = ValidateArray(allPlayers, 64) || hasValidContainer;
    if (playersBL) hasValidContainer = ValidateList(playersBL, 32) || hasValidContainer;
    if (playersGR) hasValidContainer = ValidateList(playersGR, 32) || hasValidContainer;

    return hasValidContainer;
}

bool IL2CPPBridge::Initialize(HMODULE gameAssembly) {
    if (s_Initialized) return true;

    if (!gameAssembly) {
        DebugLog("[IL2CPPBridge] ERROR: gameAssembly is null\n");
        return false;
    }

    s_GameAssemblyBase = (void*)gameAssembly;
    s_SingletonGet = (SingletonGetFn)((char*)gameAssembly + RVAConstants::SingletonGet);
    if (!IsExecutableAddress((void*)s_SingletonGet)) {
        DebugLog("[IL2CPPBridge] ERROR: SingletonGet address is not executable: 0x%p\n", s_SingletonGet);
        s_GameAssemblyBase = nullptr;
        s_SingletonGet = nullptr;
        return false;
    }

    s_Initialized = true;
    DebugLog("[IL2CPPBridge] Initialized successfully (Singleton method)\n");
    DebugLog("  GameAssembly: 0x%p\n", gameAssembly);
    DebugLog("  SingletonGet: 0x%p (RVA+0x%lX)\n", s_SingletonGet, RVAConstants::SingletonGet);

    void* methodInfoPtr = (void*)((char*)gameAssembly + RVAConstants::GM_Singleton_MethodInfo);
    DebugLog("  GM_Singleton_MethodInfo address: 0x%p\n", methodInfoPtr);

    void* methodInfo = nullptr;
    if (SafeReadValue<void*>(methodInfoPtr, &methodInfo)) {
        DebugLog("  GM_Singleton_MethodInfo content: 0x%p\n", methodInfo);
    }

    return true;
}

bool IL2CPPBridge::IsGameAssemblyReady() {
    if (!s_GameAssemblyBase) return false;
    HMODULE current = GetModuleHandleA("GameAssembly.dll");
    return current && (void*)current == s_GameAssemblyBase && IsExecutableAddress((void*)s_SingletonGet);
}

void IL2CPPBridge::ResetSessionState() {
    if (s_CachedInstance) {
        DebugLog("[IL2CPPBridge] Resetting cached GameManager instance: 0x%p\n", s_CachedInstance);
    }
    s_CachedInstance = nullptr;
}

static void* CallSingletonGet(IL2CPPBridge::SingletonGetFn fn, void* methodInfo) {
    if (!fn) return nullptr;
#if defined(_MSC_VER)
    __try {
        return fn(methodInfo);
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return nullptr;
    }
#else
    SAFE_TRY {
        return fn(methodInfo);
    } SAFE_EXCEPT_RET(nullptr)
#endif
}

void* IL2CPPBridge::TryGetGameManagerInstance() {
    if (!IsGameAssemblyReady()) {
        return nullptr;
    }

    static int retryCount = 0;
    const bool shouldLog = (retryCount++ % 120 == 0);
    if (shouldLog) {
        DebugLog("[IL2CPPBridge] Getting GameManager instance (retry %d)...\n", retryCount);
    }

    void* methodInfo = nullptr;
    void* methodInfoPtr = (void*)((char*)s_GameAssemblyBase + RVAConstants::GM_Singleton_MethodInfo);
    SafeReadValue<void*>(methodInfoPtr, &methodInfo);

    void* instance = nullptr;

    if (methodInfo && IsValidPointer(methodInfo)) {
        instance = CallSingletonGet(s_SingletonGet, methodInfo);
        if (shouldLog) {
            DebugLog("[IL2CPPBridge] [Method 1] SingletonGet(MI=0x%p) => 0x%p\n", methodInfo, instance);
        }
    }

    if (ValidateGameManagerInstance(instance)) {
        if (shouldLog) {
            DebugLog("[IL2CPPBridge] [OK] GameManager instance: 0x%p\n", instance);
        }
        return instance;
    }

    if (shouldLog) {
        DebugLog("[IL2CPPBridge] [X] GameManager not available yet (retry %d)\n", retryCount);
    }
    return nullptr;
}

void* IL2CPPBridge::GetGameManagerInstance() {
    if (s_CachedInstance) {
        if (ValidateGameManagerInstance(s_CachedInstance)) {
            return s_CachedInstance;
        }
        DebugLog("[IL2CPPBridge] Cached GM instance invalid, clearing cache\n");
        s_CachedInstance = nullptr;
    }

    void* instance = TryGetGameManagerInstance();
    if (instance) {
        s_CachedInstance = instance;
    }
    return instance;
}

}
