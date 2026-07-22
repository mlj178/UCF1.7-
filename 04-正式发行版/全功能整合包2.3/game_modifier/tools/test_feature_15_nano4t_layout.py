import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VIEW = ROOT / "ui" / "views" / "nano4t_view.py"
MANIFEST = ROOT / "features" / "15_nano4t" / "manifest.json"


class Nano4tLayoutTests(unittest.TestCase):
    def test_nano4t_selector_has_outer_card_boundary(self):
        text = VIEW.read_text(encoding="utf-8")

        self.assertIn("nano4t_card = ctk.CTkFrame", text)
        self.assertIn('border_width=1', text)
        self.assertIn('border_color="#555555"', text)
        self.assertIn("nano4t_title_frame = ctk.CTkFrame(nano4t_card", text)
        self.assertIn('text="🧬"', text)
        self.assertIn('text="多人生化Buff选择"', text)
        self.assertIn("nano4t_top_frame = ctk.CTkFrame(nano4t_card", text)
        self.assertIn("nano4t_next_label = ctk.CTkLabel(nano4t_card", text)
        self.assertIn("nano4t_sel_frame = ctk.CTkFrame(nano4t_card", text)
        self.assertIn("btn_frame = ctk.CTkFrame(nano4t_card", text)
        self.assertIn("battle_round_frame = ctk.CTkFrame(scroll", text)

    def test_nano4t_tab_title_is_short_category_name(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

        self.assertEqual(manifest["display_name"], "多人生化Buff选择")
        self.assertEqual(manifest["tab_title"], "多人生化")
        self.assertEqual(manifest["ui"]["tab_title"], "多人生化")


if __name__ == "__main__":
    unittest.main()
