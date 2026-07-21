import re
import unittest
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
JS_FILE = BASE_DIR / "AAAAA-game_mode_override_min.js"
UI_FILE = BASE_DIR / "AAAAA-game_mode_override_ui.py"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class GameModeOverrideStaticTests(unittest.TestCase):

    def test_sniper_bot_first_grant_override_is_scoped(self):
        text = read_text(JS_FILE)

        required_tokens = [
            "SNIPER_BOT_FALLBACK_WEAPON_INDEX",
            "2568",
            "function maybeOverrideLimitedBotGrant",
            "fallbackWeaponIndexForSelectedMode",
            "player.clientIsBot !== true",
            "grantSeq !== 1",
            "function resetWeaponGrantForPlayer",
            "resetWeaponGrantForPlayer(args[0])",
            "args[1] = ptr(fallbackWeaponIndex)",
            "botSniperOverrideHits",
        ]

        for token in required_tokens:
            self.assertIn(token, text)

    def test_sniper_override_happens_before_give_weapon_by_bag_returns(self):
        text = read_text(JS_FILE)

        hook = text.split("RVA.GameManager_GiveWeaponByBag", 1)[1]
        hook = hook.split("RVA.GameManager_GiveWeapon", 1)[0]

        self.assertIn("maybeOverrideLimitedBotGrant", hook)
        self.assertIn("this.effectiveWeaponIndex", hook)
        self.assertIn("this.originalWeaponIndex", hook)
        self.assertLess(hook.index("maybeOverrideLimitedBotGrant"), hook.index("probeWeaponGrant"))
        self.assertIn("this.effectiveWeaponIndex", hook.split("probeWeaponGrant", 1)[1])

    def test_respawn_resets_sniper_bot_weapon_grant_sequence(self):
        text = read_text(JS_FILE)

        hook = text.split("RVA.Player_Respawn", 1)[1]
        hook = hook.split("Runtime.hookInstalled", 1)[0]

        self.assertIn("resetWeaponGrantForPlayer(args[0])", hook)
        self.assertLess(hook.index("resetWeaponGrantForPlayer(args[0])"), hook.index("probeLifecycle"))

    def test_sniper_override_catches_later_main_weapon_grants(self):
        text = read_text(JS_FILE)

        helper = text.split("function maybeOverrideLimitedBotGrant", 1)[1]
        helper = helper.split("function rememberWeaponGrant", 1)[0]

        self.assertIn("lookupWeaponDataByIndex(originalWeaponIndex)", helper)
        self.assertIn("originalWeapon.wpnClass", helper)
        self.assertIn("isRelevantWeaponLimitMismatch(expectedClass, originalWeapon.wpnClass)", helper)
        self.assertIn("result.reason = 'not-weapon-limit-mismatch'", helper)
        self.assertLess(helper.index("isRelevantWeaponLimitMismatch(expectedClass, originalWeapon.wpnClass)"), helper.index("args[1] = ptr(fallbackWeaponIndex)"))

    def test_weapon_only_modes_preserve_current_map_rules(self):
        text = read_text(JS_FILE)

        self.assertRegex(text, r"sniper:\s*\{[^}]*weaponOnly:\s*true")
        self.assertRegex(text, r"handgun:\s*\{[^}]*weaponOnly:\s*true")
        self.assertIn("function applyWeaponOnlyMode", text)
        self.assertIn("if (selected.weaponOnly) return applyWeaponOnlyMode(selected)", text)
        self.assertIn("if (selected.weaponOnly && !shouldUseTeamRulesForWeaponOnly(selected))", text)
        self.assertIn("msg: '武器限制模式沿用地图原规则'", text)
        self.assertIn("staticFields.add(OFF.GameManager_weaponLimited).writeS32(selected.weaponLimited)", text)

    def test_special_mode_is_presented_as_knife_battle(self):
        js_text = read_text(JS_FILE)
        ui_text = read_text(UI_FILE)

        self.assertRegex(js_text, r"special:\s*\{[^}]*label:\s*'刀战'[^}]*weaponLimited:\s*1")
        self.assertRegex(js_text, r"special:\s*\{[^}]*weaponOnly:\s*true")
        self.assertNotRegex(js_text, r"special:\s*\{[^}]*useTargetMapWeaponLimited")
        self.assertIn('"刀战": "special"', ui_text)
        self.assertNotIn('"特殊战": "special"', ui_text)

    def test_knife_battle_uses_current_map_rules_and_knife_bot_override(self):
        text = read_text(JS_FILE)

        self.assertIn("if (weaponLimited === 1) return '当前地图规则 + 刀限制';", text)
        self.assertIn("var KNIFE_BOT_FALLBACK_WEAPON_INDEX", text)
        self.assertIn("if (Runtime.modeKey === 'special') return 6;", text)
        self.assertIn("if (Runtime.modeKey === 'special') return KNIFE_BOT_FALLBACK_WEAPON_INDEX;", text)
        self.assertIn("function maybeOverrideLimitedBotGrant", text)
        self.assertIn("var expectedClass = expectedWeaponClassForSelectedMode();", text)
        self.assertIn("args[1] = ptr(fallbackWeaponIndex)", text)
        self.assertIn("this.override = maybeOverrideLimitedBotGrant(args)", text)

    def test_handgun_battle_uses_pistol_bot_override(self):
        text = read_text(JS_FILE)

        self.assertIn("var HANDGUN_BOT_FALLBACK_WEAPON_INDEX = 1168", text)
        self.assertIn("if (Runtime.modeKey === 'handgun') return 5;", text)
        self.assertIn("if (Runtime.modeKey === 'handgun') return HANDGUN_BOT_FALLBACK_WEAPON_INDEX;", text)
        self.assertIn("function maybeOverrideLimitedBotGrant", text)
        self.assertIn("args[1] = ptr(fallbackWeaponIndex)", text)

    def test_probe_logging_is_quiet_by_default(self):
        js_text = read_text(JS_FILE)
        ui_text = read_text(UI_FILE)

        self.assertIn("enabled: false,", js_text.split("probe: {", 1)[1].split("level:", 1)[0])
        self.assertIn('"probe_enabled": False', ui_text)

        helper = js_text.split("function maybeOverrideLimitedBotGrant", 1)[1]
        helper = helper.split("function rememberWeaponGrant", 1)[0]
        self.assertIn("if (Runtime.probe.enabled) {", helper)
        self.assertLess(helper.index("if (Runtime.probe.enabled) {"), helper.index("sendLog("))

    def test_weapon_limited_modes_switch_nano_maps_to_team_score_rules(self):
        text = read_text(JS_FILE)

        self.assertRegex(text, r"special:\s*\{[^}]*teamDeathOnNano:\s*true")
        self.assertRegex(text, r"sniper:\s*\{[^}]*teamDeathOnNano:\s*true")
        self.assertRegex(text, r"handgun:\s*\{[^}]*teamDeathOnNano:\s*true")
        self.assertIn("function shouldTeamDeathWeaponOnlyOverride", text)
        self.assertIn("if (!selected.teamDeathOnNano) return false", text)
        self.assertIn("return beforeMode.ready && isNanoGameModeValue(beforeMode.gameMode)", text)
        self.assertIn("return applyTeamDeathWeaponOnlyMode(selected, beforeMode)", text)
        self.assertIn("findTargetMapAsset(Runtime.gameRoom, MODES.team_death.gameMode)", text)
        self.assertIn("staticFields.add(OFF.GameManager_gameMode).writeS32(MODES.team_death.gameMode)", text)
        self.assertIn("forceTeamRules: true", text)
        self.assertIn("if (selected.weaponOnly && !shouldUseTeamRulesForWeaponOnly(selected))", text)

    def test_weapon_limited_nano_split_uses_source_map_mode_and_current_apply(self):
        text = read_text(JS_FILE)

        self.assertIn("lastSourceMapMode", text)
        self.assertIn("Runtime.lastSourceMapMode = readS32(args[0].add(OFF.MapAsset_gameMode))", text)
        self.assertIn("function shouldUseTeamRulesForWeaponOnly", text)
        self.assertIn("if (Runtime.lastSourceMapMode !== null && Runtime.lastSourceMapMode !== undefined)", text)
        self.assertIn("return isNanoGameModeValue(Runtime.lastSourceMapMode)", text)
        self.assertIn("Runtime.lastApplied.key === Runtime.modeKey", text)
        self.assertIn("if (selected.weaponOnly && !shouldUseTeamRulesForWeaponOnly(selected))", text)

    def test_ui_file_still_loads_min_script(self):
        text = read_text(UI_FILE)

        self.assertIn('JS_FILE = os.path.join(BASE_DIR, "AAAAA-game_mode_override_min.js")', text)
        self.assertIn("self.script.exports_sync.setconfig", text)


if __name__ == "__main__":
    unittest.main()
