#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「可视化」页：进图读什么、画什么（逐类勾选 + 图例）。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import tkinter as tk

import customtkinter as ctk

from ui.consts import FONT_S, MARK_BALLS


class VisTab:
    # ---- 「可视化」页：总开关 + 各类数据（勾选）----
    # 2026-11-19 用户要求：一颗开关同时管「读不读」和「画不画」；总开关排最上面。
    # 2026-11-21 用户要求：玩家坐标记录搬到「开发者选项」页，这一页只留「进图要看什么」。
    def build_vis_tab(self, tab, hint, items):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        by = {k: (label, desc, default) for k, label, desc, default in items}
        if "visualizer" in by:
            self.switch_card(body, "visualizer", *by["visualizer"])
        # 2026-11-20 用户要求：罗盘单独排到最后一排，前面拉一条虚线隔开
        tail = [k for k in ("vis_compass",) if k in by]
        keys = [k for k in by if k != "visualizer" and k not in tail] + tail
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(box, text="画哪些数据", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=(2, 4))
        # 2026-11-19 用户要求：并列展示；英文类名太长就在勾选项里换行，不排成一行一个。
        # CTkCheckBox 的文字不会换行，所以勾选框留空，文字用旁边可换行的 CTkLabel 画。
        txts, legends = [], []
        grow, gcol = 0, 0
        sep_done = False
        for key in keys:
            if key in tail and not sep_done:
                if gcol:                      # 虚线要独占一行：先把当前行封口
                    grow, gcol = grow + 1, 0
                self.vis_dashed_sep(grid, grow)
                grow += 1
                sep_done = True
            label, desc, default = by[key]
            var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
            self.vars[key] = var
            cell = ctk.CTkFrame(grid, fg_color="transparent")
            # sticky="nw"：同一行里说明长短不一时顶对齐，不再垂直居中错开（罗盘那排）
            cell.grid(row=grow, column=gcol, sticky="nw", padx=(0, 18), pady=6)
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
            gcol += 1
            if gcol >= 3:
                grow, gcol = grow + 1, 0
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)
        self.after(120, lambda: self.wrap_cells(body, txts, legends, 1.0))
        ctk.CTkLabel(box, text="勾上 = 读这一类并画出来；关掉 = 不读也不画（少一次可能出事的读取）。\n"
                              "只影响画面，不影响 Ctrl+E 导出（导出读什么由「导出」页那几项决定），"
                              "也不改动游戏本身。\n"
                              "游戏在运行时改勾选会**立刻下发**（0.5 s 内生效，不用重进图）；"
                              "游戏没开就只存配置，下次启动按配置来。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=600).pack(
            fill="x", padx=12, pady=(8, 10))
        self.build_mark_ball_card(body)

    # ---- 「点位上的小球」：DLL 给每个标记建的可视化球，颜色 = 类型 ----
    # 2026-11-26 用户要求：写在「可视化」页里，只记颜色和是什么。
    def build_mark_ball_card(self, body):
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 10))
        ctk.CTkLabel(box, text="点位上的小球（DLL 自己建的，不是游戏里的物体）",
                     font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        # 圆点用画出来的色块，不用 emoji：Tk 8.6 在 Windows 上把 🟡🟢🔵🔴
        # 全渲染成同一个灰色斜纹圈，颜色区分不出来（2026-11-26 实测截图）。
        for chip, name, what in MARK_BALLS:
            row = ctk.CTkFrame(box, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=1)
            ctk.CTkFrame(row, width=12, height=12, corner_radius=6,
                         fg_color=chip).pack(side="left", padx=(2, 6))
            ctk.CTkLabel(row, text=name, font=FONT_S,
                         text_color="#c9d1d9", width=24, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=what, font=FONT_S, text_color="#9aa0a6",
                         anchor="w", justify="left").pack(side="left")
        ctk.CTkLabel(box, text="建点 / 读点时才有：球在那个点正上方 0.45 m，游戏里的点位本身看不见，"
                              "靠它找位置。不写进 markers.txt 或包文件，换图 / 退游戏就没了。\n"
                              "显隐：Ctrl+V 关掉 → 球和数据一起没；Ctrl+0 只切球（随时能按，不用开编辑模式）；"
                              "两个都开着球才在。\n"
                              "本页那 10 个勾选管的是「读不读游戏自己的数据」，不管球（球来自你自己的 markers.txt）。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=600).pack(
            fill="x", padx=12, pady=(6, 10))
