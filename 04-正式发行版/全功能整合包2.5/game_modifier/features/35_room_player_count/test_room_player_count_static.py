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


if __name__ == "__main__":
    unittest.main()
