import json
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).resolve().parent
SCRIPT = FEATURE_DIR / "script.js"
PANEL = FEATURE_DIR / "panel.py"
MANIFEST = FEATURE_DIR / "manifest.json"


class NanoClothTargetStaticTests(unittest.TestCase):
    """契约测试：37 增加防化服的应用对象下拉框与"全体人类"实现。"""

    def setUp(self):
        self.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.script = SCRIPT.read_text(encoding="utf-8")
        self.panel = PANEL.read_text(encoding="utf-8")

    # ---- manifest ----

    def test_manifest_declares_target_combo(self):
        combos = [
            control
            for control in self.manifest["controls"]
            if control.get("type") == "combo" and control.get("key") == "cloth_target"
        ]
        self.assertEqual(len(combos), 1)
        combo = combos[0]
        self.assertEqual(combo["values"], ["local_player", "all_humans"])
        self.assertEqual(combo["default"], "local_player")
        self.assertEqual(combo["display_values"]["local_player"], "仅本地玩家")
        self.assertEqual(combo["display_values"]["all_humans"], "全体人类")
        self.assertIn(combo["action"], self.manifest["rpc"])

    def test_manifest_stores_target_config_and_handle(self):
        self.assertEqual(self.manifest["config"]["cloth_target"], "local_player")
        self.assertEqual(
            self.manifest["ui_handles"]["cloth_target_var"],
            "nano_cloth_cloth_target_var",
        )

    # ---- panel ----

    def test_panel_builds_target_dropdown(self):
        self.assertIn("CTkComboBox", self.panel)
        self.assertIn("仅本地玩家", self.panel)
        self.assertIn("全体人类", self.panel)
        self.assertIn('"cloth_target"', self.panel)
        self.assertIn('handles.get("cloth_target_var"', self.panel)

    def test_panel_returns_the_handle_name_declared_in_manifest(self):
        handle = self.manifest["ui_handles"]["cloth_target_var"]
        self.assertIn(f'handles.get("cloth_target_var", "{handle}")', self.panel)

    # ---- script ----

    def test_script_supports_both_targets(self):
        self.assertIn("TARGET_LOCAL = 'local_player'", self.script)
        self.assertIn("TARGET_ALL_HUMANS = 'all_humans'", self.script)
        self.assertIn("cloth_target: TARGET_LOCAL", self.script)
        self.assertIn("Runtime.config.cloth_target = normalizeTarget(config.cloth_target)", self.script)

    def test_script_reads_game_manager_all_players(self):
        # 与 34-角色变身 / 08-聚怪 一致：Singleton<GameManager> + allPlayers(+0x1C) Il2CppArray
        self.assertIn("Singleton_GameManager_get_instance: 0x004A8170", self.script)
        self.assertIn("SingletonGameManager_get_instance_Method: 0x00E1CE64", self.script)
        self.assertIn("gmAllPlayers: 0x1C", self.script)
        self.assertIn("arrayLength: 0x0C", self.script)
        self.assertIn("arrayItems: 0x10", self.script)

    def test_script_excludes_nano_ghosts_from_all_humans(self):
        self.assertIn("Player_get_isNanoGhost: 0x00B56050", self.script)
        self.assertIn("!native.isNanoGhost(player, ptr(0))", self.script)

    def test_all_humans_applies_only_on_main_thread_hook(self):
        # 挂起动作只在 Player.Update（主线程）里消费；RPC 线程只置 pending
        self.assertIn("performPending(player, localUpdate)", self.script)
        self.assertIn("native.addNanoClothCount(player, value, ptr(0))", self.script)

    def test_all_humans_branch_does_not_require_local_player(self):
        # all_humans 分支必须早于 localUpdate 门控，否则 remote 玩家的 Update 无法消费挂起动作
        all_branch = self.script.index("if (target === TARGET_ALL_HUMANS) {")
        local_guard = self.script.index("if (!localUpdate) return;")
        self.assertLess(all_branch, local_guard)

    def test_round_boundary_clears_added_cloth(self):
        # 游戏只在“自己发放过防化服”的人类出生时重置为 1；我们额外加的数量没有该标记，
        # 所以必须在回合边界手动清零，否则跨回合越叠越多。
        self.assertIn("Player_SetNanoClothCount: 0x00B533A0", self.script)
        self.assertIn("clientDataHaveNanoCloth: 0x2C", self.script)
        self.assertIn("function clearHumanClothAtRoundBoundary(", self.script)
        self.assertIn("clearHumanClothAtRoundBoundary('game_round_end')", self.script)
        self.assertIn("clearHumanClothAtRoundBoundary('new_game_round_start')", self.script)
        self.assertIn("native.setNanoClothCount(player, 0, ptr(0));", self.script)

    def test_round_clear_keeps_game_granted_cloth(self):
        self.assertIn("function hasNativeNanoCloth(", self.script)
        self.assertIn("if (hasNativeNanoCloth(player)) continue;", self.script)

    def test_round_clear_only_runs_after_the_feature_was_used(self):
        self.assertIn(
            "Runtime.stats.applyCount > 0 || Runtime.stats.allHumansApplyCount > 0",
            self.script,
        )

    def test_no_redundant_local_hud_refresh_remains(self):
        # AddNanoClothCount/SetNanoClothCount 都用 Player.get_isFocusPlayer 门控 SetNanoClothUI，
        # 给队友写数量不会污染本地 HUD，所以不需要额外的 count=0 刷新
        self.assertNotIn("refreshLocalClothHud", self.script)

    def test_status_reports_target_and_cleared_count(self):
        self.assertIn("cloth_target: Runtime.config.cloth_target", self.script)
        self.assertIn("last_apply_target: Runtime.stats.lastApplyTarget", self.script)
        self.assertIn("cleared_humans: Runtime.stats.clearedHumans", self.script)


if __name__ == "__main__":
    unittest.main()
