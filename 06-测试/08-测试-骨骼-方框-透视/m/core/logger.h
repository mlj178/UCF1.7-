#pragma once
#include <stdio.h>

namespace Logger {
    void Initialize(const char* logPath);
    void Shutdown();
    
    void Log(const char* tag, const char* fmt, ...);
    void LogError(const char* tag, const char* fmt, ...);
    void LogWarning(const char* tag, const char* fmt, ...);
}

#define LOG(tag, fmt, ...) Logger::Log(tag, fmt, ##__VA_ARGS__)
#define LOG_ERROR(tag, fmt, ...) Logger::LogError(tag, fmt, ##__VA_ARGS__)
#define LOG_WARN(tag, fmt, ...) Logger::LogWarning(tag, fmt, ##__VA_ARGS__)
