#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""通用小工具：文件 / 时间 / 大小 / 哈希 / 配置 / 游戏进程 / 日志读取。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import hashlib
import json
import os
import subprocess
import sys
import time

from ui.consts import CREATE_NO_WINDOW
from ui.env import CFG_PATH, DEPLOY, GAME_LOG_DIR, LOG_DIR, P


def find_log(name):
    r"""日志在哪：工程端 log\ → <部署端>\log\ → 部署端根目录（越往后越老）。"""
    for p in (os.path.join(LOG_DIR, name),
              os.path.join(GAME_LOG_DIR, name),
              os.path.join(DEPLOY, name)):
        if os.path.isfile(p):
            return p
    return os.path.join(LOG_DIR, name)


def _cut(text, n):
    r"""长名字截断（表格列宽固定，别让一行把整张表撑歪）。"""
    text = str(text or "")
    return text if len(text) <= n else text[:max(1, n - 1)] + "…"


def file_sha256(path):
    r"""小文件的 sha256（几毫秒）；读不了返回空串。"""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for blk in iter(lambda: f.read(65536), b""):
                h.update(blk)
        return h.hexdigest()
    except OSError:
        return ""


def compact_path(path, limit=52):
    r"""路径太长就省略：只留盘符 + 末尾若干层（区分信息通常在尾巴上）。
    D:\BaiduNetdiskDownload\test-1\UnityCrossFire1.7.1\UnityCrossFire.exe -> D:\…\test-1\UnityCrossFire1.7.1\UnityCrossFire.exe
    """
    path = str(path or "")
    if len(path) <= limit:
        return path
    drive, rest = os.path.splitdrive(path)
    keep = limit - len(drive) - 2
    if keep <= 8:
        return path[: limit - 1] + "…"
    return drive + "\\…" + rest[-keep:]


def game_tag(game_exe):
    r"""底部按钮上「这是哪一份游戏」的短标签：从游戏目录往上，跳过像游戏名的层级。
    ...\BaiduNetdiskDownload\test-1\UnityCrossFire1.7.1\...\UnityCrossFire.exe -> test-1
    ...\BaiduNetdiskDownload\UnityCrossFire1.7.1\...\UnityCrossFire.exe          -> BaiduNetdiskDownload
    """
    try:
        game_dir = os.path.dirname(os.path.abspath(game_exe))
        parts = [p for p in game_dir.replace("/", "\\").split("\\") if p]
        i = len(parts) - 1
        while i >= 0 and parts[i].lower().startswith("unitycrossfire"):
            i -= 1
        if i >= 0:
            return parts[i]
        return os.path.basename(game_dir) or game_dir
    except Exception:
        return ""


def _python():
    r"""跑 navdata.py 用的解释器：控制台是 .pyw，sys.executable 可能是 pythonw.exe，
    那样子进程没有控制台、输出不好收，优先换成同目录的 python.exe。"""
    exe = sys.executable or "python"
    if exe.lower().endswith("pythonw.exe"):
        cand = os.path.join(os.path.dirname(exe), "python.exe")
        if os.path.isfile(cand):
            return cand
    return exe


def _listdir(path):
    try:
        return os.listdir(path)
    except OSError:
        return []


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%d %s" % (n, unit)) if unit == "B" else ("%.1f %s" % (n, unit))
        n /= 1024.0
    return "%.1f GB" % n


def fmt_time(ts):
    if not ts:
        return "（空）"
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def fmt_short(ts):
    r"""行内用的短时间：11-21 10:41（数据页按块报数，不再占一长串年份）。

    日期和时间之间用不换行空格：Tk 的自动换行只在空格处断行，
    普通空格会让「最近 11-21 12:16」断成两行、时间字悬在下一行。"""
    if not ts:
        return "—"
    t = time.localtime(ts)
    return time.strftime("%m-%d", t) + "\u00a0" + time.strftime("%H:%M", t)


def dir_bytes(root):
    r"""整个目录递归的 (字节数, 最新写入时间)；读不动就当 0 / 空。
    和 dir_stats 的区别：dir_stats 只数 maps/nav/vis，这个连 final、packs 一起算。"""
    total = 0
    latest = 0.0
    for base, _dirs, files in os.walk(root):
        for fn in files:
            try:
                st = os.stat(os.path.join(base, fn))
            except OSError:
                continue
            total += st.st_size
            latest = max(latest, st.st_mtime)
    return total, latest


def dir_stats(root):
    r"""这一版数据的 (文件数, 字节数, 最新写入时间)：每张图的 map.json + navmesh.bin + 路线 txt。

    ② 的 packs、final 不在这里算（成品 / 编辑中 两行各自报数），不然数字会混。"""
    n = total = 0
    latest = 0.0
    for _key, path in list(P.map_files(root)) + list(P.navmesh_files(root)) + list(P.route_files(root)):
        try:
            st = os.stat(path)
        except OSError:
            continue
        n += 1
        total += st.st_size
        latest = max(latest, st.st_mtime)
    return n, total, latest


def load_cfg():
    try:
        with open(CFG_PATH, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_cfg(cfg):
    tmp = CFG_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, CFG_PATH)


_PROC_CACHE = {"t": 0.0, "v": False}


def _game_running_fast():
    r"""Toolhelp 快照枚举进程（约 2 ms）。tasklist 子进程要 300+ ms，
    切「编辑中 / 成品」两页时会明显顿一下，所以这里绕开子进程。
    不是 Windows / 结构对不上时返回 None，调用方退回 tasklist。"""
    try:
        import ctypes
        from ctypes import wintypes

        class PROCESSENTRY32W(ctypes.Structure):
            _fields_ = [("dwSize", wintypes.DWORD),
                        ("cntUsage", wintypes.DWORD),
                        ("th32ProcessID", wintypes.DWORD),
                        ("th32DefaultHeapID", ctypes.c_size_t),
                        ("th32ModuleID", wintypes.DWORD),
                        ("cntThreads", wintypes.DWORD),
                        ("th32ParentProcessID", wintypes.DWORD),
                        ("pcPriClassBase", ctypes.c_long),
                        ("dwFlags", wintypes.DWORD),
                        ("szExeFile", wintypes.WCHAR * 260)]

        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k32.Process32FirstW.argtypes = [wintypes.HANDLE,
                                        ctypes.POINTER(PROCESSENTRY32W)]
        k32.Process32FirstW.restype = wintypes.BOOL
        k32.Process32NextW.argtypes = [wintypes.HANDLE,
                                       ctypes.POINTER(PROCESSENTRY32W)]
        k32.Process32NextW.restype = wintypes.BOOL
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        k32.CloseHandle.restype = wintypes.BOOL

        snap = k32.CreateToolhelp32Snapshot(0x00000002, 0)   # TH32CS_SNAPPROCESS
        if not snap or snap == ctypes.c_void_p(-1).value:
            return None
        try:
            entry = PROCESSENTRY32W()
            entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
            ok = k32.Process32FirstW(snap, ctypes.byref(entry))
            while ok:
                if str(entry.szExeFile).lower() == "unitycrossfire.exe":
                    return True
                ok = k32.Process32NextW(snap, ctypes.byref(entry))
            return False
        finally:
            k32.CloseHandle(snap)
    except Exception:                   # noqa: BLE001  退回 tasklist
        return None


def game_running(fresh=False, ttl=1.0):
    r"""游戏在不在跑？1 s 内复用上次结果（切页、4 s 状态定时器都会问）。
    fresh=True 强制作一次真扫描（kill_game 等游戏退出时用）。"""
    now = time.time()
    if not fresh and now - _PROC_CACHE["t"] < ttl:
        return _PROC_CACHE["v"]
    fast = _game_running_fast()
    if fast is None:
        try:
            out = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq UnityCrossFire.exe", "/NH"],
                capture_output=True, text=True, errors="replace", timeout=5,
                creationflags=CREATE_NO_WINDOW)
            fast = "UnityCrossFire.exe" in (out.stdout or "")
        except Exception:
            fast = False
    _PROC_CACHE["t"] = now
    _PROC_CACHE["v"] = bool(fast)
    return bool(fast)


def kill_game(wait=8.0):
    r"""车测前必须关掉游戏：UCF_AUTOTEST 只对**新进程**生效。
    返回 True = 确认已退出；False = 8 秒还没关掉（可能卡死，交给用户处理）。"""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "UnityCrossFire.exe"],
                       capture_output=True, creationflags=CREATE_NO_WINDOW)
    except OSError:
        return False
    deadline = time.time() + wait
    while time.time() < deadline:
        if not game_running(fresh=True):
            return True
        time.sleep(0.3)
    return not game_running(fresh=True)


def read_log_from(path, offset):
    r"""从字节偏移接着读日志；文件被轮转/改小而 offset 超了，就从头再读。"""
    try:
        size = os.path.getsize(path)
    except OSError:
        return "", 0
    if size < offset:
        offset = 0
    try:
        with open(path, "rb") as f:
            f.seek(offset)
            data = f.read()
    except OSError:
        return "", offset
    return data.decode("utf-8", "replace"), offset + len(data)


def tail_log(n=6):
    try:
        with open(find_log("ucf_mod.log"), "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 65536))
            data = f.read().decode("utf-8", "replace")
    except OSError:
        return []
    lines = [ln for ln in data.splitlines() if ln.strip()]
    return lines[-n:]
