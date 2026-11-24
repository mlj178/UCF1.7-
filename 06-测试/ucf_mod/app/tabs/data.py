#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""「数据」页：三区路径与时间、部署 / 还原 / 校验。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import os
import queue

import customtkinter as ctk

from ui.consts import FONT, FONT_S
from ui.env import DEPLOY, DEV, FINAL_ROOT, NATIVE, PACKS, TEST_VIS
from ui.packs import _FINAL_FP_RE, final_stats, load_packs, pack_dir
from ui.stats import data_counts, diff_count, export_filed, test_stats, tree_hashes
from ui.util import dir_bytes, dir_stats, fmt_short, fmt_time, human_size


class DataTab:
    # ---- 数据页：三区在哪 / 什么时候写的 / 一致不一致（原来三个 .bat 的活）----
    def build_data_tab(self, tab):
        r"""① 备份版 / ② 开发版 / ③ 游戏目录（运行时）的路径、最近写入时间、条数，
        外加 发布到成品（编辑中→成品）/ 还原 ①→② / 校验 ① 的按钮。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text="① 只读快照；② 唯一数据源：一张图一个文件夹（map.json + navmesh.bin），另有 final 成品、packs 草稿、vis 收件箱；"
                               "③ 游戏目录只当运行环境，不放数据。\n"
                               "数据流：游戏导出 → ② vis →（整理导出）→ ② <图>\\导出\\ + <图>\\map.json；"
                               "草稿做完 →（发布这张图）→ ② final\\<指纹>.txt（一张图一份，没有版本）。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=620).pack(fill="x", padx=12, pady=(8, 2))

        self.data_cards = []
        for tag, name, root, hint in (
                ("①", "备份版（只读）", NATIVE, "冻结快照，永不编辑"),
                ("②", "开发版（图文件夹 / 成品 / 编辑中 / 收件箱）", DEV,
                 "一张图一个文件夹：01_TransportShip运输船\\map.json + navmesh.bin；"
                 "另有 final 成品 / packs 编辑中 / vis 收件箱"),
                ("③", "游戏目录（运行时）", DEPLOY, "只放 dll / 配置 / markers；2026-11-21 起不放数据")):
            box = ctk.CTkFrame(body, corner_radius=8)
            box.pack(fill="x", padx=10, pady=(8, 0))
            top = ctk.CTkFrame(box, fg_color="transparent")
            top.pack(fill="x", padx=12, pady=(8, 0))
            ctk.CTkLabel(top, text="%s %s" % (tag, name), font=FONT).pack(side="left")
            when = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6")
            when.pack(side="right")
            prow = ctk.CTkFrame(box, fg_color="transparent")
            prow.pack(fill="x", padx=12)
            open_btn = ctk.CTkButton(prow, text="打开文件夹", width=88, height=22,
                                     font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                     command=lambda p=root: self.open_folder(p))
            open_btn.pack(side="right", padx=(8, 0))
            ctk.CTkLabel(prow, text=root, font=("Consolas", 11), text_color="#7f8792",
                         anchor="w", justify="left", wraplength=500).pack(
                side="left", fill="x", expand=True)
            info = None
            if tag == "②":
                # 2026-11-21 用户要求：成品 / 编辑中 别挤一行（「9 图」是 maps 的、
                # 「8 可走面」是 vis 的，混在一起像同一份数据）。三块各占一行。
                self.dev_rows = {}
                self.dev_open = {}
                ctk.CTkFrame(box, height=1, fg_color="#33383f").pack(
                    fill="x", padx=12, pady=(6, 0))
                for key, label, color, sub in (
                        ("final", "成品（final · 只读）", "#d6b676", FINAL_ROOT),
                        ("packs", "编辑中（packs · 可写）", "#8fb7d9", PACKS),
                        ("vis", "收件箱（vis）", "#9aa0a6", TEST_VIS)):
                    rw = ctk.CTkFrame(box, fg_color="transparent")
                    rw.pack(fill="x", padx=12, pady=(6, 0))
                    ctk.CTkLabel(rw, text=label, font=FONT_S, text_color=color,
                                 width=148, anchor="w").pack(side="left", anchor="n")
                    # 每块自己的文件夹，不用先从 ② 根目录再往下点
                    op = ctk.CTkButton(rw, text="打开", width=46, height=20, font=FONT_S,
                                       fg_color="#3a3f47", hover_color="#4a5058",
                                       command=lambda p=sub: self.open_folder(p))
                    op.pack(side="right", padx=(8, 0), anchor="n")
                    self.dev_open[key] = op
                    txt = ctk.CTkLabel(rw, text="", font=FONT_S, anchor="w", justify="left",
                                       text_color="#c9d1d9", wraplength=600)
                    txt.pack(side="left", fill="x", expand=True)
                    # 窗口变宽/变窄就重算换行宽度：148 给标签、66 给「打开」按钮，
                    # 再留 46 的余量——Configure 事件偶尔比最终宽度早到，宁可早换行也别截字
                    rw.bind("<Configure>", lambda e, w=txt: w.configure(
                        wraplength=max(200, e.width - 260)))
                    self.dev_rows[key] = txt
                ctk.CTkFrame(box, height=8, fg_color="transparent").pack()
            else:
                info = ctk.CTkLabel(box, text="", font=FONT_S, anchor="w", justify="left",
                                    text_color="#c9d1d9")
                info.pack(fill="x", padx=12, pady=(0, 8))
            self.data_cards.append({"tag": tag, "hint": hint, "root": root,
                                    "time": when, "info": info, "open": open_btn})

        self.lbl_same = ctk.CTkLabel(body, text="", font=FONT_S, anchor="w", justify="left",
                                     wraplength=620, text_color="#c9d1d9")
        self.lbl_same.pack(fill="x", padx=14, pady=(8, 0))

        row = ctk.CTkFrame(body, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkButton(row, text="发布到成品（编辑中 → 成品）", font=FONT_S, height=32,
                      fg_color="#2f9e44", hover_color="#37b24d",
                      command=self.do_promote).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="从备份还原 ①→②", font=FONT_S, height=32, fg_color="#8a4b1e",
                      hover_color="#a55d26",
                      command=self.do_restore).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="校验备份版", font=FONT_S, height=32, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.do_verify).pack(side="left", padx=(0, 6))
        ctk.CTkButton(row, text="刷新", font=FONT_S, height=32, width=64, fg_color="#3a3f47",
                      hover_color="#4a5058",
                      command=self.refresh_data).pack(side="left")

        self.data_out = ctk.CTkTextbox(body, height=118, font=("Consolas", 11),
                                       fg_color="#141414", activate_scrollbars=True)
        self.data_out.pack(fill="x", padx=12, pady=(8, 12))
        self.data_out.insert("end", "（点上面的按钮，命令输出会贴在这里）")
        self.data_out.configure(state="disabled")
        self._busy = ""
        self._q = queue.Queue()
        self.after(150, self.pump_navdata)
        self.refresh_data()

    def pump_navdata(self):
        r"""工作线程只往队列里塞结果，Tk 控件一律在主线程改（跨线程 after() 会报
        "main thread is not in main loop"）。"""
        while True:
            try:
                title, code, text = self._q.get_nowait()
            except queue.Empty:
                break
            self._navdata_done(title, code, text)
        self.after(150, self.pump_navdata)

    def refresh_data(self):
        r"""重算三区的路径/时间/条数 + 两两一致性；文件都在本机，毫秒级。"""
        if not hasattr(self, "data_cards"):
            return
        for card in self.data_cards:
            root = card["root"]
            n, total, latest = dir_stats(root)
            card["time"].configure(text=("最近写入 " + fmt_time(latest)) if latest else "（空）")
            if card["tag"] == "②":
                # 成品 / 编辑中 / 收件箱 各占一行，各算各的数
                self.refresh_dev_rows()
                continue
            maps, files, lines, bins = data_counts(root)
            text = "%d 图 · 路线 %d 个文件/%d 条 · %d 可走面 · %s，共 %d 个文件" % (
                maps, files, lines, bins, human_size(total), n)
            if card["tag"] == "③":
                # 2026-11-21 起 ③ 只当运行环境：数字没意义，直接说清楚
                text = "运行时：dll / ucf_mod.json / markers\\；数据全在 ②，游戏目录不放数据"
            card["info"].configure(text=text)
        try:
            d1, d2 = tree_hashes(NATIVE), tree_hashes(DEV)
        except OSError:
            self.lbl_same.configure(text="一致性：读不动某个数据区")
            return
        n12 = diff_count(d1, d2)
        n_exp = test_stats(DEV)[0]
        st = final_stats()
        n_fin = int(st.get("n") or 0)
        self.lbl_same.configure(
            text=r"一致性（只比每张图的 map.json 与路线 txt，索引与 names.json 不算）："
                 + ("①=②（工作区还没改动）" if n12 == 0 else "① vs ② 有 %d 个文件不同" % n12)
                 + " · 成品 %d 张图（每图一份）" % n_fin
                 + " · " + ("收件箱没有导出" if n_exp == 0
                            else "收件箱有 %d 份导出待整理" % n_exp))

    def refresh_dev_rows(self):
        r"""② 卡拆三块报数（成品 / 编辑中 / 收件箱），各算各的，别再挤成一行：
        以前「9 图」是 maps 里的、「8 可走面」是 vis 里的，看着像同一份数据。"""
        rows = getattr(self, "dev_rows", None)
        if not rows:
            return
        # —— 成品：几张图 / 占多大 / 最近发布（没有版本）——
        st = final_stats()
        n_maps = int(st.get("n") or 0)
        n_bytes, latest = dir_bytes(FINAL_ROOT)
        if n_maps:
            rows["final"].configure(text="%d 张图（每图一份） · %s · 最近发布\u00a0%s" % (
                n_maps, human_size(n_bytes), fmt_short(latest)))
        else:
            rows["final"].configure(
                text="空的（启动成品 = 全原生）· 去「编辑中」选张图 → 发布这张图到成品")

        # —— 编辑中：几张图有草稿 / 占多大 + 地图名 ——
        names = load_packs()
        n_txt = 0
        for pid in names:
            try:
                n_txt += len([fn for fn in os.listdir(pack_dir(pid))
                              if _FINAL_FP_RE.match(fn)])
            except OSError:
                pass
        p_bytes, p_latest = dir_bytes(PACKS)
        if names:
            shown = [self.folder_label(x) if hasattr(self, "folder_label") else x
                     for x in names[:4]]
            if len(names) > len(shown):
                shown.append("等 %d 张" % len(names))
            rows["packs"].configure(text="%d 张图有草稿 · %d 个路线文件 · %s · 最近\u00a0%s\n%s" % (
                len(names), n_txt, human_size(p_bytes), fmt_short(p_latest),
                "、 ".join(shown)))
        else:
            rows["packs"].configure(
                text="没有草稿（「人机路点」页选张图，点「开始编辑这张图」）")

        # —— 收件箱：还躺着几份待整理 / 已归位几份 ——
        n_json, n_bin, _n_packs, t_total, t_latest = test_stats(DEV)
        n_filed = export_filed(DEV)
        if n_json or n_bin:
            rows["vis"].configure(text="待整理 %d 份 · 已归位 %d 份 · %s · 最近\u00a0%s" % (
                n_json, n_filed, human_size(t_total), fmt_short(t_latest)))
        elif n_filed:
            rows["vis"].configure(text="空的 · 已归位 %d 份（在各图文件夹的「导出」里）" % n_filed)
        else:
            rows["vis"].configure(text="空的 · 游戏里按 Ctrl+E 导出会写这里")
