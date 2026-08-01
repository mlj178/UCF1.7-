import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "ui" / "app.py"
SHELL_VIEW = ROOT / "ui" / "views" / "shell_view.py"


class ConnectButtonRemovalTests(unittest.TestCase):
    def test_main_window_has_no_manual_connection_entrypoint(self):
        app_text = APP.read_text(encoding="utf-8")
        shell_text = SHELL_VIEW.read_text(encoding="utf-8")

        self.assertNotIn("_build_connect_button", app_text)
        self.assertNotIn("def _connect(self):", app_text)
        self.assertNotIn("self.btn_frame", app_text)
        self.assertNotIn("on_connect", shell_text)
        self.assertNotIn("def build_connect_button", shell_text)
        self.assertNotIn('text="连接游戏"', shell_text)

    def test_main_window_still_starts_automatic_session_manager(self):
        app_text = APP.read_text(encoding="utf-8")

        self.assertIn("GameSessionManager.get_instance().start()", app_text)


if __name__ == "__main__":
    unittest.main()
