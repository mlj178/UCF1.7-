#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「地图总览」页：一张图一行，矩阵 / 卡片 / 看板三种视图共用同一份数据。

只读页：本页不发布、不建草稿、不写数据；按钮只做刷新、打开目录、跳回「人机路点」。
"""
import os
import time
import tkinter as tk

import customtkinter as ctk

from ui.consts import FONT, FONT_S
from ui.env import DEV, PACKS
from ui.overview import STATUS_LABEL, collect_overview
from ui.util import _cut, compact_path


def _num(n):
    try:
        return "{:,}".format(int(n or 0))
    except (TypeError, ValueError):
        return str(n or 0)


VIEWS = ("矩阵", "卡片", "看板")

STATUS_STYLE = {
    "drafting": ("#22b8cf", "#162b2e"),
    "sync": ("#40c057", "#1e2c22"),
    "publish": ("#f0a020", "#2c2418"),
    "finalonly": ("#4c8dff", "#1c2635"),
    "idle": ("#9aa0a6", "#272a2e"),
    "nograph": ("#9775fa", "#241f33"),
}

DEPLOY_STYLE = {
    "ok": "#40c057",
    "warn": "#f0a020",
    "bad": "#e03131",
    "none": "#737b85",
}

GAME_STYLE = {
    "ok": "#75db8a",
    "warn": "#f0b95d",
    "edit": "#82aef0",
    "native": "#cfd6de",
    "nograph": "#c3a6ff",
}


class OverviewTab:
    def build_overview_tab(self, tab):
        self.ov_filter = "all"
        self.ov_q = ""
        self.ov_expanded = ""
        self.ov_data = None
        self.ov_last = ""
        self._ov_search_job = None
        view = str(self.ui.get("overview_view") or "矩阵")
        self.ov_view_name = view if view in VIEWS else "矩阵"

        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        self.ov_body = body

        # ---- 标题（压成一行：表格第一屏能看到行）----
        head = ctk.CTkFrame(body, fg_color="transparent")
        head.pack(fill="x", padx=8, pady=(4, 0))
        left = ctk.CTkFrame(head, fg_color="transparent")
        left.pack(side="left")
        ctk.CTkLabel(left, text="地图总览", font=("Microsoft YaHei UI", 15, "bold"),
                     anchor="w", height=24).pack(side="left")
        self.ov_last_lbl = ctk.CTkLabel(left, text="", font=("Consolas", 9),
                                        text_color="#6f7883", anchor="w", height=14)
        self.ov_last_lbl.pack(side="left", padx=(8, 0))
        self.ov_sum_lbl = ctk.CTkLabel(left, text="", font=("Microsoft YaHei UI", 9),
                                       text_color="#8f98a2", anchor="w", height=14)
        self.ov_sum_lbl.pack(side="left", padx=(10, 0))
        btns = ctk.CTkFrame(head, fg_color="transparent")
        btns.pack(side="right")
        ctk.CTkLabel(btns, text="视图", font=("Microsoft YaHei UI", 9),
                     text_color="#8f98a2").pack(side="left")
        self.ov_view_seg = ctk.CTkSegmentedButton(
            btns, values=list(VIEWS), width=190, height=26, font=("Microsoft YaHei UI", 11),
            selected_color="#2f6fdb", selected_hover_color="#255bb4",
            unselected_color="#2a2f36", unselected_hover_color="#343a42",
            command=self.ov_on_view)
        self.ov_view_seg.set(self.ov_view_name)
        self.ov_view_seg.pack(side="left", padx=(4, 7))
        ctk.CTkButton(btns, text="刷新", width=54, height=26, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.refresh_overview).pack(side="left", padx=(0, 4))
        ctk.CTkButton(btns, text="数据目录", width=76, height=26, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.open_folder(DEV)).pack(side="left")

        # ---- 三块全局状态（紧凑，一行）----
        strip = ctk.CTkFrame(body, fg_color="transparent")
        strip.pack(fill="x", padx=8, pady=(5, 0))
        for c in range(3):
            strip.grid_columnconfigure(c, weight=1, uniform="ovglobal")
        self.ov_deploy_dot, self.ov_deploy_main, self.ov_deploy_sub = self._ov_gcard(
            strip, 0, "插件部署")
        self.ov_start_main, self.ov_start_sub = self._ov_gcard2(
            strip, 1, "当前启动档")
        self.ov_data_main, self.ov_data_sub = self._ov_gcard2(
            strip, 2, "数据")

        # ---- 筛选 / 搜索 ----
        fbar = ctk.CTkFrame(body, fg_color="transparent")
        fbar.pack(fill="x", padx=8, pady=(6, 4))
        self.ov_chips = {}
        for key, text in (("all", "全部"), ("drafting", "编辑中"), ("publish", "待发布"),
                          ("sync", "已同步"), ("finalonly", "只有成品"),
                          ("idle", "未开始"), ("nograph", "无点图")):
            b = ctk.CTkButton(fbar, text=text, width=74, height=26, corner_radius=13,
                              font=FONT_S, fg_color="#23272d", hover_color="#2f353d",
                              border_width=1, border_color="#343a44",
                              text_color="#9aa0a6",
                              command=lambda k=key: self.ov_set_filter(k))
            b.pack(side="left", padx=(0, 5))
            self.ov_chips[key] = b
        self.ov_search = ctk.CTkEntry(fbar, width=150, height=27,
                                      font=FONT_S, placeholder_text="搜索地图 / level")
        self.ov_search.pack(side="right")
        self.ov_search.bind("<KeyRelease>", lambda _e: self.ov_on_search())

        # ---- 空数据提示（有草稿/成品时隐藏；不挡地图列表）----
        self.ov_empty = ctk.CTkFrame(body, corner_radius=8, fg_color="#2b2418",
                                     border_width=1, border_color="#554329")
        self.ov_empty_lbl = ctk.CTkLabel(
            self.ov_empty,
            text="还没有草稿，也还没有成品；11 张原生底图还在。",
            font=FONT_S, text_color="#e7c584", anchor="w", justify="left",
            wraplength=520)
        self.ov_empty_lbl.pack(side="left", padx=10, pady=7)
        ctk.CTkButton(self.ov_empty, text="去人机路点选图", width=110, height=24,
                      font=FONT_S, fg_color="#2f6fdb", hover_color="#255bb4",
                      command=self.ov_goto_first).pack(side="right", padx=8, pady=6)

        self.ov_holder = ctk.CTkFrame(body, fg_color="transparent")
        self.ov_holder.pack(fill="x", padx=8)

        # ---- 图例 ----
        foot = ctk.CTkFrame(body, fg_color="transparent")
        foot.pack(fill="x", padx=10, pady=(7, 12))
        leg = ctk.CTkFrame(foot, fg_color="transparent")
        leg.pack(fill="x")
        for key in ("drafting", "publish", "sync", "finalonly", "idle", "nograph"):
            ctk.CTkLabel(leg, text="●", font=("Microsoft YaHei UI", 10),
                         text_color=STATUS_STYLE[key][0]).pack(side="left")
            ctk.CTkLabel(leg, text=STATUS_LABEL[key], font=("Microsoft YaHei UI", 9),
                         text_color="#7d8792").pack(side="left", padx=(2, 10))
        ctk.CTkLabel(
            foot,
            text="备份① = 原生底图 + 发布快照（每图最多 5 份）；部署 / 游戏加载按当前启动档算，"
                 "不是把地图复制进游戏目录。",
            font=("Microsoft YaHei UI", 9), text_color="#646d78", anchor="w",
            justify="left", wraplength=760).pack(fill="x", pady=(4, 0))

        self.after(120, self.refresh_overview)

    # ---- 小部件 ----
    def _ov_gcard(self, parent, col, label):
        card = ctk.CTkFrame(parent, corner_radius=8, fg_color="#232323",
                            border_width=1, border_color="#33383f")
        card.grid(row=0, column=col, sticky="nsew", padx=(0, 6))
        ctk.CTkLabel(card, text=label, font=("Microsoft YaHei UI", 8), height=12,
                     text_color="#727b86", anchor="w").pack(fill="x", padx=8, pady=(3, 0))
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=8)
        dot = ctk.CTkLabel(row, text="●", width=10, height=14,
                           font=("Microsoft YaHei UI", 9), text_color="#737b85")
        dot.pack(side="left")
        main = ctk.CTkLabel(row, text="—", font=("Microsoft YaHei UI", 11, "bold"),
                            anchor="w", height=17)
        main.pack(side="left", padx=(3, 0))
        sub = ctk.CTkLabel(card, text="", font=("Microsoft YaHei UI", 8), height=13,
                           text_color="#7d858f", anchor="w", justify="left",
                           wraplength=230)
        sub.pack(fill="x", padx=8, pady=(0, 3))
        return dot, main, sub

    def _ov_gcard2(self, parent, col, label):
        card = ctk.CTkFrame(parent, corner_radius=8, fg_color="#232323",
                            border_width=1, border_color="#33383f")
        card.grid(row=0, column=col, sticky="nsew", padx=(0, 6))
        ctk.CTkLabel(card, text=label, font=("Microsoft YaHei UI", 8), height=12,
                     text_color="#727b86", anchor="w").pack(fill="x", padx=8, pady=(3, 0))
        main = ctk.CTkLabel(card, text="—", font=("Microsoft YaHei UI", 11, "bold"),
                            anchor="w", height=17)
        main.pack(fill="x", padx=8)
        sub = ctk.CTkLabel(card, text="", font=("Microsoft YaHei UI", 8), height=13,
                           text_color="#7d858f", anchor="w", justify="left",
                           wraplength=230)
        sub.pack(fill="x", padx=8, pady=(0, 3))
        return main, sub


    # ---- 刷新 / 状态 ----
    def _ov_mode(self):
        on = bool(self.pack_on.get()) if hasattr(self, "pack_on") else False
        lv = ""
        if hasattr(self, "opt_map"):
            try:
                lv = self.current_map()[0]
            except Exception:                 # noqa: BLE001
                lv = ""
        return ("edit" if on else "final"), lv

    def refresh_overview(self):
        if not hasattr(self, "ov_holder"):
            return
        mode, lv = self._ov_mode()
        try:
            data = collect_overview(mode, lv)
        except Exception as exc:              # noqa: BLE001
            self.ov_data = None
            for w in self.ov_holder.winfo_children():
                w.destroy()
            ctk.CTkLabel(self.ov_holder, text="总览读不了：%s" % exc,
                         font=FONT_S, text_color="#e03131", anchor="w",
                         wraplength=700).pack(fill="x", padx=8, pady=18)
            try:
                self.set_status("地图总览读不了：%s" % exc)
            except Exception:                 # noqa: BLE001
                pass
            return
        self.ov_data = data
        self.ov_last = time.strftime("%H:%M:%S")
        self.ov_last_lbl.configure(text="上次刷新 %s · 11 张图" % self.ov_last)

        dep = data["deployment"]
        self.ov_deploy_dot.configure(text_color=DEPLOY_STYLE.get(dep["state"], "#737b85"))
        self.ov_deploy_main.configure(text=dep["text"])
        self.ov_deploy_sub.configure(text=dep["sub"])

        if mode == "edit":
            name = data["current_label"] or "当前地图"
            self.ov_start_main.configure(text="编辑中（可写）")
            if data["current_level"]:
                has_draft = any(r["level"] == data["current_level"] and r.get("draft")
                                for r in data["rows"])
                self.ov_start_sub.configure(
                    text="只加载「%s」的草稿%s" % (name, "" if has_draft else "（没有草稿，实际原生）"))
            else:
                self.ov_start_sub.configure(text="还没选图；选图后只加载那一张的草稿")
        else:
            self.ov_start_main.configure(text="成品（只读）")
            self.ov_start_sub.configure(
                text="%d 张图用成品，%d 张原生" % (
                    data["final_count"], max(0, len(data["rows"]) - data["final_count"])))
        self.ov_data_main.configure(
            text="11 张图 · 草稿 %d · 成品 %d" % (data["draft_count"], data["final_count"]))
        if data["latest_publish"]:
            self.ov_data_sub.configure(
                text="快照 %d 份 · 最近发布 %s" % (
                    data["snapshot_count"], data["latest_publish"]))
        else:
            self.ov_data_sub.configure(text="快照 %d 份 · 还没有发布" % data["snapshot_count"])
        self.ov_sum_lbl.configure(
            text="编辑中 %d · 待发布 %d · 无点图 %d" % (
                data["counts"].get("drafting", 0), data["counts"].get("publish", 0),
                data["counts"].get("nograph", 0)))

        self._ov_update_chips()
        empty = data["draft_count"] == 0 and data["final_count"] == 0
        if empty:
            self.ov_empty_lbl.configure(
                text="还没有草稿，也还没有成品；11 张原生底图还在。先选一张有路点图的图开始编辑。")
            self.ov_empty.pack(fill="x", padx=8, pady=(0, 6), before=self.ov_holder)
        else:
            self.ov_empty.pack_forget()
        self._ov_render()

    def _ov_update_chips(self):
        if not self.ov_data or not hasattr(self, "ov_chips"):
            return
        n_all = len(self.ov_data["rows"])
        names = {"all": "全部", "drafting": "编辑中", "publish": "待发布",
                 "sync": "已同步", "finalonly": "只有成品", "idle": "未开始",
                 "nograph": "无点图"}
        for key, btn in self.ov_chips.items():
            n = n_all if key == "all" else self.ov_data["counts"].get(key, 0)
            btn.configure(text="%s %d" % (names[key], n))
            self._ov_chip_style(btn, key == self.ov_filter)

    def _ov_chip_style(self, btn, on):
        if on:
            btn.configure(fg_color="#26364f", border_color="#3c6392",
                          text_color="#dce9ff", hover_color="#2d4263")
        else:
            btn.configure(fg_color="#23272d", border_color="#343a44",
                          text_color="#9aa0a6", hover_color="#2f353d")

    # ---- 视图 / 筛选 ----
    def ov_on_view(self, value):
        if value not in VIEWS or value == self.ov_view_name:
            return
        self.ov_view_name = value
        self.ui["overview_view"] = value
        try:
            from ui.util import save_cfg
            save_cfg(self.cfg)
        except OSError:
            pass
        self.ov_expanded = ""
        self._ov_render()

    def ov_set_filter(self, key):
        if key not in self.ov_chips:
            return
        self.ov_filter = key
        self.ov_expanded = ""
        for k, b in self.ov_chips.items():
            self._ov_chip_style(b, k == key)
        self._ov_render()

    def ov_on_search(self):
        if self._ov_search_job:
            try:
                self.after_cancel(self._ov_search_job)
            except Exception:                 # noqa: BLE001
                pass
        self._ov_search_job = self.after(160, self._ov_apply_search)

    def _ov_apply_search(self):
        self._ov_search_job = None
        self.ov_q = self.ov_search.get().strip().lower() if hasattr(self, "ov_search") else ""
        self.ov_expanded = ""
        self._ov_render()

    def _ov_visible_rows(self):
        if not self.ov_data:
            return []
        rows = self.ov_data["rows"]
        if self.ov_filter != "all":
            rows = [r for r in rows if r["status"] == self.ov_filter]
        if self.ov_q:
            q = self.ov_q
            rows = [r for r in rows
                    if q in (r["label"] + " " + r["level"] + " " + r["scene"]).lower()]
        return rows

    # ---- 渲染入口 ----
    def _ov_render(self):
        if not hasattr(self, "ov_holder"):
            return
        for w in self.ov_holder.winfo_children():
            w.destroy()
        if not self.ov_data:
            return
        self._ov_update_chips()
        if self.ov_view_name == "卡片":
            self._ov_build_cards()
        elif self.ov_view_name == "看板":
            self._ov_build_board()
        else:
            self._ov_build_matrix()

    def ov_toggle_row(self, level):
        self.ov_expanded = "" if self.ov_expanded == level else level
        if self.ov_view_name != "矩阵":
            return
        self._ov_build_matrix()

    def ov_show_in_matrix(self, level):
        self.ov_view_name = "矩阵"
        self.ui["overview_view"] = "矩阵"
        self.ov_view_seg.set("矩阵")
        try:
            from ui.util import save_cfg
            save_cfg(self.cfg)
        except OSError:
            pass
        self.ov_expanded = level
        self._ov_render()
        self._ov_scroll_to_level(level)

    def _ov_scroll_to_level(self, level):
        r"""B/C 点「查看」切回矩阵时，把展开的那一行滚到可见位置。"""
        try:
            rows = self._ov_visible_rows()
            idx = next((i for i, r in enumerate(rows) if r["level"] == level), 0)
            frac = max(0.0, min(0.85, (idx - 1) / float(max(1, len(rows)))))
            self.after(60, lambda: self.ov_body._parent_canvas.yview_moveto(frac))
        except Exception:                     # noqa: BLE001
            pass

    def ov_goto_first(self):
        if not hasattr(self, "opt_map"):
            return
        self.show_sub("路点数据", "人机路点")
        self.set_status("去「人机路点」选一张图，点「开始编辑这张图」")

    def ov_goto_waypoint(self, level):
        if not hasattr(self, "opt_map") or not hasattr(self, "map_disp"):
            return
        disp = ""
        for d, (lv, _lab, _fp) in self.map_disp.items():
            if lv == level:
                disp = d
                break
        if not disp:
            self.set_status("这张图没有可编辑的路点图（只有可走面）")
            return
        self.show_sub("路点数据", "人机路点")
        self.opt_map.set(disp)
        self.on_pack_change()
        self.set_status("已定位到 %s" % self.current_map()[1])

    def ov_open_dir(self, path, what):
        if path and os.path.exists(path):
            self.open_folder(path)
        else:
            self.set_status("没有 %s：%s" % (what, path or "（空）"))


    # ---- A 矩阵 ----
    def _ov_matrix_row_frame(self, parent, bg):
        row = ctk.CTkFrame(parent, fg_color="#3a3f47", corner_radius=0)
        row.pack(fill="x", pady=(0, 1))
        row.grid_columnconfigure(0, minsize=194, weight=0)
        for c in range(1, 5):
            row.grid_columnconfigure(c, minsize=128, weight=1)
        cells = []
        for c in range(5):
            cell = ctk.CTkFrame(row, fg_color=bg, corner_radius=0)
            cell.grid(row=0, column=c, sticky="nsew", padx=(0, 1 if c < 4 else 0))
            cells.append(cell)
        return row, cells

    def _ov_hcell(self, cell, main, hint=""):
        ctk.CTkLabel(cell, text=main, font=("Microsoft YaHei UI", 10, "bold"), height=15,
                     text_color="#bac2cc", anchor="w").pack(fill="x", padx=8, pady=(4, 0))
        if hint:
            ctk.CTkLabel(cell, text=hint, font=("Microsoft YaHei UI", 8), height=11,
                         text_color="#707985", anchor="w").pack(fill="x", padx=8, pady=(0, 3))

    def _ov_build_matrix(self):
        rows = self._ov_visible_rows()
        self._ov_row_widgets = {}
        box = ctk.CTkFrame(self.ov_holder, fg_color="#3a3f47", corner_radius=6)
        box.pack(fill="x", pady=(0, 2))
        hrow, cells = self._ov_matrix_row_frame(box, "#2b3138")
        for c, (main, hint) in enumerate((
                ("地图", ""),
                ("① 备份 / 原生", "快照也在这"),
                ("编辑中", "packs"),
                ("成品", "final"),
                ("部署 / 游戏加载", "按启动档"))):
            self._ov_hcell(cells[c], main, hint)
        if not rows:
            ctk.CTkLabel(self.ov_holder, text="这个筛选下没有地图",
                         font=FONT_S, text_color="#7d8792", anchor="w").pack(
                fill="x", padx=10, pady=14)
            return
        for idx, r in enumerate(rows):
            row = self._ov_matrix_data(box, r, "#242424" if idx % 2 == 0 else "#1f1f1f")
            self._ov_row_widgets[r["level"]] = row
            if self.ov_expanded == r["level"]:
                self._ov_detail(box, r)

    def _ov_matrix_data(self, box, r, bg):
        row, cells = self._ov_matrix_row_frame(box, bg)
        native = r["native"]
        draft = r.get("draft")
        final = r.get("final")
        game = r["game"]
        st_sc, st_bg = STATUS_STYLE.get(r["status"], STATUS_STYLE["idle"])

        # 地图
        top = ctk.CTkFrame(cells[0], fg_color="transparent")
        top.pack(fill="x", padx=8, pady=(5, 0))
        ctk.CTkLabel(top, text="%02d" % r["no"], font=("Consolas", 9), height=15,
                     text_color="#7c8793", width=20, anchor="w").pack(side="left")
        ctk.CTkLabel(top, text=_cut(r["label"], 8),
                     font=("Microsoft YaHei UI", 12, "bold"), height=18,
                     text_color="#eef1f4", anchor="w").pack(side="left", padx=(3, 4))
        ctk.CTkLabel(top, text=STATUS_LABEL.get(r["status"], ""),
                     font=("Microsoft YaHei UI", 9, "bold"),
                     fg_color=st_bg, text_color=st_sc, corner_radius=8,
                     height=18, width=46, anchor="center").pack(side="right")
        ctk.CTkLabel(cells[0], text="%s · %s" % (r["level"], r["scene"]),
                     font=("Consolas", 9), height=12, text_color="#6f7883", anchor="w").pack(
            fill="x", padx=8, pady=(0, 3))

        # 备份①
        if native.get("has_map"):
            bmain = "%s 点" % _num(native.get("nodes"))
            bsub = "原生底图 · 快照 %d" % len(r.get("snapshots") or [])
            bcolor = "#717b86"
        else:
            bmain = "只有可走面"
            bsub = "%s · 无 map.json" % (native.get("navmesh_name") or "navmesh")
            bcolor = "#7f6ca8"
        self._ov_cell(cells[1], bmain, bsub, sub_color=bcolor)

        # 编辑中
        if draft:
            dmain = "%s 点" % _num(draft.get("nodes"))
            if draft.get("changes", 0) == 0:
                dsub = "%s · 刚建草稿" % (draft.get("at", "")[5:16] or "-")
            else:
                dsub = "%s · %s" % (draft.get("at", "")[5:16] or "-", draft.get("mode_label", ""))
            dcolor = "#717b86"
        else:
            dmain = "—"
            dsub = "未建草稿"
            dcolor = "#b58b3c"
        self._ov_cell(cells[2], dmain, dsub, main_muted=not draft, sub_color=dcolor)

        # 成品
        if final:
            fmain = "%s 点" % _num(final.get("nodes"))
            same = draft and draft.get("sha256") == final.get("sha256")
            fsub = "%s · %s" % (final.get("published", "")[5:16] or "-",
                                "与草稿一致" if same else ("比草稿旧" if draft else "无草稿"))
            fcolor = "#717b86"
        else:
            fmain = "未发布"
            fsub = "发布后游戏才用"
            fcolor = "#b58b3c"
        self._ov_cell(cells[3], fmain, fsub, main_muted=not final, sub_color=fcolor)

        # 游戏里加载
        gmain = game.get("label", "—")
        self._ov_cell(cells[4], gmain, game.get("sub", ""),
                      main_color=GAME_STYLE.get(game.get("state"), "#cfd6de"),
                      sub_color="#717b86")

        self._ov_bind_row(row, r["level"])
        return row

    def _ov_cell(self, cell, main, sub, main_muted=False, main_color="",
                 sub_color="#717b86"):
        ctk.CTkLabel(cell, text=_cut(main, 12),
                     font=("Microsoft YaHei UI", 12, "bold"), height=17,
                     text_color=("#7b848e" if main_muted else (main_color or "#e4e8ec")),
                     anchor="w").pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(cell, text=_cut(sub, 19),
                     font=("Microsoft YaHei UI", 9), height=13,
                     text_color=sub_color, anchor="w").pack(fill="x", padx=8, pady=(0, 3))

    def _ov_bind_row(self, widget, level):
        widget.bind("<Button-1>", lambda _e, lv=level: self.ov_toggle_row(lv))
        for child in widget.winfo_children():
            self._ov_bind_row(child, level)

    def _ov_detail(self, box, r):
        native = r["native"]
        draft = r.get("draft")
        final = r.get("final")
        snaps = r.get("snapshots") or []
        detail = ctk.CTkFrame(box, fg_color="#1b1f24", corner_radius=0)
        detail.pack(fill="x", pady=(0, 1))
        inner = ctk.CTkFrame(detail, fg_color="transparent")
        inner.pack(fill="x", padx=10, pady=(7, 4))
        for c in range(3):
            inner.grid_columnconfigure(c, weight=1, uniform="ovdetail")

        items = []
        if draft:
            items.append(("编辑中 · packs",
                          draft.get("path") or draft.get("dir") or "",
                          "%s 点 / %s 边 · %s 写入" % (
                              _num(draft.get("nodes")), _num(draft.get("edges")),
                              draft.get("at", "-"))))
        elif native.get("has_map"):
            items.append(("编辑中 · packs", os.path.join(PACKS, r["folder"]),
                          "还没有草稿；去人机路点开始编辑"))
        else:
            items.append(("编辑中 · packs", "", "无点图，不能编辑"))

        items.append(("成品 · final",
                      final.get("path") if final else "",
                      ("%s 点 / %s 边 · %s 发布" % (
                          _num(final.get("nodes")), _num(final.get("edges")),
                          final.get("published", "-"))) if final else "还没有发布"))
        if snaps:
            last = " / ".join(s.get("at", "")[5:16] for s in snaps[:3])
            items.append(("备份① · native / 快照",
                          os.path.dirname(snaps[0]["path"]),
                          "原生 %s 点 · 快照 %d 份 · %s" % (
                              _num(native.get("nodes")), len(snaps), last)))
        else:
            items.append(("备份① · native", native.get("path") or "",
                          ("原生 %s 点" % _num(native.get("nodes"))) if native.get("has_map")
                          else "只有可走面 %s" % native.get("navmesh_name")))

        for c, (label, path, meta) in enumerate(items[:3]):
            boxi = ctk.CTkFrame(inner, fg_color="transparent")
            boxi.grid(row=0, column=c, sticky="nsew", padx=(0, 8))
            ctk.CTkLabel(boxi, text=label, font=("Microsoft YaHei UI", 8), height=12,
                         text_color="#6f7985", anchor="w").pack(fill="x")
            ctk.CTkLabel(boxi, text=compact_path(path, 46) if path else "—",
                         font=("Consolas", 9), height=14,
                         text_color="#aab3be", anchor="w").pack(fill="x")
            ctk.CTkLabel(boxi, text=_cut(meta, 46), font=("Microsoft YaHei UI", 8), height=12,
                         text_color="#68727d", anchor="w").pack(fill="x")

        bar = ctk.CTkFrame(detail, fg_color="transparent")
        bar.pack(fill="x", padx=10, pady=(0, 7))
        can_edit = bool(native.get("has_map"))
        ctk.CTkButton(bar, text="去人机路点", width=96, height=24, font=FONT_S,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      state=("normal" if can_edit else "disabled"),
                      command=lambda lv=r["level"]: self.ov_goto_waypoint(lv)).pack(
            side="left", padx=(0, 5))
        ctk.CTkButton(bar, text="打开草稿目录", width=104, height=24, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      state=("normal" if draft or native.get("has_map") else "disabled"),
                      command=lambda: self.ov_open_dir(
                          (draft or {}).get("dir") or "", "草稿目录")).pack(
            side="left", padx=(0, 5))
        ctk.CTkButton(bar, text="打开成品目录", width=104, height=24, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      state=("normal" if final else "disabled"),
                      command=lambda: self.ov_open_dir(
                          os.path.dirname(final["path"]) if final else "", "成品目录")).pack(
            side="left", padx=(0, 5))
        ctk.CTkButton(bar, text="打开快照目录", width=104, height=24, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      state=("normal" if snaps else "disabled"),
                      command=lambda: self.ov_open_dir(
                          os.path.dirname(snaps[0]["path"]) if snaps else "", "快照目录")).pack(
            side="left")
        ctk.CTkLabel(bar, text="当前启动档：%s · 游戏加载 %s" % (
            "编辑中" if self.ov_data and self.ov_data.get("start_mode") == "edit" else "成品",
            r["game"].get("label", "—")),
            font=("Microsoft YaHei UI", 9), text_color="#737d88", anchor="e").pack(
            side="right")


    # ---- B 卡片 ----
    def _ov_status_chip(self, parent, status):
        fg, bg = STATUS_STYLE.get(status, STATUS_STYLE["idle"])
        return ctk.CTkLabel(parent, text=STATUS_LABEL.get(status, ""),
                            font=("Microsoft YaHei UI", 9, "bold"),
                            fg_color=bg, text_color=fg, corner_radius=8,
                            height=18, width=46, anchor="center")

    def _ov_build_cards(self):
        rows = self._ov_visible_rows()
        cards = ctk.CTkFrame(self.ov_holder, fg_color="transparent")
        cards.pack(fill="x", pady=(0, 2))
        for c in range(3):
            cards.grid_columnconfigure(c, weight=1, uniform="ovcard")
        if not rows:
            ctk.CTkLabel(cards, text="这个筛选下没有地图", font=FONT_S,
                         text_color="#7d8792", anchor="w").grid(
                row=0, column=0, columnspan=3, sticky="w", padx=6, pady=14)
            return
        for idx, r in enumerate(rows):
            self._ov_card(cards, r, idx // 3, idx % 3)

    def _ov_card(self, parent, r, rr, cc):
        native = r["native"]
        draft = r.get("draft")
        final = r.get("final")
        game = r["game"]
        fg, _bg = STATUS_STYLE.get(r["status"], STATUS_STYLE["idle"])
        card = ctk.CTkFrame(parent, corner_radius=8, fg_color="#232323",
                            border_width=1, border_color=fg)
        card.grid(row=rr, column=cc, sticky="nsew", padx=(0, 6), pady=(0, 6))
        ctk.CTkFrame(card, fg_color=fg, width=3, corner_radius=0).place(
            x=0, y=0, relheight=1.0)

        head = ctk.CTkFrame(card, fg_color="transparent")
        head.pack(fill="x", padx=(10, 7), pady=(7, 1))
        ctk.CTkLabel(head, text="%02d" % r["no"], font=("Consolas", 9), height=15,
                     text_color="#7c8793", width=20, anchor="w").pack(side="left")
        ctk.CTkLabel(head, text=_cut(r["label"], 7),
                     font=("Microsoft YaHei UI", 12, "bold"), height=18,
                     text_color="#eef1f4", anchor="w").pack(side="left", padx=(2, 4))
        self._ov_status_chip(head, r["status"]).pack(side="right")
        ctk.CTkLabel(card, text="%s · %s" % (r["level"], r["scene"]),
                     font=("Consolas", 8), height=12, text_color="#6f7883", anchor="w").pack(
            fill="x", padx=(10, 7), pady=(0, 2))

        rail = ctk.CTkFrame(card, fg_color="transparent")
        rail.pack(fill="x", padx=(10, 7))
        for c in range(4):
            rail.grid_columnconfigure(c, weight=1, uniform="ovrail")
        if native.get("has_map"):
            bval = _num(native.get("nodes"))
            bsub = "快照 %d" % len(r.get("snapshots") or [])
        else:
            bval = "可走面"
            bsub = native.get("navmesh_name") or "navmesh"
        if draft:
            dval = _num(draft.get("nodes"))
            dsub = "有草稿" if draft.get("changes", 0) else "刚建"
        else:
            dval, dsub = "—", "没有"
        if final:
            fval = _num(final.get("nodes"))
            fsub = "已发布"
            if draft and draft.get("sha256") != final.get("sha256"):
                fsub = "比草稿旧"
        else:
            fval, fsub = "—", "未发布"
        dsub2 = {"ok": "游戏加载", "warn": "草稿未发", "edit": "当前档",
                 "native": "原生", "nograph": "无点图"}.get(game.get("state"), "原生")
        vals = (("备份①", bval, bsub, "#737b85"),
                ("编辑中", dval, dsub, "#82aef0" if draft else "#737b85"),
                ("成品", fval, fsub, "#d6b676" if final else "#737b85"),
                ("部署", game.get("label", "—"), dsub2,
                 GAME_STYLE.get(game.get("state"), "#cfd6de")))
        for c, (lab, val, sub, color) in enumerate(vals):
            mini = ctk.CTkFrame(rail, fg_color="transparent")
            mini.grid(row=0, column=c, sticky="nsew", padx=(0, 2))
            ctk.CTkLabel(mini, text="●", font=("Microsoft YaHei UI", 7), height=9,
                         text_color=color, anchor="w").pack(fill="x")
            ctk.CTkLabel(mini, text=lab, font=("Microsoft YaHei UI", 8), height=11,
                         text_color="#7f8994", anchor="w").pack(fill="x")
            ctk.CTkLabel(mini, text=_cut(val, 8),
                         font=("Microsoft YaHei UI", 10, "bold"), height=14,
                         text_color="#dfe4e9", anchor="w").pack(fill="x")
            ctk.CTkLabel(mini, text=_cut(sub, 9), font=("Microsoft YaHei UI", 7), height=10,
                         text_color="#69737e", anchor="w").pack(fill="x")

        foot = ctk.CTkFrame(card, fg_color="transparent")
        foot.pack(fill="x", padx=(10, 7), pady=(4, 7))
        ctk.CTkLabel(foot, text="游戏加载：", font=("Microsoft YaHei UI", 8), height=14,
                     text_color="#7d8792").pack(side="left")
        ctk.CTkLabel(foot, text=game.get("label", "—"),
                     font=("Microsoft YaHei UI", 9, "bold"), height=14,
                     text_color=GAME_STYLE.get(game.get("state"), "#cfd6de")).pack(
            side="left")
        ctk.CTkButton(foot, text="查看", width=46, height=22, font=("Microsoft YaHei UI", 9),
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda lv=r["level"]: self.ov_show_in_matrix(lv)).pack(
            side="right")
        self._ov_bind_click(card, lambda lv=r["level"]: self.ov_show_in_matrix(lv))

    def _ov_bind_click(self, widget, callback):
        widget.bind("<Button-1>", lambda _e: callback())
        for child in widget.winfo_children():
            if isinstance(child, ctk.CTkButton):
                continue
            self._ov_bind_click(child, callback)


    # ---- C 看板 ----
    def _ov_build_board(self):
        rows = self._ov_visible_rows()
        board = ctk.CTkFrame(self.ov_holder, fg_color="transparent")
        board.pack(fill="x", pady=(0, 2))
        for c in range(4):
            board.grid_columnconfigure(c, weight=1, uniform="ovboard")
        groups = (
            ("drafting", "编辑中 / 待发布", "草稿还没进成品，游戏还没用上", "#22b8cf"),
            ("sync", "已同步", "成品和草稿一致，游戏已能用", "#40c057"),
            ("finalonly", "只有成品", "没有草稿，要改先建草稿", "#4c8dff"),
            ("idle", "未开始 / 无点图", "没有草稿，也没有成品", "#737b85"),
        )
        for c, (key, title, hint, color) in enumerate(groups):
            if key == "idle":
                items = [r for r in rows if r["status"] in ("idle", "nograph")]
            elif key == "drafting":
                items = [r for r in rows if r["status"] in ("drafting", "publish")]
            else:
                items = [r for r in rows if r["status"] == key]
            col = ctk.CTkFrame(board, fg_color="#1d2126", corner_radius=8,
                               border_width=1, border_color="#2e343d")
            col.grid(row=0, column=c, sticky="nsew", padx=(0, 6))
            ctk.CTkFrame(col, fg_color=color, height=2, corner_radius=0).pack(fill="x")
            head = ctk.CTkFrame(col, fg_color="transparent")
            head.pack(fill="x", padx=7, pady=(6, 1))
            ctk.CTkLabel(head, text=title, font=("Microsoft YaHei UI", 10, "bold"), height=16,
                         text_color="#dce2e9", anchor="w").pack(side="left")
            ctk.CTkLabel(head, text=str(len(items)), font=("Consolas", 9),
                         text_color="#aab3bd", fg_color="#2a3038", corner_radius=8,
                         height=17, width=24, anchor="center").pack(side="left", padx=(5, 0))
            ctk.CTkLabel(col, text=hint, font=("Microsoft YaHei UI", 8), height=13,
                         text_color="#68727d", anchor="w", justify="left",
                         wraplength=165).pack(fill="x", padx=7, pady=(0, 4))
            if not items:
                ctk.CTkLabel(col, text="这个筛选下没有", font=("Microsoft YaHei UI", 8),
                             text_color="#626c77", anchor="center").pack(
                    fill="x", padx=7, pady=12)
                continue
            if key == "idle":
                normal = [r for r in items if r["status"] == "idle"]
                nog = [r for r in items if r["status"] == "nograph"]
                for r in normal:
                    self._ov_board_card(col, r, color)
                if normal and nog:
                    ctk.CTkFrame(col, fg_color="#2e343d", height=1).pack(
                        fill="x", padx=7, pady=(3, 5))
                    ctk.CTkLabel(col, text="只有可走面 · 不可编辑",
                                 font=("Microsoft YaHei UI", 8),
                                 text_color="#6f7984", anchor="w").pack(
                        fill="x", padx=7, pady=(0, 4))
                for r in nog:
                    self._ov_board_card(col, r, color)
            else:
                for r in items:
                    self._ov_board_card(col, r, color)

    def _ov_board_card(self, col, r, accent):
        draft = r.get("draft")
        final = r.get("final")
        native = r["native"]
        status = r["status"]
        card = ctk.CTkFrame(col, fg_color="#252a31", corner_radius=7,
                            border_width=1, border_color="#343c47")
        card.pack(fill="x", padx=6, pady=(0, 6))
        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=7, pady=(6, 0))
        ctk.CTkLabel(top, text="%02d" % r["no"], font=("Consolas", 8), height=14,
                     text_color="#7c8793", width=18, anchor="w").pack(side="left")
        ctk.CTkLabel(top, text=_cut(r["label"], 7),
                     font=("Microsoft YaHei UI", 10, "bold"), height=16,
                     text_color="#eef1f4", anchor="w").pack(side="left", padx=(2, 0))
        delta = ""
        if status in ("publish", "drafting"):
            if final:
                d = int(draft.get("nodes", 0)) - int(final.get("nodes", 0))
                delta = ("+%d" % d) if d >= 0 else str(d)
            else:
                delta = "NEW"
        if delta:
            ctk.CTkLabel(top, text=delta, font=("Consolas", 9),
                         text_color="#f0b95d", anchor="e").pack(side="right")

        if status in ("publish", "drafting"):
            mid = "草稿 %s · 成品 %s" % (
                _num(draft.get("nodes")),
                _num(final.get("nodes")) if final else "—")
            if final:
                d = abs(int(draft.get("nodes", 0)) - int(final.get("nodes", 0)))
                sub = "差 %d 点 · %s 改过" % (d, (draft.get("at") or "")[5:16])
            elif status == "drafting":
                sub = "刚建草稿 · 0 点改动"
            else:
                sub = "还没有发布 · %s" % ((draft.get("at") or "")[5:16])
        elif status == "sync":
            mid = "%s = %s" % (_num(draft.get("nodes")), _num(final.get("nodes")))
            sub = "%s 发布 · 游戏可直接用" % ((final.get("at") or "")[5:16])
        elif status == "finalonly":
            mid = "成品 %s · 无草稿" % _num(final.get("nodes"))
            sub = "%s 发布 · 要改先建草稿" % ((final.get("at") or "")[5:16])
        elif status == "nograph":
            mid = "只有可走面 %s" % (native.get("navmesh_name") or "navmesh")
            sub = "无 map.json · 不能编辑路点"
        else:
            mid = "原生 %s 点 · 无草稿" % _num(native.get("nodes"))
            sub = "还没开始编辑" if native.get("has_map") else "只有可走面"

        ctk.CTkLabel(card, text=_cut(mid, 22), font=("Microsoft YaHei UI", 9), height=14,
                     text_color="#a4adb8", anchor="w").pack(fill="x", padx=7, pady=(3, 0))
        ctk.CTkLabel(card, text=_cut(sub, 24), font=("Microsoft YaHei UI", 8), height=12,
                     text_color="#6f7984", anchor="w").pack(fill="x", padx=7, pady=(0, 0))
        if native.get("has_map"):
            b = "备份 %s · 快照 %d" % (_num(native.get("nodes")),
                                      len(r.get("snapshots") or []))
            ctk.CTkLabel(card, text=b, font=("Microsoft YaHei UI", 8), height=11,
                         text_color="#737d88", anchor="w").pack(
                fill="x", padx=7, pady=(1, 0))
        game = r["game"]
        ctk.CTkLabel(card, text="游戏加载：%s" % game.get("label", "—"),
                     font=("Microsoft YaHei UI", 8), height=11, text_color="#7d8792",
                     anchor="w").pack(fill="x", padx=7, pady=(1, 5))
        self._ov_bind_click(card, lambda lv=r["level"]: self.ov_show_in_matrix(lv))
