#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""首次设置向导：选 UnityCrossFire.exe → 六道闸门 → 一键部署 → 写用户配置。

单独运行：
    python first_run.py

被控制台调用：
    import first_run
    if first_run.ensure_ready():   # True = 已配置且已部署，可以进主界面
        ...
"""

import contextlib
import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import customtkinter as ctk
from tkinter import filedialog

import deploy_mod as D
import ucf_paths as P

FONT = ("Microsoft YaHei UI", 13)
FONT_S = ("Microsoft YaHei UI", 12)
FONT_B = ("Microsoft YaHei UI", 15, "bold")


class Wizard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UCF 控制台 · 首次设置")
        self.geometry("820x660")
        self.minsize(760, 600)
        self.game = None
        self.steps = None
        self.ok = False
        self._build()
        self._prefill()

    # ---------------------------------------------------------------- UI
    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        head = ctk.CTkFrame(self, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", padx=18, pady=(16, 6))
        ctk.CTkLabel(head, text="UCF 控制台 · 首次设置", font=FONT_B).pack(anchor="w")
        ctk.CTkLabel(
            head,
            text="选一次 UnityCrossFire.exe，把运行件装进游戏目录；以后控制台就认这个位置。",
            font=FONT_S, text_color="#9aa4b2",
        ).pack(anchor="w", pady=(2, 0))

        # 第 1 步
        box1 = ctk.CTkFrame(self)
        box1.grid(row=1, column=0, sticky="ew", padx=18, pady=6)
        box1.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(box1, text="第 1 步 · 选择游戏", font=("Microsoft YaHei UI", 13, "bold")).grid(
            row=0, column=0, sticky="w", padx=12, pady=(10, 2))
        self.path_var = ctk.StringVar(value="（还没选）")
        self.path_entry = ctk.CTkEntry(box1, textvariable=self.path_var, font=FONT_S, state="readonly")
        self.path_entry.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        ctk.CTkButton(box1, text="选择 UnityCrossFire.exe …", font=FONT_S, width=190,
                      command=self.choose).grid(row=1, column=1, padx=(0, 12), pady=(0, 8))
        self.src_label = ctk.CTkLabel(
            box1, text="", font=("Microsoft YaHei UI", 11), text_color="#7f8a99")
        self.src_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 10))

        # 检查 + 日志
        box2 = ctk.CTkFrame(self)
        box2.grid(row=2, column=0, sticky="nsew", padx=18, pady=6)
        box2.grid_columnconfigure(0, weight=1)
        box2.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(box2, text="检查 / 部署过程", font=("Microsoft YaHei UI", 13, "bold")).grid(
            row=0, column=0, sticky="w", padx=12, pady=(10, 4))
        self.log = ctk.CTkTextbox(box2, font=("Consolas", 12), wrap="none")
        self.log.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 10))
        self.log.configure(state="disabled")

        # 选项
        box3 = ctk.CTkFrame(self, fg_color="transparent")
        box3.grid(row=3, column=0, sticky="ew", padx=18, pady=(2, 0))
        self.allow_cjk = ctk.CTkCheckBox(box3, text="允许中文路径（有风险）", font=FONT_S)
        self.allow_cjk.pack(side="left")
        self.force = ctk.CTkCheckBox(box3, text="允许覆盖第三方 winhttp.dll", font=FONT_S)
        self.force.pack(side="left", padx=(18, 0))

        # 按钮
        box4 = ctk.CTkFrame(self, fg_color="transparent")
        box4.grid(row=4, column=0, sticky="ew", padx=18, pady=(10, 16))
        ctk.CTkButton(box4, text="退出", font=FONT_S, width=90, fg_color="#3a3f47",
                      hover_color="#4a505a", command=self.destroy).pack(side="right")
        self.btn_finish = ctk.CTkButton(box4, text="完成并启动控制台", font=FONT_S, width=180,
                                        command=self.finish)
        self.btn_finish.pack(side="right", padx=8)
        self.btn_deploy = ctk.CTkButton(box4, text="一键部署", font=FONT_S, width=120,
                                        command=self.deploy)
        self.btn_deploy.pack(side="right", padx=8)
        self.btn_check = ctk.CTkButton(box4, text="重新检查", font=FONT_S, width=110, fg_color="#3a3f47",
                                       hover_color="#4a505a", command=self.recheck)
        self.btn_check.pack(side="right", padx=8)

        self._set_enabled(self.btn_finish, False)
        self._set_enabled(self.btn_deploy, False)

    @staticmethod
    def _set_enabled(btn, enabled):
        btn.configure(state="normal" if enabled else "disabled")

    def _write(self, text):
        self.log.configure(state="normal")
        self.log.insert("end", text)
        self.log.see("end")
        self.log.configure(state="disabled")

    # ---------------------------------------------------------------- 逻辑
    def _prefill(self):
        cur = Path(P.DEPLOY)
        exe = cur.parent / "UnityCrossFire.exe"
        self.src_label.configure(text="当前配置来源：" + P.DEPLOY_SOURCE_CN.get(P.DEPLOY_SOURCE, P.DEPLOY_SOURCE))
        if exe.is_file():
            self.set_game(exe.parent)

    def choose(self):
        path = filedialog.askopenfilename(
            title="选择 UnityCrossFire.exe",
            filetypes=[("UnityCrossFire", "UnityCrossFire.exe"), ("可执行文件", "*.exe")],
        )
        if not path:
            return
        game = D.resolve_game(path)
        if game is None:
            self._write(f"[X] 这不是一个可用的游戏位置：{path}\n")
            return
        self.set_game(game)

    def set_game(self, game):
        self.game = Path(game)
        self.path_var.set(str(self.game / "UnityCrossFire.exe"))
        self._write(f"\n游戏目录：{self.game}\n")
        self.recheck()

    def recheck(self):
        if self.game is None:
            self._write("[!!] 先选 UnityCrossFire.exe\n")
            return
        self._set_enabled(self.btn_deploy, False)
        self._set_enabled(self.btn_finish, False)
        ok, rows = D.check_gates(self.game, allow_cjk=bool(self.allow_cjk.get()),
                                 force=bool(self.force.get()))
        self._write("\n前置检查：\n")
        for good, title, detail in rows:
            tag = D.OK if good else D.BAD
            self._write(f"  {tag} {title}  {detail}\n")
        if not ok:
            self._write("\n未通过 —— 先解决上面标 [X] 的项。\n")
            return
        try:
            self.steps = D.build_plan(self.game)
        except FileNotFoundError as exc:
            self._write(f"\n[X] {exc}\n")
            return
        current = D.all_current(self.game, self.steps)
        if current:
            self._write("\n[OK] 这个游戏目录已经部署好了，可以直接用。\n")
            self._set_enabled(self.btn_finish, True)
            self._set_enabled(self.btn_deploy, True)
        else:
            self._write("\n[OK] 检查通过，可以一键部署。\n")
            self._set_enabled(self.btn_deploy, True)

    def deploy(self):
        if self.game is None:
            return
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = D.run_deploy(self.game, self.steps, repair=False)
        except Exception as exc:
            buf.write(f"\n[X] 部署异常：{exc}\n")
            rc = 3
        self._write(buf.getvalue())
        if rc == 0:
            self._set_enabled(self.btn_finish, True)
        else:
            self._write("[X] 部署没有完成，仔细看上面的报错。\n")

    def finish(self):
        if self.game is None:
            return
        try:
            cfg = P.save_deploy(self.game)
        except OSError as exc:
            self._write(f"[X] 写配置失败：{exc}\n")
            return
        self._write(f"\n[OK] 已记住游戏位置：{cfg}\n")
        self.ok = True
        self.destroy()


def run_wizard(headless=False):
    """跑向导，返回 True = 已配置（且已部署）。headless=True 时只做检查不弹窗。"""
    if headless:
        return P.DEPLOY != P.PROJ
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = Wizard()
    app.mainloop()
    return app.ok


def ensure_ready(game_exe=None, deploy_root=None):
    """给控制台用：当前配置不可用时弹向导。返回 True 表示可以进主界面。"""
    exe = Path(game_exe) if game_exe else Path(P.DEPLOY).parent / "UnityCrossFire.exe"
    if exe.is_file():
        game = exe.parent
        try:
            if D.all_current(game):
                return True
        except Exception:
            pass
    return run_wizard()


if __name__ == "__main__":
    sys.exit(0 if run_wizard() else 1)
