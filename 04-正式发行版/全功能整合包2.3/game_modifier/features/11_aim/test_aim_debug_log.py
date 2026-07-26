import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


BASE_DIR = Path(__file__).resolve().parent
GAME_MODIFIER_DIR = BASE_DIR.parent.parent
EVENTS_FILE = BASE_DIR / "events.py"


class AimDebugLogTests(unittest.TestCase):
    def _load_events_module(self, module_name="aim_debug_events_test"):
        sys.path.insert(0, str(GAME_MODIFIER_DIR))
        self.addCleanup(lambda: sys.path.remove(str(GAME_MODIFIER_DIR)))
        spec = importlib.util.spec_from_file_location(module_name, EVENTS_FILE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_debug_sample_is_written_as_json_to_feature_log(self):
        temp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        events = self._load_events_module()
        payload = {
            "originSource": "camera",
            "targetSource": "real_bone",
            "dy": 4.25,
            "targetPitchDeg": 12.5,
            "writtenPitchDeg": 12.5,
        }

        with patch.object(events, "APP_DIR", str(temp_dir)):
            events.handle_event(None, "aim_debug_sample", payload)
            self.assertEqual(events._debug_handler.maxBytes, 2 * 1024 * 1024)
            self.assertEqual(events._debug_handler.backupCount, 2)
            events.close_debug_log()

        log_file = temp_dir / "logs" / "aim_debug.log"
        self.assertTrue(log_file.exists())
        line = log_file.read_text(encoding="utf-8").strip()
        decoded = json.loads(line)
        self.assertEqual(decoded, payload)

    def test_unrelated_event_does_not_create_log_file(self):
        temp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        events = self._load_events_module()

        with patch.object(events, "APP_DIR", str(temp_dir)):
            events.handle_event(None, "other_event", {"value": 1})
            events.close_debug_log()

        self.assertFalse((temp_dir / "logs" / "aim_debug.log").exists())

    def test_reloading_event_module_does_not_duplicate_log_handlers(self):
        temp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: shutil.rmtree(temp_dir, ignore_errors=True))
        first = self._load_events_module("aim_debug_events_first")
        second = self._load_events_module("aim_debug_events_second")

        with (
            patch.object(first, "APP_DIR", str(temp_dir)),
            patch.object(second, "APP_DIR", str(temp_dir)),
        ):
            first.handle_event(None, "aim_debug_sample", {"sequence": 1})
            second.handle_event(None, "aim_debug_sample", {"sequence": 2})
            first.close_debug_log()
            second.close_debug_log()

        lines = (temp_dir / "logs" / "aim_debug.log").read_text(
            encoding="utf-8"
        ).splitlines()
        self.assertEqual([json.loads(line)["sequence"] for line in lines], [1, 2])


if __name__ == "__main__":
    unittest.main()
