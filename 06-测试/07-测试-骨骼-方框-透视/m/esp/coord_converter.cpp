#include "coord_converter.h"
#include "esp_config.h"
#include "esp_log.h"
#include <windows.h>
#include <cmath>

void* CoordConverter::s_MainCamera = NULL;
Il2CppClass* CoordConverter::s_CameraClass = NULL;
MethodInfo* CoordConverter::s_GetMainMethod = NULL;
MethodInfo* CoordConverter::s_WorldToScreenMethod = NULL;

bool CoordConverter::Initialize() {
    s_CameraClass = IL2CPPBridge::GetClass("UnityEngine.CoreModule.dll", "UnityEngine", "Camera");
    if (!s_CameraClass) {
        dbg("[Camera] Class not found");
        return false;
    }
    
    s_GetMainMethod = IL2CPPBridge::GetMethod(s_CameraClass, "get_main", 0);
    s_WorldToScreenMethod = IL2CPPBridge::GetMethod(s_CameraClass, "WorldToScreenPoint", 1);
    
    if (!s_GetMainMethod) {
        dbg("[Camera] get_main not found");
    }
    
    if (!s_WorldToScreenMethod) {
        dbg("[Camera] WorldToScreenPoint not found");
    }
    
    dbg("[CoordConverter] Initialized OK");
    return true;
}

bool CoordConverter::WorldToScreen(const Vector3& world, Vector2* outScreen) {
    if (!outScreen) return false;
    
    if (!s_MainCamera && s_GetMainMethod) {
        s_MainCamera = IL2CPPBridge::Invoke(s_GetMainMethod, NULL, NULL);
        if (s_MainCamera) {
            dbg("[Camera] Main camera found at 0x%p", s_MainCamera);
        }
    }
    
    if (!s_MainCamera) return false;
    if (!s_WorldToScreenMethod) return false;
    
    Vector3 screenPos = {0, 0, 0};
    void* args[1] = {(void*)&world};
    void* result = IL2CPPBridge::Invoke(s_WorldToScreenMethod, s_MainCamera, args);
    
    if (result) {
        screenPos = *(Vector3*)result;
    }
    
    outScreen->x = screenPos.x;
    outScreen->y = screenPos.y;
    
    HWND hwnd = GetForegroundWindow();
    if (hwnd) {
        POINT pt = {(LONG)screenPos.x, (LONG)screenPos.y};
        ScreenToClient(hwnd, &pt);
        outScreen->x = (float)pt.x;
        outScreen->y = (float)pt.y;
    }
    
    return screenPos.z > 0.0f;
}

void CoordConverter::CalculateBoxSize(float distance, float* width, float* height) {
    if (distance < ESPConfig::MIN_DISTANCE) distance = ESPConfig::MIN_DISTANCE;
    if (distance > ESPConfig::MAX_DISTANCE) {
        *width = 0;
        *height = 0;
        return;
    }
    
    float scaleFactor = ESPConfig::ESP_BASE_SIZE / (distance * 0.1f);
    *width = scaleFactor;
    *height = scaleFactor * 2.0f;
}

bool CoordConverter::IsOnScreen(const Vector2& screen, float width, float height) {
    return screen.x > -width && screen.x < 1920 + width &&
           screen.y > -height && screen.y < 1080 + height;
}
