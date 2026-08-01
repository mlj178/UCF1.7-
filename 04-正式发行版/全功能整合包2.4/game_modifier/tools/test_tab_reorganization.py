import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURES_DIR = ROOT / "features"


def manifests():
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in FEATURES_DIR.glob("*/manifest.json")
    ]


class TabReorganizationTests(unittest.TestCase):
    def test_requested_cards_are_in_their_requested_tabs(self):
        by_id = {manifest["feature_id"]: manifest for manifest in manifests()}

        self.assertEqual(by_id["time"]["tab"], "other_tab")
        self.assertEqual(by_id["skillcd"]["tab"], "nano4t_tab")
        self.assertEqual(by_id["skillcd"]["ui"]["mode"], "special_inline_card")
        self.assertEqual(by_id["28_wall_noclip"]["tab"], "other_tab")
        for feature_id in ("timescale", "bot_pause", "free_camera"):
            self.assertEqual(by_id[feature_id]["tab"], "game_test_tab")

    def test_declared_empty_tabs_follow_grenade_tab(self):
        builder_source = (ROOT / "ui" / "views" / "plugin_tab_builder.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('"game_test_tab"', builder_source)
        self.assertIn('"game_parameters_tab"', builder_source)
        self.assertIn("special_inline_card", builder_source)


if __name__ == "__main__":
    unittest.main()
