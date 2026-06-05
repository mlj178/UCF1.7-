//=============================================================================
// m_minimal.cpp - 最小注入测试 (不含 D3D11 / Hook)
// 用途: 验证 Frida Module.load() → DllMain → CreateThread 链路是否正常
// 如果这个 DLL 不卡死游戏, 说明问题在后续的 D3D11/Inline Hook 环节
//=============================================================================
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>

static volatile bool g_Shutdown = false;

static void log_to_file(const char* fmt, ...) {
    char buf[512];
    va_list va;
    va_start(va, fmt);
    wvsprintfA(buf, fmt, va);
    va_end(va);

    // 写入 m.dll 同目录下的 esp_log.txt
    char modulePath[MAX_PATH];
    char logPath[MAX_PATH];
    GetModuleFileNameA(NULL, modulePath, MAX_PATH);  // 实际应该用 DLL 自己的路径
    // 改用固定路径
    FILE* f = fopen("D:\\esp_log.txt", "a");
    if (f) {
        fprintf(f, "%s\n", buf);
        fflush(f);
        fclose(f);
    }
    OutputDebugStringA("[ESP] ");
    OutputDebugStringA(buf);
    OutputDebugStringA("\n");
}

static DWORD WINAPI MainThread(LPVOID) {
    log_to_file("MainThread started - DLL loaded OK");
    int count = 0;
    while (!g_Shutdown) {
        Sleep(3000);
        count++;
        log_to_file("Heartbeat #%d - DLL still alive", count);
    }
    log_to_file("MainThread exit");
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hMod, DWORD reason, LPVOID) {
    switch (reason) {
    case DLL_PROCESS_ATTACH:
        DisableThreadLibraryCalls(hMod);
        CreateThread(0, 0, MainThread, 0, 0, 0);
        break;
    case DLL_PROCESS_DETACH:
        g_Shutdown = true;
        Sleep(300);
        break;
    }
    return TRUE;
}