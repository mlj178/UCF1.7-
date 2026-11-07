from pathlib import Path
import unittest


SOURCE_ROOT = (
    Path(__file__).resolve().parents[5]
    / "05-正式功能"
    / "18-Universal-ESP盒子"
    / "Universal-Dear-ImGui-Hook"
)
MANAGER_H = SOURCE_ROOT / "esp" / "game_manager.h"
MANAGER_CPP = SOURCE_ROOT / "esp" / "game_manager.cpp"
RENDERER = SOURCE_ROOT / "esp" / "esp_renderer.cpp"
BRIDGE = SOURCE_ROOT / "esp" / "il2cpp_bridge.h"


class EspPlayerCollectionStaticTests(unittest.TestCase):
    def test_snapshot_preserves_container_state_and_candidate_sources(self):
        header = MANAGER_H.read_text(encoding="utf-8")
        source = MANAGER_CPP.read_text(encoding="utf-8")
        self.assertIn("enum class ContainerReadState", header)
        self.assertIn("struct PlayerCandidate", header)
        self.assertIn("struct PlayerSnapshot", header)
        self.assertIn("BuildPlayerSnapshot", header)
        for token in (
            "SourceAllPlayers",
            "SourceBL",
            "SourceGR",
            "SourceBLAlive",
            "SourceGRAlive",
            "SourceBotUpdate",
        ):
            self.assertIn(token, source)
        self.assertNotIn("if (result.empty())", source)

    def test_snapshot_reads_mode_and_round_state(self):
        source = MANAGER_CPP.read_text(encoding="utf-8")
        bridge = BRIDGE.read_text(encoding="utf-8")
        self.assertIn("GM_gameMode", bridge)
        self.assertIn("GM_gameRoundOver", bridge)
        self.assertIn("GetGameMode", source)
        self.assertIn("IsGameRoundOver", source)

    def test_render_eligibility_fails_closed(self):
        source = MANAGER_CPP.read_text(encoding="utf-8")
        self.assertIn("IsCandidateRenderable", source)
        self.assertIn("IsPlayerClassCompatible", source)
        self.assertIn("P_currentCharacter", source)
        self.assertIn("IsPlayerDead", source)

    def test_renderer_consumes_snapshot_and_shared_enemy_rule(self):
        source = RENDERER.read_text(encoding="utf-8")
        self.assertIn("BuildPlayerSnapshot", source)
        self.assertIn("IsCandidateRenderable", source)
        self.assertIn("GameManager::IsEnemy", source)
        self.assertNotIn(
            "GetPlayerTeam(player) == GameManager::GetPlayerTeam(localPlayer)",
            source,
        )

    def test_session_self_heals_after_room_change(self):
        """退出房间再开新房间后必须能自愈：定期重取单例 + 无本地玩家看门狗。"""
        manager = MANAGER_CPP.read_text(encoding="utf-8")
        bridge = (SOURCE_ROOT / "esp" / "il2cpp_bridge.cpp").read_text(encoding="utf-8")
        common = (SOURCE_ROOT / "esp" / "esp_common.h").read_text(encoding="utf-8")

        # 旧实例内存仍可读时结构校验会骗过缓存：必须定期绕过缓存重取，并有看门狗兜底
        self.assertIn("UpdateSessionWatchdog", manager)
        self.assertIn("config::SESSION_RESYNC_FRAMES", manager)
        self.assertIn("session watchdog", manager)
        self.assertIn("GM_REQUERY_INTERVAL", common)
        self.assertIn("config::GM_REQUERY_INTERVAL", bridge)
        self.assertIn("forceRequery", bridge)
        self.assertIn("instance re-resolved", bridge)

    def test_source_policy_cannot_blank_the_whole_frame(self):
        policy = (SOURCE_ROOT / "esp" / "player_policy.h").read_text(encoding="utf-8")
        renderer = RENDERER.read_text(encoding="utf-8")

        # 模式读不到 / 不认识时不再把候选全拒
        tail = policy.split("IsSourceEligible", 1)[1]
        self.assertIn("return true;", tail)
        # 渲染器两遍扫描 + ignoreSourcePolicy 兜底
        self.assertIn("drawPass(false)", renderer)
        self.assertIn("drawPass(true)", renderer)
        self.assertIn("[&](bool relaxed)", renderer)
        self.assertIn("relaxedDrawn", renderer)
        # 兜底遍同时跳过回合结束闸门，避免 roundOver 卡住时整帧空白
        manager = MANAGER_CPP.read_text(encoding="utf-8")
        self.assertIn("if (!relaxed && snapshot.roundOver) return false;", manager)

    def test_render_diagnostics_are_exposed_to_the_modifier(self):
        pipe = (SOURCE_ROOT / "esp" / "named_pipe_server.cpp").read_text(encoding="utf-8")
        state = (SOURCE_ROOT / "esp" / "esp_state.h").read_text(encoding="utf-8")
        self.assertIn("SetDiagnostics", state)
        self.assertIn("GetDiagnostics", state)
        for field in (
            "esp_diag_mode",
            "esp_diag_candidates",
            "esp_diag_rejected_source",
            "esp_diag_rejected_object",
            "esp_diag_rejected_team",
            "esp_diag_drawn",
            "esp_diag_relaxed_drawn",
            "esp_diag_round_over",
        ):
            self.assertIn(field, pipe)

    def test_session_polling_replaces_game_hooks(self):
        # 2026-10-15：不再用 MinHook 挂钩 Bot.Update / *OnStartNewGameRound /
        # GameManager.OnDestroy（与 Frida 双引擎重复挂钩会闪退），改为渲染帧轮询会话。
        source = MANAGER_CPP.read_text(encoding="utf-8")
        self.assertIn("s_SessionEpoch++", source)
        self.assertIn("GetGameManagerInstance", source)
        self.assertIn("RefreshSession", source)
        self.assertNotIn("MH_CreateHook", source)
        self.assertNotIn("MH_EnableHook", source)
        # 兼容层仍保留：候选来源/新鲜度判定框架不删（只是不再有 Bot.Update 数据源）。
        self.assertIn("policy::IsBotFresh", source)
        self.assertIn("SourceBotUpdate", source)


if __name__ == "__main__":
    unittest.main()
