#pragma once
#include <cmath>
#include <cstring>
#include <windows.h>
#include "../imgui/imgui.h"

// Use standard C++ exceptions for compatibility
#define SAFE_TRY try
#define SAFE_EXCEPT catch(...) { return false; }
#define SAFE_EXCEPT_RET(x) catch(...) { return x; }
#define SAFE_EXCEPT_NOP catch(...) {}

namespace esp {

struct Vector3 {
    float x, y, z;
    
    Vector3() : x(0), y(0), z(0) {}
    Vector3(float _x, float _y, float _z) : x(_x), y(_y), z(_z) {}
    
    float Distance(const Vector3& other) const {
        float dx = x - other.x;
        float dy = y - other.y;
        float dz = z - other.z;
        return std::sqrt(dx*dx + dy*dy + dz*dz);
    }
};

struct Vector2 {
    float x, y;
    
    Vector2() : x(0), y(0) {}
    Vector2(float _x, float _y) : x(_x), y(_y) {}
};

inline bool SafeReadMemory(void* address, void* buffer, size_t size) {
    if (!address || !buffer || size == 0) return false;

    MEMORY_BASIC_INFORMATION mbi;
    if (VirtualQuery(address, &mbi, sizeof(mbi)) == 0) return false;
    if (mbi.State != MEM_COMMIT) return false;
    if (mbi.Protect & (PAGE_NOACCESS | PAGE_GUARD)) return false;

    uintptr_t start = reinterpret_cast<uintptr_t>(address);
    uintptr_t end = start + size;
    uintptr_t regionEnd = reinterpret_cast<uintptr_t>(mbi.BaseAddress) + mbi.RegionSize;
    if (end < start || end > regionEnd) return false;

#if defined(_MSC_VER)
    __try {
        memcpy(buffer, address, size);
        return true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
#else
    SAFE_TRY {
        memcpy(buffer, address, size);
        return true;
    }
    SAFE_EXCEPT
#endif
}

template<typename T>
inline bool SafeReadValue(void* address, T* outValue) {
    return SafeReadMemory(address, outValue, sizeof(T));
}

inline bool IsValidPointer(void* ptr) {
    if (!ptr) return false;

    return SafeReadMemory(ptr, &ptr, sizeof(ptr));
}

inline bool IsExecutableAddress(void* ptr) {
    if (!ptr) return false;

    MEMORY_BASIC_INFORMATION mbi;
    if (VirtualQuery(ptr, &mbi, sizeof(mbi)) == 0) return false;
    if (mbi.State != MEM_COMMIT) return false;
    if (mbi.Protect & (PAGE_NOACCESS | PAGE_GUARD)) return false;

    const DWORD protection = mbi.Protect & 0xFF;
    return protection == PAGE_EXECUTE ||
           protection == PAGE_EXECUTE_READ ||
           protection == PAGE_EXECUTE_READWRITE ||
           protection == PAGE_EXECUTE_WRITECOPY;
}

namespace config {
    constexpr float BOX_THICKNESS = 1.5f;
    constexpr float MAX_DISTANCE = 100.0f;
    constexpr float MIN_DISTANCE = 1.0f;
    constexpr float PLAYER_HEAD_HEIGHT = 1.65f;  // feet -> head (aimbot v2)
    constexpr float HITBOX_MAX_REF_DIST = 5.0f;   // max distance from player ref pos (meters)
    constexpr float HITBOX_MAX_REF_DIST_SQ = HITBOX_MAX_REF_DIST * HITBOX_MAX_REF_DIST;

    // Box sanity filter
    constexpr float BOX_MAX_WIDTH = 300.0f;       // max screen width (px)
    constexpr float BOX_MAX_HEIGHT = 600.0f;      // max screen height (px)
    constexpr float BOX_MIN_ASPECT = 0.15f;       // min width/height ratio
    constexpr float BOX_MAX_ASPECT = 5.0f;         // max width/height ratio

    constexpr int LOG_INTERVAL = 60;

    // 会话自愈节奏（帧）。退出房间再开新房间时，旧的 GameManager 对象可能已被销毁
    // 但内存仍可读，结构校验会继续通过，缓存就一直指向旧实例、方框再也画不出来。
    // 这里用两个兜底：定期绕过缓存重取单例 + 长时间没有本地玩家就强制重查。
    constexpr int GM_REQUERY_INTERVAL = 30;    // 每 30 帧强制重取一次 GameManager 实例
    constexpr int SESSION_RESYNC_FRAMES = 90;  // 连续 90 帧拿不到本地玩家即强制重查
    
    constexpr ImVec4 COLOR_TEAM1 = {0.78f, 0.80f, 0.82f, 1.0f};
    constexpr ImVec4 COLOR_TEAM2 = {0.5f, 0.6f, 0.7f, 1.0f};
    constexpr ImVec4 COLOR_TEAM1_HIDDEN = {0.78f, 0.80f, 0.82f, 0.5f};
    constexpr ImVec4 COLOR_TEAM2_HIDDEN = {0.5f, 0.6f, 0.7f, 0.5f};
}

}
