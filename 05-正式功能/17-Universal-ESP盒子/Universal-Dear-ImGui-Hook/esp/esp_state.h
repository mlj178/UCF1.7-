#pragma once

#include <windows.h>

class ESPState {
public:
    static ESPState& Instance() {
        static ESPState instance;
        return instance;
    }

    bool IsBoxEnabled() const {
        return m_boxEnabled;
    }

    void SetBoxEnabled(bool enabled) {
        m_boxEnabled = enabled;
    }

private:
    ESPState() : m_boxEnabled(false) {}
    ESPState(const ESPState&) = delete;
    ESPState& operator=(const ESPState&) = delete;

    volatile bool m_boxEnabled;
};
