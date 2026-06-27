import unittest

from ui.views.shell_view import apply_status_dot_style, resolve_status_hint
from ui.views.weapon_giver_view import (
    CURRENT_WEAPON_TEXT,
    GIVE_BUTTON_TEXT,
    HERO_TYPE_NAME,
    RESPAWN_WEAPON_TEXT,
    WEAPON_GIVER_TITLE,
)


class ShellViewTests(unittest.TestCase):
    def test_resolve_status_hint_maps_connection_colors(self):
        self.assertEqual(resolve_status_hint("green").fg_color, "#1a3a1a")
        self.assertEqual(resolve_status_hint("red").fg_color, "#3a1a1a")
        self.assertEqual(resolve_status_hint("yellow").fg_color, "#2a2a00")

    def test_resolve_status_hint_uses_default_for_unknown_color(self):
        hint = resolve_status_hint("unknown")

        self.assertEqual(hint.fg_color, "#2a2a00")
        self.assertEqual(hint.text_color, "#ffcc00")

    def test_resolve_status_hint_uses_readable_chinese_copy(self):
        self.assertEqual(resolve_status_hint("green").text, "已连接，点击功能开关启用修改")
        self.assertEqual(resolve_status_hint("red").text, "连接断开，正在重连...")
        self.assertEqual(
            resolve_status_hint("yellow").text,
            "1. 启动游戏  2. 进入任意模式  3. 打开本工具  4. 开启功能",
        )

    def test_apply_status_dot_style_sets_visible_text_color(self):
        label = FakeLabel()

        apply_status_dot_style(label, "green")
        self.assertEqual(label.options["text"], "●")
        self.assertEqual(label.options["text_color"], "#2ecc71")

        apply_status_dot_style(label, "red")
        self.assertEqual(label.options["text_color"], "#ff4444")

        apply_status_dot_style(label, "yellow")
        self.assertEqual(label.options["text_color"], "#ffcc00")

        apply_status_dot_style(label, "gray")
        self.assertEqual(label.options["text_color"], "#888888")

    def test_weapon_giver_copy_is_readable(self):
        self.assertEqual(WEAPON_GIVER_TITLE, "🔨 赋予武器")
        self.assertEqual(RESPAWN_WEAPON_TEXT, "复活自动装备武器")
        self.assertEqual(CURRENT_WEAPON_TEXT, "当前武器: 无")
        self.assertEqual(GIVE_BUTTON_TEXT, "赋予")
        self.assertEqual(HERO_TYPE_NAME, "英雄")


class FakeLabel:
    def __init__(self):
        self.options = {}

    def configure(self, **kwargs):
        self.options.update(kwargs)


if __name__ == "__main__":
    unittest.main()
