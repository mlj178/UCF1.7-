import unittest
from pathlib import Path


UI_DIR = Path(__file__).resolve().parent
WINDOW_CONTRACT = UI_DIR / "window_contract.py"
SETTINGS_WINDOW = UI_DIR / "settings_window.py"
INSTALLER_SCRIPT = UI_DIR.parent / "packaging" / "installer.iss"
FRIDA_MANAGER = UI_DIR.parent / "core" / "frida_manager.py"


class VersionMetadataStaticTests(unittest.TestCase):
    def test_application_version_is_2_6(self):
        self.assertIn('APP_VERSION = "v2.6"', WINDOW_CONTRACT.read_text(encoding="utf-8"))

    def test_about_page_shows_contributor_immediately_after_author(self):
        text = SETTINGS_WINDOW.read_text(encoding="utf-8")
        self.assertIn('text="代码贡献者：少年与狗子"', text)
        author_index = text.index('text="作者: 挂呱呱呱"')
        contributor_index = text.index('text="代码贡献者：少年与狗子"')
        date_index = text.index('text="2026年09月09日"')

        self.assertLess(author_index, contributor_index)
        self.assertLess(contributor_index, date_index)

    def test_installer_default_version_is_2_6(self):
        text = INSTALLER_SCRIPT.read_text(encoding="utf-8")
        self.assertIn('#define AppVersion "2.6"', text)
        self.assertIn('版本号默认取 2.6', text)

    def test_runtime_ready_message_reports_2_6(self):
        self.assertIn(
            'message="全功能整合包插件运行时 v2.6 已就绪"',
            FRIDA_MANAGER.read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
