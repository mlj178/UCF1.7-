#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""测试包 / 成品版本：台账、选择、启动、发布、还原、校验。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import json
from tkinter import messagebox
import os
import re
import shutil
import subprocess
import threading
import time
import tkinter as tk

import customtkinter as ctk

from ui.consts import CREATE_NO_WINDOW, FONT, FONT_S
from ui.env import DEV, FINAL_ROOT, HERE, MARKERS, NAVCMD, NAVDATA, ND, P, PACKS
from ui.maps import folder_alias, map_folder, map_scene
from ui.util import _python, game_running


_FINAL_FP_RE = re.compile(r"^n\d+-[0-9a-f]{16}\.txt$", re.I)   # 成品版本里的真图（不含 nogen.txt）

#: 本图编辑标记（<图>\markers.txt）的中文名：顺序就是界面上那一行的顺序
MARKER_LABELS = (("area", "守卫区"), ("nanopos", "守卫点"), ("crouch", "蹲守点"),
                 ("tag", "标签"), ("spawn", "出生点"))


_CMD_SEQ = 0


def prepare_final_root():
    r"""成品开跑前补齐两件事（幂等，每次启动游戏前调一次）：

      1) nogen.txt —— 编辑中的 grow/keep 草稿都带这个文件（空图不自动铺点），成品要一致；
      2) *.txt 设只读 —— 成品不允许游戏内保存（DLL 的 fopen("w") 会失败）。

    一图一夹（2026-11-27）：成品在 <图>\final\<指纹>.txt，没有"一个大 final 目录"了。
    返回成品根（= data\maps，给控制台的 UCF_PACK_DIR 用）；一份成品都没有就返回空串。
    """
    n = 0
    for name in P.folder_names():
        d = P.final_dir(name)
        if not os.path.isdir(d):
            continue
        try:
            ng = os.path.join(d, "nogen.txt")
            if not os.path.isfile(ng):
                with open(ng, "w", encoding="utf-8", newline="\n") as f:
                    f.write("")
            for fn in os.listdir(d):
                if _FINAL_FP_RE.match(fn):
                    os.chmod(os.path.join(d, fn), 0o444)
                    n += 1
        except OSError:
            pass
    return FINAL_ROOT if n else ""


def final_stats():
    r"""成品统计：{n, maps:{指纹:...}, latest}；读不了当空。"""
    try:
        return ND.final_store_stats()
    except Exception:                 # noqa: BLE001
        return {"n": 0, "maps": {}, "latest": ""}


def final_bytes():
    r"""成品占多大 / 最近发布（<图>\final\<指纹>.txt 加起来）。"""
    n = 0
    latest = 0.0
    for name in P.folder_names():
        d = P.final_dir(name)
        try:
            for fn in os.listdir(d):
                if not _FINAL_FP_RE.match(fn):
                    continue
                st = os.stat(os.path.join(d, fn))
                n += st.st_size
                latest = max(latest, st.st_mtime)
        except OSError:
            pass
    return n, latest


def final_versions():
    r"""兼容旧调用：成品最多只有一个“当前”，有图就返回一条，没有就空列表。

    2026-11-24 起界面不再用版本下拉；这个函数只留给还没改完的旧代码/自检。
    """
    st = final_stats()
    if not st.get("n"):
        return []
    return [{"name": "final", "exists": True, "maps": st.get("maps") or {},
             "created": st.get("latest") or "", "updated": st.get("latest") or ""}]


def final_current_name():
    r"""成品有图就返回固定名 final；没有就空串（启动成品 = 全原生）。"""
    try:
        return "final" if final_stats().get("n") else ""
    except Exception:                 # noqa: BLE001
        return ""


def pack_name_ok(name):
    r"""包名只能用英文字母、数字、下划线、短横线（插件是 C + ANSI 路径，中文读不了）。"""
    return bool(re.match(r"^[A-Za-z0-9_-]{1,48}$", name or ""))


def pack_id_ok(pid):
    r"""包 id = 地图文件夹/包名：文件夹允许中文（如 TransportShip运输船），包名仍只认英文。"""
    parts = [s for s in str(pid or "").replace("\\", "/").split("/") if s]
    if not (1 <= len(parts) <= 2):
        return False
    if len(parts) == 1:
        return pack_name_ok(parts[0])            # 老布局：根目录平铺的包名
    folder, name = parts
    if not pack_name_ok(name):
        return False
    return (bool(re.match(r'^[^\\/:*?"<>|]{1,30}$', folder))
            and folder not in (".", ".."))


def pack_dir(pid):
    r"""包 id → 目录：TransportShip/blank_b → packs\TransportShip\blank_b。

    老布局（packs\blank_b，没分类）也认，旧包和自检脚本还能直接用。
    """
    return os.path.join(PACKS, *[s for s in str(pid).replace("\\", "/").split("/") if s])


def _is_pack_dir(path):
    r"""目录里有没有包的内容：manifest.json 或 <指纹>.txt。"""
    if os.path.isfile(os.path.join(path, "manifest.json")):
        return True
    try:
        return any(re.match(r"^n\d+-[0-9a-fA-F]{16}\.txt$", fn)
                   for fn in os.listdir(path))
    except OSError:
        return False


def _is_map_root(path):
    r"""这个目录是不是「一张图的文件夹」：点图 / 可走面 / 标记 / native\ / final\ 有一个就行。

    2026-11-27 一图一夹以后草稿就在图文件夹里。老版本的 load_packs() 只认 manifest.json /
    <指纹>.txt，于是删完草稿的图文件夹会被当成「老布局的图/包」继续往下找，
    把 <图>\final\<指纹>.txt 列成一个叫 final 的草稿（对比表里多一行假的）。
    """
    for fn in ("map.json", "navmesh.bin", "markers.txt"):
        if os.path.isfile(os.path.join(path, fn)):
            return True
    for sub in (P.NATIVE_SUB, P.FINAL_SUB):
        if os.path.isdir(os.path.join(path, sub)):
            return True
    return False


def runtime_fp(lv, fp=""):
  r"""草稿文件 / 插件眼里的指纹：纯面图（没有 map.json）补完点图后是 n0-…（0 个点）。

  2026-11-27：胜利广场 / 死亡擂台 场景里没有 PointGraph，插件现场补一张 0 点的，
  运行期指纹就是 n0-0000000000000000（和飓风危城一样）。控制台这边它们的 map.json
  指纹是空串（不能冒充飓风危城去做 find_map_doc / 成品的按指纹查找），
  只在「写草稿文件名 / 告诉插件 UCF_FP」时换成这个运行期指纹。
  """
  if fp:
    return fp
  return "n0-0000000000000000" if lv else ""


def pack_manifest(pid):
    r"""读 packs/<地图文件夹>/<包名>/manifest.json；没有就返回空 dict。"""
    try:
        with open(os.path.join(pack_dir(pid), "manifest.json"), "r", encoding="utf-8") as f:
            doc = json.load(f)
        return doc if isinstance(doc, dict) else {}
    except (OSError, ValueError):
        return {}


def pack_txt(pid, fp=""):
    r"""包内某张图的 txt；不给指纹就取第一个。"""
    d = pack_dir(pid)
    if fp:
        p = os.path.join(d, fp + ".txt")
        return p if os.path.isfile(p) else ""
    try:
        files = sorted(fn for fn in os.listdir(d) if fn.endswith(".txt") and not fn.startswith("_"))
    except OSError:
        return ""
    return os.path.join(d, files[0]) if files else ""


def pack_target_fp(pid):
    r"""这个包针对哪张图：manifest.fp 优先，其次 <指纹>.txt 的文件名。"""
    fp = str(pack_manifest(pid).get("fp") or "")
    if fp:
        return fp
    p = pack_txt(pid)
    if p:
        base = os.path.basename(p)[:-4]
        if re.match(r"^n\d+-[0-9a-fA-F]{16}$", base):
            return base
    return ""


def pack_summary(pid, fp=""):
    r"""包内容摘要：空白地图(grow) / 原版+新增(keep)？几个加点 / 删点 / 加边 / 删边、最后写入时间。"""
    p = pack_txt(pid, fp)
    out = {"path": p, "grow": False, "keep": False,
           "nadd": 0, "ndel": 0, "eadd": 0, "edel": 0, "mtime": 0.0}
    if not p:
        return out
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for ln in f:
                s = ln.strip()
                if not s or s.startswith("#"):
                    continue
                if s in ("grow", "blank"):
                    out["grow"] = True       # blank 是旧写法：原生点全禁 + AddNode 新建
                elif s == "keep":
                    out["keep"] = True       # 原版基础 + 新增：原生点全保留，只新建节点
                elif s.startswith("node add "):
                    out["nadd"] += 1
                elif s.startswith("node del "):
                    out["ndel"] += 1
                elif s.startswith("edge "):
                    bits = s.split()
                    verb = bits[1] if len(bits) > 1 else ""
                    if verb in ("add", "out", "in"):
                        out["eadd"] += 1
                    elif verb in ("del", "delout", "delin"):
                        out["edel"] += 1
        out["mtime"] = os.stat(p).st_mtime
    except OSError:
        pass
    return out


def write_nav_cmd(cmd, name="", fp="", extra=None):
    r"""给运行中的插件写一条命令（原子替换，插件不会读到半截文件）。

    seq 必须单调递增：同一毫秒点两下也不能被插件当成同一条。
    extra 是附加行（例如 brush=normal / menu=on），插件按 key=value 读。
    """
    global _CMD_SEQ
    ms = int(time.time() * 1000)
    _CMD_SEQ = ms if ms > _CMD_SEQ else (_CMD_SEQ + 1)
    lines = ["seq=%d" % _CMD_SEQ, "cmd=%s" % cmd]
    if name:
        lines.append("pack=%s" % name)
    if fp:
        lines.append("fp=%s" % fp)
    for key, value in (extra or {}).items():
        if value is None or value == "":
            continue
        lines.append("%s=%s" % (key, value))
    d = os.path.dirname(NAVCMD)
    if d:
        os.makedirs(d, exist_ok=True)
    tmp = NAVCMD + ".tmp"
    # 包 id 里可能带中文地图文件夹；插件是 ANSI(GBK) 文件路径，命令文件也按 GBK 写。
    with open(tmp, "w", encoding="gbk", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    os.replace(tmp, NAVCMD)
    return _CMD_SEQ


def load_packs():
    r"""packs\ 下所有测试包 id：地图文件夹/包名（老布局的 packs\<包名> 也算，排后面）。"""
    out = []
    try:
        entries = sorted(os.listdir(PACKS))
    except OSError:
        return out
    for entry in entries:
        if entry.startswith("_"):
            continue
        d = os.path.join(PACKS, entry)
        if not os.path.isdir(d):
            continue
        if _is_pack_dir(d):
            out.append(entry)                      # 老布局：直接放在根目录
            continue
        if _is_map_root(d):
            continue                               # 图文件夹：native\ / final\ 是图数据，不是包
        try:
            subs = sorted(os.listdir(d))
        except OSError:
            continue
        for sub in subs:
            sd = os.path.join(d, sub)
            if sub.startswith("_") or not os.path.isdir(sd):
                continue
            if _is_pack_dir(sd):
                out.append("%s/%s" % (entry, sub))
    return out


def migrate_flat_packs():
    r"""把老的 packs\<包名>\ 自动挪进 packs\<地图文件夹>\<包名>\；返回 [(旧, 新)]。

    文件夹名用地图英文场景名（插件是 C + ANSI 路径，读不了中文目录）。
    目标已存在就原地不动，绝不覆盖。
    """
    moved = []
    try:
        entries = sorted(os.listdir(PACKS))
    except OSError:
        return moved
    for entry in entries:
        d = os.path.join(PACKS, entry)
        if entry.startswith("_") or not os.path.isdir(d) or not _is_pack_dir(d):
            continue
        man = pack_manifest(entry)                # 老布局按平铺名字读
        fp = str(man.get("fp") or "")
        if not fp:
            fp = pack_target_fp(entry)
        folder = map_folder(str(man.get("level") or ""), fp)
        dst = os.path.join(PACKS, folder, entry)
        if os.path.abspath(dst) == os.path.abspath(d) or os.path.isdir(dst):
            continue
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(d, dst)
        except OSError:
            continue
        moved.append((entry, "%s/%s" % (folder, entry)))
    return moved


class PackMixin:
    # ---- 原来三个 .bat 的按钮：后台跑 navdata.py，输出贴回本页 ----
    def run_navdata(self, args, title):
        if getattr(self, "_busy", ""):
            self.set_status("正在执行：%s，等它跑完" % self._busy)
            return
        self._busy = title
        self.data_out.configure(state="normal")
        self.data_out.insert("end", "\n> python navdata.py %s\n" % " ".join(args))
        self.data_out.see("end")
        self.data_out.configure(state="disabled")
        self.set_status("%s …" % title)
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        env.setdefault("UCF_PROFILE", "dev")

        def work():
            try:
                cp = subprocess.run([_python(), NAVDATA] + list(args), cwd=HERE, env=env,
                                    capture_output=True, timeout=300,
                                    creationflags=CREATE_NO_WINDOW)
                text = ((cp.stdout or b"").decode("utf-8", "replace")
                        + (cp.stderr or b"").decode("utf-8", "replace"))
                code = cp.returncode
            except Exception as exc:                       # noqa: BLE001
                text, code = "执行失败：%s" % exc, -1
            self._q.put((title, code, text))

        threading.Thread(target=work, daemon=True).start()

    def _navdata_done(self, title, code, text):
        self._busy = ""
        self.data_out.configure(state="normal")
        self.data_out.insert("end", (text.strip() or "（没有输出）") + "\n")
        self.data_out.see("end")
        self.data_out.configure(state="disabled")
        self.set_status("%s %s" % (title, "完成" if code == 0 else "失败（退出码 %s）" % code))
        self.refresh_data()
        if hasattr(self, "wp_meta"):
            self.refresh_wp_status()
        self.refresh_final_combo()
        self.refresh_compare()
        self.refresh_launch_strip()
        if title == "删除本图草稿" and code == 0:
            # 启动档还停在「编辑中」时这张图已经没草稿了：说清楚，免得以为没生效
            if getattr(self, "pack_on", None) and self.pack_on.get() and not self.draft_exists():
                self.set_status("草稿已删；启动档还是「编辑中」，这张图会走原版。"
                                "要做新的点「开始编辑这张图」。")

    def _guard_game(self, title):
        r"""游戏开着时部署/还原不会报错，但这一局读的还是旧数据 —— 先问一句，别让人以为改完没生效。"""
        if not game_running():
            return True
        return messagebox.askyesno(title, "游戏正在运行：这一局已经读进内存的数据不会变。\n"
                                          "要现在继续吗？（想让它这次生效就先关游戏）", parent=self)

    def ask_publish(self):
        r"""发布确认：只发布当前地图，成品里同图那份会被覆盖。取消返回 False。"""
        lv, lab, fp = self.current_map() if hasattr(self, "opt_map") else ("", "", "")
        folder = self.current_folder() if hasattr(self, "opt_map") else ""
        if not folder or not fp:
            return False
        if self.draft_exists():
            nd, ed = self.draft_counts()
            head = "把「%s」的草稿发布到成品？\n\n草稿：%d 点 / %d 边" % (lab or lv, nd, ed)
        else:
            return False
        if ND.final_store_has(fp):
            head += "\n成品里已有这张图的一份，会被覆盖；旧文件自动留 1 份快照。"
        else:
            head += "\n成品里还没有这张图，这是第一次发布。"
        head += "\n\n发布后，启动「成品」就会加载它。继续？"
        return messagebox.askyesno("发布这张图到成品", head, parent=self)

    def do_promote(self):
        r"""编辑中 -> 成品：覆盖 final\<指纹>.txt（和编辑中同一套加载逻辑）。

        不再新建版本、不再整套复制；旧成品由 navdata.py 自动留快照。
        """
        folder = self.current_folder() if hasattr(self, "opt_map") else ""
        if not folder:
            self.set_status("先在「编辑中」页选一张图")
            return
        if not self.current_map()[2]:
            self.set_status("纯面图只能停在「编辑中」：成品档按指纹找文件，"
                            "飓风危城 / 胜利广场 / 死亡擂台 三张 0 点图指纹都是 n0-…，会互相覆盖")
            return
        if not self.draft_exists():
            self.set_status("这张图还没有草稿：先点「开始编辑这张图」")
            return
        if not self._guard_game("发布到成品"):
            return
        if not self.ask_publish():
            return
        self.run_navdata(["pack", "promote", folder], "发布到成品")

    def do_restore(self):
        if not self._guard_game("从备份还原"):
            return
        if not messagebox.askyesno("从备份还原",
                                   "② 开发版会被 ① 备份版覆盖：\n成品里的改动和测试包都会丢掉。\n\n继续？",
                                   parent=self):
            return
        self.run_navdata(["restore"], "从备份还原")

    def do_verify(self):
        self.run_navdata(["verify"], "校验备份版")

    # ---- 测试包：取值 / 切换（UI 在「人机路点」① 选图与数据）----
    def ensure_pack_folders(self):
        r"""packs\ 下按地图建文件夹：序号_英文场景名中文名（如 01_TransportShip运输船）。

        老文件夹（没序号、纯英文、旧中文名之外的同名写法）按「去掉序号后同名」认出来，
        改名合并到新名字，里面的包跟着走；每张图最后一定有一个带序号的文件夹。
        """
        want = {}

        def accept(lv, fp=""):
            new = map_folder(lv, fp)
            want[folder_alias(new)] = new
            want[folder_alias(map_scene(lv, fp))] = new
            want[str(lv)] = new              # 更早的命名：直接叫 level1 / level9

        for lv, _lab, fp in self.maps:
            accept(lv, fp)
        for lv, _row in self.wp_scene.items():
            accept(lv)
        try:
            existing = [d for d in os.listdir(PACKS) if os.path.isdir(os.path.join(PACKS, d))]
        except OSError:
            existing = []
        for name in existing:
            new = want.get(folder_alias(name))
            if not new or new == name:
                continue
            oldp, newp = os.path.join(PACKS, name), os.path.join(PACKS, new)
            try:
                if not os.path.isdir(newp):
                    os.rename(oldp, newp)
                else:                          # 两边都在：把包挪过去，不覆盖同名
                    for sub in os.listdir(oldp):
                        src = os.path.join(oldp, sub)
                        dst = os.path.join(newp, sub)
                        if os.path.isdir(src) and not os.path.exists(dst):
                            shutil.move(src, dst)
                    try:
                        os.rmdir(oldp)
                    except OSError:
                        pass
            except OSError:
                pass
        for new in sorted(set(want.values())):
            try:
                os.makedirs(os.path.join(PACKS, new), exist_ok=True)
            except OSError:
                pass

    def folder_label(self, folder):
        r"""地图文件夹 → 界面上显示的中文名（兼容没序号 / 纯英文的旧文件夹）。"""
        key = folder_alias(folder)
        for lv, lab, fp in self.maps:
            if key in (folder_alias(map_folder(lv, fp)), folder_alias(map_scene(lv, fp))):
                return lab
        for lv, row in self.wp_scene.items():
            if key in (folder_alias(map_folder(lv)), folder_alias(map_scene(lv))):
                return str(row.get("name") or folder)
        return folder

    # ---- 单草稿模型：当前地图 -> 唯一草稿目录 ----------------------------
    def current_map(self):
        r"""下拉框当前地图 -> (level, 中文名, 指纹)；没选返回空三元组。"""
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        return self.map_disp.get(disp, ("", "", ""))

    def current_folder(self):
        r"""当前地图对应的 packs\ 一级目录名（01_TransportShip运输船）。"""
        lv, _lab, fp = self.current_map()
        return map_folder(lv, fp) if lv else ""

    def draft_dir(self):
        folder = self.current_folder()
        return pack_dir(folder) if folder else ""

    def draft_exists(self):
        d = self.draft_dir()
        if not d or not os.path.isdir(d):
            return False
        if os.path.isfile(os.path.join(d, "manifest.json")):
            return True
        try:
            return any(_FINAL_FP_RE.match(fn) for fn in os.listdir(d))
        except OSError:
            return False

    def draft_manifest(self):
        return pack_manifest(self.current_folder()) if self.current_folder() else {}

    def draft_counts(self):
        r"""当前草稿的 (node add 数, edge add 数)；没有草稿就是 (0, 0)。"""
        folder = self.current_folder()
        if not folder or not self.draft_exists():
            return 0, 0
        fp = pack_target_fp(folder)
        p = pack_txt(folder, fp)
        if not p:
            return 0, 0
        summ = pack_summary(folder, fp)
        return summ.get("nadd", 0) + summ.get("ndel", 0), summ.get("eadd", 0) + summ.get("edel", 0)

    # ---- 本图编辑标记（守卫区 / 守卫点 / 蹲守点 / 标签 / 出生点）--------------------
    # 2026-11-25 用户问「守卫区怎么删了还在」：这些标记根本不在草稿 txt 里 ——
    # 草稿只装路点/边/跳跃；标记由插件每次进图重放 markers\<图>\markers.txt。
    def marker_path(self):
        r"""当前地图的编辑标记文件：② data\navdata\dev\markers\<地图文件夹>\markers.txt。"""
        folder = self.current_folder() if hasattr(self, "opt_map") else ""
        return os.path.join(MARKERS, folder, "markers.txt") if folder else ""

    def marker_counts(self):
        r"""当前图标记条数 {area/nanopos/crouch/tag/spawn: n}；没文件全 0。"""
        counts = {k: 0 for k, _lab in MARKER_LABELS}
        p = self.marker_path()
        if not p:
            return counts
        try:
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    s = line.strip()
                    if not s or s.startswith("#"):
                        continue
                    kind = s.split()[0]
                    if kind == "spawndel":
                        counts["spawn"] += 1      # 删原生出生点也是一条改动
                    elif kind in counts:
                        counts[kind] += 1
        except OSError:
            pass
        return counts

    def marker_summary(self, counts=None, max_items=2):
        r"""「守卫区 9 · 守卫点 2」——只列非 0 的；类型多时收成「等 N 项」，别把按钮挤掉。"""
        c = counts if counts is not None else self.marker_counts()
        items = [(lab, c[k]) for k, lab in MARKER_LABELS if c.get(k)]
        bits = ["%s %d" % (lab, n) for lab, n in items[:max_items]]
        if len(items) > max_items:
            bits.append("等 %d 项" % len(items))
        return " · ".join(bits)

    def clear_markers(self, ask=True):
        r"""清空当前图的编辑标记：markers.txt 挪到 ② archive\markers_trash\<图>__<时间>\。

        不真删（和删草稿一个思路），误清能从 archive 挪回来。
        ask=False 给「删除本图草稿」复用（那边已经确认过了，不再二次弹框）。
        返回 True = 真的挪走了；False = 没动。
        """
        folder = self.current_folder() if hasattr(self, "opt_map") else ""
        p = self.marker_path()
        if not folder or not p or not os.path.isfile(p):
            if ask:
                self.set_status("这张图没有编辑标记（守卫区 / 守卫点 / 蹲守点 / 标签）")
            return False
        counts = self.marker_counts()
        summary = self.marker_summary(counts) or "（文件里没有有效条目）"
        if ask and not self._guard_game("清空本图标记"):
            return False
        if ask and not self.confirm_danger(
                "清空本图标记",
                ["「%s」的编辑标记整份清掉。" % (self.folder_label(folder) or folder),
                 "",
                 "现有：" + summary,
                 "文件：markers\\%s\\markers.txt" % folder.replace("/", "\\"),
                 "",
                 "守卫区 / 守卫点 / 蹲守点 / 标签 / 出生点 都存在 markers\\，不在草稿里；",
                 "所以删草稿不会带走它们。标记按图存、不分档：清空后成品档和原版也一起没有。",
                 "文件先挪到 archive\\markers_trash\\，误清可以挪回来。",
                 "",
                 "游戏开着时，重进图或按 Ctrl+7 才按新文件重放。"],
                ok_text="清空标记"):
            return False
        dst_dir = os.path.join(P.ARCHIVE, "markers_trash",
                               "%s__%s" % (folder, time.strftime("%Y%m%d_%H%M%S")))
        try:
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(p, os.path.join(dst_dir, "markers.txt"))
        except OSError as exc:
            self.set_status("清空标记失败：%s" % exc)
            return False
        self.refresh_draft_panel()
        self.set_status("已清空本图标记（%s）：文件在 archive\\markers_trash\\；重进图生效" % summary)
        return True

    def resolve_pack_id(self, pid):
        r"""老配置里存的是平铺包名：按尾名找回分类后的 id（地图文件夹/包名）。"""
        pid = str(pid or "").replace("\\", "/").strip("/")
        if not pid:
            return ""
        if os.path.isdir(pack_dir(pid)):
            return pid
        tail = pid.split("/")[-1]
        for x in load_packs():
            if x.split("/")[-1] == tail:
                return x
        return ""

    def disp_of(self, pid):
        for disp, x in getattr(self, "pack_disp", {}).items():
            if x == pid:
                return disp
        return ""

    def _pack_values(self):
        r"""下拉框：按地图分组排列，显示成「运输船 · blank_b」。"""
        ids = load_packs()
        self.pack_disp = {}
        order = {lv: i for i, (lv, _l, _f) in enumerate(self.maps)}

        def sort_key(pid):
            lv = str(pack_manifest(pid).get("level") or "")
            return (order.get(lv, 99), pid)

        vals = []
        for pid in sorted(ids, key=sort_key):
            folder, _sep, name = pid.rpartition("/")
            lab = self.folder_label(folder) if folder else "未分类"
            disp = "%s · %s" % (lab, name)
            while disp in self.pack_disp:      # 同名包极少见，重了就加空格区分
                disp += " "
            self.pack_disp[disp] = pid
            vals.append(disp)
        return vals or ["（还没有测试包）"]

    def pack_dict(self):
        """当前选择 → 写回 ucf_mod.json 的 pack 段（只给控制台自己用，插件不读它）。"""
        lv, lab, fp = self.current_map() if hasattr(self, "opt_map") else ("", "", "")
        folder = self.current_folder() if hasattr(self, "opt_map") else ""
        if lv and not fp:
            # 纯面图（胜利广场 / 死亡擂台）：场景里没有 PointGraph，插件进图会现场补一张
            # （0 节点），再按 grow 套草稿。有草稿才带 UCF_PACK；指纹是运行期的 n0-…。
            name = folder if (folder and self.draft_exists()) else ""
            return {"on": bool(self.pack_on.get()) if hasattr(self, "pack_on") else False,
                    "name": name, "map": lv, "label": lab,
                    "fp": runtime_fp(lv, fp) if name else "",
                    "face": True, "only_map": True}
        name = folder if (folder and self.draft_exists()) else ""
        return {
            "on": bool(self.pack_on.get()) if hasattr(self, "pack_on") else False,
            "name": name,
            "map": lv, "label": lab, "fp": fp,
            "only_map": True,
        }

    def pack_manifest_map(self, pid):
        """包对应的地图（manifest.json 的 level）；没有 manifest 就按文件夹名反查。"""
        lv = str(pack_manifest(pid).get("level") or "")
        if lv:
            return lv
        folder = folder_alias(str(pid).replace("\\", "/").split("/")[0])
        for lvl, _lab, fp in self.maps:
            if folder in (folder_alias(map_folder(lvl, fp)), folder_alias(map_scene(lvl, fp))):
                return lvl
        return ""

    def on_pack_change(self, persist=True):
        r"""地图 / 启动档变了：只刷新状态，不再有“选哪个包”这一步。"""
        on = self.seg_mode.get().startswith("编辑中") if hasattr(self, "seg_mode") else False
        if hasattr(self, "pack_on"):
            self.pack_on.set(on)
        folder = self.current_folder() if hasattr(self, "opt_map") else ""
        self._last_pack = folder
        self.pack_name = folder if (on and self.draft_exists()) else ""
        try:
            if hasattr(self, "opt_map"):
                self.opt_map.configure(state="normal")
        except Exception:                 # noqa: BLE001
            pass
        if persist:
            self.persist("编辑状态")
        self.refresh_launch_strip()
        self.refresh_wp_status()
        if hasattr(self, "lbl_final"):
            self.refresh_final_combo()
        self.update_mode_hint()
        self.refresh_compare()
        if hasattr(self, "rec_pre"):
            self.refresh_rec_ready()

    def start_or_open_draft(self):
        r"""有草稿就打开目录；没有就弹「开始编辑这张图」。"""
        if self.draft_exists():
            self.open_packs_dir()
        else:
            self.create_pack()

    def open_packs_dir(self):
        try:
            d = self.draft_dir() if self.draft_exists() else PACKS
            os.makedirs(d, exist_ok=True)
            os.startfile(d)          # noqa: SLF001  Windows 资源管理器
        except OSError as exc:
            self.set_status("打不开草稿目录：%s" % exc)

    # ---- 控制台 → 运行中插件：载入 / 重读 / 保存 / 回正式版 ----
    def selected_pack(self):
        r"""当前地图的草稿目录名（01_TransportShip运输船）；没有草稿返回空串。"""
        folder = self.current_folder() if hasattr(self, "opt_map") else ""
        return folder if (folder and self.draft_exists()) else ""

    def selected_fp(self):
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        return self.map_disp.get(disp, ("", "", ""))[2]

    def send_pack_cmd(self, cmd):
        r"""把「载入 / 重新应用 / 保存」写进 ucf_navcmd.txt，插件 0.5 s 内执行。"""
        name = self.selected_pack()
        if not name:
            self.set_status("先选一个测试包（或点「新建测试包」）")
            return
        if not pack_id_ok(name):
            self.set_status("包名只能用英文字母、数字、下划线（_）和短横线（-）：%s" % name)
            return
        fp = pack_target_fp(name) or self.selected_fp()
        try:
            seq = write_nav_cmd(cmd, name, fp)
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.persist("测试包")
        running = game_running()
        act = {"apply": "载入", "reload": "重新应用", "save": "保存"}.get(cmd, cmd)
        short = self.folder_label(name) if hasattr(self, "folder_label") else name
        if running:
            self.set_status("已发送 #%d：%s %s；游戏日志看 navcmd / naved" % (seq, act, short))
        else:
            self.set_status("游戏没开：已选中 %s，点「开始游戏」生效" % short)

    def clear_pack_map(self):
        name = self.current_folder() if hasattr(self, "opt_map") else ""
        if not name or not self.draft_exists():
            self.set_status("这张图还没有草稿")
            return
        fp = pack_target_fp(name) or self.selected_fp()
        if not fp:
            self.set_status("不知道这张图的指纹：先选一张地图")
            return
        if not messagebox.askyesno(
                "重置本图草稿",
                "把 %s 的草稿清成%s？\n"
                "只重写 packs\\%s\\%s.txt，成品不动。"
                % (self.folder_label(name) if hasattr(self, "folder_label") else name, fp,
                   "「原版基础 + 新增」（原生点原样保留，只清掉你加的点）"
                   if (pack_manifest(name).get("keep")
                       or pack_summary(name, fp)["keep"]) else "「空白地图」",
                   name.replace("/", "\\"), fp),
                parent=self):
            return
        pdir = pack_dir(name)
        txt = os.path.join(pdir, fp + ".txt")
        summ = pack_summary(name, fp)
        keep_native = bool(pack_manifest(name).get("keep") or summ["keep"])
        try:
            os.makedirs(pdir, exist_ok=True)
            with open(txt, "w", encoding="utf-8", newline="\n") as f:
                if keep_native:
                    # keep 包：原生点原样保留，清掉的只是你加的点
                    f.write("# ucf-navedit v1 fp=%s\nkeep\n" % fp)
                else:
                    f.write("# ucf-navedit v1 fp=%s\ngrow\n" % fp)
            with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
                f.write("")
            man = pack_manifest(name)
            man.setdefault("name", "%s_%s" % (map_scene(self.current_map()[0], fp),
                                              time.strftime("%Y%m%d")))
            man.setdefault("folder", name)
            man.setdefault("fp", fp)
            if "level" not in man:
                man["level"] = self.map_disp.get(self.opt_map.get(), ("", "", ""))[0]
            man["grow"] = not keep_native
            man["keep"] = keep_native
            man.pop("blank", None)
            man.pop("seed", None)
            man["cleared"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8",
                      newline="\n") as f:
                json.dump(man, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except OSError as exc:
            self.set_status("清空失败：%s" % exc)
            return
        self.send_pack_cmd("apply")
        self.set_status("已清空 %s / %s：进图后从 0 画（Ctrl+Shift+N 加点）" % (name, fp))

    def delete_draft(self):
        r"""删掉当前地图的草稿 —— 只搬 manifest / <指纹>.txt / nogen.txt，图数据原地不动。

        重置 = 留着草稿、把点/边清成 0（下次接着画）；
        删除 = 这张图回到「还没有草稿」，地图本身还在（下拉里选得到），要重做得重新「开始编辑这张图」。
        **不能整份目录搬**：一图一夹之后 map.json / navmesh.bin / native\ / final\ 都在同一个目录里。
        草稿之外还有 markers\ 里的守卫区 / 守卫点 / 蹲守点 / 标签 / 出生点：默认连草稿一起清
        （弹窗里的勾选框，默认勾上；取消勾选就只删草稿、留着标记）。
        两样都不真删：草稿挪 archive\pack_trash\，标记挪 archive\markers_trash\，误删都能挪回。
        成品 final\<指纹>.txt 不动（要撤发布去「成品」页）。
        """
        if not hasattr(self, "opt_map"):
            return
        lv, lab, _fp = self.current_map()
        folder = self.current_folder()
        where = lab or lv or folder
        if not folder or not self.draft_exists():
            self.set_status("这张图还没有草稿，没有可删的（「重置本图草稿」只清空已有的草稿）")
            return
        if not self._guard_game("删除本图草稿"):
            return
        man = self.draft_manifest()
        nd, ed = self.draft_counts()
        mode = ("空白地图" if (man.get("grow") or man.get("blank")) else
                "原版 + 新增" if man.get("keep") else "增量")
        lines = ["「%s」这张图的草稿删掉（点图、可走面、成品、标记都留着）。" % where,
                 "",
                 "草稿：%d 点 / %d 边 · %s · 创建于 %s" % (
                     nd, ed, mode, (man.get("created") or "-")[:16]),
                 "目录：packs\\%s\\" % folder.replace("/", "\\"),
                 "",
                 "删完这张图回到「还没有草稿」，要重做点「开始编辑这张图」。",
                 "成品里已发布的那份不动（要撤发布去「成品」页）。",
                 "只搬草稿三件（manifest.json / nogen.txt / <指纹>.txt）到 archive\\pack_trash\\；",
                 "map.json / 可走面 / 本图标记原地不动，误删可以挪回来。"]
        counts = self.marker_counts()
        has_markers = any(counts.values())
        marker_summary = self.marker_summary(counts) if has_markers else ""
        extra = {"checked": has_markers}
        if has_markers:
            # 守卫区/蹲守点等不在草稿里：默认一起清，用户要的就是「删干净」
            lines += ["",
                      "本图标记：%s（守卫区 / 守卫点 / 蹲守点 / 标签 / 出生点）" % marker_summary,
                      "它们在 markers\\<图>\\markers.txt，不在草稿里 —— 不清的话，新建空白草稿进图还会看到。"]
        # 自定义确认框：× / Esc / 取消 一律当「否」（askyesno 在 Windows 上关窗会返回「是」）
        if not self.confirm_danger(
                "删除本图草稿", lines, ok_text="删除草稿",
                checkbox_text=("同时清空本图标记（%s）" % marker_summary) if has_markers else "",
                checkbox_checked=True, out=extra):
            return
        if has_markers and extra.get("checked"):
            if not self.clear_markers(ask=False):
                # 标记挪不走就停手：不然草稿没了、旧标记还挂着，比现在更乱
                self.set_status("本图标记没清掉，草稿没删：先关掉游戏再试一次" )
                return
        self.run_navdata(["pack", "rm", folder], "删除本图草稿")

    def default_pack_name(self, lv, fp):
        r"""测试包默认名：地图英文场景名 + 当前日期时间，如 TransportShip_20261119_213512。

        插件是 C + ANSI 路径，包里不能有中文，所以用场景名（《地图对照表》里那一列）；
        中文名照旧写进 manifest 的 label，界面上显示的仍是中文。
        """
        base = map_scene(lv, fp)
        stamp = time.strftime("%Y%m%d_%H%M%S")
        return "%s_%s" % (base[:48 - len(stamp) - 1], stamp)

    def ask_pack_name(self, lab, lv, fp):
        r"""新建空白包的名字弹窗；点「创建」返回包名，取消返回空串。"""
        default = self.default_pack_name(lv, fp)
        top = ctk.CTkToplevel(self)
        top.title("新建测试包")
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)   # 控制台置顶时别把弹窗藏到后面

        def grab():
            try:
                if top.winfo_exists():
                    top.grab_set()
            except tk.TclError:
                pass

        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, grab)
        top.bind("<Escape>", lambda _e: top.destroy())

        out = {"name": "", "grow": True, "keep": False}

        ctk.CTkLabel(top, text="新建测试包", font=("Microsoft YaHei UI", 17, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 0))
        ctk.CTkLabel(
            top,
            text="两种建法：空白地图 = 原生路点全禁用、从 0 画；"
                 "原版基础 + 新增 = 原版路线照常走，只加你的点。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=460).pack(fill="x", padx=18, pady=(4, 10))

        # 两种建法：grow（空白地图） / keep（原版基础 + 新增）
        mode = {"keep": False}
        ctk.CTkLabel(top, text="新建方式", font=FONT_S, text_color="#9aa0a6",
                     anchor="w").pack(fill="x", padx=20, pady=(2, 4))
        seg = ctk.CTkSegmentedButton(
            top, values=["空白地图（新建节点）", "原版基础 + 新增"],
            font=FONT_S, height=32)
        seg.set("空白地图（新建节点）")
        seg.pack(fill="x", padx=18)
        mode_hint = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6",
                                 anchor="w", justify="left", wraplength=460)
        mode_hint.pack(fill="x", padx=20, pady=(4, 10))

        grid = ctk.CTkFrame(top, fg_color="transparent")
        grid.pack(fill="x", padx=14)
        cells = [("地图", "%s（%s）" % (lab, lv)), ("建好后的效果", "空白地图 · 从 0 画路线")]
        effect_lbl = [None]
        for i, (k, v) in enumerate(cells):
            cell = ctk.CTkFrame(grid, corner_radius=7, fg_color="#262626",
                                border_width=1, border_color="#383838")
            cell.grid(row=0, column=i, sticky="nsew", padx=4, pady=4)
            ctk.CTkLabel(cell, text=k, font=FONT_S, text_color="#9aa0a6",
                         anchor="w").pack(fill="x", padx=10, pady=(6, 0))
            lbl = ctk.CTkLabel(cell, text=v, font=("Microsoft YaHei UI", 13, "bold"),
                               anchor="w")
            lbl.pack(fill="x", padx=10, pady=(0, 6))
            if k == "建好后的效果":
                effect_lbl[0] = lbl
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)

        def on_mode(_v=None):
            keep = str(seg.get()).startswith("原版")
            mode["keep"] = keep
            if keep:
                text = ("原版基础 + 新增：原生路点一个都不动，原版路线照常能走；"
                        "你加的点按 PointGraph.AddNode 新建，数量不限。")
            else:
                text = ("空白地图：进图后原生路点全部禁用、自动铺点也一起关掉，"
                        "人机只走你画的路线；新点按 PointGraph.AddNode 新建，数量不限"
                        "（同一张图只建一次，大改点集要重进图）。")
            mode_hint.configure(text=text)
            if effect_lbl[0] is not None:
                effect_lbl[0].configure(
                    text=("原版路线 + 你加的点" if keep else "空白地图 · 从 0 画路线"))

        seg.configure(command=on_mode)
        on_mode()

        ctk.CTkLabel(top, text="包名", font=FONT_S, text_color="#9aa0a6",
                     anchor="w").pack(fill="x", padx=20, pady=(12, 2))
        var = tk.StringVar(value=default)
        entry = ctk.CTkEntry(top, textvariable=var, font=FONT, height=38,
                             placeholder_text="给这个包起个名字")
        entry.pack(fill="x", padx=18)
        hint = ctk.CTkLabel(top, text="", font=FONT_S, anchor="w",
                            justify="left", wraplength=460)
        hint.pack(fill="x", padx=20, pady=(4, 0))
        path = ctk.CTkLabel(top, text="", font=("Consolas", 11),
                            text_color="#6f767d", anchor="w")
        path.pack(fill="x", padx=20, pady=(2, 0))
        folder_dir = map_folder(lv, fp)

        def refresh(*_a):
            name = var.get().strip()
            if not name:
                msg, color = "还没起名", "#9aa0a6"
            elif not pack_name_ok(name):
                msg, color = "名字里只能用英文字母、数字、下划线（_）和短横线（-）", "#ff8f8f"
            elif os.path.isdir(os.path.join(folder_dir, name)):
                msg, color = "已有同名测试包：创建会覆盖这张图的旧路线", "#ffc46b"
            else:
                msg, color = "名字可以用", "#69db7c"
            hint.configure(text=msg, text_color=color)
            path.configure(text="保存到  packs\\%s\\%s\\" % (folder_dir, name or "…"))

        var.trace_add("write", refresh)
        refresh()

        def ok(_e=None):
            name = var.get().strip()
            if not pack_name_ok(name):
                refresh()
                entry.focus_set()
                self.bell()
                return
            out["name"] = name
            out["grow"] = True
            out["keep"] = bool(mode["keep"])
            top.destroy()

        btns = ctk.CTkFrame(top, fg_color="transparent")
        btns.pack(fill="x", padx=18, pady=(12, 16))
        ctk.CTkButton(btns, text="创建测试包", width=112, height=34, font=FONT,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=ok).pack(side="right")
        ctk.CTkButton(btns, text="取消", width=76, height=34, font=FONT_S,
                      fg_color="transparent", border_width=1, border_color="#4a4a4a",
                      hover_color="#2e2e2e", command=top.destroy).pack(
            side="right", padx=(0, 8))

        entry.bind("<Return>", ok)
        entry.bind("<KP_Enter>", ok)
        top.update_idletasks()
        w = max(520, top.winfo_reqwidth())
        h = top.winfo_reqheight()
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        top.geometry("%dx%d+%d+%d" % (w, h, max(x, 0), max(y, 0)))
        entry.select_range(0, "end")
        entry.focus_set()
        self.wait_window(top)
        return dict(out)

    def create_pack(self):
        r"""给当前地图建唯一草稿：从成品继续 / 空白地图（grow）/ 原版基础 + 新增（keep）。

        一张图只有一个草稿；已有草稿就直接打开目录，不再建第二个。
        """
        lv, lab, fp = self.current_map() if hasattr(self, "opt_map") else ("", "", "")
        if not lv:
            self.set_status("先选一张图，再点「开始编辑这张图」")
            return
        face = not fp
        if face:
            # 纯面图：插件进图会现场补一张 0 节点的 PointGraph（没有就没法 AddNode），
            # 草稿文件名 / manifest 用运行期指纹 n0-…。grow 时插件还会把可走面摘掉。
            fp = runtime_fp(lv, fp)
        folder = map_folder(lv, fp)
        if self.draft_exists():
            self.set_status("这张图已经有草稿：%s" % folder)
            self.open_packs_dir()
            return
        has_final = ND.final_store_has(fp)
        choices = (["从成品继续改（推荐）"] if has_final else []) + [
            "空白地图（新建节点）", "原版基础 + 新增"]
        out = {"mode": choices[0] if choices else "", "go": False}
        top = ctk.CTkToplevel(self)
        top.title("开始编辑这张图")
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)
        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, lambda: top.winfo_exists() and top.grab_set())
        top.bind("<Escape>", lambda _e: top.destroy())

        ctk.CTkLabel(top, text="开始编辑  %s" % (lab or lv),
                     font=("Microsoft YaHei UI", 17, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 0))
        ctk.CTkLabel(top, text=("成品里已有这张图（%d 点），推荐复制过来接着改；"
                                "也可以从空白地图或原版基础重画。" % (
                                    ND.final_store_meta().get(fp, {}).get("node", 0)))
                 if has_final else
                 "成品里还没有这张图：选一种底图开始画，做完再发布。",
                 font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                 wraplength=470).pack(fill="x", padx=18, pady=(4, 10))

        seg = ctk.CTkSegmentedButton(top, values=choices, font=FONT_S, height=32)
        seg.set(choices[0])
        seg.pack(fill="x", padx=18)
        hint = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6",
                            anchor="w", justify="left", wraplength=460)
        hint.pack(fill="x", padx=20, pady=(4, 10))

        def on_mode(_v=None):
            now = str(seg.get())
            if now.startswith("从成品"):
                text = "成品那一份原样复制成草稿；改完发布就是覆盖回成品。"
            elif now.startswith("空白"):
                text = ("空白地图：原生点全部禁用、自动铺点关闭，只走你画的路线；"
                        "新点按 AddNode 新建，数量不限。")
            else:
                text = ("原版基础 + 新增：原生点一个都不动，原版路线照常走；"
                        "只把新点按 AddNode 追加到原图上。")
            hint.configure(text=text)
            out["mode"] = now

        seg.configure(command=on_mode)
        on_mode()

        bar = ctk.CTkFrame(top, fg_color="transparent")
        bar.pack(fill="x", padx=18, pady=(12, 16))
        ctk.CTkButton(bar, text="取消", width=76, height=34, font=FONT_S,
                      fg_color="transparent", border_width=1, border_color="#4a4a4a",
                      hover_color="#2e2e2e", command=top.destroy).pack(side="right")
        def go():
            out["go"] = True
            top.destroy()

        ctk.CTkButton(bar, text="开始编辑", width=110, height=34, font=FONT,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=go).pack(side="right", padx=(0, 8))
        top.update_idletasks()
        w = max(520, top.winfo_reqwidth())
        h = top.winfo_reqheight()
        x = self.winfo_rootx() + (self.winfo_width() - w) // 2
        y = self.winfo_rooty() + (self.winfo_height() - h) // 2
        top.geometry("%dx%d+%d+%d" % (w, h, max(x, 0), max(y, 0)))
        self.wait_window(top)

        if not out["go"]:
            return
        mode = out["mode"]
        if not mode:
            return
        pdir = pack_dir(folder)
        tpath = os.path.join(pdir, fp + ".txt")
        keep = mode.startswith("原版")
        grow = mode.startswith("空白")
        try:
            os.makedirs(pdir, exist_ok=True)
            if mode.startswith("从成品"):
                shutil.copyfile(ND.final_store_map(fp), tpath)
            elif keep:
                with open(tpath, "w", encoding="utf-8", newline="\n") as f:
                    f.write("# ucf-navedit v1 fp=%s\n# keep: 原生点原样保留，只新增节点\nkeep\n" % fp)
            else:
                with open(tpath, "w", encoding="utf-8", newline="\n") as f:
                    f.write("# ucf-navedit v1 fp=%s\ngrow\n" % fp)
            with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
                f.write("")                       # 存在即关掉自动铺点
            now = time.strftime("%Y-%m-%d %H:%M:%S")
            summ = pack_summary(folder, fp)
            man = {
                "name": "%s_%s" % ((lab or lv) if face else map_scene(lv, fp),
                                    time.strftime("%Y%m%d")),
                "folder": folder, "level": lv, "label": lab, "fp": fp,
                "created": now, "updated": now,
                "source": ("copy-final" if mode.startswith("从成品") else
                           "console-keep" if keep else
                           "console-grow-face" if face else "console-grow"),
                "grow": bool(grow or summ["grow"]),
                "keep": bool(keep or summ["keep"]),
                "note": ("grow 草稿（空白地图）：原生点全禁用 + 新点按 AddNode 新建"
                         if not keep and not mode.startswith("从成品") else
                         "keep 草稿：原生点原样保留 + 新点按 AddNode 新建"
                         if keep else "草稿：复制成品后继续改"),
            }
            with open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8",
                      newline="\n") as f:
                json.dump(man, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except OSError as exc:
            self.set_status("建草稿失败：%s" % exc)
            return
        self.seg_mode.set("编辑中（packs·可写）")
        self.pack_on.set(True)
        self.on_pack_change()
        msg = "已建草稿 %s（%s · %s）" % (man["name"], lab, folder)
        if game_running():
            try:
                write_nav_cmd("apply", folder, fp)
                msg += "，已发送到运行中的游戏"
            except OSError:
                pass
        self.set_status(msg)

    # ---- 成品（每张图一份，没有版本下拉）----------------------------------
    def final_selected(self):
        r"""兼容旧调用：成品有图就返回固定名 final，否则空串。"""
        return final_current_name()

    def refresh_final_combo(self):
        r"""刷新成品状态行/按钮（不再有版本下拉）。"""
        st = final_stats()
        meta = st.get("maps") or {}
        if hasattr(self, "lbl_final"):
            if not meta:
                self.lbl_final.configure(
                    text="成品里还没有图：去「编辑中」选一张图，点「发布这张图到成品」。",
                    text_color="#f59f00")
            else:
                lv, lab, fp = self.current_map() if hasattr(self, "opt_map") else ("", "", "")
                cur = meta.get(fp) if fp else None
                if cur:
                    text = ("本图已发布：%s · %s · %d 点 / %d 边 · %s · sha %s" % (
                        lv, lab, cur.get("node", 0), cur.get("edge", 0),
                        (cur.get("published") or cur.get("mtime") or "-")[:16],
                        (cur.get("sha256") or "")[:8]))
                else:
                    text = "本图还没发布；成品里已有 %d 张图，最近发布 %s" % (
                        len(meta), (st.get("latest") or "-")[:16])
                self.lbl_final.configure(text=text, text_color="#8ab4f8")
        btn = getattr(self, "btn_revoke_final", None)
        if btn is not None:
            lv, _lab, fp = self.current_map() if hasattr(self, "opt_map") else ("", "", "")
            try:
                btn.configure(state="normal" if (fp and ND.final_store_has(fp)) else "disabled")
            except Exception:                 # noqa: BLE001
                pass
        if hasattr(self, "lbl_final_all"):
            if meta:
                names = []
                for _fp, m in sorted(meta.items(), key=lambda kv: (
                        str(kv[1].get("level") or ""), kv[0])):
                    names.append(m.get("label") or m.get("level") or _fp)
                self.lbl_final_all.configure(
                    text="已发布 %d 张：%s" % (len(meta), "、".join(names)),
                    text_color="#8a8f96")
            else:
                self.lbl_final_all.configure(text="成品为空：启动成品时所有图走原生。",
                                             text_color="#f59f00")
        self.update_mode_hint()
        self.refresh_game_button()

    def on_final_change(self):
        self.refresh_final_combo()
        self.refresh_wp_status()
        self.refresh_compare()

    def open_final_dir(self):
        d = FINAL_ROOT
        try:
            os.makedirs(d, exist_ok=True)
        except OSError:
            pass
        try:
            os.startfile(d)                    # noqa: S606  Windows 专用
        except OSError as exc:
            self.set_status("打不开目录：%s" % exc)

    def revoke_final(self):
        r"""撤销当前地图的发布：真删 final\<指纹>.txt（草稿不动）。"""
        lv, lab, fp = self.current_map() if hasattr(self, "opt_map") else ("", "", "")
        if not fp or not ND.final_store_has(fp):
            self.set_status("这张图还没发布")
            return
        if not messagebox.askyesno(
                "撤销这张图的发布",
                "把「%s」从成品里撤掉？\n\n"
                "只删 final\\%s.txt；草稿不动，启动成品时这张图会走原生。\n"
                "发布前的快照仍在 archive\\final_prev\\，需要时可以手工找回。\n\n继续？"
                % (lab or lv, fp),
                parent=self):
            return
        self.run_navdata(["final", "rm", fp], "撤销发布")
