#pragma once
#include <vector>
#include <cstdint>
#include <windows.h>
#include "esp_common.h"  // 需要 IsValidPointer, SafeReadValue
#include "il2cpp_bridge.h"
#include "player_policy.h"

namespace esp {

enum class ContainerReadState {
    Invalid,
    Empty,
    Valid,
};

struct PlayerCandidate {
    void* player = nullptr;
    std::uint32_t sources = policy::SourceNone;
    DWORD botLastSeenTick = 0;
    DWORD sessionEpoch = 0;
};

struct PlayerSnapshot {
    int gameMode = -1;
    bool roundOver = true;
    DWORD sessionEpoch = 0;
    ContainerReadState allPlayersState = ContainerReadState::Invalid;
    ContainerReadState blState = ContainerReadState::Invalid;
    ContainerReadState grState = ContainerReadState::Invalid;
    ContainerReadState blAliveState = ContainerReadState::Invalid;
    ContainerReadState grAliveState = ContainerReadState::Invalid;
    std::vector<PlayerCandidate> candidates;
};

// 血量信息：rate 为 0~1 的比例（方框图内血条用），current 为解密后的剩余血量
// （ObscuredInt 只读解密），max 仅用于在缺失 rate 时推算比例，界面不显示。
// hasRate / hasValue 表示该来源是否有效。
struct PlayerHealthInfo {
    bool valid = false;
    bool hasRate = false;
    bool hasValue = false;
    float rate = 0.0f;
    int current = 0;
    int max = 0;
};

class GameManager {
public:
    static bool Initialize();
    static bool IsInitialized();
    static void ResetSessionState();
    static void Cleanup();  // 清理会话缓存（已无 MinHook / 临界区资源）
    static bool RefreshSession();
    static bool HasActiveSession();

    static void* GetInstance();
    static void* GetLocalPlayer();
    static std::vector<void*> GetAllPlayers();
    static bool BuildPlayerSnapshot(PlayerSnapshot* outSnapshot);
    static int GetGameMode();
    static bool IsGameRoundOver();
    static bool IsCandidateRenderable(
        const PlayerCandidate& candidate,
        const PlayerSnapshot& snapshot,
        void* localPlayer,
        DWORD now);
    static bool IsEnemy(void* player, void* localPlayer);

    static bool IsValidPlayer(void* player);
    static bool IsPlayerDead(void* player);
    // 读取玩家血量（比例 + 可选的具体数值）。
    static bool GetPlayerHealth(void* player, PlayerHealthInfo* outHealth);
    static int GetPlayerTeam(void* player);

    // 与旧内置菜单（menu.cpp）兼容的入口。
    // 旧实现由 MinHook 回调驱动；现在只做一次同步轮询重扫，不再改写游戏代码。
    static void OnRoundStart();
    static void OnRoomChanged();
};

}
