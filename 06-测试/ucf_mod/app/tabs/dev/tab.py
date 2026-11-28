#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「开发者选项」页：玩家坐标记录 + 原始轨迹采集 + 跟随式可通行性采样。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
2026-11-28：「地面扫描」（从天上往下扫整图）整套删掉，地面真值改由「跟随式采样」
            采（玩家脚下的碰撞面）—— 扫描打不到 4 m 以上的室内地板，土丘侧面也打不到。
"""


from tkinter import messagebox
import os
import time

import customtkinter as ctk

from ui.consts import DEV_ITEMS, FONT, FONT_S
from ui.env import LOG_DIR, PMARK_TXT, ucf_trace
from ui.packs import write_nav_cmd
from ui.util import find_log, game_running, save_cfg


class DevTab:
    # ---- 「开发者选项」页（2026-11-21 用户要求：单独成页，排在最后）----
    # 只放给开发 / 离线分析用的东西，正常玩图不需要：
    #   1) 开关：玩家坐标记录（要不要在本次场景画金色方块）
    #   2) 玩家坐标记录卡片：记一条 / 看列表 / 删（写 player_marks.txt，只是日志）
    #   3) 原始轨迹采集：逐帧 JSONL，交给 AI 找「跳跃 / 蹲行 / 传送」的识别阈值
    #   4) 跟随式可通行性采样：面图用的地面真值（玩家脚下碰撞面，走一圈就采到）
    def build_dev_tab(self, tab):
        r"""控制台「开发者选项」页：可视化开关 + 玩家坐标记录 + 原始轨迹采集 + 跟随采样。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(
            body,
            text="给开发 / 离线分析用的入口，正常玩图用不到。这里只做两件事："
                 "记玩家坐标、采逐帧轨迹；都不改游戏本身，也不影响人机跑图。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(8, 2))
        for key, label, desc, default in DEV_ITEMS:
            self.switch_card(body, key, label, desc, default)
        self.build_pmark_card(body)
        self.init_trace_state()          # 轨迹采集的运行态先备好，卡片里直接用
        self.build_trace_card(body)
        self.build_follow_card(body)

    # ---- 跟随式可通行性采样（2026-11-28 用户要求）----------------------------
    # 用户原话：「根据我在游戏中的玩家的周围、根据我脚下的碰撞地面去采集，
    # 根据地面的实际形状 —— 有的是土丘，有的是有斜坡等等各种情况」。
    # 为什么不用前两种做法（这也是面图一直补不齐的根因）：
    #   从天上扫整图  -> 4 米高往下的那一遍打不到 4 米以上的室内地板；
    #   导出视觉网格  -> 不是碰撞面，Recast 只覆盖得到三成左右的地面。
    # 采**玩家脚下的真实碰撞面**：土丘 / 斜坡 / 楼梯 / 室内地板都在，
    # 「跳上去才够得着的屋顶」天然采不到（玩家不会站上去）。
    def build_follow_card(self, parent):
        r"""跟随式可通行性采样卡片：开始 / 停止 / 看计数 / 打开 log 目录。

        数据流：按钮 -> ucf_navcmd.txt 的 cmd=follow act=start|stop
                -> 插件每 250 ms 以玩家脚底为中心、半径 8 m、1 m 一格向下打射线
                -> 追加 log\ground_samples_<地图>.txt（每行 x z y）
                -> 会话日志 log\ground_follow.log、实时状态 log\ground_follow.status
        游戏内表现（采样一开就显示，不用 Ctrl+V）：
                青色小方块 = 已经采到的地面格，亮绿 = 最近 2 秒刚采到的，
                黄色圆环 = 采样范围（半径 8 m），左上角一行字是计数。
        """
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkLabel(box, text="跟随式可通行性采样（面图用的真实地面）",
                     font=("Microsoft YaHei UI", 12, "bold"), anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(
            box,
            text="进图后点「开始采样」，然后在图里走一圈：地面、楼梯、室内、土丘都走一下。\n"
                 "插件每 0.25 秒以你脚下为中心、半径 8 米、1 米一格向下打射线，把真实碰撞地面"
                 "按「格 x、格 z、地面高度 y」记下来。\n"
                 "为什么必须是你脚下：从天上往下扫打不到室内地板；导出的模型不是碰撞面"
                 "（之前面图补不齐就是这个原因）。「跳上去才够得着的屋顶」不会被采到——玩家不会站上去。\n"
                 "游戏里能看见：青色=采过的格，亮绿=刚采到的，黄色圆环=采样范围，左上角一行字是计数。\n"
                 "产物：log\\ground_samples_<地图>.txt（离线烘焙面图直接吃）、"
                 "log\\ground_follow.log（会话日志）。只读游戏、不改任何东西。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=600).pack(fill="x", padx=12, pady=(0, 6))
        brow = ctk.CTkFrame(box, fg_color="transparent")
        brow.pack(fill="x", padx=12, pady=(0, 6))
        self.fl_btn_on = ctk.CTkButton(brow, text="开始采样", width=110, command=self.follow_start)
        self.fl_btn_on.pack(side="left", padx=(0, 6))
        self.fl_btn_off = ctk.CTkButton(brow, text="停止采样", width=110, state="disabled",
                                        fg_color="#3a3a3a", command=self.follow_stop)
        self.fl_btn_off.pack(side="left", padx=(0, 6))
        ctk.CTkButton(brow, text="打开 log 文件夹", width=120, fg_color="#3a3a3a",
                      command=lambda: os.startfile(LOG_DIR)).pack(side="left")
        self.fl_stat = ctk.CTkLabel(box, text="没在采。点「开始采样」，再进图走一圈。",
                                    font=FONT_S, text_color="#9aa0a6", anchor="w",
                                    justify="left", wraplength=600)
        self.fl_stat.pack(fill="x", padx=12, pady=(0, 8))
        self.fl_state = "idle"
        self.fl_t0 = 0.0

    def follow_start(self):
        try:
            write_nav_cmd("follow", "", "", {"act": "start"})
        except OSError as exc:
            self.set_status("写命令失败：%s" % exc)
            return
        self.fl_state = "starting"
        self.fl_t0 = time.time()
        self.fl_btn_on.configure(state="disabled")
        self.fl_btn_off.configure(state="normal", fg_color="#8a3a3a")
        self.fl_stat.configure(
            text="已发命令，等插件开始采…（没反应就看 log\\ground_follow.log）", text_color="#9aa0a6")
        self.after(700, self.follow_poll)

    def follow_stop(self):
        if self.fl_state not in ("starting", "on"):
            return
        try:
            write_nav_cmd("follow", "", "", {"act": "stop"})
        except OSError:
            pass
        self.fl_state = "idle"
        self.fl_btn_on.configure(state="normal")
        self.fl_btn_off.configure(state="disabled", fg_color="#3a3a3a")
        self.fl_stat.configure(
            text="已发停止命令。数据已经写在 log 里；再点开始会接着采（不重复、不覆盖）。",
            text_color="#9aa0a6")

    def follow_poll(self):
        r"""每秒读一次插件写的 log\ground_follow.status（纯 ASCII 的 key=value）。"""
        if self.fl_state not in ("starting", "on"):
            return
        st = _read_status(find_log("ground_follow.status"))
        if st is None:
            if self.fl_state == "starting" and time.time() - self.fl_t0 < 8.0:
                self.after(500, self.follow_poll)
                return
            if self.fl_state == "starting":
                self.fl_stat.configure(
                    text="插件没回话：确认①游戏在跑 ②DLL 是带 follow 的新版"
                         "（app\\tools\\build.ps1 之后重开游戏）③已经进图（大厅里读不到玩家位置）",
                    text_color="#ff9d9d")
                self.fl_state = "idle"
                self.fl_btn_on.configure(state="normal")
                self.fl_btn_off.configure(state="disabled", fg_color="#3a3a3a")
                return
            self.after(700, self.follow_poll)
            return
        on = int(st.get("on") or 0)
        cells = int(st.get("cells") or 0)
        sess = int(st.get("sess") or 0)
        if not on:
            self.fl_state = "idle"
            self.fl_btn_on.configure(state="normal")
            self.fl_btn_off.configure(state="disabled", fg_color="#3a3a3a")
            self.fl_stat.configure(
                text="插件那边已经停了（换图会自动停）。这个文件里共 %d 格，可以接着采。" % cells,
                text_color="#9aa0a6")
            return
        if self.fl_state == "starting":
            self.fl_state = "on"
        self.fl_stat.configure(
            text="● 采集中：已采 %d 格（本次 +%d）· 1 m 格 / 半径 8 m · 边走边采，走一圈就够"
                 % (cells, sess), text_color="#8fe38f")
        self.after(700, self.follow_poll)

    # ---- 玩家坐标记录（2026-11-21 用户要求：从「可视化」搬到「开发者选项」页）----
    def build_pmark_card(self, parent, row=None, col=None):
        r"""记录当前位置 / 列表 / 单条删除 / 全部删除。

        数据流：按钮 -> ucf_navcmd.txt 的 cmd=mark -> 插件向下打射线取脚下地面点
        -> 追加 player_marks.txt（不覆盖）-> 插件在**当前场景**画一个金色方块。
        2026-11-21 用户要求：方块只显示本次、不连折线，换图 / 重开游戏不再显示；
        文件只是日志（本卡片负责查看 / 删除）。删改由控制台直接写文件。
        """
        box = ctk.CTkFrame(parent, corner_radius=8)
        if row is None:
            box.pack(fill="x", padx=10, pady=(10, 10))
        else:
            box.grid(row=row, column=col, sticky="nsew")
        ctk.CTkLabel(box, text="玩家坐标记录", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(box, text="点一次记一条，只追加不覆盖。游戏里只在本次记下时画一个金色方块（不连折线），"
                              "换图 / 重开游戏就不再显示；坐标留在 player_marks.txt 当日志。"
                              "记录的是你脚下站的那个点（和路点同一套口径）。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=600).pack(fill="x", padx=12, pady=(0, 6))
        brow = ctk.CTkFrame(box, fg_color="transparent")
        brow.pack(fill="x", padx=12, pady=(0, 8))
        brow.grid_columnconfigure(0, weight=1)
        brow.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(brow, text="记录当前位置",
                      command=self.pmark_record).grid(
            row=0, column=0, sticky="ew", padx=(0, 4), pady=(0, 6))
        ctk.CTkButton(brow, text="刷新", fg_color="#3a3f45", hover_color="#4a5058",
                      command=self.pmark_refresh).grid(
            row=0, column=1, sticky="ew", padx=(4, 0), pady=(0, 6))
        ctk.CTkButton(brow, text="全部删除", fg_color="#8a2b2b", hover_color="#a83232",
                      command=self.pmark_clear).grid(
            row=1, column=0, sticky="ew", padx=(0, 4))
        ctk.CTkButton(brow, text="打开文件", fg_color="#3a3f45", hover_color="#4a5058",
                      command=self.pmark_open_file).grid(
            row=1, column=1, sticky="ew", padx=(4, 0))
        self.pmark_box = ctk.CTkScrollableFrame(box, height=180, corner_radius=6)
        self.pmark_box.pack(fill="x", padx=12, pady=(0, 10))
        self.pmark_refresh()

    def pmark_read(self):
        r"""[(序号, x, y, z, 时间)] —— 空文件或没有文件都返回 []。"""
        out = []
        try:
            with open(find_log("player_marks.txt"), "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    if len(parts) < 4:
                        continue
                    try:
                        out.append((int(parts[0]), float(parts[1]), float(parts[2]),
                                    float(parts[3]), " ".join(parts[4:])))
                    except ValueError:
                        continue
        except OSError:
            pass
        return out

    def pmark_write(self, rows):
        r"""原子替换：插件正在读也不会读到半截。"""
        lines = ["# ucf player marks  x y z  time"]
        for idx, x, y, z, ts in rows:
            lines.append("%d %.3f %.3f %.3f %s" % (idx, x, y, z, ts))
        tmp = PMARK_TXT + ".tmp"
        try:
            d = os.path.dirname(PMARK_TXT)
            if d:
                os.makedirs(d, exist_ok=True)
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lines) + "\n")
            os.replace(tmp, PMARK_TXT)
            return True
        except OSError as exc:
            self.set_status("写 player_marks.txt 失败：%s" % exc)
            return False

    def pmark_open_file(self):
        r"""用系统默认程序打开 player_marks.txt（文件不存在就先建一个带表头的）。"""
        if not os.path.exists(PMARK_TXT):
            try:
                d = os.path.dirname(PMARK_TXT)
                if d:
                    os.makedirs(d, exist_ok=True)
                with open(PMARK_TXT, "w", encoding="utf-8", newline="\n") as f:
                    f.write("# ucf player marks  x y z  time\n")
            except OSError as exc:
                self.set_status("创建 player_marks.txt 失败：%s" % exc)
                return
        try:
            os.startfile(PMARK_TXT)
        except OSError as exc:
            self.set_status("打开 player_marks.txt 失败：%s" % exc)
        else:
            self.set_status("已打开 player_marks.txt")

    def pmark_refresh(self):
        box = getattr(self, "pmark_box", None)
        if box is None:
            return
        for w in box.winfo_children():
            w.destroy()
        rows = self.pmark_read()
        if not rows:
            ctk.CTkLabel(box, text="还没有记录。进游戏站好位置，点「记录当前位置」。",
                         font=FONT_S, text_color="#9aa0a6", anchor="w").pack(
                fill="x", padx=8, pady=6)
            return
        for idx, x, y, z, ts in rows:
            line = ctk.CTkFrame(box, fg_color="transparent")
            line.pack(fill="x", pady=2)
            ctk.CTkButton(line, text="删", width=30, height=22,
                          fg_color="#5a2626", hover_color="#7a3030",
                          command=lambda i=idx: self.pmark_del(i)).pack(side="right", padx=(4, 0))
            col = ctk.CTkFrame(line, fg_color="transparent")
            col.pack(side="left", fill="x", expand=True, padx=(4, 0))
            ctk.CTkLabel(col, text="#%d  (%.2f, %.2f, %.2f)" % (idx, x, y, z),
                         font=FONT_S, anchor="w").pack(fill="x")
            ctk.CTkLabel(col, text=ts, font=("Microsoft YaHei UI", 11),
                         text_color="#8a9098", anchor="w").pack(fill="x")

    def pmark_record(self):
        try:
            write_nav_cmd("mark")
            self.set_status("已发送记录命令：切回游戏约 0.5 秒内记下你脚下这个点")
        except OSError as exc:
            self.set_status("写命令失败：%s" % exc)
        self.after(1200, self.pmark_refresh)

    def pmark_del(self, idx):
        rows = [r for r in self.pmark_read() if r[0] != idx]
        if self.pmark_write(rows):
            self.pmark_refresh()
            self.set_status("已删除 #%d" % idx)

    def pmark_clear(self):
        if not self.pmark_read():
            self.set_status("本来就没有记录")
            return
        if not messagebox.askyesno("全部删除", "删掉 player_marks.txt 里所有玩家坐标记录？"
                                   "已经画出来的方块要换图才会消失。"):
            return
        if self.pmark_write([]):
            self.pmark_refresh()
            self.set_status("已清空全部玩家坐标记录")

    # ---- 开发者选项页：原始轨迹采集（2026-11-21 用户要求：原先在录制页，已搬走）----
    # 录制 = 走一遍 -> 重采样成路点；这里 = 把每一帧原样写下来，交给离线分析
    # （AI）找「跳跃 / 跳下 / 蹲行 / 上梯 / 传送」到底该用哪些信号识别。
    def init_trace_state(self):
        r"""轨迹采集的运行态（和录制互不影响，自己一份；建卡片前必须先调）。"""
        trace = self.cfg.get("trace")
        if not isinstance(trace, dict):
            trace = {}
            self.cfg["trace"] = trace
        # 2026-11-24：默认档位从 20 提到 30 —— 玩家实测最短滞空 0.17 s，
        # 20 Hz 只有 3~4 帧，起跳/落点会漂；30 Hz 有 5~6 帧，够判跳。
        try:
            thz = int(trace.get("hz") or 30)
        except (TypeError, ValueError):
            thz = 30
        trace["hz"] = thz if thz in ucf_trace.GEARS else 30
        # 2026-11-27：采集对象（玩家 / 人机 / 全部）和录制页同一套语义，存在会话 header 的 who。
        # 选择本身记在 ucf_mod.json 的 trace.who —— 下次打开控制台按上一次的选择恢复。
        # who_value() 顺手认中文 / 1/2/3，旧配置或手改过的文件不会把选择丢掉。
        trace["who"] = ucf_trace.who_value(trace.get("who"))
        self.trace = trace
        self.tr_state = "idle"
        self.tr_file = ""
        self.tr_off = 0
        self.tr_lines = 0              # 玩家样本数（实时 Hz 只按它算）
        self.tr_bots = 0               # 人机样本条数（10 Hz，单独数，不混进玩家 Hz）
        self.tr_last_t = 0.0
        self.tr_t0 = 0.0
        self.tr_hz = 0                 # 正在采的这份日志的档位（改档位不影响它）

    def build_trace_card(self, parent):
        r"""「开发者选项」页的「原始轨迹采集」卡：档位 / 开始停止 / 文件名 / 目录。"""
        box = self.wp_card(parent, "原始轨迹采集（给 AI 分析用）",
                           "不重采样、不生成路点；每个样本一行 JSON")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="频率档位", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.tr_seg = ctk.CTkSegmentedButton(
            row, values=["%d Hz" % h for h in ucf_trace.GEARS], width=250, height=28,
            dynamic_resizing=False, font=FONT_S,
            selected_color="#2f6fdb", selected_hover_color="#255bb4",
            unselected_color="#2a2f36", unselected_hover_color="#343a42",
            command=self.on_trace_hz)
        self.tr_seg.pack(side="left")
        self.tr_seg.set("%d Hz" % self.trace["hz"])
        ctk.CTkLabel(row, text="越高越细；每小时约 5.5~33 MB",
                     font=FONT_S, text_color="#8a8f96").pack(side="left", padx=(10, 0))

        ctk.CTkLabel(
            box,
            text="每小时占用：10 Hz ≈ 3 MB · 20 Hz ≈ 6 MB · 30 Hz ≈ 9 MB · 60 Hz ≈ 18 MB\n"
                 "建议：量跳跃用 30 Hz（一跳 5~20 帧）；连跳 / 短跳 / 调阈值用 60 Hz；"
                 "10 Hz 不适合判跳。",
            font=("Microsoft YaHei UI", 11), text_color="#8a8f96", anchor="w",
            justify="left", wraplength=600).pack(fill="x", padx=12, pady=(4, 0))

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="采集对象", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.tr_who_seg = ctk.CTkSegmentedButton(
            row, values=["玩家", "人机", "全部"], width=180, height=28,
            dynamic_resizing=False, font=FONT_S,
            selected_color="#2f6fdb", selected_hover_color="#255bb4",
            unselected_color="#2a2f36", unselected_hover_color="#343a42",
            command=self.on_trace_who)
        self.tr_who_seg.pack(side="left")
        self.tr_who_seg.set(ucf_trace.who_label(self.trace["who"]))
        ctk.CTkLabel(row, text="人机 10 Hz（位置/动作/目标/跳跃）；实测 Hz 只按玩家样本算，人机单独计数",
                     font=FONT_S, text_color="#8a8f96").pack(side="left", padx=(10, 0))

        # 2026-11-27 用户要求：采集对象要记住上一次的选择。这里把"记住了什么、存在哪"
        # 写在卡片上，重启控制台后一眼能看出恢复的是上次那个，而不是又默认玩家。
        self.tr_who_memo = ctk.CTkLabel(
            box, text="", font=("Microsoft YaHei UI", 11), text_color="#6f7680",
            anchor="w", justify="left", wraplength=600)
        self.tr_who_memo.pack(fill="x", padx=12, pady=(2, 0))
        self.refresh_trace_who_memo()

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(8, 0))
        self.tr_btn_start = ctk.CTkButton(
            row, text="开始采集", width=100, height=30, font=FONT,
            fg_color="#2f6fdb", hover_color="#255bb4", command=self.trace_start)
        self.tr_btn_start.pack(side="left")
        self.tr_btn_stop = ctk.CTkButton(
            row, text="停止", width=72, height=30, font=FONT_S,
            fg_color="#3a3f47", hover_color="#4a5058", state="disabled",
            command=self.trace_stop)
        self.tr_btn_stop.pack(side="left", padx=(8, 0))
        self.tr_btn_dir = ctk.CTkButton(
            row, text="打开日志文件夹", width=124, height=30, font=FONT_S,
            fg_color="#2a2f36", hover_color="#343a42", command=self.trace_open_dir)
        self.tr_btn_dir.pack(side="right")

        self.tr_stat = ctk.CTkLabel(box, text="未开始", font=FONT_S,
                                    text_color="#9aa0a6", anchor="w",
                                    justify="left", wraplength=600)
        self.tr_stat.pack(fill="x", padx=12, pady=(6, 0))

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="日志文件", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.tr_file_lbl = ctk.CTkLabel(
            row, text="（还没有）", font=("Consolas", 11), text_color="#dce4ee",
            anchor="w", justify="left", wraplength=520)
        self.tr_file_lbl.pack(side="left", fill="x", expand=True)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(4, 0))
        ctk.CTkLabel(row, text="日志目录", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.tr_dir_lbl = ctk.CTkLabel(
            row, text=ucf_trace.DIR, font=("Consolas", 11), text_color="#8a8f96",
            anchor="w", justify="left", wraplength=520)
        self.tr_dir_lbl.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            box,
            text="每行：t 相对秒 / dt 距上一样本 / x,y,z 玩家脚底坐标 / g 是否在地面 / "
                 "vy 竖直速度 / sp 空格 ct Ctrl。\n"
                 "落地那一帧插件会多写一行 ev=jump（起跳点、落点、跳距、跳高、滞空、起跳速度、类型）。\n"
                 "这里只负责采、不负责分析：要汇总就命令行跑 "
                 "python app\\tools\\data\\jump_stats.py <日志或目录>（录制日志同一套格式，也能直接喂）。",
            font=("Microsoft YaHei UI", 11), text_color="#8a8f96", anchor="w",
            justify="left", wraplength=600).pack(fill="x", padx=12, pady=(6, 10))

        last = ucf_trace.latest()
        if last:
            self.trace_show_file(last)
            self.tr_stat.configure(text="上次日志还在目录里：%s"
                                   % os.path.basename(last))

    def on_trace_hz(self, disp):
        try:
            hz = int(str(disp).split()[0])
        except (TypeError, ValueError):
            hz = 30
        if hz not in ucf_trace.GEARS:
            hz = 30
        self.trace["hz"] = hz
        try:
            save_cfg(self.cfg)
        except OSError:
            pass
        self.set_status("轨迹采集频率：%d Hz（下一份日志生效）" % hz)
        if self.tr_state in ("starting", "running", "stopping"):
            self.tr_stat.configure(text="档位改动从下一份日志生效（当前这份按开始时的频率写）")

    def on_trace_who(self, disp):
        r"""采集对象：玩家 / 人机 / 全部。和录制页同一套语义，写进会话 header 的 who。

        2026-11-27 用户要求：选择要记住。这里一改就落进 ucf_mod.json 的 trace.who，
        下次打开控制台由 build_trace_card 把它 set 回分段按钮（不是又默认玩家）。
        """
        who = ucf_trace.who_value(disp)
        self.trace["who"] = who
        # 走到这里不一定是用户点的（也可能是程序直接调）：把分段按钮也摆正，
        # 免得「配置里是 人机、界面还停在 全部」。set() 不会回调 command，不会递归。
        seg = getattr(self, "tr_who_seg", None)
        if seg is not None:
            seg.set(ucf_trace.who_label(who))
        saved = True
        try:
            save_cfg(self.cfg)
        except OSError:
            saved = False
        self.refresh_trace_who_memo()
        self.set_status("采集对象：%s（%s；下一份日志生效；人机 10 Hz）"
                        % (ucf_trace.who_label(who),
                           "已记住" if saved else "记住了但写盘失败"))
        if self.tr_state in ("starting", "running", "stopping"):
            self.tr_stat.configure(text="采集对象改动从下一份日志生效（当前这份按开始时的设置）")

    def trace_who_now(self):
        r"""界面当前选中的采集对象（插件值）——开始采集时以它为准，控件和 trace 状态不打架。"""
        seg = getattr(self, "tr_who_seg", None)
        raw = seg.get() if seg is not None else self.trace.get("who", "player")
        return ucf_trace.who_value(raw, self.trace.get("who", "player"))

    def refresh_trace_who_memo(self):
        r"""卡片上的「上次选择已记住」一行；选了新的即时刷新，重启后也能看出恢复的是哪个。"""
        lbl = getattr(self, "tr_who_memo", None)
        if lbl is None:
            return
        lbl.configure(text="上次的采集对象：%s（记在 ucf_mod.json 的 trace.who；"
                           "下次打开控制台仍恢复成它）"
                      % ucf_trace.who_label(self.trace.get("who", "player")))

    def trace_start(self):
        if self.tr_state in ("starting", "running", "stopping"):
            return
        # 一个写入者（2026-11-27）：插件里只有一个采样会话，接管前先把录制收尾。
        # 录制文件不会因此丢失 —— 它照样能复盘保存，也能拿去分析（同一套格式）。
        if getattr(self, "rec_state", "idle") == "rec":
            try:
                self.rec_finish()
                self.set_status("采集接管：正在把上一段录制收尾（那一段照样能复盘保存）")
            except Exception:      # noqa: BLE001  录制页半截状态不该挡住采集
                pass
        if not game_running(fresh=True):
            self.set_status("游戏没跑：先开游戏再点「开始采集」（插件只在游戏进程里写文件）")
            return
        lv, lab, fp = self.map_disp.get(self.opt_map.get(), ("", "", ""))
        pid = self.selected_pack() if hasattr(self, "opt_map") else ""
        try:
            os.makedirs(ucf_trace.DIR, exist_ok=True)
        except OSError as exc:
            self.set_status("建不了轨迹目录：%s" % exc)
            return
        # 以界面当前选择为准（2026-11-27）：万一控件被程序改成和 trace 状态不一样，
        # 开始这一份时也把它记下来 ——「上一次的选择」= 上一次真正开始采集的那个。
        who = self.trace_who_now()
        if who != self.trace.get("who"):
            self.trace["who"] = who
            self.refresh_trace_who_memo()
            try:
                save_cfg(self.cfg)
            except OSError:
                pass
        self.tr_file = ucf_trace.make_path(lv or "map")
        self.tr_hz = self.trace["hz"]
        self.tr_off = 0
        self.tr_lines = 0
        self.tr_bots = 0
        self.tr_last_t = 0.0
        self.tr_t0 = time.time()
        try:
            seq = write_nav_cmd("trace", pid, fp or self.selected_fp(),
                                {"act": "start", "out": self.tr_file,
                                 "hz": self.trace["hz"],
                                 "who": who,
                                 "map": lv or "", "label": lab or ""})
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.tr_state = "starting"
        self.tr_btn_start.configure(state="disabled")
        self.tr_btn_stop.configure(state="normal")
        self.trace_show_file(self.tr_file)
        self.tr_stat.configure(
            text="已发命令 #%d（%d Hz，采集对象：%s），等插件建文件…"
                 % (seq, self.trace["hz"], ucf_trace.who_label(who)),
            text_color="#9aa0a6")
        self.set_status("轨迹采集（采集对象：%s）：等插件开始写 %s"
                        % (ucf_trace.who_label(who), os.path.basename(self.tr_file)))
        self.after(400, self.trace_poll)

    def trace_poll(self):
        if self.tr_state not in ("starting", "running", "stopping"):
            return
        try:
            size = os.path.getsize(self.tr_file)
        except OSError:
            size = -1
        if size < 0:
            if self.tr_state == "starting" and time.time() - self.tr_t0 < 8.0:
                self.after(400, self.trace_poll)
                return
            if self.tr_state == "starting":
                self.trace_fail(
                    "插件没建文件：确认游戏在跑，且 DLL 是带 trace 的新版"
                    "（先 tools\\build.ps1 -Deploy，再重开游戏）")
                return
            self.after(600, self.trace_poll)
            return
        if self.tr_state == "starting":
            self.tr_state = "running"
        try:
            off, n, nb, last, end = ucf_trace.scan_counts(self.tr_file, self.tr_off)
        except OSError:
            off, n, nb, last, end = self.tr_off, 0, 0, None, None
        self.tr_off = off
        self.tr_lines += n
        self.tr_bots += nb
        if last is not None:
            self.tr_last_t = float(last.get("t") or 0.0)
        if size == 0:
            if not game_running(fresh=True):
                self.trace_finish(auto=True)
                return
            self.tr_stat.configure(text="等待进图…（插件已建文件；进图后写第一个样本）")
            self.after(700, self.trace_poll)
            return
        self.trace_live(size)
        if end is not None:
            self.trace_finish(auto=True)
            return
        if not game_running(fresh=True):
            self.trace_finish(auto=True)
            return
        self.after(500, self.trace_poll)

    def trace_live(self, size):
        dur = max(0.0, self.tr_last_t)
        hz = (self.tr_lines - 1) / dur if dur > 0.5 and self.tr_lines > 1 else 0.0
        self.tr_stat.configure(
            text="● 采集中 %02d:%02d · 采集对象：%s · 玩家 %d 样本 · 人机 %d 条 · "
                 "%.1f KB · 实测 %.1f Hz（档位 %d Hz）"
                 % (int(dur) // 60, int(dur) % 60,
                    ucf_trace.who_label(self.trace.get("who", "player")),
                    self.tr_lines, self.tr_bots, size / 1024.0,
                    hz, self.tr_hz or self.trace["hz"]),
            text_color="#ff9d9d")

    def trace_stop(self):
        if self.tr_state not in ("starting", "running"):
            return
        try:
            write_nav_cmd("trace", "", "", {"act": "stop"})
        except OSError:
            pass
        self.tr_state = "stopping"
        self.tr_btn_stop.configure(state="disabled")
        self.tr_stat.configure(text="正在收尾（插件写 end 行）…", text_color="#9aa0a6")
        self.after(600, self.trace_finish)

    def trace_finish(self, auto=False):
        if self.tr_state in ("idle", "stopped"):
            return
        if self.tr_file:
            try:
                off, n, nb, last, _end = ucf_trace.scan_counts(self.tr_file, self.tr_off)
                self.tr_off = off
                self.tr_lines += n
                self.tr_bots += nb
                if last is not None:
                    self.tr_last_t = float(last.get("t") or 0.0)
            except OSError:
                pass
        self.tr_state = "stopped"
        self.tr_btn_start.configure(state="normal")
        self.tr_btn_stop.configure(state="disabled")
        if self.tr_lines <= 0:
            bots = getattr(self, "tr_bots", 0)
            if not bots:
                try:
                    bots = int(ucf_trace.summary(self.tr_file).get("bots") or 0)
                except OSError:
                    pass
            if bots:
                who = ucf_trace.who_label(self.trace.get("who", "player"))
                self.tr_stat.configure(
                    text="已停止：人机 %d 条样本、玩家 0 条（采集对象：%s）" % (bots, who),
                    text_color="#f7cd74")
                self.set_status("轨迹采集停止：人机 %d 条（玩家 0 条）" % bots)
                return
            self.tr_stat.configure(
                text="已停止：没有样本（人没进图，或插件不是带 trace 的版本）",
                text_color="#f7cd74")
            self.set_status("轨迹采集停止：没有样本")
            return
        try:
            sm = ucf_trace.summary(self.tr_file)
            txt = ucf_trace.summary_text(sm)
        except OSError:
            txt = "玩家 %d 样本 · 人机 %d 条" % (self.tr_lines, getattr(self, "tr_bots", 0))
        head = "已收尾 · " if auto else "已停止 · "
        self.tr_stat.configure(text=head + txt, text_color="#9aa0a6")
        self.set_status(head + txt + " → " + os.path.basename(self.tr_file))

    def trace_fail(self, msg):
        self.tr_state = "idle"
        self.tr_btn_start.configure(state="normal")
        self.tr_btn_stop.configure(state="disabled")
        self.tr_stat.configure(text=msg, text_color="#f7cd74")
        self.set_status(msg)

    def trace_show_file(self, path):
        self.tr_file = path or ""
        self.tr_file_lbl.configure(text=os.path.basename(path) if path else "（还没有）")

    def trace_open_dir(self):
        try:
            os.makedirs(ucf_trace.DIR, exist_ok=True)
        except OSError as exc:
            self.set_status("建不了轨迹目录：%s" % exc)
            return
        try:
            os.startfile(ucf_trace.DIR)      # noqa: S606  Windows 专用
        except OSError as exc:
            self.set_status("打不开目录：%s" % exc)
            return
        self.set_status("已打开轨迹目录：%s" % ucf_trace.DIR)


def _read_status(path):
    r"""读插件写的状态文件（key=value 若干行，纯 ASCII）；没有 / 读不了返回 None。"""
    try:
        with open(path, "r", encoding="ascii", errors="replace") as f:
            out = {}
            for ln in f:
                s = ln.strip()
                if not s or "=" not in s:
                    continue
                k, v = s.split("=", 1)
                out[k.strip()] = v.strip()
            return out or None
    except OSError:
        return None

