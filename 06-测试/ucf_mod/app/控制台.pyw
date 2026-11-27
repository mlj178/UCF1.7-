#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""UCF 控制台 —— 窗口壳（入口）。页签代码在 app/tabs/，共用件在 app/ui/，路径与环境在 app/ui/env.py。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import os
import shutil
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from tabs.autotest import AutotestTab
from tabs.data import DataTab
from tabs.dev.tab import DevTab
from tabs.hotkey import HotkeyTab
from tabs.map import MapTab
from tabs.overview import OverviewTab
from tabs.record.tab import RecordTab
from tabs.vis import VisTab
from tabs.waypoint import WaypointTab
from ui.consts import FONT, FONT_B, FONT_S, GROUPS, LIVE_VIS_KEYS, TAB_GROUPS, TAB_OLD_MAP, USER_PAGES
from ui.env import (BUILD_DLL, CFG_PATH, DEPLOY, DEV, FINAL_ROOT, GAME_EXE, HERE, LOG_DIR,
                    MARKERS, NAVSERVER, P, PACKS, PAYLOAD_DLL, RUNTIME, TEST_VIS)
from ui.kit import Kit
from ui.role import ROLE_DEV, ROLE_LABEL, ROLE_USER, ask_role, env_role, normalize_role, role_from_cfg, save_role
from ui.packs import (
    PackMixin, final_stats, pack_manifest, pack_summary, pack_target_fp,
    prepare_final_root, write_nav_cmd,
)
from ui.util import _python, compact_path, game_running, game_tag, load_cfg, save_cfg, tail_log


class App(Kit, PackMixin, MapTab, VisTab, HotkeyTab, WaypointTab, OverviewTab,
          RecordTab, DataTab, AutotestTab, DevTab, ctk.CTk):
    def __init__(self, role=None):
        super().__init__()
        # 2026-11-24 用户要求：身份决定建哪些页（用户=地图/部署，开发者=全部 10 页）
        self.role = normalize_role(role) or ROLE_DEV
        self.title("UCF 控制台")
        # 高分屏 125% 缩放时 900 逻辑高会把底部按钮顶到任务栏外：
        # 按实际 DPI 折算屏幕可用高度，再夹在 680~900 之间。
        try:
            dpi = self.winfo_fpixels("1i") / 96.0
        except tk.TclError:
            dpi = 1.0
        screen_h = int(self.winfo_screenheight() / max(dpi, 0.5))
        win_h = max(680, min(900, screen_h - 120))
        # 2026-11-18：新增「人机路点」后 9 个页签 + 4 列类型卡需要约 750 内容宽，
        # 760 会把最右一列/最后一个页签裁掉；830 仍低于 1366 屏。
        self.geometry("830x%d+40+20" % win_h)   # 自己定位：交给窗口管理器会压到任务栏
        self.minsize(720, 620)
        self.protocol("WM_DELETE_WINDOW", self.on_close)   # 关窗前把没失焦的输入也存了
        self.cfg = load_cfg()
        feats = self.cfg.setdefault("features", {})
        if not isinstance(feats, dict):
            feats = {}
            self.cfg["features"] = feats
        self.feats = feats
        # 2026-11-19：可视化改成逐类开关；HUD、文字标签都已从游戏里删除
        for _old in ("vis_lists", "vis_layer_a", "vis_layer_b", "vis_layer_c", "vis_layer_d",
                     "hud", "hud_states", "hud_keys", "hud_log", "vis_labels"):
            feats.pop(_old, None)
        # 控制台自己的界面记忆（上次停在哪个页签）：只给控制台读，插件不认这一节
        ui = self.cfg.get("ui")
        if not isinstance(ui, dict):
            ui = {}
            self.cfg["ui"] = ui
        self.ui = ui

        self.vars = {}
        self.widgets = []
        # 2026-11-19：启动条件条（版本 / 包 / 生效图）—— 测试包模式的一次性预检可被静音
        self._mute_preflight = False
        self._strip_run = None

        self.head = ctk.CTkFrame(self, fg_color="transparent")
        self.head.pack(fill="x", padx=18, pady=(16, 4))
        ctk.CTkLabel(self.head, text="UCF 控制台", font=FONT_B).pack(side="left")
        # 身份牌：一眼看出这台机器是「用户」还是「开发者」；旁边随时可切（会重启）
        self.role_chip = ctk.CTkLabel(
            self.head, text=ROLE_LABEL[self.role], width=72, height=24, corner_radius=12,
            font=FONT_S,
            fg_color="#23343f" if self.role == ROLE_USER else "#2a2438",
            text_color="#7fd0e8" if self.role == ROLE_USER else "#c3a6ff")
        self.role_chip.pack(side="left", padx=(14, 4))
        self.btn_role = ctk.CTkButton(self.head, text="切换身份", width=80, height=24,
                                      font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                      command=self.switch_role)
        self.btn_role.pack(side="left")
        # 2026-11-19 用户要求：右上角加「窗口置顶」勾选 + 折叠成小条的开关。
        self.btn_fold = ctk.CTkButton(self.head, text="折叠", width=52, height=24,
                                      font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                      command=self.toggle_fold)
        self.btn_fold.pack(side="right", padx=(10, 0))
        self.master_var = tk.BooleanVar(value=bool(self.cfg.get("enabled", True)))
        # 2026-11-24：总开关只给开发者。用户身份关掉它 = 静默变原版（界面上只改按钮文案），
        # 是坑；用户要原版直接双击 exe，介绍第二行已经写了。master_var 照样从配置初始化，
        # persist() / 启动条 / 预检 / 车测都不用改。
        if self.role == ROLE_DEV:
            ctk.CTkSwitch(self.head, text="插件总开关", variable=self.master_var,
                          font=FONT, progress_color="#2f9e44",
                          command=self.on_master).pack(side="right")
        self.topmost_var = tk.BooleanVar(value=bool(self.ui.get("topmost", False)))
        ctk.CTkCheckBox(self.head, text="窗口置顶", variable=self.topmost_var, font=FONT_S,
                        checkbox_width=20, checkbox_height=20,
                        command=self.on_topmost).pack(side="right", padx=(0, 14))
        self._folded = False
        self._geom_saved = ""
        try:
            self.attributes("-topmost", bool(self.topmost_var.get()))
        except tk.TclError:
            pass

        if self.role == ROLE_USER:
            intro_text = ("只有从本窗口「开始游戏」才会加载 mod；直接双击 UnityCrossFire.exe 是原版。\n"
                          "装好之后，选好图点下面「开始游戏」就行。要改路点 / 做数据，点右上角「切换身份」。")
        else:
            intro_text = ("只有从本窗口「开始游戏」才会加载 mod；直接双击 UnityCrossFire.exe 是原版。\n"
                          "开关改完存进 ucf_mod.json，下次启动生效（游戏开着时要重开）。\n"
                          "启动档（编辑中 / 成品）是「人机路点」页顶部的两页；数据路径 / 还原 / 校验：切到「数据」页。\n"
                          "路点数据只读查看在工作台；现场编辑在「人机路点」页（游戏内 F2 菜单）。")
        self.intro = ctk.CTkLabel(self, text=intro_text,
                                  font=FONT_S, text_color="#9aa0a6", justify="left")
        self.intro.pack(anchor="w", padx=20)

        # ---- 按钮 / 状态：先按底边占位，窗口再矮也不会被页签挤没 ----
        self.bar = ctk.CTkFrame(self, fg_color="transparent")
        self.bar.pack(side="bottom", fill="x", padx=14, pady=(0, 12))
        self.btn_game = ctk.CTkButton(self.bar, text="开始游戏（加载 mod）", font=FONT, height=42,
                                      fg_color="#2f6fdb", hover_color="#255bb4",
                                      command=self.launch_game)
        self.btn_game.pack(side="left", fill="x", expand=True, padx=(0, 6))
        # 用户身份看不到开发入口（2026-11-24）：这个按钮只给开发者
        self.btn_wb = ctk.CTkButton(self.bar, text="路点工作台（查看）", font=FONT, height=42,
                                    fg_color="#3a3f47", hover_color="#4a5058",
                                    command=self.open_workbench)
        if self.role == ROLE_DEV:
            self.btn_wb.pack(side="left", fill="x", expand=True, padx=(6, 0))

        # 2026-11-19：启动条件条 —— 版本/包/生效图常驻在按钮上方，
        # 切到任何页签都看得见；这里只摆控件，文案由 refresh_launch_strip() 刷。
        self.strip = ctk.CTkFrame(self, corner_radius=8, fg_color="#232323",
                                  border_width=1, border_color="#3a3f47")
        self.strip.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
        self.strip_badge = ctk.CTkLabel(self.strip, text="成品", width=78, height=26,
                                        corner_radius=6, fg_color="#16233a",
                                        text_color="#9cc3ff",
                                        font=("Microsoft YaHei UI", 12, "bold"))
        self.strip_badge.pack(side="left", padx=(10, 8), pady=9)
        self.strip_go = ctk.CTkButton(self.strip, text="去人机路点改", width=112, height=28,
                                      font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                      command=self.on_strip_go)
        if self.role == ROLE_DEV:
            self.strip_go.pack(side="right", padx=(8, 10), pady=8)
        self.strip_main = ctk.CTkFrame(self.strip, fg_color="transparent")
        self.strip_main.pack(side="left", fill="x", expand=True, pady=8)
        self.strip_title = ctk.CTkLabel(self.strip_main, text="", anchor="w", justify="left",
                                        font=("Microsoft YaHei UI", 12, "bold"),
                                        wraplength=640)   # 版本名可能很长，宁可折行也别被裁掉
        self.strip_title.pack(fill="x")
        self.strip_sub = ctk.CTkLabel(self.strip_main, text="", anchor="w", justify="left",
                                      font=FONT_S, text_color="#9aa0a6", wraplength=500)
        self.strip_sub.pack(fill="x")
        # 2026-11-22：用户要求「看得见这次到底启动哪个 exe」——常驻显示完整路径
        self.strip_path = ctk.CTkLabel(self.strip_main, text="", anchor="w", justify="left",
                                       font=("Consolas", 11), text_color="#7f8792")
        self.strip_path.pack(fill="x")

        self.stat = ctk.CTkFrame(self, corner_radius=10)
        self.stat.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
        top = ctk.CTkFrame(self.stat, fg_color="transparent")
        top.pack(fill="x", padx=14, pady=(10, 2))
        ctk.CTkLabel(top, text="上次运行", font=("Microsoft YaHei UI", 14, "bold")).pack(side="left")
        self.dot = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
        self.dot.pack(side="right")
        self.logbox = ctk.CTkTextbox(self.stat, height=104, font=("Consolas", 12),
                                     fg_color="#141414", activate_scrollbars=True)
        self.logbox.pack(fill="x", padx=14, pady=(2, 12))

        # 2026-11-24 用户要求：身份决定建哪些页。
        #   用户   —— 平铺两页（地图 / 部署），没有分组条
        #   开发者 —— 4 个功能组 × 组内页（插件开关 / 路点数据 / 部署与测试 / 开发调试）
        self.group_names = []
        self.page_names = []
        self.page_frames = {}
        self.page_show = {}
        self._sub_memo = {}
        self.cur_group, self.cur_page = "", ""
        self._booting = True
        hint_items = {title: (hint, items) for title, hint, items in GROUPS}

        if self.role == ROLE_USER:
            self.tabview = ctk.CTkTabview(self, corner_radius=10, command=self.on_flat_tab)
            self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 4))
            self.group_names = [ROLE_LABEL[ROLE_USER]]
            for page in USER_PAGES:
                self.page_names.append(page)
                self.page_frames[page] = self.tabview.add(page)
            # 2026-11-26 启动加速：先把空窗口画出来，再建当前页，其余页后台逐页建
            self._hint_items = hint_items
            self._built = set()
            self._queue = []
            page = self._restore_user()
            self._paint_now()
            self._ensure_page(page)
            try:
                self.tabview.set(page)          # _booting 期间不触发 on_flat_tab
            except Exception:
                pass
            self.show_flat(page, persist=False)
            self._queue = [p for p in USER_PAGES if p not in self._built]
            self._start_pump(250)
        else:
            self.tabview = ctk.CTkTabview(self, corner_radius=10, command=self.on_group)
            self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 4))
            for group, pages in TAB_GROUPS:
                self.group_names.append(group)
                pane = self.tabview.add(group)
                if len(pages) > 1:
                    frames, show = self.build_sub_tabs(
                        pane, list(pages),
                        on_change=lambda page, g=group: self.show_sub(g, page))
                    self.page_show[group] = show
                else:
                    frame = ctk.CTkFrame(pane, fg_color="transparent")
                    frame.pack(fill="both", expand=True)
                    frames, show = {pages[0]: frame}, None
                    self.page_show[group] = None
                for page in pages:
                    self.page_names.append(page)
                    self.page_frames[page] = frames[page]

            # 2026-11-26 启动加速：先把空窗口画出来，只建当前页，其余按 TAB_GROUPS 顺序后台逐页建
            self._hint_items = hint_items
            self._built = set()
            self._queue = []
            group, page = self._restore_tab()
            self._paint_now()
            self._ensure_page(page)

            try:
                self.tabview.set(group)          # _booting 期间不触发 on_group
            except Exception:
                pass
            self.show_sub(group, page, persist=False)
            # 同一组里的页排前面：用户下一步最可能点的就是这一组
            cur_pages = list(dict(TAB_GROUPS).get(group) or ())
            order = cur_pages + [p for _g, pages in TAB_GROUPS for p in pages
                                 if p not in cur_pages]
            self._queue = [p for p in order if p not in self._built]
            self._start_pump(250)
        self._booting = False

        self._start_status()          # 唯一的一条状态链（见 _safe_status 的说明）

    # ---- 页签：分组（一级）+ 组内页（二级）----
    def build_page(self, page, frame, hint_items):
        r"""把一页建进指定容器。页签名 → build_*_tab 的唯一分派表。

        2026-11-24 分组重构：页签从「平铺 10 个」改成「4 组 × 组内页」，
        各页的 build_* 一行没改，只是父容器从 tabview 换成了组内 frame。
        """
        if page == "快捷键":
            hint, _items = hint_items["快捷键"]
            self.build_hotkey_tab(frame, hint)          # 热键速查（游戏内已不显示）
        elif page == "可视化":
            hint, items = hint_items["可视化"]
            self.build_vis_tab(frame, hint, items)      # 总开关 + 十类数据（勾选）
        elif page == "地图":
            hint, items = hint_items["地图"]
            self.build_group_tab(frame, hint, items)
        elif page == "地图总览":
            self.build_overview_tab(frame)              # 11 张图的状态总览（只读）
        elif page == "人机路点":
            self.build_waypoint_tab(frame)              # SyPB 式现场编辑入口
        elif page == "录制":
            self.build_record_tab(frame)                # 走一遍就把路线录下来（只写 ② 编辑中）
        elif page == "数据":
            self.build_data_tab(frame)                  # 三区路径/时间 + 部署/还原/校验
        elif page == "部署":
            try:
                import deploy_tab
                self.deploy_tab = deploy_tab.build_deploy_tab(self, frame)
            except Exception as exc:                 # 部署页坏了也别把整个控制台带崩
                ctk.CTkLabel(frame, text="部署页加载失败：%s" % exc,
                             font=FONT_S, text_color="#c92a2a").pack(padx=12, pady=12)
        elif page == "车测":
            self.build_autotest_tab(frame)              # 插件自己在进程内逐张切图
        elif page == "开发者选项":
            self.build_dev_tab(frame)                   # 坐标记录 + 原始轨迹（排在最后一组）
        else:
            raise ValueError("控制台没有这一页：%s" % page)

    # ---- 启动加速（2026-11-26）：先画窗口，页面按需 / 后台逐页建 ----------
    _PAGE_DEPS = {"数据": ("人机路点",), "车测": ("人机路点",),
                  "录制": ("人机路点",), "部署": ("人机路点",)}

    def _paint_now(self):
        r"""把还没建页的空壳先画出来：用户先看到窗口，不用等 10 页建完。"""
        try:
            self.update_idletasks()
            self.update()
        except tk.TclError:
            pass

    def _ensure_page(self, page):
        r"""这一页没建就现在建；有依赖的页先补依赖（数据/车测/录制读人机路点的 opt_*）。

        2026-11-26：加 `_building` 重入保护 —— 建页过程中如果被 `update()`（折叠/对话框）
        重入，不能再建一遍，否则会自己嵌套自己，界面就卡死。
        """
        if page in getattr(self, "_built", ()):
            return
        if page in getattr(self, "_building", ()):
            return
        if not hasattr(self, "_building"):
            self._building = set()
        for dep in self._PAGE_DEPS.get(page, ()):
            self._ensure_page(dep)
        frame = self.page_frames.get(page)
        if frame is None:
            return
        self._building.add(page)
        try:
            self.build_page(page, frame, self._hint_items)
        finally:
            self._building.discard(page)
        self._built.add(page)

    def _start_pump(self, delay=150):
        r"""只保留一条后台建页的链：重复排程会叠成两条，越跑越像卡死。"""
        if getattr(self, "_pump_on", False):
            return
        self._pump_on = True
        try:
            self._pump_job = self.after(int(delay), self._pump_pages)
        except tk.TclError:
            self._pump_on = False
            self._pump_job = None

    def _stop_pump(self):
        r"""停掉后台建页（折叠 / 关窗）；展开时 _start_pump 再续上。"""
        job = getattr(self, "_pump_job", None)
        self._pump_job = None
        self._pump_on = False
        if job:
            try:
                self.after_cancel(job)
            except Exception:             # noqa: BLE001  已经跑过/已被销毁
                pass

    def _pump_pages(self):
        r"""后台逐页建：一次只建一页，建完让出主线程，窗口不卡。

        2026-11-26：折叠时暂停（页签都藏起来了，建了也看不见），展开再接着建；
        间隔 150 ms，让点击/折叠有机会被处理。

        2026-11-26 二次卡死修复：折叠时不再排下一条。以前这里每 500 ms
        醒一次、一直醒到展开，折叠着放一晚上就是十几万次空转；
        现在整条链停掉，toggle_fold 展开时再启动。
        """
        self._pump_on = False
        self._pump_job = None
        if getattr(self, "_folded", False):
            return                          # 折叠：链停掉，展开时再续
        if time.time() < getattr(self, "_pump_pause_until", 0):
            self._start_pump(500)           # 刚展开：先别建，让窗口先响应
            return
        while self._queue:
            page = self._queue.pop(0)
            if page in self._built:
                continue
            try:
                self._ensure_page(page)
            except Exception as exc:      # noqa: BLE001  单页坏了别拖垮启动
                print("build page failed:", page, exc)
            self._start_pump(150)
            return

    #: 状态刷新间隔（毫秒）；全程序只允许一条定时链
    STATUS_EVERY = 4000

    def _start_status(self):
        r"""启动唯一的状态刷新链；已经在排队就什么都不做。"""
        if getattr(self, "_status_job", None) is not None:
            return
        self._safe_status()

    def _stop_status(self):
        r"""停掉状态链（折叠 / 关窗）；展开时 _start_status 再续上。"""
        job = getattr(self, "_status_job", None)
        self._status_job = None
        if job:
            try:
                self.after_cancel(job)
            except Exception:             # noqa: BLE001  已经跑过/已被销毁
                pass

    def _safe_status(self):
        r"""4 s 状态刷新：全控制台唯一的一条状态定时链。

        2026-11-26 卡死修复（重点）：refresh_status 以前结尾也会
        after(4000, self.refresh_status)。这里再调一次刷新，等于每 tick
        凭空多一条链：4 s 后两条、8 s 后三条……跑十分钟能堆出上百条，
        主线程永远走不出 refresh_status（Windows 事件日志里的 AppHangB1），
        窗口就从「有点卡」变成「未响应」。折叠只是让它更明显 —— 用户把窗口
        收起去干别的，回来时链已经堆满。

        现在：排程只在这里，永远一条；refresh_status 自己不再排程。
        折叠时整条链停掉（窗口都藏起来了，刷了看不见），展开立刻补一次。
        """
        self._status_job = None
        try:
            if not getattr(self, "_folded", False):
                self.refresh_status()
        except Exception:                 # noqa: BLE001  页面还没建完就先跳过
            pass
        if getattr(self, "_folded", False):
            return                        # 折叠：不排下一条，展开时 _start_status
        try:
            self._status_job = self.after(self.STATUS_EVERY, self._safe_status)
        except tk.TclError:
            self._status_job = None

    def on_group(self, name=None, persist=True):
        r"""一级页签（分组）切换：回到这一组上次停留的子页。CTkTabview 的 command 不传参数。"""
        if getattr(self, "_booting", False):
            return
        if not name:
            name = self.tabview.get()
        pages = dict(TAB_GROUPS).get(name) or ()
        if not pages:
            return
        self.show_sub(name, self._sub_memo.get(name) or pages[0], persist)

    def show_sub(self, group, page, persist=True):
        r"""切到某组的某一页：翻内容框、记位置、按页刷新数据。

        persist=False 用于启动恢复 / 程序内跳转（不写盘）。
        """
        pages = dict(TAB_GROUPS).get(group) or ()
        if page not in pages:
            page = pages[0] if pages else ""
        self._ensure_page(page)          # 懒加载：点到的页没建就先建
        show = self.page_show.get(group)
        if show is not None:
            show(page, notify=False)      # 只翻框，不再回调 on_change，避免递归
        self.cur_group, self.cur_page = group, page
        self._sub_memo[group] = page
        self.ui["tab"] = group
        self.ui["sub"] = page
        self.ui["sub_%s" % group] = page
        if persist and not getattr(self, "_booting", False):
            try:
                save_cfg(self.cfg)
            except OSError:
                pass
        self.refresh_page(page)

    def refresh_page(self, name):
        r"""进入某一页时按页刷新（原来 on_tab 里那段 if/elif）。"""
        try:
            self.save_autotest_ui()      # 离开车测页时把改过的参数带走（页没建完时跳过）
        except Exception:                # noqa: BLE001
            pass
        if name == "数据":
            self.refresh_data()
        elif name == "车测":
            self.refresh_at()
        elif name == "录制":
            self.rec_sync_from_wp()
            self.refresh_rec_ready()
        elif name == "开发者选项":
            self.pmark_refresh()         # 文件可能被编辑器 / 手改过，进来重读
        elif name == "地图总览":
            self.refresh_overview()
        elif name == "人机路点":
            if hasattr(self, "opt_pack"):
                cur = self.selected_pack()
                self.opt_pack.configure(values=self._pack_values())   # 编辑器新存的包也刷进来
                if cur and self.disp_of(cur):
                    self.opt_pack.set(self.disp_of(cur))
            self.refresh_wp_tab()

    def _restore_tab(self):
        r"""上次停在哪：先看这个身份自己的位置（切换身份时记下的），再看通用记录。"""
        pos = self.ui.get("pos_%s" % ROLE_DEV)
        groups = dict(TAB_GROUPS)
        if isinstance(pos, (list, tuple)) and len(pos) == 2:
            if pos[0] in groups and pos[1] in groups[pos[0]]:
                return pos[0], pos[1]
        old = str(self.ui.get("tab") or "")
        if old in TAB_OLD_MAP:
            return TAB_OLD_MAP[old], old
        groups = dict(TAB_GROUPS)
        if old in groups:
            page = str(self.ui.get("sub_%s" % old) or self.ui.get("sub") or "")
            if page not in groups[old]:
                page = groups[old][0]
            return old, page
        first_group, first_pages = TAB_GROUPS[0]
        return first_group, first_pages[0]

    # ---- 用户身份：两页平铺（没有分组条）----
    def on_flat_tab(self, name=None, persist=True):
        r"""用户身份切页。CTkTabview 的 command 不传参数，name 为空时自己读当前页。"""
        if getattr(self, "_booting", False):
            return
        if not name:
            name = self.tabview.get()
        self.show_flat(name, persist)

    def show_flat(self, page, persist=True):
        r"""用户身份：切到某一页、记位置、刷新数据。"""
        if page not in USER_PAGES:
            page = USER_PAGES[0]
        self._ensure_page(page)
        self.cur_group = ROLE_LABEL[ROLE_USER]
        self.cur_page = page
        self.ui["tab"] = self.cur_group
        self.ui["sub"] = page
        self.ui["sub_%s" % self.cur_group] = page
        if persist and not getattr(self, "_booting", False):
            try:
                save_cfg(self.cfg)
            except OSError:
                pass
        self.refresh_page(page)

    def _restore_user(self):
        r"""用户身份上次停在哪一页；以前存的是开发页名就落回「地图」。"""
        pos = self.ui.get("pos_%s" % ROLE_USER)
        if isinstance(pos, (list, tuple)) and len(pos) == 2 and pos[1] in USER_PAGES:
            return pos[1]
        page = str(self.ui.get("sub") or self.ui.get("tab") or "")
        return page if page in USER_PAGES else USER_PAGES[0]

    def switch_role(self):
        r"""用户 ↔ 开发者：写配置后重启控制台。

        页面是按身份建出来的（用户身份根本不建那 8 页），动态换页签会把控件状态全丢，
        重启最干净，也复用首次设置向导那套 _restart_after_setup()。
        """
        fixed = env_role()
        if fixed:
            messagebox.showinfo("切换身份",
                                "当前身份由环境变量 UCF_ROLE=%s 指定，控制台里改不了。\n"
                                "去掉这个环境变量（或改成 user / dev）再启动即可。" % fixed,
                                parent=self)
            return
        other = ROLE_DEV if self.role == ROLE_USER else ROLE_USER
        if not messagebox.askyesno(
                "切换身份",
                "切换为「%s」需要重启控制台（约 1 秒）。\n\n当前页会被记住，重启后回到对应身份。继续？"
                % ROLE_LABEL[other], parent=self):
            return
        # 把当前身份的位置记下来，切回来时还停在这一页
        self.ui["pos_%s" % self.role] = [self.cur_group, self.cur_page]
        self.ui["role"] = other
        try:
            save_cfg(self.cfg)
        except OSError:
            pass
        _restart_after_setup()

    # ---- 写盘 ----
    def persist(self, note="", live=False):
        self.cfg["enabled"] = bool(self.master_var.get())
        feats = self.cfg.setdefault("features", {})
        for k, v in self.vars.items():
            feats[k] = bool(v.get())
        if hasattr(self, "seg_mode"):
            self.cfg["pack"] = self.pack_dict()
        try:
            save_cfg(self.cfg)
        except OSError as exc:
            self.set_status("写不进 ucf_mod.json：%s" % exc)
            return
        msg = "已保存 " + (note or "")
        if live and game_running():
            # 可视化这几项可以边玩边切：写一条 cmd=vis，插件 0.5 s 内应用
            if self.send_vis_cmd():
                msg += " · 已实时下发（不用重进图）"
        elif game_running():
            msg += " · 游戏在运行，重启游戏才生效"
        self.set_status(msg)

    def send_vis_cmd(self):
        r"""把「可视化」页现在的勾选状态整批发给运行中的插件（cmd=vis）。

        整批发而不是只发改的那一个：插件也不需要记状态，收到什么就是什么。
        游戏没开就不写（配置已经存盘，下次启动按配置来）。"""
        extra = {}
        for key, field in LIVE_VIS_KEYS.items():
            var = self.vars.get(key)
            if var is not None:
                extra[field] = 1 if var.get() else 0
        if not extra:
            return False
        try:
            write_nav_cmd("vis", extra=extra)
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return False
        return True

    def on_toggle(self, key):
        self.persist(key, live=key in LIVE_VIS_KEYS)

    def on_master(self):
        self.persist("总开关")
        self.refresh_launch_strip()

    # ---- 窗口置顶 / 折叠成小条 ----------------------------------------
    def on_topmost(self):
        r"""窗口置顶：勾上就一直浮在游戏上面；状态记进 ucf_mod.json 的 ui 段。"""
        on = bool(self.topmost_var.get())
        self.ui["topmost"] = on
        self.attributes("-topmost", on)
        try:
            save_cfg(self.cfg)
        except OSError:
            pass

    def toggle_fold(self):
        r"""折叠：藏起介绍/页签/日志/底部按钮，窗口缩成只剩标题行的一条；
        再点「展开」按原尺寸、原位置回来。折叠条宽度按标题行实际内容收窄，不留空档。

        2026-11-26：折叠/展开前后 1 s 内暂停后台建页 —— 否则展开这一下正好撞上
        正在建的页（最多 1.7 s），看起来就是「展开后卡死」。
        """
        self._pump_pause_until = time.time() + 1.0
        if not self._folded:
            self._geom_saved = str(self.tk.call("wm", "geometry", self))
            self._folded = True
            # 2026-11-26 卡死修复：折叠后界面全看不见，别让后台链还醒着。
            # 两条链都停掉；展开时再启动（见下面 else 分支）。
            self._stop_status()
            self._stop_pump()
            self.intro.pack_forget()
            self.tabview.pack_forget()
            self.stat.pack_forget()
            self.strip.pack_forget()
            self.bar.pack_forget()
            self.minsize(1, 1)
            _size, x, y = self._geom_saved.split("+")
            w = self.head.winfo_reqwidth() + int(self._apply_window_scaling(44))
            h = self.head.winfo_reqheight() + int(self._apply_window_scaling(30))
            self.tk.call("wm", "geometry", self, "%dx%d+%s+%s" % (w, h, x, y))
            self.btn_fold.configure(text="展开")
            self._pump_generation = getattr(self, "_pump_generation", 0) + 1
        else:
            self._folded = False
            # 按原来的 pack 顺序装回去：介绍 → 底栏 → 日志 → 页签
            self.intro.pack(anchor="w", padx=20)
            self.bar.pack(side="bottom", fill="x", padx=14, pady=(0, 12))
            self.strip.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
            self.stat.pack(side="bottom", fill="x", padx=14, pady=(0, 8))
            self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 4))
            self.minsize(720, 620)
            self.tk.call("wm", "geometry", self, self._geom_saved)
            self.btn_fold.configure(text="折叠")
            # 展开后：当前页保证已经建好，再让后台接着建剩下的
            try:
                self._ensure_page(self.cur_page)
            except Exception:          # noqa: BLE001
                pass
            if getattr(self, "_queue", None):
                self._start_pump(400)
            # 状态链是折叠时停掉的：展开立刻补一次刷新，再照常每 4 s 一次
            self._start_status()

    def on_close(self):
        r"""关窗口 = 最后一次落盘：正停在哪个页签、车测输入框里没失焦的数字都不丢。"""
        # 2026-11-26：先把两条定时链摘掉，别让 destroy 之后的 after 回调再炸
        self._stop_status()
        self._stop_pump()
        rec_on = getattr(self, "rec_state", "") == "rec"
        tr_on = getattr(self, "tr_state", "") in ("starting", "running")
        if rec_on or tr_on:
            try:
                # 一条命令同时收掉 rec / trace：ucf_navcmd.txt 只保留最后一条命令，
                # 分开写两条会丢一条。
                write_nav_cmd("stopall")
            except OSError:
                pass
        if rec_on:
            self.set_status("录制已停止；原始轨迹留在 %s" % self.rec_file)
        if tr_on:
            self.set_status("轨迹采集已停止；日志留在 %s" % self.tr_file)
        self.save_autotest_ui()
        if getattr(self, "cur_group", ""):
            self.ui["tab"] = self.cur_group
            self.ui["sub"] = self.cur_page
            self.ui["sub_%s" % self.cur_group] = self.cur_page
        else:
            tab = self.tabview.get()
            if tab:
                self.ui["tab"] = tab
        try:
            save_cfg(self.cfg)
        except OSError:
            pass
        self.destroy()

    # ---- 状态 ----
    def set_status(self, text):
        self.dot.configure(text=text)

    def refresh_status(self):
        running = game_running()
        self.refresh_game_button(running)
        lines = tail_log(6)
        self.logbox.configure(state="normal")
        self.logbox.delete("1.0", "end")
        self.logbox.insert("end", "\n".join(lines) if lines else "（还没有日志）")
        self.logbox.configure(state="disabled")
        if not self.dot.cget("text"):
            self.set_status("配置：%s" % ("已读取" if os.path.isfile(CFG_PATH) else "未找到，用默认值"))
        if hasattr(self, "refresh_at_ready"):
            self.refresh_at_ready()      # 车测：总开关关着就别让「开跑」能点
        if hasattr(self, "wp_meta"):
            self.refresh_wp_status()
        self.refresh_launch_strip(running)
        # 2026-11-26 卡死修复：这里以前还有一行 after(4000, self.refresh_status)。
        # 它和 _safe_status 的定时链叠在一起，每次 tick 多一条，越跑越多，
        # 主线程被刷状态占满 → Windows 判无响应。排程只留 _safe_status 一处。

    def refresh_game_button(self, running=None):
        r"""底部「开始游戏」按钮：文案和颜色跟着版本走，别让用户猜。"""
        if not hasattr(self, "btn_game"):
            return
        if running is None:
            running = game_running()
        # 2026-11-22 用户要求：按钮上要能看出「这次从哪一份游戏启动」——多副本共存时不会点错
        tag = game_tag(GAME_EXE)
        suffix = ("  ［%s］" % tag) if tag else ""
        if running:
            self.btn_game.configure(text="游戏运行中" + suffix, state="disabled",
                                    fg_color="#3a3f47", hover_color="#49505a")
            return
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        if not bool(self.master_var.get()):
            # 总开关关 = 插件加载但待机（plugin.c: loaded but idle）
            self.btn_game.configure(text="开始游戏 · 插件已关（原版）" + suffix, state="normal",
                                    fg_color="#3a3f47", hover_color="#49505a")
        elif pk.get("on") and pk.get("name"):
            label = self.folder_label(pk["name"]) if hasattr(self, "folder_label") else pk["name"]
            self.btn_game.configure(text="开始游戏 · 编辑中 %s" % label + suffix,
                                    state="normal",
                                    fg_color="#a86a12", hover_color="#bf7c17")
        else:
            st = final_stats()
            if not st.get("n"):
                self.btn_game.configure(text="开始游戏 · 成品（还没有发布）" + suffix, state="disabled",
                                        fg_color="#3a3f47", hover_color="#49505a")
            else:
                self.btn_game.configure(text="开始游戏 · 成品（%d 张图）" % st["n"] + suffix,
                                        state="normal",
                                        fg_color="#2f6fdb", hover_color="#255bb4")

    # ---- 启动条件条 / 测试包预检（2026-11-19 用户要求）---------------
    # 版本选择原本只活在「人机路点」① 卡里，底部按钮又不带状态；
    # 这里把「这次启动加载什么」常驻到按钮上方，测试包再补一道预检。
    def launch_strip_info(self):
        r"""当前启动条件的文案；与 game_env() 同一套判断：总开关 → 测试包 → 正式版。"""
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        if not bool(self.master_var.get()):
            return {"mode": "off", "badge": "插件已关",
                    "title": "本次启动 = 原版（插件待机）",
                    "sub": "总开关关闭：插件加载但不动作，不读 nav、不出 F2 菜单",
                    "go": "去打开"}
        if not (pk.get("on") and pk.get("name")):
            st = final_stats()
            if self.role == ROLE_USER:      # 用户身份不提示「切到编辑中」——那是开发页
                sub = "只读：这些是发布好的数据，游戏内改动不落盘。"
            else:
                sub = "只读：游戏内改动不落盘；要改就切到「编辑中（可写）」"
            return {"mode": "final", "badge": "成品",
                    "title": ("本次启动加载 成品（%d 张图，只读）" % st["n"]) if st.get("n")
                             else "本次启动加载 成品（还没有发布 = 全原生）",
                    "sub": sub,
                    "go": "去人机路点改"}
        name = pk["name"]
        short = self.folder_label(name) if hasattr(self, "folder_label") else name
        man = pack_manifest(name)
        summ = pack_summary(name, pack_target_fp(name))
        ops = summ["nadd"] + summ["ndel"] + summ["eadd"] + summ["edel"]
        grow = bool(man.get("grow") or man.get("blank") or summ["grow"])
        keepn = bool(man.get("keep") or summ["keep"])
        kind = "原版 + 新增" if keepn else ("空白地图" if grow else "增量")
        label = str(man.get("label") or pk.get("label") or pk.get("map") or short)
        title = "%s · %s · 只对这张图生效" % (short, kind)
        if keepn:
            sub = "草稿内 %d 处改动；原生点原样保留，原版路线照常走，只按 AddNode 追加新点" % ops
        elif grow and ops == 0:
            sub = "草稿内 0 处改动：原生点全禁用又没新建节点，人机没有可走路点"
        elif grow:
            sub = "草稿内 %d 处改动；原生点全禁用，节点按 AddNode 新建（不受原生点数限制）" % ops
        else:
            sub = "草稿内 %d 处改动，套在原生点上执行" % ops
        return {"mode": "test", "badge": "编辑中", "title": title, "sub": sub,
                "go": "去人机路点改"}

    def refresh_launch_strip(self, running=None):
        r"""把启动条件画到按钮上方；运行中显示启动瞬间的快照，改选只影响下次。"""
        if not hasattr(self, "strip"):
            return
        if running is None:
            running = game_running()
        if running:
            if getattr(self, "_strip_run", None) is None:
                # 外部双击 exe 起的进程：没有 mod，更谈不上版本；单独说清楚
                info = {"mode": "off", "badge": "外部启动",
                        "title": "游戏在运行，但不是从本窗口启动的",
                        "sub": "直接双击 UnityCrossFire.exe 是原版（无 mod）；要加载成品请关掉游戏再点底部按钮",
                        "go": "去人机路点"}
            else:
                info = dict(self._strip_run)
                info["badge"] = "运行中 · " + info["badge"]
                info["sub"] += " · 改启动档只影响下次启动"
        else:
            self._strip_run = None
            info = self.launch_strip_info()
        # mode -> (外框, 底色, 徽标底, 徽标字)
        style = {
            "off": ("#5a3434", "#2a1a1a", "#301c1c", "#ff9d9d"),
            "test": ("#7a5a17", "#2c2310", "#3a2c0d", "#f7cd74"),
            "final": ("#2f4f8a", "#1a2433", "#16233a", "#9cc3ff"),
        }[info["mode"]]
        self.strip.configure(border_color=style[0], fg_color=style[1])
        self.strip_badge.configure(text=info["badge"], fg_color=style[2],
                                   text_color=style[3],
                                   width=max(78, 15 * len(info["badge"]) + 14))
        self.strip_title.configure(text=info["title"],
                                   text_color="#f7cd74" if info["mode"] == "test" else "#f0f0f0")
        self.strip_sub.configure(text=info["sub"])
        self.strip_go.configure(text=info["go"])
        # 2026-11-24：用户身份平时没有这个按钮（跳转是开发页），只有「插件关着」时露出一个
        # 「去打开」——否则用户身份的启动条是死路：按钮灰、没有任何恢复入口。
        if self.role == ROLE_USER:
            if info["mode"] == "off":
                if not self.strip_go.winfo_manager():
                    self.strip_go.pack(side="right", padx=(8, 10), pady=8)
            elif self.strip_go.winfo_manager():
                self.strip_go.pack_forget()
        if hasattr(self, "strip_path"):
            exists = os.path.isfile(GAME_EXE)
            text = "启动位置：" + compact_path(GAME_EXE, 96)
            color = "#7f8792" if exists else "#ff9d9d"
            # 2026-11-22 用户踩过：部署页选了 A，这里启动的还是 B，眼睛看不出来。
            # 只要"部署页选的位置"和"实际启动的位置"不一致，就用红字点破。
            dt = getattr(self, "deploy_tab", None)
            picked = getattr(dt, "game", None) if dt is not None else None
            if picked and os.path.dirname(GAME_EXE).lower() != str(picked).lower():
                text = "⚠ 部署页选的是 %s，但这次启动的仍是 %s" % (
                    game_tag(os.path.join(str(picked), "UnityCrossFire.exe")),
                    game_tag(GAME_EXE))
                color = "#ff9d9d"
            self.strip_path.configure(text=text, text_color=color)
        self.refresh_game_button(running)

    def on_strip_go(self):
        r"""启动条右侧按钮：插件关着就先打开；否则跳到人机路点 ① 卡。"""
        if not bool(self.master_var.get()):      # 用户身份也能从这里打开（开关不显示）
            self.master_var.set(True)
            self.on_master()
            return
        if self.role == ROLE_USER:
            return
        self.jump_to_pick()

    def jump_to_pick(self):
        r"""跳到「路点数据 → 人机路点」→「编辑中」页 →「本图草稿」，并闪一下边框。"""
        if self.role == ROLE_USER:      # 用户身份没有这一页 / 这个按钮
            return
        try:
            self.tabview.set("路点数据")
            self.show_sub("路点数据", "人机路点", persist=False)
        except Exception:
            pass
        try:
            if not self.seg_mode.get().startswith("编辑中"):
                self.seg_mode.set("编辑中（可写）")
                self.on_pack_change()
            self.show_page("编辑中")
            if hasattr(self, "page_edit_tabs"):
                self.page_edit_tabs("本图草稿")
        except Exception:                # noqa: BLE001  页面还没建好就算了
            pass
        body = getattr(self, "wp_body", None)
        if body is not None:
            try:
                body._parent_canvas.yview_moveto(0.0)   # noqa: SLF001  CTk 内部画布
            except Exception:
                pass
        card = getattr(self, "card_pick", None)
        if card is None:
            return
        try:
            card.configure(border_width=2, border_color="#f5b942")
        except Exception:
            return

        def clear():
            try:
                if card.winfo_exists():
                    card.configure(border_width=0, border_color="#383838")
            except Exception:
                pass

        self.after(1600, clear)

    def preflight_start(self):
        r"""测试包模式的启动预检；返回 True = 继续启动。

        只拦「总开关开 + 测试包选中」的启动；正式版和插件待机直接放行。
        顺带把空包风险提前说出来：空白地图 + 包内 0 处改动 = 人机没有可走路点。
        """
        pk = self.pack_dict()
        name = pk.get("name") or ""
        man = pack_manifest(name)
        summ = pack_summary(name, pack_target_fp(name))
        ops = summ["nadd"] + summ["ndel"] + summ["eadd"] + summ["edel"]
        grow = bool(man.get("grow") or man.get("blank") or summ["grow"])
        keepn = bool(man.get("keep") or summ["keep"])
        label = str(man.get("label") or pk.get("label") or pk.get("map") or "")
        level = str(man.get("level") or pk.get("map") or "")
        where = ("%s（%s）" % (label, level)) if (label and level) else (label or level or "（未知）")
        scope = "只对这张图生效"
        if keepn:
            alert = ("原版基础 + 新增（keep）：原生点一个都不动，原版路线照常能走；"
                     "草稿内 %d 处改动只按 AddNode 追加新点，数量不限。" % ops)
        elif grow and ops == 0:
            alert = ("注意：空白地图（grow）+ 草稿内 0 处改动。进图后原生点全部禁用、"
                     "又不会新建节点，人机没有可走路点，不会移动。")
        elif grow:
            alert = ("空白地图（grow）：原生点全部禁用，节点按 AddNode 新建，"
                     "草稿内 %d 处改动不受原生点数限制。" % ops)
        else:
            alert = "增量改动：草稿内 %d 处改动，套在原生点上执行。" % ops

        top = ctk.CTkToplevel(self)
        top.title("启动预检 · 编辑中")
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)   # 控制台置顶时别把预检藏到后面

        def grab():
            try:
                if top.winfo_exists():
                    top.grab_set()
            except tk.TclError:
                pass

        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, grab)   # CTkToplevel 还没 viewable 时等它映射出来
        top.bind("<Escape>", lambda _e: top.destroy())

        ctk.CTkLabel(top, text="启动预检 · 测试包模式",
                     font=("Microsoft YaHei UI", 17, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 0))
        ctk.CTkLabel(top, text="成品 / 原版不会弹这一步；确认后才会带 UCF_PACK / UCF_FP 启动游戏。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=470).pack(fill="x", padx=18, pady=(4, 4))
        # 2026-11-22：预检也把"这次到底启动哪个 exe"写出来，多副本时不会点错
        ctk.CTkLabel(top, text="将启动：" + GAME_EXE, font=("Consolas", 11),
                     text_color="#7f8792", anchor="w", justify="left",
                     wraplength=470).pack(fill="x", padx=18, pady=(0, 8))

        grid = ctk.CTkFrame(top, fg_color="transparent")
        grid.pack(fill="x", padx=14)
        cells = [("数据版本", "② 编辑中（packs）"),
                 ("本图草稿", self.folder_label(name) if hasattr(self, "folder_label") else name),
                 ("生效地图", where), ("生效范围", scope)]
        for i, (k, v) in enumerate(cells):
            cell = ctk.CTkFrame(grid, corner_radius=7, fg_color="#262626",
                                border_width=1, border_color="#383838")
            cell.grid(row=i // 2, column=i % 2, sticky="nsew", padx=4, pady=4)
            ctk.CTkLabel(cell, text=k, font=FONT_S, text_color="#9aa0a6",
                         anchor="w").pack(fill="x", padx=10, pady=(6, 0))
            ctk.CTkLabel(cell, text=v, font=("Microsoft YaHei UI", 13, "bold"),
                         anchor="w", justify="left", wraplength=210).pack(
                fill="x", padx=10, pady=(0, 6))
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)

        warn = ctk.CTkFrame(top, corner_radius=7, fg_color="#241511",
                            border_width=1, border_color="#6b3d2c")
        warn.pack(fill="x", padx=18, pady=(6, 0))
        ctk.CTkLabel(warn, text=alert, font=FONT_S, text_color="#ffb59d",
                     anchor="w", justify="left", wraplength=440).pack(
            fill="x", padx=10, pady=8)

        mute_var = tk.BooleanVar(value=self._mute_preflight)
        ctk.CTkCheckBox(top, text="本次控制台会话不再提示（启动条仍会一直显示）",
                        variable=mute_var, font=FONT_S,
                        checkbox_width=18, checkbox_height=18).pack(
            anchor="w", padx=20, pady=(10, 0))

        result = {"go": False}

        def go():
            result["go"] = True
            if mute_var.get():
                self._mute_preflight = True
            top.destroy()

        btns = ctk.CTkFrame(top, fg_color="transparent")
        btns.pack(fill="x", padx=18, pady=(12, 16))
        ctk.CTkButton(btns, text="确认启动", width=104, height=34, font=FONT,
                      fg_color="#a86a12", hover_color="#bf7c17",
                      text_color="#fff2d6", command=go).pack(side="right")
        ctk.CTkButton(btns, text="先去人机路点", width=118, height=34, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: (top.destroy(), self.jump_to_pick())).pack(
            side="right", padx=(0, 8))
        ctk.CTkButton(btns, text="取消", width=76, height=34, font=FONT_S,
                      fg_color="transparent", border_width=1, border_color="#4a4a4a",
                      hover_color="#2e2e2e", command=top.destroy).pack(
            side="right", padx=(0, 8))

        top.update_idletasks()
        w = max(520, top.winfo_reqwidth())
        h = top.winfo_reqheight()
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        top.geometry("%dx%d+%d+%d" % (w, h, max(x, 0), max(y, 0)))
        self.wait_window(top)
        return result["go"]

    # ---- 动作 ----
    def game_env(self):
        r"""启动游戏的环境变量 + 一句人话说明（「开始游戏」和「车测」共用）。

        UCF_MOD=1 是通行证。三档启动的路径也在这里定（数据全在 ②，③ 只当运行环境）：
          UCF_EXPORT_DIR     -> data\maps\_inbox（可走面 navmesh_*.bin 写这里）
          UCF_PACK_DIR       -> data\maps（草稿根；<图>\<指纹>.txt）
          成品：UCF_PACK_DIR=data\maps + UCF_NAV_SEARCH=1 + UCF_NAV_SUB=final
                —— 插件按当前图指纹找 <图>\final\<指纹>.txt，markers 也跟到 <图>\markers.txt
          编辑中：UCF_PACK=<图>（可写，游戏内存回草稿）
          原版：总开关关，插件待机
        """
        env = dict(os.environ)
        env["UCF_MOD"] = "1"
        # 2026-11-25：开发直读 —— 加载器直接从 run\build 取最新编译的插件；
        # 配置/命令也在工程端 run\runtime\，游戏目录不再需要 ucf_mod\。
        dll = BUILD_DLL if os.path.isfile(BUILD_DLL) else PAYLOAD_DLL
        if os.path.isfile(dll):
            env["UCF_MOD_DLL"] = dll
        env["UCF_MOD_DIR"] = RUNTIME
        try:
            os.makedirs(RUNTIME, exist_ok=True)
        except OSError:
            pass
        # 老配置只在第一次直读时搬一次：优先用 run\runtime 里的，缺了才从旧部署端复制。
        legacy_cfg = os.path.join(DEPLOY, "ucf_mod.json")
        if not os.path.isfile(CFG_PATH) and os.path.isfile(legacy_cfg):
            try:
                shutil.copy2(legacy_cfg, CFG_PATH)
            except OSError:
                pass
        env["UCF_EXPORT_DIR"] = TEST_VIS
        env["UCF_PACK_DIR"] = PACKS
        # 2026-11-23：日志写到工程端 log\，游戏目录不再生成；插件建不出目录才落回游戏端
        env["UCF_LOG_DIR"] = LOG_DIR
        # 2026-11-24：编辑标记（蹲守点/守卫点/守卫区/tag）也放工程端，按地图分子文件夹
        env["UCF_MARKERS_DIR"] = MARKERS
        for _d in (LOG_DIR, MARKERS):
            try:
                os.makedirs(_d, exist_ok=True)
            except OSError:
                pass
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        enabled = bool(self.master_var.get()) if hasattr(self, "master_var") else True
        note = "mod 已启用"
        if not enabled:
            # 总开关关 = 插件加载但待机（plugin.c）；状态行别再写「mod + 测试包」
            note = "插件总开关关闭：插件待机（不读 nav、不出菜单）"
        elif pk.get("on") and pk.get("name"):
            env["UCF_PACK"] = pk["name"]           # 只有一层：packs\\<地图文件夹>
            env.pop("UCF_NAV_READONLY", None)      # 草稿允许游戏内保存
            label = self.folder_label(pk["name"]) if hasattr(self, "folder_label") else pk["name"]
            note = "mod + 编辑中 %s" % label
            if pk.get("fp"):
                env["UCF_FP"] = pk["fp"]           # 永远只套这一张图，别的图跳过
                env["UCF_FPLABEL"] = pk.get("label") or pk["map"]
                note += "（只对 %s）" % (pk.get("label") or pk["map"])
        else:
            # 成品：一图一夹，插件按当前图指纹读 <图>\\final\\<指纹>.txt。
            # 和编辑中完全同一套加载逻辑（grow/keep/0 点图都照常），只是文件带只读属性。
            st = final_stats()
            d = prepare_final_root() if st.get("n") else ""
            if d:
                # 一图一夹（2026-11-27）：成品在各图自己的 final\ 里，插件按当前图指纹去搜
                # （UCF_NAV_SEARCH=1 + UCF_NAV_SUB=final），所以不设 UCF_PACK —— 一次启动照样能玩全部图。
                env["UCF_PACK_DIR"] = P.MAPS
                env["UCF_NAV_SEARCH"] = "1"
                env["UCF_NAV_SUB"] = P.FINAL_SUB
                env["UCF_NAV_READONLY"] = "1"
                for k in ("UCF_PACK", "UCF_FP", "UCF_FPLABEL", "UCF_NAV_DIR"):
                    env.pop(k, None)
                note = "mod + 成品（%d 张图，只读）" % st["n"]
            else:
                # 成品里还没有任何图：不读任何路线数据（等于原版）
                for k in ("UCF_PACK", "UCF_FP", "UCF_FPLABEL", "UCF_NAV_DIR"):
                    env.pop(k, None)
                note = "mod + 成品（还没有发布，等于原版）"
        return env, note

    def launch_game(self):
        if not os.path.isfile(GAME_EXE):
            self.set_status("找不到 %s" % GAME_EXE)
            return
        if (hasattr(self, "master_var") and self.master_var.get()
                and not (os.path.isfile(BUILD_DLL) or os.path.isfile(PAYLOAD_DLL))):
            self.set_status("插件未编译：先运行 app\\tools\\build.ps1（或先更新 run\\payload）")
            return
        # 2026-11-19：测试包模式先过一道预检（正式版 / 插件待机直接放行）
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        if (bool(self.master_var.get()) and pk.get("on") and pk.get("name")
                and not self._mute_preflight):
            if not self.preflight_start():
                self.set_status("已取消启动（草稿 %s）" % pk.get("name"))
                return
        # 通行证：只有这里启动才会带上 UCF_MOD=1，插件据此决定是否工作
        env, note = self.game_env()
        try:
            subprocess.Popen([GAME_EXE], cwd=os.path.dirname(GAME_EXE), env=env)
            self._strip_run = self.launch_strip_info()   # 运行中显示启动瞬间的快照
            self.set_status("游戏已启动（%s · %s）" % (note, game_tag(GAME_EXE)))
        except OSError as exc:
            self.set_status("启动失败：%s" % exc)
        self.after(1500, self.refresh_status)

    def open_workbench(self):
        r"""路点工作台只读：直接起 navserver（新控制台窗口看日志，关掉即停止）。"""
        if not os.path.isfile(NAVSERVER):
            self.set_status("找不到 navserver.py")
            return
        env = dict(os.environ)
        env["UCF_PROFILE"] = "dev"
        try:
            subprocess.Popen([_python(), "-u", NAVSERVER], cwd=HERE, env=env,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
            self.set_status("已打开路点工作台（只读查看）")
        except OSError as exc:
            self.set_status("打不开路点工作台：%s" % exc)


def _restart_after_setup():
    r"""向导会把游戏位置写进用户配置，但 ucf_paths 的 DEPLOY 是 import 时算好的常量，
    本进程里已经改不动了 —— 直接重启自己最省事，也最不容易踩到 40 多个使用点。"""
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception:
        try:
            subprocess.Popen([sys.executable] + sys.argv, cwd=HERE)
        except Exception:
            pass
        sys.exit(0)


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    # 2026-11-22：不再一上来就 return 1。游戏位置没配好（或配的路径已经没了）先走首次设置向导：
    # 选 UnityCrossFire.exe → 六道闸门 → 一键部署 → 写 %LOCALAPPDATA%\UCFMod\deploy.json。
    if not os.path.isfile(GAME_EXE):
        try:
            import first_run
        except Exception as exc:
            print("缺少 first_run.py，无法进入首次设置：%s" % exc)
            return 1
        if not first_run.ensure_ready(GAME_EXE, DEPLOY):
            print("没有选择游戏位置，退出。")
            return 1
        _restart_after_setup()
        return 0
    # 2026-11-24 用户要求：别人拿到自己选身份。UCF_ROLE 环境变量 > 配置 ui.role > 首次弹窗。
    role = env_role() or role_from_cfg()
    if not role:
        role = ask_role()
        try:
            save_role(role)
        except OSError:
            pass
    App(role=role).mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
