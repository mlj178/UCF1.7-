import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-fast_gunstock_min.js"
UI_FILE = BASE_DIR / "AAAAA-fast_gunstock_ui.py"
PLAN_FILE = BASE_DIR / "极速枪托-最小实现步骤.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FastGunstockStaticTests(unittest.TestCase):

    def test_js_contains_verified_rvas_and_offsets(self):
        text = read_text(JS_FILE)

        required_tokens = [
            "WpnGunOnSpecialBtnDown: 0xB629F0",
            "WpnGunGetKnifeAttackData: 0xB61F90",
            "WpnGunKnifeAttackEvent: 0xB62730",
            "WpnGunOnAnimationExit: 0xB62800",
            "WeaponGetIsMyWeapon: 0xB6E1D0",
            "CFAnimatorGetCharacterAnimator: 0xB35310",
            "CFAnimatorGetHandAnimator: 0xB35330",
            "AnimatorSetSpeed: 0xAA8C30",
            "WpnGun_realData: 0xEC",
            "WeaponDataGun_knifeAttacks: 0x180",
            "WpnGun_knifeAttackCount: 0x118",
            "WpnGun_knifeAttackAnim: 0x11C",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_js_uses_attach_hooks_and_keeps_original_game_flow(self):
        text = read_text(JS_FILE)

        self.assertIn("Interceptor.attach", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertNotIn("unlockGunstockState", text)
        self.assertNotIn("writeS32", text)
        self.assertNotIn("WpnGunOnKnifeAttackExit", text)
        self.assertIn("speedUpGunstockAnimators", text)
        self.assertIn("isLocalWeapon", text)

    def test_js_records_damage_event_without_changing_flow(self):
        text = read_text(JS_FILE)

        self.assertIn("knifeEventHook", text)
        self.assertIn("damageEventHits", text)
        self.assertIn("Interceptor.attach(mod.base.add(RVA.WpnGunKnifeAttackEvent)", text)

    def test_js_restores_speed_on_original_knife_attack_animation_exit(self):
        text = read_text(JS_FILE)

        self.assertIn("onAnimationExitHook", text)
        self.assertIn("Interceptor.attach(mod.base.add(RVA.WpnGunOnAnimationExit)", text)
        self.assertIn("readIl2CppString(args[2])", text)
        self.assertIn("this.animTag === 'knifeAttack'", text)
        self.assertIn("restoreGunstockAnimators(weapon, 'OnAnimationExit.knifeAttack'", text)
        self.assertNotIn("speedUpGunstockAnimators(weapon, 'OnKnifeAttackExit'", text)
        self.assertIn("forgetActiveWeapon(weapon)", text)

    def test_js_restores_animator_speed_without_manual_unlock(self):
        text = read_text(JS_FILE)

        self.assertIn("restoreGunstockAnimators", text)
        self.assertIn("setAnimatorSpeed(characterAnimator, 1.0", text)
        self.assertIn("setAnimatorSpeed(handAnimator, 1.0", text)
        self.assertNotIn("knifeAttackAnim=0", text)

    def test_js_exports_minimum_rpc_controls(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in ["enable", "disable", "status", "cleanup", "setmultiplier"]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

    def test_customtkinter_ui_loads_minimum_script_and_rpc(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("import frida", text)
        self.assertIn("import psutil", text)
        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "AAAAA-fast_gunstock_min.js")', text)
        self.assertIn('GAME_PROCESS_NAME = "UnityCrossFire.exe"', text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkSlider", text)
        self.assertIn("ctk.CTkTextbox", text)
        self.assertIn("self.script.exports_sync.enable()", text)
        self.assertIn("self.script.exports_sync.disable()", text)
        self.assertIn("self.script.exports_sync.status()", text)
        self.assertIn("self.script.exports_sync.cleanup()", text)
        self.assertIn("self.script.exports_sync.setmultiplier", text)

    def test_ui_does_not_shadow_tk_state_method(self):
        text = read_text(UI_FILE)

        self.assertNotIn("self.state =", text)
        self.assertNotIn("self.state.update", text)
        self.assertIn("self.game_state =", text)
        self.assertIn("self.game_state.update", text)

    def test_plan_records_core_reverse_engineering_result(self):
        text = read_text(PLAN_FILE)

        for token in [
            "WPN_Gun.OnSpecialBtnDown",
            "WPN_Gun.GetKnifeAttackData",
            "WeaponData_Gun.knifeAttacks",
            "knifeAttackAnim",
        ]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
