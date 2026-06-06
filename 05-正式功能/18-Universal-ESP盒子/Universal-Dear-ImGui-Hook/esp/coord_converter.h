#pragma once
#include "esp_common.h"
#include "il2cpp_bridge.h"

namespace esp {

class CoordConverter {
public:
    static bool Initialize();
    static bool WorldToScreen(const Vector3& world, Vector2* outScreen);
    static void CalculateBoxSize(float distance, float* width, float* height);
    static bool IsOnScreen(const Vector2& screen, float width, float height);
    
    static bool IsInitialized() { return s_Initialized; }
    
private:
    static void* s_MainCamera;
    static MethodInfo* s_WorldToScreenMethod;
    static MethodInfo* s_GetMainCameraMethod;
    static bool s_Initialized;
    
    static HWND s_GameWindow;
};

}
