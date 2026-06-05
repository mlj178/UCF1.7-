#pragma once
#include "../game/player.h"
#include "../imgui/imgui.h"
#include <vector>

class ESPRenderer {
public:
    static ESPRenderer& Instance();
    
    void Render();
    
private:
    ESPRenderer() = default;
    ~ESPRenderer() = default;
    
    void DrawPlayerESP(const PlayerData& player, const PlayerData& localPlayer);
    void DrawBox(const IL2CPP::Vector2& pos, float width, float height, const ImVec4& color);
    void DrawSkeleton(const std::vector<IL2CPP::Vector3>& bones);
    void DrawDistance(const IL2CPP::Vector2& pos, float distance);
    
    ImVec4 GetPlayerColor(const PlayerData& player, bool isVisible);
};
