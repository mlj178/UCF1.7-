import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parent / "script.js"


class GravityStaticTests(unittest.TestCase):
    def test_player_list_guard_accepts_the_100_player_room_profile(self):
        text = SCRIPT.read_text(encoding="utf-8")

        self.assertNotIn("total > 64", text)
        self.assertIn("total > 100", text)


if __name__ == "__main__":
    unittest.main()
