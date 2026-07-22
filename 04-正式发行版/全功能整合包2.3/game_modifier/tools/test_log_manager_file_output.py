import importlib
import logging
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


class LogManagerFileOutputTests(unittest.TestCase):
    def test_setup_logging_writes_file_even_when_packaged(self):
        import core.log_manager as log_manager

        original_frozen = getattr(sys, "frozen", None)
        temp_dir = Path(tempfile.mkdtemp())
        try:
            reloaded = importlib.reload(log_manager)
            reloaded.APP_DIR = str(temp_dir)
            sys.frozen = True

            reloaded.setup_logging()

            logger = logging.getLogger("game_modifier.damage_multiplier")
            logger.info("damage_diag packaged file check")
            for handler in logging.getLogger("game_modifier").handlers:
                handler.flush()

            log_file = temp_dir / "logs" / "game_modifier.log"
            self.assertTrue(log_file.exists())
            self.assertIn("damage_diag packaged file check", log_file.read_text(encoding="utf-8"))
        finally:
            root = logging.getLogger("game_modifier")
            for handler in list(root.handlers):
                handler.close()
                root.removeHandler(handler)
            if original_frozen is None:
                try:
                    delattr(sys, "frozen")
                except AttributeError:
                    pass
            else:
                sys.frozen = original_frozen
            shutil.rmtree(temp_dir, ignore_errors=True)
            importlib.reload(log_manager)


if __name__ == "__main__":
    unittest.main()
