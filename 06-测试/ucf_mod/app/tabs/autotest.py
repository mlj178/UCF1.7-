#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「车测」页：插件自己在进程内逐张 LoadScene。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import os
import queue
import subprocess
import threading
import time
import tkinter as tk

import customtkinter as ctk

from ui.consts import AT_CAN, AT_CANNOT, AT_NOTE, AT_QUICK, AT_SUMMARY, FONT, FONT_S
from ui.env import GAME_EXE, LOG_DIR
from ui.maps import load_level_table
from ui.util import find_log, kill_game, read_log_from, save_cfg


class AutotestTab:
    # ---- 车测页：插件在进程内逐张 LoadScene，不用鼠标键盘（原 tools\autotest.ps1 的 GUI 版）----
    def build_autotest_tab(self, tab):
        r"""关游戏 → 带 UCF_AUTOTEST 重开 → 轮询日志里的 RESULT PASS / FAIL / crash。
        关键点：开跑前必须先删旧 autotest.txt，否则上一次的 PASS 会被立刻当成这次的结果。"""
        self.at_levels = load_level_table()
        at = self.cfg.get("autotest") if isinstance(self.cfg.get("autotest"), dict) else {}
        sel = at.get("targets")
        if not isinstance(sel, list):
            sel = [7, 10]
        sel = set(int(x) for x in sel if str(x).isdigit())
        self.at_maps = {}
        self.at_q = queue.Queue()
        self.at_stop = threading.Event()
        self.at_busy = False

        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text="车测 = 关游戏 → 带 UCF_AUTOTEST 重开 → 插件在进程内逐张 LoadScene，"
                              "每张等 settle×250 ms → RESULT PASS 后退出。\n"
                              "只验加载链路：PASS 不代表「大厅 → 开始比赛」正常；开跑会备份 ucf_mod.log、"
                              "删旧 autotest.txt。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=620).pack(fill="x", padx=12, pady=(8, 2))

        # 结果放在最上面：窗口不高时进度框要滚动才看得到，结论必须一眼可见
        self.lbl_at = ctk.CTkLabel(body, text="", font=FONT, anchor="w", justify="left",
                                   wraplength=620, text_color="#9aa0a6")
        self.lbl_at.pack(fill="x", padx=14, pady=(8, 0))
        # 2026-11-24：总开关关着时的红条（要说了才 pack，不占空档）
        self.lbl_at_warn = ctk.CTkLabel(body, text="", font=FONT_S, anchor="w", justify="left",
                                        wraplength=620, text_color="#ffb59d")

        self.section_title(body, "地图（勾几张跑几张；数字 = buildIndex，不是 maps 里的序号）")
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(6, 0))
        for i, (lv, name) in enumerate(self.at_levels):
            n = int("".join(ch for ch in lv if ch.isdigit()) or 0)
            var = tk.BooleanVar(value=n in sel)
            self.at_maps[lv] = var
            ctk.CTkCheckBox(box, text="%d %s" % (n, name), variable=var, font=FONT_S,
                            checkbox_width=18, checkbox_height=18,
                            command=self.on_at_change).grid(
                row=i // 4, column=i % 4, sticky="w",
                padx=(12, 4), pady=(8 if i < 4 else 2, 0))
        for c in range(4):
            box.grid_columnconfigure(c, weight=1)
        ctk.CTkLabel(box, text="", height=4).grid(
            row=(len(self.at_levels) + 3) // 4, column=0, columnspan=4)

        self.section_title(body, "参数")
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(6, 0))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(8, 0))
        self.at_warm = tk.StringVar(value=str(at.get("warm", 40)))
        self.at_settle = tk.StringVar(value=str(at.get("settle", 120)))
        self.at_timeout = tk.StringVar(value=str(at.get("timeout", 600)))
        for title, var, width in (("warm（切图前等）", self.at_warm, 58),
                                  ("settle（每张等）", self.at_settle, 58),
                                  ("超时（秒）", self.at_timeout, 58)):
            ctk.CTkLabel(row, text=title, font=FONT_S).pack(side="left", padx=(0, 4))
            ent = ctk.CTkEntry(row, textvariable=var, width=width, font=FONT_S)
            ent.pack(side="left", padx=(0, 12))
            ent.bind("<FocusOut>", self.on_at_change)   # 填完就存，重启还是这三个数
            ent.bind("<Return>", self.on_at_change)
        self.at_exit = tk.BooleanVar(value=bool(at.get("exit", True)))
        ctk.CTkSwitch(box, text="跑完自动退出（PASS 后关游戏）", variable=self.at_exit,
                      font=FONT_S, progress_color="#2f9e44",
                      command=self.on_at_change).pack(
            anchor="w", padx=14, pady=(6, 0))
        self.at_freecam = tk.BooleanVar(value=bool(at.get("freecam", True)))
        ctk.CTkSwitch(box, text="自由视角（WASD 移动 · 按住右键转视角 · F7 开关）",
                      variable=self.at_freecam, font=FONT_S,
                      progress_color="#2f9e44",
                      command=self.on_at_change).pack(
            anchor="w", padx=14, pady=(2, 8))

        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=(6, 0))
        self.btn_at_run = ctk.CTkButton(row, text="开跑（会先关游戏）", font=FONT, height=34,
                                        fg_color="#2f6fdb", hover_color="#255bb4",
                                        command=self.run_autotest)
        self.btn_at_run.pack(side="left", padx=(0, 6))
        self.btn_at_stop = ctk.CTkButton(row, text="中止（关游戏）", font=FONT_S, height=34,
                                         width=110, fg_color="#8a4b1e", hover_color="#a55d26",
                                         state="disabled", command=self.stop_autotest)
        self.btn_at_stop.pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="打开日志", font=FONT_S, height=34, width=88,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.open_file(find_log("ucf_mod.log"), "ucf_mod.log")).pack(
            side="right", padx=(6, 0))
        ctk.CTkButton(row, text="打开结果", font=FONT_S, height=34, width=88,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.open_file(find_log("autotest.txt"), "autotest.txt")).pack(
            side="right")

        self.at_out = ctk.CTkTextbox(body, height=110, font=("Consolas", 11),
                                     fg_color="#141414", activate_scrollbars=True)
        self.at_out.pack(fill="x", padx=12, pady=(6, 12))
        self.at_out.insert("end", "（点「开跑」后这里贴 [at] 进度：warm / LOAD / OK / RESULT）")
        self.at_out.configure(state="disabled")

        self.section_title(body, "车测是干什么的")
        helpbox = ctk.CTkFrame(body, corner_radius=8)
        helpbox.pack(fill="x", padx=10, pady=(6, 12))

        def help_title(text):
            ctk.CTkLabel(helpbox, text=text, font=("Microsoft YaHei UI", 12, "bold"),
                         text_color="#e6edf3", anchor="w").pack(
                fill="x", padx=12, pady=(10, 2))

        def help_line(text, color="#c9d1d9"):
            ctk.CTkLabel(helpbox, text=text, font=FONT_S, text_color=color,
                         anchor="w", justify="left", wraplength=590).pack(
                fill="x", padx=16, pady=(0, 2))

        help_title("能做的事")
        for name, desc in AT_CAN:
            help_line("%s —— %s" % (name, desc))
        help_title("不能做的事")
        for item in AT_CANNOT:
            help_line("· " + item)
        help_title("注意")
        help_line(AT_NOTE)
        help_title("一句话")
        help_line(AT_SUMMARY)
        ctk.CTkLabel(helpbox, text=AT_QUICK, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=590).pack(
            fill="x", padx=12, pady=(6, 10))
        self.refresh_at()
        self.after(400, self.pump_autotest)

    def refresh_at(self):
        r"""autotest.txt 最后一条 RESULT → 「上一次车测」；没有 RESULT 说明中途被杀/崩了。"""
        self.refresh_at_ready()          # 先把「能不能开跑」刷了，再贴上一次的结果
        if not hasattr(self, "lbl_at") or self.at_busy:
            return
        try:
            with open(find_log("autotest.txt"), "r", encoding="utf-8", errors="replace") as f:
                lines = [ln.strip() for ln in f if ln.strip()]
        except OSError:
            self.lbl_at.configure(text="上一次车测：还没有 autotest.txt", text_color="#9aa0a6")
            return
        last = ""
        for ln in lines:
            if ln.startswith("RESULT"):
                last = ln
        if last:
            ok = "PASS" in last
            self.lbl_at.configure(text="上一次车测：" + last,
                                  text_color="#4ec97a" if ok else "#e8654f")
        else:
            self.lbl_at.configure(text="上一次车测：没跑到 RESULT（中途关游戏 / 崩溃）",
                                  text_color="#e8c15a")

    def refresh_at_ready(self):
        r"""「开跑」跟着插件总开关走。

        总开关关着 = plugin.c 里 loaded but idle：车测启动的游戏不读 nav、不写 autotest.txt，
        代理只能一直等到 timeout。所以关着时禁用按钮 + 红条说清楚，别让人白等。
        """
        if not hasattr(self, "btn_at_run") or getattr(self, "at_busy", False):
            return
        off = not bool(self.master_var.get())
        self.btn_at_run.configure(state="disabled" if off else "normal")
        self.set_at_warn("插件总开关关着：车测启动的插件会待机（不读 nav、不出菜单），跑不出结果。"
                         "先在右上角打开「插件总开关」再开跑。" if off else "")

    def set_at_warn(self, text=""):
        r"""车测页的红条；没话可说就收起来，不留一条空白。"""
        if not hasattr(self, "lbl_at_warn"):
            return
        if text:
            self.lbl_at_warn.configure(text=text)
            if not self.lbl_at_warn.winfo_manager():
                self.lbl_at_warn.pack(fill="x", padx=14, pady=(4, 0), before=self.lbl_at)
        elif self.lbl_at_warn.winfo_manager():
            self.lbl_at_warn.pack_forget()

    def _at_int(self, var, default):
        try:
            return max(0, int(str(var.get()).strip()))
        except (TypeError, ValueError):
            return default

    def run_autotest(self):
        if self.at_busy:
            return
        # 2026-11-24：总开关关着 = 插件待机，车测只会白等到 timeout，先拦住
        if not bool(self.master_var.get()):
            self.set_status("车测：插件总开关关着（先在右上角打开再开跑）")
            self.refresh_at_ready()
            return
        picked = [lv for lv, var in self.at_maps.items() if var.get()]
        if not picked:
            self.set_status("车测：至少勾一张图")
            return
        if not os.path.isfile(GAME_EXE):
            self.set_status("找不到 %s" % GAME_EXE)
            return
        picked.sort(key=lambda lv: int("".join(ch for ch in lv if ch.isdigit()) or 0))
        idx = ",".join(str(int("".join(ch for ch in lv if ch.isdigit()) or 0)) for lv in picked)
        warm = self._at_int(self.at_warm, 40)
        settle = self._at_int(self.at_settle, 120)
        timeout = max(30, self._at_int(self.at_timeout, 600))
        exit_when_done = bool(self.at_exit.get())
        freecam = bool(self.at_freecam.get())

        env, note = self.game_env()          # Tk 变量只在主线程读
        env["UCF_AUTOTEST"] = idx
        env["UCF_AT_WARM"] = str(warm)
        env["UCF_AT_SETTLE"] = str(settle)
        env["UCF_AT_EXIT"] = "1" if exit_when_done else "0"
        if freecam:
            env["UCF_FREECAM"] = "1"
        else:
            env.pop("UCF_FREECAM", None)     # 取消勾选时别把父进程的环境带进去

        self.save_autotest_ui()          # 车测页的勾选/参数：开跑前顺手再存一次
        try:
            save_cfg(self.cfg)
        except OSError:
            pass

        self.at_busy = True
        self.at_stop.clear()
        # 车测也是本窗口启动的：记下启动瞬间的条件，启动条别误报成「外部启动」
        strip_info = self.launch_strip_info()
        self._strip_run = strip_info
        self.btn_at_run.configure(state="disabled")
        self.btn_at_stop.configure(state="normal")
        names = " → ".join("%s(%s)" % (name, lv) for lv, name in self.at_levels if lv in picked)
        self.lbl_at.configure(text="车测进行中：%s · settle=%d · %s" % (names, settle, note),
                              text_color="#e8c15a")
        self.at_out.configure(state="normal")
        self.at_out.delete("1.0", "end")
        self.at_out.insert("end", "目标 %s · warm=%d settle=%d timeout=%ds · %s\n"
                           % (idx, warm, settle, timeout, note))
        self.at_out.configure(state="disabled")
        self.set_status("车测：正在关闭游戏 …")
        threading.Thread(target=self._at_worker,
                         args=(env, idx, timeout, strip_info), daemon=True).start()

    def stop_autotest(self):
        if not self.at_busy:
            return
        self.at_stop.set()
        self.set_status("车测：正在中止（关游戏）…")

    def save_autotest_ui(self):
        r"""车测页的勾选 + 参数也写进 ucf_mod.json：下次打开还是上次那一套。"""
        if not hasattr(self, "at_maps"):
            return
        self.cfg["autotest"] = {
            "targets": [int("".join(ch for ch in lv if ch.isdigit()) or 0)
                        for lv, var in self.at_maps.items() if var.get()],
            "warm": self._at_int(self.at_warm, 40),
            "settle": self._at_int(self.at_settle, 120),
            "timeout": max(30, self._at_int(self.at_timeout, 600)),
            "exit": bool(self.at_exit.get()),
            "freecam": bool(self.at_freecam.get()),
        }

    def on_at_change(self, _event=None):
        r"""勾一下 / 改个数就落盘（以前只在点「开跑」时才存）。"""
        self.save_autotest_ui()
        try:
            save_cfg(self.cfg)
        except OSError as exc:
            self.set_status("写不进 ucf_mod.json：%s" % exc)
            return
        self.set_status("已保存 车测设置")

    def _at_worker(self, env, idx, timeout, strip_info=None):
        r"""工作线程只读日志/开进程/写队列，Tk 控件一律回主线程改（pump_autotest）。"""
        q = self.at_q

        def put(kind, text):
            q.put((kind, text))

        try:
            put("line", "关闭游戏进程 …")
            if not kill_game():
                put("result", "RESULT 中止：游戏进程关不掉")
                return
            prev = os.path.join(LOG_DIR, "ucf_mod.prev_%s.log" % time.strftime("%H%M%S"))
            try:
                os.makedirs(LOG_DIR, exist_ok=True)
                os.replace(find_log("ucf_mod.log"), prev)
                put("line", "日志已备份：%s" % os.path.basename(prev))
            except OSError:
                pass
            try:
                os.remove(find_log("autotest.txt"))   # 不删就会把上一次的 PASS 当成这次的结果
                put("line", "已删旧 autotest.txt")
            except OSError:
                pass
            put("line", "启动 UnityCrossFire.exe  UCF_AUTOTEST=%s" % idx)
            # 关游戏和重开之间 refresh 可能把快照清掉，这里补回（只写数据，不碰 Tk）
            if strip_info:
                self._strip_run = strip_info
            proc = subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE), env=env)
            offset = 0
            seen = ""
            t0 = time.time()
            while True:
                if self.at_stop.is_set():
                    kill_game()
                    put("result", "RESULT 中止（手动，已关游戏）")
                    return
                text, offset = read_log_from(find_log("ucf_mod.log"), offset)
                if text:
                    seen += text
                    for line in text.splitlines():
                        low = line.lower()
                        if "!!! crash" in low:
                            put("line", line)
                        elif ("[at]" in line and "resolve:" not in line
                              and "settle level" not in line):
                            put("line", line)
                if "!!! crash" in seen:
                    put("result", "RESULT CRASH（VEH 已记录，见日志 crash 段）")
                    return
                if "RESULT PASS" in seen:
                    put("result", "RESULT PASS（%d 张图，%ds）"
                        % (len(idx.split(",")), int(time.time() - t0)))
                    return
                if "RESULT FAIL" in seen:
                    put("result", "RESULT FAIL（%ds，见日志）" % int(time.time() - t0))
                    return
                if proc.poll() is not None:
                    # 进程没了但可能刚写最后一行：再读一次再判
                    text, offset = read_log_from(find_log("ucf_mod.log"), offset)
                    seen += text
                    if "RESULT PASS" in seen:
                        put("result", "RESULT PASS（%d 张图，%ds）"
                            % (len(idx.split(",")), int(time.time() - t0)))
                    elif "RESULT FAIL" in seen:
                        put("result", "RESULT FAIL（见日志）")
                    else:
                        put("result", "RESULT CRASH（进程退出但没有 RESULT）")
                    return
                if time.time() - t0 > timeout:
                    kill_game()
                    put("result", "RESULT 超时（%ds，已关游戏）" % timeout)
                    return
                time.sleep(1)
        except Exception as exc:                     # noqa: BLE001
            put("result", "车测异常：%s" % exc)
        finally:
            q.put(("done", ""))

    def pump_autotest(self):
        try:
            while True:
                kind, text = self.at_q.get_nowait()
                if kind == "line":
                    self.at_out.configure(state="normal")
                    self.at_out.insert("end", text + "\n")
                    self.at_out.see("end")
                    self.at_out.configure(state="disabled")
                elif kind == "result":
                    ok = "PASS" in text
                    self.lbl_at.configure(text=text, text_color="#4ec97a" if ok else "#e8654f")
                    self.set_status("车测：" + text)
                    self.at_out.configure(state="normal")
                    self.at_out.insert("end", "\n" + text + "\n")
                    self.at_out.see("end")
                    self.at_out.configure(state="disabled")
                elif kind == "done":
                    self.at_busy = False
                    self.btn_at_run.configure(state="normal")
                    self.btn_at_stop.configure(state="disabled")
                    self.refresh_status()
        except queue.Empty:
            pass
        self.after(400, self.pump_autotest)
