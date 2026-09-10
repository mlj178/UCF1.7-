from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).with_name("script.js")


class FastGunstockNaturalDamageTests(unittest.TestCase):
    def test_unlocks_only_after_the_original_natural_damage_event(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("KnifeAttackEvent: 0xB62730", source)
        self.assertIn("自然伤害完成", source)
        self.assertIn("unlockAttack(atk, '自然伤害完成')", source)
        self.assertIn("onLeave: function ()", source)
        self.assertNotIn("knifeAttackEventFn(atk.weapon", source)
        self.assertNotIn("function doEarlyDamage", source)
        self.assertNotIn("earlyDamageDelayMs", source)

    def test_keeps_an_exception_only_guard_without_a_fixed_attack_cadence(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("maxGuardMs", source)
        self.assertNotIn("unlockDelayMs", source)
        self.assertIn("最大保护窗口", source)

    def test_skips_when_local_player_is_nano_ghost(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("Player_get_isNanoGhost: 0xB56050", source)
        self.assertIn("owner: 0x30", source)
        self.assertIn("isLocalPlayerNanoGhost(w)", source)
        self.assertIn("本地玩家为生化幽灵，极速枪托不生效", source)
        self.assertIn("ghostSkips", source)


if __name__ == "__main__":
    unittest.main()
