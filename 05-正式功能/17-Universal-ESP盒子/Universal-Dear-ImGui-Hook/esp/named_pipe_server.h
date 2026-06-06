#pragma once

#include <windows.h>

namespace NamedPipeServer {
    // Start the named pipe server thread
    void Start();

    // Stop the named pipe server thread
    void Stop();

    // Check if the server is running
    bool IsRunning();
}
