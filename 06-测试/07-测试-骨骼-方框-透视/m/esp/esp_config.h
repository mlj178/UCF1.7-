#pragma once

#include "../imgui/imgui.h"

namespace ESPConfig {
    constexpr float ESP_BASE_SIZE = 50.0f;
    constexpr float BOX_THICKNESS = 1.5f;
    constexpr float MAX_DISTANCE = 100.0f;
    constexpr float MIN_DISTANCE = 1.0f;
    
    const ImVec4 COLOR_TEAM1 = ImVec4(0.78f, 0.80f, 0.82f, 1.0f);
    const ImVec4 COLOR_TEAM2 = ImVec4(0.5f, 0.6f, 0.7f, 1.0f);
    const ImVec4 COLOR_TEAM1_HIDDEN = ImVec4(0.78f, 0.80f, 0.82f, 0.5f);
    const ImVec4 COLOR_TEAM2_HIDDEN = ImVec4(0.5f, 0.6f, 0.7f, 0.5f);
    
    constexpr int LOG_INTERVAL = 60;
}
