#pragma once
#include "esp_common.h"
#include "il2cpp_bridge.h"

namespace esp {

// ESP bounding box data (2D screen-space box from CharacterController bounds)
struct HitboxESPData {
    bool valid;
    int method;             // 0=none, 1=Bounds, 2=hitbox fallback
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

    // Bounds-based ESP data retrieval (primary method)
    static HitboxESPData GetHitboxData(void* player);

    static bool IsInitialized() { return s_Initialized; }

    // Collider.get_bounds_Injected function pointer (public for SafeCallGetBounds)
    typedef void (__cdecl *GetBoundsInjectedFn)(void* collider, void* bounds, void* methodInfo);
    static GetBoundsInjectedFn s_GetBoundsFunc;

private:
    static bool s_Initialized;

    // Bounds-based ESP (from CharacterController)
    static HitboxESPData GetBoundsData(void* player);

    // Hitbox-based fallback (from CharacterModel.hitboxes)
    static HitboxESPData GetHitboxFallbackData(void* player);
};

}
