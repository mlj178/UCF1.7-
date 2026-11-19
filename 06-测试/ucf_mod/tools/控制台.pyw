#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UCF 控制台 —— ucf_mod.json 的可视化开关面板

为什么要有它：ucf_mod 的功能开关以前散落成 collect.flag / nav\nogen.txt 之类
的标记文件，而且 ucf_mod.json 压根没被读。现在整份配置只有一个文件，
这个窗口就是它的人话界面：勾选即写盘，游戏下次启动生效。

启动游戏时会带上环境变量 UCF_MOD=1 —— 插件看到它才工作；
直接双击 UnityCrossFire.exe 没有这枚令牌，插件立刻返回，游戏就是原版。

只依赖 customtkinter（本机已有 5.2.2），不联网、不监听端口。
"""
import hashlib
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from ucf_paths import DEPLOY, DEV, NATIVE, TEST, PACKS_DIR  # noqa: E402  四版里的四个根

CFG_PATH = os.path.join(DEPLOY, "ucf_mod.json")
LOG_PATH = os.path.join(DEPLOY, "ucf_mod.log")
AUTOTEST_TXT = os.path.join(DEPLOY, "autotest.txt")   # 车测：每张图 OK + 最后 RESULT 写这里
MAP_MD = os.path.join(os.path.dirname(HERE), "docs", "地图对照表.md")
GAME_EXE = os.path.join(os.path.dirname(DEPLOY), "UnityCrossFire.exe")
NAVSERVER = os.path.join(HERE, "navserver.py")
NAVDATA = os.path.join(HERE, "navdata.py")     # 数据版本命令（部署/还原/校验/状态）
TIDY = os.path.join(HERE, "tidy_vis.py")       # 整理 ④ vis：raw/<地图>/ + navmesh/ + _state/
PACKS = PACKS_DIR                              # ④ 测试包：<包名>\<指纹>.txt + manifest.json
TEST_VIS = os.path.join(TEST, "vis")           # ④ 导出收件箱（和递给游戏的那个路径一致）
NAVCMD = os.path.join(DEPLOY, "ucf_navcmd.txt")  # 运行中命令：插件每 ~0.5 s 查一次 seq
_CMD_SEQ = 0


def load_maps():
    r"""[(level, 中文名, 指纹)] —— 指纹来自 maps\*.json（游戏自己扫出来的，不能手猜）。

    部署端没有 maps\ 时退回开发版（同一套文件，内容一致）。
    暴风（level9）原生 0 点、没有指纹，运行时就是 n0-0000000000000000。
    """
    out, seen = [], set()
    for d in (os.path.join(DEPLOY, "maps"), os.path.join(DEV, "maps")):
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or fn.startswith("_"):
                continue
            try:
                with open(os.path.join(d, fn), "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, ValueError):
                continue
            m = doc.get("map") or {}
            lv = str(m.get("level") or "")
            if not lv or lv in seen:
                continue
            fp = str(m.get("fingerprint") or "")
            if not fp and lv == "level9":
                fp = "n0-0000000000000000"
            if not fp:
                continue                      # 没指纹 = 这张图没有路点图，测不了
            seen.add(lv)
            out.append((lv, str(m.get("label") or m.get("scene") or lv), fp))
    out.sort(key=lambda r: int("".join(ch for ch in r[0] if ch.isdigit()) or 0))
    return out


def find_map_doc(fp):
    r"""(doc, path) —— 按指纹找地图 JSON；部署端优先，退回开发版。

    人机路点页用它算节点 / 边 / 出生点数量；不写任何文件。
    """
    if not fp:
        return None, ""
    for d in (os.path.join(DEPLOY, "maps"), os.path.join(DEV, "maps")):
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or fn.startswith("_"):
                continue
            path = os.path.join(d, fn)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, ValueError):
                continue
            if str((doc.get("map") or {}).get("fingerprint") or "") == fp:
                return doc, path
    return None, ""


def load_scene_counts():
    r"""{level: {jump, crouch, guard, area, tag}} —— 读《地图对照表》第二张表。

    地图 JSON 是运行期导出（只有 PointGraph + spawn/tag），
    守点/聚集区/蹲点只在场景组件统计里，所以页签显示以这张表为准。
    """
    out = {}
    try:
        with open(MAP_MD, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return out

    def num(text):
        try:
            return int("".join(ch for ch in str(text) if ch.isdigit()) or 0)
        except ValueError:
            return 0

    for line in lines:
        s = line.strip()
        if not s.startswith("| level"):
            continue
        parts = [x.strip() for x in s.strip("|").split("|")]
        if len(parts) < 11:
            continue
        out[parts[0]] = {
            "name": parts[1], "scene": parts[2],
            "jump": num(parts[3]), "nodelink": num(parts[4]),
            "nodelink2": num(parts[5]), "crouch": num(parts[6]),
            "guard": num(parts[7]), "area": num(parts[8]), "tag": num(parts[9]),
        }
    return out


def pack_name_ok(name):
    r"""包名只能用英文字母、数字、下划线、短横线（插件是 C + ANSI 路径，中文读不了）。"""
    return bool(re.match(r"^[A-Za-z0-9_-]{1,48}$", name or ""))


def pack_id_ok(pid):
    r"""包 id = 地图文件夹/包名：文件夹允许中文（如 TransportShip运输船），包名仍只认英文。"""
    parts = [s for s in str(pid or "").replace("\\", "/").split("/") if s]
    if not (1 <= len(parts) <= 2):
        return False
    if len(parts) == 1:
        return pack_name_ok(parts[0])            # 老布局：根目录平铺的包名
    folder, name = parts
    if not pack_name_ok(name):
        return False
    return (bool(re.match(r'^[^\\/:*?"<>|]{1,30}$', folder))
            and folder not in (".", ".."))


def pack_dir(pid):
    r"""包 id → 目录：TransportShip/blank_b → packs\TransportShip\blank_b。

    老布局（packs\blank_b，没分类）也认，旧包和自检脚本还能直接用。
    """
    return os.path.join(PACKS, *[s for s in str(pid).replace("\\", "/").split("/") if s])


def _is_pack_dir(path):
    r"""目录里有没有包的内容：manifest.json 或 <指纹>.txt。"""
    if os.path.isfile(os.path.join(path, "manifest.json")):
        return True
    try:
        return any(re.match(r"^n\d+-[0-9a-fA-F]{16}\.txt$", fn)
                   for fn in os.listdir(path))
    except OSError:
        return False


def map_scene(lv, fp=""):
    r"""地图英文场景名（默认包名前缀用）：maps\*.json 的 scene，缺了查《地图对照表》。"""
    doc, _p = find_map_doc(fp)
    scene = str(((doc or {}).get("map") or {}).get("scene") or "")
    if not scene:
        scene = str((load_scene_counts().get(lv) or {}).get("scene") or "")
    scene = re.sub(r"[^A-Za-z0-9_-]+", "_", scene).strip("_-")
    return scene or str(lv or "blank")


def map_folder(lv, fp=""):
    r"""测试包文件夹名：英文场景名 + 中文名，如 TransportShip运输船。

    Windows 文件系统支持中英混排；插件的 ANSI 路径在本机（代码页 936）能读中文，
    所以目录用「英文+中文」，包名仍用英文（navcmd / 日志更稳）。
    """
    doc, _p = find_map_doc(fp)
    m = (doc or {}).get("map") or {}
    scene = str(m.get("scene") or "")
    label = str(m.get("label") or "")
    if not scene or not label:
        row = load_scene_counts().get(lv) or {}
        scene = scene or str(row.get("scene") or "")
        label = label or str(row.get("name") or "")
    base = "%s%s" % (scene or lv or "blank", label)
    base = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", base).strip(" .")
    return base or str(lv or "blank")


def pack_manifest(pid):
    r"""读 packs/<地图文件夹>/<包名>/manifest.json；没有就返回空 dict。"""
    try:
        with open(os.path.join(pack_dir(pid), "manifest.json"), "r", encoding="utf-8") as f:
            doc = json.load(f)
        return doc if isinstance(doc, dict) else {}
    except (OSError, ValueError):
        return {}


def pack_txt(pid, fp=""):
    r"""包内某张图的 txt；不给指纹就取第一个。"""
    d = pack_dir(pid)
    if fp:
        p = os.path.join(d, fp + ".txt")
        return p if os.path.isfile(p) else ""
    try:
        files = sorted(fn for fn in os.listdir(d) if fn.endswith(".txt") and not fn.startswith("_"))
    except OSError:
        return ""
    return os.path.join(d, files[0]) if files else ""


def pack_target_fp(pid):
    r"""这个包针对哪张图：manifest.fp 优先，其次 <指纹>.txt 的文件名。"""
    fp = str(pack_manifest(pid).get("fp") or "")
    if fp:
        return fp
    p = pack_txt(pid)
    if p:
        base = os.path.basename(p)[:-4]
        if re.match(r"^n\d+-[0-9a-fA-F]{16}$", base):
            return base
    return ""


def seed_lines(fp):
    r"""从 ① 备份版 maps/*.json 生成「原版全量重放」行（node add + edge add）。

    给 grow 包做底：等于把这张图的原版点图整份复制过来，之后可以继续加点，
    不受原生点数限制（插件会先把原生点全标死，再按这些行新建节点）。
    """
    d = os.path.join(NATIVE, "maps")
    if not os.path.isdir(d):
        return None, 0, 0
    doc = None
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        try:
            with open(os.path.join(d, fn), "r", encoding="utf-8") as f:
                cur = json.load(f)
        except (OSError, ValueError):
            continue
        if str((cur.get("map") or {}).get("fingerprint") or "") == fp:
            doc = cur
            break
    if not doc:
        return None, 0, 0
    nodes = [n for n in (doc.get("nodes") or []) if int(n.get("walk", 1)) != 0]
    pos = {}
    for n in nodes:
        p = n.get("p") or (0.0, 0.0, 0.0)
        pos[str(n.get("id"))] = tuple(float(v) for v in p)
    lines = ["node add %.3f %.3f %.3f" % pos[k] for k in pos]
    seen, edges = set(), []
    for e in doc.get("edges") or []:
        if len(e) < 2:
            continue
        a, b = str(e[0]), str(e[1])
        if a == b or a not in pos or b not in pos:
            continue
        k = (a, b) if a < b else (b, a)
        if k in seen:
            continue
        seen.add(k)
        edges.append(k)
    for a, b in edges:
        lines.append("edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (pos[a] + pos[b]))
    return lines, len(pos), len(edges)


def pack_summary(pid, fp=""):
    r"""包内容摘要：空白底图？几个加点 / 删点 / 加边 / 删边、最后写入时间。"""
    p = pack_txt(pid, fp)
    out = {"path": p, "blank": False, "grow": False, "nadd": 0, "ndel": 0,
           "eadd": 0, "edel": 0, "mtime": 0.0}
    if not p:
        return out
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for ln in f:
                s = ln.strip()
                if not s or s.startswith("#"):
                    continue
                if s == "blank":
                    out["blank"] = True
                elif s == "grow":
                    out["grow"] = True       # blank 的加强版：新增节点，不借槽位
                elif s.startswith("node add "):
                    out["nadd"] += 1
                elif s.startswith("node del "):
                    out["ndel"] += 1
                elif s.startswith("edge "):
                    bits = s.split()
                    verb = bits[1] if len(bits) > 1 else ""
                    if verb in ("add", "out", "in"):
                        out["eadd"] += 1
                    elif verb in ("del", "delout", "delin"):
                        out["edel"] += 1
        out["mtime"] = os.stat(p).st_mtime
    except OSError:
        pass
    return out


def write_nav_cmd(cmd, name="", fp="", extra=None):
    r"""给运行中的插件写一条命令（原子替换，插件不会读到半截文件）。

    seq 必须单调递增：同一毫秒点两下也不能被插件当成同一条。
    extra 是附加行（例如 brush=normal / menu=on），插件按 key=value 读。
    """
    global _CMD_SEQ
    ms = int(time.time() * 1000)
    _CMD_SEQ = ms if ms > _CMD_SEQ else (_CMD_SEQ + 1)
    lines = ["seq=%d" % _CMD_SEQ, "cmd=%s" % cmd]
    if name:
        lines.append("pack=%s" % name)
    if fp:
        lines.append("fp=%s" % fp)
    for key, value in (extra or {}).items():
        if value is None or value == "":
            continue
        lines.append("%s=%s" % (key, value))
    d = os.path.dirname(NAVCMD)
    if d:
        os.makedirs(d, exist_ok=True)
    tmp = NAVCMD + ".tmp"
    # 包 id 里可能带中文地图文件夹；插件是 ANSI(GBK) 文件路径，命令文件也按 GBK 写。
    with open(tmp, "w", encoding="gbk", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, NAVCMD)
    return _CMD_SEQ


def load_packs():
    r"""packs\ 下所有测试包 id：地图文件夹/包名（老布局的 packs\<包名> 也算，排后面）。"""
    out = []
    try:
        entries = sorted(os.listdir(PACKS))
    except OSError:
        return out
    for entry in entries:
        if entry.startswith("_"):
            continue
        d = os.path.join(PACKS, entry)
        if not os.path.isdir(d):
            continue
        if _is_pack_dir(d):
            out.append(entry)                      # 老布局：直接放在根目录
            continue
        try:
            subs = sorted(os.listdir(d))
        except OSError:
            continue
        for sub in subs:
            sd = os.path.join(d, sub)
            if sub.startswith("_") or not os.path.isdir(sd):
                continue
            if _is_pack_dir(sd):
                out.append("%s/%s" % (entry, sub))
    return out


def migrate_flat_packs():
    r"""把老的 packs\<包名>\ 自动挪进 packs\<地图文件夹>\<包名>\；返回 [(旧, 新)]。

    文件夹名用地图英文场景名（插件是 C + ANSI 路径，读不了中文目录）。
    目标已存在就原地不动，绝不覆盖。
    """
    moved = []
    try:
        entries = sorted(os.listdir(PACKS))
    except OSError:
        return moved
    for entry in entries:
        d = os.path.join(PACKS, entry)
        if entry.startswith("_") or not os.path.isdir(d) or not _is_pack_dir(d):
            continue
        man = pack_manifest(entry)                # 老布局按平铺名字读
        fp = str(man.get("fp") or "")
        if not fp:
            fp = pack_target_fp(entry)
        folder = map_folder(str(man.get("level") or ""), fp)
        dst = os.path.join(PACKS, folder, entry)
        if os.path.abspath(dst) == os.path.abspath(d) or os.path.isdir(dst):
            continue
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(d, dst)
        except OSError:
            continue
        moved.append((entry, "%s/%s" % (folder, entry)))
    return moved

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


def dir_stats(root):
    r"""maps/ nav/ vis/ 三个子目录加起来的 (文件数, 字节数, 最新写入时间)。"""
    n = total = 0
    latest = 0.0
    for sub in ("maps", "nav", "vis"):
        d = os.path.join(root, sub)
        for fn in _listdir(d):
            p = os.path.join(d, fn)
            try:
                st = os.stat(p)
            except OSError:
                continue
            if not os.path.isfile(p):
                continue
            n += 1
            total += st.st_size
            latest = max(latest, st.st_mtime)
    return n, total, latest


def latest_export(root):
    r"""vis/ 里最新写入的导出 JSON（递归 raw/，忽略 _seen_ 标记与 navmesh）。
    返回 (文件名, 完整路径, 修改时间戳)；没有则 None。"""
    d = os.path.join(root, "vis")
    best = None
    for base, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ("navmesh", "_state", "_noise")]
        for fn in files:
            if fn.startswith("_seen_") or not fn.endswith(".json"):
                continue
            p = os.path.join(base, fn)
            try:
                st = os.stat(p)
            except OSError:
                continue
            if not os.path.isfile(p):
                continue
            if best is None or st.st_mtime > best[2]:
                best = (fn, p, st.st_mtime)
    return best


def vis_raw_dir(root):
    r"""新结构优先打开 vis\raw（按地图分好）；旧结构回退 vis 根。"""
    raw = os.path.join(root, "vis", "raw")
    return raw if os.path.isdir(raw) else os.path.join(root, "vis")


def data_counts(root):
    r"""(地图数, 编辑文件数, 编辑条数, 可走面数)。"""
    maps = len([f for f in _listdir(os.path.join(root, "maps"))
                if f.endswith(".json") and not f.startswith("_")])
    files = lines = 0
    for fn in _listdir(os.path.join(root, "nav")):
        if not fn.endswith(".txt"):
            continue
        files += 1
        try:
            with open(os.path.join(root, "nav", fn), "r", encoding="utf-8", errors="replace") as f:
                lines += len([ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")])
        except OSError:
            pass
    bins = 0
    for _base, _dirs, vis_files in os.walk(os.path.join(root, "vis")):
        bins += len([f for f in vis_files if f.startswith("navmesh_") and f.endswith(".bin")])
    return maps, files, lines, bins


def test_stats(root):
    r"""④ 测试版：(导出 JSON 数, 可走面数, 测试包数, 字节数, 最新写入时间)。"""
    vis = os.path.join(root, "vis")
    n_json = n_bin = total = 0
    latest = 0.0
    for base_dir, dirs, files in os.walk(vis):
        dirs[:] = [x for x in dirs if x not in ("_state", "_noise")]
        for fn in files:
            p = os.path.join(base_dir, fn)
            try:
                st = os.stat(p)
            except OSError:
                continue
            if not os.path.isfile(p):
                continue
            total += st.st_size
            latest = max(latest, st.st_mtime)
            if fn.startswith("navmesh_") and fn.endswith(".bin"):
                n_bin += 1
            elif fn.endswith(".json"):
                n_json += 1
    packs = 0
    pk_dir = os.path.join(root, "packs")
    try:
        for entry in os.listdir(pk_dir):
            d = os.path.join(pk_dir, entry)
            if not os.path.isdir(d):
                continue
            if _is_pack_dir(d):
                packs += 1
                continue
            for sub in _listdir(d):
                if os.path.isdir(os.path.join(d, sub)) and _is_pack_dir(os.path.join(d, sub)):
                    packs += 1
    except OSError:
        pass
    return n_json, n_bin, packs, total, latest


def tree_hashes(root):
    r"""maps/*.json（去掉 _index.json）+ nav/*.txt 的 sha1：判断两版是不是同一份数据。
    名字注册表 names.json 与自动生成的 INDEX.md 不算（格式差异不影响游戏）。"""
    out = {}
    for sub, want in (("maps", ".json"), ("nav", ".txt")):
        d = os.path.join(root, sub)
        for fn in _listdir(d):
            if not fn.endswith(want) or fn.startswith("_"):
                continue
            try:
                with open(os.path.join(d, fn), "rb") as f:
                    out[sub + "/" + fn] = hashlib.sha1(f.read()).hexdigest()
            except OSError:
                pass
    return out


def diff_count(a, b):
    keys = set(a) | set(b)
    return sum(1 for k in keys if a.get(k) != b.get(k))


CREATE_NO_WINDOW = 0x08000000
FONT = ("Microsoft YaHei UI", 13)
FONT_S = ("Microsoft YaHei UI", 12)
FONT_B = ("Microsoft YaHei UI", 15, "bold")

# ---- 开关定义：(key, 标题, 说明, 默认值) --------------------------------
GROUPS = [
    ("地图", "房间选图列表里要不要多一张「暴风」；关掉后就是原版列表", [
        ("hidden_map", "加载暴风地图", "把隐藏图 Nano30_Storm 插进房间下拉框；关掉后选不到暴风", True),
    ]),
    # 2026-11-19 用户要求：可视化按数据类别拆成勾选框，一颗开关同时管「读不读」和「画不画」；
    # 总开关（visualizer）排在本页顶部。「导出」页那 6 个 export_* 是另一套，互不影响。
    ("可视化", "进图时读什么、画什么都在这一页；关掉哪类就不读也不画（不影响 Ctrl+E 导出）", [
        ("visualizer", "可视化总开关（Visualizer）", "整套彩色点线的总开关；关掉后进图不画（可走面独立，不受影响）；Ctrl+V 随时开关", False),
        ("vis_nodes", "路点 / 连线（PointNode / Connection）", "浅蓝点 = 普通路点，橙点 = 带标签，红点 = 禁走点；蓝线 = 连线", True),
        ("vis_crouch", "蹲守点（Bot_CrouchPos）", "红色实心小方块（两阵营同色）", True),
        ("vis_guard", "守卫区 / 守卫点（Bot_GuardArea / Bot_GuardPos）", "紫色线框区 + 橙色实心点", True),
        ("vis_nano", "幽灵守区 / 幽灵守点（Bot_NanoGuardArea / Bot_NanoGuardPos）", "绿色线框区 + 青色实心点", True),
        ("vis_born", "出生点（SpawnPoint）", "潜伏者(蓝)/保卫者(红)/中立点(灰)；个人竞技用中立点、全员敌对；生化/剑客与补给箱混布，叠色偏粉紫", True),
        ("vis_supply", "补给箱（SupplyBox / RedBox / BlueBox）", "金/粉/青实心高柱 = 补给/红/蓝", True),
        ("vis_jump", "跳点（Bot_JumpLink）", "黄色连线（没有点标记）", True),
        ("vis_tag", "标签区（PointNodeTagModifier）", "橙色线框小方块", True),
        ("navmesh_show", "可走面（NavMeshGraph）", "绿色三角网线框（人机真正在上面跑的面）；Ctrl+Shift+6 随时开关；与可视化总开关无关", True),
    ]),
    # 2026-11-18：导出单独成页 —— 一个总开关 + 六项内容，默认全勾
    ("导出", "Ctrl+E 导出的总开关与内容（与可视化开关互相独立）", [
        ("export_enabled", "启用导出", "总开关；关掉后下面勾选全部不生效，Ctrl+E 不读也不写", True),
        ("export_nodes", "路点 / 连线", "JSON 主体；关掉后只导特征点（文件名 f<特征数>，不写 _seen 去重）", True),
        ("export_crouch", "人类蹲守点", "读人类蹲守点；关掉后 JSON 里 crouch=0", True),
        ("export_area", "幽灵守区 / 守点", "读幽灵守区与幽灵守点；关掉后 nano_area/nano_pos=0", True),
        ("export_guard", "守卫区 / 守卫点", "读守卫区与守卫点；关掉后 guard=0", True),
        ("export_spawn", "出生点 / 补给箱", "读出生点与补给箱；关掉后 spawn=0", True),
        ("export_tags", "跳点 / 标签区", "读跳点与标签区；关掉后 jump/tag=0", True),
    ]),
    # 2026-11-19：文字标签控件已删除；这一页保留游戏内热键速查。
    ("快捷键", "游戏内热键速查（屏幕不再显示数据面板和文字标签）", []),
    # 2026-11-19 用户要求：删除「自动铺设」整块（auto_waypoints / auto_crouch / ghost_areas）。
    # 2026-11-19 用户要求：删除「允许游戏内编辑」（editor），C 侧键保留（默认开）。
    # 2026-11-19 用户要求：整个「手动」页删除（collect_only 入口随之去掉，功能仍可用
    # collect.flag / Ctrl+Shift+X）。
]

# 「可视化」页各类数据的图例色块：游戏里画成什么颜色（照抄 src/editor.c 的 COL_* 与 vis_draw）。
# 顺序与 GROUPS 里各项的说明文字一一对应；C 侧改颜色这里要一起改。
VIS_COLORS = {
    "vis_nodes": ("#CCE0FF", "#FF8C0D", "#FF261F", "#4073F2"),
    "vis_crouch": ("#FF261F",),
    "vis_guard": ("#BF59FF", "#FF8C0D"),
    "vis_nano": ("#1AFF40", "#1AF2F2"),
    "vis_born": ("#2666FF", "#FF261F", "#B3B3B3"),
    "vis_supply": ("#FFD933", "#FF59B3", "#1AF2F2"),
    "vis_jump": ("#FFE00D",),
    "vis_tag": ("#FF8C0D",),
    "navmesh_show": ("#26FF8C",),
}

# 游戏内热键速查（控制台专用文档；游戏里不再显示这块）。按功能分组，组间空一行。
HUD_KEYS = (
    "【可视化】\n"
    "Ctrl+V 可视化总开关   Ctrl+Shift+6 可走面\n"
    "\n"
    "【导出与采集】\n"
    "Ctrl+E 手动导出   Ctrl+Shift+X 只读采集（不创建对象）\n"
    "\n"
    "【标记】\n"
    "Delete 删除准星最近标记   Ctrl+0 显示/隐藏已放标记\n"
    "\n"
    "【编辑模式】\n"
    "Ctrl+1 编辑模式   Ctrl+2 放蹲守点   Ctrl+4 建守卫区\n"
    "Ctrl+5 撤销   Ctrl+6 保存   Ctrl+7 重载   Ctrl+8 阵营   Ctrl+9 状态写日志\n"
    "\n"
    "【路点编辑（Ctrl+Shift+字母）】\n"
    "Ctrl+Shift+A 选A点   Ctrl+Shift+N 加点   Ctrl+Shift+J A↔点 连/断\n"
    "Ctrl+Shift+D 禁用点   Ctrl+Shift+Z 撤销   Ctrl+Shift+S 手动保存   Ctrl+Shift+R 重套用\n"
    "\n"
    "【F2 路点菜单】\n"
    "F2 开关 / 长按 E 备用\n"
    "1-9 直选   小键盘 8/2 上下   5 确认   0 返回   左键确认 / 右键返回"
)

HUD_NOTES = (
    "· 游戏内数据面板和文字标签已删除；节点/守区等计数看 ucf_mod.log 里的 [vis] 行，"
    "或控制台「上次运行」日志框。"
)


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


def game_running():
    try:
        out = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq UnityCrossFire.exe", "/NH"],
            capture_output=True, text=True, errors="replace", timeout=5,
            creationflags=CREATE_NO_WINDOW)
        return "UnityCrossFire.exe" in (out.stdout or "")
    except Exception:
        return False


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
        if not game_running():
            return True
        time.sleep(0.3)
    return not game_running()


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


_MAP_ROW = re.compile(r"^\|\s*\d{1,3}\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|")
_LEVELS_FALLBACK = [
    ("level1", "运输船"), ("level2", "小型工厂"), ("level3", "椰岛之巅"),
    ("level4", "胜利广场"), ("level5", "竞技场"), ("level6", "刀锋寨"),
    ("level7", "沙漠要塞"), ("level8", "生化酒店"), ("level9", "暴风"),
    ("level10", "新寂静村"), ("level11", "死亡擂台"),
]


# 车测页底部的「车测是干什么的」：用户不熟车测，按「能 / 不能 / 注意」逐条列清楚
AT_CAN = [
    ("1. 崩溃回归（主用途）", "改完 DLL 跑一遍，没有 !!! crash = 没破坏加载链路；崩了日志里有崩溃栈"),
    ("2. 采数据", "进图时自动落 vis/navmesh_*.bin（可走面）；路线 JSON 要在地图里按 Ctrl+E 手动导"),
    ("3. 验数据链路", "日志 naved: blank base / pack: skip / pack -> (official nav) 证明测试包、空白底图、正式版切换真的生效"),
    ("4. 核对图号映射", "scene[0..15] + LOAD levelN + OK (map='沙漠要塞') 确认 buildIndex 对应哪张图"),
    ("5. 看导航数据", "[nav] diag: graphs=1 / waiting for PointGraph 看出这张图有没有 PointGraph / NavMeshGraph"),
    ("6. 版本对比", "同一组参数跑旧版和新版，日志逐行对照，哪张图开始不一样一目了然"),
    ("7. 批量扫图", "一次勾 11 张，不用手动进 11 次图、不用点大厅"),
]
AT_CANNOT = [
    "人机行为、路线对不对（车测没人机）",
    "正常开局路径（大厅 → 房间 → 开始比赛）",
    "画面 / UI / 帧率 / 手感",
    "玩法逻辑（击杀、胜负、经济）",
]
AT_NOTE = ("PASS 也可能是假通过：settle 太小（20 tick = 5 秒），问题还没触发就判过了；"
           "勾的图太少，也可能刚好全避开。")
AT_SUMMARY = ("车测 = 自动进图跑一圈的快速回归 + 数据采集；核心产出「哪张图会崩」，"
              "次要产出「数据用没用上、图号对不对」。")
AT_QUICK = "日志速记：看开头 armed、数中间 OK、看结尾 RESULT。"


def load_level_table():
    r"""[(level, 中文名)] —— 只读 docs\地图对照表.md 第一张表（唯一权威表）。
    车测传的是 buildIndex，也就是 levelN 的 N，**不是** maps\NN_中文名.json 的序号：
    序号 07 是死亡擂台、它的关卡是 level11，两者不能混。"""
    out = []
    started = False
    try:
        with open(MAP_MD, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    if started:
                        break            # 空行 = 第一张表结束（后面还有别的表，不能一起读）
                    continue
                m = _MAP_ROW.match(s)
                if m:
                    started = True
                    out.append((m.group(1), m.group(2).strip()))
                elif started and not s.startswith("|"):
                    break
    except OSError:
        pass
    if len(out) < 5:
        out = list(_LEVELS_FALLBACK)
    out.sort(key=lambda r: int("".join(ch for ch in r[0] if ch.isdigit()) or 0))
    return out



def tail_log(n=6):
    try:
        with open(LOG_PATH, "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 65536))
            data = f.read().decode("utf-8", "replace")
    except OSError:
        return []
    lines = [ln for ln in data.splitlines() if ln.strip()]
    return lines[-n:]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UCF 控制台")
        # 高分屏 125% 缩放时 900 逻辑高会把底部按钮顶到任务栏外：
        # 按实际 DPI 折算屏幕可用高度，再夹在 680~900 之间。
        try:
            dpi = self.winfo_fpixels("1i") / 96.0
        except tk.TclError:
            dpi = 1.0
        screen_h = int(self.winfo_screenheight() / max(dpi, 0.5))
        win_h = max(680, min(900, screen_h - 120))
        # 2026-11-18：新增「人机路点」后 9 个页签 + 4 列类型卡需要约 750 内容宽，
        # 760 会把最右一列/最后一个页签裁掉；830 仍低于 1366 屏。
        self.geometry("830x%d+40+20" % win_h)   # 自己定位：交给窗口管理器会压到任务栏
        self.minsize(720, 620)
        self.protocol("WM_DELETE_WINDOW", self.on_close)   # 关窗前把没失焦的输入也存了
        self.cfg = load_cfg()
        feats = self.cfg.setdefault("features", {})
        if not isinstance(feats, dict):
            feats = {}
            self.cfg["features"] = feats
        self.feats = feats
        # 2026-11-19：可视化改成逐类开关；HUD、文字标签都已从游戏里删除
        for _old in ("vis_lists", "vis_layer_a", "vis_layer_b", "vis_layer_c", "vis_layer_d",
                     "hud", "hud_states", "hud_keys", "hud_log", "vis_labels"):
            feats.pop(_old, None)
        # 控制台自己的界面记忆（上次停在哪个页签）：只给控制台读，插件不认这一节
        ui = self.cfg.get("ui")
        if not isinstance(ui, dict):
            ui = {}
            self.cfg["ui"] = ui
        self.ui = ui

        self.vars = {}
        self.widgets = []
        # 2026-11-19：启动条件条（版本 / 包 / 生效图）—— 测试包模式的一次性预检可被静音
        self._mute_preflight = False
        self._strip_run = None

        self.head = ctk.CTkFrame(self, fg_color="transparent")
        self.head.pack(fill="x", padx=18, pady=(16, 4))
        ctk.CTkLabel(self.head, text="UCF 控制台", font=FONT_B).pack(side="left")
        # 2026-11-19 用户要求：右上角加「窗口置顶」勾选 + 折叠成小条的开关。
        self.btn_fold = ctk.CTkButton(self.head, text="折叠", width=52, height=24,
                                      font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                      command=self.toggle_fold)
        self.btn_fold.pack(side="right", padx=(10, 0))
        self.master_var = tk.BooleanVar(value=bool(self.cfg.get("enabled", True)))
        ctk.CTkSwitch(self.head, text="插件总开关", variable=self.master_var,
                      font=FONT, progress_color="#2f9e44",
                      command=self.on_master).pack(side="right")
        self.topmost_var = tk.BooleanVar(value=bool(self.ui.get("topmost", False)))
        ctk.CTkCheckBox(self.head, text="窗口置顶", variable=self.topmost_var, font=FONT_S,
                        checkbox_width=20, checkbox_height=20,
                        command=self.on_topmost).pack(side="right", padx=(0, 14))
        self._folded = False
        self._geom_saved = ""
        try:
            self.attributes("-topmost", bool(self.topmost_var.get()))
        except tk.TclError:
            pass

        self.intro = ctk.CTkLabel(
            self,
            text="只有从本窗口「开始游戏」才会加载 mod；直接双击 UnityCrossFire.exe 是原版。\n"
                 "开关改完存进 ucf_mod.json，下次启动生效（游戏开着时要重开）。\n"
                 "测试包模式在「人机路点」页；四版数据的路径 / 部署 / 还原 / 校验：切到「数据」页。\n"
                 "路点数据只读查看在工作台；现场编辑在「人机路点」页（游戏内 F2 菜单）。",
            font=FONT_S, text_color="#9aa0a6", justify="left")
        self.intro.pack(anchor="w", padx=20)

        # ---- 按钮 / 状态：先按底边占位，窗口再矮也不会被页签挤没 ----
        self.bar = ctk.CTkFrame(self, fg_color="transparent")
        self.bar.pack(side="bottom", fill="x", padx=14, pady=(0, 12))
        self.btn_game = ctk.CTkButton(self.bar, text="开始游戏（加载 mod）", font=FONT, height=42,
                                      fg_color="#2f6fdb", hover_color="#255bb4",
                                      command=self.launch_game)
        self.btn_game.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(self.bar, text="路点工作台（查看）", font=FONT, height=42,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_workbench).pack(side="left", fill="x", expand=True, padx=(6, 0))

        # 2026-11-19：启动条件条 —— 版本/包/生效图常驻在按钮上方，
        # 切到任何页签都看得见；这里只摆控件，文案由 refresh_launch_strip() 刷。
        self.strip = ctk.CTkFrame(self, corner_radius=8, fg_color="#232323",
                                  border_width=1, border_color="#3a3f47")
        self.strip.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
        self.strip_badge = ctk.CTkLabel(self.strip, text="正式版", width=78, height=26,
                                        corner_radius=6, fg_color="#16233a",
                                        text_color="#9cc3ff",
                                        font=("Microsoft YaHei UI", 12, "bold"))
        self.strip_badge.pack(side="left", padx=(10, 8), pady=9)
        self.strip_go = ctk.CTkButton(self.strip, text="去人机路点改", width=112, height=28,
                                      font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                      command=self.on_strip_go)
        self.strip_go.pack(side="right", padx=(8, 10), pady=8)
        self.strip_main = ctk.CTkFrame(self.strip, fg_color="transparent")
        self.strip_main.pack(side="left", fill="x", expand=True, pady=8)
        self.strip_title = ctk.CTkLabel(self.strip_main, text="", anchor="w", justify="left",
                                        font=("Microsoft YaHei UI", 12, "bold"))
        self.strip_title.pack(fill="x")
        self.strip_sub = ctk.CTkLabel(self.strip_main, text="", anchor="w", justify="left",
                                      font=FONT_S, text_color="#9aa0a6", wraplength=500)
        self.strip_sub.pack(fill="x")

        self.stat = ctk.CTkFrame(self, corner_radius=10)
        self.stat.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
        top = ctk.CTkFrame(self.stat, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(10, 2))
        ctk.CTkLabel(top, text="上次运行", font=("Microsoft YaHei UI", 14, "bold")).pack(side="left")
        self.dot = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
        self.dot.pack(side="right")
        self.logbox = ctk.CTkTextbox(self.stat, height=104, font=("Consolas", 12),
                                     fg_color="#141414", activate_scrollbars=True)
        self.logbox.pack(fill="x", padx=14, pady=(2, 12))

        # 地图 / 可视化 / 导出 / 快捷键 / 人机路点 / 数据 / 车测 —— 全部页签切换，上方不再压一块常驻面板。
        self.tabview = ctk.CTkTabview(self, corner_radius=10, command=self.on_tab)
        self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 4))
        self.tab_titles = []
        for title, hint, items in GROUPS:
            self.tab_titles.append(title)
            tab = self.tabview.add(title)
            if title == "导出":
                self.build_export_tab(tab, hint, items)  # 总开关 + 六项勾选（一行多个）+ 最近导出
            elif title == "快捷键":
                self.build_hotkey_tab(tab, hint)          # 热键速查（游戏内已不显示）
            elif title == "可视化":
                self.build_vis_tab(tab, hint, items)     # 总开关 + 九类数据（勾选）
            else:
                self.build_group_tab(tab, hint, items)
        # 人机路点要在「数据」「车测」之前：后两页读它建的 opt_pack / opt_map。
        wp_tab = self.tabview.add("人机路点")               # SyPB 式现场编辑入口
        self.build_waypoint_tab(wp_tab)
        self.build_data_tab(self.tabview.add("数据"))       # 四版路径/时间 + 部署/还原/校验
        self.build_autotest_tab(self.tabview.add("车测"))   # 不用鼠标键盘：插件自己在进程内切图
        self.tab_titles += ["人机路点", "数据", "车测"]

        # 回到上次停留的页签；记住的页签已经不存在（改版删页）就落在默认第一页
        saved_tab = str(self.ui.get("tab") or "")
        if saved_tab in self.tab_titles:
            self.tabview.set(saved_tab)
            self.on_tab(saved_tab, persist=False)

        self.refresh_status()
        self.after(4000, self.refresh_status)

    # ---- 页签内容：一组开关 = 一页 ----
    def switch_card(self, parent, key, label, desc, default):
        r"""一个开关 + 一行说明；「可视化」等页共用这份样式。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
        self.vars[key] = var
        ctk.CTkSwitch(box, text=label, variable=var, font=FONT,
                      progress_color="#2f9e44",
                      command=lambda k=key: self.on_toggle(k)).pack(
            anchor="w", padx=12, pady=(10, 0))
        ctk.CTkLabel(box, text=desc, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=600).pack(
            fill="x", padx=12, pady=(2, 10))

    def build_group_tab(self, tab, hint, items):
        r"""页内再套一层滚动区：窗口压矮时开关仍然够得着。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        for key, label, desc, default in items:
            self.switch_card(body, key, label, desc, default)

    # ---- 「可视化」页：总开关 + 九类数据（勾选）----
    # 2026-11-19 用户要求：一颗开关同时管「读不读」和「画不画」；总开关排最上面。
    def build_vis_tab(self, tab, hint, items):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        by = {k: (label, desc, default) for k, label, desc, default in items}
        if "visualizer" in by:
            self.switch_card(body, "visualizer", *by["visualizer"])
        keys = [k for k in by if k != "visualizer"]
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(box, text="画哪些数据", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=(2, 4))
        # 2026-11-19 用户要求：并列展示；英文类名太长就在勾选项里换行，不排成一行一个。
        # CTkCheckBox 的文字不会换行，所以勾选框留空，文字用旁边可换行的 CTkLabel 画。
        txts, legends = [], []
        for idx, key in enumerate(keys):
            label, desc, default = by[key]
            var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
            self.vars[key] = var
            cell = ctk.CTkFrame(grid, fg_color="transparent")
            cell.grid(row=idx // 3, column=idx % 3, sticky="w", padx=(0, 18), pady=6)
            row = ctk.CTkFrame(cell, fg_color="transparent")
            row.pack(anchor="w")
            cb = ctk.CTkCheckBox(row, text="", width=24, variable=var,
                                 command=lambda k=key: self.on_toggle(k))
            cb.pack(side="left", anchor="n")
            txt = ctk.CTkLabel(row, text=label, font=FONT_S, anchor="w",
                               justify="left", wraplength=200, cursor="hand2")
            txt.pack(side="left", padx=(4, 0), anchor="n")
            txt.bind("<Button-1>", lambda _e, c=cb: c.toggle())
            txts.append(txt)
            legends.append(self.vis_legend_row(cell, key, desc))
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)
        self.after(120, lambda: self.wrap_cells(body, txts, legends))
        ctk.CTkLabel(box, text="勾上 = 进图时读这一类并画出来；关掉 = 不读也不画（少一次可能出事的读取）。\n"
                              "只影响画面，不影响 Ctrl+E 导出（导出读什么由「导出」页那 6 项决定），"
                              "也不改动游戏本身。改完重启游戏生效。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=590).pack(
            fill="x", padx=12, pady=(8, 10))

    def wrap_cells(self, body, txts, legends):
        r"""按滚动区可见宽度给勾选项文字定换行；量的是画布，不是会被长文字撑大的内层。"""
        w = body._parent_canvas.winfo_width()
        if w <= 1:                                  # 还没显示出来，下一拍再量
            self.after(120, lambda: self.wrap_cells(body, txts, legends))
            return
        # 逻辑宽度扣掉：卡片左右 10、网格左右 12、滚动条余量 6；再按 3 列分
        logical = w / self._get_window_scaling() - (10 * 2 + 12 * 2 + 6)
        textw = max(120, int(logical / 3 - 18 - 30 - 12))  # 18 列距 / 30 勾选框 / 12 余量
        for txt in txts:
            txt.configure(wraplength=textw)
        for lg in legends:                          # 图例前面还有缩进和色块，留 30
            lg.configure(wraplength=max(120, textw - 30))

    def vis_legend_row(self, parent, key, text):
        r"""图例行：色块 + 游戏里的形状说明（颜色和形状照抄 editor.c 的 vis_draw）。"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", padx=(24, 0), pady=(2, 0))
        for c in VIS_COLORS.get(key, ()):
            ctk.CTkFrame(row, width=12, height=12, corner_radius=2,
                         fg_color=c).pack(side="left", padx=(0, 3))
        lbl = ctk.CTkLabel(row, text=text, font=FONT_S, text_color="#9aa0a6",
                           anchor="w", justify="left", wraplength=230)
        lbl.pack(side="left")
        return lbl

    # ---- 「导出」页：总开关（开关）+ 六项内容（一行多个勾选框）+ 最近导出 ----
    def build_export_tab(self, tab, hint, items):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        by = {k: (label, desc, default) for k, label, desc, default in items}
        if "export_enabled" in by:
            self.switch_card(body, "export_enabled", *by["export_enabled"])
        keys = [k for k in by if k != "export_enabled"]
        self.export_checkboxes(body, keys, by)
        self.build_export_info(body)

    def export_checkboxes(self, parent, keys, by):
        r"""导出内容：纯勾选框，一行放 3 个（用户 2026-11-18 要求）。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(box, text="导出内容", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=(2, 4))
        for idx, key in enumerate(keys):
            label, _desc, default = by[key]
            var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
            self.vars[key] = var
            ctk.CTkCheckBox(grid, text=label, variable=var, font=FONT_S,
                            command=lambda k=key: self.on_toggle(k)).grid(
                row=idx // 3, column=idx % 3, sticky="w", padx=(0, 18), pady=6)
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)
        ctk.CTkLabel(box, text="勾上 = Ctrl+E 时导出这一类；只影响导出，不影响画面。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=590).pack(
            fill="x", padx=12, pady=(0, 10))

    # ---- 「导出」页底部：最近一次导出的文件信息 ----
    def build_export_info(self, parent):
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(12, 12))
        head = ctk.CTkFrame(box, fg_color="transparent")
        head.pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(head, text="最近一次导出", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(side="left")
        ctk.CTkButton(head, text="打开文件夹", width=88, height=22, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.open_folder(vis_raw_dir(TEST))).pack(
            side="right")
        ctk.CTkButton(head, text="整理", width=56, height=22, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.tidy_vis).pack(side="right", padx=(0, 6))
        self.exp_name = ctk.CTkLabel(box, text="（还没有导出）", font=FONT_S,
                                     anchor="w", justify="left", wraplength=600)
        self.exp_name.pack(fill="x", padx=12, pady=(4, 0))
        self.exp_path = ctk.CTkLabel(box, text="", font=("Consolas", 12),
                                     anchor="w", justify="left", wraplength=600)
        self.exp_path.pack(fill="x", padx=12, pady=(4, 0))
        self.exp_time = ctk.CTkLabel(box, text="", font=FONT_S, text_color="#9aa0a6",
                                     anchor="w", justify="left", wraplength=600)
        self.exp_time.pack(fill="x", padx=12, pady=(4, 10))
        self.refresh_export_info()

    def refresh_export_info(self):
        r"""刷新「最近一次导出」：文件名 / 完整路径 / 修改时间；每 4 s 跟着状态一起刷。"""
        if not hasattr(self, "exp_name"):
            return
        hit = latest_export(TEST)
        if not hit:
            self.exp_name.configure(text="（还没有导出）")
            self.exp_path.configure(text="路径：%s（④ 测试版）" % TEST_VIS)
            self.exp_time.configure(text="修改时间：—")
            return
        fn, path, mtime = hit
        self.exp_name.configure(text="文件名：%s" % fn)
        self.exp_path.configure(text="路径：%s" % path)
        self.exp_time.configure(text="修改时间：%s" % fmt_time(mtime))

    def tidy_vis(self):
        r"""把 vis 里的导出按地图归类（tidy_vis.py 可反复跑，已归位的不会动）。"""
        if not os.path.isfile(TIDY):
            self.set_status("找不到 tidy_vis.py")
            return
        if not messagebox.askyesno(
                "整理导出",
                "把 vis 里的导出按地图归类：\n"
                "  raw\\<级别_中文名>\\<时间>_<指纹>.json\n"
                "  navmesh\\ 去重后的可走面\n"
                "  _state\\ 去重标记\n\n"
                "会删除与全局可走面完全相同的副本。继续？", parent=self):
            return
        try:
            env = dict(os.environ, PYTHONIOENCODING="utf-8")
            r = subprocess.run([sys.executable, "-u", TIDY], cwd=HERE,
                               capture_output=True, timeout=120, env=env)
            out = (r.stdout or b"").decode("utf-8", "replace").strip()
            err = (r.stderr or b"").decode("utf-8", "replace").strip()
            last = (out.splitlines() or ["(无输出)"])[-1]
            self.set_status("整理完成：%s" % (last if r.returncode == 0 else (err or last)))
        except Exception as exc:  # noqa: BLE001
            self.set_status("整理失败：%r" % exc)
            return
        self.refresh_export_info()

    # ---- 小标题（车测页用） ----
    def section_title(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Microsoft YaHei UI", 12, "bold"),
                     text_color="#c9d1d9", anchor="w").pack(
            fill="x", padx=14, pady=(12, 0))

    # ---- 「快捷键」页：只读速查表 ----
    def text_card(self, parent, title, text, height):
        r"""深色只读文本框（和「上次运行」日志同一套配色），插完内容立刻锁死。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(box, text=title, font=FONT, anchor="w").pack(
            fill="x", padx=12, pady=(8, 0))
        tb = ctk.CTkTextbox(box, height=height, font=("Consolas", 12),
                            fg_color="#141414", wrap="word")
        tb.pack(fill="x", padx=12, pady=(4, 10))
        tb.insert("1.0", text)
        tb.configure(state="disabled")
        return tb

    def build_hotkey_tab(self, tab, hint):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        self.text_card(body, "游戏内热键", HUD_KEYS, 330)
        ctk.CTkLabel(body, text=HUD_NOTES, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=14, pady=(10, 12))

    # ---- 「人机路点」页：SyPB 式现场编辑的控制台入口 ----
    def wp_card(self, parent, title, sub=""):
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        head = ctk.CTkFrame(box, fg_color="transparent")
        head.pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(head, text=title, font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(side="left")
        if sub:
            ctk.CTkLabel(head, text=sub, font=FONT_S, text_color="#9aa0a6",
                         anchor="e").pack(side="right")
        return box

    def wp_var(self, key, default):
        if key in self.vars:
            return self.vars[key]
        var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
        self.vars[key] = var
        return var

    def wp_switch(self, parent, key, label, default):
        var = self.wp_var(key, default)
        sw = ctk.CTkSwitch(parent, text=label, variable=var, font=FONT_S,
                           progress_color="#2f9e44",
                           command=lambda k=key: self.on_toggle(k))
        return sw

    def build_waypoint_tab(self, tab):
        r"""控制台「人机路点」页。

        设计：design/console-waypoint-tab.html。它不直接改游戏，
        只负责选图/包、写 ucf_mod.json 开关、给运行中的插件发 ucf_navcmd，
        并显示当前图的指纹与原生点/边数。
        """
        # 测试包 / 地图选择的状态由本页持有（2026-11-19 「测试数据」页删除后并入这里）；
        # 数据页、车测页仍然读 opt_pack / opt_map / seg_mode。
        self.maps = load_maps()                 # [(level, 中文名, 指纹)]
        self.map_disp = {("%s（%s）" % (lab, lv)): (lv, lab, fp) for lv, lab, fp in self.maps}
        pk = self.cfg.get("pack") if isinstance(self.cfg.get("pack"), dict) else {}
        self.pack_on = tk.BooleanVar(value=bool(pk.get("on", False)))
        self.pack_only = tk.BooleanVar(value=bool(pk.get("only_map", True)))
        self.pack_name = str(pk.get("name") or "")
        self.pack_map = str(pk.get("map") or (self.maps[0][0] if self.maps else ""))
        self.wp_scene = load_scene_counts()
        self.pack_disp = {}                     # 下拉框显示文字 → 包 id（地图文件夹/包名）
        self.ensure_pack_folders()              # 按地图自动建 packs\<场景名>\
        migrate_flat_packs()                    # 根目录的老包挪进地图文件夹
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        self.wp_body = body        # 「去人机路点改」跳过来时滚回 ① 卡
        ctk.CTkLabel(
            body,
            text="进游戏现场编辑：F2 打开路点菜单（长按 E 备用）；1-9 直选，小键盘 8/2 上下、5 确认、0 返回，左键/右键也可。\n"
                 "菜单打开时 W/A/S/D/空格仍可移动，Q/R/G/F/Tab 等会拦掉；选完 A 可走到 B 再按小键盘 5 连边。\n"
                 "按 F2 / 小键盘前先点一下游戏画面，让游戏窗口拿到焦点（控制台在前台时游戏收不到键）。\n"
                 "空白包=原生点全禁用；必须整图连通。只连主路还不够：孤立点、出生点、蹲守标记都可能让 Bot 取不到路。\n"
                 "markers 目前全局不分图，换图前先清掉别图的蹲守点；只测局部请用正式版 + 先删几个远处点腾槽位。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(8, 2))

        # ① 选图与数据
        box = self.wp_card(body, "① 选图与数据", "测试包只对一张图生效")
        self.card_pick = box       # 跳转时高亮这一张
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="数据版本", font=FONT_S,
                     text_color="#9aa0a6").pack(side="left", padx=(0, 6))
        self.seg_mode = ctk.CTkSegmentedButton(
            row, values=["正式版（nav）", "测试包（packs）"], font=FONT_S,
            command=lambda _v: self.on_pack_change())
        self.seg_mode.pack(side="left")
        self.seg_mode.set("测试包（packs）" if self.pack_on.get() else "正式版（nav）")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="测试包", font=FONT_S,
                     text_color="#9aa0a6").pack(side="left", padx=(0, 6))
        pack_values = self._pack_values()
        self.opt_pack = ctk.CTkOptionMenu(
            row, values=pack_values, font=FONT_S, width=262,
            command=lambda _v: self.on_pack_change())
        self.opt_pack.pack(side="left", padx=(0, 6))
        want = self.resolve_pack_id(self.pack_name)   # 上次选的包重启后接着选中
        if want and self.disp_of(want):
            self.opt_pack.set(self.disp_of(want))
        ctk.CTkButton(row, text="新建测试包", width=96, height=28, font=FONT_S,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=self.create_blank_pack).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="打开目录", width=76, height=28, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_packs_dir).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="清空本图", width=80, height=28, font=FONT_S,
                      fg_color="#8a4b1e", hover_color="#a55d26",
                      command=self.clear_pack_map).pack(side="left")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="地图", font=FONT_S,
                     text_color="#9aa0a6").pack(side="left", padx=(0, 6))
        self.opt_map = ctk.CTkOptionMenu(
            row, values=list(self.map_disp) or ["（没有可测的路点图）"],
            font=FONT_S, width=250,
            command=lambda _v: self.on_pack_change())
        self.opt_map.pack(side="left", padx=(0, 8))
        if self.pack_map:
            for disp, (lv, _lab, _fp) in self.map_disp.items():
                if lv == self.pack_map:
                    self.opt_map.set(disp)
                    break
        ctk.CTkCheckBox(row, text="只对这张图生效", variable=self.pack_only,
                        font=FONT_S, checkbox_width=18, checkbox_height=18,
                        command=self.on_pack_change).pack(side="left")

        self.wp_meta = ctk.CTkLabel(box, text="", font=("Consolas", 11),
                                    text_color="#9aa0a6", anchor="w",
                                    justify="left", wraplength=620)
        self.wp_meta.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(
            box,
            text="测试包按地图归类：packs\\<地图>\\<包名>\\，打开目录就能看到每张图一个文件夹。\n"
                 "空白底图两种建法：复用原生槽位（blank，点数 ≤ 原生点数）/ 真·新建节点（grow，不限点数）。\n"
                 "用运输船 / 新寂静村这种有原生点的图；飓风危城原生 0 点：只能建「真·新建节点（grow）」，"
                 "测试包只影响选中的图，正式版游戏内只读。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(2, 8))

        # ② 游戏内编辑
        box = self.wp_card(body, "② 游戏内编辑", "配置写 ucf_mod.json")
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=8, pady=(4, 4))
        switches = [
            ("wp_menu", "编辑菜单（F2 / 长按 E）", True),
            ("visualizer", "路点 / 边显示（Ctrl+V）", False),
            ("navmesh_show", "可走面线框（Ctrl+Shift+6）", True),
            ("wp_autoground", "加点自动落地", True),
        ]
        for idx, (key, label, default) in enumerate(switches):
            self.wp_switch(grid, key, label, default).grid(
                row=idx // 2, column=idx % 2, sticky="w",
                padx=(8, 6), pady=5)
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)
        ctk.CTkLabel(
            box,
            text="改完存进 ucf_mod.json；游戏开着时这些开关要重启才生效。"
                 "游戏内快捷键（Ctrl+Shift+N/J/D/Z、Ctrl+V）仍然可用。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=600).pack(fill="x", padx=12, pady=(0, 8))

        # ③ 自动铺设：只占位，不接任何功能（2026-11-19 用户要求）
        box = self.wp_card(body, "③ 自动铺设", "预留")
        ctk.CTkLabel(
            box,
            text="预留位置：自动铺设暂未接入，这里不做任何事。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(2, 12))

        self.on_pack_change(persist=False)
        self.refresh_wp_status()

    def refresh_wp_tab(self):
        if not hasattr(self, "wp_meta"):
            return
        self.refresh_wp_status()

    def refresh_wp_status(self):
        if not hasattr(self, "wp_meta"):
            return
        pk = self.pack_dict() if hasattr(self, "opt_pack") else {}
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        doc, _path = find_map_doc(fp)
        counts = (doc or {}).get("counts") or {}
        nodes = int(counts.get("nodes") or 0)
        edges = int(counts.get("edges") or 0)
        pack_on = bool(pk.get("on"))
        self.wp_meta.configure(
            text="指纹 %s · 原生 %d 点 / %d 边 · %s" % (
                fp or "—", nodes, edges,
                ("测试包 " + (self.disp_of(name) or name) if pack_on and name else "正式版（只读）")))

    # ---- 数据页：四版在哪 / 什么时候写的 / 一致不一致（原来三个 .bat 的活）----
    def build_data_tab(self, tab):
        r"""① 备份版/② 开发版/③ 部署版/④ 测试版 的路径、最近写入时间、条数，
        外加 导入 ④→② / 部署 ②→③ / 还原 ①→② / 校验 ① 的按钮。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text="① 只读快照；② 游戏内编辑 / 导入写这里；③ 游戏真正读这里；④ 插件导出和测试包落这里。"
                               "数据流：游戏导出 → ④ →（导入到开发版）→ ② →（部署到游戏）→ ③。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=620).pack(fill="x", padx=12, pady=(8, 2))

        self.data_cards = []
        for tag, name, root, hint in (
                ("①", "备份版（只读）", NATIVE, "冻结快照，永不编辑"),
                ("②", "开发版", DEV, "游戏内编辑 / 导入写这里"),
                ("③", "部署版", DEPLOY, "游戏插件读这里"),
                ("④", "测试版", TEST, "导出与测试包落这里，导入 ② 才生效")):
            box = ctk.CTkFrame(body, corner_radius=8)
            box.pack(fill="x", padx=10, pady=(8, 0))
            top = ctk.CTkFrame(box, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(8, 0))
            ctk.CTkLabel(top, text="%s %s" % (tag, name), font=FONT).pack(side="left")
            when = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
            when.pack(side="right")
            prow = ctk.CTkFrame(box, fg_color="transparent")
            prow.pack(fill="x", padx=12)
            open_btn = ctk.CTkButton(prow, text="打开文件夹", width=88, height=22,
                                     font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                     command=lambda p=root: self.open_folder(p))
            open_btn.pack(side="right", padx=(8, 0))
            ctk.CTkLabel(prow, text=root, font=("Consolas", 11), text_color="#7f8792",
                         anchor="w", justify="left", wraplength=500).pack(
                side="left", fill="x", expand=True)
            info = ctk.CTkLabel(box, text="", font=FONT_S, anchor="w", justify="left",
                                text_color="#c9d1d9")
            info.pack(fill="x", padx=12, pady=(0, 8))
            self.data_cards.append({"tag": tag, "hint": hint, "root": root,
                                    "time": when, "info": info, "open": open_btn})

        self.lbl_same = ctk.CTkLabel(body, text="", font=FONT_S, anchor="w", justify="left",
                                     wraplength=620, text_color="#c9d1d9")
        self.lbl_same.pack(fill="x", padx=14, pady=(8, 0))

        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkButton(row, text="导入到开发版 ④→②", font=FONT_S, height=32, fg_color="#2f7d4f",
                      hover_color="#256a41",
                      command=self.do_import).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="部署到游戏 ②→③", font=FONT_S, height=32, fg_color="#2f6fdb",
                      hover_color="#255bb4",
                      command=self.do_publish).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="还原原生 ①→②", font=FONT_S, height=32, fg_color="#8a4b1e",
                      hover_color="#a55d26",
                      command=self.do_restore).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="校验备份版", font=FONT_S, height=32, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.do_verify).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="刷新", font=FONT_S, height=32, width=64, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.refresh_data).pack(side="left")

        self.data_out = ctk.CTkTextbox(body, height=118, font=("Consolas", 11),
                                       fg_color="#141414", activate_scrollbars=True)
        self.data_out.pack(fill="x", padx=12, pady=(8, 12))
        self.data_out.insert("end", "（点上面的按钮，命令输出会贴在这里）")
        self.data_out.configure(state="disabled")
        self._busy = ""
        self._q = queue.Queue()
        self.after(150, self.pump_navdata)
        self.refresh_data()

    def pump_navdata(self):
        r"""工作线程只往队列里塞结果，Tk 控件一律在主线程改（跨线程 after() 会报
        "main thread is not in main loop"）。"""
        while True:
            try:
                title, code, text = self._q.get_nowait()
            except queue.Empty:
                break
            self._navdata_done(title, code, text)
        self.after(150, self.pump_navdata)

    def refresh_data(self):
        r"""重算四版的路径/时间/条数 + 两两一致性；文件都在本机，毫秒级。"""
        if not hasattr(self, "data_cards"):
            return
        for card in self.data_cards:
            root = card["root"]
            if card["tag"] == "④":
                n_json, n_bin, n_packs, total, latest = test_stats(root)
                names = load_packs()
                card["time"].configure(text=("最近写入 " + fmt_time(latest)) if latest
                                       else "（还没有导出）")
                card["info"].configure(
                    text="导出 %d 份 JSON · 可走面 %d 份 · 测试包 %d 个（%s）· %s"
                         % (n_json, n_bin, n_packs,
                            "、".join(x.split("/")[-1] for x in names) if names else "无",
                            human_size(total)))
                continue
            n, total, latest = dir_stats(root)
            maps, files, lines, bins = data_counts(root)
            card["time"].configure(text="最近写入 " + fmt_time(latest))
            card["info"].configure(
                text="%d 图 · 编辑 %d 个文件/%d 条 · %d 可走面 · %s，共 %d 个文件"
                     % (maps, files, lines, bins, human_size(total), n))
        try:
            d1, d2, d3 = tree_hashes(NATIVE), tree_hashes(DEV), tree_hashes(DEPLOY)
        except OSError:
            self.lbl_same.configure(text="一致性：读不动某个版本")
            return
        n12, n23 = diff_count(d1, d2), diff_count(d2, d3)
        n_exp = test_stats(TEST)[0]
        self.lbl_same.configure(
            text=r"一致性（只比 maps\*.json 与 nav\*.txt，索引与 names.json 不算）："
                 + ("①=②" if n12 == 0 else "① vs ② 有 %d 个文件不同" % n12)
                 + " · " + ("②=③" if n23 == 0 else "② vs ③ 有 %d 个文件不同" % n23)
                 + " · " + ("④ 没有导出" if n_exp == 0
                            else "④ 有 %d 份导出（导入到开发版）" % n_exp))

    # ---- 车测页：插件在进程内逐张 LoadScene，不用鼠标键盘（原 tools\autotest.ps1 的 GUI 版）----
    def build_autotest_tab(self, tab):
        r"""关游戏 → 带 UCF_AUTOTEST 重开 → 轮询日志里的 RESULT PASS / FAIL / crash。
        关键点：开跑前必须先删旧 autotest.txt，否则上一次的 PASS 会被立刻当成这次的结果。"""
        self.at_levels = load_level_table()
        at = self.cfg.get("autotest") if isinstance(self.cfg.get("autotest"), dict) else {}
        sel = at.get("targets")
        if not isinstance(sel, list):
            sel = [7, 10]
        sel = set(int(x) for x in sel if str(x).isdigit())
        self.at_maps = {}
        self.at_q = queue.Queue()
        self.at_stop = threading.Event()
        self.at_busy = False

        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text="车测 = 关游戏 → 带 UCF_AUTOTEST 重开 → 插件在进程内逐张 LoadScene，"
                              "每张等 settle×250 ms → RESULT PASS 后退出。\n"
                              "只验加载链路：PASS 不代表「大厅 → 开始比赛」正常；开跑会备份 ucf_mod.log、"
                              "删旧 autotest.txt。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=620).pack(fill="x", padx=12, pady=(8, 2))

        # 结果放在最上面：窗口不高时进度框要滚动才看得到，结论必须一眼可见
        self.lbl_at = ctk.CTkLabel(body, text="", font=FONT, anchor="w", justify="left",
                                   wraplength=620, text_color="#9aa0a6")
        self.lbl_at.pack(fill="x", padx=14, pady=(8, 0))

        self.section_title(body, "地图（勾几张跑几张；数字 = buildIndex，不是 maps 里的序号）")
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(6, 0))
        for i, (lv, name) in enumerate(self.at_levels):
            n = int("".join(ch for ch in lv if ch.isdigit()) or 0)
            var = tk.BooleanVar(value=n in sel)
            self.at_maps[lv] = var
            ctk.CTkCheckBox(box, text="%d %s" % (n, name), variable=var, font=FONT_S,
                            checkbox_width=18, checkbox_height=18,
                            command=self.on_at_change).grid(
                row=i // 4, column=i % 4, sticky="w",
                padx=(12, 4), pady=(8 if i < 4 else 2, 0))
        for c in range(4):
            box.grid_columnconfigure(c, weight=1)
        ctk.CTkLabel(box, text="", height=4).grid(
            row=(len(self.at_levels) + 3) // 4, column=0, columnspan=4)

        self.section_title(body, "参数")
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(6, 0))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 0))
        self.at_warm = tk.StringVar(value=str(at.get("warm", 40)))
        self.at_settle = tk.StringVar(value=str(at.get("settle", 120)))
        self.at_timeout = tk.StringVar(value=str(at.get("timeout", 600)))
        for title, var, width in (("warm（切图前等）", self.at_warm, 58),
                                  ("settle（每张等）", self.at_settle, 58),
                                  ("超时（秒）", self.at_timeout, 58)):
            ctk.CTkLabel(row, text=title, font=FONT_S).pack(side="left", padx=(0, 4))
            ent = ctk.CTkEntry(row, textvariable=var, width=width, font=FONT_S)
            ent.pack(side="left", padx=(0, 12))
            ent.bind("<FocusOut>", self.on_at_change)   # 填完就存，重启还是这三个数
            ent.bind("<Return>", self.on_at_change)
        self.at_exit = tk.BooleanVar(value=bool(at.get("exit", True)))
        ctk.CTkSwitch(box, text="跑完自动退出（PASS 后关游戏）", variable=self.at_exit,
                      font=FONT_S, progress_color="#2f9e44",
                      command=self.on_at_change).pack(
            anchor="w", padx=14, pady=(6, 0))
        self.at_freecam = tk.BooleanVar(value=bool(at.get("freecam", True)))
        ctk.CTkSwitch(box, text="自由视角（WASD 移动 · 按住右键转视角 · F7 开关）",
                      variable=self.at_freecam, font=FONT_S,
                      progress_color="#2f9e44",
                      command=self.on_at_change).pack(
            anchor="w", padx=14, pady=(2, 8))

        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=(6, 0))
        self.btn_at_run = ctk.CTkButton(row, text="开跑（会先关游戏）", font=FONT, height=34,
                                        fg_color="#2f6fdb", hover_color="#255bb4",
                                        command=self.run_autotest)
        self.btn_at_run.pack(side="left", padx=(0, 6))
        self.btn_at_stop = ctk.CTkButton(row, text="中止（关游戏）", font=FONT_S, height=34,
                                         width=110, fg_color="#8a4b1e", hover_color="#a55d26",
                                         state="disabled", command=self.stop_autotest)
        self.btn_at_stop.pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="打开日志", font=FONT_S, height=34, width=88,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.open_file(LOG_PATH, "ucf_mod.log")).pack(
            side="right", padx=(6, 0))
        ctk.CTkButton(row, text="打开结果", font=FONT_S, height=34, width=88,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.open_file(AUTOTEST_TXT, "autotest.txt")).pack(
            side="right")

        self.at_out = ctk.CTkTextbox(body, height=110, font=("Consolas", 11),
                                     fg_color="#141414", activate_scrollbars=True)
        self.at_out.pack(fill="x", padx=12, pady=(6, 12))
        self.at_out.insert("end", "（点「开跑」后这里贴 [at] 进度：warm / LOAD / OK / RESULT）")
        self.at_out.configure(state="disabled")

        self.section_title(body, "车测是干什么的")
        helpbox = ctk.CTkFrame(body, corner_radius=8)
        helpbox.pack(fill="x", padx=10, pady=(6, 12))

        def help_title(text):
            ctk.CTkLabel(helpbox, text=text, font=("Microsoft YaHei UI", 12, "bold"),
                         text_color="#e6edf3", anchor="w").pack(
                fill="x", padx=12, pady=(10, 2))

        def help_line(text, color="#c9d1d9"):
            ctk.CTkLabel(helpbox, text=text, font=FONT_S, text_color=color,
                         anchor="w", justify="left", wraplength=590).pack(
                fill="x", padx=16, pady=(0, 2))

        help_title("能做的事")
        for name, desc in AT_CAN:
            help_line("%s —— %s" % (name, desc))
        help_title("不能做的事")
        for item in AT_CANNOT:
            help_line("· " + item)
        help_title("注意")
        help_line(AT_NOTE)
        help_title("一句话")
        help_line(AT_SUMMARY)
        ctk.CTkLabel(helpbox, text=AT_QUICK, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=590).pack(
            fill="x", padx=12, pady=(6, 10))
        self.refresh_at()
        self.after(400, self.pump_autotest)

    def open_file(self, path, what):
        if not os.path.isfile(path):
            self.set_status("还没有 %s" % what)
            return
        try:
            os.startfile(path)      # noqa: SLF001  Windows 资源管理器
            self.set_status("已打开 %s" % what)
        except OSError as exc:
            self.set_status("打不开 %s：%s" % (what, exc))

    def refresh_at(self):
        r"""autotest.txt 最后一条 RESULT → 「上一次车测」；没有 RESULT 说明中途被杀/崩了。"""
        if not hasattr(self, "lbl_at") or self.at_busy:
            return
        try:
            with open(AUTOTEST_TXT, "r", encoding="utf-8", errors="replace") as f:
                lines = [ln.strip() for ln in f if ln.strip()]
        except OSError:
            self.lbl_at.configure(text="上一次车测：还没有 autotest.txt", text_color="#9aa0a6")
            return
        last = ""
        for ln in lines:
            if ln.startswith("RESULT"):
                last = ln
        if last:
            ok = "PASS" in last
            self.lbl_at.configure(text="上一次车测：" + last,
                                  text_color="#4ec97a" if ok else "#e8654f")
        else:
            self.lbl_at.configure(text="上一次车测：没跑到 RESULT（中途关游戏 / 崩溃）",
                                  text_color="#e8c15a")

    def _at_int(self, var, default):
        try:
            return max(0, int(str(var.get()).strip()))
        except (TypeError, ValueError):
            return default

    def run_autotest(self):
        if self.at_busy:
            return
        picked = [lv for lv, var in self.at_maps.items() if var.get()]
        if not picked:
            self.set_status("车测：至少勾一张图")
            return
        if not os.path.isfile(GAME_EXE):
            self.set_status("找不到 %s" % GAME_EXE)
            return
        picked.sort(key=lambda lv: int("".join(ch for ch in lv if ch.isdigit()) or 0))
        idx = ",".join(str(int("".join(ch for ch in lv if ch.isdigit()) or 0)) for lv in picked)
        warm = self._at_int(self.at_warm, 40)
        settle = self._at_int(self.at_settle, 120)
        timeout = max(30, self._at_int(self.at_timeout, 600))
        exit_when_done = bool(self.at_exit.get())
        freecam = bool(self.at_freecam.get())

        env, note = self.game_env()          # Tk 变量只在主线程读
        env["UCF_AUTOTEST"] = idx
        env["UCF_AT_WARM"] = str(warm)
        env["UCF_AT_SETTLE"] = str(settle)
        env["UCF_AT_EXIT"] = "1" if exit_when_done else "0"
        if freecam:
            env["UCF_FREECAM"] = "1"
        else:
            env.pop("UCF_FREECAM", None)     # 取消勾选时别把父进程的环境带进去

        self.save_autotest_ui()          # 车测页的勾选/参数：开跑前顺手再存一次
        try:
            save_cfg(self.cfg)
        except OSError:
            pass

        self.at_busy = True
        self.at_stop.clear()
        # 车测也是本窗口启动的：记下启动瞬间的条件，启动条别误报成「外部启动」
        strip_info = self.launch_strip_info()
        self._strip_run = strip_info
        self.btn_at_run.configure(state="disabled")
        self.btn_at_stop.configure(state="normal")
        names = " → ".join("%s(%s)" % (name, lv) for lv, name in self.at_levels if lv in picked)
        self.lbl_at.configure(text="车测进行中：%s · settle=%d · %s" % (names, settle, note),
                              text_color="#e8c15a")
        self.at_out.configure(state="normal")
        self.at_out.delete("1.0", "end")
        self.at_out.insert("end", "目标 %s · warm=%d settle=%d timeout=%ds · %s\n"
                           % (idx, warm, settle, timeout, note))
        self.at_out.configure(state="disabled")
        self.set_status("车测：正在关闭游戏 …")
        threading.Thread(target=self._at_worker,
                         args=(env, idx, timeout, strip_info), daemon=True).start()

    def stop_autotest(self):
        if not self.at_busy:
            return
        self.at_stop.set()
        self.set_status("车测：正在中止（关游戏）…")

    def save_autotest_ui(self):
        r"""车测页的勾选 + 参数也写进 ucf_mod.json：下次打开还是上次那一套。"""
        if not hasattr(self, "at_maps"):
            return
        self.cfg["autotest"] = {
            "targets": [int("".join(ch for ch in lv if ch.isdigit()) or 0)
                        for lv, var in self.at_maps.items() if var.get()],
            "warm": self._at_int(self.at_warm, 40),
            "settle": self._at_int(self.at_settle, 120),
            "timeout": max(30, self._at_int(self.at_timeout, 600)),
            "exit": bool(self.at_exit.get()),
            "freecam": bool(self.at_freecam.get()),
        }

    def on_at_change(self, _event=None):
        r"""勾一下 / 改个数就落盘（以前只在点「开跑」时才存）。"""
        self.save_autotest_ui()
        try:
            save_cfg(self.cfg)
        except OSError as exc:
            self.set_status("写不进 ucf_mod.json：%s" % exc)
            return
        self.set_status("已保存 车测设置")

    def _at_worker(self, env, idx, timeout, strip_info=None):
        r"""工作线程只读日志/开进程/写队列，Tk 控件一律回主线程改（pump_autotest）。"""
        q = self.at_q

        def put(kind, text):
            q.put((kind, text))

        try:
            put("line", "关闭游戏进程 …")
            if not kill_game():
                put("result", "RESULT 中止：游戏进程关不掉")
                return
            prev = os.path.join(DEPLOY, "ucf_mod.prev_%s.log" % time.strftime("%H%M%S"))
            try:
                os.replace(LOG_PATH, prev)
                put("line", "日志已备份：%s" % os.path.basename(prev))
            except OSError:
                pass
            try:
                os.remove(AUTOTEST_TXT)      # 不删就会把上一次的 PASS 当成这次的结果
                put("line", "已删旧 autotest.txt")
            except OSError:
                pass
            put("line", "启动 UnityCrossFire.exe  UCF_AUTOTEST=%s" % idx)
            # 关游戏和重开之间 refresh 可能把快照清掉，这里补回（只写数据，不碰 Tk）
            if strip_info:
                self._strip_run = strip_info
            proc = subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE), env=env)
            offset = 0
            seen = ""
            t0 = time.time()
            while True:
                if self.at_stop.is_set():
                    kill_game()
                    put("result", "RESULT 中止（手动，已关游戏）")
                    return
                text, offset = read_log_from(LOG_PATH, offset)
                if text:
                    seen += text
                    for line in text.splitlines():
                        low = line.lower()
                        if "!!! crash" in low:
                            put("line", line)
                        elif ("[at]" in line and "resolve:" not in line
                              and "settle level" not in line):
                            put("line", line)
                if "!!! crash" in seen:
                    put("result", "RESULT CRASH（VEH 已记录，见日志 crash 段）")
                    return
                if "RESULT PASS" in seen:
                    put("result", "RESULT PASS（%d 张图，%ds）"
                        % (len(idx.split(",")), int(time.time() - t0)))
                    return
                if "RESULT FAIL" in seen:
                    put("result", "RESULT FAIL（%ds，见日志）" % int(time.time() - t0))
                    return
                if proc.poll() is not None:
                    # 进程没了但可能刚写最后一行：再读一次再判
                    text, offset = read_log_from(LOG_PATH, offset)
                    seen += text
                    if "RESULT PASS" in seen:
                        put("result", "RESULT PASS（%d 张图，%ds）"
                            % (len(idx.split(",")), int(time.time() - t0)))
                    elif "RESULT FAIL" in seen:
                        put("result", "RESULT FAIL（见日志）")
                    else:
                        put("result", "RESULT CRASH（进程退出但没有 RESULT）")
                    return
                if time.time() - t0 > timeout:
                    kill_game()
                    put("result", "RESULT 超时（%ds，已关游戏）" % timeout)
                    return
                time.sleep(1)
        except Exception as exc:                     # noqa: BLE001
            put("result", "车测异常：%s" % exc)
        finally:
            q.put(("done", ""))

    def pump_autotest(self):
        try:
            while True:
                kind, text = self.at_q.get_nowait()
                if kind == "line":
                    self.at_out.configure(state="normal")
                    self.at_out.insert("end", text + "\n")
                    self.at_out.see("end")
                    self.at_out.configure(state="disabled")
                elif kind == "result":
                    ok = "PASS" in text
                    self.lbl_at.configure(text=text, text_color="#4ec97a" if ok else "#e8654f")
                    self.set_status("车测：" + text)
                    self.at_out.configure(state="normal")
                    self.at_out.insert("end", "\n" + text + "\n")
                    self.at_out.see("end")
                    self.at_out.configure(state="disabled")
                elif kind == "done":
                    self.at_busy = False
                    self.btn_at_run.configure(state="normal")
                    self.btn_at_stop.configure(state="disabled")
                    self.refresh_status()
        except queue.Empty:
            pass
        self.after(400, self.pump_autotest)

    def on_tab(self, name=None, persist=True):
        r"""页签切换：刷新这一页的数据，并把「上次停在哪」写进 ucf_mod.json。
        CTkTabview 的 command 不传参数，name 为空时自己读当前页签。"""
        if not name:
            name = self.tabview.get()
        self.save_autotest_ui()          # 离开车测页时把改过的参数带走
        self.ui["tab"] = name
        if persist:
            try:
                save_cfg(self.cfg)
            except OSError:
                pass
        if name == "数据":
            self.refresh_data()
        elif name == "导出":
            self.refresh_export_info()
        elif name == "车测":
            self.refresh_at()
        elif name == "人机路点":
            if hasattr(self, "opt_pack"):
                cur = self.selected_pack()
                self.opt_pack.configure(values=self._pack_values())   # 编辑器新存的包也刷进来
                if cur and self.disp_of(cur):
                    self.opt_pack.set(self.disp_of(cur))
            self.refresh_wp_tab()

    # ---- 原来三个 .bat 的按钮：后台跑 navdata.py，输出贴回本页 ----
    def run_navdata(self, args, title):
        if getattr(self, "_busy", ""):
            self.set_status("正在执行：%s，等它跑完" % self._busy)
            return
        self._busy = title
        self.data_out.configure(state="normal")
        self.data_out.insert("end", "\n> python navdata.py %s\n" % " ".join(args))
        self.data_out.see("end")
        self.data_out.configure(state="disabled")
        self.set_status("%s …" % title)
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env.setdefault("UCF_PROFILE", "dev")

        def work():
            try:
                cp = subprocess.run([_python(), NAVDATA] + list(args), cwd=HERE, env=env,
                                    capture_output=True, timeout=300,
                                    creationflags=CREATE_NO_WINDOW)
                text = ((cp.stdout or b"").decode("utf-8", "replace")
                        + (cp.stderr or b"").decode("utf-8", "replace"))
                code = cp.returncode
            except Exception as exc:                       # noqa: BLE001
                text, code = "执行失败：%s" % exc, -1
            self._q.put((title, code, text))

        threading.Thread(target=work, daemon=True).start()

    def _navdata_done(self, title, code, text):
        self._busy = ""
        self.data_out.configure(state="normal")
        self.data_out.insert("end", (text.strip() or "（没有输出）") + "\n")
        self.data_out.see("end")
        self.data_out.configure(state="disabled")
        self.set_status("%s %s" % (title, "完成" if code == 0 else "失败（退出码 %s）" % code))
        self.refresh_data()

    def _guard_game(self, title):
        r"""游戏开着时部署/还原不会报错，但这一局读的还是旧数据 —— 先问一句，别让人以为改完没生效。"""
        if not game_running():
            return True
        return messagebox.askyesno(title, "游戏正在运行：这一局已经读进内存的数据不会变。\n"
                                          "要现在继续吗？（想让它这次生效就先关游戏）", parent=self)

    def do_import(self):
        r"""④ 测试版 -> ② 开发版：可走面 + 原始导出。不改 ③，游戏在跑也能做。"""
        self.run_navdata(["import"], "导入到开发版")

    def do_publish(self):
        if not self._guard_game("部署到游戏"):
            return
        self.run_navdata(["publish"], "部署到游戏")

    def do_restore(self):
        if not self._guard_game("还原原生"):
            return
        if not messagebox.askyesno("还原原生",
                                   "② 开发版会被 ① 备份版覆盖：\n还没部署到游戏的改动会丢掉。\n\n继续？",
                                   parent=self):
            return
        self.run_navdata(["restore"], "还原原生")

    def do_verify(self):
        self.run_navdata(["verify"], "校验备份版")

    # ---- 写盘 ----
    def persist(self, note=""):
        self.cfg["enabled"] = bool(self.master_var.get())
        feats = self.cfg.setdefault("features", {})
        for k, v in self.vars.items():
            feats[k] = bool(v.get())
        if hasattr(self, "seg_mode"):
            self.cfg["pack"] = self.pack_dict()
        try:
            save_cfg(self.cfg)
        except OSError as exc:
            self.set_status("写不进 ucf_mod.json：%s" % exc)
            return
        msg = "已保存 " + (note or "")
        if game_running():
            msg += " · 游戏在运行，重启游戏才生效"
        self.set_status(msg)

    def on_toggle(self, key):
        self.persist(key)

    def on_master(self):
        self.persist("总开关")
        self.refresh_launch_strip()

    # ---- 窗口置顶 / 折叠成小条 ----------------------------------------
    def on_topmost(self):
        r"""窗口置顶：勾上就一直浮在游戏上面；状态记进 ucf_mod.json 的 ui 段。"""
        on = bool(self.topmost_var.get())
        self.ui["topmost"] = on
        self.attributes("-topmost", on)
        try:
            save_cfg(self.cfg)
        except OSError:
            pass

    def toggle_fold(self):
        r"""折叠：藏起介绍/页签/日志/底部按钮，窗口缩成只剩标题行的一条；
        再点「展开」按原尺寸、原位置回来。折叠条宽度按标题行实际内容收窄，不留空档。"""
        if not self._folded:
            self._geom_saved = str(self.tk.call("wm", "geometry", self))
            self._folded = True
            self.intro.pack_forget()
            self.tabview.pack_forget()
            self.stat.pack_forget()
            self.strip.pack_forget()
            self.bar.pack_forget()
            self.minsize(1, 1)
            _size, x, y = self._geom_saved.split("+")
            w = self.head.winfo_reqwidth() + int(self._apply_window_scaling(44))
            h = self.head.winfo_reqheight() + int(self._apply_window_scaling(30))
            self.tk.call("wm", "geometry", self, "%dx%d+%s+%s" % (w, h, x, y))
            self.btn_fold.configure(text="展开")
        else:
            self._folded = False
            # 按原来的 pack 顺序装回去：介绍 → 底栏 → 日志 → 页签
            self.intro.pack(anchor="w", padx=20)
            self.bar.pack(side="bottom", fill="x", padx=14, pady=(0, 12))
            self.strip.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
            self.stat.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
            self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 4))
            self.minsize(720, 620)
            self.tk.call("wm", "geometry", self, self._geom_saved)
            self.btn_fold.configure(text="折叠")

    def on_close(self):
        r"""关窗口 = 最后一次落盘：正停在哪个页签、车测输入框里没失焦的数字都不丢。"""
        self.save_autotest_ui()
        tab = self.tabview.get()
        if tab:
            self.ui["tab"] = tab
        try:
            save_cfg(self.cfg)
        except OSError:
            pass
        self.destroy()

    # ---- 测试包：取值 / 切换（UI 在「人机路点」① 选图与数据）----
    def ensure_pack_folders(self):
        r"""packs\ 下按地图建文件夹：英文场景名+中文名（如 TransportShip运输船）。

        以前建过的纯英文文件夹（TransportShip）会自动改名合并过来，已有的包跟着走。
        """
        pairs = []
        for lv, _lab, fp in self.maps:
            pairs.append((map_scene(lv, fp), map_folder(lv, fp)))
        for lv, _row in self.wp_scene.items():
            pairs.append((map_scene(lv), map_folder(lv)))
        for old, new in pairs:
            oldp, newp = os.path.join(PACKS, old), os.path.join(PACKS, new)
            try:
                if old != new and os.path.isdir(oldp):
                    if not os.path.isdir(newp):
                        os.rename(oldp, newp)
                    else:                      # 两边都在：把包挪过去，不覆盖同名
                        for sub in os.listdir(oldp):
                            src = os.path.join(oldp, sub)
                            dst = os.path.join(newp, sub)
                            if os.path.isdir(src) and not os.path.exists(dst):
                                shutil.move(src, dst)
                        try:
                            os.rmdir(oldp)
                        except OSError:
                            pass
                os.makedirs(newp, exist_ok=True)
            except OSError:
                pass

    def folder_label(self, folder):
        r"""地图文件夹 → 界面上显示的中文名（兼容旧的纯英文文件夹）。"""
        for lv, lab, fp in self.maps:
            if folder in (map_folder(lv, fp), map_scene(lv, fp)):
                return lab
        for lv, row in self.wp_scene.items():
            if folder in (map_folder(lv), map_scene(lv)):
                return str(row.get("name") or folder)
        return folder

    def resolve_pack_id(self, pid):
        r"""老配置里存的是平铺包名：按尾名找回分类后的 id（地图文件夹/包名）。"""
        pid = str(pid or "").replace("\\", "/").strip("/")
        if not pid:
            return ""
        if os.path.isdir(pack_dir(pid)):
            return pid
        tail = pid.split("/")[-1]
        for x in load_packs():
            if x.split("/")[-1] == tail:
                return x
        return ""

    def disp_of(self, pid):
        for disp, x in getattr(self, "pack_disp", {}).items():
            if x == pid:
                return disp
        return ""

    def _pack_values(self):
        r"""下拉框：按地图分组排列，显示成「运输船 · blank_b」。"""
        ids = load_packs()
        self.pack_disp = {}
        order = {lv: i for i, (lv, _l, _f) in enumerate(self.maps)}

        def sort_key(pid):
            lv = str(pack_manifest(pid).get("level") or "")
            return (order.get(lv, 99), pid)

        vals = []
        for pid in sorted(ids, key=sort_key):
            folder, _sep, name = pid.rpartition("/")
            lab = self.folder_label(folder) if folder else "未分类"
            disp = "%s · %s" % (lab, name)
            while disp in self.pack_disp:      # 同名包极少见，重了就加空格区分
                disp += " "
            self.pack_disp[disp] = pid
            vals.append(disp)
        return vals or ["（还没有测试包）"]

    def pack_dict(self):
        """当前选择 → 写回 ucf_mod.json 的 pack 段（只给控制台自己用，插件不读它）。"""
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        lv, lab, fp = self.map_disp.get(disp, ("", "", ""))
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        return {
            "on": bool(self.pack_on.get()),
            "name": name,
            "map": lv, "label": lab, "fp": fp,
            "only_map": bool(self.pack_only.get()),
        }

    def pack_manifest_map(self, pid):
        """包对应的地图（manifest.json 的 level）；没有 manifest 就按文件夹名反查。"""
        lv = str(pack_manifest(pid).get("level") or "")
        if lv:
            return lv
        folder = str(pid).replace("\\", "/").split("/")[0]
        for lvl, _lab, fp in self.maps:
            if folder in (map_folder(lvl, fp), map_scene(lvl, fp)):
                return lvl
        return ""

    def on_pack_change(self, persist=True):
        on = self.seg_mode.get().startswith("测试包")
        self.pack_on.set(on)
        disp = self.opt_pack.get()
        name = "" if disp.startswith("（") else getattr(self, "pack_disp", {}).get(disp, "")
        if not name and not disp.startswith("（"):
            name = self.resolve_pack_id(disp)
        if not name:
            packs = self._pack_values()
            self.opt_pack.configure(values=packs)
            if packs and not packs[0].startswith("（"):
                self.opt_pack.set(packs[0])
                name = self.pack_disp.get(packs[0], "")
        # 换包时自动把地图切到包对应的那张图（包只对它生效，选错图等于空跑）
        if on and name and name != getattr(self, "_last_pack", ""):
            lv = self.pack_manifest_map(name)
            for mdisp, (lvl, _lab, _fp) in self.map_disp.items():
                if lv and lvl == lv:
                    self.opt_map.set(mdisp)
                    break
        self._last_pack = name
        self.pack_name = name
        state = "normal" if on else "disabled"
        try:
            self.opt_pack.configure(state=state)
            self.opt_map.configure(state=state)
        except Exception:
            pass
        if persist:
            self.persist("测试包")
        self.refresh_launch_strip()

    def open_packs_dir(self):
        try:
            os.makedirs(PACKS, exist_ok=True)
            os.startfile(PACKS)      # noqa: SLF001  Windows 资源管理器
        except OSError as exc:
            self.set_status("打不开 packs 目录：%s" % exc)

    def open_folder(self, path):
        r"""数据页每张卡旁边的「打开文件夹」：不存在就提示，不替用户创建。"""
        if not os.path.isdir(path):
            self.set_status("目录不存在：%s" % path)
            return
        try:
            os.startfile(path)      # noqa: SLF001  Windows 资源管理器
        except OSError as exc:
            self.set_status("打不开目录：%s" % exc)
            return
        self.set_status("已打开：%s" % path)

    # ---- 控制台 → 运行中插件：载入 / 重读 / 保存 / 回正式版 ----
    def selected_pack(self):
        r"""当前选中的包 id（地图文件夹/包名）；没选返回空串。"""
        disp = self.opt_pack.get() if hasattr(self, "opt_pack") else ""
        if not disp or disp.startswith("（"):
            return ""
        return getattr(self, "pack_disp", {}).get(disp) or self.resolve_pack_id(disp)

    def selected_fp(self):
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        return self.map_disp.get(disp, ("", "", ""))[2]

    def send_pack_cmd(self, cmd):
        r"""把「载入 / 重新应用 / 保存」写进 ucf_navcmd.txt，插件 0.5 s 内执行。"""
        name = self.selected_pack()
        if not name:
            self.set_status("先选一个测试包（或点「新建测试包」）")
            return
        if not pack_id_ok(name):
            self.set_status("包名只能用英文字母、数字、下划线（_）和短横线（-）：%s" % name)
            return
        fp = pack_target_fp(name) if self.pack_only.get() else ""
        if self.pack_only.get() and not fp:
            fp = self.selected_fp()
        try:
            seq = write_nav_cmd(cmd, name, fp)
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.persist("测试包")
        running = game_running()
        act = {"apply": "载入", "reload": "重新应用", "save": "保存"}.get(cmd, cmd)
        short = name.split("/")[-1]
        if running:
            self.set_status("已发送 #%d：%s %s；游戏日志看 navcmd / naved" % (seq, act, name))
        else:
            self.set_status("游戏没开：已选中 %s，点「开始游戏」生效" % short)

    def clear_pack_map(self):
        name = self.selected_pack()
        if not name:
            self.set_status("先选一个测试包")
            return
        fp = pack_target_fp(name) or self.selected_fp()
        if not fp:
            self.set_status("不知道这张图的指纹：先在右侧选一张地图")
            return
        if not messagebox.askyesno(
                "清空当前图",
                "把测试包 %s 里 %s 的路线清成「空白底图」？\n"
                "（grow 包会保留 grow：清的是点，不降级成借槽位）\n"
                "只重写 packs\\%s\\%s.txt，不动正式版 nav\\。"
                % (name.split("/")[-1], fp, name.replace("/", "\\"), fp),
                parent=self):
            return
        pdir = pack_dir(name)
        txt = os.path.join(pdir, fp + ".txt")
        summ = pack_summary(name, fp)
        keep_grow = bool(pack_manifest(name).get("grow") or summ["grow"])
        try:
            os.makedirs(pdir, exist_ok=True)
            with open(txt, "w", encoding="utf-8", newline="\n") as f:
                f.write("# ucf-navedit v1 fp=%s\nblank\n" % fp)
                if keep_grow:
                    f.write("grow\n")      # 清空只清点，不把 grow 模式降级成 blank
            with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
                f.write("")
            man = pack_manifest(name)
            man.setdefault("name", name.split("/")[-1])
            man.setdefault("folder", name.replace("\\", "/").split("/")[0])
            man.setdefault("fp", fp)
            if "level" not in man:
                man["level"] = self.map_disp.get(self.opt_map.get(), ("", "", ""))[0]
            man["blank"] = True
            man["grow"] = keep_grow
            man["cleared"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8",
                      newline="\n") as f:
                json.dump(man, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except OSError as exc:
            self.set_status("清空失败：%s" % exc)
            return
        self.send_pack_cmd("apply")
        self.set_status("已清空 %s / %s：进图后从 0 画（Ctrl+Shift+N 加点）" % (name, fp))

    def default_pack_name(self, lv, fp):
        r"""空白包默认名：地图英文场景名 + 当前日期时间，如 TransportShip_20261119_213512。

        插件是 C + ANSI 路径，包里不能有中文，所以用场景名（《地图对照表》里那一列）；
        中文名照旧写进 manifest 的 label，界面上显示的仍是中文。
        """
        base = map_scene(lv, fp)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        return "%s_%s" % (base[:48 - len(stamp) - 1], stamp)

    def ask_blank_pack_name(self, lab, lv, fp):
        r"""新建空白包的名字弹窗；点「创建」返回包名，取消返回空串。"""
        default = self.default_pack_name(lv, fp)
        top = ctk.CTkToplevel(self)
        top.title("新建空白测试包")
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)   # 控制台置顶时别把弹窗藏到后面

        def grab():
            try:
                if top.winfo_exists():
                    top.grab_set()
            except tk.TclError:
                pass

        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, grab)
        top.bind("<Escape>", lambda _e: top.destroy())

        out = {"name": "", "grow": False, "seed": False}

        ctk.CTkLabel(top, text="新建空白测试包", font=("Microsoft YaHei UI", 17, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 0))
        ctk.CTkLabel(
            top,
            text="进图后原生路点全部禁用、自动铺点也一起关掉，人机只走你自己画的路线。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=460).pack(fill="x", padx=18, pady=(4, 10))

        # 新建方式：blank（借槽位） / grow（真·新建，空底图） / seed（原版全量复制 + grow）
        mode = {"grow": False, "seed": False}
        ctk.CTkLabel(top, text="新建方式", font=FONT_S, text_color="#9aa0a6",
                     anchor="w").pack(fill="x", padx=20, pady=(2, 4))
        seg = ctk.CTkSegmentedButton(
            top, values=["复用原生槽位（blank）", "真·新建节点（grow）", "复制原版路点（seed）"],
            font=FONT_S, height=32)
        seg.set("复用原生槽位（blank）")
        seg.pack(fill="x", padx=18)
        mode_hint = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6",
                                 anchor="w", justify="left", wraplength=460)
        mode_hint.pack(fill="x", padx=20, pady=(4, 10))

        grid = ctk.CTkFrame(top, fg_color="transparent")
        grid.pack(fill="x", padx=14)
        cells = [("地图", "%s（%s）" % (lab, lv)), ("建好后的效果", "空白底图 · 从 0 画路线")]
        effect_lbl = [None]
        for i, (k, v) in enumerate(cells):
            cell = ctk.CTkFrame(grid, corner_radius=7, fg_color="#262626",
                                border_width=1, border_color="#383838")
            cell.grid(row=0, column=i, sticky="nsew", padx=4, pady=4)
            ctk.CTkLabel(cell, text=k, font=FONT_S, text_color="#9aa0a6",
                         anchor="w").pack(fill="x", padx=10, pady=(6, 0))
            lbl = ctk.CTkLabel(cell, text=v, font=("Microsoft YaHei UI", 13, "bold"),
                               anchor="w")
            lbl.pack(fill="x", padx=10, pady=(0, 6))
            if k == "建好后的效果":
                effect_lbl[0] = lbl
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)

        def on_mode(_v=None):
            name = str(seg.get())
            seed = name.startswith("复制")
            grow = name.startswith("真") or seed
            mode["grow"] = grow
            mode["seed"] = seed
            if seed:
                text = ("seed：把这张图的原版点 + 边整份复制进包里，再用 grow 新建；"
                        "等于「原版底图 + 随便加点」，不受原生点数限制。")
            elif grow:
                text = ("grow：原生点照样标死，但路线点用 PointGraph.AddNode 新建，"
                        "点数不受原生点数限制（同一张图只建一次，改点集要重进图）。")
            else:
                text = ("blank：原生点标死后，路线点借用这些腾出来的槽位；"
                        "点数不能超过原生点数，抽到没借到的槽位会站住。")
            mode_hint.configure(text=text)
            if effect_lbl[0] is not None:
                effect_lbl[0].configure(
                    text=("原版复制 · 新建节点" if seed else
                          "空白底图 · 新建节点" if grow else "空白底图 · 借原生槽位"))

        seg.configure(command=on_mode)
        on_mode()

        ctk.CTkLabel(top, text="包名", font=FONT_S, text_color="#9aa0a6",
                     anchor="w").pack(fill="x", padx=20, pady=(12, 2))
        var = tk.StringVar(value=default)
        entry = ctk.CTkEntry(top, textvariable=var, font=FONT, height=38,
                             placeholder_text="给这个包起个名字")
        entry.pack(fill="x", padx=18)
        hint = ctk.CTkLabel(top, text="", font=FONT_S, anchor="w",
                            justify="left", wraplength=460)
        hint.pack(fill="x", padx=20, pady=(4, 0))
        path = ctk.CTkLabel(top, text="", font=("Consolas", 11),
                            text_color="#6f767d", anchor="w")
        path.pack(fill="x", padx=20, pady=(2, 0))
        folder_dir = map_folder(lv, fp)

        def refresh(*_a):
            name = var.get().strip()
            if not name:
                msg, color = "还没起名", "#9aa0a6"
            elif not pack_name_ok(name):
                msg, color = "名字里只能用英文字母、数字、下划线（_）和短横线（-）", "#ff8f8f"
            elif os.path.isdir(os.path.join(folder_dir, name)):
                msg, color = "已有同名测试包：创建会覆盖这张图的旧路线", "#ffc46b"
            else:
                msg, color = "名字可以用", "#69db7c"
            hint.configure(text=msg, text_color=color)
            path.configure(text="保存到  packs\\%s\\%s\\" % (folder_dir, name or "…"))

        var.trace_add("write", refresh)
        refresh()

        def ok(_e=None):
            name = var.get().strip()
            if not pack_name_ok(name):
                refresh()
                entry.focus_set()
                self.bell()
                return
            out["name"] = name
            out["grow"] = bool(mode["grow"])
            out["seed"] = bool(mode["seed"])
            top.destroy()

        btns = ctk.CTkFrame(top, fg_color="transparent")
        btns.pack(fill="x", padx=18, pady=(12, 16))
        ctk.CTkButton(btns, text="创建测试包", width=112, height=34, font=FONT,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=ok).pack(side="right")
        ctk.CTkButton(btns, text="取消", width=76, height=34, font=FONT_S,
                      fg_color="transparent", border_width=1, border_color="#4a4a4a",
                      hover_color="#2e2e2e", command=top.destroy).pack(
            side="right", padx=(0, 8))

        entry.bind("<Return>", ok)
        entry.bind("<KP_Enter>", ok)
        top.update_idletasks()
        w = max(520, top.winfo_reqwidth())
        h = top.winfo_reqheight()
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        top.geometry("%dx%d+%d+%d" % (w, h, max(x, 0), max(y, 0)))
        entry.select_range(0, "end")
        entry.focus_set()
        self.wait_window(top)
        return dict(out)

    def create_blank_pack(self):
        r"""给当前选中的地图建一份「空白底图」测试包。

        文件里的 `blank` 让插件先把这张图的原生路点全部禁用，再套用包里自己画的
        node add / edge add；`nogen.txt` 同时关掉插件的自动铺路点。这样进图后
        人机只剩你画的路线，适合从 0 设计、验证。
        """
        disp = self.opt_map.get()
        if disp not in self.map_disp:
            self.set_status("先选一张有指纹的图，再建空白包")
            return
        lv, lab, fp = self.map_disp[disp]
        got = self.ask_blank_pack_name(lab, lv, fp)
        if not got or not got.get("name"):
            return
        name = got["name"]
        seed = bool(got.get("seed"))
        grow = bool(got.get("grow")) or seed
        # 0 点图（暴风）：没有原生槽位、也没有原版点可复制，只有 grow 能用
        if fp == "n0-0000000000000000":
            if seed:
                messagebox.showwarning(
                    "0 点图没有原版点可复制",
                    "暴风原生 0 个路点，没有可播种的原版数据；改选「真·新建节点（grow）」",
                    parent=self)
                return
            if not grow:
                messagebox.showwarning(
                    "这张图只能建 grow 包",
                    "暴风原生 0 个路点，没有可复用的节点槽位；\n"
                    "只有「真·新建节点（grow）」能在 0 点图上建路线。", parent=self)
                return
        seed_lines_, sn, se = (seed_lines(fp) if seed else (None, 0, 0))
        if seed and not seed_lines_:
            messagebox.showwarning(
                "没有原版点图数据",
                "① 备份版 maps\\ 里找不到 %s 的原生点图，没法播种。\n"
                "先用 navdata.py freeze 生成备份版，或改用「真·新建节点（grow）" % fp,
                parent=self)
            return
        folder = map_folder(lv, fp)
        pid = "%s/%s" % (folder, name)
        pdir = pack_dir(pid)
        tpath = os.path.join(pdir, fp + ".txt")
        if os.path.isfile(tpath) and not messagebox.askyesno(
                "覆盖测试包", "测试包 %s 里已经有 %s.txt，覆盖成空白底图？" % (name, fp),
                parent=self):
            return
        try:
            os.makedirs(pdir, exist_ok=True)
            with open(tpath, "w", encoding="utf-8", newline="\n") as f:
                if seed:
                    f.write("# ucf-navedit v1 fp=%s\n# seed: 原版点图全量重放\nblank\ngrow\n" % fp)
                    for ln in seed_lines_:
                        f.write(ln + "\n")
                else:
                    f.write("# ucf-navedit v1 fp=%s\nblank\n" % fp)
                    if grow:
                        f.write("grow\n")
            with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
                f.write("")                       # 存在即关掉自动铺点
            man = {
                "name": name, "folder": folder, "level": lv, "label": lab, "fp": fp,
                "created": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": ("console-seed" if seed else
                           "console-grow" if grow else "console-blank"),
                "blank": True, "grow": bool(grow), "seed": bool(seed),
                "note": ("原版播种测试包：%d 点 + %d 边全量复制，再按 grow 新建（可继续加点）" % (sn, se)
                         if seed else
                         "grow 测试包：原生点全禁用，路线点按 AddNode 新建（数量不受原生点数限制）"
                         if grow else
                         "空白底图测试包：原生点全禁用 + nogen.txt 关自动铺点；路线自己画"),
            }
            with open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8",
                      newline="\n") as f:
                json.dump(man, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except OSError as exc:
            self.set_status("建包失败：%s" % exc)
            return
        values = self._pack_values()
        self.opt_pack.configure(values=values)
        self.opt_pack.set(self.disp_of(pid))
        self.seg_mode.set("测试包（packs）")
        self.pack_on.set(True)
        self.on_pack_change()
        msg = "已建%s测试包 %s（%s · %s）" % (
            "原版播种" if seed else (" grow" if grow else "空白"), name, lab, folder)
        if game_running():
            try:
                write_nav_cmd("apply", pid, fp)
                msg += "，已发送到运行中的游戏"
            except OSError:
                pass
        self.set_status(msg)

    # ---- 状态 ----
    def set_status(self, text):
        self.dot.configure(text=text)

    def refresh_status(self):
        running = game_running()
        self.refresh_game_button(running)
        lines = tail_log(6)
        self.logbox.configure(state="normal")
        self.logbox.delete("1.0", "end")
        self.logbox.insert("end", "\n".join(lines) if lines else "（还没有日志）")
        self.logbox.configure(state="disabled")
        if not self.dot.cget("text"):
            self.set_status("配置：%s" % ("已读取" if os.path.isfile(CFG_PATH) else "未找到，用默认值"))
        self.refresh_export_info()
        if hasattr(self, "wp_meta"):
            self.refresh_wp_status()
        self.refresh_launch_strip(running)
        self.after(4000, self.refresh_status)

    def refresh_game_button(self, running=None):
        r"""底部「开始游戏」按钮：文案和颜色跟着版本走，别让用户猜。"""
        if not hasattr(self, "btn_game"):
            return
        if running is None:
            running = game_running()
        if running:
            self.btn_game.configure(text="游戏运行中", state="disabled",
                                    fg_color="#3a3f47", hover_color="#49505a")
            return
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        if not bool(self.master_var.get()):
            # 总开关关 = 插件加载但待机（plugin.c: loaded but idle）
            self.btn_game.configure(text="开始游戏 · 插件已关（原版）", state="normal",
                                    fg_color="#3a3f47", hover_color="#49505a")
        elif pk.get("on") and pk.get("name"):
            self.btn_game.configure(text="开始游戏 · 测试包 %s" % pk["name"].split("/")[-1],
                                    state="normal",
                                    fg_color="#a86a12", hover_color="#bf7c17")
        else:
            self.btn_game.configure(text="开始游戏 · 正式版（nav）", state="normal",
                                    fg_color="#2f6fdb", hover_color="#255bb4")

    # ---- 启动条件条 / 测试包预检（2026-11-19 用户要求）---------------
    # 版本选择原本只活在「人机路点」① 卡里，底部按钮又不带状态；
    # 这里把「这次启动加载什么」常驻到按钮上方，测试包再补一道预检。
    def launch_strip_info(self):
        r"""当前启动条件的文案；与 game_env() 同一套判断：总开关 → 测试包 → 正式版。"""
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        if not bool(self.master_var.get()):
            return {"mode": "off", "badge": "插件已关",
                    "title": "本次启动 = 原版（插件待机）",
                    "sub": "总开关关闭：插件加载但不动作，不读 nav、不出 F2 菜单",
                    "go": "去打开"}
        if not (pk.get("on") and pk.get("name")):
            return {"mode": "official", "badge": "正式版",
                    "title": "本次启动加载 ③ 部署版 nav",
                    "sub": "游戏内只读：改动不落盘；要改数据请用 ② 开发版 / ④ 测试包",
                    "go": "查看版本"}
        name = pk["name"]
        short = name.split("/")[-1]
        man = pack_manifest(name)
        summ = pack_summary(name, pack_target_fp(name))
        ops = summ["nadd"] + summ["ndel"] + summ["eadd"] + summ["edel"]
        blank = bool(man.get("blank") or summ["blank"])
        grow = bool(man.get("grow") or summ["grow"])
        seed = bool(man.get("seed"))
        kind = ("原版播种" if seed else
                "真·新建" if grow else ("空白底图" if blank else "增量"))
        label = str(man.get("label") or pk.get("label") or pk.get("map") or "")
        scope = ("只对 %s 生效" % label) if (pk.get("only_map") and label) else "全部地图生效"
        title = "%s · %s · %s" % (self.disp_of(name) or short, kind, scope)
        if seed:
            sub = "包内 %d 处改动；原版点+边全量重放，按 AddNode 新建（可继续加点）" % ops
        elif grow and ops == 0:
            sub = "包内 0 处改动：原生点全禁用且不新建节点，人机没有可走路点"
        elif grow:
            sub = "包内 %d 处改动；原生点全禁用，节点按 AddNode 新建（不受原生点数限制）" % ops
        elif blank and ops == 0:
            sub = "包内 0 处改动：进图后原生点全禁用，人机没有可走路点，不会移动"
        elif blank:
            sub = "包内 %d 处改动；原生点全禁用，人机只走包里画的路线" % ops
        else:
            sub = "包内 %d 处改动，套在原生点上执行" % ops
        return {"mode": "test", "badge": "测试包", "title": title, "sub": sub,
                "go": "去人机路点改"}

    def refresh_launch_strip(self, running=None):
        r"""把启动条件画到按钮上方；运行中显示启动瞬间的快照，改选只影响下次。"""
        if not hasattr(self, "strip"):
            return
        if running is None:
            running = game_running()
        if running:
            if getattr(self, "_strip_run", None) is None:
                # 外部双击 exe 起的进程：没有 mod，更谈不上版本；单独说清楚
                info = {"mode": "off", "badge": "外部启动",
                        "title": "游戏在运行，但不是从本窗口启动的",
                        "sub": "直接双击 UnityCrossFire.exe 是原版（无 mod）；要加载版本请关掉游戏再点底部按钮",
                        "go": "去人机路点"}
            else:
                info = dict(self._strip_run)
                info["badge"] = "运行中 · " + info["badge"]
                info["sub"] += " · 改版本只影响下次启动"
        else:
            self._strip_run = None
            info = self.launch_strip_info()
        # mode -> (外框, 底色, 徽标底, 徽标字)
        style = {
            "off": ("#5a3434", "#2a1a1a", "#301c1c", "#ff9d9d"),
            "test": ("#7a5a17", "#2c2310", "#3a2c0d", "#f7cd74"),
            "official": ("#3a3f47", "#232323", "#16233a", "#9cc3ff"),
        }[info["mode"]]
        self.strip.configure(border_color=style[0], fg_color=style[1])
        self.strip_badge.configure(text=info["badge"], fg_color=style[2],
                                   text_color=style[3],
                                   width=max(78, 15 * len(info["badge"]) + 14))
        self.strip_title.configure(text=info["title"],
                                   text_color="#f7cd74" if info["mode"] == "test" else "#f0f0f0")
        self.strip_sub.configure(text=info["sub"])
        self.strip_go.configure(text=info["go"])
        self.refresh_game_button(running)

    def on_strip_go(self):
        r"""启动条右侧按钮：插件关着就先打开；否则跳到人机路点 ① 卡。"""
        if not bool(self.master_var.get()):
            self.master_var.set(True)
            self.on_master()
            return
        self.jump_to_pick()

    def jump_to_pick(self):
        r"""跳到「人机路点」页，滚回 ① 选图与数据并闪一下边框。"""
        try:
            self.tabview.set("人机路点")
        except Exception:
            pass
        body = getattr(self, "wp_body", None)
        if body is not None:
            try:
                body._parent_canvas.yview_moveto(0.0)   # noqa: SLF001  CTk 内部画布
            except Exception:
                pass
        card = getattr(self, "card_pick", None)
        if card is None:
            return
        try:
            card.configure(border_width=2, border_color="#f5b942")
        except Exception:
            return

        def clear():
            try:
                if card.winfo_exists():
                    card.configure(border_width=0, border_color="#383838")
            except Exception:
                pass

        self.after(1600, clear)

    def preflight_start(self):
        r"""测试包模式的启动预检；返回 True = 继续启动。

        只拦「总开关开 + 测试包选中」的启动；正式版和插件待机直接放行。
        顺带把空包风险提前说出来：空白底图 + 包内 0 处改动 = 人机没有可走路点。
        """
        pk = self.pack_dict()
        name = pk.get("name") or ""
        man = pack_manifest(name)
        summ = pack_summary(name, pack_target_fp(name))
        ops = summ["nadd"] + summ["ndel"] + summ["eadd"] + summ["edel"]
        blank = bool(man.get("blank") or summ["blank"])
        grow = bool(man.get("grow") or summ["grow"])
        seed = bool(man.get("seed"))
        label = str(man.get("label") or pk.get("label") or pk.get("map") or "")
        level = str(man.get("level") or pk.get("map") or "")
        where = ("%s（%s）" % (label, level)) if (label and level) else (label or level or "（未知）")
        scope = "只对这张图生效" if pk.get("only_map") else "全部地图生效"
        if seed:
            alert = ("原版播种：包里是这张图原版点+边的全量副本（%d 处），"
                     "按 grow 新建；原生点全部禁用，之后可以继续加点。" % ops)
        elif grow and ops == 0:
            alert = ("注意：真·新建（grow）+ 包内 0 处改动。进图后原生点全部禁用、"
                     "又不会新建节点，人机没有可走路点，不会移动。")
        elif grow:
            alert = ("真·新建（grow）：原生点全部禁用，节点按 AddNode 新建，"
                     "包内 %d 处改动不受原生点数限制。" % ops)
        elif blank and ops == 0:
            alert = ("注意：空白底图 + 包内 0 处改动。进图后原生点全部禁用，"
                     "人机没有可走路点，不会移动。")
        elif blank:
            alert = "空白底图：原生点全部禁用，人机只走包内 %d 处改动画出的路线。" % ops
        else:
            alert = "增量改动：包内 %d 处改动，套在原生点上执行。" % ops

        top = ctk.CTkToplevel(self)
        top.title("启动预检 · 测试包模式")
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)   # 控制台置顶时别把预检藏到后面

        def grab():
            try:
                if top.winfo_exists():
                    top.grab_set()
            except tk.TclError:
                pass

        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, grab)   # CTkToplevel 还没 viewable 时等它映射出来
        top.bind("<Escape>", lambda _e: top.destroy())

        ctk.CTkLabel(top, text="启动预检 · 测试包模式",
                     font=("Microsoft YaHei UI", 17, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 0))
        ctk.CTkLabel(top, text="正式版不会弹这一步；确认后才会带 UCF_PACK / UCF_FP 启动游戏。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=470).pack(fill="x", padx=18, pady=(4, 10))

        grid = ctk.CTkFrame(top, fg_color="transparent")
        grid.pack(fill="x", padx=14)
        cells = [("数据版本", "④ 测试包（packs）"),
                 ("测试包", self.disp_of(name) or name.split("/")[-1]),
                 ("生效地图", where), ("生效范围", scope)]
        for i, (k, v) in enumerate(cells):
            cell = ctk.CTkFrame(grid, corner_radius=7, fg_color="#262626",
                                border_width=1, border_color="#383838")
            cell.grid(row=i // 2, column=i % 2, sticky="nsew", padx=4, pady=4)
            ctk.CTkLabel(cell, text=k, font=FONT_S, text_color="#9aa0a6",
                         anchor="w").pack(fill="x", padx=10, pady=(6, 0))
            ctk.CTkLabel(cell, text=v, font=("Microsoft YaHei UI", 13, "bold"),
                         anchor="w", justify="left", wraplength=210).pack(
                fill="x", padx=10, pady=(0, 6))
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)

        warn = ctk.CTkFrame(top, corner_radius=7, fg_color="#241511",
                            border_width=1, border_color="#6b3d2c")
        warn.pack(fill="x", padx=18, pady=(6, 0))
        ctk.CTkLabel(warn, text=alert, font=FONT_S, text_color="#ffb59d",
                     anchor="w", justify="left", wraplength=440).pack(
            fill="x", padx=10, pady=8)

        mute_var = tk.BooleanVar(value=self._mute_preflight)
        ctk.CTkCheckBox(top, text="本次控制台会话不再提示（启动条仍会一直显示）",
                        variable=mute_var, font=FONT_S,
                        checkbox_width=18, checkbox_height=18).pack(
            anchor="w", padx=20, pady=(10, 0))

        result = {"go": False}

        def go():
            result["go"] = True
            if mute_var.get():
                self._mute_preflight = True
            top.destroy()

        btns = ctk.CTkFrame(top, fg_color="transparent")
        btns.pack(fill="x", padx=18, pady=(12, 16))
        ctk.CTkButton(btns, text="确认启动", width=104, height=34, font=FONT,
                      fg_color="#a86a12", hover_color="#bf7c17",
                      text_color="#fff2d6", command=go).pack(side="right")
        ctk.CTkButton(btns, text="先去人机路点", width=118, height=34, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: (top.destroy(), self.jump_to_pick())).pack(
            side="right", padx=(0, 8))
        ctk.CTkButton(btns, text="取消", width=76, height=34, font=FONT_S,
                      fg_color="transparent", border_width=1, border_color="#4a4a4a",
                      hover_color="#2e2e2e", command=top.destroy).pack(
            side="right", padx=(0, 8))

        top.update_idletasks()
        w = max(520, top.winfo_reqwidth())
        h = top.winfo_reqheight()
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        top.geometry("%dx%d+%d+%d" % (w, h, max(x, 0), max(y, 0)))
        self.wait_window(top)
        return result["go"]

    # ---- 动作 ----
    def game_env(self):
        r"""启动游戏的环境变量 + 一句人话说明（「开始游戏」和「车测」共用）。

        UCF_MOD=1 是通行证。四版路径也在这里定：
          UCF_EXPORT_DIR     -> ④ 测试版 vis（Ctrl+E 导出、navmesh、_seen_ 都写这里）
          UCF_PACK_DIR       -> ④ 测试版 packs（测试包）
          UCF_NAV_READONLY=1 -> 没选测试包时，游戏内保存不写 ③ 部署版 nav
        """
        env = dict(os.environ)
        env["UCF_MOD"] = "1"
        env["UCF_EXPORT_DIR"] = TEST_VIS
        env["UCF_PACK_DIR"] = PACKS
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        enabled = bool(self.master_var.get()) if hasattr(self, "master_var") else True
        note = "mod 已启用"
        if not enabled:
            # 总开关关 = 插件加载但待机（plugin.c）；状态行别再写「mod + 测试包」
            note = "插件总开关关闭：插件待机（不读 nav、不出菜单）"
        elif pk.get("on") and pk.get("name"):
            env["UCF_PACK"] = pk["name"]           # 地图文件夹/包名，插件按子目录读
            env.pop("UCF_NAV_READONLY", None)      # 测试包允许游戏内保存
            note = "mod + 测试包 %s" % pk["name"].split("/")[-1]
            if pk.get("only_map") and pk.get("fp"):
                env["UCF_FP"] = pk["fp"]
                env["UCF_FPLABEL"] = pk.get("label") or pk["map"]
                note += "（只对 %s）" % (pk.get("label") or pk["map"])
        else:
            env["UCF_NAV_READONLY"] = "1"          # 正式版：游戏内不许直接写 ③
            note = "mod 已启用（正式版：游戏内改动不落盘，改数据请用 ②/④）"
        return env, note

    def launch_game(self):
        if not os.path.isfile(GAME_EXE):
            self.set_status("找不到 %s" % GAME_EXE)
            return
        # 2026-11-19：测试包模式先过一道预检（正式版 / 插件待机直接放行）
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        if (bool(self.master_var.get()) and pk.get("on") and pk.get("name")
                and not self._mute_preflight):
            if not self.preflight_start():
                self.set_status("已取消启动（测试包 %s）" % pk.get("name"))
                return
        # 通行证：只有这里启动才会带上 UCF_MOD=1，插件据此决定是否工作
        env, note = self.game_env()
        try:
            subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE), env=env)
            self._strip_run = self.launch_strip_info()   # 运行中显示启动瞬间的快照
            self.set_status("游戏已启动（%s）" % note)
        except OSError as exc:
            self.set_status("启动失败：%s" % exc)
        self.after(1500, self.refresh_status)

    def open_workbench(self):
        r"""路点工作台只读：直接起 navserver（新控制台窗口看日志，关掉即停止）。"""
        if not os.path.isfile(NAVSERVER):
            self.set_status("找不到 navserver.py")
            return
        env = dict(os.environ)
        env["UCF_PROFILE"] = "dev"
        try:
            subprocess.Popen([_python(), "-u", NAVSERVER], cwd=HERE, env=env,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.set_status("已打开路点工作台（只读查看）")
        except OSError as exc:
            self.set_status("打不开路点工作台：%s" % exc)


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    if not os.path.isdir(DEPLOY):
        print("部署端不存在：" + DEPLOY)
        return 1
    App().mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
