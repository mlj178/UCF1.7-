#include "esp_renderer.h"
#include "esp_state.h"
#include "game_manager.h"
#include "transform_helper.h"
#include "coord_converter.h"
#include "../stdafx.h"
#include <algorithm>
#include <cmath>
#include <cstdio>

namespace esp {

bool ESPRenderer::s_Enabled = true;
bool ESPRenderer::s_Initialized = false;
int ESPRenderer::s_FrameCounter = 0;

static bool SafeDrawPlayer(void* player, void* localPlayer) {
    if (!player || player == localPlayer) return false;

#if defined(_MSC_VER)
    __try {
        ESPRenderer::DrawPlayerESP(player, localPlayer);
        return true;
    } __except(EXCEPTION_EXECUTE_HANDLER) {
        DebugLog("[ESP] DrawPlayerESP access violation for player 0x%p\n", player);
        return false;
    }
#else
    SAFE_TRY {
        ESPRenderer::DrawPlayerESP(player, localPlayer);
        return true;
    } SAFE_EXCEPT_RET(false)
#endif
}

bool ESPRenderer::Initialize() {
    if (s_Initialized) return true;

    // 说明（2026-10-15 闪退修复）：
    // 旧实现在这里调用 GameManager::InitializeBotHook() / InitializeRoomHooks()，
    // 用 MinHook 改写 GameAssembly.dll 的 Bot.Update / *OnStartNewGameRound /
    // GameManager.OnDestroy 函数头，与 Frida 脚本在同一地址重复挂钩，被定性为
    // 10-11 闪退（双引擎重复挂钩 + 内存损坏）的来源。现在 DLL 不再改写任何游戏
    // 代码字节，会话刷新完全由渲染帧轮询完成，因此这里不再安装任何游戏钩子。

    if (!GameManager::Initialize()) {
        DebugLog("[ESPRenderer] GameManager init failed\n");
        return false;
    }

    if (!TransformHelper::Initialize()) {
        DebugLog("[ESPRenderer] TransformHelper init failed\n");
        return false;
    }

    if (!CoordConverter::Initialize()) {
        DebugLog("[ESPRenderer] CoordConverter init failed\n");
        return false;
    }

    s_Initialized = true;
    DebugLog("[ESPRenderer] Initialized successfully (no GameAssembly hooks)\n");
    return true;
}

void ESPRenderer::Render() {
    // Check if ESP box is enabled via external control
    if (!ESPState::Instance().IsBoxEnabled()) return;
    if (!s_Enabled || !s_Initialized) return;

    PlayerSnapshot snapshot;
    if (!GameManager::BuildPlayerSnapshot(&snapshot)) return;

    void* localPlayer = GameManager::GetLocalPlayer();
    if (!localPlayer) return;

    const DWORD now = GetTickCount();
    int drawnCount = 0;
    int rejectedSource = 0;
    int rejectedObject = 0;
    int rejectedTeam = 0;
    int relaxedDrawn = 0;

    // 一次扫描；relaxed=true 时跳过来源策略与回合结束闸门（兜底重试用）。
    auto drawPass = [&](bool relaxed) {
        int drawn = 0;
        for (const PlayerCandidate& candidate : snapshot.candidates) {
            if (!relaxed) {
                const bool botFresh =
                    policy::HasSource(candidate.sources, policy::SourceBotUpdate) &&
                    candidate.sessionEpoch == snapshot.sessionEpoch &&
                    policy::IsBotFresh(candidate.botLastSeenTick, now);
                if (!policy::IsSourceEligible(snapshot.gameMode, candidate.sources, botFresh)) {
                    ++rejectedSource;
                    continue;
                }
            }
            if (!GameManager::IsCandidateRenderable(candidate, snapshot, localPlayer, now,
                                                    relaxed)) {
                if (!relaxed) ++rejectedObject;
                continue;
            }
            if (!ESPState::Instance().IsAllPlayersEnabled() &&
                !GameManager::IsEnemy(candidate.player, localPlayer)) {
                if (!relaxed) ++rejectedTeam;
                continue;
            }
            if (SafeDrawPlayer(candidate.player, localPlayer)) ++drawn;
        }
        return drawn;
    };

    drawnCount = drawPass(false);
    if (drawnCount == 0 && rejectedSource > 0) {
        // 来源策略把整帧候选全拒了（模式读不到 / 退出房间再进新房间后容器分布变了）：
        // 兜底再扫一遍，只保留死活、已生成、敌我、epoch 这些硬过滤。
        // 宁可画出来，也不要整帧空白地“功能失效”。
        relaxedDrawn = drawPass(true);
        drawnCount += relaxedDrawn;
    }

    // 落一份诊断，供修改器经命名管道读取（方框空白时用于定位原因）。
    ESPState::Instance().SetDiagnostics(
        snapshot.gameMode,
        static_cast<unsigned long>(snapshot.sessionEpoch),
        snapshot.roundOver ? 1 : 0,
        static_cast<int>(snapshot.candidates.size()),
        rejectedSource, rejectedObject, rejectedTeam, drawnCount, relaxedDrawn);

    s_FrameCounter++;
    if (s_FrameCounter % config::LOG_INTERVAL == 0) {
        DebugLog(
            "[ESP] mode=%d epoch=%lu states=%d/%d/%d/%d/%d candidates=%zu "
            "rejectedSource=%d rejectedObject=%d rejectedTeam=%d drawn=%d relaxed=%d\n",
            snapshot.gameMode,
            snapshot.sessionEpoch,
            static_cast<int>(snapshot.allPlayersState),
            static_cast<int>(snapshot.blState),
            static_cast<int>(snapshot.grState),
            static_cast<int>(snapshot.blAliveState),
            static_cast<int>(snapshot.grAliveState),
            snapshot.candidates.size(),
            rejectedSource,
            rejectedObject,
            rejectedTeam,
            drawnCount,
            relaxedDrawn);
    }
}

void ESPRenderer::DrawPlayerESP(void* player, void* localPlayer) {
    if (!player) return;

    static int debugCounter = 0;
    bool shouldLog = (debugCounter++ % 600 == 0);

    // === Primary: Bounds/Hitbox ESP ===
    HitboxESPData hitbox = TransformHelper::GetHitboxData(player);

    if (hitbox.valid) {
        // Reject off-screen
        if (std::abs(hitbox.centerX) > 5000.f || std::abs(hitbox.centerY) > 5000.f) {
            if (shouldLog) DebugLog("[ESP] off-screen center (%.1f, %.1f)\n", hitbox.centerX, hitbox.centerY);
            return;
        }

        Vector2 center = { hitbox.centerX, hitbox.centerY };
        if (!CoordConverter::IsOnScreen(center, hitbox.width, hitbox.height)) return;

        if (shouldLog) {
            const char* methodName = (hitbox.method == 1) ? "Bounds" : "Hitbox";
            DebugLog("[ESP] %s: player=0x%p box=%.1fx%.1f center=(%.1f,%.1f) screen=%d\n",
                     methodName, player, hitbox.width, hitbox.height, hitbox.centerX, hitbox.centerY,
                     hitbox.validScreenCount);
        }

        ImVec4 color = GetPlayerColor(player, localPlayer);
        // 方框轮廓可单独关闭：关闭后仍按血量选项画血条/数值。
        if (ESPState::Instance().IsBoxOutlineEnabled()) {
            DrawBox(center, hitbox.width, hitbox.height, color, config::BOX_THICKNESS);
        }

        PlayerHealthInfo health;
        if (GameManager::GetPlayerHealth(player, &health)) {
            DrawHealthOverlay(center, hitbox.width, hitbox.height, health);
        }
        return;
    }

    // === Fallback (characterContainer + fixed height) ===
    DrawPlayerESPFallback(player, localPlayer, shouldLog);
}

void ESPRenderer::DrawPlayerESPFallback(void* player, void* localPlayer, bool shouldLog) {
    Vector3 feetPos = TransformHelper::GetPlayerPosition(player);
    if (feetPos.x == 0.f && feetPos.y == 0.f && feetPos.z == 0.f) {
        if (shouldLog) DebugLog("[ESP] Fallback: GetPlayerPosition failed for 0x%p\n", player);
        return;
    }

    Vector3 headPos = feetPos;
    headPos.y += config::PLAYER_HEAD_HEIGHT;

    Vector2 screenFeet, screenHead;
    if (!CoordConverter::WorldToScreen(feetPos, &screenFeet)) return;
    if (!CoordConverter::WorldToScreen(headPos, &screenHead)) return;

    float topY = (std::min)(screenHead.y, screenFeet.y);
    float bottomY = (std::max)(screenHead.y, screenFeet.y);
    float boxHeight = bottomY - topY;
    if (boxHeight < 4.0f || boxHeight > 800.0f) return;

    float boxWidth = boxHeight * 0.42f;
    Vector2 center;
    center.x = (screenFeet.x + screenHead.x) * 0.5f;
    center.y = (topY + bottomY) * 0.5f;

    if (std::abs(center.x) > 5000.f || std::abs(center.y) > 5000.f) return;
    if (!CoordConverter::IsOnScreen(center, boxWidth, boxHeight)) return;

    if (shouldLog) {
        DebugLog("[ESP] Fallback: player=0x%p feet=(%.1f,%.1f) head=(%.1f,%.1f)\n",
                 player, screenFeet.x, screenFeet.y, screenHead.x, screenHead.y);
    }

    ImVec4 color = GetPlayerColor(player, localPlayer);
    if (ESPState::Instance().IsBoxOutlineEnabled()) {
        DrawBox(center, boxWidth, boxHeight, color, config::BOX_THICKNESS);
    }

    PlayerHealthInfo health;
    if (GameManager::GetPlayerHealth(player, &health)) {
        DrawHealthOverlay(center, boxWidth, boxHeight, health);
    }
}

void ESPRenderer::DrawBox(const Vector2& center, float w, float h, 
                          const ImVec4& color, float thickness) {
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    
    ImVec2 p1(center.x - w/2, center.y - h/2);
    ImVec2 p2(center.x + w/2, center.y + h/2);
    
    ImU32 col = ImGui::ColorConvertFloat4ToU32(color);
    drawList->AddRect(p1, p2, col, 0.0f, 0, thickness);
}

// 血量覆盖层：
//   HealthDisplay = 仅血条 / 仅数值 / 血条 + 数值
//   HealthMode    = 百分比 / 剩余数值（只显示当前血量，不显示上限）
void ESPRenderer::DrawHealthOverlay(const Vector2& center, float w, float h,
                                    const PlayerHealthInfo& health) {
    if (!health.valid || (!health.hasRate && !health.hasValue)) return;

    const int display = ESPState::Instance().GetHealthDisplay();
    const int mode = ESPState::Instance().GetHealthMode();

    const bool drawBar = (display == esphealth::DISPLAY_BAR || display == esphealth::DISPLAY_BOTH);
    const bool drawText = (display == esphealth::DISPLAY_TEXT || display == esphealth::DISPLAY_BOTH);
    if (!drawBar && !drawText) return;

    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    if (!drawList) return;

    const float barHeight = 3.0f;
    const float gap = 3.0f;
    const float textHeight = 17.0f;

    const float left = center.x - w / 2.0f;
    const float right = left + w;
    const float top = center.y - h / 2.0f;

    const float barTop = top - gap - barHeight;
    // 数值默认画在血条上方；只画数值时紧贴方框上沿。
    const float textY = (drawBar || !drawText)
        ? (barTop - textHeight)
        : (top - textHeight - 1.0f);

    if (drawBar && health.hasRate) {
        float rate = health.rate;
        if (!std::isfinite(rate)) rate = 0.0f;
        if (rate < 0.0f) rate = 0.0f;
        if (rate > 1.0f) rate = 1.0f;

        const float fillWidth = w * rate;
        drawList->AddRectFilled(ImVec2(left, barTop), ImVec2(right, barTop + barHeight),
                                IM_COL32(20, 20, 20, 190));
        drawList->AddRectFilled(ImVec2(left, barTop), ImVec2(left + fillWidth, barTop + barHeight),
                                IM_COL32(70, 220, 90, 235));
    }

    if (drawText) {
        char text[32] = {};
        if (mode == esphealth::MODE_VALUE && health.hasValue) {
            // 只显示剩余血量本身，不显示 "当前/上限"。
            sprintf_s(text, sizeof(text), "%d", health.current);
        } else {
            float rate = health.hasRate ? health.rate : 0.0f;
            if (!std::isfinite(rate)) rate = 0.0f;
            int percent = static_cast<int>(rate * 100.0f + 0.5f);
            if (percent < 0) percent = 0;
            if (percent > 100) percent = 100;
            sprintf_s(text, sizeof(text), "%d%%", percent);
        }
        drawList->AddText(ImGui::GetFont(), textHeight, ImVec2(left, textY),
                          IM_COL32(255, 255, 255, 240), text);
    }
}

ImVec4 ESPRenderer::GetPlayerColor(void* player, void* localPlayer) {
    if (!player) return ImVec4(1.0f, 1.0f, 1.0f, 1.0f);

    int playerTeam = GameManager::GetPlayerTeam(player);
    const bool isEnemy = GameManager::IsEnemy(player, localPlayer);

    // Team enum: BlackList=0, GlobalRisk=1.


    if (isEnemy) {
        // Enemy colors.
        if (playerTeam == 0) {
            // BlackList enemy.
            return ImVec4(1.0f, 0.2f, 0.2f, 1.0f);
        } else if (playerTeam == 1) {
            // GlobalRisk enemy.
            return ImVec4(0.8f, 0.0f, 0.0f, 1.0f);
        } else {
            // Unknown enemy.
            return ImVec4(1.0f, 0.5f, 0.0f, 1.0f);
        }
    } else {
        // Ally colors.
        if (playerTeam == 0) {
            // BlackList ally.
            return ImVec4(0.2f, 0.4f, 1.0f, 1.0f);
        } else if (playerTeam == 1) {
            // GlobalRisk ally.
            return ImVec4(0.0f, 0.2f, 0.8f, 1.0f);
        } else {
            // Unknown ally.
            return ImVec4(0.0f, 0.8f, 0.8f, 1.0f);
        }
    }
}

}
