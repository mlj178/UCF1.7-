#include "coord_converter.h"
#include "../stdafx.h"

namespace esp {

void* CoordConverter::s_MainCamera = nullptr;
MethodInfo* CoordConverter::s_WorldToScreenMethod = nullptr;
MethodInfo* CoordConverter::s_GetMainCameraMethod = nullptr;
bool CoordConverter::s_Initialized = false;
HWND CoordConverter::s_GameWindow = nullptr;

// Camera.WorldToScreenPoint_Injected @ RVA 0x327EE0
// void(Camera* this, Vector3* position, int32_t eye, Vector3* ret, MethodInfo* method)
typedef void (__cdecl *WorldToScreenInjectedFn)(void* camera, void* position, int eye, void* result, void* methodInfo);
typedef void* (__cdecl *GetMainCameraFn)(void* methodInfo);

static WorldToScreenInjectedFn s_WorldToScreenFunc = nullptr;
static GetMainCameraFn s_GetMainCameraFunc = nullptr;

static void* SafeCallGetMainCamera(GetMainCameraFn fn) {
    if (!fn) return nullptr;
#if defined(_MSC_VER)
    __try {
        return fn(nullptr);
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return nullptr;
    }
#else
    SAFE_TRY {
        return fn(nullptr);
    } SAFE_EXCEPT_RET(nullptr)
#endif
}

static bool SafeCallWorldToScreen(WorldToScreenInjectedFn fn, void* camera, Vector3* world, Vector3* result) {
    if (!fn || !camera || !world || !result) return false;
#if defined(_MSC_VER)
    __try {
        fn(camera, world, 2, result, nullptr);
        return true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
#else
    SAFE_TRY {
        fn(camera, world, 2, result, nullptr);
        return true;
    } SAFE_EXCEPT_RET(false)
#endif
}

static void* GetMainCamera() {
    if (!s_GetMainCameraFunc) return nullptr;
    void* camera = SafeCallGetMainCamera(s_GetMainCameraFunc);
    if (camera && IsValidPointer(camera)) return camera;
    return nullptr;
}

bool CoordConverter::Initialize() {
    if (s_Initialized) return true;
    if (!IL2CPPBridge::IsInitialized()) {
        DebugLog("[CoordConverter] ERROR: IL2CPPBridge not initialized\n");
        return false;
    }

    s_GameWindow = globals::mainWindow;
    DebugLog("[CoordConverter] Game window: 0x%p\n", s_GameWindow);

    HMODULE gameAssembly = GetModuleHandleA("GameAssembly.dll");
    if (!gameAssembly) {
        DebugLog("[CoordConverter] ERROR: GameAssembly.dll not found\n");
        return false;
    }

    void* base = (void*)gameAssembly;
    s_WorldToScreenFunc = (WorldToScreenInjectedFn)((char*)base + RVAConstants::Camera_WorldToScreenPoint_Injected);
    s_GetMainCameraFunc = (GetMainCameraFn)((char*)base + RVAConstants::Camera_get_main);
    if (!IsExecutableAddress((void*)s_WorldToScreenFunc) || !IsExecutableAddress((void*)s_GetMainCameraFunc)) {
        DebugLog("[CoordConverter] ERROR: camera function address is not executable\n");
        s_WorldToScreenFunc = nullptr;
        s_GetMainCameraFunc = nullptr;
        return false;
    }

    DebugLog("[CoordConverter] WorldToScreenPoint_Injected at 0x%p (RVA+0x%lX)\n",
             s_WorldToScreenFunc, RVAConstants::Camera_WorldToScreenPoint_Injected);
    DebugLog("[CoordConverter] get_main func at 0x%p (RVA+0x%lX)\n",
             s_GetMainCameraFunc, RVAConstants::Camera_get_main);

    s_MainCamera = GetMainCamera();
    if (!s_MainCamera) {
        DebugLog("[CoordConverter] WARNING: Main camera null at init (will retry per frame)\n");
    } else {
        DebugLog("[CoordConverter] Main camera: 0x%p\n", s_MainCamera);
    }

    s_Initialized = true;
    DebugLog("[CoordConverter] Initialized: 1\n");
    return true;
}

bool CoordConverter::WorldToScreen(const Vector3& world, Vector2* outScreen) {
    if (!outScreen || !s_WorldToScreenFunc) return false;

    void* camera = GetMainCamera();
    if (!camera) return false;
    s_MainCamera = camera;

    Vector3 worldPos = world;
    Vector3 result = {};
    if (!SafeCallWorldToScreen(s_WorldToScreenFunc, camera, &worldPos, &result)) {
        return false;
    }

    // z <= 0 means behind camera
    if (result.z <= 0.0f) return false;

    // Unity WorldToScreenPoint: game viewport pixels, origin bottom-left.
    // ImGui overlay: same viewport size, origin top-left. Do NOT use ScreenToClient.
    float screenX = result.x;
    float screenY = result.y;

    float clientH = 1080.0f;
    HWND hwnd = s_GameWindow ? s_GameWindow : globals::mainWindow;
    RECT rc = {};
    if (hwnd && GetClientRect(hwnd, &rc) && rc.bottom > rc.top) {
        clientH = (float)(rc.bottom - rc.top);
    } else if (ImGui::GetCurrentContext()) {
        clientH = ImGui::GetIO().DisplaySize.y;
    }

    screenY = clientH - screenY;

    outScreen->x = screenX;
    outScreen->y = screenY;
    return true;
}

void CoordConverter::CalculateBoxSize(float distance, float* width, float* height) {
    if (distance < config::MIN_DISTANCE) distance = config::MIN_DISTANCE;
    if (distance > config::MAX_DISTANCE) distance = config::MAX_DISTANCE;

    float scaleFactor = config::ESP_BASE_SIZE / (distance * 0.1f);
    *width = scaleFactor;
    *height = scaleFactor * 2.0f;
}

bool CoordConverter::IsOnScreen(const Vector2& screen, float width, float height) {
    RECT rc = {};
    HWND hwnd = s_GameWindow ? s_GameWindow : globals::mainWindow;
    float screenW = 1920.0f;
    float screenH = 1080.0f;
    if (hwnd && GetClientRect(hwnd, &rc)) {
        screenW = (float)(rc.right - rc.left);
        screenH = (float)(rc.bottom - rc.top);
    }

    if (screen.x < -width || screen.x > screenW + width) return false;
    if (screen.y < -height || screen.y > screenH + height) return false;
    return true;
}

}
