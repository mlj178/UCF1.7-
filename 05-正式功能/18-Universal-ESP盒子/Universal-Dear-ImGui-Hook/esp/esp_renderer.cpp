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

    // Install Bot hook and Room change hooks
    GameManager::InitializeBotHook();
    GameManager::InitializeRoomHooks();

    // Wait a bit for hooks to capture instances
    Sleep(100);

    // Priority 2: Initialize GameManager (will use hooked instance if available)
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
    DebugLog("[ESPRenderer] Initialized successfully\n");
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
    for (const PlayerCandidate& candidate : snapshot.candidates) {
        const bool botFresh =
            policy::HasSource(candidate.sources, policy::SourceBotUpdate) &&
            candidate.sessionEpoch == snapshot.sessionEpoch &&
            policy::IsBotFresh(candidate.botLastSeenTick, now);
        if (!policy::IsSourceEligible(snapshot.gameMode, candidate.sources, botFresh)) {
            ++rejectedSource;
            continue;
        }
        if (!GameManager::IsCandidateRenderable(candidate, snapshot, localPlayer, now)) {
            ++rejectedObject;
            continue;
        }
        if (!ESPState::Instance().IsAllPlayersEnabled() &&
            !GameManager::IsEnemy(candidate.player, localPlayer)) {
            ++rejectedTeam;
            continue;
        }
        if (SafeDrawPlayer(candidate.player, localPlayer)) ++drawnCount;
    }

    s_FrameCounter++;
    if (s_FrameCounter % config::LOG_INTERVAL == 0) {
        DebugLog(
            "[ESP] mode=%d epoch=%lu states=%d/%d/%d/%d/%d candidates=%zu "
            "rejectedSource=%d rejectedObject=%d rejectedTeam=%d drawn=%d\n",
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
            drawnCount);
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
        DrawBox(center, hitbox.width, hitbox.height, color, config::BOX_THICKNESS);
        float healthRate = 0.0f;
        if (GameManager::GetPlayerHealth(player, &healthRate)) {
            DrawHealthBar(center, hitbox.width, hitbox.height, healthRate);
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
    DrawBox(center, boxWidth, boxHeight, color, config::BOX_THICKNESS);
    float healthRate = 0.0f;
    if (GameManager::GetPlayerHealth(player, &healthRate)) {
        DrawHealthBar(center, boxWidth, boxHeight, healthRate);
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

void ESPRenderer::DrawHealthBar(const Vector2& center, float w, float h, float rate) {
    if (!std::isfinite(rate) || rate <= 0.0f || rate > 1.0f) return;

    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    const float barHeight = 3.0f;
    const float gap = 3.0f;
    const float left = center.x - w / 2.0f;
    const float top = center.y - h / 2.0f - gap - barHeight;
    const float right = left + w;
    const float fillWidth = w * rate;
    const int percent = (std::max)(0, (std::min)(100, static_cast<int>(rate * 100.0f + 0.5f)));
    char hpText[16] = {};
    sprintf_s(hpText, sizeof(hpText), "%d%%", percent);

    drawList->AddText(ImGui::GetFont(), 17.0f,
                      ImVec2(left, top - 17.0f),
                      IM_COL32(255, 255, 255, 240), hpText);
    drawList->AddRectFilled(ImVec2(left, top), ImVec2(right, top + barHeight), IM_COL32(20, 20, 20, 190));
    drawList->AddRectFilled(ImVec2(left, top), ImVec2(left + fillWidth, top + barHeight), IM_COL32(70, 220, 90, 235));
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
