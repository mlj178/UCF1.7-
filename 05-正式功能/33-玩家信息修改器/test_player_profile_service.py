import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from player_profile_service import (
    PlayerProfile,
    get_default_player_data_path,
    save_profile,
    update_player_section_text,
)


class PlayerProfileServiceTests(unittest.TestCase):
    def test_default_path_uses_supplied_home_directory(self):
        home = Path(r"C:\Users\Someone")

        path = get_default_player_data_path(home)

        self.assertEqual(
            path,
            home / "AppData" / "LocalLow" / "Alexander_GaGa" / "UnityCrossFire" / "PlayerData.dat",
        )

    def test_insert_player_section_before_inven(self):
        original = "[Inven]\nDefaultBag=4\n"
        profile = PlayerProfile(nickname="内個", level=30, vip_level=2)

        updated = update_player_section_text(original, profile)

        self.assertEqual(
            updated,
            "[Player]\nNickName=内個\nLevel=30\nVipLevel=2\n\n[Inven]\nDefaultBag=4\n",
        )

    def test_update_existing_player_section_without_touching_inven(self):
        original = (
            "[Player]\n"
            "NickName=old\n"
            "Level=1\n"
            "VipLevel=0\n"
            "\n"
            "[Inven]\n"
            "DefaultBag=4\n"
            "Bag1=915,1761\n"
        )
        profile = PlayerProfile(nickname="新名字", level=50, vip_level=9)

        updated = update_player_section_text(original, profile)

        self.assertEqual(updated.count("[Player]"), 1)
        self.assertIn("NickName=新名字\n", updated)
        self.assertIn("Level=50\n", updated)
        self.assertIn("VipLevel=9\n", updated)
        self.assertIn("[Inven]\nDefaultBag=4\nBag1=915,1761\n", updated)

    def test_save_profile_writes_backup_before_change(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "PlayerData.dat"
            path.write_text("[Inven]\nDefaultBag=4\n", encoding="utf-8")

            result = save_profile(path, PlayerProfile(nickname="内個", level=30, vip_level=2))

            self.assertTrue(result.backup_path.exists())
            self.assertEqual(result.backup_path.read_text(encoding="utf-8"), "[Inven]\nDefaultBag=4\n")
            self.assertIn("[Player]\nNickName=内個\nLevel=30\nVipLevel=2\n", path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
