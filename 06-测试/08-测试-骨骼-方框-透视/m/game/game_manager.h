#pragma once
#include "../il2cpp/il2cpp_api.h"
#include "player.h"
#include <vector>

class GameManager {
public:
    static GameManager& Instance();
    
    bool Initialize();
    void Update();
    
    std::vector<PlayerData> GetAllPlayers();
    PlayerData GetLocalPlayer();
    
private:
    GameManager() = default;
    ~GameManager() = default;
    
    IL2CPP::Class m_GameManagerClass;
    IL2CPP::Method m_GetAllPlayersMethod;
    IL2CPP::Method m_GetLocalPlayerMethod;
    
    bool m_Initialized = false;
};
