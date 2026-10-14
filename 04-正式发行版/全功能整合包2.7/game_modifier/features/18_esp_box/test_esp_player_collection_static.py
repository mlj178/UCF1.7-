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
