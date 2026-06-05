#pragma once
#include "../imgui/imgui.h"

struct ESPConfig {
    bool enabled = true;
    bool showBox = true;
    bool showSkeleton = false;
    bool showDistance = true;
    bool showHealth = false;
    
    int openMenuKey = 0x2D;    // VK_INSERT
    int uninjectKey = 0x23;   // VK_END
    int toggleESPKey = 0x70;  // VK_F1
    
    ImVec4 enemyColor = ImVec4(1.0f, 0.0f, 0.0f, 1.0f);
    ImVec4 teamColor = ImVec4(0.0f, 1.0f, 0.0f, 1.0f);
    ImVec4 visibleColor = ImVec4(1.0f, 1.0f, 0.0f, 1.0f);
    
    float boxThickness = 1.0f;
    float skeletonThickness = 1.5f;
    float maxDistance = 500.0f;
    
    bool LoadFromFile(const char* path);
    bool SaveToFile(const char* path);
};

extern ESPConfig g_Config;
