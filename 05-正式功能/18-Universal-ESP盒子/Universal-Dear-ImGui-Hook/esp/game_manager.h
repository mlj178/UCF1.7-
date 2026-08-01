#pragma once
#include <vector>
#include <unordered_map>
#include <windows.h>
#include "esp_common.h"  // 需要 IsValidPointer, SafeReadValue
#include "il2cpp_bridge.h"

namespace esp {

// Bot player entry with timestamp and epoch for cross-round protection
struct BotPlayerEntry {
    void* player;
    DWORD timestamp;  // GetTickCount() timestamp
    DWORD epoch;      // Session epoch for cross-round protection
};

class GameManager {
public:
    static bool Initialize();
    static bool IsInitialized();
    static void ResetSessionState();
    static void Cleanup();  // Cleanup resources including critical section
    static bool RefreshSession();
    static bool HasActiveSession();
    
    static void* GetInstance();
    static void* GetLocalPlayer();
    static std::vector<void*> GetAllPlayers();
    
    static bool IsValidPlayer(void* player);
    static bool IsPlayerDead(void* player);
    static bool GetPlayerHealth(void* player, float* outRate);
    static int GetPlayerTeam(void* player);
    
    // Bot Hook相关
    static void InitializeBotHook();
    static void InitializeRoomHooks();  // Room change detection hooks
    static std::vector<void*> GetBotPlayers();
    static void OnBotUpdate(void* botInstance);
    static void OnRoomChanged();  // Called when room changes
    static void OnRoundStart();   // Called when new game round starts
    static void OnGameDestroy();  // Called when GameManager is destroyed
    
private:
    // Bot Hook相关成员
    static void ClearRuntimeCaches(const char* reason);
    static bool IsPlayerInCurrentRoom(void* player);  // Check if player is in current GM.allPlayers
    static std::unordered_map<void*, BotPlayerEntry> s_BotPlayers;  // 改为带时间戳的map
    static bool s_BotHookInitialized;
    static CRITICAL_SECTION s_BotPlayersCS;  // 线程同步临界区
    static bool s_CritSecInitialized;
    
    // Session epoch for cross-round protection
    static DWORD s_SessionEpoch;
    static DWORD s_LastRoundChangeTime;
    
    // 时间戳过期配置
    static constexpr DWORD BOT_ENTRY_TIMEOUT_MS = 5000;  // 5秒过期
    static constexpr DWORD ROUND_CHANGE_COOLDOWN_MS = 2000;  // 2秒冷却期
};

}
