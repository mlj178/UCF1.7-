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

    def test_applies_speed_only_from_game_main_thread(self):
        self.assertNotIn("setInterval(", self.source)
        self.assertIn("function installMainThreadHook()", self.source)
        self.assertIn("base.add(0xAF6A00)", self.source)
        self.assertIn("function processPendingTimeScaleWrite(", self.source)

    def test_invalidates_cached_pointers_during_room_teardown(self):
        self.assertIn("base.add(0xAEE850)", self.source)
        self.assertIn("base.add(0xAFB6F0)", self.source)
        self.assertIn("function beginRoomShutdown(", self.source)
        self.assertIn("_roomShuttingDown = true", self.source)


if __name__ == "__main__":
    unittest.main()
