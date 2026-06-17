import unittest
from pathlib import Path


class Nano4TExitResetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app_path = Path(__file__).parents[1] / "ui" / "app.py"
        cls.source = app_path.read_text(encoding="utf-8")
        script_path = Path(__file__).parents[1] / "scripts" / "nano4t.js"
        cls.script_source = script_path.read_text(encoding="utf-8")

    def test_destroy_and_healthcheck_exit_share_one_reset_path(self):
        event_block = self.source[
            self.source.index("def _on_nano4t_event("):
            self.source.index("def _log(", self.source.index("def _on_nano4t_event("))
        ]
        self.assertGreaterEqual(
            event_block.count("self._handle_nano4t_mode_exit()"),
            2,
        )

    def test_exit_reset_clears_mode_and_battle_round_ui(self):
        reset_block = self.source[
            self.source.index("def _handle_nano4t_mode_exit("):
            self.source.index("def _nano4t_update_round_label(")
        ]
        self.assertIn("self._nano4t_activated = False", reset_block)
        self.assertIn("self._battle_round_active = False", reset_block)
        self.assertIn("self._frida.send_toggle('battle_round_always', False)", reset_block)
        self.assertIn('self.nano4t_next_label.configure(text="")', reset_block)
        self.assertIn('text="[未激活]"', reset_block)
        self.assertIn("状态: ⚪ 等待进入多人生化模式...", reset_block)

    def test_native_requests_are_dispatched_from_modebase_update(self):
        self.assertIn("function processPendingRequests()", self.script_source)
        self.assertIn("ModeBase_Update", self.script_source)
        self.assertIn("processPendingRequests();", self.script_source)
        self.assertIn("_pendingRequests.init = true", self.script_source)
        self.assertIn("_pendingRequests.health = true", self.script_source)
        self.assertIn("_pendingRequests.current = true", self.script_source)

    def test_background_polling_semantics_are_preserved(self):
        health_block = self.source[
            self.source.index("def _nano4t_auto_health_bg("):
            self.source.index("def _nano4t_auto_getcurrent_bg(")
        ]
        self.assertIn("time.sleep(2)", health_block)
        self.assertIn("self._frida.call_export('nano4thealthcheck')", health_block)
        self.assertIn("self._frida.call_export('nano4tinit')", health_block)


if __name__ == "__main__":
    unittest.main()
