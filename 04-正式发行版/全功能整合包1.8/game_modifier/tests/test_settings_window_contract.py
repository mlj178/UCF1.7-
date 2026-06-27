import unittest
from pathlib import Path


class SettingsWindowContractTests(unittest.TestCase):
    def test_settings_window_closing_is_the_save_path_without_save_button(self):
        source = (Path(__file__).resolve().parents[1] / "ui" / "settings_window.py").read_text(encoding="utf-8")

        self.assertIn('self.protocol("WM_DELETE_WINDOW", self._on_save)', source)
        self.assertIn("save_and_apply", source)
        self.assertNotIn("保存并应用", source)

    def test_feature_tabs_do_not_define_extra_card_click_binding_helper(self):
        source = (Path(__file__).resolve().parents[1] / "ui" / "views" / "feature_tabs_view.py").read_text(encoding="utf-8")

        self.assertNotIn("bind_clickable_widgets", source)
        self.assertNotIn("toggle_callback", source)


if __name__ == "__main__":
    unittest.main()
