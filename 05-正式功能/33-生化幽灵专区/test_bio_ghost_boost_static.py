import ast
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).resolve().parent


def read_text(name):
    return (FEATURE_DIR / name).read_text(encoding="utf-8")


class BioGhostBoostSingleFeatureTests(unittest.TestCase):
    def test_min_script_declares_33_single_feature_runtime(self):
        script = read_text("AAAAA-bio_ghost_boost_min.js")

        for marker in (
            "Bio Ghost Boost v1",
            "33_bio_ghost_boost",
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
            "rpc.exports",
        ):
            self.assertIn(marker, script)

    def test_ui_loads_single_feature_js_and_exposes_all_v1_controls(self):
        ui = read_text("AAAAA-bio_ghost_boost_ui.py")
        ast.parse(ui, filename="AAAAA-bio_ghost_boost_ui.py")

        for marker in (
            "AAAAA-bio_ghost_boost_min.js",
            "BioGhostBoostApp",
            "damage_taken_multiplier",
            "attack_damage_multiplier",
            "move_speed_multiplier",
            "knife_speed_multiplier",
            "knife_range_multiplier",
            "knockback_multiplier",
            "skill_no_cooldown",
            "script.exports_sync.setconfig",
            "script.exports_sync.enable",
            "script.exports_sync.disable",
            "script.exports_sync.status",
            "script.exports_sync.cleanup",
        ):
            self.assertIn(marker, ui)

    def test_ui_does_not_drop_pending_enable_after_connection(self):
        ui = read_text("AAAAA-bio_ghost_boost_ui.py")

        self.assertIn('result = self.script.exports_sync.enable(self._current_config())', ui)
        self.assertIn(
            "if self.desired_enabled:\n"
            '            self._rpc_call("enable")\n'
            "        else:\n"
            "            self._send_config()\n"
            "            self._refresh_status()",
            ui,
        )

    def test_script_reports_local_player_and_ghost_detection_diagnostics(self):
        script = read_text("AAAAA-bio_ghost_boost_min.js")

        for marker in (
            "localPlayerPtr",
            "captureLocalPlayerHook",
            "localPlayerSeen",
            "localGhostSeen",
            "lastIsGhostValue",
            "local_player_seen",
            "local_ghost_seen",
            "last_is_ghost_value",
        ):
            self.assertIn(marker, script)

    def test_brief_doc_lists_knockback_as_experimental(self):
        doc = read_text("生化幽灵专区-简要说明.md")

        for marker in (
            "33-生化幽灵专区",
            "击退倍率",
            "实验项",
            "本地玩家成为生化幽灵",
        ):
            self.assertIn(marker, doc)


if __name__ == "__main__":
    unittest.main()
