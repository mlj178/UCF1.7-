#include "transform_helper.h"
#include "coord_converter.h"
#include "../stdafx.h"
#include <cmath>
#include <algorithm>

namespace esp {

// Function pointer types
// Component.get_transform: Transform*(Component*, MethodInfo*)
// Transform.get_position: void(Vector3* ret, Transform* transform, MethodInfo*)
typedef void* (__cdecl *GetTransformFn)(void* component, void* methodInfo);
typedef void (__cdecl *GetPositionFn)(void* result, void* transform, void* methodInfo);

static GetTransformFn s_GetTransformFunc = nullptr;
static GetPositionFn s_GetPositionFunc = nullptr;
TransformHelper::GetBoundsInjectedFn TransformHelper::s_GetBoundsFunc = nullptr;
bool TransformHelper::s_Initialized = false;

// Unity Bounds struct layout (24 bytes): m_Center(12) + m_Extents(12)
struct UnityBounds {
    Vector3 center;   // offset 0x00
    Vector3 extents;  // offset 0x0C
};

static void* SafeCallGetTransform(GetTransformFn fn, void* component) {
    if (!fn || !component) return nullptr;
#if defined(_MSC_VER)
    __try {
        return fn(component, nullptr);
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return nullptr;
    }
#else
    SAFE_TRY {
        return fn(component, nullptr);
    } SAFE_EXCEPT_RET(nullptr)
#endif
}

static bool SafeCallGetPosition(GetPositionFn fn, void* transform, Vector3* outPos) {
    if (!fn || !transform || !outPos) return false;
#if defined(_MSC_VER)
    __try {
        fn(outPos, transform, nullptr);
        return true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
#else
    SAFE_TRY {
        fn(outPos, transform, nullptr);
        return true;
    } SAFE_EXCEPT_RET(false)
#endif
}

static bool SafeCallGetBounds(TransformHelper::GetBoundsInjectedFn fn, void* collider, UnityBounds* outBounds) {
    if (!fn || !collider || !outBounds) return false;
#if defined(_MSC_VER)
    __try {
        fn(collider, outBounds, nullptr);
        return true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
#else
    SAFE_TRY {
        fn(collider, outBounds, nullptr);
        return true;
    } SAFE_EXCEPT_RET(false)
#endif
}

static bool IsSanePosition(const Vector3& pos) {
    if (std::abs(pos.x) < 0.001f && std::abs(pos.y) < 0.001f && std::abs(pos.z) < 0.001f) {
        return false;
    }
    if (std::abs(pos.x) > 1000.f || std::abs(pos.y) > 1000.f || std::abs(pos.z) > 1000.f) {
        return false;
    }
    if (std::abs(pos.x) > 500.f && std::abs(pos.y) < 0.001f && std::abs(pos.z) < 0.001f) {
        return false;
    }
    return true;
}

static void LogRejectedPosition(const char* source, const Vector3& pos) {
    static int rejectLogCounter = 0;
    if (rejectLogCounter++ % 120 == 0) {
        DebugLog("[TransformHelper] Rejected %s position: (%.2f, %.2f, %.2f)\n",
                 source ? source : "unknown", pos.x, pos.y, pos.z);
    }
}

bool TransformHelper::Initialize() {
    if (s_Initialized) return true;
    if (!IL2CPPBridge::IsInitialized()) {
        DebugLog("[TransformHelper] ERROR: IL2CPPBridge not initialized\n");
        return false;
    }

    void* gameAssemblyBase = IL2CPPBridge::GetBase();
    if (!gameAssemblyBase) {
        DebugLog("[TransformHelper] ERROR: GameAssembly base is null\n");
        return false;
    }

    // Get function addresses
    s_GetTransformFunc = (GetTransformFn)((char*)gameAssemblyBase + RVAConstants::Component_get_transform);
    s_GetPositionFunc = (GetPositionFn)((char*)gameAssemblyBase + RVAConstants::Transform_get_position);
    s_GetBoundsFunc = (GetBoundsInjectedFn)((char*)gameAssemblyBase + RVAConstants::Collider_get_bounds_Injected);

    if (!IsExecutableAddress((void*)s_GetTransformFunc) || !IsExecutableAddress((void*)s_GetPositionFunc)) {
        DebugLog("[TransformHelper] ERROR: transform function address is not executable\n");
        s_GetTransformFunc = nullptr;
        s_GetPositionFunc = nullptr;
        return false;
    }

    if (!IsExecutableAddress((void*)s_GetBoundsFunc)) {
        DebugLog("[TransformHelper] WARNING: get_bounds_Injected address is not executable, Bounds method disabled\n");
        s_GetBoundsFunc = nullptr;
    }

    DebugLog("[TransformHelper] get_transform func at 0x%p (RVA+0x%lX)\n",
             s_GetTransformFunc, RVAConstants::Component_get_transform);
    DebugLog("[TransformHelper] get_position func at 0x%p (RVA+0x%lX)\n",
             s_GetPositionFunc, RVAConstants::Transform_get_position);
    if (s_GetBoundsFunc) {
        DebugLog("[TransformHelper] get_bounds_Injected at 0x%p (RVA+0x%lX)\n",
                 s_GetBoundsFunc, RVAConstants::Collider_get_bounds_Injected);
    }

    s_Initialized = true;
    DebugLog("[TransformHelper] Initialized successfully\n");
    return true;
}

void* TransformHelper::GetTransform(void* player) {
    if (!s_GetTransformFunc || !player) return nullptr;
    if (!IsValidPointer(player)) {
        DebugLog("[TransformHelper] GetTransform: Invalid player pointer\n");
        return nullptr;
    }
    void* transform = SafeCallGetTransform(s_GetTransformFunc, player);
    if (transform && !IsValidPointer(transform)) {
        DebugLog("[TransformHelper] GetTransform returned invalid pointer: 0x%p\n", transform);
        return nullptr;
    }
    return transform;
}

Vector3 TransformHelper::GetPlayerPosition(void* player) {
    if (!player || !IsValidPointer(player)) return Vector3();

    void* container = nullptr;
    if (SafeReadValue<void*>((char*)player + OffsetConstants::P_characterContainer, &container)
        && container && IsValidPointer(container)) {
        Vector3 pos = GetPosition(container);
        if (IsSanePosition(pos)) {
            return pos;
        }
        LogRejectedPosition("characterContainer", pos);
    }

    void* transform = GetTransform(player);
    if (transform) {
        Vector3 pos = GetPosition(transform);
        if (IsSanePosition(pos)) {
            return pos;
        }
        LogRejectedPosition("transform", pos);
    }

    return Vector3();
}

Vector3 TransformHelper::GetPosition(void* transform) {
    if (!s_GetPositionFunc || !transform) return Vector3();
    if (!IsValidPointer(transform)) {
        DebugLog("[TransformHelper] GetPosition: Invalid transform pointer\n");
        return Vector3();
    }
    Vector3 result;
    if (SafeCallGetPosition(s_GetPositionFunc, transform, &result)) {
        return result;
    }
    return Vector3();
}

// ============================================================================
// Primary method: CharacterController Bounds
// Uses Entity.characterController (offset 0x2C) -> Collider.get_bounds_Injected
// Returns 8 corner points of the AABB in world space, projected to screen
// ============================================================================
HitboxESPData TransformHelper::GetBoundsData(void* player) {
    HitboxESPData data = {};
    data.valid = false;
    data.method = 0;
    data.validScreenCount = 0;
    data.left = 99999.f;
    data.right = -99999.f;
    data.top = 99999.f;
    data.bottom = -99999.f;

    if (!s_GetBoundsFunc || !player || !IsValidPointer(player)) return data;

    // Step 1: Read CharacterController from Entity+0x2C
    void* controller = nullptr;
    if (!SafeReadValue<void*>((char*)player + OffsetConstants::E_characterController, &controller)
        || !controller || !IsValidPointer(controller)) {
        return data;
    }

    // Step 2: Call Collider.get_bounds_Injected(controller, &bounds, nullptr)
    UnityBounds bounds;
    memset(&bounds, 0, sizeof(bounds));
    if (!SafeCallGetBounds(s_GetBoundsFunc, controller, &bounds)) {
        return data;
    }

    // Step 3: Validate bounds data
    // extents should be positive and reasonable (character size ~0.3-2.0m)
    if (bounds.extents.x < 0.01f || bounds.extents.y < 0.01f || bounds.extents.z < 0.01f) {
        return data;
    }
    if (bounds.extents.x > 10.f || bounds.extents.y > 10.f || bounds.extents.z > 10.f) {
        return data;
    }
    if (!IsSanePosition(bounds.center)) {
        return data;
    }

    // Step 4: Calculate 8 corner points of the AABB
    // min = center - extents, max = center + extents
    Vector3 bmin, bmax;
    bmin.x = bounds.center.x - bounds.extents.x;
    bmin.y = bounds.center.y - bounds.extents.y;
    bmin.z = bounds.center.z - bounds.extents.z;
    bmax.x = bounds.center.x + bounds.extents.x;
    bmax.y = bounds.center.y + bounds.extents.y;
    bmax.z = bounds.center.z + bounds.extents.z;

    // 8 corners of the AABB
    Vector3 corners[8] = {
        {bmin.x, bmin.y, bmin.z},
        {bmax.x, bmin.y, bmin.z},
        {bmin.x, bmax.y, bmin.z},
        {bmax.x, bmax.y, bmin.z},
        {bmin.x, bmin.y, bmax.z},
        {bmax.x, bmin.y, bmax.z},
        {bmin.x, bmax.y, bmax.z},
        {bmax.x, bmax.y, bmax.z},
    };

    // Step 5: Project all 8 corners to screen space
    int screenCount = 0;
    for (int i = 0; i < 8; i++) {
        Vector2 screen;
        if (CoordConverter::WorldToScreen(corners[i], &screen)) {
            data.left = (std::min)(data.left, screen.x);
            data.right = (std::max)(data.right, screen.x);
            data.top = (std::min)(data.top, screen.y);
            data.bottom = (std::max)(data.bottom, screen.y);
            screenCount++;
        }
    }

    data.validScreenCount = screenCount;

    if (screenCount < 2 || data.left >= data.right || data.top >= data.bottom) {
        return data;
    }

    // Step 6: Calculate final box
    data.width = data.right - data.left;
    data.height = data.bottom - data.top;
    data.centerX = (data.left + data.right) * 0.5f;
    data.centerY = (data.top + data.bottom) * 0.5f;

    // Handle too-narrow boxes
    if (data.width < data.height * 0.30f) {
        data.width = data.height * 0.40f;
    }

    // Validate final box size
    if (data.width > config::BOX_MAX_WIDTH || data.height > config::BOX_MAX_HEIGHT) {
        return data;
    }
    float aspect = data.width / data.height;
    if (aspect < config::BOX_MIN_ASPECT || aspect > config::BOX_MAX_ASPECT) {
        return data;
    }
    if (data.height < 4.0f) {
        return data;
    }

    data.valid = true;
    data.method = 1;
    return data;
}

// ============================================================================
// Fallback method: hitbox transforms (original method, used when Bounds fails)
// ============================================================================
HitboxESPData TransformHelper::GetHitboxFallbackData(void* player) {
    HitboxESPData data = {};
    data.valid = false;
    data.method = 0;
    data.validScreenCount = 0;
    data.left = 99999.f;
    data.right = -99999.f;
    data.top = 99999.f;
    data.bottom = -99999.f;

    if (!player || !IsValidPointer(player)) return data;

    static int diagCounter = 0;
    int diagIdx = diagCounter++;
    bool shouldDiag = (diagIdx < 3) || (diagIdx % 600 == 0);

    // Get currentCharacter
    void* currentCharacter = nullptr;
    if (!SafeReadValue<void*>((char*)player + OffsetConstants::P_currentCharacter, &currentCharacter)
        || !currentCharacter || !IsValidPointer(currentCharacter)) {
        return data;
    }

    // Get player reference position for outlier filtering
    Vector3 refPos = Vector3();
    bool hasRefPos = false;
    void* container = nullptr;
    if (SafeReadValue<void*>((char*)player + OffsetConstants::P_characterContainer, &container)
        && container && IsValidPointer(container)) {
        refPos = GetPosition(container);
        hasRefPos = IsSanePosition(refPos);
    }

    // Helper lambda to add a transform point
    auto addTransformPoint = [&](uintptr_t offset) -> bool {
        void* tf = nullptr;
        if (SafeReadValue<void*>((char*)currentCharacter + offset, &tf)
            && tf && IsValidPointer(tf)) {
            Vector3 world = GetPosition(tf);
            if (IsSanePosition(world)) {
                if (hasRefPos) {
                    float dx = world.x - refPos.x;
                    float dy = world.y - refPos.y;
                    float dz = world.z - refPos.z;
                    if (dx*dx + dy*dy + dz*dz > config::HITBOX_MAX_REF_DIST_SQ) {
                        return false;
                    }
                }
                Vector2 screen;
                if (CoordConverter::WorldToScreen(world, &screen)) {
                    data.left = (std::min)(data.left, screen.x);
                    data.right = (std::max)(data.right, screen.x);
                    data.top = (std::min)(data.top, screen.y);
                    data.bottom = (std::max)(data.bottom, screen.y);
                    data.validScreenCount++;
                    return true;
                }
            }
        }
        return false;
    };

    // Get hitboxes array (Transform[] at +0x74)
    void* hitboxesArr = nullptr;
    if (SafeReadValue<void*>((char*)currentCharacter + OffsetConstants::CM_hitboxes, &hitboxesArr)
        && hitboxesArr && IsValidPointer(hitboxesArr)) {
        int count = 0;
        if (SafeReadValue<int>((char*)hitboxesArr + OffsetConstants::Arr_len, &count)
            && count > 0 && count <= 64) {
            for (int i = 0; i < count; i++) {
                void* tf = nullptr;
                if (!SafeReadValue<void*>((char*)hitboxesArr + OffsetConstants::Arr_data + i * sizeof(void*), &tf)
                    || !tf || !IsValidPointer(tf)) {
                    continue;
                }
                Vector3 world = GetPosition(tf);
                if (!IsSanePosition(world)) continue;
                if (hasRefPos) {
                    float dx = world.x - refPos.x;
                    float dy = world.y - refPos.y;
                    float dz = world.z - refPos.z;
                    if (dx*dx + dy*dy + dz*dz > config::HITBOX_MAX_REF_DIST_SQ) {
                        continue;
                    }
                }
                Vector2 screen;
                if (!CoordConverter::WorldToScreen(world, &screen)) continue;
                data.validScreenCount++;
                data.left = (std::min)(data.left, screen.x);
                data.right = (std::max)(data.right, screen.x);
                data.top = (std::min)(data.top, screen.y);
                data.bottom = (std::max)(data.bottom, screen.y);
            }
        }
    }

    // Add neck/spine/spine1 as supplement points
    addTransformPoint(OffsetConstants::CM_neck);
    addTransformPoint(OffsetConstants::CM_spine);
    addTransformPoint(OffsetConstants::CM_spine1);

    // Add helmet collider
    void* helmet = nullptr;
    if (SafeReadValue<void*>((char*)currentCharacter + OffsetConstants::CM_helmet, &helmet)
        && helmet && IsValidPointer(helmet)) {
        void* helmetCollider = nullptr;
        if (SafeReadValue<void*>((char*)helmet + OffsetConstants::Helmet_collider, &helmetCollider)
            && helmetCollider && IsValidPointer(helmetCollider)) {
            void* helmetTf = GetTransform(helmetCollider);
            if (helmetTf && IsValidPointer(helmetTf)) {
                Vector3 world = GetPosition(helmetTf);
                if (IsSanePosition(world)) {
                    bool tooFar = false;
                    if (hasRefPos) {
                        float dx = world.x - refPos.x;
                        float dy = world.y - refPos.y;
                        float dz = world.z - refPos.z;
                        tooFar = (dx*dx + dy*dy + dz*dz > config::HITBOX_MAX_REF_DIST_SQ);
                    }
                    if (!tooFar) {
                        Vector2 screen;
                        if (CoordConverter::WorldToScreen(world, &screen)) {
                            data.left = (std::min)(data.left, screen.x);
                            data.right = (std::max)(data.right, screen.x);
                            data.top = (std::min)(data.top, screen.y);
                            data.bottom = (std::max)(data.bottom, screen.y);
                            data.validScreenCount++;
                        }
                    }
                }
            }
        }
    }

    if (data.validScreenCount < 2 || data.left >= data.right || data.top >= data.bottom) {
        return data;
    }

    data.width = data.right - data.left;
    data.height = data.bottom - data.top;
    data.centerX = (data.left + data.right) * 0.5f;
    data.centerY = (data.top + data.bottom) * 0.5f;

    if (data.width < data.height * 0.30f) {
        data.width = data.height * 0.40f;
    }

    if (data.width > config::BOX_MAX_WIDTH || data.height > config::BOX_MAX_HEIGHT) {
        if (shouldDiag) DebugLog("[HitboxFallback] player=0x%p box too large: %.1fx%.1f\n", player, data.width, data.height);
        return data;
    }
    float aspect = data.width / data.height;
    if (aspect < config::BOX_MIN_ASPECT || aspect > config::BOX_MAX_ASPECT) {
        return data;
    }
    if (data.height < 4.0f) {
        return data;
    }

    data.valid = true;
    data.method = 2;

    if (shouldDiag) {
        DebugLog("[HitboxFallback] player=0x%p screen=%d box=%.1fx%.1f\n",
                 player, data.validScreenCount, data.width, data.height);
    }

    return data;
}

// ============================================================================
// Main entry: try Bounds first, fallback to hitbox
// ============================================================================
HitboxESPData TransformHelper::GetHitboxData(void* player) {
    static int diagCounter = 0;
    int diagIdx = diagCounter++;
    bool shouldDiag = (diagIdx < 5) || (diagIdx % 600 == 0);

    // Primary: CharacterController Bounds
    if (s_GetBoundsFunc) {
        HitboxESPData data = GetBoundsData(player);
        if (data.valid) {
            if (shouldDiag) {
                DebugLog("[ESPData] player=0x%p method=Bounds box=%.1fx%.1f center=(%.1f,%.1f)\n",
                         player, data.width, data.height, data.centerX, data.centerY);
            }
            return data;
        }
    }

    // Fallback: hitbox transforms
    HitboxESPData data = GetHitboxFallbackData(player);
    if (data.valid && shouldDiag) {
        DebugLog("[ESPData] player=0x%p method=Hitbox box=%.1fx%.1f center=(%.1f,%.1f)\n",
                 player, data.width, data.height, data.centerX, data.centerY);
    }
    return data;
}

}
