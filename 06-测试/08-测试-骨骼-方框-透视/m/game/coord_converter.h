#pragma once
#include "../il2cpp/il2cpp_api.h"

class CoordConverter {
public:
    static CoordConverter& Instance();
    
    bool Initialize();
    bool WorldToScreen(const IL2CPP::Vector3& world, IL2CPP::Vector2* screen);
    
private:
    CoordConverter() = default;
    ~CoordConverter() = default;
    
    IL2CPP::Class m_CameraClass;
    IL2CPP::Method m_WorldToScreenMethod;
    void* m_MainCamera;
    
    bool m_Initialized = false;
};
