import unittest
from pathlib import Path


class SpeedGunScriptTests(unittest.TestCase):
    def setUp(self):
        script = Path(__file__).parents[1] / "scripts" / "speed_gun.js"
        self.source = script.read_text(encoding="utf-8")

    def test_requires_weapon_data_write_before_marking_task_complete(self):
        self.assertIn("var dataApplied = false;", self.source)
        self.assertIn("return animApplied && dataApplied;", self.source)
        self.assertIn("return true;", self.source)

    def test_hooks_weapon_ownership_and_deploy_lifecycle(self):
        self.assertIn("base.add(0xB6CDC0)", self.source)
        self.assertIn("base.add(0xB6D8C0)", self.source)
        self.assertIn("base.add(0xB67030)", self.source)
        self.assertIn("base.add(0xB61E60)", self.source)
        self.assertIn("notifyWeaponAcquired(this.self)", self.source)

    def test_rpg_speed_is_applied_before_first_fire(self):
        marker = "base.add(0xB67700)"
        block = self.source[self.source.index(marker):]
        self.assertIn("onEnter: function(args)", block[:700])
        self.assertIn("applyRpgSpeed(this.self)", block[:700])

    def test_reapplies_selected_weapon_after_deploy_finishes(self):
        self.assertIn("base.add(0xB166A0)", self.source)
        self.assertIn("function refreshSelectedWeapon(", self.source)
        self.assertIn("safeReadPointer(playerWeapons, 0x18)", self.source)
        self.assertIn("rpgAnimSpeedFn(weapon, ptr(0))", self.source)
        self.assertIn("grenadeAnimSpeedFn(weapon, ptr(0))", self.source)


if __name__ == "__main__":
    unittest.main()
