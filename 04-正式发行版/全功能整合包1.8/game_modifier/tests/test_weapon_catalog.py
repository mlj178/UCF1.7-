import unittest

from core.weapon_catalog import TYPE_COLORS, WEAPON_LIST, get_weapon_name


class WeaponCatalogTests(unittest.TestCase):
    def test_catalog_exposes_weapon_names_and_type_colors(self):
        self.assertGreater(len(WEAPON_LIST), 0)
        self.assertIn("120", [weapon[0] for weapon in WEAPON_LIST])
        self.assertTrue(TYPE_COLORS)
        self.assertEqual(get_weapon_name("120"), "NANOKNIFE")

    def test_catalog_returns_fallback_name_for_unknown_weapon(self):
        self.assertEqual(get_weapon_name("999999"), "weapon999999")


if __name__ == "__main__":
    unittest.main()
