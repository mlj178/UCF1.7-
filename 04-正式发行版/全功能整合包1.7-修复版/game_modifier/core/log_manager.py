"""
Unified logging module based on Python standard logging.

- All log messages go to both UI (via EventBus) and disk (logs/game_modifier.log)
- trace_id is auto-generated per session for correlation
- Log files rotate to avoid unbounded growth
"""

import logging
import os
import sys
import uuid
from logging.handlers import RotatingFileHandler

from core.config import APP_DIR

# Global trace_id for this program session
TRACE_ID = uuid.uuid4().hex[:8]

# Custom level: SUCCESS (between INFO=20 and WARNING=30)
SUCCESS = 25
logging.addLevelName(SUCCESS, 'SUCCESS')

# Level mapping from app's level strings to logging levels
_LEVEL_MAP = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'success': SUCCESS,
    'warning': logging.WARNING,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

_initialized = False


def _ensure_log_dir():
    """Create logs directory if not exists"""
    log_dir = os.path.join(APP_DIR, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    return log_dir


def setup_logging():
    """Initialize the root logger with file + console handlers."""
    global _initialized
    if _initialized:
        return
    _initialized = True

    log_dir = _ensure_log_dir()
    log_file = os.path.join(log_dir, 'game_modifier.log')

    # Root logger
    root = logging.getLogger('game_modifier')
    root.setLevel(logging.DEBUG)

    # File handler: rotating, 5MB per file, keep 3 backups
    fmt = logging.Formatter(
        f'[%(asctime)s.%(msecs)03d] [%(levelname)s] [{TRACE_ID}] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # Console handler (for debug in IDE)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    root.addHandler(ch)

    root.info('Logging initialized, trace_id=%s', TRACE_ID)


def get_logger(module_name: str) -> logging.Logger:
    """Get a child logger for a specific module."""
    if not _initialized:
        setup_logging()
    return logging.getLogger(f'game_modifier.{module_name}')


def log_to_file(level_str: str, module: str, message: str):
    """
    Bridge: write a log message from EventBus 'log_message' to the file logger.
    Called by the EventBus subscriber so all existing emit('log_message') calls
    automatically get persisted to disk.
    """
    logger = get_logger(module)
    level = _LEVEL_MAP.get(level_str, logging.INFO)
    logger.log(level, message)
