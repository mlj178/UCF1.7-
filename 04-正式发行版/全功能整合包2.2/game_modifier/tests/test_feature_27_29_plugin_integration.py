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
                "ModeBase_Nano_OnStartNewGameRound",
                "StartGenerateSupplyBox",
                "Mode_Nano4_Terminator_UpgrandeBoxGenerator",
                "UI_GameRoom_GenerateBotClient",
                "GameManager_AddPlayers",
                "MapManager_Awake",
                "MapManager_GetSupplyBoxPoint",
                "MapManager_GetSpawnPoint",
                "GameManager_GiveWeaponByBag",
                "Player_Spawn",
                "Player_Respawn",
            ],
        )
        forbidden_hooks = {
            "ModeBase_UpdateTimeUI",
            "ModeBase_OnStartNewGameRound",
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

    def test_game_mode_override_scopes_nano4t_supplybox_attribute_chain(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]

        self.assertIn("Mode_Nano4_Terminator_TypeInfo", script_text)
        self.assertIn("StartGenerateSupplyBox", script_text)
        self.assertIn("TERMINATOR_SUPPLY_GHOST_ATTR_ID = 8", script_text)
        self.assertIn("TERMINATOR_SUPPLY_HUMAN_ATTR_ID = 18", script_text)
        self.assertIn("function terminatorSupplyCompatIsActive()", script_text)
        self.assertIn("Runtime.modeKey === 'nano4_terminator'", script_text)
        self.assertIn("Runtime.lastApplied.gameMode === MODES.nano4_terminator.gameMode", script_text)
        self.assertIn("function ensureTerminatorSupplyAttributeChain(modeInstance, reason)", script_text)
        self.assertIn("function loadTerminatorAttributePointers(modeInstance)", script_text)
        self.assertIn("instanceClass.equals(typeInfo)", script_text)
        self.assertIn("Mode_Nano4_Terminator_attribute_Nano: 0xE0", script_text)
        self.assertIn("Mode_Nano4_Terminator_attribute_Human: 0xE4", script_text)
        self.assertIn("OFF.Mode_Nano4_Terminator_attribute_Nano", script_text)
        self.assertIn("OFF.Mode_Nano4_Terminator_attribute_Human", script_text)
        self.assertIn("writeManagedReference(field, attr)", script_text)
        self.assertIn("ensureTerminatorSupplyAttributeChain(args[0], 'ModeBase_Nano.OnStartNewGameRound.enter')", install_block)
        self.assertIn("ensureTerminatorSupplyAttributeChain(args[0], 'StartGenerateSupplyBox.enter')", install_block)
        self.assertNotIn("function applyTerminatorBattleRoundFlag(reason)", script_text)
        self.assertNotIn("Mode_Nano4_Terminator_isBattleRound", script_text)
        self.assertNotIn("isBattleRound=1", script_text)
        self.assertIn("ensureNeutralSpawnFallbackFromTeam('GetSpawnPoint')", install_block)
        self.assertIn("ensureTeamSpawnFallbackFromNeutral(team, 'GetSpawnPoint')", install_block)
        self.assertEqual(install_block.count("resetWeaponGrantForPlayer(args[0])"), 2)
        self.assertNotIn("probeBotPipeline(", install_block)
        self.assertNotIn("probeLifecycle(", install_block)
        self.assertNotIn("probeWeaponGrant(", install_block)

    def test_game_mode_override_falls_back_supplybox_points_on_non_bio_maps(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]

        self.assertIn("MapManager_SP_SupplyBox: 0x1C", script_text)
        self.assertIn("MapManager_SP_RedBox: 0x20", script_text)
        self.assertIn("MapManager_SP_BlueBox: 0x24", script_text)
        self.assertIn("MapManager_IDList_SupplyBox: 0x28", script_text)
        self.assertIn("MapManager_IDList_RedBox: 0x2C", script_text)
        self.assertIn("MapManager_IDList_BlueBox: 0x30", script_text)
        self.assertIn("System_Collections_Generic_List_int_TypeInfo: 0x00E1F6D8", script_text)
        self.assertIn("ManagedObject_New: 0x00167D20", script_text)
        self.assertIn("List_int_ctor: 0x00430E90", script_text)
        self.assertIn("List_int_Add: 0x009EF780", script_text)
        self.assertIn("function terminatorSupplyPointFallbackIsActive()", script_text)
        self.assertIn("function ensureTerminatorSupplyPointFallbacks(reason)", script_text)
        self.assertIn("key === 'supply'", script_text)
        self.assertIn("['bl', 'supply', 'neutral', 'gr']", script_text)
        self.assertIn("['gr', 'supply', 'neutral', 'bl']", script_text)
        self.assertIn("ensureSupplyPointArray(OFF.MapManager_SP_SupplyBox", script_text)
        self.assertIn("ensureSupplyPointArray(OFF.MapManager_SP_RedBox", script_text)
        self.assertIn("ensureSupplyPointArray(OFF.MapManager_SP_BlueBox", script_text)
        self.assertIn("ensureSupplyPointIndexList(OFF.MapManager_IDList_SupplyBox", script_text)
        self.assertIn("ensureSupplyPointIndexList(OFF.MapManager_IDList_RedBox", script_text)
        self.assertIn("ensureSupplyPointIndexList(OFF.MapManager_IDList_BlueBox", script_text)
        self.assertIn("Runtime.listIntAdd(listPtr, i, ptr(0))", script_text)
        self.assertIn("Runtime.objectNew(listTypeInfo)", script_text)
        self.assertIn("Runtime.listIntCtor(listPtr, ptr(0))", script_text)
        self.assertIn("writeManagedReference(targetField, fallback.ptr)", script_text)
        supply_fallback_block = script_text.split("function terminatorSupplyPointFallbackIsActive()", 1)[1].split("function ensureSupplyPointArray", 1)[0]
        self.assertNotIn("!isNanoGameModeValue(Runtime.lastApplied.sourceMapMode)", supply_fallback_block)
        self.assertIn("ensureTerminatorSupplyPointFallbacks('MapManager.Awake')", install_block)
        self.assertIn("ensureTerminatorSupplyPointFallbacks('ModeBase_Nano.OnStartNewGameRound.enter')", install_block)
        self.assertIn("ensureTerminatorSupplyPointFallbacks('StartGenerateSupplyBox.enter')", install_block)
        self.assertIn("supplyBoxSpawnFallbackCount", script_text)
        self.assertIn("supplyBoxSpawnFallbackLast", script_text)
        self.assertNotIn("Instantiate", script_text)

    def test_game_mode_override_logs_nano4t_supplybox_pipeline_diagnostics(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]

        self.assertIn("MapManager_GetSupplyBoxPoint: 0x00AEB8A0", script_text)
        self.assertIn("SUPPLY_BOX_TYPE_YELLOW = 0", script_text)
        self.assertIn("SUPPLY_BOX_TYPE_RED = 1", script_text)
        self.assertIn("SUPPLY_BOX_TYPE_BLUE = 2", script_text)
        self.assertIn("function summarizeSupplyPointState(reason)", script_text)
        self.assertIn("function logSupplyBoxPipeline(stage, extra)", script_text)
        self.assertIn("function supplyBoxTypeLabel(type)", script_text)
        self.assertIn("Runtime.supplyBoxPipelineDiagnostics", script_text)
        self.assertIn("Runtime.supplyBoxPointRequests", script_text)
        self.assertIn("logSupplyBoxPipeline('MapManager.Awake.afterSupplyFallback'", install_block)
        self.assertIn("logSupplyBoxPipeline('ModeBase_Nano.OnStartNewGameRound.afterSupplyFallback'", install_block)
        self.assertIn("logSupplyBoxPipeline('StartGenerateSupplyBox.enter.afterSupplyFallback'", install_block)
        self.assertIn("logSupplyBoxPipeline('StartGenerateSupplyBox.leave.afterGeneratorCheck'", install_block)
        self.assertIn("logSupplyBoxPipeline('UpgrandeBoxGenerator.enter'", install_block)
        self.assertIn("Interceptor.attach(base.add(RVA.MapManager_GetSupplyBoxPoint)", install_block)
        self.assertIn("logSupplyBoxPipeline('GetSupplyBoxPoint.enter'", install_block)
        self.assertIn("logSupplyBoxPipeline('GetSupplyBoxPoint.leave'", install_block)
        self.assertIn("supplyBoxPipelineDiagnostics", script_text)
        self.assertIn("supplyBoxPointRequests", script_text)

    def test_game_mode_override_primes_supplybox_points_at_get_point_entry(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]
        get_point_block = install_block.split("RVA.MapManager_GetSupplyBoxPoint", 1)[1].split("Runtime.hooks.push(Interceptor.attach(base.add(RVA.MapManager_GetSpawnPoint)", 1)[0]

        self.assertNotIn("Runtime.mapManager = args[0]", get_point_block)
        self.assertIn("ensureTerminatorSupplyPointFallbacks('GetSupplyBoxPoint.enter')", get_point_block)
        self.assertLess(
            get_point_block.index("logSupplyBoxPipeline('GetSupplyBoxPoint.enter'"),
            get_point_block.index("ensureTerminatorSupplyPointFallbacks('GetSupplyBoxPoint.enter')"),
        )

    def test_game_mode_override_validates_cached_map_manager_before_supplybox_fallback(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        helper_block = script_text.split("function isUsableMapManagerForSupplyFallback", 1)[1].split("function ensureSupplyPointArray", 1)[0]
        ensure_block = script_text.split("function ensureTerminatorSupplyPointFallbacks", 1)[1].split("function ensureTeamSpawnFallbackFromNeutral", 1)[0]

        self.assertIn("function isUsablePointer(value)", script_text)
        self.assertIn("ptr('0x10000')", script_text)
        self.assertIn("isNullOrLikelyArrayPointer", helper_block)
        self.assertIn("sourceOffsets", helper_block)
        self.assertIn("OFF.MapManager_SP_BL", helper_block)
        self.assertIn("OFF.MapManager_SP_GR", helper_block)
        self.assertNotIn("OFF.MapManager_SP_RedBox", helper_block)
        self.assertNotIn("OFF.MapManager_SP_BlueBox", helper_block)
        self.assertIn("hasFallbackSource", helper_block)
        self.assertIn("if (!isUsableMapManagerForSupplyFallback(Runtime.mapManager", ensure_block)

    def test_game_mode_override_rebuilds_invalid_supplybox_id_lists(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        helper_block = script_text.split("function ensureSupplyPointIndexList", 1)[1].split("function ensureTerminatorSupplyPointFallbacks", 1)[0]

        self.assertIn("var shouldCreateList = !listPtr || currentSize === null", helper_block)
        self.assertIn("if (shouldCreateList)", helper_block)
        self.assertIn("writeManagedReference(listField, listPtr)", helper_block)
        self.assertIn("currentSize === null", helper_block)

    def test_game_mode_override_uses_nano4t_upgrade_box_generator_coroutines(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]

        self.assertIn("Mode_Nano4_Terminator_UpgrandeBoxGenerator: 0x00B45E00", script_text)
        self.assertIn("UnityEngine_MonoBehaviour_StartCoroutine_Auto: 0x004E8830", script_text)
        self.assertIn("TERMINATOR_UPGRADE_BOX_RED_DELAY = 62", script_text)
        self.assertIn("TERMINATOR_UPGRADE_BOX_BLUE_DELAY = 91", script_text)
        self.assertIn("TERMINATOR_UPGRADE_BOX_RED_TEAM = 0", script_text)
        self.assertIn("TERMINATOR_UPGRADE_BOX_BLUE_TEAM = 1", script_text)
        self.assertIn("Runtime.createUpgradeBoxGenerator = new NativeFunction", install_block)
        self.assertIn("base.add(RVA.Mode_Nano4_Terminator_UpgrandeBoxGenerator)", install_block)
        self.assertIn("Runtime.startCoroutineAuto = new NativeFunction", install_block)
        self.assertIn("base.add(RVA.UnityEngine_MonoBehaviour_StartCoroutine_Auto)", install_block)
        self.assertIn("['pointer', 'int', 'int', 'pointer']", install_block)
        self.assertIn("['pointer', 'pointer', 'pointer']", install_block)
        self.assertIn("function markNativeUpgradeBoxGeneratorStarted(modeInstance, reason)", script_text)
        self.assertIn("function ensureTerminatorUpgradeBoxGeneratorsStarted(modeInstance, reason)", script_text)
        self.assertIn("isTerminatorModeInstance(modeInstance)", script_text)
        self.assertIn("Runtime.createUpgradeBoxGenerator(modeInstance, TERMINATOR_UPGRADE_BOX_RED_DELAY, TERMINATOR_UPGRADE_BOX_RED_TEAM, ptr(0))", script_text)
        self.assertIn("Runtime.createUpgradeBoxGenerator(modeInstance, TERMINATOR_UPGRADE_BOX_BLUE_DELAY, TERMINATOR_UPGRADE_BOX_BLUE_TEAM, ptr(0))", script_text)
        self.assertIn("Runtime.startCoroutineAuto(modeInstance, redGenerator, ptr(0))", script_text)
        self.assertIn("Runtime.startCoroutineAuto(modeInstance, blueGenerator, ptr(0))", script_text)
        self.assertIn("markNativeUpgradeBoxGeneratorStarted(args[0], 'UpgrandeBoxGenerator.enter')", install_block)
        self.assertIn("this.modeInstance = args[0]", install_block)
        self.assertIn("ensureTerminatorUpgradeBoxGeneratorsStarted(this.modeInstance, 'StartGenerateSupplyBox.leave')", install_block)
        self.assertIn("upgradeBoxGeneratorFallbackCount", script_text)
        self.assertIn("upgradeBoxGeneratorNativeCount", script_text)
        self.assertNotIn("Runtime.generateUpgradeBox", script_text)
        self.assertNotIn("UnityEngine_Object_Instantiate", script_text)

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

    def test_game_mode_override_keeps_nano_from_deathmatch_populated_without_lifecycle_hooks(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        install_block = script_text.split("function installHooks()", 1)[1].split("function statusObject()", 1)[0]

        self.assertIn("deferModeApplyUntilBotGeneration", script_text)
        self.assertIn("function shouldDeferNanoModeApplyUntilBotGeneration(selected)", script_text)
        self.assertIn("function applyDeferredModeAfterBotGeneration(reason)", script_text)
        self.assertIn("function nanoRulesAreActiveForCurrentStart()", script_text)
        self.assertIn("function normalizeRoomBotTeamsForNanoRules(reason)", script_text)
        self.assertIn("function ensureNanoRuleSpawnFallbacks(reason)", script_text)
        defer_block = script_text.split("function shouldDeferNanoModeApplyUntilBotGeneration(selected)", 1)[1].split("function nanoRulesAreActiveForCurrentStart()", 1)[0]
        self.assertIn("Runtime.lastSourceMapMode === 1", defer_block)
        self.assertIn("selected.gameMode >= 4 && selected.gameMode <= 6", defer_block)
        helper_block = script_text.split("function nanoRulesAreActiveForCurrentStart()", 1)[1].split("function findTargetMapAsset", 1)[0]
        self.assertIn("Runtime.lastApplied.sourceMapMode === 1", helper_block)
        self.assertIn("Runtime.lastApplied.gameMode >= 4 && Runtime.lastApplied.gameMode <= 6", helper_block)
        self.assertIn("readU8(clientData.add(OFF.ClientData_isBot))", helper_block)
        self.assertIn("var desiredTeam = nextTeam", helper_block)
        self.assertIn("clientData.add(OFF.ClientData_joinTeam).writeS32(desiredTeam)", helper_block)
        self.assertIn("ensureTeamSpawnFallbackFromNeutral(0, reason)", helper_block)
        self.assertIn("ensureTeamSpawnFallbackFromNeutral(1, reason)", helper_block)
        self.assertNotIn("clientData.add(OFF.ClientData_joinTeam).writeS32(2)", helper_block)
        self.assertIn("markDeferredModeApply('ApplyGameSetting.leave')", install_block)
        self.assertIn("applyDeferredModeAfterBotGeneration('GenerateBotClient.leave')", install_block)
        self.assertIn("applyDeferredModeAfterBotGeneration('GameManager.AddPlayers.enter')", install_block)
        start_leave_block = install_block.split("onLeave: function () {", 1)[1].split("Runtime.startDepth = Math.max", 1)[0]
        self.assertNotIn("applyDeferredModeAfterBotGeneration", start_leave_block)
        self.assertLess(
            install_block.index("markDeferredModeApply('ApplyGameSetting.leave')"),
            install_block.index("applyDeferredModeAfterBotGeneration('GenerateBotClient.leave')"),
        )
        self.assertLess(
            install_block.index("applyDeferredModeAfterBotGeneration('GenerateBotClient.leave')"),
            install_block.index("normalizeRoomBotTeamsForNanoRules('GenerateBotClient.leave')"),
        )
        self.assertIn("normalizeRoomBotTeamsForNanoRules('ApplyGameSetting.leave')", install_block)
        self.assertIn("normalizeRoomBotTeamsForNanoRules('GenerateBotClient.leave')", install_block)
        self.assertIn("normalizeRoomBotTeamsForNanoRules('GameManager.AddPlayers.enter')", install_block)
        self.assertIn("ensureNanoRuleSpawnFallbacks('GameManager.AddPlayers.enter')", install_block)
        self.assertIn("ensureNanoRuleSpawnFallbacks('MapManager.Awake')", install_block)
        self.assertNotIn("ModeBase_Nano_DeathEvent", install_block)

    def test_game_mode_override_team_rules_from_bio_maps_use_fixed_12_minute_time_limit_only(self):
        script_text = (FEATURES / "27_game_mode_override" / "script.js").read_text(encoding="utf-8")
        team_rule_block = script_text.split("function buildTeamRule(dropdownsPtr)", 1)[1].split("function applySelectedModeRules", 1)[0]

        self.assertIn("function shouldUseFixedTeamTimeLimit()", script_text)
        fixed_rule_block = script_text.split("function shouldUseFixedTeamTimeLimit()", 1)[1].split("function buildTeamRule", 1)[0]
        self.assertIn("Runtime.modeKey === 'team_death'", fixed_rule_block)
        self.assertIn("Runtime.lastApplied.forceTeamRules", fixed_rule_block)
        self.assertIn("isNanoGameModeValue(Runtime.lastApplied.sourceMapMode)", fixed_rule_block)
        self.assertIn("if (shouldUseFixedTeamTimeLimit())", team_rule_block)
        self.assertIn("fixed.teamDeathFromNanoTimeLimit", team_rule_block)
        self.assertIn("targetScore: 0", team_rule_block)
        self.assertIn("readDropdownValue(dropdownsPtr, 0, 0)", team_rule_block)
        self.assertIn("readIntArrayElement(killArray", team_rule_block)
        self.assertIn("static.killConditionTime", team_rule_block)

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
