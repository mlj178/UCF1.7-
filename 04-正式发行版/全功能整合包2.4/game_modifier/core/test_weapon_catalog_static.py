import unittest
from pathlib import Path


CATALOG_FILE = Path(__file__).resolve().with_name("weapon_catalog.py")


class WeaponCatalogStaticTests(unittest.TestCase):

    def test_weapon_giver_catalog_keeps_nanoknife_and_requested_hunter_weapons(self):
        text = CATALOG_FILE.read_text(encoding="utf-8")

        required_entries = {
            '("120", "NANOKNIFE", "NANOKNIFE",': "NANOKNIFE",
            '("541", "\u53cc\u6301\u5e93\u514b\u91cc", "\u53cc\u6301\u5e93\u514b\u91cc",': "Ghost Hunter dual kukri",
            '("673", "\u53cc\u6301\u6218\u65a7", "\u53cc\u6301\u6218\u65a7",': "The Vengeance dual axe",
        }

        for entry, label in required_entries.items():
            self.assertIn(entry, text, label)

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
