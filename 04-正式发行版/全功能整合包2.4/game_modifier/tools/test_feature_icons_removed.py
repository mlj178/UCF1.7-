import json
import unittest
from pathlib import Path

from core.plugin.plugin_contract import PluginContract


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "features"
FEATURE_CARD = ROOT / "ui" / "components" / "feature_card.py"
SETTINGS = ROOT / "ui" / "settings_window.py"
CONFIG = ROOT / "core" / "config.py"


class FeatureIconRemovalTests(unittest.TestCase):
    def test_feature_manifests_do_not_store_icons_and_remain_valid(self):
        contract = PluginContract(logger=lambda _message: None)
        manifests = sorted(FEATURES.glob("*/manifest.json"))

        self.assertGreater(len(manifests), 1)
        for path in manifests:
            manifest = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(path=path):
                self.assertNotIn("icon", manifest)
                self.assertTrue(contract.validate(manifest))

    def test_feature_card_and_hotkey_settings_do_not_read_icons(self):
        feature_card_text = FEATURE_CARD.read_text(encoding="utf-8")
        settings_text = SETTINGS.read_text(encoding="utf-8")
        config_text = CONFIG.read_text(encoding="utf-8")

        self.assertNotIn('manifest.get("icon"', feature_card_text)
        self.assertNotIn("['icon']", settings_text)
        self.assertNotIn('"icon": manifest.get("icon"', config_text)


if __name__ == "__main__":
    unittest.main()
