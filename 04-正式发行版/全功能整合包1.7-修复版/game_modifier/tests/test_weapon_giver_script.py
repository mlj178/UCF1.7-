import unittest
from pathlib import Path


class WeaponGiverScriptTests(unittest.TestCase):
    def setUp(self):
        script = Path(__file__).parents[1] / "scripts" / "weapon_giver.js"
        self.source = script.read_text(encoding="utf-8")

    def test_first_special_weapon_request_is_given_twice(self):
        self.assertIn("_specialDoubleGiveWeaponIds", self.source)
        self.assertIn("repeatCount = 2;", self.source)

    def test_enable_clears_stale_shutdown_state(self):
        enable_block = self.source[self.source.index("enable: function() {"):]
        self.assertIn("resetRoomState(null, false, null);", enable_block[:500])

    def test_rpc_can_give_without_explicit_module_enable(self):
        give_block = self.source[self.source.index("function giveWeapon("):]
        self.assertNotIn("if (!enabled)", give_block[:500])

    def test_native_player_checks_are_cached_and_fail_closed(self):
        self.assertIn("var _isDeadFunc = null;", self.source)
        self.assertIn("var _isMyPlayerFunc = null;", self.source)
        dead_block = self.source[self.source.index("function isPlayerDead("):]
        self.assertIn("return true;", dead_block[:500])

    def test_player_destroy_preserves_shutdown_state(self):
        destroy_marker = "base.add(RVA.Player_OnDestroy)"
        destroy_block = self.source[self.source.index(destroy_marker):]
        self.assertIn(
            "modules.speedgun.clearRoomState(_roomShuttingDown, _exitingModeBaseInstance)",
            destroy_block[:1000],
        )


if __name__ == "__main__":
    unittest.main()
