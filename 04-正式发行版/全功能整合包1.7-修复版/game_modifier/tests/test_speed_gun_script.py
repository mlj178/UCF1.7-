import unittest
from pathlib import Path


class SpeedGunScriptTests(unittest.TestCase):
    def setUp(self):
        script = Path(__file__).parents[1] / "scripts" / "speed_gun.js"
        self.source = script.read_text(encoding="utf-8")

    def test_retry_only_finishes_after_weapon_data_is_ready(self):
        self.assertIn("var dataApplied = false;", self.source)
        self.assertIn("return dataApplied;", self.source)
        self.assertNotIn("return dataApplied || animApplied;", self.source)

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

    def test_pending_retry_does_not_store_weapon_pointer_across_frames(self):
        self.assertNotIn("weapon: weapon", self.source)
        self.assertNotIn("pendingWeaponSpeedMap", self.source)
        self.assertIn("function getCurrentPlayerWeapons()", self.source)
        self.assertIn("refreshSelectedWeapon(playerWeapons, false)", self.source)

    def test_pending_retry_uses_its_own_offsets(self):
        self.assertIn("GameManager_TypeInfo: 0x0E2933C", self.source)
        self.assertIn("Klass_staticFields: 0x5C", self.source)
        self.assertIn("Player_wpns: 0xA0", self.source)
        self.assertNotIn("mod.base.add(RVA.GameManager_TypeInfo)", self.source)
        self.assertNotIn("safeReadPointer(myPlayer, OFF.Player_wpns)", self.source)

    def test_enable_clears_stale_shutdown_state(self):
        enable_block = self.source[self.source.index("enable: function() {"):]
        self.assertIn("clearRoomState(false, null);", enable_block[:500])


if __name__ == "__main__":
    unittest.main()
