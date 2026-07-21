import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "features"


FEATURES_UNDER_TEST = {
    "27_game_mode_override": {
        "feature_id": "27_game_mode_override",
        "canonical_id": "game_mode_override",
        "display_name": "游戏模式切换",
        "desc": "切换游戏模式，请在游戏房间创建前应用。",
        "config_keys": {"enabled", "mode_key"},
        "rpc": {"enable", "disable", "setconfig", "status", "cleanup", "dispose"},
        "panel_marker": "MODE_OPTIONS",
    },
    "28_wall_noclip": {
        "feature_id": "28_wall_noclip",
        "canonical_id": "wall_noclip",
        "display_name": "人体穿墙",
        "desc": "按住Alt，让玩家穿过墙体等障碍物。",
        "config_keys": {"horizontalScale", "requireAltKey"},
        "rpc": {"enable", "disable", "setconfig", "status", "cleanup"},
        "panel_marker": "build_card",
    },
    "29_bullet_wall_penetration": {
        "feature_id": "29_bullet_wall_penetration",
        "canonical_id": "bullet_wall_penetration",
        "display_name": "子弹穿墙",
        "desc": "玩家开火允许子弹穿墙。",
        "config_keys": {"forceHitboxOnlyDuringLocalDamage", "logEveryDamageHits"},
        "rpc": {"enable", "disable", "setconfig", "status", "cleanup"},
        "panel_marker": "build_card",
    },
}


class FeaturePluginIntegrationTest(unittest.TestCase):
    def test_feature_directories_have_required_plugin_files(self):
        for dirname in FEATURES_UNDER_TEST:
            with self.subTest(dirname=dirname):
                feature_dir = FEATURES / dirname
                for filename in ("__init__.py", "manifest.json", "feature.py", "panel.py", "events.py", "script.js"):
                    self.assertTrue((feature_dir / filename).is_file(), f"{dirname}/{filename} is missing")

    def test_manifests_match_2_2_plugin_contract(self):
        for dirname, expected in FEATURES_UNDER_TEST.items():
            with self.subTest(dirname=dirname):
                manifest = json.loads((FEATURES / dirname / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["feature_id"], expected["feature_id"])
                self.assertEqual(manifest["canonical_id"], expected["canonical_id"])
                self.assertEqual(manifest["display_name"], expected["display_name"])
                self.assertEqual(manifest["desc"], expected["desc"])
                self.assertNotEqual(manifest["icon"], "*")
                self.assertTrue(manifest["layout"].get("title_color"))
                self.assertEqual(manifest["script"], "script.js")
                self.assertEqual(manifest["runtime"]["type"], "plugin_script")
                self.assertTrue(manifest["lifecycle"]["cleanup"])
                self.assertIn("restore", manifest["lifecycle"])
                self.assertTrue(set(manifest["rpc"]).issuperset(expected["rpc"]))
                self.assertTrue(set(manifest["config"]).issuperset(expected["config_keys"]))
                self.assertIn("sync_enabled_from_config", manifest["state"])

    def test_game_mode_override_card_does_not_expose_probe_logging(self):
        feature_dir = FEATURES / "27_game_mode_override"
        manifest = json.loads((feature_dir / "manifest.json").read_text(encoding="utf-8"))
        panel_text = (feature_dir / "panel.py").read_text(encoding="utf-8")
        manifest_text = json.dumps(manifest, ensure_ascii=False)
        self.assertNotIn("probe", manifest_text.lower())
        self.assertNotIn("探测日志", panel_text)
        self.assertNotIn("probe", panel_text.lower())

    def test_game_mode_override_installs_only_esp_safe_gameplay_hooks(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]
        hook_targets = re.findall(r"Interceptor\.attach\(base\.add\(RVA\.([A-Za-z0-9_]+)\)", install_block)
        self.assertEqual(
            hook_targets,
            [
                "UI_GameRoom_OnStartGameBtnDown",
                "MapAsset_ApplyGameSetting",
                "UI_GameRoom_GenerateBotClient",
                "GameManager_AddPlayers",
                "MapManager_Awake",
                "MapManager_GetSpawnPoint",
                "GameManager_GiveWeaponByBag",
                "Player_Spawn",
                "Player_Respawn",
            ],
        )
        forbidden_hooks = {
            "ModeBase_UpdateTimeUI",
            "ModeBase_OnStartNewGameRound",
            "ModeBase_Nano_OnStartNewGameRound",
            "ModeBase_Nano_CheckRoundOver",
            "GameManager_GameRoundEnd",
            "MapManager_NewGameRoundStart",
            "GameManager_DeathEventBroadcast",
            "Mode_TeamDeath_DeathEvent",
            "ModeBase_Nano_DeathEvent",
            "Mode_Nano4_DeathEvent",
            "Mode_Nano4_Terminator_DeathEvent",
            "Mode_Nano6_DeathEvent",
            "Player_OnEntityDeath",
        }
        self.assertTrue(forbidden_hooks.isdisjoint(hook_targets))
        self.assertIn("Runtime.getWpnData = new NativeFunction", install_block)
        self.assertIn("maybeOverrideLimitedBotGrant(args)", install_block)
        self.assertIn("normalizeRoomBotTeamsForTeamRules('GenerateBotClient.leave')", install_block)
        self.assertIn("normalizeRoomBotTeamsForTeamRules('GameManager.AddPlayers.enter')", install_block)
        self.assertIn("ensureTeamRuleSpawnFallbacks('GameManager.AddPlayers.enter')", install_block)
        self.assertIn("ensureTeamRuleSpawnFallbacks('MapManager.Awake')", install_block)
        self.assertIn("ensureNeutralSpawnFallbackFromTeam('GetSpawnPoint')", install_block)
        self.assertIn("ensureTeamSpawnFallbackFromNeutral(team, 'GetSpawnPoint')", install_block)
        self.assertEqual(install_block.count("resetWeaponGrantForPlayer(args[0])"), 2)
        self.assertNotIn("probeBotPipeline(", install_block)
        self.assertNotIn("probeLifecycle(", install_block)
        self.assertNotIn("probeWeaponGrant(", install_block)

    def test_game_mode_override_uses_low_risk_handgun_bot_fallback(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        self.assertIn("var HANDGUN_BOT_FALLBACK_WEAPON_INDEX = 20", script_text)
        self.assertIn("if (Runtime.modeKey === 'handgun') return HANDGUN_BOT_FALLBACK_WEAPON_INDEX", script_text)
        self.assertNotIn("var HANDGUN_BOT_FALLBACK_WEAPON_INDEX = 1168", script_text)

    def test_game_mode_override_normalizes_bot_teams_only_for_team_rules(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]

        self.assertIn("function teamRulesAreActiveForCurrentStart()", script_text)
        self.assertIn("function normalizeRoomBotTeamsForTeamRules(reason)", script_text)
        self.assertIn("function ensureTeamRuleSpawnFallbacks(reason)", script_text)
        helper_block = script_text.split("function teamRulesAreActiveForCurrentStart()", 1)[1].split("function findTargetMapAsset", 1)[0]
        self.assertIn("Runtime.lastApplied.gameMode === MODES.team_death.gameMode", helper_block)
        self.assertIn("readU8(clientData.add(OFF.ClientData_isBot))", helper_block)
        self.assertIn("var desiredTeam = nextTeam", helper_block)
        self.assertIn("if (joinTeam !== desiredTeam)", helper_block)
        self.assertIn("clientData.add(OFF.ClientData_joinTeam).writeS32(desiredTeam)", helper_block)
        self.assertNotIn("if (joinTeam !== 2 && joinTeam !== null) continue", helper_block)
        self.assertIn("normalizeRoomBotTeamsForTeamRules('ApplyGameSetting.leave')", install_block)
        self.assertIn("normalizeRoomBotTeamsForTeamRules('GenerateBotClient.leave')", install_block)
        self.assertIn("normalizeRoomBotTeamsForTeamRules('GameManager.AddPlayers.enter')", install_block)
        self.assertIn("ensureTeamSpawnFallbackFromNeutral(0, reason)", helper_block)
        self.assertIn("ensureTeamSpawnFallbackFromNeutral(1, reason)", helper_block)
        self.assertLess(
            install_block.index("normalizeRoomBotTeamsForTeamRules('GenerateBotClient.leave')"),
            install_block.index("normalizeRoomBotTeamsForTeamRules('GameManager.AddPlayers.enter')"),
        )
        self.assertLess(
            install_block.index("normalizeRoomBotTeamsForTeamRules('GameManager.AddPlayers.enter')"),
            install_block.index("Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_GetSpawnPoint)"),
        )
        self.assertNotIn("normalizeRoomBotTeamsForTeamRules", install_block.split("Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_GetSpawnPoint)", 1)[1])

    def test_bullet_wall_penetration_keeps_hitbox_only_default_hidden(self):
        feature_dir = FEATURES / "29_bullet_wall_penetration"
        manifest = json.loads((feature_dir / "manifest.json").read_text(encoding="utf-8"))
        panel_text = (feature_dir / "panel.py").read_text(encoding="utf-8")
        manifest_text = json.dumps(manifest, ensure_ascii=False)
        control_keys = {control.get("key") for control in manifest.get("controls", [])}

        self.assertIs(manifest["config"].get("forceHitboxOnlyDuringLocalDamage"), True)
        self.assertNotIn("forceHitboxOnlyDuringLocalDamage", control_keys)
        self.assertNotIn("HitBox-only", manifest_text)
        self.assertNotIn("forceHitboxOnlyDuringLocalDamage_switch", manifest.get("ui_handles", {}))
        self.assertNotIn("HitBox-only", panel_text)
        self.assertNotIn("forceHitboxOnlyDuringLocalDamage", panel_text)

    def test_bullet_wall_penetration_shares_row_with_fast_gunstock(self):
        manifests = []
        for manifest_path in FEATURES.glob("*/manifest.json"):
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if manifest.get("tab") == "weapon_tab":
                manifests.append(manifest)

        positions = {}
        row = 0
        col = 0
        for manifest in sorted(manifests, key=lambda item: int(item.get("order", 0))):
            colspan = int((manifest.get("layout") or {}).get("columnspan", 1))
            if colspan >= 2 and col == 1:
                row += 1
                col = 0
            positions[manifest["feature_id"]] = {"row": row, "col": col, "columnspan": colspan}
            if colspan >= 2 or col == 1:
                row += 1
                col = 0
            else:
                col = 1

        fast_gunstock = positions["fast_gunstock"]
        bullet_wall = positions["29_bullet_wall_penetration"]
        self.assertEqual(fast_gunstock["columnspan"], 1)
        self.assertEqual(bullet_wall["columnspan"], 1)
        self.assertEqual(fast_gunstock["row"], bullet_wall["row"])
        self.assertEqual(fast_gunstock["col"], 0)
        self.assertEqual(bullet_wall["col"], 1)

    def test_runtime_script_keeps_original_identity_and_adds_2_2_rpc_adapter(self):
        for dirname, expected in FEATURES_UNDER_TEST.items():
            with self.subTest(dirname=dirname):
                feature_dir = FEATURES / dirname
                adapted = (feature_dir / "script.js").read_text(encoding="utf-8")
                self.assertIn(expected["canonical_id"], adapted)
                self.assertIn("setConfig", adapted)
                self.assertIn("setconfig", adapted)
                self.assertIn("config", adapted.split("enable:", 1)[1].split("disable:", 1)[0])

    def test_python_shell_files_use_plugin_base_and_generic_callbacks(self):
        for dirname, expected in FEATURES_UNDER_TEST.items():
            with self.subTest(dirname=dirname):
                feature_dir = FEATURES / dirname
                feature_py = (feature_dir / "feature.py").read_text(encoding="utf-8")
                panel_py = (feature_dir / "panel.py").read_text(encoding="utf-8")
                events_py = (feature_dir / "events.py").read_text(encoding="utf-8")
                self.assertIn("PluginFeatureBase", feature_py)
                self.assertIn("class PluginFeature", feature_py)
                self.assertIn(expected["panel_marker"], panel_py)
                self.assertIn('callbacks["toggle"]', panel_py)
                self.assertNotIn("FridaManager", panel_py)
                self.assertNotIn("exports_sync", panel_py)
                self.assertIn("handle_event", events_py)


if __name__ == "__main__":
    unittest.main()
