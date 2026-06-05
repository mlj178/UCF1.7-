#pragma once

#include "coord_converter.h"
#include "../imgui/imgui.h"

class ESPRenderer {
public:
    static bool s_Enabled;
    
    static void Render();
    static void DrawPlayerESP(void* player, void* localPlayer);
    static void DrawBox(const Vector2& center, float width, float height, 
                       const ImVec4& color, float thickness = 1.0f);
    static ImVec4 GetPlayerColor(void* player, bool isVisible);
};
