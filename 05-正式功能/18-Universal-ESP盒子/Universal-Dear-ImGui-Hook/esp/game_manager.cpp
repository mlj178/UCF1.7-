#include "game_manager.h"
#include "../stdafx.h"
#include <algorithm>
#include <cmath>
#include <unordered_map>

// ============================================================================
// 2026-10-15 闪退修复（P0）——不再对 GameAssembly.dll 打任何 MinHook 内联钩子
//
// 历史实现（已删除）会用 MinHook 挂钩以下游戏函数：
//   - Bot.Update                       (RVA 0xB33370)
//   - ModeBase.OnStartNewGameRound     (RVA 0xAF5B30)   ← Frida「自瞄」也挂同一地址
//   - ModeBase_Nano.OnStartNewGameRound(RVA 0xAF15D0)   ← Frida「强制决战」也挂同一地址
//   - GameManager.OnDestroy            (RVA 0xAFB6F0)
//
// 修改器的 Frida 脚本会在同一段函数头（前 5 字节）上再打一次内联钩子。两个引擎
// 先后改写/搬运同一段代码，trampoline 互相覆盖，属未定义行为；10-11 多人生化
// （终结者）闪退已定性为「双引擎重复挂钩 + 内存损坏」，且崩在补给箱虚调用上。
//
// 现在本 DLL 不改写 GameAssembly.dll 的任何一个代码字节：
//   1. 会话（GameManager 实例）在渲染帧内轮询 + 结构校验，实例变化即视为新会话，
//      自动换 epoch 并丢弃旧候选，不再依赖任何回合/销毁回调；
//   2. Bot 不再单独挂钩采集，玩家统一来自 GameManager 的玩家容器
//      （allPlayers / playersBL / playersGR / *_Alive）；
//   3. DLL 里剩下的 Hook 只有 D3D11 Present / ResizeBuffers 与 kernel32 的
//      LoadLibraryA/W —— 都在系统 DLL 上，Frida 侧不碰，不存在重复挂钩。
// ============================================================================

namespace esp {

static void* s_gameManagerInstance = nullptr;
static bool s_initialized = false;
static bool s_hasActiveSession = false;
// 会话序号：GameManager 实例出现/更换/消失时递增，用于丢弃跨会话残留候选。
static DWORD s_SessionEpoch = 0;

typedef bool (__cdecl *GetIsDeadFn)(void* entity, void* methodInfo);
typedef void* (__cdecl *GetHealthDataFn)(void* entity, void* methodInfo);
typedef float (__cdecl *GetHealthRateFn)(void* healthData, void* methodInfo);
typedef bool (__cdecl *IsSameTeamFn)(int team, int otherTeam, void* methodInfo);

static void ClearSessionCaches(const char* reason) {
    if (s_gameManagerInstance || s_hasActiveSession) {
        DebugLog("[GameManager] Clearing session state: %s\n", reason ? reason : "unknown");
    }
    s_gameManagerInstance = nullptr;
    s_hasActiveSession = false;
    IL2CPPBridge::ResetSessionState();
}

static bool IsSaneCount(int count, int maxCount) {
    return count >= 0 && count <= maxCount;
}

struct PlayerContainerRead {
    ContainerReadState state = ContainerReadState::Invalid;
    std::vector<void*> players;
};

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

static PlayerContainerRead ReadArrayPlayers(void* arrayPtr, int maxCount, const char* label) {
    PlayerContainerRead result;
    if (!arrayPtr || !IsValidPointer(arrayPtr)) return result;

    int length = 0;
    if (!SafeReadValue<int>((char*)arrayPtr + OffsetConstants::Arr_len, &length)) return result;
    if (!IsSaneCount(length, maxCount)) {
        DebugLog("[GameManager] Ignoring %s with invalid length: %d\n", label, length);
        return result;
    }
    if (length == 0) {
        result.state = ContainerReadState::Empty;
        return result;
    }

    for (int i = 0; i < length; ++i) {
        void* player = nullptr;
        if (SafeReadValue<void*>((char*)arrayPtr + OffsetConstants::Arr_data + i * sizeof(void*), &player)) {
            AddUniquePlayer(result.players, player);
        }
    }
    result.state = ContainerReadState::Valid;
    return result;
}

static PlayerContainerRead ReadListPlayers(void* listPtr, int maxCount, const char* label) {
    PlayerContainerRead result;
    if (!listPtr || !IsValidPointer(listPtr)) return result;

    void* items = nullptr;
    int count = 0;
    if (!SafeReadValue<void*>((char*)listPtr + OffsetConstants::List_items, &items)) return result;
    if (!SafeReadValue<int>((char*)listPtr + OffsetConstants::List_size, &count)) return result;
    if (!IsSaneCount(count, maxCount)) {
        DebugLog("[GameManager] Ignoring %s with invalid size: %d\n", label, count);
        return result;
    }
    if (count == 0) {
        result.state = ContainerReadState::Empty;
        return result;
    }
    if (!items || !IsValidPointer(items)) return result;

    for (int i = 0; i < count; ++i) {
        void* player = nullptr;
        if (SafeReadValue<void*>((char*)items + OffsetConstants::Arr_data + i * sizeof(void*), &player)) {
            AddUniquePlayer(result.players, player);
        }
    }
    result.state = ContainerReadState::Valid;
    return result;
}

static void* GetGameManagerStaticFields() {
    void* gameAssembly = IL2CPPBridge::GetBase();
    if (!gameAssembly) return nullptr;

    void* klass = nullptr;
    void* typeInfoSlot = static_cast<char*>(gameAssembly) + RVAConstants::GameManager_TypeInfo;
    if (!SafeReadValue<void*>(typeInfoSlot, &klass) || !klass || !IsValidPointer(klass)) {
        return nullptr;
    }

    void* staticFields = nullptr;
    if (!SafeReadValue<void*>(static_cast<char*>(klass) + OffsetConstants::Klass_staticFields,
                              &staticFields) ||
        !staticFields || !IsValidPointer(staticFields)) {
        return nullptr;
    }
    return staticFields;
}

static void MergeCandidate(
    PlayerSnapshot& snapshot,
    std::unordered_map<void*, size_t>& index,
    void* player,
    std::uint32_t source,
    DWORD botLastSeen = 0,
    DWORD epoch = 0) {
    if (!player) return;

    auto found = index.find(player);
    if (found == index.end()) {
        PlayerCandidate candidate;
        candidate.player = player;
        candidate.sources = source;
        candidate.botLastSeenTick = botLastSeen;
        candidate.sessionEpoch = epoch;
        index.emplace(player, snapshot.candidates.size());
        snapshot.candidates.push_back(candidate);
        return;
    }

    PlayerCandidate& candidate = snapshot.candidates[found->second];
    candidate.sources |= source;
    if (botLastSeen != 0) candidate.botLastSeenTick = botLastSeen;
    if (epoch != 0) candidate.sessionEpoch = epoch;
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

bool GameManager::Initialize() {
    if (s_initialized) return true;
    if (!IL2CPPBridge::IsInitialized()) return false;

    DebugLog("[GameManager] ===== Initialize (polling session, no game hooks) =====\n");

    s_initialized = true;
    RefreshSession();
    return true;
}

bool GameManager::IsInitialized() {
    return s_initialized;
}

void GameManager::ResetSessionState() {
    ClearSessionCaches("explicit reset");
}

void GameManager::Cleanup() {
    DebugLog("[GameManager] Cleanup called.\n");
    ClearSessionCaches("cleanup");
    s_initialized = false;
}

bool GameManager::RefreshSession() {
    if (!s_initialized || !IL2CPPBridge::IsInitialized() || !IL2CPPBridge::IsGameAssemblyReady()) {
        ClearSessionCaches("bridge unavailable");
        return false;
    }

    // 每帧轮询 GameManager 单例；IL2CPPBridge 内部会缓存并逐次校验，
    // 因此只要缓存有效就不会重复调用 SingletonGet。
    void* newInstance = IL2CPPBridge::GetGameManagerInstance();
    if (!newInstance) {
        if (s_hasActiveSession || s_gameManagerInstance) {
            // 离开房间 / 场景销毁：立刻断开会话，避免继续拿旧指针。
            ClearSessionCaches("GameManager unavailable");
            s_SessionEpoch++;
        }
        return false;
    }

    if (newInstance != s_gameManagerInstance) {
        DebugLog("[GameManager] GameManager instance changed: 0x%p -> 0x%p\n",
                 s_gameManagerInstance, newInstance);
        s_gameManagerInstance = newInstance;
        s_SessionEpoch++;
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

    void* staticFields = GetGameManagerStaticFields();
    if (!staticFields) return nullptr;

    void* myPlayer = nullptr;
    if (SafeReadValue<void*>(static_cast<char*>(staticFields) + OffsetConstants::GM_myPlayer,
                             &myPlayer) &&
        IsValidPlayer(myPlayer)) {
        return myPlayer;
    }

    return nullptr;
}

static bool SafeCallIsSameTeam(
    IsSameTeamFn fn,
    int team,
    int otherTeam,
    bool* outSameTeam) {
    if (!fn || !outSameTeam) return false;

#if defined(_MSC_VER)
    __try {
        *outSameTeam = fn(team, otherTeam, nullptr);
        return true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
#else
    SAFE_TRY {
        *outSameTeam = fn(team, otherTeam, nullptr);
        return true;
    } SAFE_EXCEPT_RET(false)
#endif
}

static void LogTeamRuleFallback() {
    static int logCounter = 0;
    if (logCounter++ % config::LOG_INTERVAL == 0) {
        DebugLog("[ESP] ExpandUtil.IsSameTeam unavailable; using verified Neutral fallback\n");
    }
}

int GameManager::GetGameMode() {
    void* staticFields = GetGameManagerStaticFields();
    if (!staticFields) return -1;

    int gameMode = -1;
    if (!SafeReadValue<int>(static_cast<char*>(staticFields) + OffsetConstants::GM_gameMode,
                            &gameMode) ||
        !policy::IsKnownGameMode(gameMode)) {
        return -1;
    }
    return gameMode;
}

bool GameManager::IsGameRoundOver() {
    void* staticFields = GetGameManagerStaticFields();
    if (!staticFields) return true;

    bool roundOver = true;
    if (!SafeReadValue<bool>(
            static_cast<char*>(staticFields) + OffsetConstants::GM_gameRoundOver,
            &roundOver)) {
        return true;
    }
    return roundOver;
}

bool GameManager::BuildPlayerSnapshot(PlayerSnapshot* outSnapshot) {
    if (!outSnapshot) return false;
    *outSnapshot = PlayerSnapshot{};
    if (!RefreshSession() || !s_gameManagerInstance) return false;

    PlayerSnapshot snapshot;
    snapshot.gameMode = GetGameMode();
    snapshot.roundOver = IsGameRoundOver();
    snapshot.sessionEpoch = s_SessionEpoch;

    void* allPlayers = nullptr;
    void* playersBL = nullptr;
    void* playersGR = nullptr;
    void* playersBLAlive = nullptr;
    void* playersGRAlive = nullptr;
    SafeReadValue<void*>(static_cast<char*>(s_gameManagerInstance) + OffsetConstants::GM_allPlayers,
                         &allPlayers);
    SafeReadValue<void*>(static_cast<char*>(s_gameManagerInstance) + OffsetConstants::GM_playersBL,
                         &playersBL);
    SafeReadValue<void*>(static_cast<char*>(s_gameManagerInstance) + OffsetConstants::GM_playersGR,
                         &playersGR);
    SafeReadValue<void*>(
        static_cast<char*>(s_gameManagerInstance) + OffsetConstants::GM_playersBL_Alive,
        &playersBLAlive);
    SafeReadValue<void*>(
        static_cast<char*>(s_gameManagerInstance) + OffsetConstants::GM_playersGR_Alive,
        &playersGRAlive);

    const PlayerContainerRead allRead = ReadArrayPlayers(allPlayers, 64, "allPlayers");
    const PlayerContainerRead blRead = ReadListPlayers(playersBL, 32, "playersBL");
    const PlayerContainerRead grRead = ReadListPlayers(playersGR, 32, "playersGR");
    const PlayerContainerRead blAliveRead =
        ReadListPlayers(playersBLAlive, 32, "playersBL_Alive");
    const PlayerContainerRead grAliveRead =
        ReadListPlayers(playersGRAlive, 32, "playersGR_Alive");

    snapshot.allPlayersState = allRead.state;
    snapshot.blState = blRead.state;
    snapshot.grState = grRead.state;
    snapshot.blAliveState = blAliveRead.state;
    snapshot.grAliveState = grAliveRead.state;

    std::unordered_map<void*, size_t> index;
    index.reserve(allRead.players.size() + blRead.players.size() + grRead.players.size() +
                  blAliveRead.players.size() + grAliveRead.players.size());
    for (void* player : allRead.players) {
        MergeCandidate(snapshot, index, player, policy::SourceAllPlayers, 0, snapshot.sessionEpoch);
    }
    for (void* player : blRead.players) {
        MergeCandidate(snapshot, index, player, policy::SourceBL, 0, snapshot.sessionEpoch);
    }
    for (void* player : grRead.players) {
        MergeCandidate(snapshot, index, player, policy::SourceGR, 0, snapshot.sessionEpoch);
    }
    for (void* player : blAliveRead.players) {
        MergeCandidate(snapshot, index, player, policy::SourceBLAlive, 0, snapshot.sessionEpoch);
    }
    for (void* player : grAliveRead.players) {
        MergeCandidate(snapshot, index, player, policy::SourceGRAlive, 0, snapshot.sessionEpoch);
    }

    *outSnapshot = std::move(snapshot);
    return true;
}

std::vector<void*> GameManager::GetAllPlayers() {
    PlayerSnapshot snapshot;
    std::vector<void*> players;
    if (!BuildPlayerSnapshot(&snapshot)) return players;
    players.reserve(snapshot.candidates.size());
    for (const PlayerCandidate& candidate : snapshot.candidates) {
        players.push_back(candidate.player);
    }
    return players;
}

static bool IsPlayerClassCompatible(void* player, void* localPlayer) {
    void* playerKlass = nullptr;
    void* localKlass = nullptr;
    return player && localPlayer &&
           SafeReadValue<void*>(player, &playerKlass) &&
           SafeReadValue<void*>(localPlayer, &localKlass) &&
           playerKlass && playerKlass == localKlass &&
           IsValidPointer(playerKlass);
}

static bool IsPlayerSpawned(void* player) {
    if (!player) return false;

    void* currentCharacter = nullptr;
    void* characterContainer = nullptr;
    void* characterController = nullptr;
    if (!SafeReadValue<void*>(
            static_cast<char*>(player) + OffsetConstants::P_currentCharacter,
            &currentCharacter) ||
        !SafeReadValue<void*>(
            static_cast<char*>(player) + OffsetConstants::P_characterContainer,
            &characterContainer) ||
        !SafeReadValue<void*>(
            static_cast<char*>(player) + OffsetConstants::E_characterController,
            &characterController)) {
        return false;
    }

    if (!currentCharacter || !IsValidPointer(currentCharacter)) return false;
    const bool hasContainer = characterContainer && IsValidPointer(characterContainer);
    const bool hasController = characterController && IsValidPointer(characterController);
    return hasContainer || hasController;
}

bool GameManager::IsCandidateRenderable(
    const PlayerCandidate& candidate,
    const PlayerSnapshot& snapshot,
    void* localPlayer,
    DWORD now) {
    if (!HasActiveSession() || snapshot.roundOver) return false;
    if (candidate.sessionEpoch != snapshot.sessionEpoch) return false;
    if (!candidate.player || candidate.player == localPlayer) return false;
    if (!IsPlayerClassCompatible(candidate.player, localPlayer)) return false;

    const bool botFresh =
        policy::HasSource(candidate.sources, policy::SourceBotUpdate) &&
        candidate.sessionEpoch == s_SessionEpoch &&
        policy::IsBotFresh(candidate.botLastSeenTick, now);
    if (!policy::IsSourceEligible(snapshot.gameMode, candidate.sources, botFresh)) {
        return false;
    }
    if (IsPlayerDead(candidate.player)) return false;
    if (!IsPlayerSpawned(candidate.player)) return false;
    return true;
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

// ---------------------------------------------------------------------------
// 血量读取
//
// HealthData.currentHealth / maxHealth / tempHealth 都是 CodeStage AntiCheat 的
// ObscuredInt（加密整数），布局（相对字段起点）：
//   currentCryptoKey @ +0x00 (int)
//   hiddenValue      @ +0x04 (int)
//   inited           @ +0x08 (bool)
// 明文 = hiddenValue ^ currentCryptoKey；currentCryptoKey 为 0 时游戏内部会换成
// 静态密钥 0x6C81C（与 37-增加防化服 / 36-增加血量 的实测结论一致）。
//
// 这里只解密读取，不写回任何字段，属于纯只读探测。
// ---------------------------------------------------------------------------
static bool ReadObscuredInt(void* fieldPtr, int* outValue) {
    if (!fieldPtr || !outValue) return false;

    int key = 0;
    int hidden = 0;
    if (!SafeReadValue<int>(static_cast<char*>(fieldPtr) + OffsetConstants::ObscuredInt_key, &key)) {
        return false;
    }
    if (!SafeReadValue<int>(static_cast<char*>(fieldPtr) + OffsetConstants::ObscuredInt_hidden, &hidden)) {
        return false;
    }

    const int resolvedKey = (key != 0) ? key : OffsetConstants::OBSCURED_INT_STATIC_KEY;
    const int value = hidden ^ resolvedKey;
    if (value < 0 || value > 1000000) return false;

    *outValue = value;
    return true;
}

bool GameManager::GetPlayerHealth(void* player, PlayerHealthInfo* outHealth) {
    if (!outHealth) return false;
    *outHealth = PlayerHealthInfo{};

    if (!HasActiveSession() || !player || !IsValidPlayer(player)) return false;

    void* gameAssembly = IL2CPPBridge::GetBase();
    if (!gameAssembly) return false;

    auto getHealthData = (GetHealthDataFn)((char*)gameAssembly + RVAConstants::Entity_get_healthData);
    auto getHealthRate = (GetHealthRateFn)((char*)gameAssembly + RVAConstants::HealthData_get_rate);
    if (!IsExecutableAddress((void*)getHealthData) || !IsExecutableAddress((void*)getHealthRate)) {
        return false;
    }

    void* healthData = nullptr;
    float rate = -1.0f;
    bool callOk = false;
#if defined(_MSC_VER)
    __try {
        healthData = getHealthData(player, nullptr);
        if (healthData) rate = getHealthRate(healthData, nullptr);
        callOk = true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        callOk = false;
    }
#else
    SAFE_TRY {
        healthData = getHealthData(player, nullptr);
        if (healthData) rate = getHealthRate(healthData, nullptr);
        callOk = true;
    } SAFE_EXCEPT_NOP
#endif

    if (!callOk || !healthData || !IsValidPointer(healthData)) return false;

    PlayerHealthInfo info;
    info.hasRate = std::isfinite(rate) && rate > 0.0f && rate <= 1.0f;
    if (info.hasRate) info.rate = rate;

    int current = 0;
    int maxHealth = 0;
    const bool haveCurrent =
        ReadObscuredInt(static_cast<char*>(healthData) + OffsetConstants::HD_currentHealth, &current);
    const bool haveMax =
        ReadObscuredInt(static_cast<char*>(healthData) + OffsetConstants::HD_maxHealth, &maxHealth);

    int temp = 0;
    if (haveCurrent &&
        ReadObscuredInt(static_cast<char*>(healthData) + OffsetConstants::HD_tempHealth, &temp) &&
        temp > 0) {
        // 临时护盾血量会计入实际血量，和游戏 rate 的口径保持一致。
        current += temp;
    }

    if (haveCurrent && haveMax && maxHealth > 0) {
        info.hasValue = true;
        info.current = current;
        info.max = maxHealth;
        if (!info.hasRate) {
            float computed = static_cast<float>(current) / static_cast<float>(maxHealth);
            if (computed > 1.0f) computed = 1.0f;
            info.rate = computed;
            info.hasRate = true;
        }
    } else if (haveCurrent) {
        info.hasValue = true;
        info.current = current;
        info.max = 0;
    }

    info.valid = info.hasRate || info.hasValue;
    if (!info.valid) return false;

    *outHealth = info;
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

bool GameManager::IsEnemy(void* player, void* localPlayer) {
    const int playerTeam = GetPlayerTeam(player);
    const int localTeam = GetPlayerTeam(localPlayer);
    if (playerTeam < 0 || localTeam < 0) return false;

    void* base = IL2CPPBridge::GetBase();
    auto isSameTeam = base
        ? reinterpret_cast<IsSameTeamFn>(
              static_cast<char*>(base) + RVAConstants::ExpandUtil_IsSameTeam)
        : nullptr;

    bool sameTeam = true;
    if (isSameTeam && IsExecutableAddress(reinterpret_cast<void*>(isSameTeam)) &&
        SafeCallIsSameTeam(isSameTeam, localTeam, playerTeam, &sameTeam)) {
        return !sameTeam;
    }

    LogTeamRuleFallback();
    return !policy::IsSameTeamByGameRule(localTeam, playerTeam);
}

// 旧实现由 MinHook 的回合开始回调驱动；现在退化为一次同步轮询重扫。
void GameManager::OnRoundStart() {
    RefreshSession();
}

// 旧内置菜单在关闭 ESP 时调用它清缓存；现在整段清掉再重扫。
void GameManager::OnRoomChanged() {
    ClearSessionCaches("room changed");
    RefreshSession();
}

}
