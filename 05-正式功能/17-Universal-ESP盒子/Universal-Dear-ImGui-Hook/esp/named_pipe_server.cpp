#include "named_pipe_server.h"
#include "esp_state.h"
#include "../stdafx.h"
#include <string>
#include <sstream>
#include <atomic>

namespace NamedPipeServer {

static HANDLE s_thread = nullptr;
static std::atomic<bool> s_running{false};
static std::atomic<bool> s_unload_requested{false};

// Protocol version
static const int PROTOCOL_VERSION = 2;
static const char* DLL_VERSION = "1.7";

// Pipe name will be dynamically generated based on PID
static std::string s_pipe_name;
static const DWORD BUFFER_SIZE = 4096;

// Get current process PID
static DWORD GetCurrentPID() {
    return GetCurrentProcessId();
}

// Generate pipe name for current process
static std::string GetPipeName() {
    if (s_pipe_name.empty()) {
        DWORD pid = GetCurrentPID();
        char buf[256];
        snprintf(buf, sizeof(buf), "\\\\.\\pipe\\ucf_universal_hook_%lu", pid);
        s_pipe_name = buf;
    }
    return s_pipe_name;
}

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

// Build hello response with full state
static std::string BuildHelloResponse() {
    std::ostringstream oss;
    oss << "{"
        << "\"ok\":true"
        << ",\"pid\":" << GetCurrentPID()
        << ",\"protocol\":" << PROTOCOL_VERSION
        << ",\"dll_version\":\"" << DLL_VERSION << "\""
        << ",\"esp_box\":" << (ESPState::Instance().IsBoxEnabled() ? "true" : "false")
        << "}";
    return oss.str();
}

// Build state response
static std::string BuildStateResponse() {
    std::ostringstream oss;
    oss << "{"
        << "\"ok\":true"
        << ",\"esp_box\":" << (ESPState::Instance().IsBoxEnabled() ? "true" : "false")
        << ",\"revision\":" << ESPState::Instance().GetRevision()
        << "}";
    return oss.str();
}

// Process a command and return response
static std::string ProcessCommand(const std::string& cmd) {
    std::string cmdType = GetJsonString(cmd, "cmd");

    if (cmdType == "ping") {
        return BuildResponse(true);
    }
    else if (cmdType == "hello") {
        // Return full state and metadata
        PipeLog("Hello received, returning state");
        return BuildHelloResponse();
    }
    else if (cmdType == "get_state") {
        // Return current state with revision
        return BuildStateResponse();
    }
    else if (cmdType == "set_state") {
        // Set state with revision check
        int revision = 0;
        std::string revStr = GetJsonString(cmd, "revision");
        if (!revStr.empty()) {
            revision = std::stoi(revStr);
        }

        bool esp_box = GetJsonBool(cmd, "esp_box");

        // Only apply if revision is newer
        if (revision > ESPState::Instance().GetRevision()) {
            ESPState::Instance().SetBoxEnabled(esp_box, revision);
            PipeLog("State updated: esp_box=%s, revision=%d", esp_box ? "true" : "false", revision);
        } else {
            PipeLog("State update ignored: old revision %d <= current %d", revision, ESPState::Instance().GetRevision());
        }

        return BuildStateResponse();
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
    else if (cmdType == "reset") {
        // Reset all states
        ESPState::Instance().Reset();
        PipeLog("All states reset");
        return BuildStateResponse();
    }
    else if (cmdType == "shutdown") {
        PipeLog("Shutdown requested");
        // Legacy command: keep DLL and feature state alive for a new client.
        PipeLog("State preserved, pipe server continues running");
        return BuildResponse(true);
    }
    else if (cmdType == "unload") {
        ESPState::Instance().Reset();
        s_unload_requested = true;
        PipeLog("Unload requested");
        return BuildResponse(true);
    }
    else {
        return BuildResponse(false, "unknown command");
    }
}

// Pipe server thread function
static DWORD WINAPI PipeServerThread(LPVOID) {
    PipeLog("Thread started");

    std::string pipeName = GetPipeName();
    PipeLog("Pipe name: %s", pipeName.c_str());

    while (s_running) {
        // Create named pipe for this process
        HANDLE hPipe = CreateNamedPipeA(
            pipeName.c_str(),
            PIPE_ACCESS_DUPLEX,
            PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
            1,              // max instances: single instance per process
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

            if (s_unload_requested) {
                break;
            }
        }

        DisconnectNamedPipe(hPipe);
        CloseHandle(hPipe);

        if (s_unload_requested) {
            break;
        }
    }

    bool shouldUnload = s_unload_requested.exchange(false);
    s_running = false;
    PipeLog("Thread exiting");
    if (shouldUnload) {
        Uninject();
    }
    return 0;
}

void Start() {
    if (s_running) {
        PipeLog("Already running");
        return;
    }

    s_running = true;
    s_unload_requested = false;
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
    std::string pipeName = GetPipeName();
    HANDLE wakePipe = CreateFileA(
        pipeName.c_str(),
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
