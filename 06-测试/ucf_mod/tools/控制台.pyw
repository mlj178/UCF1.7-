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
import json
import os
import subprocess
import sys
import tkinter as tk

import customtkinter as ctk

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from ucf_paths import DEPLOY  # noqa: E402  工程端/部署端的唯一真相

CFG_PATH = os.path.join(DEPLOY, "ucf_mod.json")
LOG_PATH = os.path.join(DEPLOY, "ucf_mod.log")
GAME_EXE = os.path.join(os.path.dirname(DEPLOY), "UnityCrossFire.exe")
EDITOR_BAT = os.path.join(HERE, "启动导航编辑器.bat")

CREATE_NO_WINDOW = 0x08000000
FONT = ("Microsoft YaHei UI", 13)
FONT_S = ("Microsoft YaHei UI", 11)
FONT_B = ("Microsoft YaHei UI", 15, "bold")

# ---- 开关定义：(key, 标题, 说明, 默认值) --------------------------------
GROUPS = [
    ("地图", "房间选图列表里要不要多一张「暴风」；关掉后就是原版列表", [
        ("hidden_map", "加载暴风地图", "把隐藏图 Nano30_Storm 插进房间下拉框；关掉后选不到暴风", True),
    ]),
    ("建图", "只在「一个路点都没有」的地图上触发；这三项互相独立，各自生效", [
        ("auto_waypoints", "自动铺人机路点", "4 米栅格多层采样 → 建点 → 自动连线", True),
        ("auto_crouch", "自动补蹲守点", "图里蹲守点为 0 时自动布点；已有则跳过", True),
        ("ghost_areas", "幽灵守卫区", "凭空造 Bot_NanoGuardArea 巡逻区", True),
    ]),
    ("查看", "所有地图都生效，只影响显示和导出，不改游戏状态", [
        ("hud", "进图显示状态面板", "左上角那块字；Ctrl+H 随时开关", True),
        ("visualizer", "进图就画导航网格", "彩色点线；Ctrl+V 随时开关", False),
        ("navmesh_show", "画 A* 可走面", "NavMeshGraph 三角网线框（人机真正在上面跑的面）；Ctrl+Shift+6 随时开关；网页编辑器同一份数据", True),
        ("auto_export", "进图自动导出路点", "写进 vis\\，每张图都会导一份", True),
    ]),
    ("手动", "只有你按键时才发生", [
        ("editor", "允许游戏内编辑", "Ctrl+1 进入编辑模式，放蹲守点/改路点", True),
        ("collect_only", "只读采集", "只导出路点，绝不创建任何游戏对象", False),
    ]),
]


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
        self.geometry("720x780")
        self.minsize(680, 700)
        self.cfg = load_cfg()
        feats = self.cfg.setdefault("features", {})
        if not isinstance(feats, dict):
            feats = {}
            self.cfg["features"] = feats

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
                 "开关改完存进 ucf_mod.json，下次启动生效（游戏开着时要重开）。",
            font=FONT_S, text_color="#9aa0a6", justify="left").pack(anchor="w", padx=20)

        self.body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.body.pack(fill="both", expand=True, padx=14, pady=(8, 4))

        for title, hint, items in GROUPS:
            box = ctk.CTkFrame(self.body, corner_radius=10)
            box.pack(fill="x", pady=(0, 10))
            ctk.CTkLabel(box, text=title, font=("Microsoft YaHei UI", 14, "bold"),
                         anchor="w").pack(fill="x", padx=14, pady=(10, 0))
            ctk.CTkLabel(box, text=hint, font=FONT_S, text_color="#9aa0a6",
                         anchor="w", justify="left", wraplength=620).pack(fill="x", padx=14)
            for key, label, desc, default in items:
                row = ctk.CTkFrame(box, fg_color="transparent")
                row.pack(fill="x", padx=14, pady=(8, 2))
                var = tk.BooleanVar(value=bool(feats.get(key, default)))
                self.vars[key] = var
                sw = ctk.CTkSwitch(row, text=label, variable=var, font=FONT,
                                   progress_color="#2f9e44",
                                   command=lambda k=key: self.on_toggle(k))
                sw.pack(anchor="w")
                ctk.CTkLabel(row, text="      " + desc, font=FONT_S,
                             text_color="#9aa0a6", anchor="w",
                             justify="left", wraplength=620).pack(fill="x")
            ctk.CTkLabel(box, text="", font=FONT_S).pack(pady=1)

        # ---- 状态 ----
        stat = ctk.CTkFrame(self, corner_radius=10)
        stat.pack(fill="x", padx=14, pady=(0, 8))
        top = ctk.CTkFrame(stat, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(10, 2))
        ctk.CTkLabel(top, text="上次运行", font=("Microsoft YaHei UI", 14, "bold")).pack(side="left")
        self.dot = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
        self.dot.pack(side="right")
        self.logbox = ctk.CTkTextbox(stat, height=120, font=("Consolas", 11),
                                     fg_color="#141414", activate_scrollbars=True)
        self.logbox.pack(fill="x", padx=14, pady=(2, 12))

        # ---- 按钮 ----
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x", padx=14, pady=(0, 14))
        self.btn_game = ctk.CTkButton(bar, text="开始游戏（加载 mod）", font=FONT, height=42,
                                      fg_color="#2f6fdb", hover_color="#255bb4",
                                      command=self.launch_game)
        self.btn_game.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(bar, text="打开导航编辑器", font=FONT, height=42,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_editor).pack(side="left", fill="x", expand=True, padx=(6, 0))

        self.refresh_status()
        self.after(4000, self.refresh_status)

    # ---- 写盘 ----
    def persist(self, note=""):
        self.cfg["enabled"] = bool(self.master_var.get())
        feats = self.cfg.setdefault("features", {})
        for k, v in self.vars.items():
            feats[k] = bool(v.get())
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
        self.after(4000, self.refresh_status)

    # ---- 动作 ----
    def launch_game(self):
        if not os.path.isfile(GAME_EXE):
            self.set_status("找不到 %s" % GAME_EXE)
            return
        # 通行证：只有这里启动才会带上 UCF_MOD=1，插件据此决定是否工作
        env = dict(os.environ)
        env["UCF_MOD"] = "1"
        try:
            subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE), env=env)
            self.set_status("游戏已启动（mod 已启用）")
        except OSError as exc:
            self.set_status("启动失败：%s" % exc)
        self.after(1500, self.refresh_status)

    def open_editor(self):
        if not os.path.isfile(EDITOR_BAT):
            self.set_status("找不到 %s" % EDITOR_BAT)
            return
        subprocess.Popen(["cmd", "/c", "start", "", EDITOR_BAT], shell=False)
        self.set_status("已打开导航编辑器（浏览器）")


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
