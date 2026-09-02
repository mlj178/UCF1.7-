import unittest
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from gravity_airmove_probe import SessionSummary, build_log_paths, choose_target, run_probe


class LogPathAndSummaryTests(unittest.TestCase):
    def test_build_log_paths_separates_label_and_timestamp(self):
        events_path, summary_path = build_log_paths("logs", "2.5", "20260902_180000")
        self.assertEqual(events_path.name, "gravity_airmove_2.5_20260902_180000.jsonl")
        self.assertEqual(summary_path.name, "gravity_airmove_2.5_20260902_180000_summary.json")

    def test_summary_counts_airborne_and_horizontal_motion_samples(self):
        summary = SessionSummary(label="2.5")
        summary.observe({"type": "player_snapshot", "grounded": False})
        summary.observe({"type": "controller_move", "vector_readable": True})
        summary.observe({"type": "probe_error", "message": "sample"})
        report = summary.to_dict()
        self.assertEqual(report["airborne_samples"], 1)
        self.assertEqual(report["readable_horizontal_moves"], 1)
        self.assertEqual(report["errors"], 1)

    def test_choose_target_returns_only_unitycrossfire_process(self):
        processes = [
            {"pid": 100, "name": "UCF2.4修改器.exe"},
            {"pid": 200, "name": "UnityCrossFire.exe"},
        ]
        self.assertEqual(choose_target(processes), {"pid": 200, "name": "UnityCrossFire.exe"})

    def test_choose_target_rejects_ambiguous_game_processes(self):
        processes = [
            {"pid": 200, "name": "UnityCrossFire.exe"},
            {"pid": 201, "name": "UnityCrossFire-Test.exe"},
        ]
        self.assertIsNone(choose_target(processes))

    def test_probe_script_has_only_readonly_operations(self):
        source = Path(__file__).with_name("gravity_airmove_probe.js").read_text(encoding="utf-8").lower()
        self.assertIn("interceptor.attach", source)
        self.assertIn("readu8", source)
        self.assertIn("readfloat", source)
        self.assertNotIn(".write", source)
        self.assertNotIn("interceptor.replace", source)
        self.assertNotIn("nativecallback", source)
        self.assertNotIn("nativefunction", source)

    def test_probe_script_observes_getter_and_reads_x86_vector_by_value(self):
        source = Path(__file__).with_name("gravity_airmove_probe.js").read_text(encoding="utf-8")
        self.assertIn("Player.get_isMyPlayer", source)
        self.assertIn("onLeave(retval)", source)
        self.assertIn("stackArgToFloat(args[1])", source)
        self.assertIn("stackArgToFloat(args[2])", source)
        self.assertIn("stackArgToFloat(args[3])", source)
        self.assertIn("if (!localController || !args[0].equals(localController))", source)

    def test_run_probe_returns_zero_when_stopped_during_process_wait(self):
        class InterruptingDevice:
            def enumerate_processes(self):
                raise KeyboardInterrupt

        fake_frida = SimpleNamespace(get_local_device=lambda: InterruptingDevice())
        with patch.dict("sys.modules", {"frida": fake_frida}):
            self.assertEqual(run_probe("2.5", poll_seconds=0.001), 0)

    def test_run_probe_finishes_when_attached_session_detaches(self):
        class FakeScript:
            def on(self, _name, _callback):
                pass

            def load(self):
                pass

        class DetachedSession:
            def on(self, name, callback):
                if name == "detached":
                    callback("process-terminated", None)

            def create_script(self, _source):
                return FakeScript()

            def detach(self):
                pass

        class AttachedDevice:
            def enumerate_processes(self):
                return [SimpleNamespace(pid=200, name="UnityCrossFire.exe")]

            def attach(self, _pid):
                return DetachedSession()

        fake_frida = SimpleNamespace(get_local_device=lambda: AttachedDevice())
        with patch.dict("sys.modules", {"frida": fake_frida}):
            self.assertEqual(run_probe("2.5", poll_seconds=0.001), 0)

    def test_run_probe_writes_summary_when_frida_initialization_fails(self):
        logs_dir = Path(__file__).with_name("logs")
        before = set(logs_dir.glob("gravity_airmove_2.4_*_summary.json"))
        fake_frida = SimpleNamespace(get_local_device=lambda: (_ for _ in ()).throw(RuntimeError("no device")))
        with patch.dict("sys.modules", {"frida": fake_frida}):
            self.assertEqual(run_probe("2.4", poll_seconds=0.001), 1)
        summaries = set(logs_dir.glob("gravity_airmove_2.4_*_summary.json")) - before
        self.assertEqual(len(summaries), 1)
        report = json.loads(summaries.pop().read_text(encoding="utf-8"))
        self.assertEqual(report["errors"], 1)

    def test_readme_documents_two_version_comparison_workflow(self):
        text = Path(__file__).with_name("README.md").read_text(encoding="utf-8")
        self.assertIn("2.4", text)
        self.assertIn("2.5", text)
        self.assertIn("只读", text)


if __name__ == "__main__":
    unittest.main()
