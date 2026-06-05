#include "logger.h"
#include <Windows.h>
#include <stdio.h>
#include <stdarg.h>

namespace Logger {
    static char s_LogPath[MAX_PATH] = {0};
    static CRITICAL_SECTION s_CS;
    static bool s_Initialized = false;
    
    void Initialize(const char* logPath) {
        if (s_Initialized) {
            return;
        }
        
        InitializeCriticalSection(&s_CS);
        strcpy_s(s_LogPath, MAX_PATH, logPath);
        
        FILE* f = fopen(s_LogPath, "w");
        if (f) {
            fclose(f);
        }
        
        s_Initialized = true;
    }
    
    void Shutdown() {
        if (!s_Initialized) {
            return;
        }
        
        DeleteCriticalSection(&s_CS);
        s_Initialized = false;
    }
    
    static void WriteLog(const char* level, const char* tag, const char* fmt, va_list args) {
        if (!s_Initialized) {
            return;
        }
        
        EnterCriticalSection(&s_CS);
        
        char buf[1024];
        vsnprintf(buf, sizeof(buf), fmt, args);
        
        SYSTEMTIME st;
        GetLocalTime(&st);
        
        char logLine[2048];
        snprintf(logLine, sizeof(logLine), "[%02d:%02d:%02d.%03d] [%s] [%s] %s\n",
                 st.wHour, st.wMinute, st.wSecond, st.wMilliseconds,
                 level, tag, buf);
        
        FILE* f = fopen(s_LogPath, "a");
        if (f) {
            fputs(logLine, f);
            fclose(f);
        }
        
        OutputDebugStringA(logLine);
        
        LeaveCriticalSection(&s_CS);
    }
    
    void Log(const char* tag, const char* fmt, ...) {
        va_list args;
        va_start(args, fmt);
        WriteLog("INFO", tag, fmt, args);
        va_end(args);
    }
    
    void LogError(const char* tag, const char* fmt, ...) {
        va_list args;
        va_start(args, fmt);
        WriteLog("ERROR", tag, fmt, args);
        va_end(args);
    }
    
    void LogWarning(const char* tag, const char* fmt, ...) {
        va_list args;
        va_start(args, fmt);
        WriteLog("WARN", tag, fmt, args);
        va_end(args);
    }
}
