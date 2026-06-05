#include "esp_renderer.h"
#include "game_manager.h"
#include "transform_helper.h"
#include "esp_config.h"
#include "esp_log.h"
#include <cmath>

bool ESPRenderer::s_Enabled = true;

void ESPRenderer::Render() {
    if (!s_Enabled) return;
    
    void* localPlayer = GameManager::GetLocalPlayer();
    if (!localPlayer) return;
    
    auto players = GameManager::GetAllPlayers();
    
    int drawnCount = 0;
    for (void* player : players) {
        if (player == localPlayer) continue;
        
        int playerTeam = GameManager::GetPlayerTeam(player);
        int localTeam = GameManager::GetPlayerTeam(localPlayer);
        if (playerTeam == localTeam) continue;
        
        if (GameManager::IsPlayerDead(player)) continue;
        
        DrawPlayerESP(player, localPlayer);
        drawnCount++;
    }
    
    static int frameCounter = 0;
    if (++frameCounter % ESPConfig::LOG_INTERVAL == 0) {
        dbg("[ESP] Players: %d, Drawn: %d", (int)players.size(), drawnCount);
    }
}

void ESPRenderer::DrawPlayerESP(void* player, void* localPlayer) {
    void* transform = TransformHelper::GetTransform(player);
    if (!transform) return;
    
    Vector3 worldPos = TransformHelper::GetPosition(transform);
    
    Vector2 screenPos;
    if (!CoordConverter::WorldToScreen(worldPos, &screenPos)) return;
    
    void* localTransform = TransformHelper::GetTransform(localPlayer);
    if (!localTransform) return;
    
    Vector3 localPos = TransformHelper::GetPosition(localTransform);
    
    float dx = worldPos.x - localPos.x;
    float dy = worldPos.y - localPos.y;
    float dz = worldPos.z - localPos.z;
    float distance = std::sqrt(dx*dx + dy*dy + dz*dz);
    
    float width, height;
    CoordConverter::CalculateBoxSize(distance, &width, &height);
    
    if (width <= 0 || height <= 0) return;
    
    if (!CoordConverter::IsOnScreen(screenPos, width, height)) return;
    
    bool isVisible = true;
    ImVec4 color = GetPlayerColor(player, isVisible);
    
    DrawBox(screenPos, width, height, color, ESPConfig::BOX_THICKNESS);
}

void ESPRenderer::DrawBox(const Vector2& center, float w, float h, 
                          const ImVec4& color, float thickness) {
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    
    ImVec2 p1(center.x - w/2, center.y - h/2);
    ImVec2 p2(center.x + w/2, center.y + h/2);
    
    ImU32 col = ImGui::ColorConvertFloat4ToU32(color);
    drawList->AddRect(p1, p2, col, 0.0f, 0, thickness);
}

ImVec4 ESPRenderer::GetPlayerColor(void* player, bool isVisible) {
    int teamID = GameManager::GetPlayerTeam(player);
    
    if (teamID == 0) {
        return isVisible ? ESPConfig::COLOR_TEAM1 : ESPConfig::COLOR_TEAM1_HIDDEN;
    } else {
        return isVisible ? ESPConfig::COLOR_TEAM2 : ESPConfig::COLOR_TEAM2_HIDDEN;
    }
}
