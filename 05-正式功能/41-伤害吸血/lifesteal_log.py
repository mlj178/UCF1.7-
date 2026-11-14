"""伤害吸血 · 运行日志持久化。

为什么单独抽一个模块：
    独立测试 UI（AAAAA-lifesteal_ui.py）和将来整合包里的 feature.py 要写同一种日志，
    路径 / 行格式 / 滚动规则只能有一处定义，不然两边各写一套，出问题对不上。
    写日志属于纯观测，**任何情况下都不允许影响功能**，所以模块内部吞掉所有异常。

日志位置：
    <功能目录>/logs/lifesteal-YYYYmmdd-HHMMSS.log
    - 每启动一次一个新文件：一次测试 = 一个文件，方便和游戏里的表现对照；
    - 同一目录最多保留 MAX_FILES 个文件，超出删最旧的；
    - 单个文件超过 MAX_BYTES 自动滚到 -2 / -3；
    - 功能目录不可写时（装到 Program Files 之类）退到 %LOCALAPPDATA%\\UCFModifier\\logs。

行格式：
    2026-11-14 11:20:31.123 [INFO ] [ui] 文本 key=value key2=value2

环境变量：
    LIFESTEAL_LOG_LEVEL=DEBUG  可以把 DEBUG 也写进文件（默认只写 INFO 及以上）。
"""

from __future__ import annotations

import json
import os
import threading
import time
from datetime import datetime

MAX_FILES = 20
MAX_BYTES = 8 * 1024 * 1024
LEVELS = ("DEBUG", "INFO", "WARN", "ERROR")
LEVEL_ENV = "LIFESTEAL_LOG_LEVEL"

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def default_log_dir():
    """优先写在功能目录下的 logs/；不可写时退到用户目录，绝不因此报错。"""
    primary = os.path.join(_BASE_DIR, "logs")
    try:
        os.makedirs(primary, exist_ok=True)
        probe = os.path.join(primary, ".write_probe")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
        return primary
    except Exception:
        fallback = os.path.join(
            os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"), "UCFModifier", "logs"
        )
        try:
            os.makedirs(fallback, exist_ok=True)
        except Exception:
            pass
        return fallback


def _format_value(value):
    if isinstance(value, float):
        text = ("%.4f" % value).rstrip("0").rstrip(".")
        return text or "0"
    if value is None or isinstance(value, (str, int, bool)):
        return str(value)
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except Exception:
        return str(value)


def _format_fields(fields):
    if not fields:
        return ""
    parts = []
    for key in sorted(fields):
        parts.append(str(key) + "=" + _format_value(fields[key]))
    return " " + " ".join(parts)


class RunLogger(object):
    """一次运行对应一个日志文件（线程安全）。"""

    def __init__(self, log_dir=None, prefix="lifesteal", source="ui", echo=False):
        self.log_dir = os.path.abspath(log_dir or default_log_dir())
        self.prefix = prefix
        self.source = source
        self.echo = echo
        self.min_level = self._level_from_env()
        self._lock = threading.RLock()
        self._handle = None
        self._path = ""
        self._base = time.strftime(prefix + "-%Y%m%d-%H%M%S")
        self._part = 0
        self._closed = False
        self._open_next_part()

    @staticmethod
    def _level_from_env():
        raw = (os.environ.get(LEVEL_ENV) or "INFO").strip().upper()
        return raw if raw in LEVELS else "INFO"

    # ---------- 文件管理 ----------

    def _open_next_part(self):
        try:
            os.makedirs(self.log_dir, exist_ok=True)
        except Exception:
            return
        self._part += 1
        suffix = "" if self._part == 1 else "-%d" % self._part
        path = os.path.join(self.log_dir, self._base + suffix + ".log")
        try:
            handle = open(path, "a", encoding="utf-8", newline="")
        except Exception:
            self._handle = None
            return
        self._handle = handle
        self._path = path
        if self._part == 1:
            self._prune()
            self._write_line("INFO", "运行日志开始", {"file": path, "level": self.min_level})

    def _prune(self):
        try:
            names = [
                os.path.join(self.log_dir, name)
                for name in os.listdir(self.log_dir)
                if name.startswith(self.prefix + "-") and name.endswith(".log")
            ]
        except Exception:
            return
        if len(names) <= MAX_FILES:
            return
        try:
            names.sort(key=lambda item: os.path.getmtime(item))
        except Exception:
            return
        for stale in names[: len(names) - MAX_FILES]:
            try:
                os.remove(stale)
            except Exception:
                pass

    def _roll(self):
        try:
            if self._handle is not None:
                self._handle.flush()
                self._handle.close()
        except Exception:
            pass
        self._handle = None
        self._open_next_part()

    def path(self):
        return self._path

    # ---------- 写入 ----------

    def _write_line(self, level, message, fields):
        line = "%s [%-5s] [%s] %s%s" % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
            level,
            self.source,
            message,
            _format_fields(fields),
        )
        handle = self._handle
        if handle is not None:
            try:
                if handle.tell() > MAX_BYTES:
                    self._roll()
                    handle = self._handle
                if handle is not None:
                    handle.write(line + "\n")
                    handle.flush()
            except Exception:
                pass
        if self.echo:
            try:
                print(line)
            except Exception:
                pass

    def write(self, level, message, **fields):
        if self._closed:
            return
        level = (str(level) or "INFO").strip().upper()
        if level not in LEVELS:
            level = "INFO"
        if LEVELS.index(level) < LEVELS.index(self.min_level):
            return
        with self._lock:
            try:
                if self._handle is None:
                    self._open_next_part()
                self._write_line(level, message, fields)
            except Exception:
                pass

    def debug(self, message, **fields):
        self.write("DEBUG", message, **fields)

    def info(self, message, **fields):
        self.write("INFO", message, **fields)

    def warn(self, message, **fields):
        self.write("WARN", message, **fields)

    def error(self, message, **fields):
        self.write("ERROR", message, **fields)

    def close(self):
        with self._lock:
            if self._closed:
                return
            self._write_line("INFO", "运行日志结束", {})
            self._closed = True
            try:
                if self._handle is not None:
                    self._handle.flush()
                    self._handle.close()
            except Exception:
                pass
            self._handle = None


_LOGGER = None
_REGISTRY_LOCK = threading.RLock()


def start(log_dir=None, prefix="lifesteal", source="ui", echo=False):
    """启动一次运行日志；重复调用返回同一个文件路径。"""
    global _LOGGER
    with _REGISTRY_LOCK:
        if _LOGGER is None:
            _LOGGER = RunLogger(log_dir=log_dir, prefix=prefix, source=source, echo=echo)
        return _LOGGER.path()


def get():
    return _LOGGER


def path():
    logger = _LOGGER
    return logger.path() if logger is not None else ""


def stop():
    global _LOGGER
    with _REGISTRY_LOCK:
        logger = _LOGGER
        _LOGGER = None
    if logger is not None:
        logger.close()


def write(level, message, **fields):
    logger = _LOGGER
    if logger is not None:
        logger.write(level, message, **fields)


def debug(message, **fields):
    write("DEBUG", message, **fields)


def info(message, **fields):
    write("INFO", message, **fields)


def warn(message, **fields):
    write("WARN", message, **fields)


def error(message, **fields):
    write("ERROR", message, **fields)
