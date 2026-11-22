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


def _tag_of(game_dir):
    r"""短标签：从游戏目录往上跳过像游戏名的层级（…\\test-1\\UnityCrossFire1.7.1 -> test-1）。"""
    parts = [p for p in str(game_dir).replace("/", "\\").split("\\") if p]
    i = len(parts) - 1
    while i >= 0 and parts[i].lower().startswith("unitycrossfire"):
        i -= 1
    if i >= 0:
        return parts[i]
    return os.path.basename(str(game_dir)) or str(game_dir)


def _compact(path, limit=60):
    r"""路径太长就省略：只留盘符 + 末尾若干层（区分信息通常在尾巴上）。"""
    path = str(path or "")
    if len(path) <= limit:
        return path
    drive, rest = os.path.splitdrive(path)
    keep = limit - len(drive) - 2
    if keep <= 8:
        return path[: limit - 1] + "…"
    return drive + "\\…" + rest[-keep:]


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
        self._pending_switch = False      # 用户选了新位置并同意"部署完就切过去"
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
        # 输入框宽度有限会把路径截断，这里单独一行把**完整 exe 路径**显示出来（自动换行）
        self.exe_path_lbl = ctk.CTkLabel(box, text="", font=("Consolas", 11),
                                         text_color="#7f8792", anchor="w", justify="left",
                                         wraplength=660)
        self.exe_path_lbl.pack(fill="x", padx=12, pady=(0, 2))

        # 2026-11-22 用户要求：记住用过的几个游戏位置，能挑一个启动
        hrow = ctk.CTkFrame(box, fg_color="transparent")
        hrow.pack(fill="x", padx=12, pady=(0, 6))
        ctk.CTkLabel(hrow, text="历史位置", font=FONT_S, text_color="#9aa0a6",
                     width=56, anchor="w").pack(side="left")
        self.hist_var = ctk.StringVar(value="（还没有记录）")
        self.hist_menu = ctk.CTkOptionMenu(hrow, values=["（还没有记录）"], variable=self.hist_var,
                                           width=390, height=26, font=FONT_C,
                                           fg_color=GREY, button_color="#4a5058",
                                           command=self._on_hist_pick)
        self.hist_menu.pack(side="left", padx=(8, 6), fill="x", expand=True)
        ctk.CTkButton(hrow, text="切换并重启", width=100, height=26, font=FONT_S,
                      command=self.switch_selected).pack(side="left")
        ctk.CTkButton(hrow, text="忘记", width=56, height=26, font=FONT_S,
                      fg_color="#5a3434", hover_color="#6d3f3f",
                      command=self.forget_selected).pack(side="left", padx=(6, 0))
        # 下拉框里只放短标签（区分用的文件夹名），完整路径单独一行显示，不靠猜
        self.hist_path_lbl = ctk.CTkLabel(box, text="", font=("Consolas", 11),
                                          text_color="#7f8792", anchor="w")
        self.hist_path_lbl.pack(fill="x", padx=12, pady=(0, 4))

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
        self._refresh_history()

    def _refresh_history(self):
        r"""把最近用过的游戏位置灌进下拉框。

        下拉框只放短标签（区分用的文件夹名 + 盘符），完整路径单独一行显示——
        路径一长，中间省略容易把 test-1 这种关键层级吃掉，光看下拉框会选错。
        """
        hist = P.load_history()
        self._hist_map = {}
        values = []
        for item in hist:
            g = item["game_dir"]
            drive = os.path.splitdrive(g)[0] or "?"
            base = "%s（%s）" % (_tag_of(g), drive)
            if item.get("current"):
                base += " · 在用"
            if not item["exists"]:
                base += " · 不存在"
            label, n = base, 2
            while label in self._hist_map:
                label = "%s #%d" % (base, n)
                n += 1
            self._hist_map[label] = g
            values.append(label)
        if not values:
            values = ["（还没有记录）"]
        self.hist_menu.configure(values=values)
        cur = str(P.game_dir_of()).lower()
        for label, g in self._hist_map.items():
            if g.lower() == cur:
                self.hist_var.set(label)
                self._on_hist_pick(label)
                break
        else:
            self.hist_var.set(values[0])
            self._on_hist_pick(values[0])

    def _on_hist_pick(self, choice=None):
        g = getattr(self, "_hist_map", {}).get(choice or self.hist_var.get(), "")
        self.hist_path_lbl.configure(text=g or "（还没有记录）",
                                     text_color="#7f8792" if os.path.isdir(g) else "#c92a2a")

    def switch_selected(self):
        g = getattr(self, "_hist_map", {}).get(self.hist_var.get())
        if not g:
            return
        if not os.path.isfile(os.path.join(g, "UnityCrossFire.exe")):
            messagebox.showerror("位置不存在", "这个目录里没有 UnityCrossFire.exe：\n" + g)
            return
        try:
            P.save_deploy(g)
        except OSError as exc:
            messagebox.showerror("写配置失败", str(exc))
            return
        if messagebox.askyesno("切换游戏位置",
                               "把控制台切到：\n%s\n\n现在重启控制台让它生效？" % g):
            restart_console()
        else:
            self.hint_lbl.configure(text="已记住，下次启动生效")

    def forget_selected(self):
        g = getattr(self, "_hist_map", {}).get(self.hist_var.get())
        if not g:
            return
        if not P.forget_history(g):
            messagebox.showinfo("删不了", "这是当前正在用的位置；先切到别的，再回来忘掉它。")
            return
        self._refresh_history()

    def reload(self):
        self.set_game(self.game, note="")

    def choose(self):
        r"""选择游戏 = 选择"接下来从哪一份启动"。

        2026-11-22 用户反馈：选完只是本页换了，底部「开始游戏」还在启动旧的那份，
        完全看不出来。现在选完直接问一句 —— 同意就部署 + 切换 + 重启，一步到位。
        """
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
        self.set_game(game, note="")
        if str(game).lower() == str(P.game_dir_of()).lower():
            self.hint_lbl.configure(text="✓ 这就是控制台当前生效的位置", text_color="#7f8792")
            return
        if messagebox.askyesno(
                "切换游戏位置",
                "把控制台切到这一份？\n\n%s\n\n（会先部署，然后重启控制台；"
                "底部「开始游戏」以后就从它启动）" % game):
            self._pending_switch = True
            self.run("deploy")

    def set_game(self, game, note=""):
        self.game = Path(game) if game else None
        self.hint_lbl.configure(text=note)
        if not self.game:
            self.path_var.set("（未配置）")
            self.exe_path_lbl.configure(text="还没有选游戏：点右边按钮选 UnityCrossFire.exe",
                                        text_color="#c92a2a")
            self._render_rows([("缺失", "UnityCrossFire.exe", "还没选游戏")])
            self._enable(False)
            return
        self.path_var.set(str(self.game / "UnityCrossFire.exe"))
        exe = self.game / "UnityCrossFire.exe"
        cur = str(P.game_dir_of())
        if str(self.game).lower() == cur.lower():
            self.hint_lbl.configure(text="✓ 控制台当前生效的位置", text_color="#7f8792")
        else:
            self.hint_lbl.configure(
                text="⚠ 仅查看：底部「开始游戏」现在启动的还是 %s" % _tag_of(cur),
                text_color="#f7cd74")
        self.exe_path_lbl.configure(
            text="启动用这个 exe：" + str(exe),
            text_color="#7f8792" if exe.is_file() else "#c92a2a")
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
        self.q.put((kind, buf.getvalue(), rc))

    def _pump(self):
        try:
            while True:
                kind, text, rc = self.q.get_nowait()
                self._write(text.replace("\n\n", "\n") + f"\n[退出码 {rc}]\n")
                self.busy = False
                self._enable(bool(self.game))
                if self.game:
                    self._render_rows(self._status())
                if kind in ("deploy", "repair"):
                    if rc == 0 and self.game:
                        self._after_deploy()
                    else:
                        self._pending_switch = False      # 部署失败就别惦记着重启了
        except queue.Empty:
            pass
        self.console.after(150, self._pump)

    def _after_deploy(self):
        r"""部署成功：把这个位置记进用户配置 + 历史，并问一句要不要马上切过去。"""
        try:
            P.save_deploy(self.game)
        except OSError as exc:
            self._write("\n[!!] 写用户配置失败：%s\n" % exc)
            return
        self._refresh_history()
        same = str(P.game_dir_of()).lower() == str(self.game).lower()
        if same:
            self.hint_lbl.configure(text="✓ 已部署，控制台正在用这个位置", text_color="#7f8792")
            self._pending_switch = False
            return
        self.hint_lbl.configure(text="已部署并记住；重启后生效", text_color="#f7cd74")
        if self._pending_switch:
            self._pending_switch = False
            restart_console()          # choose() 里已经问过了，这里直接重启
            return
        if messagebox.askyesno("切换游戏位置",
                               "部署完成：\n%s\n\n现在重启控制台切到它吗？" % self.game):
            restart_console()


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
