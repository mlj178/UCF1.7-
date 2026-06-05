#pragma once

#include "il2cpp_bridge.h"
#include "transform_helper.h"

struct Vector2 {
    float x, y;
};

class CoordConverter {
public:
    static bool Initialize();
    static bool WorldToScreen(const Vector3& world, Vector2* outScreen);
    static void CalculateBoxSize(float distance, float* width, float* height);
    static bool IsOnScreen(const Vector2& screen, float width, float height);
    
private:
    static void* s_MainCamera;
    static Il2CppClass* s_CameraClass;
    static MethodInfo* s_GetMainMethod;
    static MethodInfo* s_WorldToScreenMethod;
};
