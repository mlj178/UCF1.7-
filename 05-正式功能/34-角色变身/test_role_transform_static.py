from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "AAAAA-role_transform_min.js"
UI = ROOT / "AAAAA-role_transform_ui.py"


class RoleTransformStaticTests(unittest.TestCase):
    def test_script_queues_four_actions_for_main_thread_execution(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for action in (
            "local_hero",
            "local_terminator",
            "bot_hero",
            "bot_terminator",
        ):
            self.assertIn(action, script)
        for token in (
            'feature_id: "role_transform"',
            "pendingAction",
            "ModeBase_Update: 0x00AF6A00",
            "function consumePendingAction",
            "trigger: queueAction",
        ):
            self.assertIn(token, script)

    def test_script_uses_native_select_and_random_routes(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for token in (
            "NanoRoleSelect_OpenMasterRole: 0x00B4ED30",
            "Mode_Nano4_Terminator_BecomeRandomMasterHero: 0x00B42E90",
            "Mode_Nano4_Terminator_TryBecomeRandomMasterTerminator: 0x00B45B90",
            "Native.openMasterRole(selector, isHero ? 1 : 0, ptr(0))",
            "Native.becomeRandomMasterHero(mode, player, 0, ptr(0))",
            "Native.tryBecomeRandomMasterTerminator(mode, player, ptr(0))",
        ):
            self.assertIn(token, script)
        for signature in (
            "'void', ['pointer', 'int', 'pointer'], CALL_CONV",
            "'void', ['pointer', 'pointer', 'int', 'pointer'], CALL_CONV",
            "'void', ['pointer', 'pointer', 'pointer'], CALL_CONV",
        ):
            self.assertIn(signature, script)

    def test_every_action_requires_a_valid_nano4_mode(self):
        script = SCRIPT.read_text(encoding="utf-8")
        body = script.split("function executeAction", 1)[1].split(
            "function consumePendingAction", 1
        )[0]
        self.assertLess(
            body.index("Native.getModeNano4(ptr(0))"),
            body.index("applyLocalSelection(true)"),
        )

    def test_script_resolves_game_manager_with_real_generic_method_info(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for token in (
            "Singleton_GameManager_get_instance: 0x004A8170",
            "SingletonGameManager_get_instance_Method: 0x00E1CE64",
            ".add(RVA.SingletonGameManager_get_instance_Method).readPointer()",
            "Native.getGameManager(methodInfo)",
            "GameManager_allPlayers: 0x1C",
            "Il2CppArray_length: 0x0C",
            "Il2CppArray_items: 0x10",
        ):
            self.assertIn(token, script)

    def test_bot_route_filters_identity_and_dead_players(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for token in (
            "Player_clientData: 0x94",
            "ClientData_isBot: 0x1C",
            "Player_healthData: 0x1C",
            "Player_isRespawning: 0xD8",
            "HealthData_get_isDead: 0x00AE4830",
            "function isBotPlayer",
            "function isDeadPlayer",
            "function isRespawningPlayer",
            "player.add(OFF.Player_healthData).readPointer()",
            "if (!isBotPlayer(player) || isLocalPlayer(player) || isDeadPlayer(player) || isRespawningPlayer(player))",
        ):
            self.assertIn(token, script)

    def test_pending_action_is_cleared_before_native_execution(self):
        script = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("function consumePendingAction", script)
        body = script.split("function consumePendingAction", 1)[1].split(
            "function attachHooks", 1
        )[0]
        self.assertLess(body.index('Runtime.pendingAction = ""'), body.index("executeAction(action)"))

    def test_trigger_only_queues_and_does_not_call_native_functions(self):
        script = SCRIPT.read_text(encoding="utf-8")
        self.assertIn("function queueAction", script)
        body = script.split("function queueAction", 1)[1].split(
            "function status", 1
        )[0]
        self.assertIn("Runtime.pendingAction = action", body)
        self.assertNotIn("Native.openMasterRole", body)
        self.assertNotIn("Native.becomeRandomMasterHero", body)
        self.assertNotIn("Native.tryBecomeRandomMasterTerminator", body)

    def test_script_does_not_simulate_supply_pickup_or_write_nano_role(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for forbidden in (
            "SupplyBox_PickupDispatchCall",
            "SupplyBox_OnTriggerStay",
            "OnPlayerPickUpSupplyBox",
            "TRANSFORM_BOX_TYPE",
            "Player_nanoRole).write",
        ):
            self.assertNotIn(forbidden, script)

    def test_lifecycle_clears_pending_and_detaches_update_hook(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for token in (
            "function resetRuntime",
            "function cleanupHooks",
            'Runtime.pendingAction = ""',
            "hook.detach()",
            "function enableFeature",
            "function disableFeature",
            "function cleanupFeature",
            "function updateConfig",
            "rpc.exports",
        ):
            self.assertIn(token, script)

    def test_ui_exposes_four_fixed_action_buttons(self):
        ui = UI.read_text(encoding="utf-8")
        for token in (
            '"local_hero": "本地玩家：选择英雄"',
            '"local_terminator": "本地玩家：选择超级终结者"',
            '"bot_hero": "所有 Bot：随机英雄"',
            '"bot_terminator": "所有 Bot：随机超级终结者"',
            "def trigger_action(self, action):",
            'self._run_rpc("trigger", action)',
        ):
            self.assertIn(token, ui)
        for forbidden in ("toggle_probe", "BooleanVar", "probe_button", "desired_probe"):
            self.assertNotIn(forbidden, ui)

    def test_ui_enables_feature_after_connection(self):
        ui = UI.read_text(encoding="utf-8")
        connected = ui.split("    def _on_connected", 1)[1].split(
            "    def on_message", 1
        )[0]
        self.assertIn('self._run_rpc("enable")', connected)
        self.assertNotIn("self.config()", connected)

    def test_ui_uses_background_connection_and_safe_shutdown(self):
        ui = UI.read_text(encoding="utf-8")
        for token in (
            "customtkinter",
            "threading.Thread(target=self._connect_worker, daemon=True).start()",
            "queue.Queue",
            "self.rpc_lock = threading.Lock()",
            "with self.rpc_lock:",
            "self.connection_label = ctk.CTkLabel",
        ):
            self.assertIn(token, ui)
        self.assertNotIn("self.state = ctk.CTkLabel", ui)
        shutdown_body = ui.split("    def _shutdown_worker", 1)[1]
        self.assertNotIn("script.exports_sync.cleanup()", shutdown_body)


if __name__ == "__main__":
    unittest.main()
