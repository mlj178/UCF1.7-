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
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox, simpledialog

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
    r"""插件只认 ASCII 包名（fopen/CreateDirectoryA），先在控制台挡掉。"""
    return bool(re.match(r"^[A-Za-z0-9_-]{1,48}$", name or ""))


def pack_manifest(name):
    r"""读 packs/<包名>/manifest.json；没有就返回空 dict。"""
    try:
        with open(os.path.join(PACKS, name, "manifest.json"), "r", encoding="utf-8") as f:
            doc = json.load(f)
        return doc if isinstance(doc, dict) else {}
    except (OSError, ValueError):
        return {}


def pack_txt(name, fp=""):
    r"""包内某张图的 txt；不给指纹就取第一个。"""
    d = os.path.join(PACKS, name)
    if fp:
        p = os.path.join(d, fp + ".txt")
        return p if os.path.isfile(p) else ""
    try:
        files = sorted(fn for fn in os.listdir(d) if fn.endswith(".txt") and not fn.startswith("_"))
    except OSError:
        return ""
    return os.path.join(d, files[0]) if files else ""


def pack_target_fp(name):
    r"""这个包针对哪张图：manifest.fp 优先，其次 <指纹>.txt 的文件名。"""
    fp = str(pack_manifest(name).get("fp") or "")
    if fp:
        return fp
    p = pack_txt(name)
    if p:
        base = os.path.basename(p)[:-4]
        if re.match(r"^n\d+-[0-9a-fA-F]{16}$", base):
            return base
    return ""


def pack_summary(name, fp=""):
    r"""包内容摘要：空白底图？几个加点 / 删点 / 加边 / 删边、最后写入时间。"""
    p = pack_txt(name, fp)
    out = {"path": p, "blank": False, "nadd": 0, "ndel": 0,
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
    with open(tmp, "w", encoding="ascii", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, NAVCMD)
    return _CMD_SEQ


def load_packs():
    r"""packs\ 下有哪些测试包（目录名 = 包名，只认 ASCII 名）。"""
    try:
        return sorted(d for d in os.listdir(PACKS) if os.path.isdir(os.path.join(PACKS, d)))
    except OSError:
        return []

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
        packs = len([d for d in os.listdir(pk_dir) if os.path.isdir(os.path.join(pk_dir, d))])
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
FONT_S = ("Microsoft YaHei UI", 11)
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
    ("手动", "只有你按键时才发生；下面「自动铺设」是进图时自动补，不按键也会跑", [
        ("editor", "允许游戏内编辑", "Ctrl+1 进入编辑模式，放蹲守点/改路点", True),
        ("collect_only", "只读采集", "只导出路点，绝不创建任何游戏对象", False),
        # 2026-11-18：自动铺设从工作台搬回控制台「手动」页（用户要求）
        ("auto_waypoints", "自动铺路点 + 连线", "进图时这张图没有 PointGraph（没路点）才触发：沿可走面铺点并连边；已有路点的图不动", True),
        ("auto_crouch", "自动补蹲守点", "没有蹲守点的图自动补一批 Bot_CrouchPos；已有蹲守点的图不动", True),
        ("ghost_areas", "自动造幽灵守区", "没有幽灵守区/守点的图凭空造一套；已有守区的图不动", True),
    ]),
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
                 "测试包模式、四版数据的路径 / 部署 / 还原 / 校验：切到「测试数据」「数据」页。\n"
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

        self.stat = ctk.CTkFrame(self, corner_radius=10)
        self.stat.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
        top = ctk.CTkFrame(self.stat, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(10, 2))
        ctk.CTkLabel(top, text="上次运行", font=("Microsoft YaHei UI", 14, "bold")).pack(side="left")
        self.dot = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
        self.dot.pack(side="right")
        self.logbox = ctk.CTkTextbox(self.stat, height=104, font=("Consolas", 11),
                                     fg_color="#141414", activate_scrollbars=True)
        self.logbox.pack(fill="x", padx=14, pady=(2, 12))

        # 地图 / 可视化 / 导出 / 手动 / 测试数据 / 数据 / 车测 —— 全部页签切换，上方不再压一块常驻面板。
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
            elif title == "手动":
                self.build_manual_tab(tab, hint, items)  # 按键开关 + 自动铺设（进图自动补）
            elif title == "可视化":
                self.build_vis_tab(tab, hint, items)     # 总开关 + 九类数据（勾选）
            else:
                self.build_group_tab(tab, hint, items)
        # 人机路点必须排在「测试数据」前面：页签顺序 = 添加顺序。
        # 但它的控件要读 opt_pack / opt_map，所以先占位，等测试数据页建完再填内容。
        wp_tab = self.tabview.add("人机路点")               # SyPB 式现场编辑入口
        self.build_pack_tab(self.tabview.add("测试数据"))   # 正式版 / 测试包 + 只对哪张图生效
        self.build_waypoint_tab(wp_tab)
        self.build_data_tab(self.tabview.add("数据"))       # 四版路径/时间 + 部署/还原/校验
        self.build_autotest_tab(self.tabview.add("车测"))   # 不用鼠标键盘：插件自己在进程内切图
        self.tab_titles += ["人机路点", "测试数据", "数据", "车测"]

        # 回到上次停留的页签；记住的页签已经不存在（改版删页）就落在默认第一页
        saved_tab = str(self.ui.get("tab") or "")
        if saved_tab in self.tab_titles:
            self.tabview.set(saved_tab)
            self.on_tab(saved_tab, persist=False)

        self.refresh_status()
        self.after(4000, self.refresh_status)

    # ---- 页签内容：一组开关 = 一页 ----
    def switch_card(self, parent, key, label, desc, default):
        r"""一个开关 + 一行说明；「可视化」「手动」等页共用这份样式。"""
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

    # ---- 「手动」页：按键开关 + 自动铺设（进图时自动补，不按键也跑） ----
    def build_manual_tab(self, tab, hint, items):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        auto_keys = ("auto_waypoints", "auto_crouch", "ghost_areas")
        manual = [it for it in items if it[0] not in auto_keys]
        auto = [it for it in items if it[0] in auto_keys]
        for key, label, desc, default in manual:
            self.switch_card(body, key, label, desc, default)
        if auto:
            ctk.CTkLabel(body, text="自动铺设", font=("Microsoft YaHei UI", 12, "bold"),
                         anchor="w").pack(fill="x", padx=12, pady=(14, 0))
            ctk.CTkLabel(body, text="进图时自动补数据：只补缺的，不覆盖已有的；改完重启游戏生效。",
                         font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                         wraplength=620).pack(fill="x", padx=12, pady=(2, 0))
            for key, label, desc, default in auto:
                self.switch_card(body, key, label, desc, default)
            ctk.CTkLabel(body, text="录制（F9）仍在游戏里；路线编辑在游戏内完成，工作台只读查看。",
                         font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                         wraplength=620).pack(fill="x", padx=12, pady=(8, 12))

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
        self.exp_path = ctk.CTkLabel(box, text="", font=("Consolas", 11),
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
        tb = ctk.CTkTextbox(box, height=height, font=("Consolas", 11),
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

    # ---- 测试数据页：正式版 / 测试包 + 只对哪张图生效（S3）----
    def build_pack_tab(self, tab):
        r"""启动前在这里选：这次进图读 nav\（正式）还是 packs\<包名>（测试），
        以及只让哪一张图的路线生效。选完点「开始游戏」，两个值以环境变量
        （UCF_PACK / UCF_FP）递给游戏进程；选了测试包也不会动正式版一个文件。"""
        self.maps = load_maps()                 # [(level, 中文名, 指纹)]
        self.map_disp = {("%s（%s）" % (lab, lv)): (lv, lab, fp) for lv, lab, fp in self.maps}
        pk = self.cfg.get("pack") if isinstance(self.cfg.get("pack"), dict) else {}
        self.pack_on = tk.BooleanVar(value=bool(pk.get("on", False)))
        self.pack_only = tk.BooleanVar(value=bool(pk.get("only_map", True)))
        self.pack_name = str(pk.get("name") or "")
        self.pack_map = str(pk.get("map") or (self.maps[0][0] if self.maps else ""))

        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text="选「测试包」= 进图读 ④ navdata\\test\\packs\\<包名> 里的路线；"
                              "选「正式版」= 读 ③ 部署版 nav\\。\n"
                              "进图后直接在游戏里画：Ctrl+Shift+N 加点 · Ctrl+Shift+A 选起点 · "
                              "Ctrl+Shift+J 连/断边 · Ctrl+Shift+D 删点 · Ctrl+Shift+Z 撤销；改完自动存盘。\n"
                              "「新建空白包」= 原生点全禁用后从 0 画；「载入到游戏」= 不重启就切到当前包。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=620).pack(fill="x", padx=12, pady=(8, 2))
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 0))
        self.seg_mode = ctk.CTkSegmentedButton(
            row, values=["正式版（nav）", "测试包（packs）"], font=FONT_S,
            command=lambda _v: self.on_pack_change())
        self.seg_mode.pack(side="left")
        self.seg_mode.set("测试包（packs）" if self.pack_on.get() else "正式版（nav）")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 0))
        ctk.CTkLabel(row, text="测试包", font=FONT, width=64, anchor="w").pack(side="left")
        pack_values = self._pack_values()
        self.opt_pack = ctk.CTkOptionMenu(row, values=pack_values, font=FONT_S,
                                          width=200, command=lambda _v: self.on_pack_change())
        self.opt_pack.pack(side="left", padx=(0, 6))
        if self.pack_name in pack_values:   # 上次选的包重启后接着选中（包被删了就落第一个）
            self.opt_pack.set(self.pack_name)
        ctk.CTkButton(row, text="刷新", width=56, font=FONT_S, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.refresh_packs).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="打开目录", width=80, font=FONT_S, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.open_packs_dir).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="新建空白包", width=96, font=FONT_S, fg_color="#2f6fdb",
                      hover_color="#255bb4",
                      command=self.create_blank_pack).pack(side="left")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 0))
        ctk.CTkCheckBox(row, text="只对这张图生效", variable=self.pack_only, font=FONT,
                        checkbox_width=20, checkbox_height=20,
                        command=self.on_pack_change).pack(side="left", padx=(0, 10))
        self.opt_map = ctk.CTkOptionMenu(
            row, values=list(self.map_disp) or ["（没有可测的路点图）"], font=FONT_S,
            width=240, command=lambda _v: self.on_pack_change())
        self.opt_map.pack(side="left")
        if self.pack_map:
            for disp, (lv, _lab, _fp) in self.map_disp.items():
                if lv == self.pack_map:
                    self.opt_map.set(disp)
                    break

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 0))
        ctk.CTkButton(row, text="载入到游戏", width=92, font=FONT_S, fg_color="#2f6fdb",
                      hover_color="#255bb4",
                      command=lambda: self.send_pack_cmd("apply")).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="重新应用", width=80, font=FONT_S, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=lambda: self.send_pack_cmd("reload")).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="保存路线", width=80, font=FONT_S, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.save_pack_now).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="清空当前图", width=92, font=FONT_S, fg_color="#8a4b1e",
                      hover_color="#a55d26",
                      command=self.clear_pack_map).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="回正式版", width=80, font=FONT_S, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.back_to_official).pack(side="left")

        self.lbl_pack = ctk.CTkLabel(box, text="", font=FONT_S, text_color="#c9d1d9",
                                     anchor="w", justify="left", wraplength=620)
        self.lbl_pack.pack(fill="x", padx=14, pady=(8, 0))
        ctk.CTkLabel(box, text="游戏运行中改完点「载入到游戏」立即生效；游戏没开时只是选中，点「开始游戏」生效。\n"
                              "「重新应用」= 重读 pack 文件（外部改过 txt 时用它）；「保存路线」= 让游戏把内存里的改动写回文件。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=620).pack(fill="x", padx=14, pady=(2, 0))

        ctk.CTkLabel(box, text="", font=FONT_S).pack(pady=1)
        self.on_pack_change(persist=False)

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

    def wp_type_counts(self):
        r"""当前选中地图的「场景组件」计数。

        normal/edges 来自 maps/*.json；守点/聚集区/蹲点/标签来自
        《地图对照表》第二张表（地图 JSON 不导这些组件）。
        """
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        doc, _path = find_map_doc(fp)
        counts = (doc or {}).get("counts") or {}
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        lv = self.map_disp.get(disp, ("", "", ""))[0]
        sc = self.wp_scene.get(lv, {})
        return {
            "normal": int(counts.get("nodes") or 0),
            "jump": int(sc.get("jump") or counts.get("jump") or 0),
            "crouch": int(sc.get("crouch") or counts.get("crouch") or 0),
            "guard": int(sc.get("guard") or counts.get("guard") or 0),
            "area": int(sc.get("area") or counts.get("area") or 0),
            "tag": int(sc.get("tag") or counts.get("tag") or 0),
            "spawn": int(counts.get("spawn") or 0),
            "box": None,
        }, doc, sc

    def build_waypoint_tab(self, tab):
        r"""控制台「人机路点」页。

        设计：docs/design/console-waypoint-tab.html。它不直接改游戏，
        只负责选图/包、写 ucf_mod.json 开关、给运行中的插件发 ucf_navcmd，
        并把节点/边/特征计数和最近 [naved] 日志显示出来。
        """
        self._wp_syncing = False
        self.wp_scene = load_scene_counts()
        self.wp_brush = str(self.feats.get("wp_brush") or "normal")
        if self.wp_brush not in ("normal", "jump", "crouch", "guard", "area", "tag"):
            self.wp_brush = "normal"
        self.wp_type_defs = [
            ("normal", "普通路点", "复用", "#4f8cff"),
            ("jump", "跳跃点", "新增", "#a78bfa"),
            ("crouch", "蹲守点", "复用", "#f59e0b"),
            ("guard", "守点", "复用", "#22d3ee"),
            ("area", "聚集区", "复用", "#f472b6"),
            ("tag", "标签区", "新增", "#84cc16"),
            ("spawn", "出生点", "只读", "#34d399"),
            ("box", "补给箱", "只读", "#facc15"),
        ]
        self.wp_type_btns = {}

        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(
            body,
            text="进游戏现场编辑：F2 打开路点菜单（长按 E 备用）；1-9 直选，小键盘 8/2 上下、5 确认、0 返回，左键/右键也可。\n"
                 "菜单打开时 W/A/S/D/空格仍可移动，Q/R/G/F/Tab 等会拦掉；选完 A 可走到 B 再按小键盘 5 连边。\n"
                 "按 F2 / 小键盘前先点一下游戏画面，让游戏窗口拿到焦点（控制台在前台时游戏收不到键）。\n"
                 "空白包=原生点全禁用；必须整图连通。只连主路还不够：孤立点、出生点、蹲守标记都可能让 Bot 取不到路。\n"
                 "markers 目前全局不分图，换图前先清掉别图的蹲守点；只测局部请用 ③ 正式版 + 先删几个远处点腾槽位。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(8, 2))

        # ① 选图与数据
        box = self.wp_card(body, "① 选图与数据", "④ 包只对一张图生效")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="数据版本", font=FONT_S,
                     text_color="#9aa0a6").pack(side="left", padx=(0, 6))
        self.wp_seg = ctk.CTkSegmentedButton(
            row, values=["④ 测试包", "③ 正式版"], font=FONT_S,
            command=lambda _v: self.apply_wp_selection())
        self.wp_seg.pack(side="left")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="测试包", font=FONT_S,
                     text_color="#9aa0a6").pack(side="left", padx=(0, 6))
        self.wp_pack = ctk.CTkOptionMenu(
            row, values=self._pack_values(), font=FONT_S, width=190,
            command=lambda _v: self.apply_wp_selection())
        self.wp_pack.pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="新建空白包", width=96, height=28, font=FONT_S,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=self.create_blank_pack).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="打开目录", width=76, height=28, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_packs_dir).pack(side="left")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="地图", font=FONT_S,
                     text_color="#9aa0a6").pack(side="left", padx=(0, 6))
        self.wp_map = ctk.CTkOptionMenu(
            row, values=list(self.map_disp) or ["（没有可测的路点图）"],
            font=FONT_S, width=250,
            command=lambda _v: self.apply_wp_selection())
        self.wp_map.pack(side="left", padx=(0, 8))
        self.wp_only = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(row, text="只对这张图生效", variable=self.wp_only,
                        font=FONT_S, checkbox_width=18, checkbox_height=18,
                        command=self.apply_wp_selection).pack(side="left")

        self.wp_meta = ctk.CTkLabel(box, text="", font=("Consolas", 10),
                                    text_color="#9aa0a6", anchor="w",
                                    justify="left", wraplength=620)
        self.wp_meta.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(
            box,
            text="空白底图用运输船 / 新寂静村（有原生点可借槽位）；飓风危城原生 0 点，"
                 "建不了空白包，只能开自动铺点。④ 包只影响选中的图，③ 正式版游戏内只读。",
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
            ("collect_only", "只读采集（不创建对象）", False),
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

        # ③ 点类型
        box = self.wp_card(body, "③ 点类型", "菜单 1-9 · 点选笔刷")
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=8, pady=(4, 4))
        for idx, (key, label, badge, color) in enumerate(self.wp_type_defs):
            btn = ctk.CTkButton(
                grid, text=label, font=FONT_S, width=110, height=46, anchor="w",
                fg_color="#262626", hover_color="#333333",
                text_color="#e8e8e8", border_width=2, border_color="#3a3a3a",
                command=lambda k=key: self.set_wp_brush(k))
            btn.grid(row=idx // 4, column=idx % 4, sticky="nsew", padx=3, pady=3)
            self.wp_type_btns[key] = btn
        for c in range(4):
            grid.grid_columnconfigure(c, weight=1)
        ctk.CTkLabel(
            box,
            text="点一下 = 设为当前笔刷；游戏运行中立即发 brush=... 给插件。"
                 "出生点 / 补给箱只读；跳跃点会新建 Bot_JumpLink（实验性，重启不保留）；"
                 "标签区写 node tag + markers。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=600).pack(fill="x", padx=12, pady=(0, 8))

        # ④ 本次编辑
        box = self.wp_card(body, "④ 本次编辑", "点/边写 ④ 包；特征写 markers")
        stats = ctk.CTkFrame(box, fg_color="transparent")
        stats.pack(fill="x", padx=8, pady=(4, 0))
        self.wp_stat_nodes = self.wp_stat_cell(stats, 0, "节点")
        self.wp_stat_edges = self.wp_stat_cell(stats, 1, "边")
        self.wp_stat_feat = self.wp_stat_cell(stats, 2, "特征")
        self.wp_stat_edits = self.wp_stat_cell(stats, 3, "④ 包改动")
        for c in range(4):
            stats.grid_columnconfigure(c, weight=1)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=8, pady=(6, 0))
        ctk.CTkButton(row, text="撤销 Ctrl+Z", width=88, height=28, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.wp_cmd("undo", "撤销")).pack(side="left", padx=(0, 5))
        ctk.CTkButton(row, text="重做 Ctrl+Y", width=88, height=28, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.wp_cmd("redo", "重做")).pack(side="left", padx=(0, 5))
        ctk.CTkButton(row, text="保存 Ctrl+S", width=88, height=28, font=FONT_S,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=lambda: self.wp_cmd("save", "保存")).pack(side="left", padx=(0, 5))
        ctk.CTkButton(row, text="重读 Ctrl+Shift+R", width=112, height=28, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.wp_cmd("reload", "重读")).pack(side="left", padx=(0, 5))
        ctk.CTkButton(row, text="清空本图", width=80, height=28, font=FONT_S,
                      fg_color="#8a4b1e", hover_color="#a55d26",
                      command=self.clear_pack_map).pack(side="left")

        self.wp_action_status = ctk.CTkLabel(
            box, text="就绪：点底部「开始游戏（加载 mod）」→ 进图后 F2 打开菜单；小键盘 8/2 上下，5 确认，0 返回。",
            font=FONT_S, text_color="#c9d1d9", anchor="w", justify="left",
            wraplength=620)
        self.wp_action_status.pack(fill="x", padx=12, pady=(6, 0))

        self.wp_log = ctk.CTkTextbox(box, height=72, font=("Consolas", 10),
                                     fg_color="#141414", wrap="word",
                                     activate_scrollbars=True)
        self.wp_log.pack(fill="x", padx=12, pady=(4, 8))
        self.wp_log.configure(state="disabled")

        self.sync_wp_from_pack()
        self.refresh_wp_types()
        self.refresh_wp_status()

    def wp_stat_cell(self, parent, col, title):
        cell = ctk.CTkFrame(parent, corner_radius=6)
        cell.grid(row=0, column=col, sticky="nsew", padx=3, pady=2)
        ctk.CTkLabel(cell, text=title, font=FONT_S, text_color="#9aa0a6",
                     anchor="w").pack(fill="x", padx=8, pady=(4, 0))
        value = ctk.CTkLabel(cell, text="—", font=("Consolas", 15, "bold"),
                             anchor="w")
        value.pack(fill="x", padx=8, pady=(0, 4))
        return value

    def sync_wp_from_pack(self):
        r"""把「测试数据」页的当前选择同步到人机路点页（只读镜像）。"""
        if not hasattr(self, "wp_seg") or self._wp_syncing:
            return
        self._wp_syncing = True
        try:
            pk = self.pack_dict()
            self.wp_seg.set("④ 测试包" if pk.get("on") else "③ 正式版")
            packs = self._pack_values()
            self.wp_pack.configure(values=packs)
            name = str(pk.get("name") or "")
            if name and name in packs:
                self.wp_pack.set(name)
            elif packs:
                self.wp_pack.set(packs[0])
            disp = ""
            for d, (lv, _lab, _fp) in self.map_disp.items():
                if lv == pk.get("map"):
                    disp = d
                    break
            if disp:
                self.wp_map.set(disp)
            self.wp_only.set(bool(pk.get("only_map", True)))
        finally:
            self._wp_syncing = False

    def apply_wp_selection(self):
        r"""人机路点页改了图/包 → 推回「测试数据」页的正式控件。

        game_env()/pack_dict() 仍然只读 opt_pack / opt_map / seg_mode，
        所以这里不另造一套选择，避免两页各选各的。
        """
        if getattr(self, "_wp_syncing", False) or not hasattr(self, "opt_pack"):
            return
        self._wp_syncing = True
        try:
            on = self.wp_seg.get().startswith("④")
            self.seg_mode.set("测试包（packs）" if on else "正式版（nav）")
            self.pack_on.set(on)
            self.pack_only.set(bool(self.wp_only.get()))
            name = self.wp_pack.get()
            if name.startswith("（"):
                name = ""
            packs = load_packs()
            self.opt_pack.configure(values=packs or ["（还没有测试包）"])
            if name:
                self.opt_pack.set(name)
            disp = self.wp_map.get()
            if disp in self.map_disp:
                self.opt_map.set(disp)
            self.on_pack_change()
        finally:
            self._wp_syncing = False
        self.sync_wp_from_pack()
        self.refresh_wp_types()
        self.refresh_wp_status()

    def refresh_wp_tab(self):
        if not hasattr(self, "wp_seg"):
            return
        self.sync_wp_from_pack()
        self.refresh_wp_types()
        self.refresh_wp_status()

    def refresh_wp_types(self):
        if not hasattr(self, "wp_type_btns"):
            return
        counts, _doc, _sc = self.wp_type_counts()
        for idx, (key, label, badge, color) in enumerate(self.wp_type_defs):
            cnt = counts.get(key)
            shown = "—" if cnt is None else str(cnt)
            if key == "box":
                shown = "—"
            text = "%s  %s" % (label, shown)
            text += chr(10) + "%s · 菜单 %d" % (badge, idx + 1)
            btn = self.wp_type_btns[key]
            btn.configure(
                text=text,
                border_color=(color if self.wp_brush == key else "#3a3a3a"),
                border_width=2,
                state=("disabled" if badge == "只读" else "normal"))

    def set_wp_brush(self, key):
        defs = {k: (label, badge, color) for k, label, badge, color in self.wp_type_defs}
        if key not in defs:
            return
        label, badge, _color = defs[key]
        if badge == "只读":
            self.set_status("%s 是只读图层，第一版不写" % label)
            return
        self.wp_brush = key
        self.feats["wp_brush"] = key
        self.persist("笔刷")
        if game_running():
            try:
                seq = write_nav_cmd("brush", extra={"brush": key})
                self.set_status("已发送 #%d：笔刷 → %s" % (seq, label))
            except OSError as exc:
                self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
        else:
            self.set_status("笔刷 → %s（游戏没开，进图后生效）" % label)
        self.refresh_wp_types()

    def refresh_wp_status(self):
        if not hasattr(self, "wp_meta"):
            return
        self.refresh_wp_types()
        pk = self.pack_dict() if hasattr(self, "opt_pack") else {}
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        lv, label, _fp = self.map_disp.get(disp, ("", "", ""))
        doc, _path = find_map_doc(fp)
        counts = (doc or {}).get("counts") or {}
        sc = self.wp_scene.get(lv, {})
        nodes = int(counts.get("nodes") or 0)
        edges = int(counts.get("edges") or 0)
        feat = (int(sc.get("guard") or 0) + int(sc.get("crouch") or 0) +
                int(sc.get("area") or 0) + int(sc.get("tag") or 0))
        pack_on = bool(pk.get("on"))
        if name:
            info = pack_summary(name, fp)
            edits = info["nadd"] + info["eadd"] + info["ndel"] + info["edel"]
            edits_text = str(edits)
        else:
            edits_text = "—"
        self.wp_stat_nodes.configure(text=str(nodes))
        self.wp_stat_edges.configure(text=str(edges))
        self.wp_stat_feat.configure(text=str(feat))
        self.wp_stat_edits.configure(text=edits_text)
        self.wp_meta.configure(
            text="指纹 %s · 原生 %d 点 / %d 边 · %s" % (
                fp or "—", nodes, edges,
                ("④ " + name if pack_on and name else "③ 正式版（只读）")))
        if pack_on and name:
            self.wp_action_status.configure(
                text="④ 测试包 %s · 只对 %s 生效；游戏运行中点按钮会写 ucf_navcmd。" % (
                    name, label or lv or "本图"))
        else:
            self.wp_action_status.configure(
                text="③ 正式版（nav）· 游戏内只读（UCF_NAV_READONLY=1）；"
                     "要保存请先切 ④ 测试包。")
        lines = [ln for ln in tail_log(40)
                 if ("[naved]" in ln or "[edit]" in ln or "[wp]" in ln)]
        lines = lines[-5:]
        text = chr(10).join(lines) if lines else "（还没有编辑日志）"
        self.wp_log.configure(state="normal")
        self.wp_log.delete("1.0", "end")
        self.wp_log.insert("end", text)
        self.wp_log.configure(state="disabled")

    def wp_cmd(self, cmd, label=""):
        if not game_running():
            self.set_status("游戏没开：进图后「%s」才有效" % (label or cmd))
            return
        if cmd in ("save", "reload"):
            if not self.pack_on.get() or not self.selected_pack():
                self.set_status("③ 正式版只读：先切 ④ 测试包再%s" % (label or cmd))
                return
            self.send_pack_cmd(cmd)
            return
        try:
            seq = write_nav_cmd(cmd)
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.set_status("已发送 #%d：%s；日志看 naved" % (seq, label or cmd))

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
            ctk.CTkLabel(prow, text=root, font=("Consolas", 10), text_color="#7f8792",
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

        self.data_out = ctk.CTkTextbox(body, height=118, font=("Consolas", 10),
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
                         % (n_json, n_bin, n_packs, "、".join(names) if names else "无",
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

        self.at_out = ctk.CTkTextbox(body, height=110, font=("Consolas", 10),
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
        threading.Thread(target=self._at_worker, args=(env, idx, timeout), daemon=True).start()

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

    def _at_worker(self, env, idx, timeout):
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
        elif name == "测试数据" and hasattr(self, "opt_pack"):
            names = load_packs()            # 编辑器新存的包，切过来就能看到
            self.opt_pack.configure(values=names or ["（还没有测试包）"])
            self.refresh_pack_status()
        elif name == "人机路点":
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
        if hasattr(self, "wp_brush"):
            feats["wp_brush"] = str(self.wp_brush)
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

    # ---- 测试数据：取值 / 切换 / 刷新 ----
    def _pack_values(self):
        names = load_packs()
        return names or ["（还没有测试包）"]

    def pack_dict(self):
        """当前选择 → 写回 ucf_mod.json 的 pack 段（只给控制台自己用，插件不读它）。"""
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        lv, lab, fp = self.map_disp.get(disp, ("", "", ""))
        name = self.opt_pack.get() if hasattr(self, "opt_pack") else ""
        if name.startswith("（"):
            name = ""
        return {
            "on": bool(self.pack_on.get()),
            "name": name,
            "map": lv, "label": lab, "fp": fp,
            "only_map": bool(self.pack_only.get()),
        }

    def pack_manifest_map(self, name):
        """包对应的地图（manifest.json 的 level）；没有 manifest 就返回空。"""
        try:
            with open(os.path.join(PACKS, name, "manifest.json"), "r", encoding="utf-8") as f:
                return str((json.load(f) or {}).get("level") or "")
        except (OSError, ValueError):
            return ""

    def on_pack_change(self, persist=True):
        on = self.seg_mode.get().startswith("测试包")
        self.pack_on.set(on)
        name = self.opt_pack.get()
        if name.startswith("（"):
            packs = load_packs()
            name = packs[0] if packs else ""
            self.opt_pack.configure(values=packs or ["（还没有测试包）"])
            if name:
                self.opt_pack.set(name)
        # 换包时自动把地图切到包对应的那张图（包只对它生效，选错图等于空跑）
        if on and name and name != getattr(self, "_last_pack", ""):
            lv = self.pack_manifest_map(name)
            for disp, (lvl, _lab, _fp) in self.map_disp.items():
                if lv and lvl == lv:
                    self.opt_map.set(disp)
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
            self.persist("测试数据")
        self.refresh_pack_status()
        self.sync_wp_from_pack()

    def refresh_packs(self):
        packs = load_packs()
        self.opt_pack.configure(values=packs or ["（还没有测试包）"])
        if packs and self.opt_pack.get().startswith("（"):
            self.opt_pack.set(packs[0])
        self.on_pack_change()
        self.refresh_pack_status()
        self.set_status("测试包：%d 个" % len(packs))

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
        name = self.opt_pack.get() if hasattr(self, "opt_pack") else ""
        return "" if name.startswith("（") else name

    def selected_fp(self):
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        return self.map_disp.get(disp, ("", "", ""))[2]

    def refresh_pack_status(self):
        r"""测试数据页底部那行：当前包是不是空白、几个点/边、最后写入时间。"""
        if not hasattr(self, "lbl_pack"):
            return
        name = self.selected_pack()
        if not name:
            self.lbl_pack.configure(text="当前：正式版 nav\\（官方路线 / 没有选测试包）")
            return
        fp = pack_target_fp(name) or self.selected_fp()
        info = pack_summary(name, fp)
        man = pack_manifest(name)
        label = str(man.get("label") or man.get("level") or "")
        when = time.strftime("%H:%M:%S", time.localtime(info["mtime"])) if info["mtime"] else "（空）"
        bits = ["空白底图" if info["blank"] else "增量改动",
                "%d 点 / %d 边" % (info["nadd"], info["eadd"])]
        if info["ndel"] or info["edel"]:
            bits.append("删 %d 点 / %d 边" % (info["ndel"], info["edel"]))
        bits.append("改于 " + when)
        text = "当前包 %s%s · %s" % (name, ("（%s）" % label) if label else "", " · ".join(bits))
        if not info["path"]:
            text += " · 还没有 %s.txt" % (fp or "本图")
        self.lbl_pack.configure(text=text)

    def send_pack_cmd(self, cmd):
        r"""把「载入 / 重新应用 / 保存」写进 ucf_navcmd.txt，插件 0.5 s 内执行。"""
        name = self.selected_pack()
        if not name:
            self.set_status("先选一个测试包（或点「新建空白包」）")
            return
        if not pack_name_ok(name):
            self.set_status("包名只能是 ASCII 字母/数字/_/-：%s" % name)
            return
        fp = pack_target_fp(name) if self.pack_only.get() else ""
        if self.pack_only.get() and not fp:
            fp = self.selected_fp()
        try:
            seq = write_nav_cmd(cmd, name, fp)
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.persist("测试数据")
        running = game_running()
        act = {"apply": "载入", "reload": "重新应用", "save": "保存"}.get(cmd, cmd)
        if running:
            self.set_status("已发送 #%d：%s %s；游戏日志看 navcmd / naved" % (seq, act, name))
        else:
            self.set_status("游戏没开：已选中 %s，点「开始游戏」生效" % name)
        self.refresh_pack_status()

    def save_pack_now(self):
        if not self.selected_pack():
            self.set_status("先选一个测试包")
            return
        if not game_running():
            self.set_status("游戏没开：游戏里加点/删点本来就会自动写回 pack，不需要手动保存")
            return
        self.send_pack_cmd("save")

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
                "只重写 packs\\%s\\%s.txt，不动正式版 nav\\。" % (name, fp, name, fp),
                parent=self):
            return
        pdir = os.path.join(PACKS, name)
        txt = os.path.join(pdir, fp + ".txt")
        try:
            os.makedirs(pdir, exist_ok=True)
            with open(txt, "w", encoding="utf-8", newline="\n") as f:
                f.write("# ucf-navedit v1 fp=%s\nblank\n" % fp)
            with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
                f.write("")
            man = pack_manifest(name)
            man.setdefault("name", name)
            man.setdefault("fp", fp)
            if "level" not in man:
                man["level"] = self.map_disp.get(self.opt_map.get(), ("", "", ""))[0]
            man["blank"] = True
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

    def back_to_official(self):
        try:
            write_nav_cmd("off")
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.seg_mode.set("正式版（nav）")
        self.pack_on.set(False)
        self.on_pack_change()
        self.set_status("已切回正式版 nav\\%s" % ("，游戏运行中立即生效" if game_running() else ""))

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
        if fp == "n0-0000000000000000":
            messagebox.showwarning(
                "这张图做不了空白包",
                "暴风原生 0 个路点，插件没有可复用的节点槽位；空白包里的 node add 套不进去。\n"
                "请选运输船 / 新寂静村这种有原生路点的图。", parent=self)
            return
        name = simpledialog.askstring(
            "新建空白测试包", "包名（ASCII 字母/数字/_/-，例：blank_a）：", parent=self)
        if not name:
            return
        name = name.strip()
        if not re.match(r"^[A-Za-z0-9_-]{1,48}$", name):
            self.set_status("包名只能用 ASCII 字母/数字/_/-，1~48 字符")
            return
        pdir = os.path.join(PACKS, name)
        tpath = os.path.join(pdir, fp + ".txt")
        if os.path.isfile(tpath) and not messagebox.askyesno(
                "覆盖测试包", "测试包 %s 里已经有 %s.txt，覆盖成空白底图？" % (name, fp),
                parent=self):
            return
        try:
            os.makedirs(pdir, exist_ok=True)
            with open(tpath, "w", encoding="utf-8", newline="\n") as f:
                f.write("# ucf-navedit v1 fp=%s\nblank\n" % fp)
            with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
                f.write("")                       # 存在即关掉自动铺点
            man = {
                "name": name, "level": lv, "label": lab, "fp": fp,
                "created": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "console-blank", "blank": True,
                "note": "空白底图测试包：原生点全禁用 + nogen.txt 关自动铺点；路线自己画",
            }
            with open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8",
                      newline="\n") as f:
                json.dump(man, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except OSError as exc:
            self.set_status("建包失败：%s" % exc)
            return
        packs = load_packs()
        self.opt_pack.configure(values=packs or ["（还没有测试包）"])
        self.opt_pack.set(name)
        self.seg_mode.set("测试包（packs）")
        self.pack_on.set(True)
        self.on_pack_change()
        msg = "已建空白测试包 %s（%s）" % (name, lab)
        if game_running():
            try:
                write_nav_cmd("apply", name, fp)
                msg += "，已发送到运行中的游戏"
            except OSError:
                pass
        self.set_status(msg)
        self.refresh_pack_status()

    # ---- 状态 ----
    def set_status(self, text):
        self.dot.configure(text=text)

    def refresh_status(self):
        if game_running():
            self.btn_game.configure(text="游戏运行中", state="disabled")
        else:
            self.btn_game.configure(text="开始游戏（加载 mod）", state="normal")
        lines = tail_log(6)
        self.logbox.configure(state="normal")
        self.logbox.delete("1.0", "end")
        self.logbox.insert("end", "\n".join(lines) if lines else "（还没有日志）")
        self.logbox.configure(state="disabled")
        if not self.dot.cget("text"):
            self.set_status("配置：%s" % ("已读取" if os.path.isfile(CFG_PATH) else "未找到，用默认值"))
        self.refresh_pack_status()
        self.refresh_export_info()
        if hasattr(self, "wp_meta"):
            self.refresh_wp_status()
        self.after(4000, self.refresh_status)

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
        note = "mod 已启用"
        if pk.get("on") and pk.get("name"):
            env["UCF_PACK"] = pk["name"]
            env.pop("UCF_NAV_READONLY", None)      # 测试包允许游戏内保存
            note = "mod + 测试包 %s" % pk["name"]
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
        # 通行证：只有这里启动才会带上 UCF_MOD=1，插件据此决定是否工作
        env, note = self.game_env()
        try:
            subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE), env=env)
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
