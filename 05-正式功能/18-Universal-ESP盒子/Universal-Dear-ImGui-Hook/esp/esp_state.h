#pragma once

#include <windows.h>
#include <atomic>

class ESPState {
public:
    static ESPState& Instance() {
        static ESPState instance;
        return instance;
    }

    bool IsBoxEnabled() const {
        return m_boxEnabled.load(std::memory_order_acquire);
    }

    void SetBoxEnabled(bool enabled, int revision = 0) {
        // If revision is 0, auto-increment
        if (revision == 0) {
            revision = m_revision.load(std::memory_order_acquire) + 1;
        }
        
        // Only apply if revision is newer
        int current_rev = m_revision.load(std::memory_order_acquire);
        if (revision > current_rev) {
            m_boxEnabled.store(enabled, std::memory_order_release);
            m_revision.store(revision, std::memory_order_release);
        }
    }

    int GetRevision() const {
        return m_revision.load(std::memory_order_acquire);
    }

    void Reset() {
        m_boxEnabled.store(false, std::memory_order_release);
        m_revision.store(0, std::memory_order_release);
    }

private:
    ESPState() : m_boxEnabled(false), m_revision(0) {}
    ESPState(const ESPState&) = delete;
    ESPState& operator=(const ESPState&) = delete;

    std::atomic<bool> m_boxEnabled;
    std::atomic<int> m_revision;
};
