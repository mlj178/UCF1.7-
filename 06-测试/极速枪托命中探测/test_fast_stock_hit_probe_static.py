from pathlib import Path
import unittest


SCRIPT_PATH = Path(__file__).with_name("AAAAA-fast_stock_hit_probe_min.js")
RUNNER_PATH = Path(__file__).with_name("run_fast_stock_hit_probe.py")
TRIAL_SCRIPT_PATH = Path(__file__).with_name("AAAAA-fast_stock_hit_stun_bypass_min.js")
PRECISE_SCRIPT_PATH = Path(__file__).with_name("AAAAA-fast_stock_hit_stun_precise_min.js")
WAIT_SCRIPT_PATH = Path(__file__).with_name("AAAAA-fast_stock_hit_stun_wait_min.js")


class FastStockHitProbeStaticTests(unittest.TestCase):
    def test_probe_declares_the_required_read_only_observation_points(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8")

        for rva in (
            "0xB629F0",  # WPN_Gun.OnSpecialBtnDown
            "0xB62730",  # WPN_Gun.KnifeAttackEvent
            "0xB6B380",  # Weapon.CallKnifeAttack
            "0xB3F470",  # Entity.OnEntityHurt
            "0xB34CC0",  # CFAnimator.PlayKnifeHitStunAnim
            "0xB73050",  # knife-hit-stun coroutine MoveNext
            "0xB62800",  # WPN_Gun.OnAnimationExit
        ):
            self.assertIn(rva, source)

        self.assertIn("Interceptor.attach", source)
        self.assertGreaterEqual(source.count("attachProbe(module.base.add"), 7)
        self.assertIn("rpc.exports", source)
        self.assertIn("enable", source)
        self.assertIn("disable", source)
        self.assertIn("status", source)
        self.assertIn("cleanup", source)

    def test_probe_does_not_include_game_memory_writes_or_replacements(self):
        source = SCRIPT_PATH.read_text(encoding="utf-8").lower()

        for forbidden in (
            ".writefloat(",
            ".writeu8(",
            ".writeu32(",
            ".writes32(",
            ".writepointer(",
            "interceptor.replace",
            "nativecallback",
        ):
            self.assertNotIn(forbidden, source)

    def test_runner_attaches_only_to_an_existing_process_and_writes_utf8_logs(self):
        source = RUNNER_PATH.read_text(encoding="utf-8")

        self.assertIn('PROCESS_NAME = "UnityCrossFire.exe"', source)
        self.assertIn("frida.attach", source)
        self.assertIn("script.exports_sync.enable()", source)
        self.assertIn('encoding="utf-8"', source)
        self.assertIn("script.exports_sync.cleanup()", source)
        self.assertNotIn("frida.spawn", source)

    def test_trial_bypasses_only_local_hit_stun_and_restores_the_original_function(self):
        source = TRIAL_SCRIPT_PATH.read_text(encoding="utf-8")

        self.assertIn("CFAnimator_PlayKnifeHitStunAnim: 0xB34CC0", source)
        self.assertIn("Interceptor.replace", source)
        self.assertIn("Interceptor.revert", source)
        self.assertIn("isLocalWeapon(self)", source)
        self.assertIn("originalPlayKnifeHitStun", source)
        self.assertIn("rpc.exports", source)
        self.assertNotIn(".writeFloat(", source)
        self.assertNotIn(".writeU8(", source)

    def test_runner_can_select_the_hit_stun_validation_script(self):
        source = RUNNER_PATH.read_text(encoding="utf-8")

        self.assertIn("import argparse", source)
        self.assertIn('"probe"', source)
        self.assertIn('"bypass"', source)
        self.assertIn("AAAAA-fast_stock_hit_stun_bypass_min.js", source)

    def test_precise_trial_keeps_the_original_hit_flow_and_restores_only_local_animator_speed(self):
        source = PRECISE_SCRIPT_PATH.read_text(encoding="utf-8")

        for required in (
            "KnifeHitStunCoroutine_MoveNext: 0xB73050",
            "CFAnimator_get_characterAnimator: 0xB35310",
            "CFAnimator_get_handAnimator: 0xB35330",
            "Animator_set_speed: 0xAA8C30",
            "Interceptor.attach",
            "state === 1",
            "restoreLocalAnimatorSpeeds",
            "local_hit_stun_speed_restored",
            "Interceptor.detachAll",
        ):
            self.assertIn(required, source)

        self.assertNotIn("Interceptor.replace", source)
        self.assertNotIn("Interceptor.revert", source)
        self.assertNotIn(".writeFloat(", source)
        self.assertNotIn(".writeU8(", source)

    def test_runner_can_select_the_precise_hit_stun_validation_script(self):
        source = RUNNER_PATH.read_text(encoding="utf-8")

        self.assertIn('"precise"', source)
        self.assertIn("AAAAA-fast_stock_hit_stun_precise_min.js", source)

    def test_wait_trial_shortens_only_the_local_hit_stun_coroutine_wait(self):
        source = WAIT_SCRIPT_PATH.read_text(encoding="utf-8")

        for required in (
            "KnifeHitStunCoroutine_MoveNext: 0xB73050",
            "WaitForSeconds_ctor: 0xA59F50",
            "Process.getCurrentThreadId()",
            "activeLocalPauseThreads",
            "args[1] = ptr(0)",
            "local_hit_stun_wait_shortened",
            "Interceptor.detachAll",
        ):
            self.assertIn(required, source)

        self.assertNotIn("Interceptor.replace", source)
        self.assertNotIn("Interceptor.revert", source)
        self.assertNotIn(".writeFloat(", source)
        self.assertNotIn(".writeU8(", source)

    def test_runner_can_select_the_wait_validation_script(self):
        source = RUNNER_PATH.read_text(encoding="utf-8")

        self.assertIn('"wait"', source)
        self.assertIn("AAAAA-fast_stock_hit_stun_wait_min.js", source)


if __name__ == "__main__":
    unittest.main()
