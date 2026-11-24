#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「导出」页：Ctrl+E 导出开关、内容勾选、最近导出、整理收件箱。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


from tkinter import messagebox
import os
import subprocess
import sys
import tkinter as tk

import customtkinter as ctk

from ui.consts import FONT_S
from ui.env import HERE, TEST, TEST_VIS, TIDY
from ui.stats import latest_export, vis_raw_dir
from ui.util import fmt_time


class ExportTab:
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
            self.exp_path.configure(text="路径：%s（② 开发版 收件箱）" % TEST_VIS)
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
