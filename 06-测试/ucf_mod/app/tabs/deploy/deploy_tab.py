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
UCF_ROOT = HERE
while not (UCF_ROOT / ".ucfroot").is_file() and UCF_ROOT.parent != UCF_ROOT:
    UCF_ROOT = UCF_ROOT.parent          # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (UCF_ROOT / "app" / "core", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

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
        # 2026-11-24 用户反馈：下拉框要「先选再点按钮」，选中的那条还藏在弹层里，
        # 换成一列列表行 —— 每行自带「切换 / 忘记」，点一下就换，不用先选中。
        hhead = ctk.CTkFrame(box, fg_color="transparent")
        hhead.pack(fill="x", padx=12, pady=(0, 2))
        ctk.CTkLabel(hhead, text="历史位置", font=FONT_S, text_color="#9aa0a6").pack(side="left")
        ctk.CTkLabel(hhead, text="「编辑」可起名字、写备注", font=FONT_S,
                     text_color="#6b7280").pack(side="right")
        self.hist_box = ctk.CTkFrame(box, fg_color="transparent")
        self.hist_box.pack(fill="x", padx=12, pady=(0, 6))

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
        r"""重建历史位置列表：一行一个位置，动作就在这一行上。

        2026-11-24 用户反馈：下拉框只承载「选中」、按钮另挂在右边，等于两次操作，
        选中的那条还折在弹层里看不见。改成一列行后切换点一次就完，当前项靠
        边框 + 「在用」标出来，目录不存在的直接标红并禁用切换。
        """
        for w in self.hist_box.winfo_children():
            w.destroy()
        hist = P.load_history()
        if not hist:
            ctk.CTkLabel(self.hist_box, text="（还没有记录，选一次游戏位置就会记下来）",
                         font=FONT_S, text_color="#6b7280", anchor="w").pack(fill="x", pady=2)
            return
        for item in hist:
            self._hist_row(item["game_dir"], bool(item.get("current")), bool(item["exists"]),
                           item.get("name") or "", item.get("note") or "")

    def _hist_row(self, game_dir, is_current, exists, name, note):
        r"""一行 = 两行信息：上面是名字 + 备注 + 动作，下面是路径。

        2026-11-24 用户要求：备注跟在名字后面同一行（一眼就能对上「这份是干嘛的」），
        路径单独放第二行，不再被备注挤掉。
        """
        r = ctk.CTkFrame(self.hist_box, corner_radius=6,
                         fg_color="#2b3038" if is_current else "#22262c")
        r.pack(fill="x", pady=2)

        l1 = ctk.CTkFrame(r, fg_color="transparent")
        l1.pack(fill="x", padx=(8, 6), pady=(4, 0))
        ctk.CTkLabel(l1, text="●", font=("Segoe UI", 9), width=12, height=18,
                     text_color="#2f9e44" if is_current else "#5b626b").pack(
            side="left", padx=(0, 6))
        title = name or _tag_of(game_dir)
        if len(title) > 16:                       # 太长的名字会把整行撑开
            title = title[:15] + "…"
        ctk.CTkLabel(l1, text=title, font=FONT, height=20, anchor="w",
                     text_color="#e6edf3" if name else "#9aa0a6").pack(side="left")

        if is_current:
            ctk.CTkLabel(l1, text="在用", font=FONT_S, text_color="#2f9e44").pack(
                side="right")
            if not exists:
                ctk.CTkLabel(l1, text="目录不存在", font=FONT_S,
                             text_color="#c92a2a").pack(side="right", padx=(0, 8))
            ctk.CTkButton(l1, text="编辑", width=48, height=22, font=FONT_S,
                          fg_color=GREY, hover_color=GREY_H,
                          command=lambda: self.edit_entry(game_dir, name, note)).pack(
                side="right", padx=(0, 8))
        else:
            ctk.CTkButton(l1, text="忘记", width=48, height=22, font=FONT_S,
                          fg_color="#5a3434", hover_color="#6d3f3f",
                          command=lambda: self.forget(game_dir)).pack(
                side="right")
            ctk.CTkButton(l1, text="切换", width=52, height=22, font=FONT_S,
                          fg_color="#2f9e44" if exists else GREY,
                          hover_color="#37b24d" if exists else GREY,
                          state="normal" if exists else "disabled",
                          command=lambda: self.switch_to(game_dir)).pack(
                side="right", padx=(6, 0))
            if not exists:
                ctk.CTkLabel(l1, text="目录不存在", font=FONT_S,
                             text_color="#c92a2a").pack(side="right", padx=(0, 8))
            ctk.CTkButton(l1, text="编辑", width=48, height=22, font=FONT_S,
                          fg_color=GREY, hover_color=GREY_H,
                          command=lambda: self.edit_entry(game_dir, name, note)).pack(
                side="right", padx=(0, 6))

        # 备注放在最后 pack：先让右边的按钮占好位，剩下的中间空档正好给它
        if note:
            ctk.CTkLabel(l1, text=note if len(note) <= 40 else note[:39] + "…",
                         font=FONT_S, height=18, anchor="w", text_color="#9aa0a6").pack(
                side="left", padx=(8, 0), fill="x", expand=True)

        l2 = ctk.CTkFrame(r, fg_color="transparent")
        l2.pack(fill="x", padx=(26, 10), pady=(0, 4))
        ctk.CTkLabel(l2, text=_compact(game_dir, 80), font=FONT_C, height=18, anchor="w",
                     text_color="#c92a2a" if not exists else "#7f8792").pack(
            side="left", fill="x", expand=True)

    def edit_entry(self, game_dir, name, note):
        r"""给这份位置起名字、写备注（只改显示，不动实际路径）。"""
        dlg = ctk.CTkToplevel(self.console)
        dlg.title("名字与备注")
        dlg.geometry("440x266")
        dlg.resizable(False, False)
        dlg.transient(self.console)

        ctk.CTkLabel(dlg, text="名字（留空就显示文件夹名）", font=FONT_S,
                     text_color="#9aa0a6").pack(anchor="w", padx=16, pady=(14, 2))
        name_var = ctk.StringVar(value=name)
        name_entry = ctk.CTkEntry(dlg, textvariable=name_var, font=FONT, height=30)
        name_entry.pack(fill="x", padx=16)

        ctk.CTkLabel(dlg, text="备注（比如：打了运输船测试包）", font=FONT_S,
                     text_color="#9aa0a6").pack(anchor="w", padx=16, pady=(10, 2))
        note_var = ctk.StringVar(value=note)
        ctk.CTkEntry(dlg, textvariable=note_var, font=FONT, height=30).pack(
            fill="x", padx=16)

        ctk.CTkLabel(dlg, text=_compact(game_dir, 58), font=FONT_C, text_color="#7f8792",
                     anchor="w", justify="left", wraplength=396).pack(
            fill="x", padx=16, pady=(10, 0))

        def save():
            try:
                P.rename_history(game_dir, name_var.get().strip(), note_var.get().strip())
            except OSError as exc:
                messagebox.showerror("写配置失败", str(exc), parent=dlg)
                return
            dlg.destroy()
            self._refresh_history()

        bar = ctk.CTkFrame(dlg, fg_color="transparent")
        bar.pack(fill="x", padx=16, pady=(14, 0))
        ctk.CTkButton(bar, text="保存", width=80, height=28, font=FONT_S,
                      fg_color="#2f9e44", hover_color="#37b24d",
                      command=save).pack(side="right")
        ctk.CTkButton(bar, text="取消", width=70, height=28, font=FONT_S,
                      fg_color=GREY, hover_color=GREY_H,
                      command=dlg.destroy).pack(side="right", padx=(0, 8))
        dlg.bind("<Return>", lambda e: save())
        dlg.bind("<Escape>", lambda e: dlg.destroy())
        dlg.grab_set()
        name_entry.focus_set()

    def switch_to(self, game_dir):
        g = game_dir
        if not os.path.isfile(os.path.join(g, "UnityCrossFire.exe")):
            messagebox.showerror("位置不存在", "这个目录里没有 UnityCrossFire.exe：\n" + g)
            self._refresh_history()
            return
        try:
            P.save_deploy(g)
        except OSError as exc:
            messagebox.showerror("写配置失败", str(exc))
            return
        if messagebox.askyesno("切换游戏位置",
                               "把控制台切到「%s」？\n\n%s\n\n现在重启控制台让它生效？"
                               % (self._label_of(g), g)):
            restart_console()
        else:
            self.hint_lbl.configure(text="已记住，下次启动生效")

    def _label_of(self, game_dir):
        """弹窗里用用户起的名字，没起名字就退回文件夹名。"""
        for item in P.load_history():
            if item["game_dir"].lower() == str(game_dir).lower() and item.get("name"):
                return item["name"]
        return _tag_of(game_dir)

    def forget(self, game_dir):
        if not P.forget_history(game_dir):
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
