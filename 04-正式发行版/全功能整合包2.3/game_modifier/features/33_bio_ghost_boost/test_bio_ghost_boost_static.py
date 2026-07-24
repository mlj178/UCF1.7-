import json
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).resolve().parent


def read_text(name):
    return (FEATURE_DIR / name).read_text(encoding="utf-8")


class BioGhostBoostStaticTests(unittest.TestCase):
    def test_manifest_declares_bio_ghost_boost_plugin_contract(self):
        manifest = json.loads(read_text("manifest.json"))

        self.assertEqual(manifest["feature_id"], "33_bio_ghost_boost")
        self.assertEqual(manifest["display_name"], "生化幽灵专区")
        self.assertEqual(manifest["tab"], "bio_ghost_tab")
        self.assertEqual(manifest["tab_title"], "生化幽灵")
        self.assertEqual(manifest["runtime"]["type"], "plugin_script")
        self.assertIs(manifest["state"]["sync_enabled_from_config"], True)
        self.assertIs(manifest["lifecycle"]["requires_room_ready_reapply"], False)
        self.assertIs(manifest["lifecycle"]["room_ready_retry"], False)
        self.assertTrue(manifest["lifecycle"]["room_ready_reapply_exempt_reason"])

        config = manifest["config"]
        for key in (
            "damage_taken_multiplier",
            "attack_damage_multiplier",
            "move_speed_multiplier",
            "knife_speed_multiplier",
            "knife_range_multiplier",
            "skill_no_cooldown",
            "knockback_multiplier",
        ):
            self.assertIn(key, config)

        for rpc_name in ("enable", "disable", "setConfig", "set_config", "setconfig", "status", "cleanup"):
            self.assertIn(rpc_name, manifest["rpc"])


    def test_script_contains_required_hooks_and_ghost_filters(self):
        script = read_text("script.js")

        for marker in (
            "rpc.exports",
            "isLocalGhostPlayer",
            "RVA.Entity_OnEntityHurt",
            "RVA.Player_OnEntityHurt",
            "RVA.PropertyModifier_Get",
            "RVA.PlayerWeapons_get_KnifeSpeed",
            "RVA.WPN_Knife_GetKnifeAttackData",
            "RVA.Player_Update",
            "RVA.Skill_EndCold",
            "OFF.Entity_isGhostEntity",
            "OFF.Entity_isNoHitFeedback",
            "OFF.Player_velData",
            "scaleKnockbackVelocity",
        ):
            self.assertIn(marker, script)

        self.assertNotIn("require(", script)
        self.assertNotIn("scripts/" + "_common.js", script)
        self.assertNotIn("features/" + "_shared/common.js", script)


    def test_panel_uses_only_safe_plugin_callbacks(self):
        panel = read_text("panel.py")

        for callback in ('callbacks["toggle"]', 'callbacks["set_config"]', 'callbacks["action"]'):
            self.assertIn(callback, panel)

        forbidden = (
            "FridaManager",
            "core.frida_manager",
            "context._app",
            "app._",
            ".get_state(",
            ".set_state(",
            ".get_handle(",
            ".set_handle(",
            ".controller(",
            ".service(",
        )
        for marker in forbidden:
            self.assertNotIn(marker, panel)


if __name__ == "__main__":
    unittest.main()
