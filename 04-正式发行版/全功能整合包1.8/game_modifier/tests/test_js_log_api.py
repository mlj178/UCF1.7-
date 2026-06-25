import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class JsLogApiTests(unittest.TestCase):
    def test_common_script_defines_audience_log_helpers(self):
        common_js = (PROJECT_ROOT / "scripts" / "_common.js").read_text(encoding="utf-8")

        self.assertIn("function sendUserLog", common_js)
        self.assertIn("function sendDevLog", common_js)
        self.assertIn("function sendBothLog", common_js)
        self.assertIn("sendRoutedLog(level, module, message, 'user'", common_js)
        self.assertIn("sendRoutedLog(level, module, message, 'dev'", common_js)
        self.assertIn("sendRoutedLog(level, module, message, 'both'", common_js)

    def test_round_skip_uses_dev_log_for_hook_details(self):
        round_skip_js = (PROJECT_ROOT / "scripts" / "10-skip_round.js").read_text(encoding="utf-8")

        self.assertIn("sendDevLog", round_skip_js)
        self.assertIn("sendUserLog", round_skip_js)
        self.assertNotIn("addLog('info', '新回合", round_skip_js)


if __name__ == "__main__":
    unittest.main()
