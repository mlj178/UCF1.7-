import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "script.js"
UI_FILE = BASE_DIR / "AAAAA-fixed_point_teleport_ui.py"
DOC_FILE = BASE_DIR / "定点瞬移-简要说明.md"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class FixedPointTeleportStaticTests(unittest.TestCase):

    def test_js_contains_feature_id_rvas_and_offsets(self):
        text = read_text(JS_FILE)

        required_tokens = [
            'feature_id: "fixed_point_teleport"',
            "Player_Update: 0x00B551D0",
            "Player_get_isMyPlayer: 0x00B55FD0",
            "Player_SetPos: 0x00B534C0",
            "Component_get_transform: 0x0032CF40",
            "Transform_get_position_Injected: 0x003F4280",
            "ModeBase_UpdateTimeUI: 0x00AF6930",
            "GameManager_GameRoundEnd: 0x00AFAA40",
            "GameManager_NewGameRoundStart: 0x00AEBCB0",
            "GameManager_OnDestroy: 0x00AEBD40",
            "Player_characterController: 0x2C",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_js_uses_player_setpos_for_teleport_and_does_not_replace(self):
        text = read_text(JS_FILE)

        self.assertIn("Interceptor.attach", text)
        self.assertNotIn("Interceptor.replace", text)
        self.assertIn("native.playerSetPos", text)
        self.assertIn("function requestTeleportToSavedPoint()", text)
        self.assertIn("function performPendingActions(player)", text)
        self.assertIn("native.playerSetPos(player, point.x, point.y, point.z, ptr(0))", text)
        self.assertNotIn("Transform_set_position_Injected", text)

    def test_js_defers_save_and_teleport_to_player_update(self):
        text = read_text(JS_FILE)

        save_rpc = text.split("savepoint: function ()", 1)[1].split("teleporttopoint:", 1)[0]
        teleport_rpc = text.split("teleporttopoint: function ()", 1)[1].split("savepoint2:", 1)[0]
        save2_rpc = text.split("savepoint2: function ()", 1)[1].split("teleporttopoint2:", 1)[0]
        teleport2_rpc = text.split("teleporttopoint2: function ()", 1)[1].split("}", 1)[0]
        player_update_hook = text.split('attachHook("Player.Update"', 1)[1].split("});", 1)[0]

        self.assertIn("queueSavePoint(1)", save_rpc)
        self.assertIn("queueTeleportToPoint(1)", teleport_rpc)
        self.assertIn("queueSavePoint(2)", save2_rpc)
        self.assertIn("queueTeleportToPoint(2)", teleport2_rpc)
        self.assertNotIn("readPlayerPosition", save_rpc)
        self.assertNotIn("native.playerSetPos", teleport_rpc)
        self.assertNotIn("readPlayerPosition", save2_rpc)
        self.assertNotIn("native.playerSetPos", teleport2_rpc)
        self.assertIn("performPendingActions(args[0])", player_update_hook)

    def test_js_clears_saved_point_and_pending_actions_on_runtime_reset(self):
        text = read_text(JS_FILE)

        reset_fn = text.split("function resetRuntime(reason)", 1)[1].split("function captureLocalPlayer", 1)[0]
        self.assertIn("resetSavedPointSlots()", reset_fn)
        self.assertIn("Runtime.pending.saveSlot = 0", reset_fn)
        self.assertIn("Runtime.pending.teleportSlot = 0", reset_fn)

    def test_js_preserves_saved_points_across_round_lifecycle(self):
        text = read_text(JS_FILE)

        self.assertIn("function clearPendingRoundActions(reason)", text)

        clear_pending_fn = text.split("function clearPendingRoundActions(reason)", 1)[1].split(
            "function handleRoundBoundary", 1
        )[0]
        round_end_hook = text.split('attachHook("GameManager.GameRoundEnd"', 1)[1].split(
            'attachHook("GameManager.NewGameRoundStart"', 1
        )[0]
        new_round_hook = text.split('attachHook("GameManager.NewGameRoundStart"', 1)[1].split(
            'attachHook("GameManager.OnDestroy"', 1
        )[0]
        round_clear_forbidden_tokens = [
            "resetRuntime",
            "resetSavedPointSlots",
            "Runtime.savedPoints",
            "Runtime.roomGeneration",
        ]

        self.assertIn("Runtime.pending.saveSlot = 0", clear_pending_fn)
        self.assertIn("Runtime.pending.teleportSlot = 0", clear_pending_fn)
        for forbidden_token in round_clear_forbidden_tokens:
            self.assertNotIn(forbidden_token, clear_pending_fn)

        self.assertIn('clearPendingRoundActions("game_round_end")', round_end_hook)
        self.assertNotIn("handleRoundBoundary", round_end_hook)
        self.assertIn('clearPendingRoundActions("new_game_round_start")', new_round_hook)
        self.assertNotIn("handleRoundBoundary", new_round_hook)
        for hook_segment in [round_end_hook, new_round_hook]:
            for forbidden_token in round_clear_forbidden_tokens:
                self.assertNotIn(forbidden_token, hook_segment)

    def test_js_keeps_full_reset_for_room_lifecycle(self):
        text = read_text(JS_FILE)

        room_boundary_fn = text.split("function handleRoundBoundary(reason, nextModeBase)", 1)[1].split(
            "function handleModeBaseSeen", 1
        )[0]
        mode_base_seen_fn = text.split("function handleModeBaseSeen(modeBase)", 1)[1].split(
            "function captureLocalPlayer", 1
        )[0]
        mode_base_hook = text.split('attachHook("ModeBase.UpdateTimeUI"', 1)[1].split(
            'attachHook("GameManager.GameRoundEnd"', 1
        )[0]
        game_manager_destroy_hook = text.split('attachHook("GameManager.OnDestroy"', 1)[1].split(
            "Runtime.initialized = true", 1
        )[0]

        self.assertIn("handleModeBaseSeen(args[0])", mode_base_hook)
        self.assertIn('handleRoundBoundary("mode_base_changed", modeBase)', mode_base_seen_fn)
        self.assertIn('handleRoundBoundary("game_manager_destroy")', game_manager_destroy_hook)
        self.assertIn("resetRuntime(Runtime.stats.lastRoomReason)", room_boundary_fn)

    def test_js_saved_point_is_bound_to_current_room_generation(self):
        text = read_text(JS_FILE)

        self.assertIn("roomGeneration", text)
        self.assertIn("Runtime.roomGeneration += 1", text)
        self.assertIn("room_generation: Runtime.roomGeneration", text)
        self.assertIn("function hasValidSavedPoint(slot)", text)
        self.assertIn("Runtime.savedPoints[slot].room_generation !== Runtime.roomGeneration", text)
        self.assertIn('"saved_point_expired"', text)

    def test_js_saves_position_from_local_player_only(self):
        text = read_text(JS_FILE)

        self.assertIn("function captureLocalPlayer", text)
        self.assertIn("native.isMyPlayer(player, ptr(0))", text)
        self.assertIn("function queueSavePoint(slot)", text)
        self.assertIn("Runtime.savedPoints", text)
        self.assertIn("saved_point", text)

        capture_fn = text.split("function captureLocalPlayer(player, reason)", 1)[1].split("function attachHook", 1)[0]
        self.assertIn("!isReadablePtr(player)", capture_fn)
        self.assertLess(
            capture_fn.index("!isReadablePtr(player)"),
            capture_fn.index("native.isMyPlayer(player, ptr(0))"),
        )

    def test_js_validates_transform_pointer_before_reading_position(self):
        text = read_text(JS_FILE)

        read_position_fn = text.split("function readPlayerPosition(player)", 1)[1].split("function canQueueAction", 1)[0]
        self.assertIn("!isReadablePtr(transform)", read_position_fn)
        self.assertLess(
            read_position_fn.index("!isReadablePtr(transform)"),
            read_position_fn.index("native.transformGetPosition(transform, posBuffer, ptr(0))"),
        )

    def test_js_exports_standard_rpc_and_point_commands(self):
        text = read_text(JS_FILE)

        self.assertIn("rpc.exports", text)
        for export_name in [
            "enable",
            "disable",
            "status",
            "cleanup",
            "setconfig",
            "savepoint",
            "teleporttopoint",
            "savepoint2",
            "teleporttopoint2",
        ]:
            self.assertRegex(text, rf"\b{export_name}\s*:")

        self.assertNotRegex(text, r"\bclearpoint\s*:")
        self.assertNotIn("clearSavedPoint", text)
        self.assertNotIn("clearCount", text)
        self.assertNotIn("clear_count", text)

        for status_key in [
            "has_saved_point",
            "saved_point",
            "last_teleport_result",
            "save_count",
            "teleport_count",
        ]:
            self.assertIn(status_key, text)

    def test_ui_loads_script_and_uses_standard_rpc(self):
        text = read_text(UI_FILE)

        self.assertIn("import customtkinter as ctk", text)
        self.assertIn("import frida", text)
        self.assertIn("import psutil", text)
        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "AAAAA-fixed_point_teleport_min.js")', text)
        self.assertIn('GAME_PROCESS_NAME = "UnityCrossFire.exe"', text)
        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn("ctk.CTkButton", text)
        self.assertIn("ctk.CTkTextbox", text)
        self.assertIn("self.script.exports_sync.enable()", text)
        self.assertIn("self.script.exports_sync.disable()", text)
        self.assertIn("self.script.exports_sync.status()", text)
        self.assertIn("self.script.exports_sync.cleanup()", text)
        self.assertIn("self.script.exports_sync.setconfig", text)
        self.assertIn("self.script.exports_sync.savepoint()", text)
        self.assertIn("self.script.exports_sync.teleporttopoint()", text)
        self.assertIn("self.script.exports_sync.savepoint2()", text)
        self.assertIn("self.script.exports_sync.teleporttopoint2()", text)
        self.assertNotIn("self.script.exports_sync.clearpoint()", text)

    def test_ui_exposes_second_point_slot(self):
        text = read_text(UI_FILE)

        self.assertIn("点位1", text)
        self.assertIn("点位2", text)
        self.assertIn("保存点位2", text)
        self.assertIn("瞬移到点位2", text)
        self.assertIn("savepoint2", text)
        self.assertIn("teleporttopoint2", text)

    def test_ui_uses_point_one_labels_without_legacy_single_point_copy(self):
        text = read_text(UI_FILE)

        self.assertNotRegex(text, re.compile(r"hotkey|keyboard|RegisterHotKey|VK_", re.I))
        self.assertIn("保存点位1", text)
        self.assertIn("瞬移到点位1", text)
        self.assertNotIn("保存当前位置", text)
        self.assertNotIn("瞬移到保存点", text)

    def test_doc_records_sources_and_minimal_scope(self):
        text = read_text(DOC_FILE)

        for token in [
            "feature_id: fixed_point_teleport",
            "Player.SetPos",
            "RVA 0xB534C0",
            "Player.Update",
            "RVA 0xB551D0",
            "Player.get_isMyPlayer",
            "RVA 0xB55FD0",
            "点位1",
            "点位2",
            "F1",
            "F2",
        ]:
            self.assertIn(token, text)


if __name__ == "__main__":
    unittest.main()
