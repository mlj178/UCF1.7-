#include "game_manager.h"
#include "esp_log.h"
#include <stdio.h>

void* GameManager::s_Instance = NULL;
Il2CppClass* GameManager::s_Class = NULL;
FieldInfo* GameManager::s_InstanceField = NULL;
MethodInfo* GameManager::s_GetLocalPlayerMethod = NULL;

bool GameManager::Initialize() {
    dbg("[GameManager] Initialize start");
    
    dbg("[GameManager] Calling GetClass...");
    s_Class = IL2CPPBridge::GetClass("Assembly-CSharp.dll", "Assembly-CSharp", "GameManager");
    if (!s_Class) {
        dbg("[GameManager] Class not found");
        return false;
    }
    dbg("[GameManager] Class found at 0x%p", s_Class);
    
    dbg("[GameManager] Calling GetField for Instance...");
    s_InstanceField = IL2CPPBridge::GetField(s_Class, "Instance");
    if (!s_InstanceField) {
        dbg("[GameManager] Instance field not found");
        return false;
    }
    dbg("[GameManager] Instance field found at 0x%p", s_InstanceField);
    
    dbg("[GameManager] Calling GetMethod for get_LocalPlayer...");
    s_GetLocalPlayerMethod = IL2CPPBridge::GetMethod(s_Class, "get_LocalPlayer", 0);
    dbg("[GameManager] get_LocalPlayer method: 0x%p", s_GetLocalPlayerMethod);
    
    dbg("[GameManager] Initialized OK");
    return true;
}

void* GameManager::GetInstance() {
    if (s_Instance) return s_Instance;
    
    if (!s_InstanceField) return NULL;
    
    s_Instance = IL2CPPBridge::GetStaticFieldValue(s_InstanceField);
    if (s_Instance) {
        dbg("[GameManager] Instance found at 0x%p", s_Instance);
    }
    
    return s_Instance;
}

void* GameManager::GetLocalPlayer() {
    void* instance = GetInstance();
    if (!instance) return NULL;
    
    if (!s_GetLocalPlayerMethod) {
        return IL2CPPBridge::ReadField<void*>(instance, 0x10);
    }
    
    void* result = IL2CPPBridge::Invoke(s_GetLocalPlayerMethod, instance, NULL);
    return result;
}

std::vector<void*> GameManager::GetAllPlayers() {
    std::vector<void*> players;
    
    void* instance = GetInstance();
    if (!instance) return players;
    
    void* playersBL = IL2CPPBridge::ReadField<void*>(instance, 0x20);
    void* playersGR = IL2CPPBridge::ReadField<void*>(instance, 0x28);
    
    auto readPlayerList = [&players](void* list) {
        if (!list) return;
        
        void* playersArrayPtr = IL2CPPBridge::ReadField<void*>(list, 0x0);
        void** playersArray = (void**)playersArrayPtr;
        int count = IL2CPPBridge::ReadField<int>(list, 0x4);
        
        if (playersArray && count > 0 && count < 100) {
            for (int i = 0; i < count; i++) {
                void* player = playersArray[i];
                if (player && IsValidPlayer(player)) {
                    players.push_back(player);
                }
            }
        }
    };
    
    readPlayerList(playersBL);
    readPlayerList(playersGR);
    
    return players;
}

bool GameManager::IsValidPlayer(void* player) {
    if (!player) return false;
    return true;
}

bool GameManager::IsPlayerDead(void* player) {
    if (!player) return false;
    
    int health = IL2CPPBridge::ReadField<int>(player, 0x9C);
    return health <= 0;
}

int GameManager::GetPlayerTeam(void* player) {
    if (!player) return 0;
    
    return IL2CPPBridge::ReadField<int>(player, 0x20);
}
