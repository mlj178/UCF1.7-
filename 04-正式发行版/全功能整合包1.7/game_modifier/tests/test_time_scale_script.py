import os
import sys
import unittest


GAME_MODIFIER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if GAME_MODIFIER_DIR not in sys.path:
    sys.path.insert(0, GAME_MODIFIER_DIR)


class TimeScaleScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        script_path = os.path.join(
            GAME_MODIFIER_DIR,
            "scripts",
            "time_scale.js",
        )
        with open(script_path, "r", encoding="utf-8") as script:
            cls.source = script.read()

    def test_retries_transient_initialization_failures(self):
        self.assertIn("function resetInitCache()", self.source)
        self.assertIn("_initError = null", self.source)

    def test_validates_memory_page_before_writing_time_scale(self):
        self.assertIn("Process.findRangeByAddress", self.source)
        self.assertIn("range.protection.indexOf('w')", self.source)
        self.assertIn("function isPlausibleTimeScale", self.source)

    def test_reapplies_speed_after_time_manager_rebuilds(self):
        self.assertIn("function startApplyTimer()", self.source)
        self.assertIn("safeWriteTimeScale(currentSpeed)", self.source)
        self.assertIn("function stopApplyTimer()", self.source)


if __name__ == "__main__":
    unittest.main()
