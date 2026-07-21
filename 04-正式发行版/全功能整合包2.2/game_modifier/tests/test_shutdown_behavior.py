import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ShutdownBehaviorTest(unittest.TestCase):
    def test_main_window_close_does_not_wait_for_live_game_session_shutdown(self):
        app_text = (ROOT / "ui" / "app.py").read_text(encoding="utf-8")
        close_block = app_text.split("def _on_close(self):", 1)[1].split("\n    def ", 1)[0]

        self.assertIn("GameSessionManager.get_instance().stop_async()", close_block)
        self.assertLess(close_block.index("stop_async()"), close_block.index("self.destroy()"))
        self.assertNotIn("feature.cleanup(\"app_close\")", close_block)

    def test_session_manager_async_stop_prevents_atexit_from_blocking_again(self):
        manager_text = (ROOT / "core" / "game_session_manager.py").read_text(encoding="utf-8")

        self.assertIn("def stop_async(self):", manager_text)
        self.assertIn("target=self._stop_impl", manager_text)
        self.assertIn("daemon=True", manager_text)
        self.assertIn("def _begin_stop(self):", manager_text)
        self.assertIn("if not self._begin_stop():", manager_text)


if __name__ == "__main__":
    unittest.main()
