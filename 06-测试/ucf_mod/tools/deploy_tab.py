#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""控制台的「部署」页：选游戏位置 → 六道闸门 → 一键部署 / 校验 / 卸载。

被 控制台.pyw 调用：
    import deploy_tab
    deploy_tab.build_deploy_tab(self, self.tabview.add("部署"))

单独跑（调试 UI）：
    python deploy_tab.py
"""

import contextlib
import importlib
import io
import os
import queue
import sys
import threading
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import customtkinter as ctk
from tkinter import filedialog, messagebox

import deploy_mod as D
import ucf_paths as P

FONT = ("Microsoft YaHei UI", 13)
FONT_S = ("Microsoft YaHei UI", 12)
FONT_C = ("Consolas", 11)
GREY = "#3a3f47"
GREY_H = "#4a5058"


def restart_console():
    r"""用户换游戏位置后，ucf_paths.DEPLOY 还是旧值 —— 重启一次最稳。"""
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        import subprocess
        try:
            subprocess.Popen([sys.executable] + [str(Path(globals().get("__file__", "")))], cwd=str(HERE))
        except Exception:
            pass
        sys.exit(0)


class DeployTab:
    def __init__(self, console, tab):
        self.console = console
        self.tab = tab
        self.game = None
        self.steps = None
        self.q = queue.Queue()
        self.busy = False
        self._build()
        self._load_current()
        self.console.after(150, self._pump)

    # ------------------------------------------------------------ UI
    def _build(self):
        body = ctk.CTkScrollableFrame(self.tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(
            body,
            text="把插件装进游戏目录：选一次 UnityCrossFire.exe，点「一键部署」。\n"
                 "会写入 winhttp.dll / winhttp_orig.dll / ucf_mod\\（dll、README、uninstall.ps1），"
                 "并生成部署清单；覆盖前先备份，卸载能还原。直接双击游戏 exe 是原版，必须用控制台「开始游戏」。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left", wraplength=640,
        ).pack(fill="x", padx=12, pady=(8, 4))

        # ---- 游戏位置 ----
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        top = ctk.CTkFrame(box, fg_color="transparent")
        top.pack(fill="x", padx=12, pady=(8, 0))
        ctk.CTkLabel(top, text="游戏位置", font=FONT).pack(side="left")
        self.src_lbl = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
        self.src_lbl.pack(side="right")

        prow = ctk.CTkFrame(box, fg_color="transparent")
        prow.pack(fill="x", padx=12, pady=(4, 6))
        self.path_var = ctk.StringVar(value="（未配置）")
        ctk.CTkEntry(prow, textvariable=self.path_var, font=FONT_C, state="readonly").pack(
            side="left", fill="x", expand=True)
        ctk.CTkButton(prow, text="选择 UnityCrossFire.exe", width=170, height=26, font=FONT_S,
                      command=self.choose).pack(side="left", padx=(8, 0))

        brow = ctk.CTkFrame(box, fg_color="transparent")
        brow.pack(fill="x", padx=12, pady=(0, 10))
        ctk.CTkButton(brow, text="打开游戏目录", width=110, height=24, font=FONT_S,
                      fg_color=GREY, hover_color=GREY_H,
                      command=self.open_folder).pack(side="left")
        ctk.CTkButton(brow, text="重新检查", width=90, height=24, font=FONT_S,
                      fg_color=GREY, hover_color=GREY_H,
                      command=self.reload).pack(side="left", padx=(6, 0))
        ctk.CTkButton(brow, text="重启控制台", width=100, height=24, font=FONT_S,
                      fg_color=GREY, hover_color=GREY_H,
                      command=restart_console).pack(side="left", padx=(6, 0))
        self.hint_lbl = ctk.CTkLabel(brow, text="", font=FONT_S, text_color="#d6b676")
        self.hint_lbl.pack(side="left", padx=(10, 0))

        # ---- 部署状态 ----
        self.state_box = ctk.CTkFrame(body, corner_radius=8)
        self.state_box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(self.state_box, text="部署状态", font=FONT).pack(anchor="w", padx=12, pady=(8, 2))
        self.rows = ctk.CTkFrame(self.state_box, fg_color="transparent")
        self.rows.pack(fill="x", padx=12, pady=(0, 10))

        # ---- 操作 ----
        act = ctk.CTkFrame(body, fg_color="transparent")
        act.pack(fill="x", padx=10, pady=(10, 0))
        self.btn_deploy = ctk.CTkButton(act, text="一键部署", height=32, font=FONT_S,
                                        fg_color="#2f9e44", hover_color="#37b24d",
                                        command=lambda: self.run("deploy"))
        self.btn_deploy.pack(side="left", padx=(0, 6))
        self.btn_repair = ctk.CTkButton(act, text="修复（强制重拷）", height=32, font=FONT_S,
                                        fg_color=GREY, hover_color=GREY_H,
                                        command=lambda: self.run("repair"))
        self.btn_repair.pack(side="left", padx=(0, 6))
        self.btn_verify = ctk.CTkButton(act, text="校验", height=32, width=70, font=FONT_S,
                                        fg_color=GREY, hover_color=GREY_H,
                                        command=lambda: self.run("verify"))
        self.btn_verify.pack(side="left", padx=(0, 6))
        self.btn_uninstall = ctk.CTkButton(act, text="卸载", height=32, width=70, font=FONT_S,
                                           fg_color="#8a4b1e", hover_color="#a55d26",
                                           command=lambda: self.run("uninstall"))
        self.btn_uninstall.pack(side="left", padx=(0, 6))
        self.btn_wizard = ctk.CTkButton(act, text="首次设置向导…", height=32, font=FONT_S,
                                        fg_color=GREY, hover_color=GREY_H,
                                        command=self.open_wizard)
        self.btn_wizard.pack(side="left")

        self.out = ctk.CTkTextbox(body, height=150, font=FONT_C,
                                  fg_color="#141414", activate_scrollbars=True)
        self.out.pack(fill="x", padx=12, pady=(10, 12))
        self.out.insert("end", "（部署过程的输出会贴在这里）")
        self.out.configure(state="disabled")

    # ------------------------------------------------------------ 数据
    def _load_current(self):
        cur = Path(P.DEPLOY)
        exe = cur.parent / "UnityCrossFire.exe"
        self.src_lbl.configure(text="来源：" + P.DEPLOY_SOURCE_CN.get(P.DEPLOY_SOURCE, P.DEPLOY_SOURCE))
        self.set_game(exe.parent if exe.is_file() else None, note="")

    def reload(self):
        self.set_game(self.game, note="")

    def choose(self):
        picked = filedialog.askopenfilename(
            title="选择 UnityCrossFire.exe",
            filetypes=[("UnityCrossFire", "UnityCrossFire.exe"), ("可执行文件", "*.exe")],
        )
        if not picked:
            return
        game = D.resolve_game(picked)
        if game is None:
            messagebox.showerror("选错了", "请选 UnityCrossFire.exe 本身，或者游戏目录。")
            return
        self.set_game(game, note="已切换，记得点「重启控制台」让其它页签也跟着换")

    def set_game(self, game, note=""):
        self.game = Path(game) if game else None
        self.hint_lbl.configure(text=note)
        if not self.game:
            self.path_var.set("（未配置）")
            self._render_rows([("缺失", "UnityCrossFire.exe", "还没选游戏")])
            self._enable(False)
            return
        self.path_var.set(str(self.game / "UnityCrossFire.exe"))
        self.steps = None
        try:
            self.steps = D.build_plan(self.game)
        except Exception:
            self.steps = None
        self._render_rows(self._status())
        self._enable(True)

    def _status(self):
        rows = []
        if not self.steps:
            return [("缺失", "payload", "payload 目录不完整，无法部署")]
        for s in self.steps:
            dst = s["dst"]
            rel = str(dst.relative_to(self.game)).replace(os.sep, "/")
            if not dst.is_file():
                rows.append(("缺失", rel, s["role"]))
            elif D.sha256_file(dst) != s["sha256"]:
                rows.append(("不一致", rel, s["role"]))
            else:
                rows.append(("一致", rel, s["role"]))
        return rows

    def _render_rows(self, rows):
        for w in self.rows.winfo_children():
            w.destroy()
        color = {"一致": "#2f9e44", "缺失": "#c92a2a", "不一致": "#d6b676"}
        for state, name, role in rows:
            r = ctk.CTkFrame(self.rows, fg_color="transparent")
            r.pack(fill="x", pady=1)
            ctk.CTkLabel(r, text=state, font=FONT_S, width=52, anchor="w",
                         text_color=color.get(state, "#c9d1d9")).pack(side="left")
            ctk.CTkLabel(r, text=name, font=FONT_C, width=220, anchor="w",
                         text_color="#c9d1d9").pack(side="left")
            ctk.CTkLabel(r, text=role, font=FONT_S, anchor="w",
                         text_color="#7f8792").pack(side="left", fill="x", expand=True)

    def _enable(self, on):
        state = "normal" if on else "disabled"
        for b in (self.btn_deploy, self.btn_repair, self.btn_verify, self.btn_uninstall):
            b.configure(state=state)

    def _write(self, text):
        self.out.configure(state="normal")
        self.out.insert("end", text)
        self.out.see("end")
        self.out.configure(state="disabled")

    def open_folder(self):
        if not self.game:
            return
        target = self.game / "ucf_mod" if (self.game / "ucf_mod").is_dir() else self.game
        try:
            os.startfile(str(target))
        except Exception as exc:
            self._write(f"\n打不开目录：{exc}\n")

    def open_wizard(self):
        try:
            import first_run
            importlib.reload(first_run)
            if first_run.run_wizard():
                self.hint_lbl.configure(text="向导已完成，点「重启控制台」后生效")
                self._load_current()
        except Exception as exc:
            self._write(f"\n首启向导打不开：{exc}\n")

    # ------------------------------------------------------------ 执行
    def run(self, kind):
        if not self.game or self.busy:
            return
        if kind == "uninstall":
            if not messagebox.askyesno("确认卸载", "把部署进游戏目录的文件删掉，并还原覆盖前的原件？"):
                return
        self.busy = True
        for b in (self.btn_deploy, self.btn_repair, self.btn_verify, self.btn_uninstall, self.btn_wizard):
            b.configure(state="disabled")
        self._write(f"\n──── {kind} ────\n")
        threading.Thread(target=self._worker, args=(kind, self.game), daemon=True).start()

    def _worker(self, kind, game):
        buf = io.StringIO()
        try:
            steps = D.build_plan(game)
            with contextlib.redirect_stdout(buf):
                if kind == "deploy":
                    rc = D.run_deploy(game, steps, repair=False)
                elif kind == "repair":
                    rc = D.run_deploy(game, steps, repair=True)
                elif kind == "verify":
                    rc = D.run_verify(game)
                else:
                    rc = D.run_uninstall(game)
        except Exception as exc:
            buf.write(f"\n[X] 执行异常：{exc}\n")
            rc = 3
        self.q.put((buf.getvalue(), rc))

    def _pump(self):
        try:
            while True:
                text, rc = self.q.get_nowait()
                self._write(text.replace("\n\n", "\n") + f"\n[退出码 {rc}]\n")
                self.busy = False
                self._enable(bool(self.game))
                if self.game:
                    self._render_rows(self._status())
        except queue.Empty:
            pass
        self.console.after(150, self._pump)


def build_deploy_tab(console, tab):
    return DeployTab(console, tab)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("部署页 · 预览")
    root.geometry("900x760")
    tv = ctk.CTkTabview(root)
    tv.pack(fill="both", expand=True, padx=10, pady=10)
    build_deploy_tab(root, tv.add("部署"))
    root.mainloop()
