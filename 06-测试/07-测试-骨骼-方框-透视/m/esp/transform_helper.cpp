#include "transform_helper.h"
#include "esp_log.h"
#include <stdio.h>

Il2CppClass* TransformHelper::s_TransformClass = NULL;
MethodInfo* TransformHelper::s_GetPositionMethod = NULL;

bool TransformHelper::Initialize() {
    s_TransformClass = IL2CPPBridge::GetClass("UnityEngine.CoreModule.dll", "UnityEngine", "Transform");
    if (!s_TransformClass) {
        dbg("[Transform] Class not found");
        return false;
    }
    
    s_GetPositionMethod = IL2CPPBridge::GetMethod(s_TransformClass, "get_position", 0);
    if (!s_GetPositionMethod) {
        dbg("[Transform] get_position not found, trying get_position_Injected");
        s_GetPositionMethod = IL2CPPBridge::GetMethod(s_TransformClass, "get_position_Injected", 1);
    }
    
    dbg("[Transform] Initialized OK");
    return true;
}

void* TransformHelper::GetTransform(void* player) {
    if (!player) return NULL;
    return IL2CPPBridge::ReadField<void*>(player, 0x54);
}

Vector3 TransformHelper::GetPosition(void* transform) {
    Vector3 pos = {0, 0, 0};
    
    if (!transform) return pos;
    if (!s_GetPositionMethod) return pos;
    
    void* args[1] = {&pos};
    void* result = IL2CPPBridge::Invoke(s_GetPositionMethod, transform, args);
    
    if (result) {
        pos = *(Vector3*)result;
    }
    
    return pos;
}
