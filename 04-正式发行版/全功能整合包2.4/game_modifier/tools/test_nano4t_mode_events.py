import importlib
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
events_module = importlib.import_module("features.15_nano4t.events")


class ImmediateContext:
    def after(self, _delay_ms, callback):
        callback()


class FakeRuntime:
    def __init__(self):
        self.calls = []

    def on_mode_detected(self):
        self.calls.append("enter")

    def handle_mode_exit(self):
        self.calls.append("exit")


class Nano4tModeEventTests(unittest.TestCase):
    def setUp(self):
        self.runtime = FakeRuntime()
        self.original_runtime_factory = events_module._runtime
        events_module._runtime = lambda _context: self.runtime

    def tearDown(self):
        events_module._runtime = self.original_runtime_factory

    def test_mode_enter_updates_the_runtime_without_waiting_for_a_round_event(self):
        events_module.handle_event(ImmediateContext(), "nano4t_mode_enter", {})
        self.assertEqual(self.runtime.calls, ["enter"])

    def test_mode_exit_clears_the_runtime(self):
        events_module.handle_event(ImmediateContext(), "nano4t_mode_exit", {})
        self.assertEqual(self.runtime.calls, ["exit"])

    def test_nano4t_has_no_battle_round_compatibility_trigger(self):
        source_root = Path(__file__).resolve().parents[1]
        events_source = (source_root / "features" / "15_nano4t" / "events.py").read_text(encoding="utf-8")
        runtime_source = (source_root / "features" / "15_nano4t" / "runtime.py").read_text(encoding="utf-8")
        self.assertNotIn('event == "mode_detected"', events_source)
        self.assertNotIn('feature_id="battle_round"', runtime_source)


if __name__ == "__main__":
    unittest.main()
