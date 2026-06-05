#include "transform_helper.h"
#include "coord_converter.h"
#include "../stdafx.h"
#include <cmath>

namespace esp {

// 使用RVA常量（直接访问静态成员）

// Function pointer types (verified from script.json / aimbot v2.js)
// Component.get_transform: Transform*(Component*, MethodInfo*)
// Transform.get_position: void(Vector3* ret, Transform* transform, MethodInfo*)
typedef void* (__cdecl *GetTransformFn)(void* component, void* methodInfo);
typedef void (__cdecl *GetPositionFn)(void* result, void* transform, void* methodInfo);
static GetTransformFn s_GetTransformFunc = nullptr;
static GetPositionFn s_GetPositionFunc = nullptr;
bool TransformHelper::s_Initialized = false;

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

static bool IsSanePosition(const Vector3& pos) {
    if (std::abs(pos.x) < 0.001f && std::abs(pos.y) < 0.001f && std::abs(pos.z) < 0.001f) {
        return false;
    }

    if (std::abs(pos.x) > 1000.f || std::abs(pos.y) > 1000.f || std::abs(pos.z) > 1000.f) {
        return false;
    }

    // Observed invalid room-transition/container values look like (3000+, 0, 0).
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
    
    // 获取函数地址
    s_GetTransformFunc = (GetTransformFn)((char*)gameAssemblyBase + RVAConstants::Component_get_transform);
    s_GetPositionFunc = (GetPositionFn)((char*)gameAssemblyBase + RVAConstants::Transform_get_position);
    if (!IsExecutableAddress((void*)s_GetTransformFunc) || !IsExecutableAddress((void*)s_GetPositionFunc)) {
        DebugLog("[TransformHelper] ERROR: transform function address is not executable\n");
        s_GetTransformFunc = nullptr;
        s_GetPositionFunc = nullptr;
        return false;
    }
    
    DebugLog("[TransformHelper] get_transform func at 0x%p (RVA+0x%lX)\n", 
             s_GetTransformFunc, RVAConstants::Component_get_transform);
    DebugLog("[TransformHelper] get_position func at 0x%p (RVA+0x%lX)\n", 
             s_GetPositionFunc, RVAConstants::Transform_get_position);
    
    s_Initialized = true;
    DebugLog("[TransformHelper] Initialized successfully\n");
    return true;
}

void* TransformHelper::GetTransform(void* player) {
    if (!s_GetTransformFunc || !player) return nullptr;

    // Validate player pointer
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

    // characterContainer is a Transform* (confirmed from dump.cs: offset 0x58)
    // We must call Transform.get_position() on it, NOT read raw offsets.
    void* container = nullptr;
    if (SafeReadValue<void*>((char*)player + OffsetConstants::P_characterContainer, &container)
        && container && IsValidPointer(container)) {
        // Call Transform.get_position() on the characterContainer Transform
        Vector3 pos = GetPosition(container);
        if (IsSanePosition(pos)) {
            return pos;
        }
        LogRejectedPosition("characterContainer", pos);
    }

    // Fallback: use Component.get_transform() + Transform.get_position()
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

    // Validate transform pointer
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

// Get hitbox-based ESP data (2D bounding box from CharacterModel.hitboxes)
HitboxESPData TransformHelper::GetHitboxData(void* player) {
    HitboxESPData data = {};
    data.valid = false;
    data.hitboxCount = 0;
    data.validWorldCount = 0;
    data.validScreenCount = 0;
    data.left = 99999.f;
    data.right = -99999.f;
    data.top = 99999.f;
    data.bottom = -99999.f;
    if (!player || !IsValidPointer(player)) return data;

    // One-time diagnostic logging
    static int diagCounter = 0;
    int diagIdx = diagCounter++;
    bool shouldDiag = (diagIdx < 3) || (diagIdx % 600 == 0);

    // Step 1: Get currentCharacter
    void* currentCharacter = nullptr;
    if (!SafeReadValue<void*>((char*)player + OffsetConstants::P_currentCharacter, &currentCharacter)
        || !currentCharacter || !IsValidPointer(currentCharacter)) {
        if (shouldDiag) DebugLog("[HitboxDiag] player=0x%p currentCharacter null\n", player);
        return data;
    }

    // Helper lambda to add a transform point
    int neckAdded = 0, helmetAdded = 0;
    auto addTransformPoint = [&](uintptr_t offset) -> bool {
        void* tf = nullptr;
        if (SafeReadValue<void*>((char*)currentCharacter + offset, &tf)
            && tf && IsValidPointer(tf)) {
            Vector3 world = GetPosition(tf);
            if (IsSanePosition(world)) {
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

    // Step 2: Get hitboxes array (Transform[] at +0x74) - body hitboxes
    void* hitboxesArr = nullptr;
    if (SafeReadValue<void*>((char*)currentCharacter + OffsetConstants::CM_hitboxes, &hitboxesArr)
        && hitboxesArr && IsValidPointer(hitboxesArr)) {
        int count = 0;
        if (SafeReadValue<int>((char*)hitboxesArr + OffsetConstants::Arr_len, &count)
            && count > 0 && count <= 64) {
            data.hitboxCount = count;

            // Iterate hitbox transforms
            for (int i = 0; i < count; i++) {
                void* tf = nullptr;
                if (!SafeReadValue<void*>((char*)hitboxesArr + OffsetConstants::Arr_data + i * sizeof(void*), &tf)
                    || !tf || !IsValidPointer(tf)) {
                    continue;
                }

                Vector3 world = GetPosition(tf);
                if (!IsSanePosition(world)) continue;
                data.validWorldCount++;

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

    // Step 3: ALWAYS add neck/spine/spine1 as fixed supplement points (not fallback!)
    // These provide head top and body stability
    neckAdded = addTransformPoint(OffsetConstants::CM_neck) ? 1 : 0;
    addTransformPoint(OffsetConstants::CM_spine);
    addTransformPoint(OffsetConstants::CM_spine1);

    // Step 4: Add helmet collider as head supplement
    void* helmet = nullptr;
    if (SafeReadValue<void*>((char*)currentCharacter + OffsetConstants::CM_helmet, &helmet)
        && helmet && IsValidPointer(helmet)) {
        void* helmetCollider = nullptr;
        if (SafeReadValue<void*>((char*)helmet + OffsetConstants::Helmet_collider, &helmetCollider)
            && helmetCollider && IsValidPointer(helmetCollider)) {
            // Get transform from collider
            void* helmetTf = GetTransform(helmetCollider);
            if (helmetTf && IsValidPointer(helmetTf)) {
                Vector3 world = GetPosition(helmetTf);
                if (IsSanePosition(world)) {
                    Vector2 screen;
                    if (CoordConverter::WorldToScreen(world, &screen)) {
                        data.left = (std::min)(data.left, screen.x);
                        data.right = (std::max)(data.right, screen.x);
                        data.top = (std::min)(data.top, screen.y);
                        data.bottom = (std::max)(data.bottom, screen.y);
                        data.validScreenCount++;
                        helmetAdded = 1;
                    }
                }
            }
        }
    }

    // Check if we have enough points
    if (data.validScreenCount < 2 || data.left >= data.right || data.top >= data.bottom) {
        if (shouldDiag) DebugLog("[HitboxDiag] player=0x%p insufficient points: screenCount=%d\n", player, data.validScreenCount);
        return data;
    }

    // Calculate final box
    data.width = data.right - data.left;
    data.height = data.bottom - data.top;
    data.centerX = (data.left + data.right) * 0.5f;
    data.centerY = (data.top + data.bottom) * 0.5f;

    // Handle too-narrow boxes
    if (data.width < data.height * 0.30f) {
        data.width = data.height * 0.40f;
    }

    // Validate final box
    if (data.height < 4.0f || data.height > 800.0f) {
        if (shouldDiag) DebugLog("[HitboxDiag] player=0x%p invalid height: %.1f\n", player, data.height);
        return data;
    }

    data.valid = true;

    if (shouldDiag) {
        DebugLog("[HitboxDiag] player=0x%p hbc=%d screen=%d box=%.1fx%.1f neck=%d helmet=%d\n",
                 player, data.hitboxCount, data.validScreenCount,
                 data.width, data.height, neckAdded, helmetAdded);
    }

    return data;
}

}
