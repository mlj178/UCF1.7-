#include "game_manager.h"
#include "../stdafx.h"
#include <algorithm>

namespace esp {

static void* s_gameManagerInstance = nullptr;
static bool s_initialized = false;
static bool s_hasActiveSession = false;
// GameManager::OnDestroy can run before its static instance field is cleared.
// Block render-side reacquisition until the next real round-start event.
static volatile LONG s_BlockSessionRefresh = 0;

// Static member initialization
std::unordered_map<void*, BotPlayerEntry> GameManager::s_BotPlayers;
bool GameManager::s_BotHookInitialized = false;
CRITICAL_SECTION GameManager::s_BotPlayersCS;
bool GameManager::s_CritSecInitialized = false;
constexpr DWORD GameManager::BOT_ENTRY_TIMEOUT_MS;
constexpr DWORD GameManager::ROUND_CHANGE_COOLDOWN_MS;
DWORD GameManager::s_SessionEpoch = 0;
DWORD GameManager::s_LastRoundChangeTime = 0;

typedef void (__cdecl *BotUpdateFunc)(void* bot, void* methodInfo);
typedef bool (__cdecl *GetIsDeadFn)(void* entity, void* methodInfo);
typedef void* (__cdecl *GetHealthDataFn)(void* entity, void* methodInfo);
typedef float (__cdecl *GetHealthRateFn)(void* healthData, void* methodInfo);

static BotUpdateFunc s_OriginalBotUpdate = nullptr;

void GameManager::ClearRuntimeCaches(const char* reason) {
    if (s_gameManagerInstance || !s_BotPlayers.empty()) {
        DebugLog("[GameManager] Clearing session state: %s\n", reason ? reason : "unknown");
    }
    s_gameManagerInstance = nullptr;
    s_hasActiveSession = false;
    
    if (s_CritSecInitialized) {
        EnterCriticalSection(&s_BotPlayersCS);
    }
    s_BotPlayers.clear();
    if (s_CritSecInitialized) {
        LeaveCriticalSection(&s_BotPlayersCS);
    }
    
    IL2CPPBridge::ResetSessionState();
}

static bool IsSaneCount(int count, int maxCount) {
    return count >= 0 && count <= maxCount;
}

static void AddUniquePlayer(std::vector<void*>& players, void* player) {
    if (!player) return;

    if (!GameManager::IsValidPlayer(player)) {
        static int invalidCounter = 0;
        if (invalidCounter++ % 120 == 0) {
            DebugLog("[GameManager] AddUniquePlayer: Invalid player 0x%p\n", player);
        }
        return;
    }

    players.push_back(player);
}

static void ReadArrayPlayers(void* arrayPtr, std::vector<void*>& players, int maxCount, const char* label) {
    if (!arrayPtr || !IsValidPointer(arrayPtr)) return;

    int length = 0;
    if (!SafeReadValue<int>((char*)arrayPtr + OffsetConstants::Arr_len, &length)) return;
    if (!IsSaneCount(length, maxCount)) {
        DebugLog("[GameManager] Ignoring %s with invalid length: %d\n", label, length);
        return;
    }

    for (int i = 0; i < length; ++i) {
        void* player = nullptr;
        if (SafeReadValue<void*>((char*)arrayPtr + OffsetConstants::Arr_data + i * sizeof(void*), &player)) {
            AddUniquePlayer(players, player);
        }
    }
}

static void ReadListPlayers(void* listPtr, std::vector<void*>& players, int maxCount, const char* label) {
    if (!listPtr || !IsValidPointer(listPtr)) return;

    void* items = nullptr;
    int count = 0;
    if (!SafeReadValue<void*>((char*)listPtr + OffsetConstants::List_items, &items)) return;
    if (!SafeReadValue<int>((char*)listPtr + OffsetConstants::List_size, &count)) return;
    if (!IsSaneCount(count, maxCount)) {
        DebugLog("[GameManager] Ignoring %s with invalid size: %d\n", label, count);
        return;
    }
    if (count == 0 || !items || !IsValidPointer(items)) return;

    for (int i = 0; i < count; ++i) {
        void* player = nullptr;
        if (SafeReadValue<void*>((char*)items + OffsetConstants::Arr_data + i * sizeof(void*), &player)) {
            AddUniquePlayer(players, player);
        }
    }
}

static bool SafeCallIsDead(GetIsDeadFn fn, void* player, bool* outValue) {
    if (!fn || !player || !outValue) return false;

#if defined(_MSC_VER)
    __try {
        *outValue = fn(player, nullptr);
        return true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
#else
    SAFE_TRY {
        *outValue = fn(player, nullptr);
        return true;
    } SAFE_EXCEPT_RET(false)
#endif
}

static void __cdecl HookedBotUpdate(void* botInstance, void* methodInfo) {
    if (s_OriginalBotUpdate) {
#if defined(_MSC_VER)
        __try {
            s_OriginalBotUpdate(botInstance, methodInfo);
        } __except(EXCEPTION_EXECUTE_HANDLER) {
            return;
        }
#else
        SAFE_TRY {
            s_OriginalBotUpdate(botInstance, methodInfo);
        } SAFE_EXCEPT_NOP
#endif
    }

    GameManager::OnBotUpdate(botInstance);
}

bool GameManager::Initialize() {
    if (s_initialized) return true;
    if (!IL2CPPBridge::IsInitialized()) return false;

    DebugLog("[GameManager] ===== Initialize =====\n");
    
    // 初始化临界区（用于线程同步）
    if (!s_CritSecInitialized) {
        InitializeCriticalSection(&s_BotPlayersCS);
        s_CritSecInitialized = true;
        DebugLog("[GameManager] Critical section initialized\n");
    }
    
    s_initialized = true;
    RefreshSession();
    return true;
}

bool GameManager::IsInitialized() {
    return s_initialized;
}

void GameManager::ResetSessionState() {
    ClearRuntimeCaches("explicit reset");
}

void GameManager::Cleanup() {
    DebugLog("[GameManager] Cleanup called.\n");
    
    // Clear caches first
    ClearRuntimeCaches("cleanup");
    
    // Delete critical section
    if (s_CritSecInitialized) {
        DeleteCriticalSection(&s_BotPlayersCS);
        s_CritSecInitialized = false;
        DebugLog("[GameManager] Critical section deleted.\n");
    }
    
    s_initialized = false;
}

bool GameManager::RefreshSession() {
    if (!s_initialized || !IL2CPPBridge::IsInitialized() || !IL2CPPBridge::IsGameAssemblyReady()) {
        ClearRuntimeCaches("bridge unavailable");
        return false;
    }

    if (InterlockedCompareExchange(&s_BlockSessionRefresh, 0, 0) != 0) {
        return false;
    }

    void* newInstance = IL2CPPBridge::GetGameManagerInstance();
    if (!newInstance) {
        if (s_hasActiveSession || s_gameManagerInstance) {
            ClearRuntimeCaches("GameManager unavailable");
        }
        return false;
    }

    if (newInstance != s_gameManagerInstance) {
        DebugLog("[GameManager] GameManager instance changed: 0x%p -> 0x%p\n",
                 s_gameManagerInstance, newInstance);
        s_gameManagerInstance = newInstance;
        
        // 线程安全清理 s_BotPlayers
        if (s_CritSecInitialized) {
            EnterCriticalSection(&s_BotPlayersCS);
        }
        s_BotPlayers.clear();
        if (s_CritSecInitialized) {
            LeaveCriticalSection(&s_BotPlayersCS);
        }
    }

    s_hasActiveSession = true;
    return true;
}

bool GameManager::HasActiveSession() {
    return s_hasActiveSession && s_gameManagerInstance && IsValidPointer(s_gameManagerInstance);
}

void* GameManager::GetInstance() {
    return HasActiveSession() ? s_gameManagerInstance : nullptr;
}

void* GameManager::GetLocalPlayer() {
    if (!HasActiveSession()) return nullptr;

    void* gameAssembly = IL2CPPBridge::GetBase();
    if (!gameAssembly) return nullptr;

    void* typeInfoSlot = (void*)((char*)gameAssembly + RVAConstants::GameManager_TypeInfo);
    void* klass = nullptr;
    if (SafeReadValue<void*>(typeInfoSlot, &klass) && klass && IsValidPointer(klass)) {
        void* staticFields = nullptr;
        if (SafeReadValue<void*>((char*)klass + OffsetConstants::Klass_staticFields, &staticFields)
            && staticFields && IsValidPointer(staticFields)) {
            void* myPlayer = nullptr;
            if (SafeReadValue<void*>(staticFields, &myPlayer) && IsValidPlayer(myPlayer)) {
                return myPlayer;
            }
        }
    }

    return nullptr;
}

std::vector<void*> GameManager::GetAllPlayers() {
    std::vector<void*> result;
    if (!RefreshSession()) return result;

    void* instance = s_gameManagerInstance;
    if (!instance) return result;

    // Primary source: playersBL_Alive + playersGR_Alive (only alive players)
    void* playersBL_Alive = nullptr;
    if (SafeReadValue<void*>((char*)instance + OffsetConstants::GM_playersBL_Alive, &playersBL_Alive)) {
        ReadListPlayers(playersBL_Alive, result, 32, "playersBL_Alive");
    }

    void* playersGR_Alive = nullptr;
    if (SafeReadValue<void*>((char*)instance + OffsetConstants::GM_playersGR_Alive, &playersGR_Alive)) {
        ReadListPlayers(playersGR_Alive, result, 32, "playersGR_Alive");
    }

    // Fallback: if alive lists are empty, try allPlayers
    if (result.empty()) {
        void* allPlayersArr = nullptr;
        if (SafeReadValue<void*>((char*)instance + OffsetConstants::GM_allPlayers, &allPlayersArr)) {
            ReadArrayPlayers(allPlayersArr, result, 64, "allPlayers");
        }
    }

    std::sort(result.begin(), result.end());
    result.erase(std::unique(result.begin(), result.end()), result.end());

    static int logCounter = 0;
    if (logCounter++ % 120 == 0) {
        DebugLog("[GameManager] Got %zu unique players\n", result.size());
    }

    return result;
}

bool GameManager::IsValidPlayer(void* player) {
    if (!player || !IsValidPointer(player)) return false;

    // 1. Check object's klass pointer (IL2CPP object header, offset 0x00)
    // If object is GC collected, klass pointer may be invalid
    void* klass = nullptr;
    if (!SafeReadValue<void*>(player, &klass)) {
        static int logCounter = 0;
        if (logCounter++ % 120 == 0) {
            DebugLog("[GameManager] IsValidPlayer: Failed to read klass for 0x%p\n", player);
        }
        return false;
    }
    if (!klass || !IsValidPointer(klass)) {
        static int logCounter = 0;
        if (logCounter++ % 120 == 0) {
            DebugLog("[GameManager] IsValidPlayer: Invalid klass 0x%p for player 0x%p\n", klass, player);
        }
        return false;
    }

    // 2. Check team field (Entity.team, offset 0x20)
    int team = -1;
    if (!SafeReadValue<int>((char*)player + OffsetConstants::E_team, &team)) return false;
    if (team < 0 || team > 2) return false;

    // 3. Check characterContainer (Player.characterContainer, offset 0x58)
    void* container = nullptr;
    if (SafeReadValue<void*>((char*)player + OffsetConstants::P_characterContainer, &container)) {
        if (container && !IsValidPointer(container)) return false;
    }

    return true;
}

bool GameManager::IsPlayerDead(void* player) {
    // 1. Basic validation: session and pointer validity
    if (!HasActiveSession()) return true;
    if (!player || !IsValidPointer(player)) return true;

    // 2. Quick validation: check object's klass pointer (avoid accessing recycled objects)
    void* klass = nullptr;
    if (!SafeReadValue<void*>(player, &klass) || !klass || !IsValidPointer(klass)) {
        // Object has been GC collected, treat as dead
        static int logCounter = 0;
        if (logCounter++ % 120 == 0) {
            DebugLog("[GameManager] IsPlayerDead: Object recycled, klass invalid for 0x%p\n", player);
        }
        return true;
    }

    // 3. Full validation: use IsValidPlayer
    if (!IsValidPlayer(player)) return true;

    // 4. Get get_isDead function address
    void* gameAssembly = IL2CPPBridge::GetBase();
    if (!gameAssembly) return true;

    GetIsDeadFn getIsDead = (GetIsDeadFn)((char*)gameAssembly + RVAConstants::Entity_get_isDead);
    if (!IsExecutableAddress((void*)getIsDead)) {
        DebugLog("[GameManager] get_isDead address is not executable: 0x%p\n", getIsDead);
        return true;
    }

    // 5. Call get_isDead (with SEH protection)
    bool isDead = true;
    if (!SafeCallIsDead(getIsDead, player, &isDead)) {
        // SEH caught exception, object may have been GC collected
        static int failCounter = 0;
        if (failCounter++ % 60 == 0) {
            DebugLog("[GameManager] get_isDead SEH exception for player 0x%p, treating as dead (count: %d)\n",
                     player, failCounter);
        }
        return true;
    }

    static int logCounter = 0;
    if (logCounter++ % 600 == 0) {
        DebugLog("[GameManager] IsPlayerDead(0x%p) = %d\n", player, isDead ? 1 : 0);
    }

    return isDead;
}

bool GameManager::GetPlayerHealth(void* player, float* outRate) {
    if (!outRate || !HasActiveSession() || !player || !IsValidPlayer(player)) return false;

    void* gameAssembly = IL2CPPBridge::GetBase();
    if (!gameAssembly) return false;

    auto getHealthData = (GetHealthDataFn)((char*)gameAssembly + RVAConstants::Entity_get_healthData);
    auto getHealthRate = (GetHealthRateFn)((char*)gameAssembly + RVAConstants::HealthData_get_rate);
    if (!IsExecutableAddress((void*)getHealthData) || !IsExecutableAddress((void*)getHealthRate)) {
        return false;
    }

    void* healthData = nullptr;
    float rate = -1.0f;
#if defined(_MSC_VER)
    __try {
        healthData = getHealthData(player, nullptr);
        if (healthData) rate = getHealthRate(healthData, nullptr);
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
#else
    SAFE_TRY {
        healthData = getHealthData(player, nullptr);
        if (healthData) rate = getHealthRate(healthData, nullptr);
    } SAFE_EXCEPT_RET(false)
#endif

    if (!std::isfinite(rate) || rate <= 0.0f || rate > 1.0f) return false;
    *outRate = rate;
    return true;
}

int GameManager::GetPlayerTeam(void* player) {
    if (!IsValidPlayer(player)) return -1;

    int team = -1;
    if (SafeReadValue<int>((char*)player + OffsetConstants::E_team, &team)) {
        return team;
    }
    return -1;
}

void GameManager::InitializeBotHook() {
    if (s_BotHookInitialized) {
        DebugLog("[GameManager] BotHook already initialized\n");
        return;
    }

    HMODULE gameModule = GetModuleHandleA("GameAssembly.dll");
    if (!gameModule) {
        DebugLog("[GameManager] BotHook: GameAssembly not loaded\n");
        return;
    }

    void* botUpdateAddr = (void*)((uintptr_t)gameModule + 0xB33370);
    if (!IsExecutableAddress(botUpdateAddr)) {
        DebugLog("[GameManager] BotHook: Bot.Update address is not executable: 0x%p\n", botUpdateAddr);
        return;
    }

    DebugLog("[GameManager] BotHook: Bot.Update at 0x%p (RVA+0xB33370)\n", botUpdateAddr);

    MH_STATUS createStatus = MH_CreateHook(botUpdateAddr, &HookedBotUpdate, reinterpret_cast<LPVOID*>(&s_OriginalBotUpdate));
    if (createStatus != MH_OK) {
        DebugLog("[GameManager] BotHook: Failed to create hook: %s\n", MH_StatusToString(createStatus));
        return;
    }

    MH_STATUS enableStatus = MH_EnableHook(botUpdateAddr);
    if (enableStatus != MH_OK) {
        DebugLog("[GameManager] BotHook: Failed to enable hook: %s\n", MH_StatusToString(enableStatus));
        MH_RemoveHook(botUpdateAddr);
        s_OriginalBotUpdate = nullptr;
        return;
    }

    s_BotHookInitialized = true;
    DebugLog("[GameManager] BotHook: Bot.Update hooked successfully\n");
}

// Room/Round change detection - Key RVA addresses
static constexpr uintptr_t RVA_ModeBase_OnStartNewGameRound = 0xAF5B30;
static constexpr uintptr_t RVA_ModeBase_Nano_OnStartNewGameRound = 0xAF15D0;
static constexpr uintptr_t RVA_GameManager_OnDestroy = 0xAFB6F0;

typedef void (__cdecl *RoundStartFunc)(void* modeBase, void* methodInfo);
typedef void (__cdecl *GameDestroyFunc)(void* gm, void* methodInfo);

static RoundStartFunc s_OriginalRoundStart = nullptr;
static RoundStartFunc s_OriginalNanoRoundStart = nullptr;
static GameDestroyFunc s_OriginalGameDestroy = nullptr;

static void __cdecl HookedRoundStart(void* modeBase, void* methodInfo) {
    GameManager::OnRoundStart();
    
    if (s_OriginalRoundStart) {
#if defined(_MSC_VER)
        __try {
            s_OriginalRoundStart(modeBase, methodInfo);
        } __except(EXCEPTION_EXECUTE_HANDLER) {
            return;
        }
#else
        SAFE_TRY {
            s_OriginalRoundStart(modeBase, methodInfo);
        } SAFE_EXCEPT_NOP
#endif
    }
}

static void __cdecl HookedNanoRoundStart(void* modeBaseNano, void* methodInfo) {
    GameManager::OnRoundStart();

    if (s_OriginalNanoRoundStart) {
#if defined(_MSC_VER)
        __try {
            s_OriginalNanoRoundStart(modeBaseNano, methodInfo);
        } __except(EXCEPTION_EXECUTE_HANDLER) {
            return;
        }
#else
        SAFE_TRY {
            s_OriginalNanoRoundStart(modeBaseNano, methodInfo);
        } SAFE_EXCEPT_NOP
#endif
    }
}

static void __cdecl HookedGameDestroy(void* gm, void* methodInfo) {
    GameManager::OnGameDestroy();
    
    if (s_OriginalGameDestroy) {
#if defined(_MSC_VER)
        __try {
            s_OriginalGameDestroy(gm, methodInfo);
        } __except(EXCEPTION_EXECUTE_HANDLER) {
            return;
        }
#else
        SAFE_TRY {
            s_OriginalGameDestroy(gm, methodInfo);
        } SAFE_EXCEPT_NOP
#endif
    }
}

void GameManager::InitializeRoomHooks() {
    HMODULE gameModule = GetModuleHandleA("GameAssembly.dll");
    if (!gameModule) {
        DebugLog("[GameManager] RoomHooks: GameAssembly not loaded\n");
        return;
    }
    
    // Hook 1: ModeBase$$OnStartNewGameRound (0xAF5B30)
    void* addr1 = (void*)((uintptr_t)gameModule + RVA_ModeBase_OnStartNewGameRound);
    if (IsExecutableAddress(addr1)) {
        MH_STATUS status = MH_CreateHook(addr1, &HookedRoundStart, 
                                         reinterpret_cast<LPVOID*>(&s_OriginalRoundStart));
        if (status == MH_OK) {
            MH_EnableHook(addr1);
            DebugLog("[GameManager] RoomHooks: ModeBase$$OnStartNewGameRound hooked at 0x%p\n", addr1);
        } else {
            DebugLog("[GameManager] RoomHooks: Failed to hook OnStartNewGameRound: %s\n", MH_StatusToString(status));
        }
    }

    // Hook 2: ModeBase_Nano$$OnStartNewGameRound (0xAF15D0).
    // Nano4, Nano4_Terminator and Nano6 call this shared implementation, while
    // it does not call ModeBase$$OnStartNewGameRound. Hooking it restores the
    // ESP session after leaving another room without weakening stale-pointer protection.
    void* addrNano = (void*)((uintptr_t)gameModule + RVA_ModeBase_Nano_OnStartNewGameRound);
    if (IsExecutableAddress(addrNano)) {
        MH_STATUS status = MH_CreateHook(addrNano, &HookedNanoRoundStart,
                                         reinterpret_cast<LPVOID*>(&s_OriginalNanoRoundStart));
        if (status == MH_OK) {
            MH_STATUS enableStatus = MH_EnableHook(addrNano);
            if (enableStatus == MH_OK) {
                DebugLog("[GameManager] RoomHooks: ModeBase_Nano$$OnStartNewGameRound hooked at 0x%p\n", addrNano);
            } else {
                DebugLog("[GameManager] RoomHooks: Failed to enable Nano OnStartNewGameRound: %s\n",
                         MH_StatusToString(enableStatus));
            }
        } else {
            DebugLog("[GameManager] RoomHooks: Failed to hook Nano OnStartNewGameRound: %s\n",
                     MH_StatusToString(status));
        }
    }
    
    // Hook 3: GameManager$$OnDestroy (0xAFB6F0)
    void* addr2 = (void*)((uintptr_t)gameModule + RVA_GameManager_OnDestroy);
    if (IsExecutableAddress(addr2)) {
        MH_STATUS status = MH_CreateHook(addr2, &HookedGameDestroy,
                                         reinterpret_cast<LPVOID*>(&s_OriginalGameDestroy));
        if (status == MH_OK) {
            MH_EnableHook(addr2);
            DebugLog("[GameManager] RoomHooks: GameManager$$OnDestroy hooked at 0x%p\n", addr2);
        } else {
            DebugLog("[GameManager] RoomHooks: Failed to hook OnDestroy: %s\n", MH_StatusToString(status));
        }
    }
}

void GameManager::OnRoundStart() {
    DWORD currentTime = GetTickCount();

    // A real round-start means the new room lifecycle is ready for ESP reads.
    InterlockedExchange(&s_BlockSessionRefresh, 0);
    
    // Increment session epoch
    s_SessionEpoch++;
    s_LastRoundChangeTime = currentTime;
    
    DebugLog("[GameManager] OnRoundStart: New round started, epoch=%lu, clearing bot cache\n", s_SessionEpoch);
    
    // Clear bot cache
    if (s_CritSecInitialized) {
        EnterCriticalSection(&s_BotPlayersCS);
    }
    size_t count = s_BotPlayers.size();
    s_BotPlayers.clear();
    if (s_CritSecInitialized) {
        LeaveCriticalSection(&s_BotPlayersCS);
    }
    
    DebugLog("[GameManager] OnRoundStart: Cleared %zu bot entries, cooldown 2s\n", count);
}

void GameManager::OnGameDestroy() {
    DebugLog("[GameManager] OnGameDestroy: GameManager destroyed, epoch=%lu\n", s_SessionEpoch);

    // Set this before clearing caches so the render thread cannot immediately
    // reacquire the stale static GameManager pointer during scene teardown.
    InterlockedExchange(&s_BlockSessionRefresh, 1);
    
    // Increment session epoch
    s_SessionEpoch++;
    
    // Clear all runtime caches
    ClearRuntimeCaches("GameManager destroyed");
}

void GameManager::OnRoomChanged() {
    // Keep for compatibility, but delegate to OnRoundStart
    OnRoundStart();
}

// Check if player is in current GM's alive player lists
bool GameManager::IsPlayerInCurrentRoom(void* player) {
    if (!player || !s_gameManagerInstance) return false;
    
    // Check playersBL_Alive (List<Player> at +0x24)
    void* listBL = nullptr;
    if (SafeReadValue<void*>((char*)s_gameManagerInstance + OffsetConstants::GM_playersBL_Alive, &listBL)
        && listBL && IsValidPointer(listBL)) {
        void* items = nullptr;
        int count = 0;
        if (SafeReadValue<void*>((char*)listBL + OffsetConstants::List_items, &items)
            && SafeReadValue<int>((char*)listBL + OffsetConstants::List_size, &count)
            && count > 0 && count <= 32 && items && IsValidPointer(items)) {
            for (int i = 0; i < count; i++) {
                void* p = nullptr;
                if (SafeReadValue<void*>((char*)items + OffsetConstants::Arr_data + i * sizeof(void*), &p)) {
                    if (p == player) return true;
                }
            }
        }
    }
    
    // Check playersGR_Alive (List<Player> at +0x2C)
    void* listGR = nullptr;
    if (SafeReadValue<void*>((char*)s_gameManagerInstance + OffsetConstants::GM_playersGR_Alive, &listGR)
        && listGR && IsValidPointer(listGR)) {
        void* items = nullptr;
        int count = 0;
        if (SafeReadValue<void*>((char*)listGR + OffsetConstants::List_items, &items)
            && SafeReadValue<int>((char*)listGR + OffsetConstants::List_size, &count)
            && count > 0 && count <= 32 && items && IsValidPointer(items)) {
            for (int i = 0; i < count; i++) {
                void* p = nullptr;
                if (SafeReadValue<void*>((char*)items + OffsetConstants::Arr_data + i * sizeof(void*), &p)) {
                    if (p == player) return true;
                }
            }
        }
    }
    
    // Fallback: check allPlayers array (Player[] at +0x1C)
    void* allPlayersPtr = nullptr;
    if (SafeReadValue<void*>((char*)s_gameManagerInstance + OffsetConstants::GM_allPlayers, &allPlayersPtr)
        && allPlayersPtr && IsValidPointer(allPlayersPtr)) {
        int count = 0;
        if (SafeReadValue<int>((char*)allPlayersPtr + OffsetConstants::Arr_len, &count)
            && count > 0 && count <= 64) {
            for (int i = 0; i < count; i++) {
                void* p = nullptr;
                if (SafeReadValue<void*>((char*)allPlayersPtr + OffsetConstants::Arr_data + i * sizeof(void*), &p)) {
                    if (p == player) return true;
                }
            }
        }
    }
    
    return false;
}

void GameManager::OnBotUpdate(void* botInstance) {
    if (!HasActiveSession() || !botInstance || !IsValidPointer(botInstance)) return;
    
    DWORD currentTime = GetTickCount();
    
    // Skip Bot.Update during round change cooldown (2 seconds)
    if (currentTime - s_LastRoundChangeTime < ROUND_CHANGE_COOLDOWN_MS) {
        return;
    }

    void* player = nullptr;
    if (!SafeReadValue<void*>((char*)botInstance + 0x24, &player) || !player) return;
    
    // Validate player pointer
    if (!IsValidPointer(player) || !IsValidPlayer(player)) return;
    
    // CRITICAL: Check if player is in current room's allPlayers
    if (!IsPlayerInCurrentRoom(player)) {
        static int rejectCount = 0;
        if (rejectCount++ % 60 == 0) {
            DebugLog("[GameManager] OnBotUpdate: Rejected player 0x%p (not in current room)\n", player);
        }
        return;
    }
    
    // Thread-safe write with current epoch
    if (s_CritSecInitialized) {
        EnterCriticalSection(&s_BotPlayersCS);
    }
    
    BotPlayerEntry entry;
    entry.player = player;
    entry.timestamp = currentTime;
    entry.epoch = s_SessionEpoch;  // Use current epoch
    s_BotPlayers[player] = entry;
    
    if (s_CritSecInitialized) {
        LeaveCriticalSection(&s_BotPlayersCS);
    }
}

std::vector<void*> GameManager::GetBotPlayers() {
    std::vector<void*> players;
    
    if (!HasActiveSession()) {
        if (s_CritSecInitialized) {
            EnterCriticalSection(&s_BotPlayersCS);
        }
        size_t count = s_BotPlayers.size();
        if (count > 0) {
            DebugLog("[GameManager] GetBotPlayers: Clearing %zu bot players (no session)\n", count);
        }
        s_BotPlayers.clear();
        if (s_CritSecInitialized) {
            LeaveCriticalSection(&s_BotPlayersCS);
        }
        return players;
    }

    DWORD currentTime = GetTickCount();
    DWORD currentEpoch = s_SessionEpoch;
    int expiredCount = 0;
    int invalidCount = 0;
    int epochMismatchCount = 0;
    
    if (s_CritSecInitialized) {
        EnterCriticalSection(&s_BotPlayersCS);
    }
    
    for (auto it = s_BotPlayers.begin(); it != s_BotPlayers.end();) {
        void* player = it->first;
        DWORD timestamp = it->second.timestamp;
        DWORD epoch = it->second.epoch;
        
        // Check epoch mismatch (cross-round protection)
        if (epoch != currentEpoch) {
            it = s_BotPlayers.erase(it);
            epochMismatchCount++;
            continue;
        }
        
        // Check timestamp expiration
        if (currentTime - timestamp > BOT_ENTRY_TIMEOUT_MS) {
            it = s_BotPlayers.erase(it);
            expiredCount++;
            continue;
        }
        
        // Check pointer validity
        void* klass = nullptr;
        bool isValid = player && IsValidPointer(player) &&
                       SafeReadValue<void*>(player, &klass) && 
                       klass && IsValidPointer(klass) &&
                       IsValidPlayer(player);
        
        if (isValid) {
            players.push_back(player);
            ++it;
        } else {
            it = s_BotPlayers.erase(it);
            invalidCount++;
        }
    }
    
    if (s_CritSecInitialized) {
        LeaveCriticalSection(&s_BotPlayersCS);
    }
    
    static int logCounter = 0;
    if (logCounter++ % 60 == 0) {
        DebugLog("[GameManager] GetBotPlayers: total=%zu, epochMismatch=%d, expired=%d, invalid=%d, valid=%zu, epoch=%lu\n",
                 s_BotPlayers.size(), epochMismatchCount, expiredCount, invalidCount, players.size(), currentEpoch);
    }
    
    return players;
}

}
