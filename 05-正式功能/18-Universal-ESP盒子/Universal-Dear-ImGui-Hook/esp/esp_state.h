#pragma once

#include <windows.h>
#include <atomic>

// 血量覆盖层的显示选项（由外部修改器经命名管道下发）：
//   HealthMode:    0 = 百分比（"85%"），1 = 剩余数值（"85"，只显示当前血量，不含上限）
//   HealthDisplay: 0 = 仅血条，1 = 仅数值，2 = 血条 + 数值
namespace esphealth {
    constexpr int MODE_PERCENT = 0;
    constexpr int MODE_VALUE = 1;

    constexpr int DISPLAY_BAR = 0;
    constexpr int DISPLAY_TEXT = 1;
    constexpr int DISPLAY_BOTH = 2;

    inline int NormalizeMode(int mode) {
        return (mode == MODE_VALUE) ? MODE_VALUE : MODE_PERCENT;
    }

    inline int NormalizeDisplay(int display) {
        if (display == DISPLAY_TEXT || display == DISPLAY_BOTH) return display;
        return DISPLAY_BAR;
    }
}

class ESPState {
public:
    static ESPState& Instance() {
        static ESPState instance;
        return instance;
    }

    bool IsBoxEnabled() const {
        return m_boxEnabled.load(std::memory_order_acquire);
    }

    bool IsAllPlayersEnabled() const {
        return m_allPlayers.load(std::memory_order_acquire);
    }

    // ---- 渲染诊断（外部经命名管道读取）------------------------------------
    // 方框整帧为空时，用来判断到底是"没有候选""被来源策略拒了"还是"被死活/敌我过滤拒了"。
    struct Diagnostics {
        int gameMode = -1;
        int epoch = 0;
        int roundOver = 0;
        int candidates = 0;
        int rejectedSource = 0;
        int rejectedObject = 0;
        int rejectedTeam = 0;
        int drawn = 0;
        int relaxedDrawn = 0;
    };

    void SetDiagnostics(int gameMode, unsigned long epoch, int roundOver, int candidates,
                        int rejectedSource, int rejectedObject, int rejectedTeam,
                        int drawn, int relaxedDrawn) {
        m_diagGameMode.store(gameMode, std::memory_order_relaxed);
        m_diagEpoch.store(static_cast<int>(epoch), std::memory_order_relaxed);
        m_diagRoundOver.store(roundOver, std::memory_order_relaxed);
        m_diagCandidates.store(candidates, std::memory_order_relaxed);
        m_diagRejectedSource.store(rejectedSource, std::memory_order_relaxed);
        m_diagRejectedObject.store(rejectedObject, std::memory_order_relaxed);
        m_diagRejectedTeam.store(rejectedTeam, std::memory_order_relaxed);
        m_diagDrawn.store(drawn, std::memory_order_relaxed);
        m_diagRelaxedDrawn.store(relaxedDrawn, std::memory_order_relaxed);
    }

    Diagnostics GetDiagnostics() const {
        Diagnostics d;
        d.gameMode = m_diagGameMode.load(std::memory_order_relaxed);
        d.epoch = m_diagEpoch.load(std::memory_order_relaxed);
        d.roundOver = m_diagRoundOver.load(std::memory_order_relaxed);
        d.candidates = m_diagCandidates.load(std::memory_order_relaxed);
        d.rejectedSource = m_diagRejectedSource.load(std::memory_order_relaxed);
        d.rejectedObject = m_diagRejectedObject.load(std::memory_order_relaxed);
        d.rejectedTeam = m_diagRejectedTeam.load(std::memory_order_relaxed);
        d.drawn = m_diagDrawn.load(std::memory_order_relaxed);
        d.relaxedDrawn = m_diagRelaxedDrawn.load(std::memory_order_relaxed);
        return d;
    }

    // 方框轮廓开关：关闭后仍按血量选项画血条/数值，只是不画四周方框。
    bool IsBoxOutlineEnabled() const {
        return m_boxOutline.load(std::memory_order_acquire);
    }

    int GetHealthMode() const {
        return m_healthMode.load(std::memory_order_acquire);
    }

    int GetHealthDisplay() const {
        return m_healthDisplay.load(std::memory_order_acquire);
    }

    // 兼容旧调用：只改开关/范围，其余选项沿用当前值。
    void SetState(bool enabled, bool allPlayers, int revision = 0) {
        SetState(enabled, allPlayers, IsBoxOutlineEnabled(),
                 GetHealthMode(), GetHealthDisplay(), revision);
    }

    void SetState(bool enabled, bool allPlayers, int healthMode, int healthDisplay,
                  int revision = 0) {
        SetState(enabled, allPlayers, IsBoxOutlineEnabled(),
                 healthMode, healthDisplay, revision);
    }

    void SetState(bool enabled, bool allPlayers, bool boxOutline,
                  int healthMode, int healthDisplay, int revision = 0) {
        if (revision == 0) {
            revision = m_revision.load(std::memory_order_acquire) + 1;
        }
        int current_rev = m_revision.load(std::memory_order_acquire);
        if (revision > current_rev) {
            m_boxEnabled.store(enabled, std::memory_order_release);
            m_allPlayers.store(allPlayers, std::memory_order_release);
            m_boxOutline.store(boxOutline, std::memory_order_release);
            m_healthMode.store(esphealth::NormalizeMode(healthMode), std::memory_order_release);
            m_healthDisplay.store(esphealth::NormalizeDisplay(healthDisplay),
                                  std::memory_order_release);
            m_revision.store(revision, std::memory_order_release);
        }
    }

    void SetBoxEnabled(bool enabled, int revision = 0) {
        SetState(enabled, IsAllPlayersEnabled(), IsBoxOutlineEnabled(),
                 GetHealthMode(), GetHealthDisplay(), revision);
    }

    int GetRevision() const {
        return m_revision.load(std::memory_order_acquire);
    }

    void Reset() {
        m_boxEnabled.store(false, std::memory_order_release);
        m_allPlayers.store(false, std::memory_order_release);
        m_boxOutline.store(true, std::memory_order_release);
        m_healthMode.store(esphealth::MODE_PERCENT, std::memory_order_release);
        m_healthDisplay.store(esphealth::DISPLAY_BOTH, std::memory_order_release);
        m_revision.store(0, std::memory_order_release);
    }

private:
    ESPState()
        : m_boxEnabled(false),
          m_allPlayers(false),
          m_boxOutline(true),
          m_healthMode(esphealth::MODE_PERCENT),
          m_healthDisplay(esphealth::DISPLAY_BOTH),
          m_revision(0) {}
    ESPState(const ESPState&) = delete;
    ESPState& operator=(const ESPState&) = delete;

    std::atomic<bool> m_boxEnabled;
    std::atomic<bool> m_allPlayers;
    std::atomic<bool> m_boxOutline;
    std::atomic<int> m_diagGameMode{ -1 };
    std::atomic<int> m_diagEpoch{ 0 };
    std::atomic<int> m_diagRoundOver{ 0 };
    std::atomic<int> m_diagCandidates{ 0 };
    std::atomic<int> m_diagRejectedSource{ 0 };
    std::atomic<int> m_diagRejectedObject{ 0 };
    std::atomic<int> m_diagRejectedTeam{ 0 };
    std::atomic<int> m_diagDrawn{ 0 };
    std::atomic<int> m_diagRelaxedDrawn{ 0 };
    std::atomic<int> m_healthMode;
    std::atomic<int> m_healthDisplay;
    std::atomic<int> m_revision;
};
