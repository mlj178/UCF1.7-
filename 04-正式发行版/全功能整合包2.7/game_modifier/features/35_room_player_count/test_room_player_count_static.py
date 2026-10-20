import json
import unittest
from pathlib import Path


FEATURE_DIR = Path(__file__).resolve().parent
RUNTIME_JS = FEATURE_DIR / "script.js"
FORMAL_JS = (
    FEATURE_DIR.parents[4]
    / "05-正式功能"
    / "35-全模式房间人数"
    / "AAAAA-room_player_count_min.js"
)


class RoomPlayerCountStaticTests(unittest.TestCase):
    def test_manifest_marks_room_count_as_visible_in_ui(self):
        manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))

        self.assertTrue(manifest["ui"]["visible"])

    def test_plugin_page_skips_features_explicitly_hidden_from_ui(self):
        page = FEATURE_DIR.parents[1] / "ui" / "pages" / "plugin_feature_page.py"
        text = page.read_text(encoding="utf-8")

        self.assertIn('if manifest.get("ui", {}).get("visible", True) is False:', text)

    def test_help_text_is_short_and_wraps_inside_the_card(self):
        manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))
        panel = (FEATURE_DIR / "panel.py").read_text(encoding="utf-8")
        expected = "开启后，设置人数并点击“应用人数”。下一局生效；关闭后恢复默认人数。"

        self.assertEqual(expected, manifest["desc"])
        self.assertNotIn("功能说明：", manifest["desc"])
        self.assertIn("wraplength=250", panel)
        self.assertIn(expected, panel)

    def test_manifest_places_room_count_in_the_right_column_across_two_rows(self):
        manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))

        self.assertEqual(2, manifest["layout"]["rowspan"])
        self.assertEqual(85, manifest["order"])

    def test_panel_places_slider_on_its_own_row_with_user_facing_help(self):
        text = (FEATURE_DIR / "panel.py").read_text(encoding="utf-8")

        self.assertIn('slider_row = ctk.CTkFrame(frame, fg_color="transparent")', text)
        self.assertIn('slider_row.pack(fill="x", padx=10, pady=(2, 4))', text)
        self.assertIn("开启后，设置人数并点击“应用人数”。", text)
        self.assertIn("关闭后恢复默认人数。", text)

    def test_panel_exposes_a_switch_and_requires_it_before_apply(self):
        text = (FEATURE_DIR / "panel.py").read_text(encoding="utf-8")

        self.assertIn("ctk.CTkSwitch", text)
        self.assertIn('callbacks["toggle"](self.feature_id)', text)
        self.assertIn('if not self.callbacks["is_enabled"](self.feature_id):', text)
        self.assertIn("请先开启功能", text)

    def test_manifest_disables_startup_restore(self):
        manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))

        self.assertFalse(manifest["lifecycle"]["restore"])

    def test_runtime_enable_only_arms_and_apply_requires_enabled(self):
        text = RUNTIME_JS.read_text(encoding="utf-8")
        enable_body = text.split("function enable(config)", 1)[1].split(
            "function installPatch(requested)", 1
        )[0]
        apply_body = text.split("function applyConfig(config)", 1)[1].split(
            "function disable()", 1
        )[0]

        self.assertNotIn("writeState(", enable_body)
        self.assertIn("enabled = true", enable_body)
        self.assertIn("if (!enabled)", apply_body)
        self.assertIn("feature_disabled", apply_body)

    def test_known_30_player_baseline_has_a_complete_reversible_v3_profile(self):
        required_rvas = [
            "0x12AF7F", "0x154FBA", "0x2BF6F8", "0x3D18E2", "0x5C0E4B",
            "0x72BE79", "0x9DA472", "0xAF9C69", "0xAFAD8D", "0xAFD066",
            "0xB25C56", "0xB25D3F", "0xB30F3C", "0xB43D76", "0xB44895",
            "0xB67F07", "0xB74657",
        ]

        for path in (RUNTIME_JS, FORMAL_JS):
            text = path.read_text(encoding="utf-8")
            self.assertIn("BASE_30_TO_V3_PROFILE", text, path.name)
            self.assertIn("function applyBaselineProfile()", text, path.name)
            self.assertIn("function restoreBaselineProfile()", text, path.name)
            self.assertIn("baseline_30_auto_patched", text, path.name)
            self.assertIn("profilePatchedByThisScript", text, path.name)
            for rva in required_rvas:
                self.assertIn(rva, text, f"{path.name} missing {rva}")

    def test_nano_ghost_count_falls_back_to_the_last_authored_slot(self):
        text = RUNTIME_JS.read_text(encoding="utf-8")

        self.assertIn("NANO_GHOST_TAIL_RVA = 0xAF04FB", text)
        self.assertIn("NANO_GHOST_TAIL_BASE_HEX = '6a 00 e8 fe 74 67 ff 50 e8 28 78 67 ff'", text)
        self.assertIn("NANO_GHOST_TAIL_FIXED_HEX = '8b 51 0c 4a 8b 44 91 10 5d c3 90 90 90'", text)
        self.assertIn("NANO_GHOST_INDEX_LEGACY_HEX = '3c 1d 76 02 b0 1d'", text)

        install = text.split("function installPatch(requested)", 1)[1].split(
            "function applyConfig(config)", 1
        )[0]
        self.assertIn("applyNanoGhostTailFallback()", install)
        self.assertIn("restoreNanoGhostTail()", install)
        self.assertIn("restoreNanoGhostTail()", text.split("function disable()", 1)[1])

    def test_profile_writes_are_validated_before_write_and_restored_on_cleanup(self):
        text = RUNTIME_JS.read_text(encoding="utf-8")

        self.assertIn("profileState()", text)
        self.assertIn("writeProfileBytes('v3')", text)
        self.assertIn("writeProfileBytes('base')", text)
        self.assertIn("if (state !== 'base')", text)
        self.assertIn("if (state === 'v3')", text)
        self.assertIn("restoreBaselineProfile()", text.split("function disable()", 1)[1])

        apply_profile = text.split("function applyBaselineProfile()", 1)[1].split("function restoreBaselineProfile()", 1)[0]
        self.assertIn("writeProfileBytes('v3')", apply_profile)
        self.assertIn("writeProfileBytes('base')", apply_profile)


    def test_v3_profile_does_not_patch_the_local_player_supply_box_branch(self):
        # hotfix7: the old v3 profile's 0xB44895 -> 0x2BF6F8 -> 0x1553BA cave
        # ran on every local-player supply-box pickup and ended in a DEP crash
        # (call this). It must never come back into the write profile.
        for path in (RUNTIME_JS, FORMAL_JS):
            text = path.read_text(encoding="utf-8")
            profile = text.split("var BASE_30_TO_V3_PROFILE = [", 1)[1].split("];", 1)[0]
            for rva in ("0xB44895", "0x2BF6F8", "0x154FBA", "0x5C0E4B"):
                self.assertNotIn(rva, profile, f"{path.name} writes {rva}")
            self.assertIn("function clearLegacySupplyBoxCheat()", text, path.name)

        runtime = RUNTIME_JS.read_text(encoding="utf-8")
        apply_body = runtime.split("function applyBaselineProfile()", 1)[1].split(
            "function restoreBaselineProfile()", 1
        )[0]
        self.assertIn("clearLegacySupplyBoxCheat();", apply_body)
        disable_body = runtime.split("function disable()", 1)[1]
        self.assertIn("clearLegacySupplyBoxCheat();", disable_body)

    def test_v3_profile_does_not_install_unrelated_cheat_payloads(self):
        # hotfix8: 0x12AF7F / 0x3D18E2 / 0x72BE79 / 0x9DA472 were weapon /
        # jump / RPG cheat caves carried over from the 100-player cheat build.
        # Neither build branches into them, so they only shipped dead bytes;
        # the room-count profile must not write them at all.
        dead_rvas = ("0x12AF7F", "0x3D18E2", "0x72BE79", "0x9DA472")
        for path in (RUNTIME_JS, FORMAL_JS):
            text = path.read_text(encoding="utf-8")
            profile = text.split("var BASE_30_TO_V3_PROFILE = [", 1)[1].split("];", 1)[0]
            legacy = text.split("var LEGACY_CHEAT_CAVES = [", 1)[1].split("];", 1)[0]
            self.assertIn("function clearLegacyCheatCaves()", text, path.name)
            for rva in dead_rvas:
                self.assertNotIn(rva, profile, f"{path.name} writes {rva}")
                self.assertIn(rva, legacy, f"{path.name} cannot restore {rva}")

        runtime = RUNTIME_JS.read_text(encoding="utf-8")
        apply_body = runtime.split("function applyBaselineProfile()", 1)[1].split(
            "function restoreBaselineProfile()", 1
        )[0]
        self.assertIn("clearLegacyCheatCaves();", apply_body)
        self.assertIn("clearLegacyCheatCaves();", runtime.split("function disable()", 1)[1])

    def test_profile_writer_uses_the_matching_base_or_v3_column(self):
        # 2.7 shipped writeEntry[1 + index], so writing v3 read column 3
        # (undefined) and the recovery path wrote v3 bytes while reporting a
        # base-write failure. Keep the column index exact.
        text = RUNTIME_JS.read_text(encoding="utf-8")
        self.assertIn("writeByteArray(hexBytes(writeEntry[index]))", text)
        self.assertNotIn("writeEntry[1 + index]", text)

if __name__ == "__main__":
    unittest.main()
