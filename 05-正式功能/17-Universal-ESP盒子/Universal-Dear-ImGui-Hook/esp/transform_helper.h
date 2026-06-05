#pragma once
#include "esp_common.h"
#include "il2cpp_bridge.h"

namespace esp {

// Hitbox-based ESP data (2D bounding box from hitbox transforms)
struct HitboxESPData {
    bool valid;
    int hitboxCount;        // Total hitbox transforms found
    int validWorldCount;    // Valid world positions
    int validScreenCount;   // Valid screen positions after projection
    float left, right, top, bottom;  // 2D bounding box in screen coords
    float width, height;    // Final box dimensions
    float centerX, centerY; // Box center
};

class TransformHelper {
public:
    static bool Initialize();
    static void* GetTransform(void* player);
    static Vector3 GetPosition(void* transform);
    static Vector3 GetPlayerPosition(void* player);

    // Hitbox-based position retrieval (preferred method)
    static HitboxESPData GetHitboxData(void* player);

    static bool IsInitialized() { return s_Initialized; }

private:
    static bool s_Initialized;
};

}
