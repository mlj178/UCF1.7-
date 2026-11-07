"""
Unified logging module based on Python standard logging.

- **开发版**（python 直接运行）：日志写盘到 logs/game_modifier.log，5MB 轮转保留 3 份，
  便于离线排查。
- **发行版**（PyInstaller 打包成 exe，sys.frozen=True）：**绝不落盘**，
  不创建 logs 目录、不打开任何 .log 文件；只挂一个 NullHandler。
  界面日志面板走 EventBus（app._log），不受影响，仍会显示。
- trace_id is auto-generated per session for correlation
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


def file_logging_enabled():
    """是否允许把日志持久化成文件。

    唯一判据：**打包成 exe 后一律禁止**（发行版不产生任何 .log 文件）。
    开发版保持写盘，供离线排查。任何新增的日志落盘点都必须先过这个函数。
    """
    return not getattr(sys, "frozen", False)


def _ensure_log_dir():
    """Create logs directory if not exists（仅开发版会走到这里）"""
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

    # Root logger
    root = logging.getLogger('game_modifier')
    root.setLevel(logging.DEBUG)

    if not file_logging_enabled():
        # 发行版（exe）：不建 logs 目录、不打开 .log 文件，只丢弃日志。
        # 界面日志面板不受影响（它读的是 EventBus 消息，不是 logging handler）。
        root.addHandler(logging.NullHandler())
        return

    # File handler: rotating, 5MB per file, keep 3 backups
    fmt = logging.Formatter(
        f'[%(asctime)s.%(msecs)03d] [%(levelname)s] [{TRACE_ID}] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_dir = _ensure_log_dir()
    log_file = os.path.join(log_dir, 'game_modifier.log')
    fh = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    root.addHandler(fh)

    # Console handler: 所有环境都输出到控制台
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
