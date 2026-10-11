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
    def test_defaults_to_chest_target_with_sixty_degree_fov(self):
        text = read_text(SCRIPT_FILE)

        self.assertRegex(text, r"HEAD:\s*0")
        self.assertRegex(text, r"NECK:\s*3")
        self.assertRegex(text, r"CHEST:\s*7")
        self.assertRegex(text, r"aimBone:\s*BONE\.CHEST")
        self.assertRegex(text, r"maxAngleFOV:\s*60\.0")
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
            "function chooseTargetCandidateWithHysteresis(candidates, distanceBand, currentPlayer, angleAdvantage)",
            "var candidates = []",
            "selectionDistance:",
            "best = chooseTargetCandidateWithHysteresis(",
        ]:
            self.assertIn(token, text)

        scanner_fn = text.split("function targetScanner()", 1)[1].split("function writeAimbot()", 1)[0]
        self.assertLess(scanner_fn.index("checkSelectionLineOfSight"), scanner_fn.index("candidates.push"))
        self.assertIn("var selectionDistance = angles.dist", scanner_fn)
        self.assertNotIn("var targetRoot = getPlayerPos(p)", scanner_fn)
        self.assertNotIn("angleDeg < bestAngleDeg", scanner_fn)

    def test_actual_shot_validation_must_hit_target_entity_with_game_gun_mask(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "visibilityOriginClearance: 0.20",
            "visibilityTargetExtraDistance: 0.50",
            "visibilityLayerMask: 25",
            "visibilityHitBoxLayer: 3",
            "shotVisibilityQueryTriggerInteraction: 2",
            "Object_FindObjectFromInstanceID",
            "Component_get_gameObject",
            "GameObject_get_layer",
            "Component_GetComponentInParent_Entity",
            "Component_GetComponentInParent_Entity_MethodInfo",
            "RaycastHit_ColliderInstanceId: 0x28",
            "function calculateVisibilityRayDistance(targetDistance, originClearance, targetExtraDistance)",
            "function resolveRaycastHit(physicsScratch)",
            "function isTargetDamageHit(hitEntityMatchesTarget, colliderLayer, hitBoxLayer)",
            "function checkShotRayHitsTarget(from, to, targetPlayer, physicsScratch)",
            "isTargetDamageHit(",
            "hitEntity.equals(myPlayer)",
            "lastVisibilityReason = 'no_hit'",
            "lastVisibilityReason = 'target_hit'",
            "lastVisibilityReason = 'target_non_hitbox'",
            "function emitAimScanDiagnostic(scanStats)",
            "event: 'aim_debug_sample'",
            "stage: 'target_scan'",
            "candidates: scanStats.candidates || 0",
            "firstAngleDeg:",
            "firstSelectionDistance:",
            "reason: scanStats.reason || 'no_ranked_candidate'",
            "emitAimScanDiagnostic(scanStats)",
        ]:
            self.assertIn(token, text)

        visibility_fn = text.split("function checkShotRayHitsTarget(from, to, targetPlayer, physicsScratch)", 1)[1].split("function findShootableChestPoint", 1)[0]
        self.assertIn("var rayDistance = calculateVisibilityRayDistance", visibility_fn)
        self.assertIn("CONFIG.visibilityLayerMask", visibility_fn)
        self.assertIn("CONFIG.shotVisibilityQueryTriggerInteraction", visibility_fn)
        self.assertIn("if (!haveHit) {", visibility_fn)
        self.assertIn("isTargetDamageHit(", visibility_fn)
        self.assertIn("hit.colliderLayer", visibility_fn)
        self.assertIn("CONFIG.visibilityHitBoxLayer", visibility_fn)
        self.assertNotIn("return !haveHit", visibility_fn)

        shot_point_fn = text.split("function findShootableChestPoint", 1)[1].split("function redirectShootRay", 1)[0]
        self.assertIn("checkShotRayHitsTarget(origin, points[i], targetPlayer, physicsScratch)", shot_point_fn)

        write_fn = text.split("function writeAimbot()", 1)[1].split("function aimLoop()", 1)[0]
        self.assertIn("emitAimScanDiagnostic({ reason: 'refresh_failed' })", write_fn)
        self.assertIn("reason: 'write_exception'", write_fn)

        aim_loop = text.split("function aimLoop()", 1)[1].split("function installRoomHooks", 1)[0]
        self.assertIn("reason: 'mouse_read_failed'", aim_loop)

    def test_selection_checks_walls_and_actual_shoot_ray_owns_hitbox_validation(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "selectionVisibilityLayerMask: 17",
            "selectionVisibilityTargetClearance: 0.10",
            "selectionVisibilityQueryTriggerInteraction: 1",
            "Recoil_GetShootRay:                     0xB195C0",
            "function calculateSelectionRayDistance(targetDistance, originClearance, targetClearance)",
            "function checkSelectionLineOfSight(from, to, physicsScratch)",
            "function buildShotDirection(origin, target)",
            "function buildChestAimPointCandidates(basePoint, horizontalOffset, verticalOffset)",
            "function findShootableChestPoint(origin, targetPlayer, basePoint, physicsScratch)",
            "function redirectShootRay(rayBuffer)",
            "function writeRayDirection(rayBuffer, direction)",
            "stage: 'shot_ray'",
            "targets: scanStats.targets || []",
            "detail.status = 'candidate'",
            "detail.status = 'out_fov'",
            "detail.status = 'blocked_environment'",
        ]:
            self.assertIn(token, text)

        scanner_fn = text.split("function targetScanner()", 1)[1].split("function writeAimbot()", 1)[0]
        self.assertIn("checkSelectionLineOfSight(myPos, targetPos, physicsScratch)", scanner_fn)
        self.assertNotIn("checkVisibility(myPos, targetPos, p)", scanner_fn)
        self.assertIn("emitAimScanDiagnostic(scanStats)", scanner_fn)
        self.assertNotIn("if (!best) emitAimScanDiagnostic(scanStats)", scanner_fn)

        refresh_fn = text.split("function refreshCachedTargetAim()", 1)[1].split("function getBonePos", 1)[0]
        self.assertNotIn("checkVisibility(", refresh_fn)
        self.assertNotIn("checkShotRayHitsTarget(", refresh_fn)

        hooks_fn = text.split("function installRoomHooks(base)", 1)[1].split("return {", 1)[0]
        self.assertIn("base.add(RVA_AIM.Recoil_GetShootRay)", hooks_fn)
        self.assertIn("this.retBuffer = args[0]", hooks_fn)
        self.assertIn("localRecoil.equals(args[1])", hooks_fn)
        self.assertIn("redirectShootRay(this.retBuffer)", hooks_fn)

        shot_fn = text.split("function redirectShootRay(rayBuffer)", 1)[1].split("function targetScanner()", 1)[0]
        self.assertIn("var physicsScratch = createPhysicsScratch()", shot_fn)
        self.assertIn("findShootableChestPoint", shot_fn)
        self.assertIn("buildShotDirection", shot_fn)
        self.assertIn("writeRayDirection", shot_fn)

    def test_visibility_runs_on_camera_thread_with_operation_local_physics_buffers(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "targetScanIntervalMs: 30",
            "visibilityCheck: true",
            "var PHYSICS_NATIVE_OPTIONS = { abi: 'mscdecl', scheduling: 'exclusive' }",
            "function createPhysicsScratch()",
            "scene: Memory.alloc(4)",
            "ray: Memory.alloc(24)",
            "hit: Memory.alloc(0x2C)",
            "function runTargetScannerOnMainThread()",
            "runTargetScannerOnMainThread()",
        ]:
            self.assertIn(token, text)

        native_init = text.split("function initNativeFunctions()", 1)[1].split("function isValidPlayer", 1)[0]
        self.assertIn("PHYSICS_NATIVE_OPTIONS", native_init)

        module_state = text.split("var singletonGetter = null", 1)[1].split("function resetAimState", 1)[0]
        for shared_buffer in [
            "var physicsSceneBuffer = null",
            "var visibilityRayBuffer = null",
            "var visibilityHitBuffer = null",
        ]:
            self.assertNotIn(shared_buffer, module_state)

        scanner_fn = text.split("function targetScanner()", 1)[1].split("function writeAimbot()", 1)[0]
        self.assertIn("var physicsScratch = CONFIG.visibilityCheck ? createPhysicsScratch() : null", scanner_fn)

        hooks_fn = text.split("function installRoomHooks(base)", 1)[1].split("return {", 1)[0]
        camera_hook = hooks_fn.split("RVA_AIM.Brain_PushStateToUnityCamera", 1)[1].split("RVA_AIM.Recoil_GetShootRay", 1)[0]
        self.assertIn("cacheAimCamera(this.brain)", camera_hook)
        self.assertIn("runTargetScannerOnMainThread()", camera_hook)

        enable_fn = text.split("enable: function()", 1)[1].split("disable: function()", 1)[0]
        self.assertNotIn("setInterval(targetScanner", enable_fn)

    def test_manual_crosshair_movement_yields_control_and_rescans_with_hysteresis(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "manualOverrideThresholdDeg: 3.0",
            "manualOverrideAccumWindowMs: 120",
            "manualOverridePauseMs: 150",
            "targetSwitchAngleAdvantageDeg: 2.0",
            "function updateManualAimAccumulator(state, deltaDeg, nowMs)",
            "function detectManualAimOverride(currentRotation, nowMs)",
            "function chooseTargetCandidateWithHysteresis(candidates, distanceBand, currentPlayer, angleAdvantage)",
            "manualOverrideUntilMs = nowMs + CONFIG.manualOverridePauseMs",
            "lastWrittenAim.valid = false",
            "chooseTargetCandidateWithHysteresis(",
        ]:
            self.assertIn(token, text)

        write_fn = text.split("function writeAimbot()", 1)[1].split("function aimLoop()", 1)[0]
        self.assertIn("if (nowMs < manualOverrideUntilMs) return", write_fn)
        self.assertIn("if (detectManualAimOverride(currentRotation, nowMs)) return", write_fn)
        self.assertIn("lastWrittenAim.yawDeg = finalYawDeg", write_fn)
        self.assertIn("lastWrittenAim.pitchDeg = finalPitchDeg", write_fn)

        aim_loop = text.split("function aimLoop()", 1)[1].split("function installRoomHooks", 1)[0]
        self.assertIn("lastWrittenAim.valid = false", aim_loop)

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

    def test_chest_prefers_character_spine_transforms_before_animator_and_height_fallback(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "CM_spine:           0x5C",
            "CM_spine1:          0x60",
            "function getCharacterChestPos(player)",
            "character.add(OFF_AIM.CM_spine1).readPointer()",
            "character.add(OFF_AIM.CM_spine).readPointer()",
            "spine1Pos.source = 'character_spine1'",
            "spinePos.source = 'character_spine'",
        ]:
            self.assertIn(token, text)

        chest_fn = text.split("function getCharacterChestPos(player)", 1)[1].split("function getMethodInfo", 1)[0]
        self.assertLess(
            chest_fn.index("character.add(OFF_AIM.CM_spine1)"),
            chest_fn.index("character.add(OFF_AIM.CM_spine)"),
        )
        self.assertIn("distance3d(root, spine1Pos) <= CONFIG.maxBoneRootDistance", chest_fn)
        self.assertIn("distance3d(root, spinePos) <= CONFIG.maxBoneRootDistance", chest_fn)

        aim_point_fn = text.split("function getAimPoint(player, boneIndex)", 1)[1].split("function getLocalAimOrigin", 1)[0]
        self.assertIn("boneIndex === BONE.CHEST ? getCharacterChestPos(player) : null", aim_point_fn)
        self.assertLess(aim_point_fn.index("characterChest"), aim_point_fn.index("getRealBonePos"))
        self.assertLess(aim_point_fn.index("getRealBonePos"), aim_point_fn.index("getFallbackBonePos"))

    def test_bone_read_diagnostics_identify_failure_stage_and_are_rate_limited(self):
        text = read_text(SCRIPT_FILE)

        for token in [
            "var lastBoneDiagnosticAtMs = 0",
            "function emitBoneReadDiagnostic(reason, player, boneIndex, error, animatorSource)",
            "(now - lastBoneDiagnosticAtMs) < CONFIG.diagnosticLogIntervalMs",
            "stage: 'bone_read'",
            "animatorSource: animatorSource || 'player'",
            "requestedBoneIndex:",
            "humanBoneIndex:",
            "emitBoneReadDiagnostic('native_unavailable'",
            "emitBoneReadDiagnostic('animator_missing'",
            "emitBoneReadDiagnostic('bone_transform_missing'",
            "emitBoneReadDiagnostic('bone_position_invalid'",
            "emitBoneReadDiagnostic('bone_root_check_failed'",
            "emitBoneReadDiagnostic('bone_read_exception'",
        ]:
            self.assertIn(token, text)

        bone_fn = text.split("function getRealBonePos(player, boneIndex)", 1)[1].split("function isBoneNearPlayer", 1)[0]
        self.assertIn("emitBoneReadDiagnostic", bone_fn)
        self.assertIn("pos.source = 'real_bone'", bone_fn)

    def test_real_bone_prefers_current_character_animator_then_player(self):
        text = read_text(SCRIPT_FILE)
        bone_fn = text.split("function getRealBonePos(player, boneIndex)", 1)[1].split("function isBoneNearPlayer", 1)[0]

        for token in [
            "player.add(OFF_AIM.P_currentCharacter).readPointer()",
            "componentGetAnimator(currentCharacter, componentMethodInfo)",
            "animatorSource = 'currentCharacter'",
            "componentGetAnimator(player, componentMethodInfo)",
            "animatorSource = 'player'",
            "animatorAttempts = 'currentCharacter,player'",
        ]:
            self.assertIn(token, bone_fn)

        self.assertLess(
            bone_fn.index("componentGetAnimator(currentCharacter, componentMethodInfo)"),
            bone_fn.index("componentGetAnimator(player, componentMethodInfo)"),
        )

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
        self.assertEqual(manifest["config"]["aimBone"], "chest")
        self.assertEqual(manifest["config"]["maxAngleFOV"], 60.0)
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
        self.assertIn("if (!btnDown) {", aim_loop)


if __name__ == "__main__":
    unittest.main()
