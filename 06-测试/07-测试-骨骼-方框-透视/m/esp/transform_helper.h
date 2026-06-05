#pragma once

#include "il2cpp_bridge.h"

struct Vector3 {
    float x, y, z;
};

class TransformHelper {
public:
    static bool Initialize();
    static void* GetTransform(void* player);
    static Vector3 GetPosition(void* transform);
    
private:
    static Il2CppClass* s_TransformClass;
    static MethodInfo* s_GetPositionMethod;
};
