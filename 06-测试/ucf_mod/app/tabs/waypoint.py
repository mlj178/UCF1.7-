#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「人机路点」页：编辑中 / 成品两档、节点计数、清空、版本对比。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import time
import tkinter as tk

import customtkinter as ctk

from ui.consts import CMP_COLOR, CMP_SHORT, CMP_TEXT, FONT_S
from ui.maps import _navmesh_name, find_map_doc, load_maps, load_scene_counts, maps_not_listed
from ui.packs import (
    final_current_name, final_versions, load_packs, migrate_flat_packs, pack_summary,
    pack_target_fp, pack_txt,
)
from ui.util import _cut, file_sha256


class WaypointTab:
    # ---- 「人机路点」页：SyPB 式现场编辑的控制台入口 ----
    def wp_card(self, parent, title, sub=""):
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        head = ctk.CTkFrame(box, fg_color="transparent")
        head.pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(head, text=title, font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(side="left")
        if sub:
            ctk.CTkLabel(head, text=sub, font=FONT_S, text_color="#9aa0a6",
                         anchor="e").pack(side="right")
        return box

    def wp_var(self, key, default):
        if key in self.vars:
            return self.vars[key]
        var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
        self.vars[key] = var
        return var

    def wp_switch(self, parent, key, label, default):
        var = self.wp_var(key, default)
        sw = ctk.CTkSwitch(parent, text=label, variable=var, font=FONT_S,
                           progress_color="#2f9e44",
                           command=lambda k=key: self.on_toggle(k))
        return sw

    def build_waypoint_tab(self, tab):
        r"""控制台「人机路点」页。

        设计：早期 design/ 下的页签样稿（已归档到 archive/design/）。它不直接改游戏，
        只负责选图/包、写 ucf_mod.json 开关、给运行中的插件发 ucf_navcmd，
        并显示当前图的指纹与原生点/边数。
        """
        # 测试包 / 地图选择的状态由本页持有（2026-11-19 「测试数据」页删除后并入这里）；
        # 数据页、车测页仍然读 opt_pack / opt_map / seg_mode。
        self.maps = load_maps()                 # [(level, 中文名, 指纹)]
        self.map_disp = {("%s（%s）" % (lab, lv)): (lv, lab, fp) for lv, lab, fp in self.maps}
        pk = self.cfg.get("pack") if isinstance(self.cfg.get("pack"), dict) else {}
        self.pack_on = tk.BooleanVar(value=bool(pk.get("on", False)))
        self.pack_only = tk.BooleanVar(value=bool(pk.get("only_map", True)))
        self.pack_name = str(pk.get("name") or "")
        self.pack_map = str(pk.get("map") or (self.maps[0][0] if self.maps else ""))
        self.wp_scene = load_scene_counts()
        self.pack_disp = {}                     # 下拉框显示文字 → 包 id（地图文件夹/包名）
        self.ensure_pack_folders()              # 按地图自动建 packs\<场景名>\
        migrate_flat_packs()                    # 根目录的老包挪进地图文件夹
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        self.wp_body = body        # 「去人机路点改」跳过来时滚回 ① 卡
        # ① 启动档：编辑中 / 成品 两页（2026-11-21 用户要求：两档内容分开成两页，
        #    页内再用标签切换；不再把两档挤在同一张卡里只换个下拉）
        box = self.wp_card(body, "启动档", "两页各管一档；底部「开始游戏」跟着当前页走")
        self.card_mode = box
        srow = ctk.CTkFrame(box, fg_color="transparent")
        srow.pack(fill="x", padx=12, pady=(6, 0))
        self.seg_mode = ctk.CTkSegmentedButton(
            srow, values=["编辑中（packs·可写）", "成品（只读）"],
            width=470, height=36, dynamic_resizing=False,
            font=("Microsoft YaHei UI", 13, "bold"),
            selected_color="#2f6fdb", selected_hover_color="#255bb4",
            unselected_color="#2a2f36", unselected_hover_color="#343a42",
            command=lambda _v: self.on_page_change())
        self.seg_mode.pack(side="left")
        self.seg_mode.set("编辑中（packs·可写）" if self.pack_on.get() else "成品（只读）")
        self.lbl_mode = ctk.CTkLabel(box, text="", font=FONT_S, text_color="#9aa0a6",
                                     anchor="w", justify="left", wraplength=620)
        self.lbl_mode.pack(fill="x", padx=12, pady=(6, 8))

        self.page_holder = ctk.CTkFrame(body, fg_color="transparent")
        self.page_holder.pack(fill="x")
        self.page_edit = ctk.CTkFrame(self.page_holder, fg_color="transparent")
        self.page_final = ctk.CTkFrame(self.page_holder, fg_color="transparent")
        self.page_is_edit = True
        self.build_edit_page(self.page_edit)
        self.build_final_page(self.page_final)
        self.show_page("编辑中" if self.pack_on.get() else "成品")

        # 游戏内编辑：两档共用（成品档里菜单照样能开，只是改动存不进去）
        box = self.wp_card(body, "游戏内编辑", "配置写 ucf_mod.json")
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=8, pady=(4, 4))
        switches = [
            ("wp_menu", "编辑菜单（F2 / 长按 E）", True),
            ("visualizer", "路点 / 边显示（Ctrl+V）", False),
            ("navmesh_show", "可走面线框（Ctrl+Shift+6）", True),
            ("wp_autoground", "加点自动落地", True),
        ]
        for idx, (key, label, default) in enumerate(switches):
            self.wp_switch(grid, key, label, default).grid(
                row=idx // 2, column=idx % 2, sticky="w",
                padx=(8, 6), pady=5)
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)
        ctk.CTkLabel(
            box,
            text="改完存进 ucf_mod.json；游戏开着时这些开关要重启才生效。"
                 "游戏内快捷键（Ctrl+Shift+N/J/D/Z、Ctrl+V）仍然可用。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=600).pack(fill="x", padx=12, pady=(0, 8))

        self.on_pack_change(persist=False)
        self.refresh_wp_status()

    # ---- 「人机路点」页内：编辑中 / 成品 两页 ------------------------------
    # 页内按钮条在 ui/kit.py 的 build_sub_tabs()（2026-11-24 分组时提到共用层）。
    def show_page(self, which):
        r"""切换「编辑中 / 成品」整页：两档内容各占一块，不再共用一个下拉。"""
        self.page_is_edit = str(which).startswith("编辑中")
        if self.page_is_edit:
            self.page_final.pack_forget()
            self.page_edit.pack(fill="x")
        else:
            self.page_edit.pack_forget()
            self.page_final.pack(fill="x")
        self.update_mode_hint()
        # 对比表：回到成品页时如果它正开着又脏着，当场补上（否则要等用户点标签）
        if (not self.page_is_edit and getattr(self, "_cmp_dirty", False)
                and getattr(self, "_final_tab", "") == "版本对比"):
            self.refresh_compare(force=True)

    def update_mode_hint(self):
        r"""启动档下面那行话：这一页在做什么、启动会用哪一档。"""
        if not hasattr(self, "lbl_mode"):
            return
        if getattr(self, "page_is_edit", True):
            txt = "编辑中（packs·可写）：选包 + 地图 → 游戏内 F2 加点/连线 → 存回包 → 发布到成品。"
            name = self.selected_pack() if hasattr(self, "opt_pack") else ""
            if name:
                txt += "  当前包：" + (self.disp_of(name) or name)
        else:
            ver = self.final_selected() if hasattr(self, "opt_final") else final_current_name()
            if ver:
                # 版本名就是测试包名（可能有 20+ 字符），这行只讲这一页在做什么，名字看下面下拉框
                txt = ("成品（只读）：整版加载，和编辑中是同一个文件，玩起来一样。"
                       "想做新版本去「编辑中」页改。")
            else:
                txt = "成品：还没有版本。先去「编辑中」页做好，再点「发布到成品」。"
        self.lbl_mode.configure(text=txt)

    def on_page_change(self):
        r"""启动档切换：整页换掉，并记住这次启动用哪一档（写进 ucf_mod.json）。"""
        self.show_page(self.seg_mode.get())
        self.on_pack_change(persist=False)      # 只刷新，别在状态行写「已保存 测试包」
        self.persist("启动档")

    def missing_maps_hint(self):
        r"""地图下拉下面那行灰字：为什么少了几张图（不说清楚，看起来就像数据丢了）。"""
        miss = maps_not_listed([lv for lv, _lab, _fp in self.maps])
        if not miss:
            return ""
        face = [m for m in miss if m[3]]       # 有可走面、没路点图 = 纯面图
        todo = [m for m in miss if not m[3]]   # 连可走面都没落盘
        bits = []
        if face:
            name = "、".join("%02d %s（%s）" % (int(no), cn, lv)
                              for no, lv, cn, _f in face)
            nm = " / ".join(_navmesh_name(lv) for _no, lv, _cn, _f in face)
            bits.append("%s只有可走面 %s：场景里原生没有 PointGraph（0 个路点），"
                        "导不出 map.json 和指纹，人机走三角网、改点图对它无效"
                        % (name, nm))
        if todo:
            name = "、".join("%02d %s（%s）" % (int(no), cn, lv)
                              for no, lv, cn, _f in todo)
            bits.append("%s 还没采集到路点图" % name)
        return ("下拉里只有 %d 张有路点图的图；" % len(self.maps)) + "；".join(bits) + "。"

    def build_edit_page(self, page):
        r"""「编辑中」页：「选包与地图」+「发布到成品」两个标签。"""
        frames, show = self.build_sub_tabs(page, ["选包与地图", "发布到成品"])
        self.page_edit_tabs = show

        box = self.wp_card(frames["选包与地图"], "测试包", "只对一张图生效")
        self.card_pick = box
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="测试包", font=FONT_S, text_color="#9aa0a6",
                     width=48, anchor="w").pack(side="left", padx=(0, 6))
        self.opt_pack = ctk.CTkOptionMenu(
            row, values=self._pack_values(), font=FONT_S, width=262,
            command=lambda _v: self.on_pack_change())
        self.opt_pack.pack(side="left", padx=(0, 6))
        want = self.resolve_pack_id(self.pack_name)   # 上次选的包重启后接着选中
        if want and self.disp_of(want):
            self.opt_pack.set(self.disp_of(want))
        ctk.CTkButton(row, text="新建测试包", width=96, height=28, font=FONT_S,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=self.create_pack).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="打开目录", width=76, height=28, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_packs_dir).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="清空本图", width=80, height=28, font=FONT_S,
                      fg_color="#8a4b1e", hover_color="#a55d26",
                      command=self.clear_pack_map).pack(side="left")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="地图", font=FONT_S, text_color="#9aa0a6",
                     width=48, anchor="w").pack(side="left", padx=(0, 6))
        self.opt_map = ctk.CTkOptionMenu(
            row, values=list(self.map_disp) or ["（没有可测的路点图）"],
            font=FONT_S, width=250,
            command=lambda _v: self.on_pack_change())
        self.opt_map.pack(side="left", padx=(0, 8))
        if self.pack_map:
            for disp, (lv, _lab, _fp) in self.map_disp.items():
                if lv == self.pack_map:
                    self.opt_map.set(disp)
                    break
        ctk.CTkCheckBox(row, text="只对这张图生效", variable=self.pack_only,
                        font=FONT_S, checkbox_width=18, checkbox_height=18,
                        command=self.on_pack_change).pack(side="left")
        # 少的那几张图在这里说清楚：纯面图没有 PointGraph，永远进不了下拉
        hint = self.missing_maps_hint()
        if hint:
            ctk.CTkLabel(box, text=hint, font=FONT_S, text_color="#8a8f96",
                         anchor="w", justify="left",
                         wraplength=620).pack(fill="x", padx=12, pady=(4, 0))

        self.wp_meta = ctk.CTkLabel(box, text="", font=("Consolas", 11),
                                    text_color="#9aa0a6", anchor="w",
                                    justify="left", wraplength=620)
        self.wp_meta.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(
            box,
            text="测试包按地图归类：packs\\<序号_场景名中文名>\\<包名>\\，序号按《地图对照表》（01 运输船 … 11 新寂静村）。\n"
                 "两种建法：空白地图（grow，原生点全禁用、从 0 画）/ 原版基础 + 新增（keep，原版路线照常走，只加你的点）。\n"
                 "两种都不限点数；飓风危城原生 0 点用「空白地图」。测试包只影响选中的图。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(2, 6))
        ctk.CTkLabel(
            box,
            text=("进游戏现场编辑：F2 打开路点菜单（长按 E 备用）；1-9 直选，小键盘 8/2 上下、5 确认、0 返回。\n"
                  "菜单打开时 W/A/S/D/空格仍可移动；选完 A 可走到 B 再按小键盘 5 连边。\n"
                  "按 F2 / 小键盘前先点一下游戏画面，让游戏窗口拿到焦点（控制台在前台时游戏收不到键）。\n"
                  "空白包=原生点全禁用；必须整图连通：孤立点、出生点、蹲守标记都可能让 Bot 取不到路。"),
            font=("Consolas", 11), text_color="#8a8f96", anchor="w",
            justify="left", wraplength=620).pack(fill="x", padx=12, pady=(0, 10))

        box = self.wp_card(frames["发布到成品"], "发布到成品", "编辑中 → 成品（只读）")
        ctk.CTkLabel(
            box,
            text="发布 = 把当前测试包的 <指纹>.txt 原样复制进成品，字节一样 → 玩起来一样。\n"
                 "默认「新建一版」：以当前版为底整套复制再替换这张图，版本名沿用测试包的名字，老版本全留着；\n"
                 "也可以只更新当前版。成品里的文件自动设成只读；发完切到上面的「成品」页就能选它启动。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(6, 4))
        prow = ctk.CTkFrame(box, fg_color="transparent")
        prow.pack(fill="x", padx=12, pady=(2, 10))
        self.btn_promote = ctk.CTkButton(
            prow, text="发布到成品（编辑中 → 成品）", font=FONT_S, height=30,
            fg_color="#2f9e44", hover_color="#37b24d", command=self.do_promote)
        self.btn_promote.pack(side="left")
        ctk.CTkLabel(prow, text="默认新建一版、版本名跟包名（老版本全留着）；成品目录 final\\",
                     font=FONT_S, text_color="#9aa0a6").pack(side="left", padx=(10, 0))

    def build_final_page(self, page):
        r"""「成品」页：「版本」+「版本对比」两个标签（成品只读，按版本整套启动）。"""
        frames, show = self.build_sub_tabs(page, ["版本", "版本对比"])
        self._final_tab = "版本"

        def final_tabs(name):
            r"""切成品页标签；切到「版本对比」时把之前攒下的刷新补上。"""
            self._final_tab = name
            show(name)
            if name == "版本对比" and getattr(self, "_cmp_dirty", False):
                self.refresh_compare(force=True)

        self.page_final_tabs = final_tabs

        box = self.wp_card(frames["版本"], "成品版本", "一版 = 一整套数据（所有图一起）")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="启动版本", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.opt_final = ctk.CTkOptionMenu(
            row, values=["（还没有版本）"], font=FONT_S, width=262,
            command=lambda _v: self.on_final_change())
        self.opt_final.pack(side="left", padx=(0, 6))
        self.btn_rename_final = ctk.CTkButton(
            row, text="改名", width=56, height=28, font=FONT_S,
            fg_color="#3a3f47", hover_color="#4a5058", command=self.rename_final)
        self.btn_rename_final.pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="打开目录", width=76, height=28, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_final_dir).pack(side="left", padx=(0, 6))
        self.btn_delete_final = ctk.CTkButton(
            row, text="删除", width=56, height=28, font=FONT_S,
            fg_color="#8a1c1c", hover_color="#a32424", command=self.delete_final)
        self.btn_delete_final.pack(side="left")
        self.lbl_final = ctk.CTkLabel(box, text="", font=("Consolas", 11),
                                      text_color="#9aa0a6", anchor="w",
                                      justify="left", wraplength=620)
        self.lbl_final.pack(fill="x", padx=12, pady=(4, 0))
        ctk.CTkLabel(
            box,
            text="成品只读：游戏里改得动，但存不进去（文件带只读属性）。\n"
                 "想做新东西去「编辑中」页改，再点「发布到成品」；版本名跟包名，老版本都留着。\n"
                 "启动成品 = 整版加载（UCF_PACK_DIR=②\\final + UCF_PACK=<版本>），和编辑中同一套加载逻辑。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(2, 8))
        self.final_disp = {}
        self.refresh_final_combo()

        self.build_compare_card(frames["版本对比"])

    def refresh_wp_tab(self):
        if not hasattr(self, "wp_meta"):
            return
        self.refresh_wp_status()

    # ---- 版本对比面板：编辑中的每个包 ↔ 选中的成品版本（颜色 = 状态）------
    # ---- 版本对比表：编辑中 ↔ 成品 左右并排，最后一列给结论（2026-11-21 改成表格）
    def build_compare_card(self, parent):
        r"""成品页「版本对比」：一张表，左边编辑中、右边成品，最后一列结论。"""
        box = self.wp_card(parent, "版本对比 · 编辑中 ↔ 成品",
                           "sha256 相同 = 同一个文件，玩起来一样")
        head = ctk.CTkFrame(box, fg_color="transparent")
        head.pack(fill="x", padx=12, pady=(4, 0))
        self.lbl_cmp = ctk.CTkLabel(head, text="", font=FONT_S, text_color="#9aa0a6",
                                    anchor="w", justify="left", wraplength=430)
        self.lbl_cmp.pack(side="left")
        ctk.CTkButton(head, text="刷新", width=56, height=26, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.refresh_compare).pack(side="right")
        self.cmp_body = ctk.CTkFrame(box, fg_color="#3a3f47", corner_radius=6)
        self.cmp_body.pack(fill="x", padx=10, pady=(6, 2))
        leg = ctk.CTkFrame(box, fg_color="transparent")
        leg.pack(fill="x", padx=12, pady=(2, 8))
        for key in ("same", "diff", "only_pack", "only_final", "fp_bad"):
            ctk.CTkLabel(leg, text=CMP_TEXT[key], font=("Consolas", 11),
                         text_color=CMP_COLOR[key]).pack(side="left", padx=(0, 10))
        self._cmp_dirty = True
        self.refresh_compare(force=True)

    def compare_groups(self):
        r"""[(fp, 左=编辑中, 右=成品条目, 状态)]：每个包一组，外加成品里没有包对应的图。"""
        ver = self.final_selected()
        vmeta = next((v for v in final_versions() if v["name"] == ver), None) or {}
        fmaps = dict(vmeta.get("maps") or {})
        known = {fp: (lv, lab) for lv, lab, fp in self.maps}
        rows, used = [], set()
        for pid in load_packs():
            fp = pack_target_fp(pid)
            p = pack_txt(pid, fp)
            if not p:
                continue
            summ = pack_summary(pid, fp)
            mtime = "-"
            if summ.get("mtime"):
                mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(summ["mtime"]))
            # 表格里只要包名本身：去掉「运输船 · 」前缀，不然两行截断后长得一样
            raw_name = str(self.disp_of(pid) or pid).split(" · ")[-1].split("/")[-1]
            left = {"name": raw_name, "fp": fp,
                    "mtime": mtime, "node": summ.get("nadd", 0) + summ.get("ndel", 0),
                    "edge": summ.get("eadd", 0) + summ.get("edel", 0),
                    "sha": file_sha256(p)}
            right = fmaps.get(fp)
            used.add(fp)
            if fp not in known:
                st = "fp_bad"
            elif not right:
                st = "only_pack"
            elif right.get("sha256") and right["sha256"] == left["sha"]:
                st = "same"
            else:
                st = "diff"
            rows.append((fp, left, right, st))
        for fp, m in sorted(fmaps.items()):
            if fp not in used:
                rows.append((fp, None, m, "only_final"))
        return known, rows

    # ---- 对比表的小零件 ---------------------------------------------------
    def _cmp_cell(self, row, col, fg):
        r"""一个格子：靠 1px 缝隙当网格线（父框底色 #3a3f47）。"""
        cell = ctk.CTkFrame(self.cmp_body, corner_radius=0, fg_color=fg)
        cell.grid(row=row, column=col, sticky="nsew",
                  padx=(0, 0 if col == 3 else 1), pady=(0, 1))
        return cell

    def _cmp_side(self, row, col, fg, meta, missing):
        r"""左/右半边的一格：第一行包名，第二行 时间 · 点/边 · sha。"""
        cell = self._cmp_cell(row, col, fg)
        if not meta:
            ctk.CTkLabel(cell, text="—", font=("Consolas", 11),
                         text_color="#6c7278", anchor="w").pack(fill="x", padx=8, pady=(4, 0))
            ctk.CTkLabel(cell, text=missing, font=("Microsoft YaHei UI", 10),
                         text_color="#6c7278", anchor="w").pack(fill="x", padx=8, pady=(0, 4))
            return
        name = str(meta.get("name") or meta.get("from_pack") or "-").split("/")[-1]
        when = str(meta.get("mtime") or meta.get("published") or "-")
        if len(when) >= 16 and when[:4].isdigit():
            when = when[5:16]
        node = int(meta.get("node") or 0)
        edge = int(meta.get("edge") or 0)
        sha = str(meta.get("sha256") or meta.get("sha") or "-")[:8]
        ctk.CTkLabel(cell, text=_cut(name, 30), font=("Consolas", 11),
                     text_color="#e6e6e6", anchor="w").pack(fill="x", padx=8, pady=(4, 0))
        ctk.CTkLabel(cell, text="%s · %d/%d · %s" % (when, node, edge, sha),
                     font=("Consolas", 10), text_color="#868e96",
                     anchor="w").pack(fill="x", padx=8, pady=(0, 4))

    def refresh_compare(self, force=False):
        r"""重建对比表（切包 / 换成品版本 / 发布完都会调）。

        表在别的页签/别的页时只记一笔（_cmp_dirty），等它真被看见再画，
        免得每次切档都白建 20 个控件。
        """
        if not hasattr(self, "cmp_body"):
            return
        if not force and not self.cmp_body.winfo_ismapped():
            self._cmp_dirty = True
            return
        self._cmp_dirty = False
        try:
            for w in self.cmp_body.winfo_children():
                w.destroy()
            known, rows = self.compare_groups()
        except Exception as exc:                     # noqa: BLE001
            self.lbl_cmp.configure(text="对比读不了：%s" % exc, text_color="#e03131")
            return
        ver = self.final_selected()
        if not ver:
            self.lbl_cmp.configure(text="成品里还没有版本：先发布一版，才能比。",
                                   text_color="#f59f00")
        else:
            cnt = {}
            for _fp, _l, _r, st in rows:
                cnt[st] = cnt.get(st, 0) + 1
            self.lbl_cmp.configure(
                text="%d 组：%s" % (
                    len(rows),
                    " · ".join("%s %d" % (CMP_TEXT[k], cnt[k])
                               for k in ("same", "diff", "only_pack", "only_final", "fp_bad")
                               if cnt.get(k))),
                text_color="#9aa0a6")
        if not rows:
            ctk.CTkLabel(self.cmp_body, text="编辑中还没有包，成品里也没有图 —— 没得比。",
                         font=FONT_S, text_color="#868e96", anchor="w").grid(
                row=0, column=0, columnspan=4, sticky="w", padx=10, pady=8)
            return
        # 列宽：地图 / 编辑中 / 成品 / 结论
        self.cmp_body.grid_columnconfigure(0, minsize=104, weight=0)
        self.cmp_body.grid_columnconfigure(1, minsize=240, weight=1)
        self.cmp_body.grid_columnconfigure(2, minsize=240, weight=1)
        self.cmp_body.grid_columnconfigure(3, minsize=96, weight=0)
        for col, text in enumerate(("地图", "编辑中（packs）", "成品", "结论")):
            cell = self._cmp_cell(0, col, "#2b3138")
            ctk.CTkLabel(cell, text=text, font=("Microsoft YaHei UI", 11, "bold"),
                         text_color="#c9cdd2", anchor="w").pack(
                fill="x", padx=8, pady=(6, 0) if col == 2 else 6)
            if col == 2:           # 版本名太长不进表头，单起一行小字
                ctk.CTkLabel(cell, text=_cut(ver or "—", 30), font=("Consolas", 10),
                             text_color="#868e96", anchor="w").pack(
                    fill="x", padx=8, pady=(0, 4))
        for idx, (fp, left, right, st) in enumerate(rows[:14]):
            bg = "#262626" if idx % 2 == 0 else "#1f1f1f"
            lv, lab = known.get(fp, ("", ""))
            if not lab and right:
                lab = str(right.get("label") or "")
                lv = lv or str(right.get("level") or "")
            cell = self._cmp_cell(idx + 1, 0, bg)
            ctk.CTkLabel(cell, text=lab or "未知地图",
                         font=("Microsoft YaHei UI", 11, "bold"),
                         text_color="#e6e6e6", anchor="w").pack(fill="x", padx=8, pady=(4, 0))
            ctk.CTkLabel(cell, text=lv or "-", font=("Consolas", 10),
                         text_color="#868e96", anchor="w").pack(fill="x", padx=8, pady=(0, 4))
            self._cmp_side(idx + 1, 1, bg, left, "没有这个包")
            self._cmp_side(idx + 1, 2, bg, right,
                           "包作废，没发布过" if st == "fp_bad" else "这一版里没有这张图")
            cell = self._cmp_cell(idx + 1, 3, bg)
            ctk.CTkLabel(cell, text=CMP_SHORT.get(st, st),
                         font=("Microsoft YaHei UI", 11, "bold"),
                         text_color=CMP_COLOR.get(st, "#868e96"),
                         anchor="w").pack(fill="x", padx=8, pady=(12, 0))
        if len(rows) > 14:
            ctk.CTkLabel(self.cmp_body, text="…还有 %d 组没显示（先归档几个包）"
                         % (len(rows) - 14), font=FONT_S, text_color="#868e96",
                         anchor="w").grid(row=15, column=0, columnspan=4,
                                          sticky="w", padx=10, pady=6)

    def refresh_wp_status(self):
        if not hasattr(self, "wp_meta"):
            return
        pk = self.pack_dict() if hasattr(self, "opt_pack") else {}
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        doc, _path = find_map_doc(fp)
        counts = (doc or {}).get("counts") or {}
        nodes = int(counts.get("nodes") or 0)
        edges = int(counts.get("edges") or 0)
        pack_on = bool(pk.get("on"))
        if pack_on and name:
            which = "编辑中 " + (self.disp_of(name) or name)
        else:
            ver = self.final_selected() if hasattr(self, "opt_final") else final_current_name()
            which = ("成品 %s（只读）" % ver) if ver else "成品（还没有版本）"
        self.wp_meta.configure(
            text="指纹 %s · 原生 %d 点 / %d 边 · %s" % (fp or "—", nodes, edges, which))
