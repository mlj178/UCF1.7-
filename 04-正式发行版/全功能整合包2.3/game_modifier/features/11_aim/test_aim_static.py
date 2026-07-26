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
        self.assertRegex(text, r"aimBone:\s*BONE\.HEAD")
        self.assertIn("BONE_Y_OFFSET[BONE.HEAD] = 1.65", text)
        self.assertIn("BONE_Y_OFFSET[BONE.NECK] = 1.45", text)
        self.assertIn("BONE_Y_OFFSET[BONE.CHEST] = 1.05", text)
        self.assertNotIn("boneIndex % yOffsets.length", text)

    def test_runtime_prefers_character_model_head_before_other_fallbacks(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "Collider_get_bounds_Injected",
            "P_currentCharacter",
            "CM_neck",
            "CM_helmet",
            "Helmet_collider",
            "function readColliderBoundsCenter(collider)",
            "function getCharacterHeadPos(player)",
            "pos.source = 'helmet_bounds'",
            "neckPos.source = 'character_neck'",
            "Component_GetComponent_Animator",
            "Animator_GetBoneTransform",
            "HUMAN_BONE.HEAD = 10",
            "function toHumanBodyBone(boneIndex)",
            "componentGetAnimator",
            "animatorGetBoneTransform",
            "function getRealBonePos(player, boneIndex)",
            "function getFallbackBonePos(player, boneIndex)",
            "function getAimPoint(player, boneIndex)",
        ]:
            self.assertIn(token, text)

        aim_point_fn = text.split("function getAimPoint(player, boneIndex)", 1)[1].split("function getLocalAimOrigin", 1)[0]
        self.assertLess(aim_point_fn.index("getCharacterHeadPos"), aim_point_fn.index("getRealBonePos"))
        self.assertLess(aim_point_fn.index("getRealBonePos"), aim_point_fn.index("getFallbackBonePos"))

        real_bone_fn = text.split("function getRealBonePos(player, boneIndex)", 1)[1].split("function getAimPoint", 1)[0]
        self.assertLess(real_bone_fn.index("componentGetAnimator"), real_bone_fn.index("animatorGetBoneTransform"))
        self.assertIn("toHumanBodyBone(boneIndex)", real_bone_fn)
        self.assertIn("readTransformPosition(boneTransform)", real_bone_fn)
        self.assertIn("isBoneNearPlayer(player, pos)", real_bone_fn)

        fallback_fn = text.split("function getFallbackBonePos(player, boneIndex)", 1)[1].split("function getAimPoint", 1)[0]
        self.assertIn("var pos = getPlayerPos(player)", fallback_fn)
        self.assertIn("pos.y += yOff", fallback_fn)

    def test_target_selection_uses_visible_candidates_and_nearest_distance_band(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "nearestDistanceBand: 2.0",
            "visibilityCheck: true",
            "Physics_get_defaultPhysicsScene_Injected",
            "PhysicsScene_Internal_Raycast_Injected",
            "function chooseTargetCandidate(candidates, distanceBand)",
            "var candidates = []",
            "selectionDistance:",
            "best = chooseTargetCandidate(candidates, CONFIG.nearestDistanceBand)",
        ]:
            self.assertIn(token, text)

        scanner_fn = text.split("function targetScanner()", 1)[1].split("function writeAimbot()", 1)[0]
        self.assertLess(scanner_fn.index("checkVisibility"), scanner_fn.index("candidates.push"))
        self.assertNotIn("angleDeg < bestAngleDeg", scanner_fn)

    def test_local_death_and_write_path_clear_cached_target(self):
        text = read_text(SCRIPT_FILE)

        scanner_fn = text.split("function targetScanner()", 1)[1].split("function writeAimbot()", 1)[0]
        self.assertIn("if (isDeadFn(myPlayer, ptr(0))) { resetAimState('local_dead_scan'); return; }", scanner_fn)

        write_fn = text.split("function writeAimbot()", 1)[1].split("function aimLoop()", 1)[0]
        self.assertIn("if (!isMyPlayerFn(myPlayer, ptr(0))) { resetAimState('local_invalid_write'); return; }", write_fn)
        self.assertIn("if (isDeadFn(myPlayer, ptr(0))) { resetAimState('local_dead_write'); return; }", write_fn)

    def test_camera_origin_requires_recent_camera_near_player_eye(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "maxCameraPlayerDistance",
            "function distance3d(a, b)",
            "function resetAimState(reason)",
            "var localEye = getLocalAimOrigin(player)",
            "distance3d(aimCamera.position, localEye) <= CONFIG.maxCameraPlayerDistance",
        ]:
            self.assertIn(token, text)

        get_origin_fn = text.split("function getAimOrigin(player)", 1)[1].split("function normalizeAngleDeg", 1)[0]
        self.assertLess(get_origin_fn.index("var localEye = getLocalAimOrigin(player)"), get_origin_fn.index("source: 'camera'"))

    def test_real_bone_position_must_be_near_player_root(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "maxBoneRootDistance",
            "function isBoneNearPlayer(player, bonePos)",
            "return distance3d(root, bonePos) <= CONFIG.maxBoneRootDistance",
        ]:
            self.assertIn(token, text)

    def test_local_eye_origin_is_separate_from_target_bone(self):
        text = read_text(SCRIPT_FILE)

        self.assertRegex(text, r"localEyeHeight:\s*1\.55")
        self.assertIn("function getLocalAimOrigin(player)", text)
        self.assertIn("basePos.y += CONFIG.localEyeHeight", text)
        self.assertNotIn("var myPos = getBonePos(myPlayer, CONFIG.aimBone)", text)

    def test_transform_position_uses_verified_injected_call_convention(self):
        text = read_text(SCRIPT_FILE)

        self.assertIn("Transform_get_position_Injected: 0x3F4280", text)
        self.assertIn("base.add(RVA_AIM.Transform_get_position_Injected)", text)
        self.assertIn("transformGetPos(transform, posBuf, ptr(0))", text)
        self.assertNotIn("transformGetPos(posBuf, transform, ptr(0))", text)

    def test_pitch_calculation_uses_world_height_delta_and_clamps_to_camera_range(self):
        text = read_text(SCRIPT_FILE)

        calc_fn = text.split("function calculateTargetAngles(from, to)", 1)[1].split("function angleDistanceDeg", 1)[0]
        for token in [
            "var dy = to.y - from.y",
            "var hDist = Math.sqrt(dx*dx + dz*dz)",
            "var pitch = Math.atan2(dy, hDist) * 180.0 / Math.PI",
            "targetPitchDeg: clampPitchDeg(pitch)",
        ]:
            self.assertIn(token, calc_fn)

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
            "localEye.source = 'player_eye'",
            "x: aimCamera.position.x",
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

    def test_pitch_storage_uses_same_sign_as_world_space_calculation(self):
        text = read_text(SCRIPT_FILE)

        self.assertNotIn("function toStoredPitchDeg", text)
        self.assertNotIn("function fromStoredPitchDeg", text)
        self.assertIn("pitchDeg: storedPitchDeg", text)
        self.assertIn(
            "player.add(OFF_AIM.P_cameraRotation + 4).writeFloat(pitchDeg)",
            text,
        )

        scanner_fn = text.split("function targetScanner()", 1)[1].split("function writeAimbot()", 1)[0]
        self.assertIn("var scanRotation = readCameraRotation(myPlayer)", scanner_fn)
        self.assertIn("scanPitchDeg = scanRotation.pitchDeg", scanner_fn)

        write_fn = text.split("function writeAimbot()", 1)[1].split("function aimLoop()", 1)[0]
        self.assertIn("var currentRotation = readCameraRotation(myPlayer)", write_fn)
        self.assertIn("var curPitchDeg = currentRotation.pitchDeg", write_fn)
        self.assertIn("writeCameraRotation(myPlayer, finalYawDeg, finalPitchDeg)", write_fn)

    def test_diagnostics_are_structured_and_rate_limited_to_one_second(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "diagnosticLogIntervalMs: 1000",
            "var lastAimDiagnosticAtMs = 0",
            "function emitAimDiagnostic(refreshed, currentRotation, finalYawDeg, finalPitchDeg)",
            "(now - lastAimDiagnosticAtMs) < CONFIG.diagnosticLogIntervalMs",
            "type: 'plugin_event'",
            "feature: 'aim'",
            "event: 'aim_debug_sample'",
            "originSource:",
            "originRootSource:",
            "targetSource:",
            "targetRootSource:",
            "horizontalDistance:",
            "rawPitchDeg:",
            "writtenYawDeg:",
            "writtenPitchDeg:",
        ]:
            self.assertIn(token, text)

        for token in [
            "transformPos.positionSource = 'player_transform'",
            "containerPos.positionSource = 'container_transform'",
            "rawPos.positionSource = 'container_raw'",
            "pos.source = 'real_bone'",
            "pos.source = 'fallback'",
        ]:
            self.assertIn(token, text)

        write_fn = text.split("function writeAimbot()", 1)[1].split("function aimLoop()", 1)[0]
        self.assertLess(
            write_fn.index("writeCameraRotation(myPlayer, finalYawDeg, finalPitchDeg)"),
            write_fn.index("emitAimDiagnostic(refreshed, currentRotation, finalYawDeg, finalPitchDeg)"),
        )

        reset_fn = text.split("function resetAimState(reason)", 1)[1].split("var RVA_AIM", 1)[0]
        self.assertNotIn("lastAimDiagnosticAtMs = 0", reset_fn)

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
        self.assertEqual(manifest["config"]["aimBone"], "head")
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
