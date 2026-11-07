import unittest
from pathlib import Path


UI_DIR = Path(__file__).resolve().parent
DIALOG = UI_DIR / "disclaimer_dialog.py"


class DisclaimerReadGateStaticTests(unittest.TestCase):
    """首次启动声明弹窗必须强制阅读若干秒后才能点「我已知晓并继续」。"""

    def setUp(self):
        self.text = DIALOG.read_text(encoding="utf-8")

    def test_read_countdown_is_five_seconds(self):
        self.assertIn("READ_SECONDS = 5", self.text)

    def test_accept_button_starts_disabled(self):
        accept_block = self.text[self.text.index("self._accept_button = ctk.CTkButton("):]
        accept_block = accept_block[:accept_block.index("pack(side=")]
        self.assertIn('state="disabled"', accept_block)

    def test_countdown_starts_with_dialog_and_updates_text(self):
        self.assertIn("self._start_countdown()", self.text)
        self.assertIn("self.after(1000, self._tick_countdown)", self.text)
        self.assertIn('f"请阅读（{self._remaining_seconds} 秒）"', self.text)

    def test_accept_is_blocked_until_countdown_finishes(self):
        accept_block = self.text[self.text.index("def _on_accept(self):"):]
        accept_block = accept_block[:accept_block.index("def _on_decline")]
        self.assertIn("if self._remaining_seconds > 0:", accept_block)
        self.assertLess(
            accept_block.index("if self._remaining_seconds > 0:"),
            accept_block.index("mark_acknowledged()"),
        )

    def test_countdown_timer_is_cancelled_on_destroy(self):
        self.assertIn("def _cancel_countdown(self):", self.text)
        destroy_block = self.text[self.text.index("def destroy(self):"):]
        destroy_block = destroy_block[:destroy_block.index("def _on_accept")]
        self.assertIn("self._cancel_countdown()", destroy_block)
        self.assertIn("after_cancel", self.text)


if __name__ == "__main__":
    unittest.main()
