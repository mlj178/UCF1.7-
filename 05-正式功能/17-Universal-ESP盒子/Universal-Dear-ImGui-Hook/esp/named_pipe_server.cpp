#include "named_pipe_server.h"
#include "esp_state.h"
#include "../stdafx.h"
#include <string>
#include <sstream>

namespace NamedPipeServer {

static HANDLE s_thread = nullptr;
static volatile bool s_running = false;

// Pipe name must match Python client
static const char* PIPE_NAME = "\\\\.\\pipe\\ucf_universal_hook";

// Buffer size for pipe messages
static const DWORD BUFFER_SIZE = 4096;

// Log helper
static void PipeLog(const char* format, ...) {
    char buf[512];
    va_list args;
    va_start(args, format);
    vsnprintf(buf, sizeof(buf), format, args);
    va_end(args);
    DebugLog("[PipeServer] %s\n", buf);
}

// Simple JSON parser helpers
static std::string GetJsonString(const std::string& json, const std::string& key) {
    std::string search = "\"" + key + "\"";
    size_t pos = json.find(search);
    if (pos == std::string::npos) return "";

    pos = json.find(':', pos);
    if (pos == std::string::npos) return "";

    // Skip whitespace
    while (pos < json.size() && (json[pos] == ':' || json[pos] == ' ' || json[pos] == '\t')) pos++;

    if (pos >= json.size()) return "";

    if (json[pos] == '"') {
        // String value
        pos++;
        size_t end = json.find('"', pos);
        if (end == std::string::npos) return "";
        return json.substr(pos, end - pos);
    } else {
        // Non-string value (true/false/number)
        size_t end = pos;
        while (end < json.size() && json[end] != ',' && json[end] != '}' && json[end] != ' ') end++;
        return json.substr(pos, end - pos);
    }
}

static bool GetJsonBool(const std::string& json, const std::string& key) {
    std::string val = GetJsonString(json, key);
    return val == "true";
}

// Build JSON response
static std::string BuildResponse(bool ok, const std::string& error = "") {
    std::ostringstream oss;
    oss << "{\"ok\":" << (ok ? "true" : "false");
    if (!error.empty()) {
        oss << ",\"error\":\"" << error << "\"";
    }
    oss << "}";
    return oss.str();
}

// Process a command and return response
static std::string ProcessCommand(const std::string& cmd) {
    std::string cmdType = GetJsonString(cmd, "cmd");

    if (cmdType == "ping") {
        return BuildResponse(true);
    }
    else if (cmdType == "set_feature") {
        std::string feature = GetJsonString(cmd, "feature");
        bool enabled = GetJsonBool(cmd, "enabled");

        if (feature == "esp_box") {
            ESPState::Instance().SetBoxEnabled(enabled);
            PipeLog("ESP box %s", enabled ? "enabled" : "disabled");
            return BuildResponse(true);
        }
        else {
            return BuildResponse(false, "unknown feature");
        }
    }
    else if (cmdType == "shutdown") {
        PipeLog("Shutdown requested");
        s_running = false;
        return BuildResponse(true);
    }
    else {
        return BuildResponse(false, "unknown command");
    }
}

// Pipe server thread function
static DWORD WINAPI PipeServerThread(LPVOID) {
    PipeLog("Thread started");

    while (s_running) {
        // Try to clean up stale pipe instances from previous injections
        // by connecting as a client first
        {
            HANDLE hCleanup = CreateFileA(
                PIPE_NAME,
                GENERIC_READ | GENERIC_WRITE,
                0, NULL, OPEN_EXISTING, 0, NULL);
            if (hCleanup != INVALID_HANDLE_VALUE) {
                // Stale pipe found, close it to allow new pipe creation
                CloseHandle(hCleanup);
                PipeLog("Cleaned up stale pipe instance");
                Sleep(100);
            }
        }

        // Create named pipe
        HANDLE hPipe = CreateNamedPipeA(
            PIPE_NAME,
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            2,              // max instances: allow 1 extra for cleanup
            BUFFER_SIZE,    // out buffer size
            BUFFER_SIZE,    // in buffer size
            0,              // default timeout
            nullptr         // default security
        );

        if (hPipe == INVALID_HANDLE_VALUE) {
            PipeLog("CreateNamedPipe failed: %d", GetLastError());
            Sleep(1000);
            continue;
        }

        PipeLog("Pipe created, waiting for client...");

        // Wait for client connection
        BOOL connected = ConnectNamedPipe(hPipe, nullptr);
        if (!connected && GetLastError() != ERROR_PIPE_CONNECTED) {
            PipeLog("ConnectNamedPipe failed: %d", GetLastError());
            CloseHandle(hPipe);
            continue;
        }

        PipeLog("Client connected");

        // Process messages from client
        while (s_running) {
            char buffer[BUFFER_SIZE] = {0};
            DWORD bytesRead = 0;

            BOOL success = ReadFile(hPipe, buffer, sizeof(buffer) - 1, &bytesRead, nullptr);
            if (!success || bytesRead == 0) {
                DWORD err = GetLastError();
                if (err == ERROR_BROKEN_PIPE) {
                    PipeLog("Client disconnected");
                } else {
                    PipeLog("ReadFile failed: %d", err);
                }
                break;
            }

            buffer[bytesRead] = '\0';
            PipeLog("Received: %s", buffer);

            // Process command
            std::string response = ProcessCommand(buffer);
            PipeLog("Sending: %s", response.c_str());

            // Send response
            DWORD bytesWritten = 0;
            success = WriteFile(hPipe, response.c_str(), (DWORD)response.length(), &bytesWritten, nullptr);
            if (!success) {
                PipeLog("WriteFile failed: %d", GetLastError());
                break;
            }

            FlushFileBuffers(hPipe);
        }

        DisconnectNamedPipe(hPipe);
        CloseHandle(hPipe);
    }

    PipeLog("Thread exiting");
    return 0;
}

void Start() {
    if (s_running) {
        PipeLog("Already running");
        return;
    }

    s_running = true;
    s_thread = CreateThread(nullptr, 0, PipeServerThread, nullptr, 0, nullptr);

    if (s_thread) {
        PipeLog("Started successfully");
    } else {
        PipeLog("Failed to start thread: %d", GetLastError());
        s_running = false;
    }
}

void Stop() {
    if (!s_running) return;

    PipeLog("Stopping...");
    s_running = false;

    // Wake up ConnectNamedPipe by connecting as a client
    // This is necessary because ConnectNamedPipe blocks indefinitely
    HANDLE wakePipe = CreateFileA(
        "\\\\.\\pipe\\ucf_universal_hook",
        GENERIC_READ | GENERIC_WRITE,
        0, NULL, OPEN_EXISTING, 0, NULL);
    if (wakePipe != INVALID_HANDLE_VALUE) {
        // Connected successfully, close immediately
        CloseHandle(wakePipe);
        PipeLog("Wake-up connection sent");
    }

    if (s_thread) {
        // Wait for thread to exit
        WaitForSingleObject(s_thread, 3000);
        CloseHandle(s_thread);
        s_thread = nullptr;
    }

    PipeLog("Stopped");
}

bool IsRunning() {
    return s_running;
}

} // namespace NamedPipeServer
