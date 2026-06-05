#include "coord_converter.h"
#include "../core/logger.h"

CoordConverter& CoordConverter::Instance() {
    static CoordConverter instance;
    return instance;
}

bool CoordConverter::Initialize() {
    if (m_Initialized) {
        return true;
    }
    
    Il2CppClass* klass = IL2CPP::API::GetClass("UnityEngine.CoreModule", "UnityEngine", "Camera");
    if (!klass) {
        LOG_ERROR("CoordConverter", "Failed to get Camera class");
        return false;
    }
    
    m_CameraClass = IL2CPP::Class(klass);
    
    m_Initialized = true;
    LOG("CoordConverter", "Initialized successfully");
    return true;
}

bool CoordConverter::WorldToScreen(const IL2CPP::Vector3& world, IL2CPP::Vector2* screen) {
    if (!screen) return false;
    // TODO: Implement world to screen conversion
    return false;
}
