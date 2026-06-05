#pragma once

#include <vector>
#include "il2cpp_bridge.h"

class GameManager {
public:
    static bool Initialize();
    static void* GetInstance();
    static void* GetLocalPlayer();
    static std::vector<void*> GetAllPlayers();
    
    static bool IsValidPlayer(void* player);
    static bool IsPlayerDead(void* player);
    static int GetPlayerTeam(void* player);
    
private:
    static void* s_Instance;
    static Il2CppClass* s_Class;
    static FieldInfo* s_InstanceField;
    static MethodInfo* s_GetLocalPlayerMethod;
};
