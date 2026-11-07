import unittest
from pathlib import Path


GAME_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = GAME_ROOT / "core" / "config.py"
SPEC_FILE = GAME_ROOT / "game_modifier_onedir.spec"


class SharedResourceDirectoryStaticTests(unittest.TestCase):
    """2.8 起资源由各版本共享：来源统一为 04-正式发行版/00-资源。"""

    def test_config_prefers_shared_resource_directory(self):
        text = CONFIG_FILE.read_text(encoding="utf-8")

        self.assertIn('_shared_resource_dir = os.path.join(_release_root, "00-资源")', text)
        self.assertIn(
            "RESOURCE_DIR = _shared_resource_dir if os.path.isdir(_shared_resource_dir) else _legacy_resource_dir",
            text,
        )

    def test_spec_reads_resources_from_release_root(self):
        text = SPEC_FILE.read_text(encoding="utf-8")

        self.assertIn('release_root_dir = os.path.dirname(os.path.dirname(current_dir))', text)
        self.assertIn('shared_resource_dir = os.path.join(release_root_dir, "00-资源")', text)
        self.assertIn(
            "resource_dir = shared_resource_dir if os.path.isdir(shared_resource_dir) else legacy_resource_dir",
            text,
        )

    def test_bundled_resource_target_path_is_unchanged(self):
        text = SPEC_FILE.read_text(encoding="utf-8")

        # 打包产物内部仍落在 _internal/资源，运行时 frozen 分支无需改动
        self.assertIn('datas.append((resource_path, "资源"))', text)
        self.assertIn('add_data_tree(red_source, os.path.join("资源", red_subdir))', text)


if __name__ == "__main__":
    unittest.main()
