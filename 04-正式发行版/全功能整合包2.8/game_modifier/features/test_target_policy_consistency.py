"""跨功能契约：自瞄与开火直伤必须使用同一套目标策略。

两边是独立的 Frida 脚本（没有共享 JS 模块），所以用这个测试把
“外锥 / 内锥 / 角度优先 / 距离 tiebreak / 粘滞 margin”钉成同一组数字。
确认帧允许不同：自瞄是连续扫描（2），枪械是开火事件驱动（1）。
"""

import json
import re
import unittest
from pathlib import Path


FEATURES_DIR = Path(__file__).resolve().parent
AIM_SCRIPT = FEATURES_DIR / "11_aim" / "script.js"
AIM_MANIFEST = FEATURES_DIR / "11_aim" / "manifest.json"
DD_SCRIPT = FEATURES_DIR / "40_direct_damage" / "script.js"
DD_MANIFEST = FEATURES_DIR / "40_direct_damage" / "manifest.json"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def number(pattern: str, text: str) -> float:
    match = re.search(pattern, text)
    if not match:
        raise AssertionError("pattern not found: %s" % pattern)
    return float(match.group(1))


class TargetPolicyConsistencyTests(unittest.TestCase):
    def test_shared_cone_and_ranking_numbers_match(self):
        aim = read(AIM_SCRIPT)
        dd = read(DD_SCRIPT)

        pairs = (
            (r"outerConeDeg:\s*([0-9.]+)", r"target_outer_cone_deg:\s*([0-9.]+)"),
            (r"innerConeDeg:\s*([0-9.]+)", r"target_inner_cone_deg:\s*([0-9.]+)"),
            (r"angleTieDeg:\s*([0-9.]+)", r"target_angle_tie_deg:\s*([0-9.]+)"),
            (r"switchMarginDeg:\s*([0-9.]+)", r"target_switch_margin_deg:\s*([0-9.]+)"),
            (r"switchCooldownMs:\s*([0-9.]+)", r"target_switch_cooldown_ms:\s*([0-9.]+)"),
        )
        for aim_pattern, dd_pattern in pairs:
            self.assertEqual(
                number(aim_pattern, aim),
                number(dd_pattern, dd),
                "自瞄与直伤的共享目标策略参数不一致：%s / %s" % (aim_pattern, dd_pattern),
            )

    def test_confirm_scans_differ_only_by_update_cadence(self):
        aim = number(r"switchConfirmScans:\s*([0-9.]+)", read(AIM_SCRIPT))
        dd = number(r"target_switch_confirm_scans:\s*([0-9.]+)", read(DD_SCRIPT))
        self.assertEqual(aim, 2.0, "连续扫描的自瞄需要两帧确认")
        self.assertEqual(dd, 1.0, "开火事件驱动的枪械每次开火只判断一次")

    def test_manifests_expose_the_same_defaults(self):
        aim_manifest = json.loads(read(AIM_MANIFEST))["config"]
        dd_manifest = json.loads(read(DD_MANIFEST))["config"]
        self.assertEqual(aim_manifest["outerConeDeg"], dd_manifest["target_outer_cone_deg"])
        self.assertEqual(aim_manifest["innerConeDeg"], dd_manifest["target_inner_cone_deg"])
        self.assertEqual(aim_manifest["angleTieDeg"], dd_manifest["target_angle_tie_deg"])
        self.assertEqual(aim_manifest["switchMarginDeg"], dd_manifest["target_switch_margin_deg"])

    def test_both_scripts_implement_inner_cone_then_angle_then_distance(self):
        for path in (AIM_SCRIPT, DD_SCRIPT):
            text = read(path)
            for token in (
                "function pickBestCandidate(",
                "function candidateIsBetter(",
                "bestInner",
                "innerLimit",
                "aAngle + tie < bAngle",
                "return a.dist < b.dist",
            ):
                self.assertIn(token, text, "%s 缺少统一排序实现：%s" % (path.name, token))

    def test_old_distance_band_and_mode_table_are_gone(self):
        aim = read(AIM_SCRIPT)
        dd = read(DD_SCRIPT)
        for retired in ("nearestDistanceBand", "targetSwitchAngleAdvantageDeg", "chooseTargetCandidateWithHysteresis"):
            self.assertNotIn(retired, aim, "自瞄仍残留旧策略：%s" % retired)
        for retired in ("TARGET_MODE", "target_mode", "max_angle_deg", "homing_cone_deg", "homing_cone_fallback"):
            self.assertNotIn(retired, dd, "直伤仍残留旧策略：%s" % retired)


if __name__ == "__main__":
    unittest.main()
