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

// File-based debug logging system
class FileLogger {
private:
    FILE* logFile = nullptr;
    bool initialized = false;
    bool writeEnabled = true;
    
public:
    ~FileLogger() {
        if (logFile) {
            fclose(logFile);
            logFile = nullptr;
        }
    }
    
    void Initialize() {
        if (initialized) return;
        
        // Fixed log path in DLL project directory
        const char* logPath = "D:\\trae_project\\Universal-Dear-ImGui-Hook\\esp_debug.log";
        
        // Keep the log readable while the injected DLL is still writing.
        logFile = _fsopen(logPath, "a", _SH_DENYNO);
        if (!logFile) {
            writeEnabled = false;
            // Still output to DebugView
            OutputDebugStringA("[FileLogger] ERROR: Failed to open log file\n");
            return;
        }
        
        initialized = true;
        writeEnabled = true;
        
        // Write header immediately
        SYSTEMTIME st;
        GetLocalTime(&st);
        fprintf(logFile, "\n========================================\n");
        fprintf(logFile, "ESP Debug Log - %04d-%02d-%02d %02d:%02d:%02d\n",
                st.wYear, st.wMonth, st.wDay, st.wHour, st.wMinute, st.wSecond);
        fprintf(logFile, "========================================\n");
        fflush(logFile);
    }
    
    void Log(const char* message) {
        // Always initialize first
        if (!initialized) {
            Initialize();
        }
        
        // Write to file if enabled
        if (writeEnabled && logFile) {
            SYSTEMTIME st;
            GetLocalTime(&st);
            fprintf(logFile, "[%02d:%02d:%02d.%03d] %s",
                    st.wHour, st.wMinute, st.wSecond, st.wMilliseconds, message);
            fflush(logFile);
        }
        
        // ALWAYS output to DebugView
        OutputDebugStringA(message);
    }
};

// Global file logger instance
static FileLogger g_FileLogger;

// Helper macro for debug logging to file and DebugView
inline void DebugLog(const char* fmt, ...) {
    // Always log - disable filtering temporarily
    char buf[512];
    va_list args;
    va_start(args, fmt);
    vsnprintf(buf, sizeof(buf), fmt, args);
    va_end(args);
    g_FileLogger.Log(buf);
}
