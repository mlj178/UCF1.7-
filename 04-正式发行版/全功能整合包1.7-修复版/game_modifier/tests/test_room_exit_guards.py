import unittest
from pathlib import Path


class RoomExitGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scripts = Path(__file__).parents[1] / "scripts"
        cls.gravity = (scripts / "gravity.js").read_text(encoding="utf-8")
        cls.godmode = (scripts / "godmode.js").read_text(encoding="utf-8")

    def test_gravity_stops_native_access_during_room_shutdown(self):
        self.assertIn("var roomShuttingDown = true", self.gravity)
        self.assertIn("function beginRoomShutdown()", self.gravity)
        self.assertIn("if (roomShuttingDown) return;", self.gravity)
        self.assertIn("base.add(0xAF6A00)", self.gravity)
        self.assertIn("base.add(0xAEE850)", self.gravity)
        self.assertIn("base.add(0xAFB6F0)", self.gravity)
        self.assertIn("roomShuttingDown = false", self.gravity)

    def test_godmode_clears_cached_player_during_room_shutdown(self):
        self.assertIn("var roomShuttingDown = true", self.godmode)
        self.assertIn("function beginRoomShutdown()", self.godmode)
        self.assertIn("cachedMyPlayer = null", self.godmode)
        self.assertIn("base.add(0xAF6A00)", self.godmode)
        self.assertIn("base.add(0xAEE850)", self.godmode)
        self.assertIn("base.add(0xAFB6F0)", self.godmode)
        self.assertIn("roomShuttingDown = false", self.godmode)


if __name__ == "__main__":
    unittest.main()
