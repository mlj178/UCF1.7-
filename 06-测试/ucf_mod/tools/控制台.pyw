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

from ucf_paths import DEPLOY, DEV, NATIVE  # noqa: E402  工程端/部署端的唯一真相

CFG_PATH = os.path.join(DEPLOY, "ucf_mod.json")
LOG_PATH = os.path.join(DEPLOY, "ucf_mod.log")
GAME_EXE = os.path.join(os.path.dirname(DEPLOY), "UnityCrossFire.exe")
EDITOR_BAT = os.path.join(HERE, "启动导航编辑器.bat")
NAVDATA = os.path.join(HERE, "navdata.py")     # 数据版本命令（部署/还原/校验/状态）
PACKS = os.path.join(DEPLOY, "packs")          # 测试包：<包名>\<指纹>.txt + manifest.json
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
                elif s.startswith("edge add "):
                    out["eadd"] += 1
                elif s.startswith("edge del "):
                    out["edel"] += 1
        out["mtime"] = os.stat(p).st_mtime
    except OSError:
        pass
    return out


def write_nav_cmd(cmd, name="", fp=""):
    r"""给运行中的插件写一条命令（原子替换，插件不会读到半截文件）。

    seq 必须单调递增：同一毫秒点两下也不能被插件当成同一条。
    """
    global _CMD_SEQ
    ms = int(time.time() * 1000)
    _CMD_SEQ = ms if ms > _CMD_SEQ else (_CMD_SEQ + 1)
    lines = ["seq=%d" % _CMD_SEQ, "cmd=%s" % cmd]
    if name:
        lines.append("pack=%s" % name)
    if fp:
        lines.append("fp=%s" % fp)
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
    bins = len([f for f in _listdir(os.path.join(root, "vis"))
                if f.startswith("navmesh_") and f.endswith(".bin")])
    return maps, files, lines, bins


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
    ("查看", "导出和读游戏组件表；显示类开关已全部移到「状态面板」页", [
        ("auto_export", "进图自动导出路点", "写进 vis\\，每张图都会导一份", True),
        ("vis_lists", "读游戏组件表", "可视化时读游戏的守区/蹲守/出生点静态表；进图闪退时的兜底开关——关掉后完全不碰这些表，只画 A* 图与可走面", True),
    ]),
    # 2026-11-17 20:5x：面板的开关从游戏里搬到这一页（用户要求：开关进控制台，游戏里不再展示）。
    ("状态面板", "游戏内左上角只留状态数字；开关都在这一页（写 ucf_mod.json，下次启动生效）", [
        ("hud", "显示状态面板", "左上角那块字；关掉后进图不建；Ctrl+H 仍能叫出", True),
        ("hud_states", "显示开关状态行", "面板第一行：可视化 / 五层 / 标签 各自的开关状态（默认不显示）", False),
        ("hud_keys", "显示快捷键帮助块", "Ctrl+H 那四行键位表（默认不显示；Ctrl+H 仍可临时叫出）", False),
        ("hud_log", "显示导出 / 最近日志行", "导出结果 + 最近 3 行日志；Ctrl+M 随时开关", True),
        ("visualizer", "可视化总开关", "彩色点线；Ctrl+V 随时开关", False),
        ("vis_layer_a", "A 路点 / 连线", "关掉后不画 A 层（导出仍全量）", True),
        ("vis_layer_b", "B 人类蹲守", "关掉后不画 B 层", True),
        ("vis_layer_c", "C 幽灵守区", "关掉后不画 C 层", True),
        ("vis_layer_d", "D 出生点 / 补给箱", "关掉后不画 D 层", True),
        ("vis_layer_e", "E 模式", "关掉后不画 E 层", True),
        ("navmesh_show", "F 可走面", "NavMeshGraph 三角网线框（人机真正在上面跑的面）；Ctrl+Shift+6 随时开关；与可视化总开关无关", True),
    ]),
    ("手动", "只有你按键时才发生", [
        ("editor", "允许游戏内编辑", "Ctrl+1 进入编辑模式，放蹲守点/改路点", True),
        ("collect_only", "只读采集", "只导出路点，绝不创建任何游戏对象", False),
    ]),
]

# ---- 「状态面板」页的控件编排 -----------------------------------------
# 五层开关排成 2 列；文字标签是三态，单独一张卡（GROUPS 只认 bool）。
LAYER_KEYS = ("vis_layer_a", "vis_layer_b", "vis_layer_c", "vis_layer_d",
              "vis_layer_e", "navmesh_show")
LABEL_VALUES = ["关", "近距 35 m", "全部"]
LABEL_DEFAULT = 0

# 文案照抄 src/editor.c 的 hud_refresh()：C 侧改了这里也要改。
# tools/test_console_switches.py 会逐行核对 HUD_KEYS，忘了同步会直接报错。
HUD_KEYS = (
    "Ctrl+V 可视化总开关   Ctrl+Shift+1..6  A路点/B人类/C幽灵/D出生/箱/E模式/F可走面   Ctrl+Shift+L 文字标签 关/近距/全部\n"
    "Ctrl+E 手动导出   Ctrl+M 日志行开关   Ctrl+H 本面板开关   Delete 删除准星最近标记   Ctrl+0 显示/隐藏已放标记\n"
    "Ctrl+1 编辑模式  Ctrl+2 蹲守点  Ctrl+4 幽灵守区  Ctrl+5 撤销  Ctrl+6 保存  Ctrl+7 重载  Ctrl+8 阵营  Ctrl+9 状态\n"
    "路点编辑: Ctrl+Shift+A 选A点  Ctrl+Shift+N 加点  Ctrl+Shift+J A↔点 连/断  Ctrl+Shift+D 禁用点  Ctrl+Shift+Z 撤销  Ctrl+Shift+R 重套用（改完自动存盘）"
)

HUD_NOTES = (
    "· 游戏里面板只留状态数字（节点 / 可走面 / 标记 / 数据来源）；开关状态行和快捷键块默认不显示。\n"
    "· 本页开关写进 ucf_mod.json，下次启动生效；游戏内热键仍可临时改（Ctrl+V / Ctrl+Shift+1..6 / "
    "Ctrl+Shift+L / Ctrl+M / Ctrl+H），但只对本次进程有效、画面不再回显状态。\n"
    "· 文字标签「近距」= 35 m；只读采集模式不创建 HUD，没有路点图的图也不画。"
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
            capture_output=True, text=True, timeout=5,
            creationflags=CREATE_NO_WINDOW)
        return "UnityCrossFire.exe" in (out.stdout or "")
    except Exception:
        return False


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
        self.geometry("760x%d+40+20" % win_h)   # 自己定位：交给窗口管理器会压到任务栏
        self.minsize(680, 620)
        self.cfg = load_cfg()
        feats = self.cfg.setdefault("features", {})
        if not isinstance(feats, dict):
            feats = {}
            self.cfg["features"] = feats
        self.feats = feats
        # 文字标签是三态（0 关 / 1 近距 / 2 全部），不在 self.vars 的 bool 表里
        lm = feats.get("vis_labels", LABEL_DEFAULT)
        try:
            lm = int(lm)
        except (TypeError, ValueError):
            lm = LABEL_DEFAULT
        self.label_mode = lm if lm in (0, 1, 2) else LABEL_DEFAULT

        self.vars = {}
        self.widgets = []

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(16, 4))
        ctk.CTkLabel(head, text="UCF 控制台", font=FONT_B).pack(side="left")
        self.master_var = tk.BooleanVar(value=bool(self.cfg.get("enabled", True)))
        ctk.CTkSwitch(head, text="插件总开关", variable=self.master_var,
                      font=FONT, progress_color="#2f9e44",
                      command=self.on_master).pack(side="right")

        ctk.CTkLabel(
            self,
            text="只有从本窗口「开始游戏」才会加载 mod；直接双击 UnityCrossFire.exe 是原版。\n"
                 "开关改完存进 ucf_mod.json，下次启动生效（游戏开着时要重开）。\n"
                 "测试包模式、四版数据的路径 / 部署 / 还原 / 校验：切到「测试数据」「数据」页。",
            font=FONT_S, text_color="#9aa0a6", justify="left").pack(anchor="w", padx=20)

        # ---- 按钮 / 状态：先按底边占位，窗口再矮也不会被页签挤没 ----
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(side="bottom", fill="x", padx=14, pady=(0, 12))
        self.btn_game = ctk.CTkButton(bar, text="开始游戏（加载 mod）", font=FONT, height=42,
                                      fg_color="#2f6fdb", hover_color="#255bb4",
                                      command=self.launch_game)
        self.btn_game.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(bar, text="导航编辑器（可选）", font=FONT, height=42,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_editor).pack(side="left", fill="x", expand=True, padx=(6, 0))

        stat = ctk.CTkFrame(self, corner_radius=10)
        stat.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
        top = ctk.CTkFrame(stat, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(10, 2))
        ctk.CTkLabel(top, text="上次运行", font=("Microsoft YaHei UI", 14, "bold")).pack(side="left")
        self.dot = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
        self.dot.pack(side="right")
        self.logbox = ctk.CTkTextbox(stat, height=104, font=("Consolas", 11),
                                     fg_color="#141414", activate_scrollbars=True)
        self.logbox.pack(fill="x", padx=14, pady=(2, 12))

        # 地图 / 查看 / 状态面板 / 手动 / 测试数据 / 数据 —— 全部页签切换，上方不再压一块常驻面板。
        self.tabview = ctk.CTkTabview(self, corner_radius=10, command=self.on_tab)
        self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 4))
        for title, hint, items in GROUPS:
            tab = self.tabview.add(title)
            if title == "状态面板":
                self.build_hud_tab(tab, hint, items)    # 开关 + 面板长什么样 + Ctrl+H 快捷键
            else:
                self.build_group_tab(tab, hint, items)
        self.build_pack_tab(self.tabview.add("测试数据"))   # 正式版 / 测试包 + 只对哪张图生效
        self.build_data_tab(self.tabview.add("数据"))       # 四版路径/时间 + 部署/还原/校验

        self.refresh_status()
        self.after(4000, self.refresh_status)

    # ---- 页签内容：一组开关 = 一页 ----
    def switch_card(self, parent, key, label, desc, default):
        r"""一个开关 + 一行说明；「查看」「状态面板」等页共用这份样式。"""
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

    # ---- 「状态面板」页：开关 + 面板内容 + Ctrl+H 快捷键（只读示意）----
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

    # ---- 「状态面板」页：游戏里的开关全部搬到这里 ----
    def section_title(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Microsoft YaHei UI", 12, "bold"),
                     text_color="#c9d1d9", anchor="w").pack(
            fill="x", padx=14, pady=(12, 0))

    def multi_switch_card(self, parent, keys, by, note=""):
        r"""一张卡里排 2 列开关（显示内容 / 可视化层）：只留标题，末尾一行小字。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(6, 0))
        for idx, key in enumerate(keys):
            label, _desc, default = by[key]
            var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
            self.vars[key] = var
            ctk.CTkSwitch(box, text=label, variable=var, font=FONT_S,
                          progress_color="#2f9e44",
                          command=lambda k=key: self.on_toggle(k)).grid(
                row=idx // 2, column=idx % 2, sticky="w",
                padx=(12, 8), pady=(10 if idx < 2 else 6, 0))
        for c in range(2):
            box.grid_columnconfigure(c, weight=1)
        last = (len(keys) + 1) // 2
        if note:
            ctk.CTkLabel(box, text=note, font=FONT_S, text_color="#9aa0a6",
                         anchor="w", justify="left", wraplength=590).grid(
                row=last, column=0, columnspan=2, sticky="w",
                padx=12, pady=(6, 10))
        else:
            ctk.CTkLabel(box, text="", height=4).grid(
                row=last, column=0, columnspan=2)
        return box

    def label_card(self, parent):
        r"""文字标签三态：关 / 近距 35 m / 全部。GROUPS 只认 bool，这里单独做一张卡。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(6, 0))
        seg = ctk.CTkSegmentedButton(box, values=LABEL_VALUES, font=FONT_S,
                                     command=self.on_labels)
        seg.pack(anchor="w", padx=12, pady=(10, 10))
        seg.set(LABEL_VALUES[self.label_mode])
        self.seg_labels = seg

    def build_hud_tab(self, tab, hint, items):
        r"""状态面板独立成页：开关全在控制台，游戏里只留状态数字（用户 2026-11-17 要求）。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        by = {k: (label, desc, default) for k, label, desc, default in items}

        self.section_title(body, "面板")
        self.multi_switch_card(
            body, ("hud", "hud_states", "hud_keys", "hud_log"), by,
            note="「显示状态面板」关掉后进图不建（Ctrl+H 仍能叫出）；状态行 / 快捷键块默认不显示，"
                 "导出与最近日志行默认显示。")

        self.section_title(body, "可视化（进图时画什么）")
        self.multi_switch_card(
            body, ("visualizer",) + LAYER_KEYS, by,
            note="热键仍可用：Ctrl+V 总开关，Ctrl+Shift+1..6 分层，Ctrl+Shift+L 标签；"
                 "F 可走面独立于可视化总开关。")

        self.section_title(body, "文字标签")
        self.label_card(body)

        self.text_card(body, "游戏内热键（面板里默认不显示，仍然可用）", HUD_KEYS, 128)
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
        ctk.CTkLabel(body, text="选「测试包」= 进图读 packs\\<包名> 里的路线；选「正式版」= 读 nav\\。\n"
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
        self.opt_pack = ctk.CTkOptionMenu(row, values=self._pack_values(), font=FONT_S,
                                          width=200, command=lambda _v: self.on_pack_change())
        self.opt_pack.pack(side="left", padx=(0, 6))
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

    # ---- 数据页：四版在哪 / 什么时候写的 / 一致不一致（原来三个 .bat 的活）----
    def build_data_tab(self, tab):
        r"""① 备份版/② 开发版/③ 部署版/④ 测试包 的路径、最近写入时间、条数，
        外加原「部署到游戏.bat / 还原原生.bat / 三版状态.bat」三件事的按钮。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text="① 只读快照；② 编辑器写这里；③ 游戏真正读这里；④ 只在你于「测试数据」"
                               "里选「测试包」时才读。改完 ② 要点「部署到游戏」③ 才会变。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=620).pack(fill="x", padx=12, pady=(8, 2))

        self.data_cards = []
        for tag, name, root, hint in (
                ("①", "备份版（只读）", NATIVE, "冻结快照，永不编辑"),
                ("②", "开发版", DEV, "编辑器写这里"),
                ("③", "部署版", DEPLOY, "游戏插件读这里"),
                ("④", "测试包", PACKS, "选「测试包」时读")):
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
                packs = load_packs()
                latest = 0.0
                bits = []
                for name in packs:
                    lines = 0
                    d = os.path.join(root, name)
                    for fn in _listdir(d):
                        if fn.endswith(".txt"):
                            try:
                                with open(os.path.join(d, fn), "r", encoding="utf-8",
                                          errors="replace") as f:
                                    lines += len([ln for ln in f
                                                  if ln.strip() and not ln.lstrip().startswith("#")])
                            except OSError:
                                pass
                        try:
                            latest = max(latest, os.stat(os.path.join(d, fn)).st_mtime)
                        except OSError:
                            pass
                    try:
                        with open(os.path.join(d, "manifest.json"), "r", encoding="utf-8") as f:
                            man = json.load(f) or {}
                        lab = str(man.get("label") or man.get("level") or "")
                    except (OSError, ValueError):
                        lab = ""
                    bits.append("%s（%s · %d 条）" % (name, lab or "无清单", lines))
                card["time"].configure(text=("最近写入 " + fmt_time(latest)) if packs else "（还没有包）")
                card["info"].configure(text=("%d 个包：" % len(packs) + "、".join(bits))
                                            if packs else "packs 目录是空的")
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
        self.lbl_same.configure(
            text=r"一致性（只比 maps\*.json 与 nav\*.txt，索引与 names.json 不算）："
                 + ("①=②" if n12 == 0 else "① vs ② 有 %d 个文件不同" % n12)
                 + " · " + ("②=③" if n23 == 0 else "② vs ③ 有 %d 个文件不同" % n23))

    def on_tab(self, name):
        if name == "数据":
            self.refresh_data()
        elif name == "测试数据" and hasattr(self, "opt_pack"):
            names = load_packs()            # 编辑器新存的包，切过来就能看到
            self.opt_pack.configure(values=names or ["（还没有测试包）"])
            self.refresh_pack_status()

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
        if hasattr(self, "seg_labels"):
            feats["vis_labels"] = int(self.label_mode)
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

    def on_labels(self, value):
        r"""文字标签三态：写 vis_labels（0/1/2），不是 bool，单独一条路径。"""
        self.label_mode = LABEL_VALUES.index(value)
        self.persist("文字标签")

    def on_master(self):
        self.persist("总开关")

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
        self.after(4000, self.refresh_status)

    # ---- 动作 ----
    def launch_game(self):
        if not os.path.isfile(GAME_EXE):
            self.set_status("找不到 %s" % GAME_EXE)
            return
        # 通行证：只有这里启动才会带上 UCF_MOD=1，插件据此决定是否工作
        env = dict(os.environ)
        env["UCF_MOD"] = "1"
        # 测试数据：只在这两个环境变量里生效，不动 ucf_mod\nav 一个字节
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        note = "mod 已启用"
        if pk.get("on"):
            if not pk.get("name"):
                note = "测试包没选（按正式版启动）"
            else:
                env["UCF_PACK"] = pk["name"]
                note = "mod + 测试包 %s" % pk["name"]
                if pk.get("only_map") and pk.get("fp"):
                    env["UCF_FP"] = pk["fp"]
                    env["UCF_FPLABEL"] = pk.get("label") or pk["map"]
                    note += "（只对 %s）" % (pk.get("label") or pk["map"])
        try:
            subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE), env=env)
            self.set_status("游戏已启动（%s）" % note)
        except OSError as exc:
            self.set_status("启动失败：%s" % exc)
        self.after(1500, self.refresh_status)

    def open_editor(self):
        if not os.path.isfile(EDITOR_BAT):
            self.set_status("找不到 %s" % EDITOR_BAT)
            return
        subprocess.Popen(["cmd", "/c", "start", "", EDITOR_BAT], shell=False)
        self.set_status("已打开导航编辑器（浏览器，可选；进游戏内画用 Ctrl+Shift+N）")


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
