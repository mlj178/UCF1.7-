from pathlib import Path
import unittest


SOURCE_ROOT = (
    Path(__file__).resolve().parents[5]
    / "05-正式功能"
    / "18-Universal-ESP盒子"
    / "Universal-Dear-ImGui-Hook"
)
RENDERER = SOURCE_ROOT / "esp" / "esp_renderer.cpp"
GAME_MANAGER = SOURCE_ROOT / "esp" / "game_manager.cpp"
BRIDGE = SOURCE_ROOT / "esp" / "il2cpp_bridge.h"


class HealthBarStaticTests(unittest.TestCase):
    def test_renderer_draws_health_bar_from_valid_enemy_health(self):
        source = RENDERER.read_text(encoding="utf-8")

        self.assertIn("GetPlayerHealth", source)
        self.assertIn("DrawHealthBar", source)
        self.assertIn("GetPlayerColor(player, localPlayer)", source)
        self.assertIn("isEnemy", source)

    def test_health_reader_uses_game_health_getters(self):
        manager = GAME_MANAGER.read_text(encoding="utf-8")
        bridge = BRIDGE.read_text(encoding="utf-8")

        self.assertIn("GetPlayerHealth", manager)
        self.assertIn("Entity_get_healthData", bridge)
        self.assertIn("HealthData_get_rate", bridge)
        self.assertIn("GetHealthDataFn", manager)
        self.assertIn("GetHealthRateFn", manager)

    def test_dead_players_are_filtered_before_health_bar_rendering(self):
        source = RENDERER.read_text(encoding="utf-8")

        self.assertIn("if (!player || player == localPlayer) return false;", source)
        self.assertIn("IsCandidateRenderable", source)

    def test_health_bar_is_horizontal_and_fills_by_width(self):
        source = RENDERER.read_text(encoding="utf-8")

        self.assertIn("const float barHeight", source)
        self.assertIn("const float fillWidth", source)
        self.assertIn("left + fillWidth", source)

    def test_both_teams_get_health_bar_and_numeric_percentage(self):
        source = RENDERER.read_text(encoding="utf-8")

        self.assertGreaterEqual(source.count("DrawHealthBar(center"), 2)
        self.assertIn("AddText", source)
        self.assertIn("%d%%", source)
        self.assertNotIn("if (isEnemy && GameManager::GetPlayerHealth", source)

    def test_health_percentage_uses_explicit_17px_font(self):
        source = RENDERER.read_text(encoding="utf-8")

        self.assertIn("ImGui::GetFont(), 17.0f", source)


if __name__ == "__main__":
    unittest.main()
