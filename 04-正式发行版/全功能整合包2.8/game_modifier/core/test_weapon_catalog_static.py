import unittest
from pathlib import Path


CATALOG_FILE = Path(__file__).resolve().with_name("weapon_catalog.py")


class WeaponCatalogStaticTests(unittest.TestCase):

    def test_weapon_giver_catalog_keeps_nanoknife_and_requested_hunter_weapons(self):
        text = CATALOG_FILE.read_text(encoding="utf-8")

        required_entries = {
            '("120", "NANOKNIFE", "NANOKNIFE",': "NANOKNIFE",
            '("541", "双持库克里", "双持库克里（幽灵猎手）",': "Ghost Hunter dual kukri",
            '("673", "双持战斧", "双持战斧（复仇女神）",': "The Vengeance dual axe",
            '("390", "FAL CAMO", "FAL CAMO（榴弹）",': "FAL CAMO grenade label",
            '("3494", "Nano AT4", "Nano AT4（火箭筒）",': "Nano AT4 rocket launcher label",
        }

        for entry, label in required_entries.items():
            self.assertIn(entry, text, label)

    def test_weapon_giver_catalog_keeps_nano_stun_grenade_label(self):
        text = CATALOG_FILE.read_text(encoding="utf-8")

        self.assertIn(
            '("2977", "震撼弹", "震撼弹", "投掷"),',
            text,
        )
        self.assertNotIn("震撼弹（剑客模式）", text)

    def test_weapon_giver_catalog_includes_standard_stun_grenade(self):
        text = CATALOG_FILE.read_text(encoding="utf-8")

        self.assertIn(
            '("1071", "震荡弹", "震荡弹", "投掷"),',
            text,
        )

    def test_weapon_giver_catalog_excludes_removed_crazyknife_variants(self):
        text = CATALOG_FILE.read_text(encoding="utf-8")

        removed_entries = {
            '("223",': "CRAZYKNIFE",
            '("224",': "HCRAZYKNIFE",
            '("225",': "MCRAZYKNIFE",
            "CRAZYKNIFE": "CRAZYKNIFE name",
            "HCRAZYKNIFE": "HCRAZYKNIFE name",
            "MCRAZYKNIFE": "MCRAZYKNIFE name",
        }

        for entry, label in removed_entries.items():
            self.assertNotIn(entry, text, label)


if __name__ == "__main__":
    unittest.main()
