#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""共用控件：开关卡片、区块标题、文本卡、图例、文件对话框。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import os
import tkinter as tk

import customtkinter as ctk

from ui.consts import FONT, FONT_S, VIS_COLORS


class Kit:
    # ---- 页签导航：一行按钮 + 一组内容框（分组页和「人机路点」页共用）----
    def build_sub_tabs(self, parent, names, on_change=None):
        r"""页内标签：一行按钮 + 一组内容框，一次只显示一个。

        没用 CTkTabview：对比表是运行时重建的，Tabview 的高度不会跟着内容长。
        on_change(name)：用户点按钮后回调（控制台用它记「上次停在哪个子页」）。
        """
        bar = ctk.CTkFrame(parent, fg_color="transparent")
        bar.pack(fill="x", padx=10, pady=(8, 0))
        holder = ctk.CTkFrame(parent, fg_color="transparent")
        holder.pack(fill="both", expand=True)
        btns, frames = {}, {}
        for name in names:
            frames[name] = ctk.CTkFrame(holder, fg_color="transparent")
            btns[name] = ctk.CTkButton(bar, text=name, width=112, height=28,
                                       font=FONT_S, corner_radius=6)
            btns[name].pack(side="left", padx=(0, 6))

        def show(name, notify=True):
            for key, frame in frames.items():
                if key == name:
                    frame.pack(fill="both", expand=True)
                else:
                    frame.pack_forget()
            for key, btn in btns.items():
                on = key == name
                btn.configure(fg_color="#2f6fdb" if on else "#2a2f36",
                              hover_color="#255bb4" if on else "#343a42",
                              text_color="#ffffff" if on else "#9aa0a6")
            if notify and on_change is not None:
                on_change(name)
        for name in names:
            btns[name].configure(command=lambda n=name: show(n))
        show(names[0], notify=False)
        return frames, show

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

    def wrap_cells(self, body, txts, legends, frac=1.0):
        r"""按滚动区可见宽度给勾选项文字定换行；量的是画布，不是会被长文字撑大的内层。
        frac = 勾选区占整页宽度的比例（默认占满；旁边并排卡片时才 < 1）。"""
        w = body._parent_canvas.winfo_width()
        if w <= 1:                                  # 还没显示出来，下一拍再量
            self.after(120, lambda: self.wrap_cells(body, txts, legends, frac))
            return
        # 逻辑宽度扣掉：卡片左右 10、网格左右 12、滚动条余量 6；再按 frac 折算、按 3 列分
        logical = (w / self._get_window_scaling() - (10 * 2 + 12 * 2 + 6)) * frac
        textw = max(96, int(logical / 3 - 18 - 30 - 12))  # 18 列距 / 30 勾选框 / 12 余量
        for txt in txts:
            txt.configure(wraplength=textw)
        for lg in legends:                          # 图例前面还有缩进和色块，留 30
            lg.configure(wraplength=max(120, textw - 30))

    def vis_dashed_sep(self, parent, row):
        r"""跨三列的虚线分隔行：Tk 没有原生虚线，用 Canvas 一段段画。"""
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(12, 6))
        bg = self._app_bg(wrap)
        kw = {"height": 2, "highlightthickness": 0, "bd": 0}
        if bg:
            kw["bg"] = bg
        cv = tk.Canvas(wrap, **kw)
        cv.pack(fill="x")

        def redraw(_e=None):
            cv.delete("all")
            w = cv.winfo_width()
            for x in range(0, max(w, 1), 10):
                cv.create_line(x, 1, x + 5, 1, fill="#5f6670", width=1)
        cv.bind("<Configure>", redraw)

    def _app_bg(self, widget):
        r"""往上找一个不透明的背景色，给 Canvas 当底色（Canvas 不支持 transparent）。"""
        w = widget
        while w is not None:
            try:
                c = w.cget("fg_color")
            except Exception:
                c = None
            if c and c != "transparent":
                try:
                    return w._apply_appearance_mode(c)
                except Exception:
                    return c
            w = w.master
        return None

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

    def open_file(self, path, what):
        if not os.path.isfile(path):
            self.set_status("还没有 %s" % what)
            return
        try:
            os.startfile(path)      # noqa: SLF001  Windows 资源管理器
            self.set_status("已打开 %s" % what)
        except OSError as exc:
            self.set_status("打不开 %s：%s" % (what, exc))

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

    def ask_text(self, title, prompt, initial=""):
        r"""一句话输入框（成品版本改名用）；取消返回空串。"""
        out = {"v": ""}
        top = ctk.CTkToplevel(self)
        top.title(title)
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)
        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, lambda: top.winfo_exists() and top.grab_set())
        top.bind("<Escape>", lambda _e: top.destroy())
        ctk.CTkLabel(top, text=title, font=("Microsoft YaHei UI", 16, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 2))
        ctk.CTkLabel(top, text=prompt, font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=430).pack(fill="x", padx=18)
        ent = ctk.CTkEntry(top, font=FONT, width=400)
        ent.pack(fill="x", padx=18, pady=(8, 4))
        ent.insert(0, initial)
        ent.focus_set()
        ctk.CTkLabel(top, text="字母 / 数字 / 中文 / 下划线 / 减号 / 点都行；不能有空格和 \\ / : * ? \" < > |",
                     font=("Consolas", 11), text_color="#8a8f96", anchor="w",
                     justify="left", wraplength=430).pack(fill="x", padx=18)
        bar = ctk.CTkFrame(top, fg_color="transparent")
        bar.pack(fill="x", padx=18, pady=(12, 16))

        def ok(_e=None):
            out["v"] = ent.get().strip()
            top.destroy()

        ent.bind("<Return>", ok)
        ctk.CTkButton(bar, text="取消", width=90, height=32, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=top.destroy).pack(side="right")
        ctk.CTkButton(bar, text="确定", width=100, height=32, font=FONT,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=ok).pack(side="right", padx=(0, 8))
        self.wait_window(top)
        return out["v"]

    def confirm_danger(self, title, lines, ok_text="删除", cancel_text="取消",
                       checkbox_text="", checkbox_checked=False, out=None):
        r"""危险操作确认：只有点红色按钮才算「是」；× / Esc / 取消都算「否」。

        故意不用 messagebox.askyesno：Windows 上它把标题栏 × 交给默认按钮，
        实测「关掉弹窗」会返回 yes —— 删文件这种动作不能赌这个。
        返回 True/False；调用方拿到 False 就当没发生过。

        checkbox_text 非空时多一个勾选框（默认 checkbox_checked），勾没勾写进 out["checked"]，
        给「删草稿时顺手清标记」这种二合一确认用。
        """
        res = {"ok": False}
        top = ctk.CTkToplevel(self)
        top.title(title)
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)
        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, lambda: top.winfo_exists() and top.grab_set())

        def close(ok=False):
            res["ok"] = bool(ok)
            if out is not None and var is not None:
                out["checked"] = bool(var.get())
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", lambda: close(False))
        top.bind("<Escape>", lambda _e: close(False))

        head = ctk.CTkFrame(top, fg_color="transparent")
        head.pack(fill="x", padx=18, pady=(16, 2))
        ctk.CTkLabel(head, text="⚠", font=("Microsoft YaHei UI", 18, "bold"),
                     text_color="#f0a020", width=26).pack(side="left")
        ctk.CTkLabel(head, text=title, font=("Microsoft YaHei UI", 15, "bold"),
                     anchor="w").pack(side="left")
        ctk.CTkLabel(top, text=chr(10).join(lines), font=FONT_S, text_color="#c9d1d9",
                     anchor="w", justify="left", wraplength=470).pack(
            fill="x", padx=18, pady=(6, 12))
        var = None
        if checkbox_text:
            var = tk.BooleanVar(value=bool(checkbox_checked))
            ctk.CTkCheckBox(top, text=checkbox_text, variable=var, font=FONT_S,
                            checkbox_width=18, checkbox_height=18,
                            fg_color="#8a1c1c", hover_color="#a32424").pack(
                anchor="w", padx=20, pady=(0, 10))
        bar = ctk.CTkFrame(top, fg_color="transparent")
        bar.pack(fill="x", padx=18, pady=(0, 16))
        ctk.CTkButton(bar, text=ok_text, width=104, height=32, font=FONT,
                      fg_color="#8a1c1c", hover_color="#a32424",
                      command=lambda: close(True)).pack(side="right")
        btn_cancel = ctk.CTkButton(bar, text=cancel_text, width=96, height=32, font=FONT,
                                   fg_color="#3a3f47", hover_color="#4a5058",
                                   command=lambda: close(False))
        btn_cancel.pack(side="right", padx=(0, 8))
        btn_cancel.focus_set()          # 默认停在「取消」：回车也不会误删
        top.update_idletasks()
        try:
            x = self.winfo_rootx() + (self.winfo_width() - top.winfo_width()) // 2
            y = self.winfo_rooty() + (self.winfo_height() - top.winfo_height()) // 3
            top.geometry("+%d+%d" % (max(x, 0), max(y, 0)))
        except tk.TclError:
            pass
        self.wait_window(top)
        return res["ok"]
