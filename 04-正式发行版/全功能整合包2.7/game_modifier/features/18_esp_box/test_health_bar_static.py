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
        self.assertIn("DrawHealthOverlay", source)
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

        # 主方案（Bounds）与后备方案（固定身高）都要画血量覆盖层。
        self.assertGreaterEqual(source.count("DrawHealthOverlay(center"), 2)
        self.assertIn("AddText", source)
        self.assertIn("%d%%", source)
        self.assertNotIn("if (isEnemy && GameManager::GetPlayerHealth", source)

    def test_health_percentage_uses_explicit_17px_font(self):
        source = RENDERER.read_text(encoding="utf-8")

        self.assertIn("const float textHeight = 17.0f;", source)
        self.assertIn("ImGui::GetFont(), textHeight", source)

    def test_health_mode_and_display_are_selectable(self):
        source = RENDERER.read_text(encoding="utf-8")
        state = (SOURCE_ROOT / "esp" / "esp_state.h").read_text(encoding="utf-8")

        # 两个下拉框的枚举分支都要有对应实现：
        # 数值/仅血条/仅数值/两者在渲染器里分支，百分比是数值分支的 else 路径。
        for token in (
            "esphealth::MODE_VALUE",
            "esphealth::DISPLAY_BAR",
            "esphealth::DISPLAY_TEXT",
            "esphealth::DISPLAY_BOTH",
        ):
            self.assertIn(token, source)
        self.assertIn("esphealth::MODE_PERCENT", state)
        self.assertIn('sprintf_s(text, sizeof(text), "%d", health.current);', source)  # 只显示剩余血量
        # 不显示 "当前/上限"（调试日志里的 "%d/%d/%d..." 与血量文本无关）
        self.assertNotIn('sprintf_s(text, sizeof(text), "%d/%d"', source)
        self.assertIn("GetHealthMode", state)
        self.assertIn("GetHealthDisplay", state)

    def test_box_outline_switch_gates_box_drawing_only(self):
        source = RENDERER.read_text(encoding="utf-8")
        state = (SOURCE_ROOT / "esp" / "esp_state.h").read_text(encoding="utf-8")

        # 方框轮廓是独立开关（默认开）：
        self.assertIn("m_boxOutline", state)
        self.assertIn("IsBoxOutlineEnabled", state)
        # 主方案与后备方案都只在开关打开时才画方框……
        self.assertIn(
            "if (ESPState::Instance().IsBoxOutlineEnabled()) {\n"
            "            DrawBox(center, hitbox.width, hitbox.height, color, config::BOX_THICKNESS);\n"
            "        }",
            source,
        )
        self.assertIn(
            "if (ESPState::Instance().IsBoxOutlineEnabled()) {\n"
            "        DrawBox(center, boxWidth, boxHeight, color, config::BOX_THICKNESS);\n"
            "    }",
            source,
        )
        # ……而血量覆盖层始终在开关之外绘制，关掉方框仍能看到血条/数值。
        self.assertEqual(source.count("DrawHealthOverlay(center"), 2)
        self.assertNotIn("IsBoxOutlineEnabled()) {\n            PlayerHealthInfo", source)

    def test_health_value_is_decoded_from_obscured_int(self):
        manager = GAME_MANAGER.read_text(encoding="utf-8")
        bridge = BRIDGE.read_text(encoding="utf-8")

        # 具体数值来自 HealthData 的三个 ObscuredInt，只读解密，不写回。
        self.assertIn("ReadObscuredInt", manager)
        self.assertIn("ObscuredInt_hidden", manager)
        self.assertIn("HD_currentHealth", bridge)
        self.assertIn("HD_maxHealth", bridge)
        self.assertIn("HD_tempHealth", bridge)
        self.assertNotIn("SafeWriteValue", manager)


if __name__ == "__main__":
    unittest.main()
