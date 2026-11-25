#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UCF 路点工作台 · 本地只读服务（只用标准库，由控制台「路点工作台（查看）」启动）

2026-11-18 起网页端永久只读，编辑能力已删除。它做三件事：
  1) 给 console/web/navview.html 列出 vis/、nav/ 里能打开的地图数据；
  2) 把 geo/web/<关卡>.bin（tools/geo/geo2web.py 生成的灰模网格）发给浏览器做 3D 视图；
  3) 提供可走面、测试包文本、地图名等只读数据。

所有 POST 写接口已移除，统一返回 405。建测试包 / 升成品请用命令行：
    python core/navdata.py pack new <包名> --level <关卡>
    python core/navdata.py pack promote <包名>     # 编辑中 -> 成品

只监听 127.0.0.1，仅本机可访问。
"""
import hashlib
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

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "app", "core"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
ROOT = HERE                                  # 兼容旧名：本文件所在目录
import ucf_paths as P  # noqa: E402   图文件夹 / 可走面 / 路线都从这取
from ucf_paths import (DEPLOY, DEPLOY as UCF, GEO, VIS, NAV, MAPS, NATIVE, DEV, DATAVIS,  # noqa: E402
                       PACKS_DIR, GAME_VIS, PROFILE, READONLY, doc)

GEOWEB = os.path.join(GEO, "web")
GEOTEX = os.path.join(GEO, "tex")      # tools/geo/fetch_tex.py 从 AssetRipper 拉下来的贴图
COMMON = P.common_dir(P.DATA)        # 公共文件（names / _index）：新布局 00_公共\，旧布局 nav\
NAMES_FILE = P.names_path(P.DATA)

# ---------------------------------------------------------------- 数据档切换
# 网页端只读，但可以在 ① 备份版 / ② 成品 / ② 编辑中 之间切换查看。
# ② 开发版是唯一数据源：成品在 ②\final\<当前版本>\，编辑中在 ②\packs\<图>\<包>\，
# 收件箱在 ②\vis\。③ 部署版只是游戏运行环境（2026-11-21 起不放导航数据），
# 不再作为“可查看的数据档”。
# 切换只改本服务的内存状态（读哪一套图文件夹），不写任何文件。
PROFILE_ORDER = ("native", "final", "pack")
PROFILE_LABEL = {"native": "① 备份版", "final": "② 成品", "pack": "② 编辑中"}
PROFILE_CN_VIEW = {
    "native": "备份版（原生·只读对照）",
    "final": "成品（final 每图一份·只读）",
    "pack": "编辑中（packs 测试包·只读）",
}
PROFILE_ROOT = {"native": NATIVE, "final": DEV, "pack": DEV}
PROFILE_ALIAS = {
    "native": "native", "backup": "native", "frozen": "native", "原生": "native", "备份": "native",
    "final": "final", "dev": "final", "develop": "final", "开发": "final",
    "成品": "final", "current": "final",
    "pack": "pack", "packs": "pack", "test": "pack", "export": "pack",
    "测试": "pack", "编辑中": "pack",
    # ③ 部署版已取消（不再放数据）：旧深链接落到 ② 成品，前端会提示一句
    "deploy": "final", "game": "final", "部署": "final",
}
FINAL = os.path.join(DEV, "final")      # ② 的成品版本集合（③ 不放数据）
VIEW_LOCK = threading.RLock()
VIEW_NOTE = ""


def profile_info():
    """当前查看档 + 路径（供 /api/workbench、/api/maps、navview 顶栏）。"""
    return {
        "profile": PROFILE,          # 兼容旧前端/深链接：值现在是 native|final|pack
        "mode": PROFILE,
        "note": VIEW_NOTE,
        "cn": PROFILE_CN_VIEW.get(PROFILE, PROFILE),
        "label": PROFILE_LABEL.get(PROFILE, PROFILE),
        "readonly": READONLY,
        "data": DATA,
        "common": COMMON,
        "maps": MAPS,
        "nav": NAV,
        "native": NATIVE,
        "dev": DEV,
        "deploy": DEPLOY,            # 仍是游戏运行目录（日志/配置用），不再参与查看档
        "packs": PACKS_DIR,
        "final": FINAL,
        "export": VIS,
        "gameVis": GAME_VIS,
        "profiles": [{"id": k, "label": PROFILE_LABEL[k], "cn": PROFILE_CN_VIEW[k]}
                     for k in PROFILE_ORDER],
    }


def dev_nav_dir(data_root, key):
    r"""② 成品目录：final\（平铺，一张图一份；不再有版本子目录）。"""
    if key != "final":
        return os.path.join(data_root, "nav")
    return os.path.join(data_root, "final")


def _final_index():
    r"""② 成品台账 dev\final\_index.json（读不到就当空台账）。"""
    try:
        with open(os.path.join(FINAL, "_index.json"), "r", encoding="utf-8") as f:
            idx = json.load(f) or {}
    except (OSError, ValueError):
        idx = {}
    return idx if isinstance(idx, dict) else {}


def _final_current_name(idx=None):
    r"""兼容旧调用：成品有 <指纹>.txt 就返回固定名 final，否则空串。"""
    return "final" if _final_has_any() else ""


def _final_has_any():
    try:
        return any(re.match(r"^n\d+-[0-9a-fA-F]{16}\.txt$", n) for n in os.listdir(FINAL))
    except OSError:
        return False


def _final_dir():
    r"""成品目录（平铺 <指纹>.txt）；一张图都没有就给空串。"""
    return FINAL if _final_has_any() else ""


def _default_view():
    """工作台启动时的默认档：成品有当前版看成品，否则有包看编辑中，再否则成品。"""
    if _final_current_name():
        return "final"
    try:
        if any(os.path.isdir(os.path.join(PACKS_DIR, n)) and not n.startswith(("_", "."))
               for n in os.listdir(PACKS_DIR)):
            return "pack"
    except OSError:
        pass
    return "final"


def set_profile(name):
    """切换“当前查看哪一档”；只改内存里的根目录，不动文件。"""
    global PROFILE, READONLY, DATA, MAPS, NAV, COMMON, NAMES_FILE, DATAVIS, VIEW_NOTE
    raw = str(name or "").strip().lower()
    key = PROFILE_ALIAS.get(raw, "")
    VIEW_NOTE = ""
    if raw in ("deploy", "game", "部署"):
        VIEW_NOTE = "③ 部署版已取消（游戏目录不放导航数据），已切到 ② 成品"
    elif raw in ("test", "export", "测试"):
        VIEW_NOTE = "旧 ④ 测试版已并入 ② 编辑中"
    elif raw in ("dev", "develop", "开发"):
        VIEW_NOTE = "② 开发版已拆成「成品 / 编辑中」，这里默认看成品"
    if key:
        PROFILE = key
        DATA = PROFILE_ROOT[key]
        # 地图数据的根：新布局就是数据根（图文件夹在它下面），旧布局才是 maps\
        MAPS = DATA if P.is_folders(DATA) else os.path.join(DATA, "maps")
        # 公共文件（names.json / _index.json）：新布局 00_公共\，旧布局 nav\
        COMMON = P.common_dir(DATA)
        # 成品搬进 final\<版本>\ 以后，成品档看的是「当前启动的那个版本」
        NAV = dev_nav_dir(DATA, key)
        NAMES_FILE = P.names_path(DATA)
        DATAVIS = os.path.join(DATA, "vis")
        # 网页端永久只读：三个档都不写文件
        READONLY = True
    return profile_info()


set_profile(_default_view())

# 网页前端（七页工作台 + 3D 查看器）在 console/web/，只有这个目录暴露给浏览器
WEB = P.WEB
# ② 测试包目录（ucf_paths.PACKS_DIR）：只对某一张图生效的路线改动

# ---------------------------------------------------------------- 可走面（NavMeshGraph）
# 原生 A* 顶点数（网格顶点去重后），逐张图实测，见 docs/地图对照表.md
# §「原生可通行空间（A* 图）」；重新核对：python tools/data/scan_native_nav.py
NATIVE_VERTS = {
    "level2": 840, "level3": 532, "level4": 716, "level5": 683,
    "level6": 559, "level7": 919, "level10": 944, "level11": 60,
}


def navmesh_for(level):
    """level -> vis/navmesh_*.bin，找不到返回 None。

    回退顺序：
      1) maps/*.json 里记录的原导出名（organize_maps.py 整理时留下的 navmesh.file）；
      2) 按原生顶点数对号：插件落盘的文件叫 navmesh_nm<顶点数>-<指纹>.bin，
         例如小型工厂 840 -> navmesh_nm840-40749e0342e84cbd.bin。
    运输船/生化酒店/暴风本来就没有 NavMeshGraph，永远返回 None。
    """
    # 0) 图文件夹里就有：<图>\navmesh.bin（当前版没有就回 ①/② 找，③ 已经不放数据）
    for root in (DATA, NATIVE, DEV):
        hit = P.navmesh_file(root, level)
        if hit:
            return hit
    # 1) 整理后的地图数据里带 navmesh.file
    try:
        for _rel, path in P.map_files(DATA):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    d = json.load(f)
            except (OSError, ValueError):
                continue
            m = d.get("map") or {}
            if m.get("level") != level:
                continue
            fn = (d.get("navmesh") or {}).get("file")
            if not fn:
                continue
            for base in (DATAVIS, VIS, os.path.join(VIS, "navmesh"),
                         os.path.join(GAME_VIS, "navmesh"),   # 迁移前的旧位置
                         os.path.join(NATIVE, "vis"),
                         os.path.join(DEV, "vis"),
                         os.path.join(UCF, "backup"), GEOWEB):
                p = os.path.join(base, os.path.basename(fn))
                if os.path.isfile(p):
                    return p
    except OSError:
        pass
    # 2) 按原生顶点数对号
    v = NATIVE_VERTS.get(level)
    if v:
        try:
            prefix = "navmesh_nm%d-" % v
            for base in (DATAVIS, VIS, os.path.join(VIS, "navmesh"),
                         os.path.join(GAME_VIS, "navmesh"),
                         os.path.join(NATIVE, "vis"), os.path.join(DEV, "vis")):
                if not os.path.isdir(base):
                    continue
                for name in sorted(os.listdir(base)):
                    if name.startswith(prefix) and name.endswith(".bin"):
                        return os.path.join(base, name)
        except OSError:
            pass
    return None


# ------------------------------------------------------- 日志 / 自动归档（新增）
AUTO = {"running": False, "at": "", "out": "", "runs": 0}
# 2026-11-23：日志主位置在工程端 log\（控制台用 UCF_LOG_DIR 指给插件）；
# 没走控制台时插件落 <部署端>\log\，更老的部署还在部署端根目录 —— 三级都认。
LOG_DIR = P.LOG_DIR                                    # 工程端（主）
GAME_LOG_DIR = os.path.join(UCF, "log")                # 部署端（没走控制台时）
LOG_FILE = os.path.join(LOG_DIR, "ucf_mod.log")


def log_file():
    r"""当前该读哪份日志：工程端 → 部署端 log\ → 部署端根目录（越往后越老）。"""
    for p in (LOG_FILE,
              os.path.join(GAME_LOG_DIR, "ucf_mod.log"),
              os.path.join(UCF, "ucf_mod.log")):
        if os.path.isfile(p):
            return p
    return LOG_FILE


def tail_log(n=120):
    """ucf_mod.log 的最后 n 行（只读尾部 256 KB，不整文件读）。"""
    try:
        with open(log_file(), "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 262144))
            raw = f.read()
            try:
                data = raw.decode("utf-8")
            except UnicodeDecodeError:
                # 插件日志是 GBK（中文 Windows），UTF-8 读不出来就回退
                data = raw.decode("gbk", "replace")
    except OSError:
        return []
    lines = [ln for ln in data.splitlines() if ln.strip()]
    return lines[-max(1, n):]


def vis_stamp():
    """vis/ 下导出文件的 (相对路径, mtime) 指纹：变了就说明插件刚写了新数据。"""
    out = []
    for base, dirs, files in os.walk(VIS):
        dirs[:] = [d for d in dirs if d not in ("_state", "_noise")]
        for name in files:
            if name.endswith(".json") or name.endswith(".bin"):
                p = os.path.join(base, name)
                try:
                    out.append((os.path.relpath(p, VIS).replace("\\", "/"),
                                int(os.path.getmtime(p))))
                except OSError:
                    pass
    return tuple(sorted(out))


def run_organize():
    """新导出自动归到 maps/NN_中文名.json（等价于手动跑 organize_maps.py --archive）。"""
    script = P.tool("organize_maps.py")
    if not os.path.isfile(script):
        return
    AUTO["running"] = True
    try:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, "-u", script, "--archive"],
                           cwd=os.path.dirname(script), capture_output=True, timeout=300, env=env)
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
    "level9": "飓风危城", "Nano30_Storm": "飓风危城", "nano30_storm": "飓风危城",
    "level10": "新寂静村", "Nano_DawnVillage": "新寂静村",
    "level11": "死亡擂台", "DeathRing": "死亡擂台",
    "level0": "主菜单",
}

# 模式分组（GameMode 枚举见 dump.cs：Nano3=3 / Nano4=4 / Nano6=5 / Nano4_Terminator=6；
# 地图归属按游戏选图表 + 实际玩法核对：沙漠要塞=生化剑客（官方页面），新寂静村=多人生化，
# 隐藏图 Nano30_Storm「飓风危城」也归多人生化。同一张图只放进一个组，避免下拉里出现两次。）
MODE_BY_LEVEL = {
    "level1": ("团队模式", 0), "level2": ("团队模式", 0), "level3": ("团队模式", 0),
    "level4": ("个人竞技", 1),
    "level5": ("特殊战", 2), "level6": ("特殊战", 2), "level11": ("特殊战", 2),
    "level8": ("生化模式", 3),
    "level7": ("生化剑客模式", 4),
    "level10": ("多人生化模式", 5), "level9": ("多人生化模式", 5),
}
# 原生场景里 0 个 WayPoint：只有可走面，永远采不到点图（见 docs/地图对照表.md §5）
NO_POINT_LEVELS = ("level4", "level11")

# 权威对照表（手写在工程端 docs/，持久保存；改了不用重启服务，下次请求就生效）
TABLE_FILE = doc("地图对照表.md")
TABLE_ROW_RE = re.compile(r"^\|\s*(\d{1,3})\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")
_table_cache = {"mtime": -1.0, "rows": []}


def load_map_table(path=None):
    """只读 md 里的第一张表（5 列权威表）。后面的「原生可通行空间」表也有 序号/关卡/中文名，
    一起读会把每张图重复一遍。"""
    path = path or TABLE_FILE
    try:
        m = os.path.getmtime(path)
    except OSError:
        return []
    if m == _table_cache["mtime"]:
        return _table_cache["rows"]
    rows = []
    started = False
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    if started:
                        break
                    continue
                hit = TABLE_ROW_RE.match(s)
                if not hit:
                    if started and not s.startswith("|"):
                        break
                    continue
                started = True
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
PACK_NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,48}$")   # 测试包名：插件是 C，保持英文
SAFE_FOLDER_RE = re.compile(r'^[^\\/:*?"<>|]{1,30}$')  # 地图文件夹：英文+中文，挡非法字符


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


def safe_relpath(s, fallback=""):
    r"""允许 vis/raw 下的相对路径（a/b.json），挡住 .. 和盘符。"""
    s = str(s or "").strip().replace("\\", "/")
    parts = [p for p in s.split("/") if p not in ("", ".", "..")]
    return "/".join(parts)[:180] or fallback


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
    # 目录名常是 level1_运输船：下划线也是分隔符，\b 在这里不成立
    m = re.search(r"(level\d+)(?=[_\-/\.]|$)", s, re.I)
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
    # 三区都只看自己图文件夹里的 map.json；② 的收件箱（vis）在 /api/workbench 里统计
    kinds = [("maps", MAPS), ("nav", NAV)]
    for kind, folder in kinds:
        entries = []
        if kind == "maps":
            # 新布局：每张图一个文件夹 `<图>\map.json`；旧布局：maps\*.json
            entries = P.map_files(DATA)
        else:
            try:
                files = sorted(os.listdir(folder))
            except OSError:
                continue
            for fn in files:
                if not fn.lower().endswith(".json") or fn in ("names.json", "_index.json"):
                    continue
                p = os.path.join(folder, fn)
                if os.path.isfile(p):
                    entries.append((fn, p))
        for fn, p in entries:
            info = summarize(p)
            if not info or info.get("error"):
                continue
            fp = info.get("fp") or ""
            key = info.get("mapName") or fp or os.path.splitext(os.path.basename(fn))[0]
            entry = dict(info)
            entry.update({"dir": kind, "file": fn, "key": key})
            # 关卡：指纹 > 地图名 > 文件名；中文名：指纹 > 地图名 > 关卡 > 内置表
            level = str(info.get("mapLevel") or "")
            if not level:
                for k in (fp, info.get("mapName"), os.path.splitext(os.path.basename(fn))[0]):
                    if k and k in names and names[k].get("level"):
                        level = names[k]["level"]
                        break
            if not level:
                level = (level_from_text(info.get("mapName") or "")
                         or level_from_text(fn) or "")
            entry["level"] = level
            # 显示名以 docs/地图对照表.md 为准（maps 里的 label / names.json 是旧快照，
            # 隐藏图改叫「飓风危城」不用回写四版数据）
            label = default_names().get(level, "")
            if not label:
                label = str(info.get("mapLabel") or "")
            if not label:
                for k in (fp, info.get("mapName"), level):
                    if k and k in names and names[k].get("name"):
                        label = names[k]["name"]
                        break
            entry["label"] = label
            out.append(entry)

    def _sort_key(e):
        # maps/ 按文件名里的序号排（01_ 02_ …），其余按中文名排
        if e.get("dir") == "maps":
            return (0, e.get("file") or "", 0)
        rank = 1 if e.get("dir") == "nav" else 2      # maps 在前，路线/其它在后
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
                if s == "blank":
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
    # <图>\<指纹>.txt（旧布局 nav\<指纹>.txt）：route_files 已经按指纹筛过，不会有日志混进来
    for _fp, p in P.route_files(DATA):
        fn = os.path.basename(p)
        if not EDIT_FILE_RE.match(fn):
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
        out.append({"level": fn[:-4], "name": default_names().get(fn[:-4], ""),
                    "bytes": os.path.getsize(p), "bbox": bbox,
                    "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p)))})
    # 同一张图有多份地形（level9 与 nano30_storm 都是暴风）：只留 levelN 那份，别在下拉里出现两次
    best = {}
    for e in out:
        nm = e.get("name") or ""
        if not nm:
            continue
        cur = best.get(nm)
        e_is_lv = bool(re.match(r"^level\d+$", e["level"]))
        c_is_lv = bool(re.match(r"^level\d+$", (cur or {}).get("level") or "x"))
        if cur is None or (e_is_lv and not c_is_lv):
            best[nm] = e
    out = [e for e in out if not e.get("name") or best.get(e["name"]) is e]

    def _geo_key(e):
        m = re.match(r"^level(\d+)$", e["level"])
        return (0, int(m.group(1)), "") if m else (1, 0, e["level"])

    out.sort(key=_geo_key)
    return out


def list_backups(fp):
    out = []
    if not fp:
        return out
    # 路线清单现在可能在：图文件夹 → ② 成品当前版本 → ② 编辑中的包 → 旧布局 nav\
    dirs = [NAV] + [os.path.dirname(p) for _rel, p in P.map_files(DATA)]
    cur = _final_dir()
    if cur:
        dirs.append(cur)
    for pk in collect_packs():
        dirs.append(os.path.join(PACKS_DIR, *str(pk.get("name") or "").split("/")))
    seen = set()
    for d in dirs:
        if not os.path.isdir(d):
            continue
        try:
            files = sorted(os.listdir(d))
        except OSError:
            continue
        for fn in files:
            if not fn.startswith(fp) or ".bak" not in fn:   # .bak_ / .bak- 都算
                continue
            p = os.path.join(d, fn)
            if not os.path.isfile(p) or os.path.abspath(p) in seen:
                continue
            seen.add(os.path.abspath(p))
            out.append({"file": fn, "size": os.path.getsize(p),
                        "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(p)))})
    out.sort(key=lambda e: e["file"], reverse=True)
    return out


# ---------------------------------------------------------------- 工作台汇总
# 2026-11-18：七页只读工作台的唯一数据入口。所有数字都从真实文件算：
#   maps/*.json（②开发版）、①备份版、③部署端、④测试包、ucf_mod.json、ucf_mod.log。
# 网页端只读；这里也只做 GET 汇总，不写任何文件。
FEATURE_KINDS = ("nano_area", "nano_pos", "crouch", "guard",
                 "guard_area", "spawn", "jump", "tag_region")
SPAWN_AUX = {0: "gr", 1: "bl", 2: "neutral", 3: "supply", 4: "red", 5: "blue"}

_hash_cache = {}
_info_cache = {}


def sha256(path):
    """文件 SHA256（按 mtime+size 缓存）；读不到返回空串。"""
    try:
        st = os.stat(path)
    except OSError:
        return ""
    key = (path, st.st_mtime, st.st_size)
    hit = _hash_cache.get(key)
    if hit is not None:
        return hit
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
    except OSError:
        return ""
    val = h.hexdigest()
    _hash_cache[key] = val
    return val


def find_navmesh(level, filename=""):
    """这张图的可走面（NavMeshGraph）导出文件；找不到返回 ("", False)。
    只找文件，不解析；运输船/生化酒店/暴风本来就没有 NavMeshGraph。"""
    for root in (DATA, NATIVE, DEV):
        p = P.navmesh_file(root, level)
        if p:
            return os.path.basename(p), True
    bases = (DATAVIS, VIS, os.path.join(VIS, "navmesh"),
             os.path.join(GAME_VIS, "navmesh"), os.path.join(NATIVE, "vis"),
             os.path.join(DEV, "vis"), os.path.join(UCF, "backup"), GEOWEB)
    if filename:
        base = os.path.basename(filename)
        for d in bases:
            p = os.path.join(d, base)
            if os.path.isfile(p):
                return base, True
    v = NATIVE_VERTS.get(level)
    if v:
        prefix = "navmesh_nm%d-" % v
        for d in bases:
            if not os.path.isdir(d):
                continue
            try:
                for name in sorted(os.listdir(d)):
                    if name.startswith(prefix) and name.endswith(".bin"):
                        return name, True
            except OSError:
                pass
    return "", False


def _map_info(path):
    """读一张地图 JSON，算出工作台要用的全部统计（按 mtime+size 缓存）。"""
    try:
        st = os.stat(path)
    except OSError:
        return None
    key = (st.st_mtime, st.st_size)
    hit = _info_cache.get(path)
    if hit and hit[0] == key:
        return dict(hit[1])
    try:
        with open(path, "r", encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, ValueError) as exc:
        info = {"error": str(exc)}
        _info_cache[path] = (key, info)
        return dict(info)

    mp = doc.get("map") or {}
    nodes = doc.get("nodes") or []
    edges = doc.get("edges") or []
    feats = doc.get("features") or []
    lines = doc.get("lines") or {}
    if not isinstance(lines, dict):
        lines = {}

    id2i = {}
    for i, n in enumerate(nodes):
        nid = n.get("id")
        if nid is not None:
            id2i.setdefault(str(nid), i)
    adj = [[] for _ in nodes]
    valid_edges = 0
    for e in edges:
        if not e or len(e) < 2:
            continue
        a = id2i.get(str(e[0]))
        b = id2i.get(str(e[1]))
        if a is None or b is None or a == b:
            continue
        adj[a].append(b)
        adj[b].append(a)
        valid_edges += 1

    walk = 0
    ys = []
    xs = []
    zs = []
    for n in nodes:
        if n.get("walk", 1):
            walk += 1
        p = n.get("p") or []
        if len(p) >= 3:
            try:
                xs.append(float(p[0]))
                ys.append(float(p[1]))
                zs.append(float(p[2]))
            except (TypeError, ValueError):
                pass

    deg = [len(a) for a in adj]
    isolated = sum(1 for d in deg if d == 0)
    degree_gt6 = sum(1 for d in deg if d > 6)
    max_degree = max(deg) if deg else 0
    comps = 0
    seen = bytearray(len(nodes))
    for i in range(len(nodes)):
        if seen[i]:
            continue
        comps += 1
        seen[i] = 1
        stack = [i]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = 1
                    stack.append(v)

    kinds = {}
    spawn_aux = {}
    crouch_aux = {}
    for f in feats:
        k = str(f.get("kind") or "")
        if not k:
            continue
        kinds[k] = kinds.get(k, 0) + 1
        a = f.get("aux")
        if k == "spawn":
            spawn_aux[str(a)] = spawn_aux.get(str(a), 0) + 1
        elif k == "crouch":
            crouch_aux[str(a)] = crouch_aux.get(str(a), 0) + 1

    bbox = mp.get("bbox")
    if not bbox and xs:
        bbox = [[min(xs), min(ys) if ys else 0.0, min(zs)],
                [max(xs), max(ys) if ys else 0.0, max(zs)]]

    level = str(mp.get("level") or "")
    nm = mp.get("navmesh") or {}
    nm_file, nm_ok = find_navmesh(level, str((nm or {}).get("file") or ""))

    info = {
        "fp": str(mp.get("fingerprint") or ""),
        "name": str(mp.get("name") or ""),
        "label": str(mp.get("label") or ""),
        "level": level,
        "scene": str(mp.get("scene") or ""),
        "source": str(mp.get("source") or ""),
        "generated": str(doc.get("generated") or ""),
        "nodes": len(nodes),
        "walkable": walk,
        "edges": valid_edges,
        "features": len(feats),
        "kinds": kinds,
        "spawnAux": spawn_aux,
        "crouchAux": crouch_aux,
        "jumpLinks": len(lines.get("jump") or []),
        "nanoNeighbor": len(lines.get("nano_neighbor") or []),
        "entranceEscape": len(lines.get("entrance_escape") or []),
        "isolated": isolated,
        "components": comps,
        "degreeGt6": degree_gt6,
        "maxDegree": max_degree,
        "support": mp.get("support", (walk / len(nodes)) if nodes else 0),
        "bbox": bbox,
        "routes": len(doc.get("routes") or []),
        "zones": len(doc.get("zones") or []),
        "navmesh": nm_ok,
        "navmeshFile": nm_file,
        "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
        "mtimeTs": st.st_mtime,
        "size": st.st_size,
    }
    _info_cache[path] = (key, info)
    return dict(info)


def _route_txt(root, fp):
    r"""<指纹>.txt 在哪：<图>\<指纹>.txt（旧布局 nav\）→ ② 成品当前版本。

    只认「成品」，**不认编辑中的包**：某个包的改动由 /api/pack-txt 明确点名，
    不能让「随便一个包」被当成基准套上去
    （2026-11-21：这里原来会退回 packs，结果运输船被 151954 那个 grow 包套成 982 点）。
    """
    if not fp:
        return ""
    if PROFILE == "pack":
        return ""                        # 编辑中档不猜包；要套包走 /api/pack-txt
    for cand_fp, p in P.route_files(root):
        if cand_fp == fp:
            return p
    if PROFILE != "final" or os.path.normpath(root) != os.path.normpath(DEV):
        return ""                        # 只有 ② 成品有 final\
    cur = _final_dir()
    p = os.path.join(cur, fp + ".txt") if cur else ""
    return p if p and os.path.isfile(p) else ""


def _edit_ops(root, fp):
    r"""编辑清单（<图>\<指纹>.txt，旧布局 nav\<指纹>.txt）里插件真正会执行的 node/edge 指令数。"""
    if not fp:
        return 0
    p = ""
    for cand_fp, cand in P.route_files(root):
        if cand_fp == fp:
            p = cand
            break
    if not p:
        p = os.path.join(root, "nav", fp + ".txt")
    if not os.path.isfile(p):
        return 0
    head = read_txt_head(p)
    return int(head.get("ops") or 0) if head else 0


def _file_time(path):
    try:
        m = os.stat(path).st_mtime
    except OSError:
        return "", 0
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(m)), m


def _map_ctx():
    r"""② 侧的附带状态：成品当前版本（final\<版本>\<指纹>.txt）、编辑中的包、图文件夹里的导出。

    成品「当前版本」用 _final_dir() 解析（_current.txt → 台账 current → 最后一版）。
    """
    final = {}
    cur = _final_dir()
    if cur:
        try:
            names = sorted(os.listdir(cur))
        except OSError:
            names = []
        for fn in names:
            f = os.path.join(cur, fn)
            if not EDIT_FILE_RE.match(fn) or not os.path.isfile(f):
                continue
            head = read_txt_head(f) or {}
            final[fn[:-4]] = {"has": True, "sha": sha256(f), "ops": int(head.get("ops") or 0)}
    # 编辑中：packs\<图文件夹>\<包名>\<指纹>.txt（collect_packs 已经把 ops 算好了）
    packs = {}
    for pk in collect_packs():
        folder = str(pk.get("folder") or "")
        if not folder:
            continue
        packs.setdefault(folder, []).append({
            "name": str(pk.get("name") or "").split("/")[-1],
            "full": str(pk.get("name") or ""),
            "ops": int(pk.get("ops") or 0),
            "fp": str(pk.get("fp") or ""),
            "grow": bool(pk.get("grow")),
            "keep": bool(pk.get("keep")),
            "blank": bool(pk.get("blank")),
            "created": str(pk.get("created") or ""),
        })
    # 这张图历史导出：<图文件夹>\导出\*.json（dev 才有这一层）
    exports = {}
    try:
        names = sorted(os.listdir(DEV))
    except OSError:
        names = []
    for name in names:
        if name.startswith(("_", ".")):
            continue
        d = os.path.join(DEV, name, "导出")
        if not os.path.isdir(d):
            continue
        n = 0
        for _base, _dirs, files in os.walk(d):
            n += len([f for f in files if f.lower().endswith(".json")])
        exports[name] = n
    return {"final": final, "packs": packs, "exports": exports}


def _no_of(file_name, row):
    no = str((row or {}).get("no") or "")
    if no:
        return no
    m = re.match(r"^(\d{1,3})_", file_name or "")
    return m.group(1) if m else ""


def _map_entry(file_name, path, info, row, ctx=None):
    """一条地图行：文件统计 + 索引行 + ②成品/编辑中/导出 + 自动铺设触发判断。"""
    info = info or {}
    row = row or {}
    level = str(info.get("level") or row.get("level") or "")
    # 显示名以 docs/地图对照表.md 为准（level9 隐藏图 = 飓风危城，文件仍叫 10_暴风.json）
    label = (default_names().get(level, "") or str(info.get("label") or "")
             or str(row.get("name") or ""))
    fp = str(info.get("fp") or row.get("fingerprint") or "")
    file_name = file_name or str(row.get("file") or "")
    mode, mode_order = MODE_BY_LEVEL.get(level, ("其他", 99))
    exists = bool(path and os.path.isfile(path))
    nodes = int(info.get("nodes") or row.get("nodes") or 0)
    edges = int(info.get("edges") or row.get("edges") or 0)
    features = int(info.get("features") or row.get("features") or 0)
    kinds = info.get("kinds") or {}
    crouch_aux = info.get("crouchAux") or {}
    status = "missing"
    if exists:
        status = "empty" if nodes == 0 else ("tiny" if nodes < 50 else "ok")

    # 没有地图 JSON 的关卡（胜利广场 / 死亡擂台）也要能看出有没有可走面
    nm_ok = bool(info.get("navmesh"))
    nm_file = str(info.get("navmeshFile") or "")
    if not nm_ok and level:
        nm_file, nm_ok = find_navmesh(level)

    # ② 侧：成品当前版本里有没有这张图、编辑中有哪些包、图文件夹里导出过几份
    ctx = ctx or {}
    folder = (file_name.split("/")[0] if "/" in (file_name or "")
              else (P.map_folder(level) if level else ""))
    fin = (ctx.get("final") or {}).get(fp) or {"has": False, "sha": "", "ops": 0}
    packs = (ctx.get("packs") or {}).get(folder) or []
    exports = int((ctx.get("exports") or {}).get(folder) or 0)

    return {
        "no": _no_of(file_name, row),
        "level": level,
        "label": label,
        "folder": folder,
        "dir": "maps",
        "mode": mode,
        "modeOrder": mode_order,
        "noPointGraph": level in NO_POINT_LEVELS,
        "scene": str(info.get("scene") or row.get("scene") or ""),
        "file": file_name,
        "fp": fp,
        "nodes": nodes,
        "walkable": int(info.get("walkable") or 0),
        "edges": edges,
        "features": features,
        "kinds": kinds,
        "spawnAux": info.get("spawnAux") or {},
        "crouchAux": crouch_aux,
        "jumpLinks": int(info.get("jumpLinks") or 0),
        "jumpEndpoints": int(kinds.get("jump") or 0),
        "isolated": int(info.get("isolated") or 0),
        "components": int(info.get("components") or 0),
        "degreeGt6": int(info.get("degreeGt6") or 0),
        "maxDegree": int(info.get("maxDegree") or 0),
        "support": info.get("support") or 0,
        "bbox": info.get("bbox"),
        "routes": int(info.get("routes") or 0),
        "zones": int(info.get("zones") or 0),
        "navmesh": nm_ok,
        "navmeshFile": nm_file,
        "mtime": info.get("mtime") or "",
        "mtimeTs": info.get("mtimeTs") or 0,
        "size": int(info.get("size") or 0),
        "status": status,
        # 这张图当前生效的编辑 = 成品当前版本里的条数（没有就是 0）；packs 单独列
        "editsDev": int(fin.get("ops") or 0),
        "editsNative": _edit_ops(NATIVE, fp),
        "final": fin,
        "packs": packs,
        "exports": exports,
        "auto": {
            "waypoints": nodes == 0,
            "crouch": sum(crouch_aux.values()) == 0,
            "guard": int(kinds.get("nano_area") or 0) == 0,
        },
    }


def collect_maps():
    r"""当前版本的图集：三区都读每张图文件夹里的 map.json（旧布局回退 maps\*.json）。"""
    ctx = _map_ctx()
    try:
        with open(P.index_path(DATA), "r", encoding="utf-8") as f:
            index = json.load(f)
    except (OSError, ValueError):
        index = {}
    idx_rows = {}
    for row in (index.get("maps") or []):
        if not isinstance(row, dict):
            continue
        fn = str(row.get("file") or "")
        idx_rows[fn or ("#%s" % row.get("no"))] = row

    out = []
    seen = set()
    seen_levels = set()
    for fn, p in P.map_files(DATA):
        info = _map_info(p)
        if not info or info.get("error"):
            continue
        out.append(_map_entry(fn, p, info, idx_rows.get(fn), ctx))
        seen.add(fn)
        if info.get("level"):
            seen_levels.add(str(info["level"]))
    for key, row in idx_rows.items():
        fn = str(row.get("file") or "")
        if fn and fn in seen:
            continue
        # 同一张图已经有文件了（索引里这条没写 file），别再加一行重复的
        if not fn and str(row.get("level") or "") in seen_levels:
            continue
        p = os.path.join(DATA, *fn.split("/")) if fn else ""
        out.append(_map_entry(fn, p, _map_info(p) if p else None, row, ctx))

    # 这一版没有 _index.json（① 备份版就是），按权威对照表补齐缺的图，
    # 否则下拉里会跳过 04 胜利广场、07 死亡擂台这类原生没有点图、只有可走面的关卡。
    # ③ 部署版不放数据（连图文件夹都没有）：别按对照表凭空补出 11 行
    if not out and not os.path.isfile(P.index_path(DATA)):
        return out
    have_levels = {str(e.get("level") or "") for e in out}
    have_nos = {str(e.get("no") or "") for e in out}
    for (t_no, t_lv, t_nm, t_sc, t_note) in load_map_table():
        no = "%02d" % t_no
        if t_lv in have_levels or no in have_nos:
            continue
        out.append(_map_entry("", "", None, {
            "no": no, "level": t_lv, "name": t_nm, "scene": t_sc, "note": t_note,
        }, ctx))

    def _sort(e):
        no = str(e.get("no") or "")
        m = re.match(r"^(\d+)", no)
        return (int(m.group(1)) if m else 999, e.get("level") or "")

    out.sort(key=_sort)
    return out


def _data_files(root):
    r"""{相对路径: 绝对路径} —— 图（<图>\map.json）+ 可走面 + 路线；统计 / 比对都按这个口径。"""
    out = {}
    for rel, path in list(P.map_files(root)) + list(P.navmesh_files(root)):
        out[rel] = path
    for fp, path in P.route_files(root):
        out[fp + ".txt"] = path
    return out


def _dir_version(root):
    """一版数据：图数 / 路线数 / 可走面数 / 体积 / 最近写入。"""
    files = _data_files(root)
    maps_n = len([k for k in files if k.endswith(".json")])
    nav_n = len([k for k in files if k.endswith(".txt")])
    bin_n = len([k for k in files if k.endswith(".bin")])
    total = 0
    latest = 0
    for path in files.values():
        try:
            st = os.stat(path)
        except OSError:
            continue
        total += st.st_size
        latest = max(latest, st.st_mtime)
    return {
        "path": root,
        "exists": os.path.isdir(root),
        "maps": maps_n,
        "nav": nav_n,
        "navmesh": bin_n,
        "bytes": total,
        "latest": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest)) if latest else "",
        "latestTs": latest,
    }


def _compare_data(a_root, b_root, suffix):
    """两版同一类数据比：相对路径相同且 sha256 相同 = 一致，其余列出来。"""
    fa = {k: v for k, v in _data_files(a_root).items() if k.endswith(suffix)}
    fb = {k: v for k, v in _data_files(b_root).items() if k.endswith(suffix)}
    same = 0
    diff = []
    for k in sorted(set(fa) & set(fb)):
        if sha256(fa[k]) == sha256(fb[k]):
            same += 1
        else:
            diff.append(k)
    return {
        "same": same,
        "diff": diff,
        "onlyA": sorted(set(fa) - set(fb)),
        "onlyB": sorted(set(fb) - set(fa)),
    }


def _consistency():
    def pair(a, b):
        return {"maps": _compare_data(a, b, ".json"),
                "nav": _compare_data(a, b, ".txt")}
    # ③ 已经没有地图数据，②vs③ 不再有意义；成品 / 编辑中的差别在 versions.dev 里
    return {"nativeDev": pair(NATIVE, DEV)}


def _is_pack_dir(path):
    if os.path.isfile(os.path.join(path, "manifest.json")):
        return True
    try:
        return any(re.match(r"^n\d+-[0-9a-fA-F]{16}\.txt$", fn) for fn in os.listdir(path))
    except OSError:
        return False


def collect_packs():
    """② 测试包：地图文件夹/包名、图、指纹、指令数、nogen、创建时间。"""
    out = []
    try:
        entries = sorted(os.listdir(PACKS_DIR))
    except OSError:
        return out
    ids = []
    for entry in entries:
        d = os.path.join(PACKS_DIR, entry)
        if entry.startswith("_") or not os.path.isdir(d):
            continue
        if _is_pack_dir(d):
            ids.append(entry)                       # 老布局：直接放在根目录
            continue
        try:
            subs = sorted(os.listdir(d))
        except OSError:
            continue
        for sub in subs:
            if os.path.isdir(os.path.join(d, sub)) and _is_pack_dir(os.path.join(d, sub)):
                ids.append("%s/%s" % (entry, sub))
    for name in ids:
        d = os.path.join(PACKS_DIR, *name.split("/"))
        manifest = {}
        try:
            with open(os.path.join(d, "manifest.json"), "r", encoding="utf-8") as f:
                manifest = json.load(f) or {}
        except (OSError, ValueError):
            manifest = {}
        ops = 0
        files = 0
        latest = 0
        try:
            for fn in os.listdir(d):
                if not fn.lower().endswith(".txt") or fn.lower() == "nogen.txt" or ".bak" in fn:
                    continue
                p = os.path.join(d, fn)
                if not os.path.isfile(p):
                    continue
                head = read_txt_head(p)
                if head:
                    ops += int(head.get("ops") or 0)
                    files += 1
                latest = max(latest, _file_time(p)[1])
        except OSError:
            pass
        nogen = os.path.isfile(os.path.join(d, "nogen.txt"))
        out.append({
            "name": name,
            "folder": name.split("/")[0] if "/" in name else name,
            "full": name,
            "label": str(manifest.get("label") or ""),
            "level": str(manifest.get("level") or ""),
            "fp": str(manifest.get("fp") or ""),
            "blank": bool(manifest.get("blank")),
            "grow": bool(manifest.get("grow")),
            "keep": bool(manifest.get("keep")),
            "note": str(manifest.get("note") or ""),
            "created": str(manifest.get("created") or ""),
            "files": files,
            "ops": ops,
            "nogen": nogen,
            "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest)) if latest else "",
        })
    return out


def collect_config():
    r"""工程端 run\runtime\ucf_mod.json：自动铺设三个开关和当前测试包。"""
    p = P.CFG_PATH
    out = {"path": p, "exists": os.path.isfile(p), "enabled": None,
           "scene": "", "label": "", "features": {}, "pack": {}}
    if not out["exists"]:
        return out
    try:
        with open(p, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f) or {}
    except (OSError, ValueError):
        return out
    feats = cfg.get("features") or {}
    out["enabled"] = bool(cfg.get("enabled", True))
    out["scene"] = str(cfg.get("scene") or "")
    out["label"] = str(cfg.get("label") or "")
    out["features"] = {k: bool(feats.get(k)) for k in
                       ("auto_waypoints", "auto_crouch", "ghost_areas",
                        "collect_only", "editor")}
    out["pack"] = cfg.get("pack") or {}
    return out


def collect_events(limit=24):
    """最近文件事件：地图导出、编辑清单、成品、测试包。"""
    events = []

    def _add(kind, text, path):
        t, ts = _file_time(path)
        if ts:
            events.append({"kind": kind, "text": text, "time": t, "ts": ts,
                           "file": os.path.basename(path)})

    roots = []
    if PROFILE == "native":
        roots = [("① 备份版", NATIVE)]
    else:
        roots = [("② 开发版", DEV)]
    for label, root in roots:
        # 新布局：<图>\map.json；旧布局回退 maps\*.json（P.map_files 两种都认）
        for fn, p in P.map_files(root):
            _add("地图", label + " · " + fn, p)
        # 路线清单：<图>\<指纹>.txt；旧布局 nav\*.txt（② 的成品在 final\、编辑中在 packs\）
        for _fp, p in P.route_files(root):
            head = read_txt_head(p)
            ops = int(head.get("ops") or 0) if head else 0
            _add("编辑", label + " 编辑清单 · %s · %d 条" % (os.path.basename(p), ops), p)
    if PROFILE == "final":
        # ② 的成品当前版本：final\<版本>\<指纹>.txt
        cur = _final_dir()
        if cur:
            try:
                names = sorted(os.listdir(cur))
            except OSError:
                names = []
            for fn in names:
                if EDIT_FILE_RE.match(fn):
                    _add("成品", "%s · %s" % (os.path.basename(cur), fn),
                         os.path.join(cur, fn))
    elif PROFILE == "pack":
        # ② 的编辑中：packs\<图>\<包>\<指纹>.txt
        for pk in collect_packs():
            d = os.path.join(PACKS_DIR, *pk["name"].split("/"))
            try:
                names = sorted(os.listdir(d))
            except OSError:
                names = []
            for fn in names:
                if EDIT_FILE_RE.match(fn):
                    _add("编辑中", "%s · %s" % (pk["name"], fn),
                         os.path.join(d, fn))
    for pk in collect_packs():
        d = os.path.join(PACKS_DIR, *pk["name"].split("/"))
        _add("测试包", "%s · %s · %d 条指令" % (pk["name"], pk["label"] or pk["level"], pk["ops"]),
             os.path.join(d, "manifest.json"))
    events.sort(key=lambda e: e["ts"], reverse=True)
    return events[:limit]


def _final_stats():
    r"""② 成品：几张图 / 体积 / 最近写入（dev\final，一张图一份）。

    兼容旧前端字段：versions 固定 0/1，current 固定 "final"；
    新前端应该直接看 maps（图数）。
    """
    maps_n = total = latest = 0
    try:
        names = sorted(os.listdir(FINAL))
    except OSError:
        names = []
    for fn in names:
        if not EDIT_FILE_RE.match(fn):
            continue
        f = os.path.join(FINAL, fn)
        try:
            st = os.stat(f)
        except OSError:
            continue
        maps_n += 1
        total += st.st_size
        latest = max(latest, st.st_mtime)
    return {"versions": 1 if maps_n else 0, "current": "final" if maps_n else "",
            "maps": maps_n, "bytes": total, "path": FINAL,
            "latest": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest)) if latest else ""}


def _packs_stats():
    r"""② 编辑中：包数 / 涉及的图数 / 体积 / 最近写入（packs\<图文件夹>\<包名>\<指纹>.txt）。"""
    packs = collect_packs()
    folders = set()
    total = latest = 0
    for pk in packs:
        name = str(pk.get("name") or "")
        if pk.get("folder"):
            folders.add(str(pk["folder"]))
        d = os.path.join(PACKS_DIR, *name.split("/"))
        try:
            files = sorted(os.listdir(d))
        except OSError:
            continue
        for fn in files:
            if not EDIT_FILE_RE.match(fn):       # 包里的 .bak-* 备份不算数据量
                continue
            f = os.path.join(d, fn)
            try:
                st = os.stat(f)
            except OSError:
                continue
            total += st.st_size
            latest = max(latest, st.st_mtime)
    return {"n": len(packs), "maps": len(folders), "bytes": total,
            "latest": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest)) if latest else ""}


def _inbox():
    r"""② 导出收件箱：vis\raw\**\*.json（导出）+ vis\**\navmesh*.bin（可走面）；_state / _noise 不算。"""
    exports = navmesh = 0
    total = 0
    latest = 0
    for base, dirs, files in os.walk(VIS):
        dirs[:] = [d for d in dirs if d not in ("_state", "_noise")]
        for fn in files:
            low = fn.lower()
            if low.endswith(".json") and fn not in ("names.json", "_index.json"):
                exports += 1
            elif low.startswith("navmesh") and low.endswith(".bin"):
                navmesh += 1
            else:
                continue
            p = os.path.join(base, fn)
            try:
                st = os.stat(p)
            except OSError:
                continue
            total += st.st_size
            latest = max(latest, st.st_mtime)
    return {"exports": exports, "navmesh": navmesh, "bytes": total,
            "latest": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(latest)) if latest else ""}


def build_workbench():
    dev = _dir_version(DEV)
    # ② 开发版再拆三块：成品（final）/ 编辑中（packs）/ 收件箱（vis）
    dev["final"] = _final_stats()
    dev["packs"] = _packs_stats()
    dev["inbox"] = _inbox()
    return {
        "ok": True,
        "server": "ucf-navserver/2 %s" % time.strftime("%Y-%m-%d %H:%M:%S"),
        "profile": profile_info(),
        "profiles": profile_info()["profiles"],
        "names": load_names(),
        "defaults": default_names(),
        "maps": collect_maps(),
        "versions": {
            "native": _dir_version(NATIVE),
            "dev": dev,
        },
        "packs": collect_packs(),
        "consistency": _consistency(),
        "config": collect_config(),
        "events": collect_events(),
        "log": tail_log(600),
        "logFile": log_file(),
    }


# ---------------------------------------------------------------- HTTP
class Handler(SimpleHTTPRequestHandler):
    server_version = "ucf-navserver/2"
    protocol_version = "HTTP/1.1"

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=WEB, **kw)      # 静态根 = console/web/

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

    # ---- /web/（工作台页面 + 3D 查看器 + 静态资源） ----
    MIME = {
        ".html": "text/html; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript; charset=utf-8",
        ".json": "application/json; charset=utf-8",
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".woff2": "font/woff2",
        ".ico": "image/x-icon",
    }

    def redirect(self, where):
        body = ("<!doctype html><meta charset=utf-8><a href=\"%s\">%s</a>" % (where, where)).encode("utf-8")
        self.send_response(302)
        self.send_header("Location", where)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        try:
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def serve_web(self, rel):
        """只允许 console/web/ 目录内的文件，挡住 .. 和绝对路径。"""
        rel = unquote(rel or "").replace("\\", "/").lstrip("/")
        full = os.path.abspath(os.path.join(WEB, *[x for x in rel.split("/") if x]))
        if os.path.commonpath([os.path.abspath(WEB), full]) != os.path.abspath(WEB):
            return self.send_json({"ok": False, "error": "路径越界: " + rel}, 400)
        if not os.path.isfile(full):
            return self.send_json({"ok": False, "error": "没有 " + rel}, 404)
        ext = os.path.splitext(full)[1].lower()
        with open(full, "rb") as f:
            body = f.read()
        return self.send_bytes(body, self.MIME.get(ext, "application/octet-stream"))

    # ---- GET ----
    def do_GET(self):
        # 版本切换会改内存里的 MAPS/NAV；整请求加锁，避免半切换状态
        with VIEW_LOCK:
            return self._do_GET()

    def _do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        path = u.path
        if path in ("/", "/index.html"):
            return self.redirect("/web/nav-studio.html")
        if path in ("/studio", "/studio/", "/studio.html"):
            return self.redirect("/web/nav-studio.html")
        # 旧入口兼容：2026-11-19 前端从 design/ 挪到 workbench/，2026-11-23 再收进 console/web/
        if path.startswith("/workbench/"):
            return self.redirect("/web/" + path[len("/workbench/"):])
        if path.startswith("/web/"):
            return self.serve_web(path[len("/web/"):])
        try:
            if path == "/api/maps":
                index = {}
                try:
                    ip = P.index_path(DATA)
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
                    "profile": profile_info(),
                })
            if path == "/api/profile":
                # 只读查看的“版本切换”：只改内存里读哪套 maps/nav，不写文件
                want = (q.get("set") or [""])[0]
                if want:
                    return self.send_json({"ok": True, "profile": set_profile(want)})
                return self.send_json({"ok": True, "profile": profile_info()})
            if path == "/api/workbench":
                # 七页只读工作台：一次拿齐地图统计 / 数据档 / 测试包 / 配置 / 事件 / 日志
                return self.send_json(build_workbench())
            if path == "/api/studio":
                # 工作台启动时一次性拿齐：版本 / 图列表 / 编辑清单 / 地形 / 日志
                index = {}
                try:
                    ip = P.index_path(DATA)
                    if os.path.isfile(ip):
                        with open(ip, "r", encoding="utf-8") as f:
                            index = json.load(f)
                except Exception:
                    index = {}
                return self.send_json({
                    "ok": True,
                    "ucf": UCF,
                    "profile": profile_info(),
                    "names": load_names(),
                    "defaults": default_names(),
                    "mapIndex": index,
                    "snapshots": list_snapshots(),
                    "edits": list_edits(),
                    "geo": list_geo(),
                    "log": tail_log(120),
                    "server": "ucf-navserver/2 %s" % time.strftime("%Y-%m-%d %H:%M:%S"),
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
                fn = safe_relpath((q.get("file") or [""])[0])
                # dir: maps（图集）/ nav（旧路线目录）/ packs（编辑中）/ vis（收件箱）
                base = {"maps": MAPS, "nav": NAV, "packs": PACKS_DIR}.get(kind, VIS)
                p = os.path.join(base, *[x for x in fn.split("/") if x])
                if os.path.commonpath([os.path.abspath(base), os.path.abspath(p)]) != os.path.abspath(base):
                    return self.send_json({"ok": False, "error": "路径越界: " + fn}, 400)
                if not os.path.isfile(p):
                    return self.send_json({"ok": False, "error": "文件不存在: " + fn}, 404)
                with open(p, "rb") as f:
                    return self.send_bytes(f.read(), "application/json; charset=utf-8")
            if path == "/api/txt":
                fp = safe_token((q.get("fp") or [""])[0])
                # 路线清单：图文件夹 → ② 成品当前版本 → ② 编辑中的包 → 旧布局 nav\
                p = _route_txt(DATA, fp) or os.path.join(NAV, fp + ".txt")
                if not os.path.isfile(p):
                    return self.send_json({"ok": True, "fp": fp, "text": "", "exists": False})
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    return self.send_json({"ok": True, "fp": fp, "text": f.read(), "exists": True})
            if path == "/api/pack-txt":
                name = (q.get("name") or [""])[0].replace("\\", "/")
                fp = safe_token((q.get("fp") or [""])[0])
                parts = [safe_token(x) for x in name.split("/") if x]
                # 包 id = 地图文件夹(可中文)/包名(英文)；只给包名时按尾名找
                ok = (1 <= len(parts) <= 2 and FP_RE.match(fp or ""))
                if ok and len(parts) == 1:
                    # 一张图一个草稿：一级就是地图文件夹（允许中文）
                    ok = (bool(SAFE_FOLDER_RE.match(parts[0])) and
                          parts[0] not in (".", ".."))
                elif ok:
                    ok = (bool(PACK_NAME_RE.match(parts[1])) and
                          bool(SAFE_FOLDER_RE.match(parts[0])) and
                          parts[0] not in (".", ".."))
                if not ok:
                    return self.send_json({"ok": False, "error": "包名或指纹格式不对"}, 400)
                pdir = os.path.join(PACKS_DIR, *parts)
                if not os.path.isdir(pdir) and len(parts) == 1:
                    tail = parts[0]
                    for d in os.listdir(PACKS_DIR) if os.path.isdir(PACKS_DIR) else []:
                        cand = os.path.join(PACKS_DIR, d, tail)
                        if os.path.isdir(cand):
                            pdir = cand
                            break
                p = os.path.join(pdir, fp + ".txt")
                if not os.path.isfile(p):
                    return self.send_json({"ok": True, "name": name, "fp": fp,
                                           "text": "", "exists": False})
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    return self.send_json({"ok": True, "name": name, "fp": fp,
                                           "text": f.read(), "exists": True})
            if path == "/api/backups":
                return self.send_json({"ok": True, "items": list_backups(safe_token((q.get("fp") or [""])[0]))})
            if path == "/api/geo":
                level = safe_token((q.get("level") or [""])[0])
                if not level:
                    return self.send_json({"ok": False, "error": "缺少 level"}, 400)
                p = os.path.join(GEOWEB, level + ".bin")
                if not os.path.isfile(p) and (q.get("build") or [""])[0] in ("1", "true"):
                    try:
                        _geo = P.tool("geo2web.py")
                        subprocess.run([sys.executable, _geo, level],
                                       cwd=os.path.dirname(_geo), timeout=120, capture_output=True)
                    except Exception as exc:
                        return self.send_json({"ok": False, "error": "生成失败: %s" % exc}, 500)
                if not os.path.isfile(p):
                    return self.send_json({
                        "ok": False,
                        "error": "没有 %s 的网格缓存，先跑 tools/geo/geo2web.py %s" % (level, level),
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
            if path == "/api/tex":
                level = safe_token((q.get("level") or [""])[0])
                name = os.path.basename((q.get("name") or [""])[0] or "")
                if not level or not name or not name.lower().endswith(".png"):
                    return self.send_json({"ok": False, "error": "缺少 level/name"}, 400)
                p = os.path.join(GEOTEX, level, name)
                if not os.path.isfile(p):
                    return self.send_json({"ok": False, "error": "没有这张贴图：%s" % name}, 404)
                with open(p, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "max-age=600")
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                return
            if path == "/api/navmesh":
                level = safe_token((q.get("level") or [""])[0])
                if not level:
                    return self.send_json({"ok": False, "error": "缺少 level"}, 400)
                p = navmesh_for(level)
                if not p:
                    return self.send_json({
                        "ok": False, "level": level,
                        "error": "没有 %s 的可走面导出（这张图没有 NavMeshGraph，或还没进过图）" % level,
                    }, 404)
                with open(p, "rb") as f:
                    body = f.read()
                if (q.get("info") or [""])[0] in ("1", "true"):
                    return self.send_json({
                        "ok": True, "level": level, "file": os.path.basename(p),
                        "bytes": len(body), "native_verts": NATIVE_VERTS.get(level),
                    })
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
        # 2026-11-18 起网页端只读：所有写接口已移除，统一返回 405。
        return self.send_json({"ok": False, "error": "只读服务，不提供写入接口"}, 405)


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
    # 2026-11-18 起只有一个只读入口；--studio 保留为无操作，防旧快捷方式报错。
    url = "http://127.0.0.1:%d/web/nav-studio.html" % port
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    srv.daemon_threads = True
    print("UCF 路点工作台 · 本地服务（只读查看）")
    print("  数据档   : %s（%s）%s" % (
        profile_info()["cn"], PROFILE, "  [只读]" if READONLY else ""))
    print("  档位切换 : /api/profile?set=native|final|pack（旧 dev/deploy/test 仍兼容）")
    print("  数据目录 : %s（每张图一个文件夹）" % DATA)
    print("  原生备份 : %s" % NATIVE)
    print("  游戏目录 : %s（运行目录，不放导航数据）" % UCF)
    print("  收件箱   : %s（② 的 vis\\：导出 / 可走面）" % VIS)
    print("  成品     : %s（② 的 final\\：一张图一份）" % FINAL)
    print("  测试包   : %s（② 的 packs\\：编辑中）" % PACKS_DIR)
    print("  打开地址 : %s" % url)
    print("  （关掉这个窗口就停止服务；本服务只读，不写任何路线数据）")
    for name in ("snapshots", "edits", "geo"):
        print("  %-10s %d" % (name, len({"snapshots": list_snapshots, "edits": list_edits, "geo": list_geo}[name]())))
    if not list_geo():
        print("  !! geo/web 是空的：3D 视图只能画路点。跑一次 tools/geo/geo2web.py 生成网格。")
    if "--no-browser" not in sys.argv:
        threading.Thread(target=lambda: (time.sleep(0.4), webbrowser.open(url)), daemon=True).start()
    # 自动归档默认关闭（2026-11-17）：它会在后台跑 organize_maps，把 maps/ 里的文件
    # 当「可疑/太小」搬去 _suspect/，和我们「原生备份只读」的约定打架。
    # 需要时手动跑：python tools/data/organize_maps.py --archive
    if "--auto-organize" in sys.argv:
        threading.Thread(target=auto_organize_loop, daemon=True).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()