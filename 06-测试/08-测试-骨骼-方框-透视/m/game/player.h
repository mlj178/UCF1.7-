#pragma once
#include "../il2cpp/il2cpp_types.h"

struct PlayerData {
    void* object;
    IL2CPP::Vector3 position;
    int teamId;
    bool isAlive;
    float health;
    bool isVisible;
};
