import unittest

from ui.window_contract import (
    APP_DISPLAY_NAME,
    APP_TITLE,
    STARTUP_LOG_TITLE,
    collapsed_geometry_for,
)


class WindowContractTests(unittest.TestCase):
    def test_app_name_drops_old_console_prefix(self):
        self.assertEqual(APP_DISPLAY_NAME, "全功能整合包 v1.8")
        self.assertEqual(APP_TITLE, "全功能整合包 v1.8")
        self.assertEqual(STARTUP_LOG_TITLE, "全功能整合包 v1.8")
        self.assertNotIn("游戏修改器控制台", APP_TITLE)

    def test_collapsed_geometry_keeps_current_position(self):
        self.assertEqual(collapsed_geometry_for("610x700+320+180"), "400x62+320+180")
        self.assertEqual(collapsed_geometry_for("700x750-8+30"), "400x62-8+30")

    def test_collapsed_geometry_handles_geometry_without_position(self):
        self.assertEqual(collapsed_geometry_for("610x700"), "400x62")


if __name__ == "__main__":
    unittest.main()
