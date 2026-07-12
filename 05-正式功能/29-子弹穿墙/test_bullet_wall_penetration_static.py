import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-bullet_wall_penetration_min.js"
UI_FILE = BASE_DIR / "AAAAA-bullet_wall_penetration_ui.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class BulletWallPenetrationStaticTests(unittest.TestCase):

    def test_js_contains_feature_id_rvas_and_offsets(self):
        text = read_text(JS_FILE)

        required_tokens = [
            'feature_id: "bullet_wall_penetration"',
            "Weapon_get_isMyWeapon: 0x00B6E1D0",
            "WPN_Gun_Damage: 0x00B613D0",
            "WeaponLogic_CheckWall: 0x00B78F80",
            "LayerConstant_cctor: 0x00AE7CD0",
            "LayerConstant_TypeInfo: 0x0E2BE3C",
            "Weapon_data: 0x68",
            "WPN_Gun_realData: 0xEC",
            "WeaponData_Gun_wallShotDamageRatio: 0x158",
            "LayerConstant_HitBox: 0x8",
            "LayerConstant_LM_GunShoot: 0x38",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_js_uses_original_damage_flow_and_wall_ratio(self):
        text = read_text(JS_FILE)

        self.assertIn("Interceptor.attach", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertIn("readWallShotDamageRatio", text)
        self.assertIn("WeaponLogic.CheckWall", text)
        self.assertIn("wallShotDamageRatio", text)
        self.assertIn("patchGunShootLayerMask", text)
        self.assertIn("restoreGunShootLayerMask", text)
        self.assertNotIn("Entity_OnEntityHurt", text)
        self.assertNotIn("GameManager_TakeDamage", text)

    def test_js_scopes_effect_to_local_weapon_damage_window(self):
        text = read_text(JS_FILE)

        damage_hook = text.split("attachHook('WPN_Gun.Damage'", 1)[1]
        on_enter = damage_hook.split("onLeave:", 1)[0]
        on_leave = damage_hook.split("onLeave:", 1)[1].split("});", 1)[0]

        self.assertIn("native.isMyWeapon", on_enter)
        self.assertIn("Runtime.damageDepth += 1", on_enter)
        self.assertIn("patchGunShootLayerMask", on_enter)
        self.assertIn("restoreGunShootLayerMask", on_leave)
        self.assertIn("Runtime.damageDepth -= 1", on_leave)

    def test_js_exports_standard_rpc_and_status(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in ["enable", "disable", "status", "cleanup", "setconfig"]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

        for status_key in [
            "damage_hits",
            "local_damage_hits",
            "layer_patch_count",
            "layer_restore_count",
            "check_wall_hits",
            "last_wall_ratio",
        ]:
            self.assertIn(status_key, text)

    def test_ui_loads_script_and_uses_standard_rpc(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("import frida", text)
        self.assertIn("import psutil", text)
        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "AAAAA-bullet_wall_penetration_min.js")', text)
        self.assertIn('GAME_PROCESS_NAME = "UnityCrossFire.exe"', text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkTextbox", text)
        self.assertIn("self.script.exports_sync.enable()", text)
        self.assertIn("self.script.exports_sync.disable()", text)
        self.assertIn("self.script.exports_sync.status()", text)
        self.assertIn("self.script.exports_sync.cleanup()", text)
        self.assertIn("self.script.exports_sync.setconfig", text)

    def test_no_global_physics_or_direct_damage_shortcut(self):
        text = read_text(JS_FILE)

        self.assertNotRegex(text, re.compile(r"Physics\$\$Raycast(All|NonAlloc)?", re.I))
        self.assertNotRegex(text, re.compile(r"Physics\$\$Linecast", re.I))
        self.assertNotIn("DamageEventData$$TakePlace", text)

    def test_restore_preserves_patch_state_until_original_mask_is_written(self):
        text = read_text(JS_FILE)

        self.assertIn("function writeOriginalMaskAndClearPatch", text)
        helper = text.split("function writeOriginalMaskAndClearPatch", 1)[1].split("function restoreGunShootLayerMask", 1)[0]

        self.assertIn("writeLayerValue(OFF.LayerConstant_LM_GunShoot, patch.originalMask)", helper)
        self.assertIn("readLayerValue(OFF.LayerConstant_LM_GunShoot)", helper)
        self.assertIn("Runtime.currentPatch = null", helper)
        self.assertLess(
            helper.index("writeLayerValue(OFF.LayerConstant_LM_GunShoot, patch.originalMask)"),
            helper.rindex("Runtime.currentPatch = null"),
        )
        self.assertIn("restore LM_GunShoot readback mismatch", helper)

    def test_disable_and_cleanup_force_restore_layer_mask(self):
        text = read_text(JS_FILE)

        self.assertIn("function forceRestoreGunShootLayerMask", text)
        disable_fn = text.split("function disableFeature()", 1)[1].split("function cleanupFeature()", 1)[0]
        cleanup_fn = text.split("function cleanupFeature()", 1)[1].split("function updateConfig", 1)[0]

        self.assertIn("forceRestoreGunShootLayerMask('disable')", disable_fn)
        self.assertIn("forceRestoreGunShootLayerMask('cleanup')", cleanup_fn)


if __name__ == "__main__":
    unittest.main()
