#pragma once
#include "esp_common.h"
#include "game_manager.h"

namespace esp {

class ESPRenderer {
public:
    static void Render();
    static void DrawPlayerESP(void* player, void* localPlayer);
    static void DrawPlayerESPFallback(void* player, void* localPlayer, bool shouldLog);
    static void DrawBox(const Vector2& center, float width, float height,
                       const ImVec4& color, float thickness = 1.5f);
    // 血量覆盖层：按 ESPState 里的 HealthMode / HealthDisplay 决定画血条、数值或两者。
    static void DrawHealthOverlay(const Vector2& center, float width, float height,
                                  const PlayerHealthInfo& health);

    static ImVec4 GetPlayerColor(void* player, void* localPlayer);

    static bool& Enabled() { return s_Enabled; }
    static bool IsInitialized() { return s_Initialized; }

    static bool Initialize();

private:
    static bool s_Enabled;
    static bool s_Initialized;
    static int s_FrameCounter;
};

}
