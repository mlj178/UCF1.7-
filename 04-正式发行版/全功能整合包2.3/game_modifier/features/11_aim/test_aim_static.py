import json
import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
SCRIPT_FILE = BASE_DIR / "script.js"
MANIFEST_FILE = BASE_DIR / "manifest.json"
FEATURE_FILE = BASE_DIR / "feature.py"
PANEL_FILE = BASE_DIR / "panel.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class AimStaticTests(unittest.TestCase):
    def test_defaults_to_head_target_and_has_explicit_bone_map(self):
        text = read_text(SCRIPT_FILE)

        self.assertRegex(text, r"HEAD:\s*0")
        self.assertRegex(text, r"NECK:\s*3")
        self.assertRegex(text, r"CHEST:\s*7")
        self.assertRegex(text, r"aimBone:\s*BONE\.NECK")
        self.assertIn("BONE_Y_OFFSET[BONE.HEAD] = 1.65", text)
        self.assertIn("BONE_Y_OFFSET[BONE.NECK] = 1.45", text)
        self.assertIn("BONE_Y_OFFSET[BONE.CHEST] = 1.05", text)
        self.assertNotIn("boneIndex % yOffsets.length", text)

    def test_runtime_uses_real_bone_transform_first_and_fallback_second(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "Component_GetComponent_Animator",
            "Animator_GetBoneTransform",
            "HUMAN_BONE.HEAD = 10",
            "function toHumanBodyBone(boneIndex)",
            "componentGetAnimator",
            "animatorGetBoneTransform",
            "function getRealBonePos(player, boneIndex)",
            "function getAimPoint(player, boneIndex)",
            "return getRealBonePos(player, boneIndex) || getFallbackBonePos(player, boneIndex)",
        ]:
            self.assertIn(token, text)

        real_bone_fn = text.split("function getRealBonePos(player, boneIndex)", 1)[1].split("function getFallbackBonePos", 1)[0]
        self.assertLess(real_bone_fn.index("componentGetAnimator"), real_bone_fn.index("animatorGetBoneTransform"))
        self.assertIn("toHumanBodyBone(boneIndex)", real_bone_fn)
        self.assertIn("readTransformPosition(boneTransform)", real_bone_fn)

    def test_local_eye_origin_is_separate_from_target_bone(self):
        text = read_text(SCRIPT_FILE)

        self.assertRegex(text, r"localEyeHeight:\s*1\.55")
        self.assertIn("function getLocalAimOrigin(player)", text)
        self.assertIn("basePos.y += CONFIG.localEyeHeight", text)
        self.assertNotIn("var myPos = getBonePos(myPlayer, CONFIG.aimBone)", text)

    def test_aim_origin_prefers_final_camera_and_falls_back_to_player_eye(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "Brain_PushStateToUnityCamera",
            "Brain_get_OutputCamera",
            "Transform_get_forward_Injected",
            "brainGetOutputCamera",
            "transformGetForward",
            "var aimCamera =",
            "function readTransformForward(transform)",
            "function cacheAimCamera(brain)",
            "function getAimOrigin(player)",
            "origin.source = 'player_eye'",
            "return { x: aimCamera.position.x",
            "source: 'camera'",
            "cacheAimCamera(this.brain)",
        ]:
            self.assertIn(token, text)

        self.assertIn("cameraCacheMaxAgeMs", text)
        self.assertNotIn("var from = getLocalAimOrigin(myPlayer);\n      var to = getAimPoint", text)
        self.assertNotIn("var myPos = getLocalAimOrigin(myPlayer);\n    if (!myPos) return;", text)

    def test_aim_loop_recalculates_target_angles_before_writing(self):
        text = read_text(SCRIPT_FILE)

        self.assertIn("function calculateTargetAngles(from, to)", text)
        self.assertIn("function refreshCachedTargetAim()", text)
        write_fn = text.split("function writeAimbot()", 1)[1].split("function aimLoop()", 1)[0]
        self.assertIn("var refreshed = refreshCachedTargetAim()", write_fn)
        self.assertIn("targetYawDeg = refreshed.targetYawDeg", write_fn)
        self.assertIn("targetPitchDeg = refreshed.targetPitchDeg", write_fn)

    def test_pitch_uses_visual_space_internally_and_inverse_storage_space_for_game_memory(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "function toStoredPitchDeg(visualPitchDeg)",
            "return -visualPitchDeg",
            "function fromStoredPitchDeg(storedPitchDeg)",
            "return -storedPitchDeg",
            "function readCameraRotation(player)",
            "function writeCameraRotation(player, yawDeg, pitchDeg)",
        ]:
            self.assertIn(token, text)

        self.assertIn("pitchDeg: fromStoredPitchDeg(storedPitchDeg)", text)
        self.assertIn("player.add(OFF_AIM.P_cameraRotation + 4).writeFloat(toStoredPitchDeg(pitchDeg))", text)
        self.assertNotIn("myPlayer.add(OFF_AIM.P_cameraRotation + 4).writeFloat(finalPitchDeg)", text)

        scanner_fn = text.split("function targetScanner()", 1)[1].split("function writeAimbot()", 1)[0]
        self.assertIn("var scanRotation = readCameraRotation(myPlayer)", scanner_fn)
        self.assertIn("scanPitchDeg = scanRotation.pitchDeg", scanner_fn)

        write_fn = text.split("function writeAimbot()", 1)[1].split("function aimLoop()", 1)[0]
        self.assertIn("var currentRotation = readCameraRotation(myPlayer)", write_fn)
        self.assertIn("var curPitchDeg = currentRotation.pitchDeg", write_fn)
        self.assertIn("writeCameraRotation(myPlayer, finalYawDeg, finalPitchDeg)", write_fn)

    def test_diagnostics_and_debug_logging_are_removed(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "diagnosticLogIntervalMs",
            "debugLog",
            "lastAimDiagnostic",
            "lastAimLogAtMs",
            "sendLogFile",
            "recordAimDiagnostic",
            "shouldEmitAimDiagnosticLog",
        ]:
            self.assertNotIn(token, text)

    def test_hidden_aim_settings_are_fixed_defaults_not_runtime_config(self):
        text = read_text(SCRIPT_FILE)

        set_config_fn = text.split("setConfig: function(cfg)", 1)[1].split("getConfig: function()", 1)[0]
        for token in [
            "cfg.aimBone",
            "cfg.smoothness",
            "cfg.maxAimDistance",
            "cfg.maxAngleFOV",
            "cfg.localEyeHeight",
        ]:
            self.assertNotIn(token, set_config_fn)

        status_fn = text.split("getConfig: function()", 1)[1].split("};", 1)[0]
        for token in [
            "aimBone",
            "localEyeHeight",
            "smoothness",
            "maxAngleFOV",
            "maxAimDistance",
        ]:
            self.assertNotIn(token, status_fn)
        self.assertIn("frameCount", status_fn)

    def test_manifest_and_feature_expose_aim_controls_consistently(self):
        manifest = json.loads(read_text(MANIFEST_FILE))
        feature_text = read_text(FEATURE_FILE)

        self.assertEqual(manifest["feature_id"], "aim")
        self.assertEqual(manifest["script"], "script.js")
        self.assertEqual(manifest["config"]["aimBone"], "neck")
        self.assertEqual(manifest["config"]["smoothness"], 1.0)
        self.assertEqual(manifest["config"]["localEyeHeight"], 1.55)
        control_keys = {control.get("key") for control in manifest["controls"] if control.get("key")}
        self.assertEqual(control_keys, set())
        self.assertEqual([control.get("type") for control in manifest["controls"]], ["switch"])
        for key in ["autoAim", "diagnosticLogIntervalMs", "debugLog"]:
            self.assertNotIn(key, manifest["config"])

        self.assertIn("js_filename = 'script.js'", feature_text)
        self.assertIn("自动瞄准敌方玩家", feature_text)

    def test_panel_renders_only_feature_card_switch(self):
        text = read_text(PANEL_FILE)

        self.assertIn("def build_card(", text)
        self.assertIn("make_feature_card", text)
        for token in [
            "CTkOptionMenu",
            "CTkSlider",
            "CTkCheckBox",
            "callbacks[\"set_config\"]",
            '"aimBone"',
            '"smoothness"',
            '"maxAngleFOV"',
            '"maxAimDistance"',
            '"localEyeHeight"',
            '"diagnosticLogIntervalMs"',
            '"debugLog"',
        ]:
            self.assertNotIn(token, text)
        self.assertNotIn('"autoAim"', text)

    def test_auto_lock_option_is_removed(self):
        script_text = read_text(SCRIPT_FILE)
        manifest_text = read_text(MANIFEST_FILE)
        panel_text = read_text(PANEL_FILE)

        for text in [script_text, manifest_text, panel_text]:
            self.assertNotIn("autoAim", text)

        aim_loop = script_text.split("function aimLoop()", 1)[1].split("function installRoomHooks", 1)[0]
        self.assertIn("if (!getMouseBtnFn) return", aim_loop)
        self.assertIn("if (!btnDown) return", aim_loop)


if __name__ == "__main__":
    unittest.main()
