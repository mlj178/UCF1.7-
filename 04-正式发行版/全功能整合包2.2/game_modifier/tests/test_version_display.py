import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class VersionDisplayTest(unittest.TestCase):
    SOURCE_CODE_URL = "https://github.com/mlj178/UCF1.7-/tree/dev/04-%E6%AD%A3%E5%BC%8F%E5%8F%91%E8%A1%8C%E7%89%88"

    def test_app_window_contract_uses_current_package_version(self):
        namespace = {}
        exec((ROOT / "ui" / "window_contract.py").read_text(encoding="utf-8"), namespace)
        self.assertEqual(namespace["APP_VERSION"], "v2.2")
        self.assertEqual(namespace["APP_DISPLAY_NAME"], "全功能整合包 v2.2")
        self.assertEqual(namespace["APP_TITLE"], "全功能整合包 v2.2")
        self.assertEqual(namespace["STARTUP_LOG_TITLE"], "全功能整合包 v2.2")

    def test_user_visible_runtime_version_is_not_stale_2_0(self):
        checked_files = [
            ROOT / "ui" / "window_contract.py",
            ROOT / "core" / "frida_manager.py",
        ]
        for path in checked_files:
            with self.subTest(path=path.relative_to(ROOT)):
                text = path.read_text(encoding="utf-8")
                self.assertIn("v2.2", text)
                self.assertNotIn("v2.0", text)

    def test_settings_about_link_points_to_source_code(self):
        text = (ROOT / "ui" / "settings_window.py").read_text(encoding="utf-8")
        self.assertIn("全功能整合包源代码", text)
        self.assertIn(self.SOURCE_CODE_URL, text)
        self.assertNotIn("历代版本更新说明", text)
        self.assertNotIn("https://mlj178.github.io/UCF1.7.1--/", text)


if __name__ == "__main__":
    unittest.main()
