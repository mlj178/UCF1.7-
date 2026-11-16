#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UCF 导航编辑器 · 本地服务（只用标准库，双击 启动导航编辑器.bat 即可）

它做四件事：
  1) 给 navview.html 列出 vis/、nav/ 里能打开的地图数据；
  2) 保存编辑结果 —— 同时写两份：
       nav/<地图名>.json   人看的权威数据（ucf-navgraph v1 + edits 段）
       nav/<指纹>.txt      游戏内插件直接读的编辑清单（ucf-navedit v1）
     保存前自动备份，可一键回滚；
  3) 把 geo/web/<关卡>.bin（geo2web.py 生成的灰模网格）发给浏览器做 3D 视图；
  4) 记住每张图的中文名（nav/names.json）。

只监听 127.0.0.1，仅本机可访问。
"""
import json
import os
import re
import socket
import struct
import subprocess
import sys
import threading
import time
import webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote

ROOT = os.path.dirname(os.path.abspath(__file__))   # 工程端 tools/
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from ucf_paths import DEPLOY as UCF, GEO, VIS, NAV, MAPS  # noqa: E402

GEOWEB = os.path.join(GEO, "web")
NAMES_FILE = os.path.join(NAV, "names.json")

# ------------------------------------------------------- 日志 / 自动归档（新增）
AUTO = {"running": False, "at": "", "out": "", "runs": 0}
LOG_FILE = os.path.join(UCF, "ucf_mod.log")


def tail_log(n=120):
    """ucf_mod.log 的最后 n 行（只读尾部 256 KB，不整文件读）。"""
    try:
        with open(LOG_FILE, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 262144))
            data = f.read().decode("utf-8", "replace")
    except OSError:
        return []
    lines = [ln for ln in data.splitlines() if ln.strip()]
    return lines[-max(1, n):]


def vis_stamp():
    """vis/ 下导出文件的 (文件名, mtime) 指纹：变了就说明插件刚写了新数据。"""
    out = []
    try:
        for name in os.listdir(VIS):
            if name.endswith(".json") or name.endswith(".bin"):
                try:
                    out.append((name, int(os.path.getmtime(os.path.join(VIS, name)))))
                except OSError:
                    pass
    except OSError:
        pass
    return tuple(sorted(out))


def run_organize():
    """新导出自动归到 maps/NN_中文名.json（等价于手动跑 organize_maps.py --archive）。"""
    script = os.path.join(ROOT, "organize_maps.py")
    if not os.path.isfile(script):
        return
    AUTO["running"] = True
    try:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, "-u", script, "--archive"],
                           cwd=ROOT, capture_output=True, timeout=300, env=env)
        txt = (r.stdout or b"").decode("utf-8", "replace").strip()
        err = (r.stderr or b"").decode("utf-8", "replace").strip()
        AUTO["out"] = txt[-1200:] or err[-600:] or "(无输出)"
    except Exception as e:                      # noqa: BLE001
        AUTO["out"] = "自动归档失败: %r" % (e,)
    finally:
        AUTO["running"] = False
        AUTO["at"] = time.strftime("%H:%M:%S")
        AUTO["runs"] += 1


def auto_organize_loop():
    """后台盯 vis/：有新导出就先等 6 秒（等插件写完），再自动归档。"""
    last = vis_stamp()
    wait = 0
    while True:
        time.sleep(2.0)
        cur = vis_stamp()
        if cur != last:
            last = cur
            wait = 6
            continue
        if wait:
            wait -= 2
            if wait <= 0:
                run_organize()
                last = vis_stamp()      # 归档会把文件搬走，别把自己再触发一次

# 内置中文名：key 可以是关卡名（level1）、小地图贴图名（level1_TransportShip）
# 兜底表：地图对照表.md 缺失/损坏时才用
BUILTIN_DEFAULT_NAMES = {
    # 关卡 -> 官方中文名（证据：sharedassets0 里的选图表「模式名/场景名/中文名」，
    # 再用每个 levelN 场景文件里的场景名交叉验证）
    "level1": "运输船", "TransportShip": "运输船",
    "level2": "小型工厂", "Factory": "小型工厂",
    "level3": "椰岛之巅", "Cebu_City": "椰岛之巅",
    "level4": "胜利广场", "NY_TM": "胜利广场",
    "level5": "竞技场", "Arena": "竞技场",
    "level6": "刀锋寨", "GrimReaperKM": "刀锋寨",
    "level7": "沙漠要塞", "DesertFort": "沙漠要塞",
    "level8": "生化酒店", "NanoResort": "生化酒店",
    "level9": "暴风", "Nano30_Storm": "暴风", "nano30_storm": "暴风",
    "level10": "新寂静村", "Nano_DawnVillage": "新寂静村",
    "level11": "死亡擂台", "DeathRing": "死亡擂台",
    "level0": "主菜单",
}

# 权威对照表（手写在 mod 根目录，持久保存；改了不用重启服务，下次请求就生效）
TABLE_FILE = os.path.join(UCF, "地图对照表.md")
TABLE_ROW_RE = re.compile(r"^\|\s*(\d{1,3})\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
_table_cache = {"mtime": -1.0, "rows": []}


def load_map_table(path=None):
    path = path or TABLE_FILE
    try:
        m = os.path.getmtime(path)
    except OSError:
        return []
    if m == _table_cache["mtime"]:
        return _table_cache["rows"]
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                hit = TABLE_ROW_RE.match(line.strip())
                if not hit:
                    continue
                name = hit.group(3).strip()
                if not name:
                    continue
                rows.append((int(hit.group(1)), hit.group(2), name,
                             hit.group(4).strip(), hit.group(5).strip()))
    except OSError:
        rows = []
    rows.sort()
    _table_cache["mtime"] = m
    _table_cache["rows"] = rows
    return rows


def default_names():
    rows = load_map_table()
    if len(rows) < 5:
        return dict(BUILTIN_DEFAULT_NAMES)
    out = {}
    for (_no, lv, nm, sc, _note) in rows:
        out[lv] = nm
        if sc:
            out[sc] = nm
    out.setdefault("level1_TransportShip", out.get("level1", ""))
    out.setdefault("nano30_storm", out.get("level9", ""))
    out.setdefault("level0", "主菜单")
    return out

TOKEN_RE = re.compile(r"^[A-Za-z0-9._-]{1,80}$")
FP_RE = re.compile(r"^n\d+-[0-9a-fA-F]{16}$")
EDIT_FILE_RE = re.compile(r"^n\d+-[0-9a-fA-F]{16}\.txt$")
NODE_RE = re.compile(r"^node\s+(add|del)\s+-?\d+(?:\.\d+)?\s+-?\d+(?:\.\d+)?\s+-?\d+(?:\.\d+)?$")
NUM = r"-?\d+(?:\.\d+)?"
EDGE_RE = re.compile(r"^edge\s+(add|del)\s+(?:%s\s+){5}%s$" % (NUM, NUM))

_cache = {}          # path -> (mtime, info)
_names = {"mtime": -1.0, "data": {}}


# ---------------------------------------------------------------- 基础工具
def ensure_dirs():
    for d in (VIS, NAV, GEOWEB):
        try:
            os.makedirs(d, exist_ok=True)
        except OSError:
            pass


def load_names():
    """返回 {key: {"name": str, "level": str}}，兼容老格式（值是字符串）。"""
    try:
        m = os.path.getmtime(NAMES_FILE)
    except OSError:
        m = -1.0
    if m == _names["mtime"]:
        return _names["data"]
    data = {}
    if m >= 0:
        try:
            with open(NAMES_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            raw = {}
        if isinstance(raw, dict):
            for k, v in raw.items():
                if isinstance(v, str):
                    data[k] = {"name": v.strip(), "level": ""}
                elif isinstance(v, dict):
                    data[k] = {"name": str(v.get("name") or "").strip(),
                               "level": str(v.get("level") or "").strip()}
    _names["mtime"] = m
    _names["data"] = data
    return data


def save_names(data):
    ensure_dirs()
    tmp = NAMES_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, NAMES_FILE)
    try:
        _names["mtime"] = os.path.getmtime(NAMES_FILE)
    except OSError:
        _names["mtime"] = -1.0
    _names["data"] = data


def safe_token(s, fallback=""):
    s = str(s or "").strip()
    s = re.sub(r'[\\/:*?"<>|\r\n\t]', "_", s)
    s = s.strip(". ")
    return s[:60] or fallback


def level_from_text(s):
    """从 "level1_TransportShip" / "level1_xxx_20261115_145521" 里抠出 level1。"""
    if not s:
        return ""
    m = re.match(r"^(level\d+)\b", s, re.I)
    if m:
        return m.group(1).lower()
    m = re.search(r"\b(level\d+)\b", s, re.I)
    return m.group(1).lower() if m else ""


# ---------------------------------------------------------------- 索引
def summarize(path):
    try:
        m = os.path.getmtime(path)
    except OSError:
        return None
    hit = _cache.get(path)
    if hit and hit[0] == m:
        return hit[1]
    info = None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        mp = data.get("map") or {}
        nodes = data.get("nodes") or []
        info = {
            "fp": str(mp.get("fingerprint") or ""),
            "mapName": str(mp.get("name") or ""),
            "source": str(mp.get("source") or ""),
            "format": str(data.get("format") or ""),
            "version": data.get("version") or 0,
            "generated": str(data.get("generated") or ""),
            "mapLevel": str(mp.get("level") or ""),
            "mapLabel": str(mp.get("label") or ""),
            "nodes": len(nodes),
            "edges": len(data.get("edges") or []),
            "features": len(data.get("features") or []),
            "bbox": mp.get("bbox") or None,
        }
    except Exception as exc:
        info = {"error": str(exc)}
    if info is not None:
        info["mtime"] = time.strftime("%Y-%m-%d %H:%M", time.localtime(m))
        info["mtimeTs"] = m
        info["size"] = os.path.getsize(path)
    _cache[path] = (m, info)
    return info


def list_snapshots():
    out = []
    names = load_names()
    for kind, folder in (("maps", MAPS), ("nav", NAV), ("vis", VIS)):
        try:
            files = sorted(os.listdir(folder))
        except OSError:
            continue
        for fn in files:
            if not fn.lower().endswith(".json") or fn in ("names.json", "_index.json"):
                continue
            p = os.path.join(folder, fn)
            if not os.path.isfile(p):
                continue
            info = summarize(p)
            if not info or info.get("error"):
                continue
            fp = info.get("fp") or ""
            key = info.get("mapName") or fp or os.path.splitext(fn)[0]
            entry = dict(info)
            entry.update({"dir": kind, "file": fn, "key": key})
            # 关卡：指纹 > 地图名 > 文件名；中文名：指纹 > 地图名 > 关卡 > 内置表
            level = str(info.get("mapLevel") or "")
            if not level:
                for k in (fp, info.get("mapName"), os.path.splitext(fn)[0]):
                    if k and k in names and names[k].get("level"):
                        level = names[k]["level"]
                        break
            if not level:
                level = level_from_text(info.get("mapName") or fn) or ""
            entry["level"] = level
            label = str(info.get("mapLabel") or "")
            if not label:
                for k in (fp, info.get("mapName"), level):
                    if k and k in names and names[k].get("name"):
                        label = names[k]["name"]
                        break
            if not label:
                label = default_names().get(level, "") or default_names().get(info.get("mapName") or "", "")
            entry["label"] = label
            out.append(entry)
    def _sort_key(e):
        # maps/ 按文件名里的序号排（01_ 02_ …），其余按中文名排
        if e.get("dir") == "maps":
            return (0, e.get("file") or "", 0)
        rank = 1 if e.get("dir") == "nav" else 2
        return (rank, e.get("label") or e.get("level") or e["file"], e.get("mtimeTs") or 0)

    out.sort(key=_sort_key)
    return out


def read_txt_head(path):
    fp = ""
    ops = 0
    bad = 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if not s:
                    continue
                if s.startswith("#"):
                    m = re.search(r"fp=(\S+)", s)
                    if m:
                        fp = m.group(1)
                    continue
                if NODE_RE.match(s) or EDGE_RE.match(s):
                    ops += 1
                else:
                    bad += 1
    except OSError:
        return None
    return {"fp": fp or os.path.splitext(os.path.basename(path))[0], "ops": ops, "bad": bad}


def list_edits():
    out = []
    try:
        files = sorted(os.listdir(NAV))
    except OSError:
        return out
    for fn in files:
        # 只认插件真正会读的那种文件名：<指纹>.txt（nav 里还躺着 probe_*.txt 之类的日志）
        if not EDIT_FILE_RE.match(fn):
            continue
        p = os.path.join(NAV, fn)
        if not os.path.isfile(p):
            continue
        head = read_txt_head(p)
        if not head:
            continue
        try:
            m = os.path.getmtime(p)
        except OSError:
            continue
        out.append({
            "dir": "nav",
            "file": fn,
            "fp": head["fp"],
            "ops": head["ops"],
            "bad": head["bad"],
            "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(m)),
            "mtimeTs": m,
            "size": os.path.getsize(p),
        })
    out.sort(key=lambda e: e["mtimeTs"] or 0, reverse=True)
    return out


def list_geo():
    out = []
    try:
        files = sorted(os.listdir(GEOWEB))
    except OSError:
        return out
    for fn in files:
        if not fn.endswith(".bin"):
            continue
        p = os.path.join(GEOWEB, fn)
        if not os.path.isfile(p):
            continue
        bbox = None
        try:
            with open(p, "rb") as f:
                head = f.read(12)
                if head[:4] == b"UCFG":
                    jl = struct.unpack("<I", head[8:12])[0]
                    hdr = json.loads(f.read(jl).decode("utf-8"))
                    bbox = hdr.get("bbox")
        except Exception:
            bbox = None
        out.append({"level": fn[:-4], "bytes": os.path.getsize(p), "bbox": bbox,
                    "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p)))})
    return out


def list_backups(fp):
    out = []
    if not fp:
        return out
    try:
        files = sorted(os.listdir(NAV))
    except OSError:
        return out
    for fn in files:
        if not fn.startswith(fp) or ".bak_" not in fn:
            continue
        p = os.path.join(NAV, fn)
        if os.path.isfile(p):
            out.append({"file": fn, "size": os.path.getsize(p),
                        "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p)))})
    out.sort(key=lambda e: e["file"], reverse=True)
    return out


def validate_txt(text):
    """返回 (ok, 有效行数, 错误信息)。游戏端只会跳过不认的行，这里宁可报错。"""
    ops = 0
    fp = ""
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            m = re.search(r"fp=(\S+)", s)
            if m:
                fp = m.group(1)
            continue
        if NODE_RE.match(s) or EDGE_RE.match(s):
            ops += 1
            continue
        return False, ops, "第 %d 行不是合法的编辑指令：%s" % (i, s[:60])
    return True, ops, ""


# ---------------------------------------------------------------- HTTP
class Handler(SimpleHTTPRequestHandler):
    server_version = "ucf-navserver/2"
    protocol_version = "HTTP/1.1"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    def log_message(self, fmt, *args):
        sys.stderr.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), fmt % args))

    # ---- helpers ----
    def send_bytes(self, body, ctype, code=200, filename=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if filename:
            self.send_header("Content-Disposition", 'attachment; filename="%s"' % filename)
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def send_json(self, obj, code=200):
        self.send_bytes(json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                        "application/json; charset=utf-8", code)

    def read_json_body(self, limit=96 * 1024 * 1024):
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return None
        if n <= 0 or n > limit:
            return None
        raw = self.rfile.read(n)
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception:
            return None

    # ---- GET ----
    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        path = u.path
        if path in ("/", "/index.html", "/navview.html"):
            self.path = "/navview.html"
            return SimpleHTTPRequestHandler.do_GET(self)
        try:
            if path == "/api/maps":
                index = {}
                try:
                    ip = os.path.join(MAPS, "_index.json")
                    if os.path.isfile(ip):
                        with open(ip, "r", encoding="utf-8") as f:
                            index = json.load(f)
                except Exception:
                    index = {}
                return self.send_json({
                    "ok": True,
                    "ucf": UCF,
                    "names": load_names(),
                    "defaults": default_names(),
                    "mapIndex": index,
                    "snapshots": list_snapshots(),
                    "edits": list_edits(),
                    "geo": list_geo(),
                })
            if path == "/api/log":
                n = 120
                try:
                    n = max(1, min(2000, int((q.get("n") or ["120"])[0])))
                except ValueError:
                    pass
                return self.send_json({
                    "ok": True,
                    "tail": tail_log(n),
                    "auto": AUTO,
                    "vis": [{"name": v[0], "mtime": v[1]} for v in vis_stamp()[-10:]],
                })
            if path == "/api/files":
                # 兼容 2026-11-15 那版 navview.html（它的接口叫 /api/files）
                snaps = list_snapshots()
                return self.send_json({
                    "ok": True, "ucf": UCF,
                    "vis": [x for x in snaps if x["dir"] == "vis"],
                    "nav": [x for x in snaps if x["dir"] == "nav"],
                })
            if path == "/api/names":
                return self.send_json({"ok": True, "names": load_names(), "defaults": default_names()})
            if path == "/api/raw":
                kind = (q.get("dir") or ["vis"])[0]
                fn = safe_token((q.get("file") or [""])[0])
                base = MAPS if kind == "maps" else (NAV if kind == "nav" else VIS)
                p = os.path.join(base, fn)
                if not os.path.isfile(p):
                    return self.send_json({"ok": False, "error": "文件不存在: " + fn}, 404)
                with open(p, "rb") as f:
                    return self.send_bytes(f.read(), "application/json; charset=utf-8")
            if path == "/api/txt":
                fp = safe_token((q.get("fp") or [""])[0])
                p = os.path.join(NAV, fp + ".txt")
                if not os.path.isfile(p):
                    return self.send_json({"ok": True, "fp": fp, "text": "", "exists": False})
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    return self.send_json({"ok": True, "fp": fp, "text": f.read(), "exists": True})
            if path == "/api/backups":
                return self.send_json({"ok": True, "items": list_backups(safe_token((q.get("fp") or [""])[0]))})
            if path == "/api/geo":
                level = safe_token((q.get("level") or [""])[0])
                if not level:
                    return self.send_json({"ok": False, "error": "缺少 level"}, 400)
                p = os.path.join(GEOWEB, level + ".bin")
                if not os.path.isfile(p) and (q.get("build") or [""])[0] in ("1", "true"):
                    try:
                        subprocess.run([sys.executable, os.path.join(ROOT, "geo2web.py"), level],
                                       cwd=ROOT, timeout=120, capture_output=True)
                    except Exception as exc:
                        return self.send_json({"ok": False, "error": "生成失败: %s" % exc}, 500)
                if not os.path.isfile(p):
                    return self.send_json({
                        "ok": False,
                        "error": "没有 %s 的网格缓存，先跑 tools/geo2web.py %s" % (level, level),
                    }, 404)
                with open(p, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return
            if path == "/api/leveltest":
                # 判断一堆坐标点属于哪个关卡（用 geo/web 的 bbox 粗判，够用且不依赖 numpy）
                return self.send_json({"ok": True, "geo": list_geo()})
        except Exception as exc:   # 兜底，别把服务搞崩
            return self.send_json({"ok": False, "error": "%s: %s" % (type(exc).__name__, exc)}, 500)
        return SimpleHTTPRequestHandler.do_GET(self)

    # ---- POST ----
    def do_POST(self):
        u = urlparse(self.path)
        body = self.read_json_body()
        if body is None:
            return self.send_json({"ok": False, "error": "请求体为空或不是 JSON"}, 400)
        try:
            if u.path == "/api/name":
                return self.post_name(body)
            if u.path == "/api/save":
                return self.post_save(body)
            if u.path == "/api/restore":
                return self.post_restore(body)
        except Exception as exc:
            return self.send_json({"ok": False, "error": "%s: %s" % (type(exc).__name__, exc)}, 500)
        return self.send_json({"ok": False, "error": "未知接口 " + u.path}, 404)

    def post_name(self, body):
        key = safe_token(body.get("key") or body.get("fp") or body.get("level"))
        name = str(body.get("name") or "").strip()[:40]
        level = str(body.get("level") or "").strip()
        if not key:
            return self.send_json({"ok": False, "error": "缺少 key"}, 400)
        names = dict(load_names())
        if not name and not level:
            names.pop(key, None)
        else:
            cur = names.get(key) or {}
            names[key] = {"name": name or cur.get("name", ""), "level": level or cur.get("level", "")}
        save_names(names)
        return self.send_json({"ok": True, "names": names})

    def post_save(self, body):
        ensure_dirs()
        fp = safe_token(body.get("fp"))
        if not FP_RE.match(fp or ""):
            return self.send_json({"ok": False, "error": "指纹格式不对：%r（应形如 n786-57a46e3465c847cb）" % fp}, 400)
        json_name = safe_token(body.get("jsonName")) or fp
        json_text = body.get("jsonText") or ""
        edit_text = body.get("editText") or ""
        if not json_text.strip():
            return self.send_json({"ok": False, "error": "jsonText 为空"}, 400)
        try:
            doc = json.loads(json_text)
        except Exception as exc:
            return self.send_json({"ok": False, "error": "JSON 非法：%s" % exc}, 400)
        ok, ops, err = validate_txt(edit_text)
        if not ok:
            return self.send_json({"ok": False, "error": err}, 400)

        json_path = os.path.join(NAV, json_name + ".json")
        txt_path = os.path.join(NAV, fp + ".txt")
        stamp = time.strftime("%Y%m%d_%H%M%S")
        backups = []
        for p in (json_path, txt_path):
            if not os.path.isfile(p):
                continue
            try:
                with open(p, "rb") as f:
                    old = f.read()
                bak = p + ".bak_" + stamp
                with open(bak, "wb") as f:
                    f.write(old)
                backups.append(os.path.basename(bak))
            except OSError:
                pass

        tmp = json_path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(json_text)
        os.replace(tmp, json_path)

        tmp = txt_path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(edit_text)
        os.replace(tmp, txt_path)

        # 顺手记住这张图的中文名 / 关卡
        label = str(body.get("label") or "").strip()[:40]
        level = str(body.get("level") or "").strip()
        if label or level:
            names = dict(load_names())
            for k in (fp, safe_token(body.get("key"))):
                if k:
                    names[k] = {"name": label or names.get(k, {}).get("name", ""),
                                "level": level or names.get(k, {}).get("level", "")}
            save_names(names)

        _cache.pop(json_path, None)
        if ops:
            note = "已写入 %d 条编辑 → nav/%s.txt（进游戏这张图会自动套用）" % (ops, fp)
        else:
            note = "编辑清单为空 → 已删除 nav/%s.txt 的效果（游戏里恢复原图）" % fp
        return self.send_json({
            "ok": True,
            "jsonPath": json_path,
            "txtPath": txt_path,
            "jsonName": json_name,
            "ops": ops,
            "nodes": len(doc.get("nodes") or []),
            "backups": backups,
            "note": note,
        })

    def post_restore(self, body):
        fn = safe_token(body.get("file"))
        if not fn or ".bak_" not in fn:
            return self.send_json({"ok": False, "error": "只能还原 .bak_* 备份文件"}, 400)
        src = os.path.join(NAV, fn)
        if not os.path.isfile(src):
            return self.send_json({"ok": False, "error": "备份不存在: " + fn}, 404)
        dst = os.path.join(NAV, fn.split(".bak_")[0])
        with open(src, "rb") as f:
            data = f.read()
        with open(dst, "wb") as f:
            f.write(data)
        return self.send_json({"ok": True, "restored": os.path.basename(dst), "bytes": len(data)})


def pick_port(preferred=8765, tries=40):
    for i in range(tries):
        p = preferred + i
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(("127.0.0.1", p))
            s.close()
            return p
        except OSError:
            s.close()
    raise SystemExit("找不到可用端口")


def main():
    ensure_dirs()
    port = pick_port()
    url = "http://127.0.0.1:%d/navview.html" % port
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    srv.daemon_threads = True
    print("UCF 导航编辑器 · 本地服务")
    print("  插件目录 : %s" % UCF)
    print("  打开地址 : %s" % url)
    print("  （关掉这个窗口就停止服务；编辑结果会写进 %s）" % NAV)
    for name in ("snapshots", "edits", "geo"):
        print("  %-10s %d" % (name, len({"snapshots": list_snapshots, "edits": list_edits, "geo": list_geo}[name]())))
    if not list_geo():
        print("  !! geo/web 是空的：3D 视图只能画路点。跑一次 tools/geo2web.py 生成网格。")
    if "--no-browser" not in sys.argv:
        threading.Thread(target=lambda: (time.sleep(0.4), webbrowser.open(url)), daemon=True).start()
    threading.Thread(target=auto_organize_loop, daemon=True).start()   # 新导出自动归档
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()