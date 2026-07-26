import json
import logging
import threading
from logging.handlers import RotatingFileHandler
from pathlib import Path

from core.config import APP_DIR


_LOGGER_NAME = "game_modifier.aim_debug_file"
_HANDLER_MARKER = "_aim_debug_handler"
_debug_logger = None
_debug_handler = None
_debug_lock = threading.RLock()


def _get_debug_logger():
    global _debug_logger, _debug_handler
    with _debug_lock:
        logger = logging.getLogger(_LOGGER_NAME)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if (
            _debug_handler is not None
            and _debug_handler in logger.handlers
        ):
            return logger

        log_dir = Path(APP_DIR) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = (log_dir / "aim_debug.log").resolve()

        for existing in list(logger.handlers):
            if not getattr(existing, _HANDLER_MARKER, False):
                continue
            existing_file = Path(getattr(existing, "baseFilename", "")).resolve()
            if existing_file == log_file:
                _debug_logger = logger
                _debug_handler = existing
                return logger
            logger.removeHandler(existing)
            existing.close()

        handler = RotatingFileHandler(
            log_file,
            maxBytes=2 * 1024 * 1024,
            backupCount=2,
            encoding="utf-8",
        )
        setattr(handler, _HANDLER_MARKER, True)
        handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(handler)

        _debug_logger = logger
        _debug_handler = handler
        return logger


def close_debug_log():
    global _debug_logger, _debug_handler
    with _debug_lock:
        if _debug_handler is not None:
            _debug_handler.flush()
            if (
                _debug_logger is not None
                and _debug_handler in _debug_logger.handlers
            ):
                _debug_logger.removeHandler(_debug_handler)
            _debug_handler.close()
        _debug_handler = None
        _debug_logger = None


def handle_event(context, event, payload):
    if event != "aim_debug_sample" or not isinstance(payload, dict) or not payload:
        return

    line = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    _get_debug_logger().info(line)


def handle_lifecycle(context, event, payload):
    if event == "app_closing":
        close_debug_log()
