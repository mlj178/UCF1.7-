#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「录制」页：录前准备 / 录制中 / 复盘三态。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import os
import re
import shutil
import time
import tkinter as tk

import customtkinter as ctk

from ui.consts import FONT, FONT_S
from ui.env import REC_RAW, ucf_rec
from ui.packs import pack_dir, pack_manifest, pack_txt, write_nav_cmd
from ui.util import game_running, tail_log


class RecordTab:
    # ---- 「录制」页：录前准备 → 录制中 → 复盘（只写 ② 开发版 · 编辑中）----
    # 设计：design/record-mode.html。控制台只做三件事：
    #   1) 把 rec start/stop/pause 写进 ucf_navcmd.txt（插件的 src/editor.c rec_tick 采样）；
    #   2) 每 0.3 s 读 jsonl，调 ucf_rec 做重采样 / 跳跃 / 落下 / 岔路识别；
    #   3) 复盘确认后，把增量行追加进 ② packs\<图>\<包>\<指纹>.txt（只增不覆盖）。
    def build_record_tab(self, tab):
        r"""控制台「录制」页：录前准备 / 录制中 / 复盘三态，卡片样式跟人机路点一致。"""
        rec = self.cfg.get("rec")
        if not isinstance(rec, dict):
            rec = {}
            self.cfg["rec"] = rec
        sw = rec.get("sw")
        rec["sw"] = ucf_rec.norm_switch(sw if isinstance(sw, dict) else {})
        try:
            step = float(rec.get("step") or ucf_rec.STEP_DEFAULT)
        except (TypeError, ValueError):
            step = ucf_rec.STEP_DEFAULT
        rec["step"] = step if step in ucf_rec.STEP_OPTIONS else ucf_rec.STEP_DEFAULT
        self.rec = rec
        self.rec_state = "ready"
        self.rec_file = ""
        self.rec_samples = []
        self.rec_result = None
        self.rec_paused = False
        self.rec_busy = False
        self.rec_t0 = 0.0
        self.rec_saved = False
        self.rec_error = ""
        self.rec_sw_vars = {}
        # 原始轨迹采集的卡片在「开发者选项」页（2026-11-21 用户要求搬走），
        # 它和录制互不影响，状态由 init_trace_state() 备好。

        # 顶部常驻条：状态 + 主操作（页面再长，「开始 / 结束 / 保存」都点得到）
        top = ctk.CTkFrame(tab, corner_radius=8, fg_color="#232323",
                           border_width=1, border_color="#3a3f47")
        top.pack(fill="x", padx=10, pady=(8, 0))
        self.rec_top = top
        self.rec_badge = ctk.CTkLabel(top, text="① 录前准备", width=118, height=26,
                                      corner_radius=6, font=("Microsoft YaHei UI", 12, "bold"),
                                      fg_color="#1f2a1f", text_color="#9be09b")
        self.rec_badge.pack(side="left", padx=(10, 8), pady=9)
        self.rec_head = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6",
                                     anchor="w", justify="left", wraplength=380)
        self.rec_head.pack(side="left", fill="x", expand=True, pady=9)
        self.rec_primary = ctk.CTkButton(
            top, text="开始录制", width=132, height=30, font=FONT,
            fg_color="#2f6fdb", hover_color="#255bb4", command=self.rec_start)
        self.rec_primary.pack(side="right", padx=(8, 10), pady=8)
        self.rec_aux = ctk.CTkButton(
            top, text="打开游戏", width=88, height=30, font=FONT_S,
            fg_color="#3a3f47", hover_color="#4a5058", command=self.launch_game)
        self.rec_aux.pack(side="right", padx=(0, 4), pady=8)
        self.rec_btn_start = self.rec_primary      # 预检按住这颗禁用/启用

        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        self.rec_body = body

        self.rec_holder = ctk.CTkFrame(body, fg_color="transparent")
        self.rec_holder.pack(fill="x")
        self.rec_ready = ctk.CTkFrame(self.rec_holder, fg_color="transparent")
        self.rec_live = ctk.CTkFrame(self.rec_holder, fg_color="transparent")
        self.rec_done = ctk.CTkFrame(self.rec_holder, fg_color="transparent")
        self.build_rec_ready(self.rec_ready)
        self.build_rec_live(self.rec_live)
        self.build_rec_done(self.rec_done)
        self.show_rec_state("ready")

        # 2026-11-21 用户要求：原始轨迹采集已搬到「开发者选项」页，这里不再放卡片

    def build_rec_ready(self, frame):
        # ① 启动条件（和人机路点共用同一个地图 / 启动档；一张图一个草稿）
        box = self.wp_card(frame, "启动条件", "地图跟「人机路点」共用；录制固定写草稿")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="启动档", font=FONT_S, text_color="#9aa0a6",
                     width=48, anchor="w").pack(side="left", padx=(0, 6))
        # 录制只写 ② 开发版（编辑中），成品档是只读的，没有第二种选法：
        # 这里只显示当前档位；万一全局停在成品，给一颗「切到编辑中」。
        self.rec_mode_lbl = ctk.CTkLabel(
            row, text="编辑中（可写）", width=172, height=26,
            corner_radius=6, font=("Microsoft YaHei UI", 12, "bold"),
            fg_color="#1f2a1f", text_color="#9be09b")
        self.rec_mode_lbl.pack(side="left")
        self.rec_mode_tip = ctk.CTkLabel(
            row, text="录制只写开发版；成品档只读，录不了",
            font=("Microsoft YaHei UI", 11), text_color="#8a8f96", anchor="w")
        self.rec_mode_tip.pack(side="left", padx=(10, 0))
        self.rec_mode_btn = ctk.CTkButton(
            row, text="切到编辑中", width=88, height=26, font=FONT_S,
            fg_color="#3a3f47", hover_color="#4a5058", command=self.rec_use_edit)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="地图", font=FONT_S, text_color="#9aa0a6",
                     width=48, anchor="w").pack(side="left", padx=(0, 6))
        self.rec_opt_map = ctk.CTkOptionMenu(
            row, values=list(self.map_disp) or ["（没有可测的路点图）"],
            font=FONT_S, width=252, command=self.on_rec_map)
        self.rec_opt_map.pack(side="left", padx=(0, 8))
        self.rec_meta = ctk.CTkLabel(box, text="", font=("Microsoft YaHei UI", 11),
                                     text_color="#9aa0a6", anchor="w",
                                     justify="left", wraplength=600)
        self.rec_meta.pack(fill="x", padx=12, pady=(6, 8))

        # ② 采样与自动识别
        box = self.wp_card(frame, "自动识别",
                           "插件 30 Hz 采玩家脚底坐标；落地由游戏自己的 isGrounded 结算，"
                           "跳链只保留 3D 1.5~3.0 m（人机真能跳的窗口）")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="采样间距", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.rec_step_seg = ctk.CTkSegmentedButton(
            row, values=["2.5 m", "4 m", "6 m"], width=210, height=28,
            dynamic_resizing=False, font=FONT_S,
            selected_color="#2f6fdb", selected_hover_color="#255bb4",
            unselected_color="#2a2f36", unselected_hover_color="#343a42",
            command=self.on_rec_step)
        self.rec_step_seg.pack(side="left")
        self.rec_step_seg.set({2.5: "2.5 m", 4.0: "4 m", 6.0: "6 m"}[self.rec["step"]])
        ctk.CTkLabel(row, text="走得越细节点越多；4 m 是默认", font=FONT_S,
                     text_color="#8a8f96").pack(side="left", padx=(10, 0))

        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=8, pady=(4, 4))
        for idx, (key, label, desc) in enumerate(ucf_rec.SWITCHES):
            cell = ctk.CTkFrame(grid, fg_color="transparent")
            cell.grid(row=idx // 2, column=idx % 2, sticky="nw",
                      padx=(6, 10), pady=5)
            var = tk.BooleanVar(value=bool(self.rec["sw"].get(key, True)))
            self.rec_sw_vars[key] = var
            ctk.CTkSwitch(cell, text=label, variable=var, font=FONT_S,
                          progress_color="#2f9e44",
                          command=lambda k=key: self.on_rec_switch(k)).pack(anchor="w")
            ctk.CTkLabel(cell, text=desc, font=("Microsoft YaHei UI", 11),
                         text_color="#8a8f96", anchor="w", justify="left",
                         wraplength=250).pack(anchor="w", padx=(2, 0))
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)

        # ③ 开始
        box = self.wp_card(frame, "开始录制", "控制台只发命令、读文件；走路和起跳都在游戏里")
        self.rec_pre = ctk.CTkLabel(box, text="", font=FONT_S, text_color="#9aa0a6",
                                    anchor="w", justify="left", wraplength=600)
        self.rec_pre.pack(fill="x", padx=12, pady=(6, 2))
        ctk.CTkButton(box, text="刷新状态", width=88, height=26, font=FONT_S,
                      fg_color="#2a2f36", hover_color="#343a42",
                      command=self.refresh_rec_ready).pack(anchor="w", padx=12, pady=(0, 2))
        ctk.CTkLabel(
            box,
            text="写 ② 开发版 · 编辑中：dev\\vis\\rec\\*.jsonl（原始轨迹）→ 复盘后追加进 "
                 "dev\\packs\\<图>\\<指纹>.txt；成品 / ③ 不动。",
            font=("Consolas", 11), text_color="#8a8f96", anchor="w",
            justify="left", wraplength=600).pack(fill="x", padx=12, pady=(2, 10))

    def build_rec_live(self, frame):
        box = self.wp_card(frame, "实时轨迹", "游戏里照常走；这里只看数字")
        self.rec_big = ctk.CTkLabel(box, text="00:00 · 0.0 m", anchor="w",
                                    font=("Consolas", 22, "bold"), text_color="#f0f0f0")
        self.rec_big.pack(fill="x", padx=14, pady=(8, 0))
        self.rec_sub = ctk.CTkLabel(box, text="等第一个样本…", anchor="w",
                                    font=FONT_S, text_color="#9aa0a6")
        self.rec_sub.pack(fill="x", padx=14, pady=(0, 4))
        self.rec_live_cv = tk.Canvas(box, width=340, height=180, bg="#161616",
                                     highlightthickness=0, bd=0)
        self.rec_live_cv.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_live_cv.bind("<Configure>",
                              lambda _e: self.rec_draw(self.rec_live_cv, self.rec_result))
        self.rec_ev = ctk.CTkLabel(box, text="（还没有事件）", anchor="w", justify="left",
                                   font=("Consolas", 11), text_color="#9aa0a6",
                                   wraplength=600)
        self.rec_ev.pack(fill="x", padx=14, pady=(0, 4))
        ctk.CTkLabel(box, text="暂停 / 结束都在右上角；结束会先让插件写 end 行，再整份识别",
                     font=FONT_S, text_color="#8a8f96", anchor="w",
                     justify="left", wraplength=600).pack(fill="x", padx=14, pady=(0, 10))

    def build_rec_done(self, frame):
        box = self.wp_card(frame, "轨迹与问题", "先看图和问题，再决定存不存")
        self.rec_sum = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                    font=FONT_S, text_color="#dce4ee", wraplength=600)
        self.rec_sum.pack(fill="x", padx=14, pady=(8, 2))
        self.rec_done_cv = tk.Canvas(box, width=340, height=160, bg="#161616",
                                     highlightthickness=0, bd=0)
        self.rec_done_cv.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_done_cv.bind("<Configure>",
                              lambda _e: self.rec_draw(self.rec_done_cv, self.rec_result))
        self.rec_issue = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                      font=FONT_S, text_color="#f7cd74", wraplength=600)
        self.rec_issue.pack(fill="x", padx=14, pady=(2, 2))
        self.rec_done_ev = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                        font=("Consolas", 11), text_color="#9aa0a6",
                                        wraplength=600)
        self.rec_done_ev.pack(fill="x", padx=14, pady=(0, 6))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_both = tk.BooleanVar(value=bool(self.rec.get("allow_both", False)))
        ctk.CTkCheckBox(row, text="跳链 / 落下也建反向边（同一处能走回来）",
                        variable=self.rec_both, font=FONT_S,
                        checkbox_width=18, checkbox_height=18,
                        command=self.on_rec_both).pack(side="left")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_btn_save = self.rec_primary      # 保存 / 重新采样都在顶部条
        ctk.CTkButton(row, text="重新录制", width=96, height=30, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.rec_reset).pack(side="left", padx=(8, 0))
        ctk.CTkButton(row, text="放弃", width=64, height=30, font=FONT_S,
                      fg_color="#8a1c1c", hover_color="#a32424",
                      command=self.rec_reset).pack(side="left", padx=(8, 0))
        self.rec_save_info = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                          font=FONT_S, text_color="#8a8f96",
                                          wraplength=600)
        self.rec_save_info.pack(fill="x", padx=14, pady=(0, 10))

    # ---- 录制页：状态 / 同步 / 预检 ------------------------------------
    def show_rec_state(self, state):
        self.rec_state = state
        for name, frame in (("ready", self.rec_ready), ("rec", self.rec_live),
                            ("done", self.rec_done)):
            if name == state:
                frame.pack(fill="x")
            else:
                frame.pack_forget()
        self.rec_head.configure(text={
            "ready": "选包 → 开始录制 → 进游戏走一遍路线",
            "rec": "在游戏里照目标走；空格起跳（含跳上箱子/台子）会自动记下",
            "done": "确认节点 / 边 / 跳链没问题，再写进草稿",
        }.get(state, ""))
        style = {
            "ready": ("#1f2a1f", "#9be09b"),
            "rec": ("#3a1c1c", "#ff9d9d"),
            "done": ("#1a2433", "#9cc3ff"),
        }.get(state, ("#242424", "#dce4ee"))
        self.rec_badge.configure(
            text={"ready": "① 录前准备", "rec": "● 录制中", "done": "③ 复盘"}[state],
            fg_color=style[0], text_color=style[1])
        conf = {
            "ready": ("开始录制", self.rec_start, "#2f6fdb", "#255bb4"),
            "rec": ("结束并复盘", self.rec_finish, "#2f9e44", "#37b24d"),
            "done": ("保存增量", self.rec_save, "#2f9e44", "#37b24d"),
        }.get(state)
        if conf:
            self.rec_primary.configure(text=conf[0], command=conf[1],
                                       fg_color=conf[2], hover_color=conf[3],
                                       state="normal")
        aux = {
            "ready": ("打开游戏", self.launch_game),
            "rec": ("继续" if self.rec_paused else "暂停", self.rec_pause_toggle),
            "done": ("重新采样", self.rec_review_retry),
        }.get(state)
        if aux:
            self.rec_aux.configure(text=aux[0], command=aux[1], state="normal")
            if state != "rec" or not self.rec_paused:
                self.rec_aux.configure(fg_color="#3a3f47")
            if not self.rec_aux.winfo_ismapped():
                self.rec_aux.pack(side="right", padx=(0, 4), pady=8)
        if state == "ready":
            self.refresh_rec_ready()

    def rec_sync_from_wp(self):
        r"""人机路点改了包 / 图，录制页的下拉框跟着改（两个下拉读同一个状态）。"""
        if not hasattr(self, "rec_opt_map"):
            return
        try:
            self.rec_show_mode()
            self.rec_opt_map.configure(values=list(self.map_disp))
            cur = self.opt_map.get() if hasattr(self, "opt_map") else ""
            if cur:
                self.rec_opt_map.set(cur)
            state = "normal" if self.pack_on.get() else "disabled"
            self.rec_opt_map.configure(state=state)
        except Exception:
            pass

    def rec_blockers(self):
        r"""开始录制前必须满足的条件；返回人话列表（空 = 可以开始）。"""
        out = []
        if not bool(self.master_var.get()):
            out.append("插件总开关关着")
        if not self.pack_on.get():
            out.append("成品档只读，先点上面「切到编辑中」")
        name = self.selected_pack() if hasattr(self, "opt_map") else ""
        if not name:
            out.append("这张图还没有草稿（先去「人机路点」点开始编辑）")
        if not self.selected_fp():
            out.append("没选地图")
        if not game_running():
            out.append("游戏没开（先点「打开游戏」）")
        return out

    def refresh_rec_ready(self):
        if not hasattr(self, "rec_pre"):
            return
        if self.rec_state != "ready":
            return          # 录制中/复盘时别去改顶部那颗「结束 / 保存」按钮
        self.rec_sync_from_wp()
        name = self.selected_pack() if hasattr(self, "opt_map") else ""
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        block = self.rec_blockers()
        if block:
            self.rec_pre.configure(text_color="#f7cd74",
                                   text="还不能开始：\n· " + "\n· ".join(block))
            self.rec_btn_start.configure(state="disabled", fg_color="#3a3f47",
                                         hover_color="#3a3f47")
        else:
            if self.rec_error:
                self.rec_pre.configure(text_color="#ff9d9d", text=self.rec_error)
            else:
                self.rec_pre.configure(
                    text_color="#9be09b",
                    text="可以开始：插件在跑，只写 ② 开发版 · 编辑中。"
                         "进游戏后点「开始录制」，走完回来点「结束并复盘」。")
            self.rec_btn_start.configure(state="normal", fg_color="#2f6fdb",
                                         hover_color="#255bb4")
        path = "dev\\packs\\" + name.replace("/", "\\") if name else "dev\\packs\\—"
        self.rec_meta.configure(
            text="指纹 %s · %s · 只写 ② 开发版（编辑中）" % (fp or "—", path))

    def rec_show_mode(self):
        r"""启动档只显示、不给选：录制只写开发版；全局停在成品时给一键切回。"""
        if not hasattr(self, "rec_mode_lbl"):
            return
        if self.pack_on.get():
            self.rec_mode_lbl.configure(text="编辑中（可写）", width=172,
                                        fg_color="#1f2a1f", text_color="#9be09b")
            self.rec_mode_tip.configure(text="录制只写草稿；成品档只读，录不了")
            if self.rec_mode_btn.winfo_manager():
                self.rec_mode_btn.pack_forget()
        else:
            self.rec_mode_lbl.configure(text="成品（只读）", width=104,
                                        fg_color="#3a2c0d", text_color="#f7cd74")
            self.rec_mode_tip.configure(text="成品档不能录；切到编辑中就能开始")
            if not self.rec_mode_btn.winfo_manager():
                self.rec_mode_btn.pack(side="right")

    def rec_use_edit(self):
        r"""从录制页一键回到编辑中（和人机路点共用同一个启动档）。"""
        self.pack_on.set(True)
        self.seg_mode.set("编辑中（可写）")
        self.on_page_change()
        self.refresh_rec_ready()
        self.set_status("已切到「编辑中」：录制只写 ② 开发版")

    def on_rec_map(self, disp):
        if hasattr(self, "opt_map"):
            self.opt_map.set(disp)
        self.on_pack_change()

    def on_rec_step(self, disp):
        try:
            step = float(str(disp).split()[0])
        except (TypeError, ValueError):
            step = ucf_rec.STEP_DEFAULT
        self.rec["step"] = step
        self.persist("录制采样间距")
        if self.rec_state == "done":
            self.rec_review_retry()

    def on_rec_switch(self, key):
        self.rec["sw"][key] = bool(self.rec_sw_vars[key].get())
        self.persist("录制识别开关")
        if self.rec_state == "done":
            self.rec_review_retry()

    def on_rec_both(self):
        self.rec["allow_both"] = bool(self.rec_both.get())
        self.persist("录制跳链方向")

    # ---- 录制：开始 / 轮询 / 暂停 / 结束 ---------------------------------
    def rec_start(self):
        if self.rec_state != "ready" or self.rec_busy:
            return
        block = self.rec_blockers()
        if block:
            self.set_status("还不能开始：" + block[0])
            self.refresh_rec_ready()
            return
        self.rec_error = ""
        name = self.selected_pack()
        fp = self.selected_fp()
        lv = self.map_disp.get(self.opt_map.get(), ("", "", ""))[0]
        tail = re.sub(r"[^0-9A-Za-z_-]+", "_", name.split("/")[-1])[:32] or "pack"
        try:
            os.makedirs(REC_RAW, exist_ok=True)
        except OSError as exc:
            self.set_status("建不了录制目录：%s" % exc)
            return
        self.rec_file = os.path.join(
            REC_RAW, "%s_%s_%s.jsonl" % (lv or "map", tail,
                                         time.strftime("%Y%m%d-%H%M%S")))
        self.rec_samples = []
        self.rec_result = None
        self.rec_saved = False
        self.rec_paused = False
        self.rec_busy = True
        try:
            seq = write_nav_cmd("rec", "", "", {"act": "start", "out": self.rec_file,
                                                "hz": 30})
        except OSError as exc:
            self.rec_busy = False
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.rec_error = ""
        self.rec_t0 = time.time()
        self.set_status("已发送 #%d：等插件开始录（%s）" % (seq, os.path.basename(self.rec_file)))
        self.show_rec_state("rec")
        self.rec_aux.configure(text="暂停", fg_color="#3a3f47")
        self.rec_big.configure(text="00:00 · 等待插件…")
        self.rec_sub.configure(text="插件每 0.5 s 看一次命令；还没写文件就是还没开始")
        self.rec_ev.configure(text="（还没有事件）")
        self.rec_live_cv.delete("all")
        self.after(400, self.rec_wait_start)

    def rec_wait_start(self):
        r"""等插件建文件 / 等第一个样本。

        插件一收到命令就会 fopen 建文件（哪怕人在大厅还没进图），所以：
          · 文件在、还是 0 字节 = 插件支持录制，在等进图 -> 最多等 90 s；
          · 文件一直没出现 = 插件没收到/没这个命令 -> 8 s 后报错（能认出旧 DLL）。
        """
        if self.rec_state != "rec":
            return
        try:
            size = os.path.getsize(self.rec_file)
        except OSError:
            size = -1
        elapsed = time.time() - self.rec_t0
        if size >= 0:
            self.rec_busy = False        # 文件建出来了就算开始成功，随时可以「结束」
        if size > 0:
            self.set_status("录制中：写 %s" % os.path.basename(self.rec_file))
            self.after(250, self.rec_poll)
            return
        if not game_running(fresh=True):
            self.rec_start_fail("游戏关掉了：录制停止（已录到的样本还在文件里）")
            return
        if size == 0:
            if elapsed < 90.0:
                self.rec_big.configure(text="等待进图…")
                self.rec_sub.configure(
                    text="插件已建文件（%d s）；进图后第一个样本就会开始写" % int(elapsed))
                self.after(500, self.rec_wait_start)
                return
            self.rec_start_fail("文件建了但 90 s 没有样本：确认已经进图（大厅没有可录的位置）")
            return
        if elapsed < 8.0:
            self.rec_sub.configure(text="已发命令，等插件建文件…")
            self.after(300, self.rec_wait_start)
            return
        tip = tail_log(30) or ""
        if "unknown cmd 'rec'" in tip:
            self.rec_start_fail(
                "插件不是带录制接口的版本：这个 ucf_mod.dll 里没有 rec 命令。"
                "先跑 tools\\build.ps1 -Deploy 再启动游戏。")
        else:
            self.rec_start_fail(
                "插件没开始录：确认游戏已进图、插件总开关开着；"
                "再看 log\\ucf_mod.log 的 navcmd / rec 行。")

    def rec_start_fail(self, msg):
        self.rec_busy = False
        self.rec_error = msg
        try:
            write_nav_cmd("rec", "", "", {"act": "stop"})
        except OSError:
            pass
        self.set_status(msg)
        self.show_rec_state("ready")

    def rec_poll(self):
        if self.rec_state != "rec":
            return
        try:
            with open(self.rec_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            lines = []
        samples, events = ucf_rec.parse_rec(lines)
        self.rec_samples = samples
        self.rec_events = events
        if samples:
            res = ucf_rec.analyse(samples, step=self.rec["step"], sw=self.rec["sw"],
                                  events=events)
            self.rec_result = res
            self.rec_update_live(res, samples)
        if not game_running(fresh=True):
            self.rec_finish(auto=True)
            return
        self.after(350, self.rec_poll)

    def rec_update_live(self, res, samples):
        if not samples:
            return
        dur = samples[-1]["t"] - samples[0]["t"]
        self.rec_big.configure(text="%02d:%02d · %.1f m" % (
            int(dur // 60), int(dur % 60), res.get("dist", 0.0)))
        if res.get("ok"):
            self.rec_sub.configure(text="%d 样本 · %d 节点 / %d 边 · 跳 %d / 落 %d / 岔 %d%s" % (
                res["samples"], res["nodes"], res["edges"], len(res["jumps"]),
                len(res["drops"]), len(res["branches"]),
                (" · 已暂停" if self.rec_paused else "")))
        else:
            self.rec_sub.configure(text="%d 样本 · %s" % (
                res["samples"], res.get("why") or "还在识别"))
        self.rec_ev.configure(text="\n".join(self.rec_event_lines(res)))
        self.rec_draw(self.rec_live_cv, res)

    def rec_event_lines(self, res):
        ev = []
        for j in res.get("jumps", [])[-2:]:
            ev.append("跳箱 · 水平 %.1f m · 按空格" % j["h"])
        for d in res.get("drops", [])[-2:]:
            ev.append("落下 · 下降 %.1f m%s" % (
                d["drop"], " · 可能摔伤" if d.get("hurt") else " · 落差 ≥ 2 m"))
        for b in res.get("branches", [])[:2]:
            ev.append("岔路候选 · 2.5 m 内回访 · 绕 %.0f m" % b["gap"])
        for j in res.get("jumps", []):
            if not (ucf_rec.LINK_MIN <= j.get("l3", 0.0) <= ucf_rec.LINK_MAX):
                ev.append("跳链跳过 · 3D %.1f m（人机做不了）" % j.get("l3", 0.0))
        for st in res.get("statics", [])[:1]:
            ev.append("静止 %.1f s · 采样照常" % st["t"])
        return ev[-4:] or ["（还没有事件）"]

    def rec_pause_toggle(self):
        if self.rec_state != "rec" or not self.rec_file:
            return
        self.rec_paused = not self.rec_paused
        act = "pause" if self.rec_paused else "resume"
        try:
            write_nav_cmd("rec", "", "", {"act": act})
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            self.rec_paused = not self.rec_paused
            return
        self.rec_aux.configure(
            text="继续" if self.rec_paused else "暂停",
            fg_color="#8a5a1c" if self.rec_paused else "#3a3f47")
        self.set_status("已暂停录制（jsonl 不再追加）" if self.rec_paused else "继续录制")

    def rec_finish(self, auto=False):
        if self.rec_state != "rec":
            return
        self.rec_busy = False            # 等待进图时也能直接结束（会提示没录到东西）
        try:
            write_nav_cmd("rec", "", "", {"act": "stop"})
        except OSError:
            pass
        if auto:
            self.set_status("游戏已退出，自动收尾…")
        self.after(700, self.rec_review_from_file)

    def rec_review_from_file(self):
        self.rec_busy = False
        try:
            with open(self.rec_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            lines = []
        samples, events = ucf_rec.parse_rec(lines)
        self.rec_samples = samples
        res = ucf_rec.analyse(samples, step=self.rec["step"], sw=self.rec["sw"],
                              events=events)
        self.rec_result = res
        if not res.get("ok"):
            self.rec_error = "这次没录到东西：%s" % (res.get("why") or "没有数据")
            self.set_status("复盘失败：%s" % (res.get("why") or "没有数据"))
            self.show_rec_state("ready")
            return
        self.rec_saved = False
        self.show_rec_state("done")
        self.rec_fill_done(res)
        self.set_status("复盘完成：%s" % ucf_rec.summary(res))

    def rec_fill_done(self, res):
        self.rec_sum.configure(text=ucf_rec.summary(res))
        lines = self.rec_event_lines(res)
        self.rec_done_ev.configure(text="\n".join(lines))
        iss = res.get("issues") or []
        self.rec_issue.configure(text=("· " + "\n· ".join(iss)) if iss else "没有发现问题")
        self.rec_draw(self.rec_done_cv, res)
        self.rec_btn_save.configure(state="normal", fg_color="#2f9e44",
                                    hover_color="#37b24d")
        name = self.selected_pack() if hasattr(self, "opt_map") else ""
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        self.rec_save_info.configure(
            text="只预览、还没写进草稿：点顶部「保存增量」才算保存\n"
                 "目标：dev\\packs\\%s\\%s.txt · 只增不覆盖 → 失败自动回滚"
                 % (name.replace("/", "\\") if name else "—", fp or "—"))

    def rec_review_retry(self):
        if not self.rec_samples:
            return
        res = ucf_rec.analyse(self.rec_samples, step=self.rec["step"], sw=self.rec["sw"],
                              events=getattr(self, "rec_events", None))
        self.rec_result = res
        if res.get("ok"):
            self.rec_saved = False
            self.rec_fill_done(res)
            self.set_status("已按当前阈值重新采样：%s" % ucf_rec.summary(res))
        else:
            self.set_status("重新采样失败：%s" % (res.get("why") or "没有数据"))

    def rec_reset(self):
        self.rec_result = None
        self.rec_samples = []
        self.rec_events = []
        self.rec_paused = False
        self.rec_busy = False
        self.rec_saved = False
        self.rec_error = ""
        self.show_rec_state("ready")

    def rec_save(self):
        if self.rec_state != "done" or not self.rec_result:
            return
        if self.rec_saved:
            return
        name = self.selected_pack() if hasattr(self, "opt_map") else ""
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        if not name or not fp:
            self.set_status("先选地图")
            return
        if not self.pack_on.get():
            self.set_status("成品档只读：切回「编辑中」再保存")
            return
        lines = ucf_rec.save_lines(self.rec_result, allow_both=bool(self.rec_both.get()))
        if not lines:
            self.set_status("没有可保存的节点 / 边")
            return
        path = pack_txt(name, fp)
        if not path:
            path = os.path.join(pack_dir(name), fp + ".txt")
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            existing = ""
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    existing = f.read()
            new = ucf_rec.dedupe_lines(lines, existing)
            if not new:
                self.set_status("这些节点 / 边包里已经有了（按 0.35 m 去重）")
                self.rec_saved = True
                self.rec_save_info.configure(text="没有新增：包里已经有这条路线")
                return
            prefix = ""
            if not existing:
                man = pack_manifest(name)
                mode = "grow" if (man.get("grow") or man.get("blank")) else "keep"
                prefix = "# ucf-navedit v1 fp=%s\n%s\n" % (fp, mode)
            ts = time.strftime("%Y%m%d-%H%M%S")
            if os.path.isfile(path):
                shutil.copy2(path, path + ".bak-rec-" + ts)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write(existing or prefix)
                if not (existing or prefix).endswith("\n"):
                    f.write("\n")
                f.write("\n".join(new) + "\n")
            os.replace(tmp, path)
        except OSError as exc:
            self.set_status("保存失败（原文件没动）：%s" % exc)
            return
        self.rec_saved = True
        self.rec_primary.configure(state="disabled", fg_color="#2a332a",
                                   hover_color="#2a332a")
        rel = "dev\\packs\\%s\\%s.txt" % (name.replace("/", "\\"), fp)
        self.rec_save_info.configure(text="已保存 %d 行 → %s" % (len(new), rel))
        self.set_status("已保存到草稿：%s（+%d 行）" % (rel, len(new)))
        if game_running():
            try:
                write_nav_cmd("apply", name, fp)
                self.set_status("已保存到草稿并通知插件重新载入（%s）" % rel)
            except OSError:
                pass

    def rec_draw(self, cv, res, live=False):
        r"""复盘 / 录制中的 2D 图：走路绿线、跳链黄虚线、落下橙虚线、节点蓝点。"""
        try:
            cv.delete("all")
            w = int(cv.winfo_width())
            h = int(cv.winfo_height())
            if w <= 10:
                w = 340
            if h <= 10:
                h = 170
            if not res or not res.get("ok") or not res.get("pieces"):
                cv.create_text(w // 2, h // 2, text="还没有轨迹",
                               fill="#6b7280", font=("Microsoft YaHei UI", 11))
                return
            pts = []
            for piece in res["pieces"]:
                pts.extend(piece["nodes"])
            if not pts:
                return
            minx = min(p[0] for p in pts)
            maxx = max(p[0] for p in pts)
            minz = min(p[2] for p in pts)
            maxz = max(p[2] for p in pts)
            pad = 16
            spanx = max(0.001, maxx - minx)
            spanz = max(0.001, maxz - minz)
            s = min((w - pad * 2) / spanx, (h - pad * 2) / spanz, 40.0)
            x0 = (w - spanx * s) / 2.0
            z0 = (h - spanz * s) / 2.0

            def P(p):
                return (x0 + (p[0] - minx) * s, h - z0 - (p[2] - minz) * s)

            for piece in res["pieces"]:
                nodes = piece["nodes"]
                for i, j in piece.get("walk", []):
                    a, b = P(nodes[i]), P(nodes[j])
                    cv.create_line(a[0], a[1], b[0], b[1], fill="#3f6b52", width=2)
            for link in res.get("links", []):
                a, b = P(link["a"]), P(link["b"])
                jump = link["kind"] == "jump"
                cv.create_line(a[0], a[1], b[0], b[1],
                               fill="#f2cc47" if jump else "#ff8c0d",
                               width=2, dash=(5, 3))
            for p in pts:
                x, y = P(p)
                cv.create_oval(x - 2, y - 2, x + 2, y + 2,
                               fill="#cfe0ff", outline="")
            for j in res.get("jumps", []):
                x, y = P(j["a"])
                cv.create_oval(x - 4, y - 4, x + 4, y + 4, outline="#f2cc47", width=2)
            for d in res.get("drops", []):
                x, y = P(d["a"])
                cv.create_oval(x - 4, y - 4, x + 4, y + 4, outline="#ff8c0d", width=2)
            for b in res.get("branches", []):
                x, y = P(b["p"])
                cv.create_oval(x - 5, y - 5, x + 5, y + 5, outline="#ffd43b")
            if pts:
                x, y = P(pts[0])
                cv.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#2f9e44", outline="")
        except tk.TclError:
            pass
