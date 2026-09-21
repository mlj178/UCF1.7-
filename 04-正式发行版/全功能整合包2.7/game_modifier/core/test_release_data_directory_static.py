import unittest
from pathlib import Path


CONFIG_FILE = Path(__file__).with_name("config.py")


class ReleaseDataDirectoryStaticTests(unittest.TestCase):
    def test_frozen_build_uses_its_own_2_6_data_directory(self):
        text = CONFIG_FILE.read_text(encoding="utf-8")

        self.assertIn('"UCFModifier", "2.6", "data"', text)
        self.assertNotIn('"UCFModifier", "2.5", "data"', text)


if __name__ == "__main__":
    unittest.main()
