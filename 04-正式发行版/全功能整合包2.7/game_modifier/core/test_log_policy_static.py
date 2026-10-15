import contextlib
import logging
import sys
import tempfile
import unittest
from logging.handlers import RotatingFileHandler
from pathlib import Path


GAME_MODIFIER_DIR = Path(__file__).resolve().parent.parent
LOG_MANAGER = Path(__file__).with_name("log_manager.py")
CONFIG_FILE = Path(__file__).with_name("config.py")
AIM_EVENTS = GAME_MODIFIER_DIR / "features" / "11_aim" / "events.py"
SPEC = GAME_MODIFIER_DIR / "game_modifier_onedir.spec"
INSTALLER = GAME_MODIFIER_DIR / "packaging" / "installer.iss"


@contextlib.contextmanager
def file_log_env(frozen, app_dir):
    """临时切换 sys.frozen / APP_DIR 并重置 logging，退出时完整还原。"""
    if str(GAME_MODIFIER_DIR) not in sys.path:
        sys.path.insert(0, str(GAME_MODIFIER_DIR))
    from core import log_manager

    root = logging.getLogger("game_modifier")
    saved_handlers = list(root.handlers)
    saved_initialized = log_manager._initialized
    saved_app_dir = log_manager.APP_DIR
    saved_frozen = getattr(sys, "frozen", None)

    for handler in list(root.handlers):
        root.removeHandler(handler)
    log_manager._initialized = False
    log_manager.APP_DIR = str(app_dir)
    if frozen:
        sys.frozen = True
    elif hasattr(sys, "frozen"):
        del sys.frozen

    try:
        yield log_manager
    finally:
        for handler in list(root.handlers):
            root.removeHandler(handler)
            with contextlib.suppress(Exception):
                handler.close()
        for handler in saved_handlers:
            root.addHandler(handler)
        log_manager._initialized = saved_initialized
        log_manager.APP_DIR = saved_app_dir
        if saved_frozen is None:
            if hasattr(sys, "frozen"):
                del sys.frozen
        else:
            sys.frozen = saved_frozen


class ReleaseLogPersistenceTests(unittest.TestCase):
    """发行版（exe）绝不把日志持久化成文件；开发版保持写盘。"""

    def test_frozen_build_creates_no_log_file_or_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with file_log_env(frozen=True, app_dir=temp_dir) as log_manager:
                log_manager.setup_logging()
                log_manager.log_to_file("info", "系统", "release-should-not-persist")

                root = logging.getLogger("game_modifier")
                self.assertTrue(
                    all(isinstance(handler, logging.NullHandler) for handler in root.handlers)
                )
                self.assertFalse(
                    any(isinstance(handler, logging.FileHandler) for handler in root.handlers)
                )
                self.assertFalse((Path(temp_dir) / "logs").exists())

    def test_dev_build_still_writes_log_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            with file_log_env(frozen=False, app_dir=temp_dir) as log_manager:
                log_manager.setup_logging()
                log_manager.log_to_file("info", "系统", "dev-line")
                root = logging.getLogger("game_modifier")
                self.assertTrue(
                    any(isinstance(handler, RotatingFileHandler) for handler in root.handlers)
                )

            log_file = Path(temp_dir) / "logs" / "game_modifier.log"
            self.assertTrue(log_file.exists())
            self.assertIn("dev-line", log_file.read_text(encoding="utf-8"))

    def test_log_manager_checks_policy_before_opening_any_file(self):
        text = LOG_MANAGER.read_text(encoding="utf-8")
        self.assertIn("def file_logging_enabled():", text)
        self.assertIn('return not getattr(sys, "frozen", False)', text)
        # 策略判定必须早于 _ensure_log_dir()/RotatingFileHandler
        self.assertLess(
            text.index("if not file_logging_enabled():"),
            text.index("log_dir = _ensure_log_dir()"),
        )

    def test_aim_debug_log_is_gated_by_the_same_policy(self):
        text = AIM_EVENTS.read_text(encoding="utf-8")
        self.assertIn("from core.log_manager import file_logging_enabled", text)
        self.assertIn("not AIM_DEBUG_LOG_ENABLED or not file_logging_enabled()", text)

    def test_packaging_never_ships_or_writes_logs(self):
        spec = SPEC.read_text(encoding="utf-8")
        self.assertIn("console=False", spec)
        # spec 只挑选运行所需文件，不收集 logs 目录
        self.assertNotIn("logs", spec.split("datas = []", 1)[1].split("a = Analysis", 1)[0])

        installer = INSTALLER.read_text(encoding="utf-8")
        self.assertIn("logs\\*", installer.replace("logs\\*", "logs\\*"))
        self.assertIn("logs", installer)


if __name__ == "__main__":
    unittest.main()
