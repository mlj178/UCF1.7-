#pragma once
#if defined _M_X64
#pragma comment(lib, "minhook/lib/libMinHook.x64.lib")
#elif defined _M_IX86
#pragma comment(lib, "minhook/lib/libMinHook.x86.lib")
#endif

#pragma comment(lib, "dxgi.lib")
#pragma comment(lib, "d3d9.lib")
#pragma comment(lib, "d3d10.lib")
#pragma comment(lib, "d3d11.lib")
#pragma comment(lib, "d3d12.lib")
#pragma comment(lib, "Psapi.lib")

#include <windows.h>
#include <vector>
#include <cstring>
#include <cstdio>
#include <cstdint>
#include <cstddef>
#include <cstdarg>
#include <share.h>
#include <map>
#include <unordered_map>
#include <unordered_set>
#include <atomic>
#include <Psapi.h>

#include <dxgi.h>
#include <dxgi1_4.h>
#include <d3d9.h>
#include <d3d10_1.h>
#include <d3d10.h>
#include <d3d11.h>
#include <d3d12.h>

#include <wrl/client.h>

#if defined _M_X64
typedef uint64_t uintx_t;
#elif defined _M_IX86
typedef uint32_t uintx_t;
#endif

#include "imgui/imgui.h"
#include "imgui/imgui_impl_win32.h"
#include "imgui/imgui_impl_dx9.h"
#include "imgui/imgui_impl_dx10.h"
#include "imgui/imgui_impl_dx11.h"
#include "imgui/imgui_impl_dx12.h"

#include "minhook/include/MinHook.h"

#include "esp/esp_common.h"
#include "esp/il2cpp_bridge.h"
#include "esp/game_manager.h"
#include "esp/transform_helper.h"
#include "esp/coord_converter.h"
#include "esp/esp_renderer.h"

#include "namespaces.h"

// File-based debug logging system (singleton to avoid multi-copy issues from static in header)
class FileLogger {
private:
    FILE* logFile = nullptr;
    bool initialized = false;
    bool writeEnabled = true;
    CRITICAL_SECTION cs;

    FileLogger() {
        InitializeCriticalSection(&cs);
    }

    FileLogger(const FileLogger&) = delete;
    FileLogger& operator=(const FileLogger&) = delete;

public:
    static FileLogger& Instance() {
        static FileLogger instance;
        return instance;
    }

    ~FileLogger() {
        EnterCriticalSection(&cs);
        if (logFile) {
            fclose(logFile);
            logFile = nullptr;
        }
        LeaveCriticalSection(&cs);
        DeleteCriticalSection(&cs);
    }

    void Log(const char* message) {
        EnterCriticalSection(&cs);

        // NOTE: 发布版停用日志持久化。以下代码被注释，不再创建/追加 esp_debug.log。
        // 仅保留 OutputDebugStringA 输出，供调试器(DBGVIEW)观察，不落盘。
        /*
        if (!initialized) {
            // Build log path next to the DLL module
            wchar_t wLogPath[MAX_PATH] = {0};
            HMODULE hMod = NULL;
            // Get the DLL module handle (globals::mainModule is set in DllMain, may not be set yet)
            // Use GetModuleHandleEx to get the DLL that contains this code
            GetModuleHandleExW(
                GET_MODULE_HANDLE_EX_FLAG_FROM_ADDRESS |
                GET_MODULE_HANDLE_EX_FLAG_UNCHANGED_REFCOUNT,
                (LPCWSTR)this,
                &hMod);
            if (hMod && GetModuleFileNameW(hMod, wLogPath, MAX_PATH)) {
                // Replace filename with esp_debug.log
                wchar_t* lastSlash = wcsrchr(wLogPath, L'\\');
                if (lastSlash) {
                    wcscpy_s(lastSlash + 1, MAX_PATH - (lastSlash + 1 - wLogPath), L"esp_debug.log");
                } else {
                    wcscpy_s(wLogPath, MAX_PATH, L"esp_debug.log");
                }
            } else {
                // Fallback to TEMP directory (always ASCII-safe)
                GetTempPathW(MAX_PATH, wLogPath);
                wcscat_s(wLogPath, MAX_PATH, L"esp_debug.log");
            }
            logFile = _wfsopen(wLogPath, L"a", _SH_DENYNO);
            if (logFile) {
                initialized = true;
                writeEnabled = true;
                SYSTEMTIME st;
                GetLocalTime(&st);
                fprintf(logFile, "\n========================================\n");
                fprintf(logFile, "ESP Debug Log - %04d-%02d-%02d %02d:%02d:%02d\n",
                        st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
                fprintf(logFile, "Log path: D:\\...\\esp_debug.log\n");
                fprintf(logFile, "========================================\n");
                fflush(logFile);
            } else {
                writeEnabled = false;
                OutputDebugStringA("[FileLogger] ERROR: Failed to open log file\n");
                LeaveCriticalSection(&cs);
                OutputDebugStringA(message);
                return;
            }
        }

        if (writeEnabled && logFile) {
            SYSTEMTIME st;
            GetLocalTime(&st);
            fprintf(logFile, "[%02d:%02d:%02d.%03d] %s",
                    st.wHour, st.wMinute, st.wSecond, st.wMilliseconds, message);
            fflush(logFile);
        }
        */

        OutputDebugStringA(message);
        LeaveCriticalSection(&cs);
    }
};

// Helper for debug logging - uses singleton FileLogger
inline void DebugLog(const char* fmt, ...) {
    char buf[512];
    va_list args;
    va_start(args, fmt);
    vsnprintf(buf, sizeof(buf), fmt, args);
    va_end(args);
    FileLogger::Instance().Log(buf);
}
