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
from ui.env import FINAL_ROOT, HERE, NAVCMD, NAVDATA, ND, PACKS
from ui.maps import folder_alias, map_folder, map_scene
from ui.util import _python, game_running


_FINAL_FP_RE = re.compile(r"^n\d+-[0-9a-f]{16}\.txt$", re.I)   # 成品版本里的真图（不含 nogen.txt）


_CMD_SEQ = 0


def prepare_final_dir(version):
    r"""成品某个版本开跑前补齐两件事（幂等，每次启动游戏前调一次）：

      1) nogen.txt —— 编辑中的 grow/keep 包都带这个文件（空图不自动铺点），成品要一致；
      2) *.txt 设只读 —— 成品不允许游戏内保存（DLL 的 fopen("w") 会失败）。

    成品档「按包」读 ②\final\<版本>\（UCF_PACK_DIR=final、UCF_PACK=<版本名>），
    和编辑中同一套加载逻辑。返回该版本目录；版本不存在就返回空串。
    """
    d = os.path.join(FINAL_ROOT, version) if version else ""
    if not d or not os.path.isdir(d):
        return ""
    try:
        ng = os.path.join(d, "nogen.txt")
        if not os.path.isfile(ng):
            with open(ng, "w", encoding="utf-8", newline="\n") as f:
                f.write("")
        for fn in os.listdir(d):
            if fn.lower().endswith(".txt"):
                try:
                    os.chmod(os.path.join(d, fn), 0o444)
                except OSError:
                    pass
    except OSError:
        pass
    return d


_FINAL_BOOTED = {"ok": False}


def final_versions():
    r"""成品所有版本（读 navdata.py 的台账）；读不了当没有。
    第一次调用顺手做一次迁移：老成品目录 ②\nav\ 有数据就搬成 v1。"""
    try:
        if not _FINAL_BOOTED["ok"]:
            _FINAL_BOOTED["ok"] = True
            ND.final_ensure_root()
        return ND.final_versions()
    except Exception:                 # noqa: BLE001
        return []


def final_current_name():
    r"""台账里当前该启动的版本名；没有就空串。"""
    try:
        return ND.final_current()
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

    def _guard_game(self, title):
        r"""游戏开着时部署/还原不会报错，但这一局读的还是旧数据 —— 先问一句，别让人以为改完没生效。"""
        if not game_running():
            return True
        return messagebox.askyesno(title, "游戏正在运行：这一局已经读进内存的数据不会变。\n"
                                          "要现在继续吗？（想让它这次生效就先关游戏）", parent=self)

    def ask_publish(self):
        r"""发布到成品：选「新建一版」还是「更新当前版」，可填备注。取消返回 None。"""
        vers = final_versions()
        cur = self.final_selected() or final_current_name()
        pack = self.selected_pack() if hasattr(self, "opt_pack") else ""
        try:
            want = ND.final_name_from_pack(pack) or ""
        except Exception:                 # noqa: BLE001
            want = ""
        out = {"into": "", "note": "", "go": False}
        top = ctk.CTkToplevel(self)
        top.title("发布到成品")
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)
        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, lambda: top.winfo_exists() and top.grab_set())
        top.bind("<Escape>", lambda _e: top.destroy())

        ctk.CTkLabel(top, text="发布到成品", font=("Microsoft YaHei UI", 17, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 0))
        if not vers:
            tip = ("成品里还没有版本：这次会建第一版 %s（版本名跟测试包同名），"
                   "以后每次发布默认再加一版，老版本都留着。" % (want or "v1"))
        else:
            tip = ("成品现在 %d 个版本，当前启动 %s。\n"
                   "「新建一版」= 以当前版为底整套复制，再用这个包替换它那张图，"
                   "新版本名叫 %s，老版本全留着；\n"
                   "「更新当前版」= 只改 %s 里那张图，版本名不变。"
                   % (len(vers), cur or "无", want or "v1", cur or "它"))
        ctk.CTkLabel(top, text=tip, font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=470).pack(fill="x", padx=18, pady=(4, 10))

        mode = {"into": ""}
        if vers:
            ctk.CTkLabel(top, text="发布方式", font=FONT_S, text_color="#9aa0a6",
                         anchor="w").pack(fill="x", padx=20, pady=(0, 4))
            seg = ctk.CTkSegmentedButton(top, values=["新建一版（推荐）", "更新当前版"],
                                         font=FONT_S, height=32)
            seg.set("新建一版（推荐）")
            seg.pack(fill="x", padx=18)
            try:
                one = ND.final_unique_name(want) if want else "v1"
            except Exception:             # noqa: BLE001
                one = want or "v1"
            ctk.CTkLabel(top, text="新建一版的版本名 = %s（跟测试包同名；重名自动加 -2）。"
                                   "两种方式都不会删掉已有的成品版本。" % one,
                         font=("Consolas", 11), text_color="#8a8f96",
                         anchor="w", justify="left", wraplength=470).pack(
                fill="x", padx=20, pady=(4, 8))
        else:
            seg = None

        ctk.CTkLabel(top, text="备注（可选，记进版本台账，例：运输船全长路线）",
                     font=FONT_S, text_color="#9aa0a6", anchor="w").pack(fill="x", padx=20, pady=(2, 4))
        ent = ctk.CTkEntry(top, font=FONT, width=420, placeholder_text="这一版改了什么")
        ent.pack(fill="x", padx=18)

        bar = ctk.CTkFrame(top, fg_color="transparent")
        bar.pack(fill="x", padx=18, pady=(14, 16))

        def go(_e=None):
            out["go"] = True
            if seg is not None and str(seg.get()).startswith("更新"):
                out["into"] = cur
            out["note"] = ent.get().strip()
            top.destroy()

        ent.bind("<Return>", go)
        ctk.CTkButton(bar, text="取消", width=90, height=32, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=top.destroy).pack(side="right")
        ctk.CTkButton(bar, text="发布", width=110, height=32, font=FONT,
                      fg_color="#2f9e44", hover_color="#37b24d",
                      command=go).pack(side="right", padx=(0, 8))
        self.wait_window(top)
        return out if out["go"] else None

    def do_promote(self):
        r"""编辑中 -> 成品：把当前包的 <指纹>.txt 发布进成品的一个版本。

        默认「新建一版」：以当前版本为底整套复制，再用这个包替换对应那张图，老版本全留着；
        也可以只更新当前版。成品档「按包启动」，和编辑中同一套加载逻辑，所以
        grow / keep / 普通增量发过去效果一模一样。写完由 navdata.py 加只读属性。
        """
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        if not name:
            self.set_status("先在「编辑中」页选一个测试包")
            return
        if not self._guard_game("发布到成品"):
            return
        got = self.ask_publish()
        if not got:
            return
        args = ["pack", "promote", name]
        if got.get("into"):
            args += ["--into", got["into"]]
        if got.get("note"):
            args += ["--note", got["note"]]
        self.run_navdata(args, "发布到成品")

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
        disp = self.opt_map.get() if hasattr(self, "opt_map") else ""
        lv, lab, fp = self.map_disp.get(disp, ("", "", ""))
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        return {
            "on": bool(self.pack_on.get()),
            "name": name,
            "map": lv, "label": lab, "fp": fp,
            "only_map": bool(self.pack_only.get()),
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
        on = self.seg_mode.get().startswith("编辑中")
        self.pack_on.set(on)
        disp = self.opt_pack.get()
        name = "" if disp.startswith("（") else getattr(self, "pack_disp", {}).get(disp, "")
        if not name and not disp.startswith("（"):
            name = self.resolve_pack_id(disp)
        if not name:
            packs = self._pack_values()
            self.opt_pack.configure(values=packs)
            if packs and not packs[0].startswith("（"):
                self.opt_pack.set(packs[0])
                name = self.pack_disp.get(packs[0], "")
        # 换包时自动把地图切到包对应的那张图（包只对它生效，选错图等于空跑）
        if on and name and name != getattr(self, "_last_pack", ""):
            lv = self.pack_manifest_map(name)
            for mdisp, (lvl, _lab, _fp) in self.map_disp.items():
                if lv and lvl == lv:
                    self.opt_map.set(mdisp)
                    break
        self._last_pack = name
        self.pack_name = name
        state = "normal" if on else "disabled"
        try:
            self.opt_pack.configure(state=state)
            self.opt_map.configure(state=state)
        except Exception:
            pass
        if persist:
            self.persist("测试包")
        self.refresh_launch_strip()
        self.refresh_wp_status()
        self.update_mode_hint()
        self.refresh_compare()
        if hasattr(self, "rec_pre"):
            self.refresh_rec_ready()

    def open_packs_dir(self):
        try:
            os.makedirs(PACKS, exist_ok=True)
            os.startfile(PACKS)      # noqa: SLF001  Windows 资源管理器
        except OSError as exc:
            self.set_status("打不开 packs 目录：%s" % exc)

    # ---- 控制台 → 运行中插件：载入 / 重读 / 保存 / 回正式版 ----
    def selected_pack(self):
        r"""当前选中的包 id（地图文件夹/包名）；没选返回空串。"""
        disp = self.opt_pack.get() if hasattr(self, "opt_pack") else ""
        if not disp or disp.startswith("（"):
            return ""
        return getattr(self, "pack_disp", {}).get(disp) or self.resolve_pack_id(disp)

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
        fp = pack_target_fp(name) if self.pack_only.get() else ""
        if self.pack_only.get() and not fp:
            fp = self.selected_fp()
        try:
            seq = write_nav_cmd(cmd, name, fp)
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.persist("测试包")
        running = game_running()
        act = {"apply": "载入", "reload": "重新应用", "save": "保存"}.get(cmd, cmd)
        short = name.split("/")[-1]
        if running:
            self.set_status("已发送 #%d：%s %s；游戏日志看 navcmd / naved" % (seq, act, name))
        else:
            self.set_status("游戏没开：已选中 %s，点「开始游戏」生效" % short)

    def clear_pack_map(self):
        name = self.selected_pack()
        if not name:
            self.set_status("先选一个测试包")
            return
        fp = pack_target_fp(name) or self.selected_fp()
        if not fp:
            self.set_status("不知道这张图的指纹：先在右侧选一张地图")
            return
        if not messagebox.askyesno(
                "清空当前图",
                "把测试包 %s 里 %s 的路线清成%s？\n"
                "只重写 packs\\%s\\%s.txt，不动成品 nav\\。"
                % (name.split("/")[-1], fp,
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
            man.setdefault("name", name.split("/")[-1])
            man.setdefault("folder", name.replace("\\", "/").split("/")[0])
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
        r"""给当前选中的地图建一份测试包：空白地图（grow）或原版基础 + 新增（keep）。

        空白地图写 `grow`：插件进图先把原生路点全部禁用，再把包里自己画的
        node add / edge add 按 PointGraph.AddNode 新建，数量不受原生点数限制；
        `nogen.txt` 同时关掉插件的自动铺点。原版基础 + 新增写 `keep`：原生路点
        一个都不动，只把新点加到原图上。
        """
        disp = self.opt_map.get()
        if disp not in self.map_disp:
            self.set_status("先选一张有指纹的图，再建测试包")
            return
        lv, lab, fp = self.map_disp[disp]
        got = self.ask_pack_name(lab, lv, fp)
        if not got or not got.get("name"):
            return
        name = got["name"]
        keep = bool(got.get("keep"))
        folder = map_folder(lv, fp)
        pid = "%s/%s" % (folder, name)
        pdir = pack_dir(pid)
        tpath = os.path.join(pdir, fp + ".txt")
        if os.path.isfile(tpath) and not messagebox.askyesno(
                "覆盖测试包", "测试包 %s 里已经有 %s.txt，覆盖成%s？" % (
                    name, fp, "「原版基础 + 新增」" if keep else "「空白地图」"),
                parent=self):
            return
        try:
            os.makedirs(pdir, exist_ok=True)
            with open(tpath, "w", encoding="utf-8", newline="\n") as f:
                if keep:
                    f.write("# ucf-navedit v1 fp=%s\n# keep: 原生点原样保留，只新增节点\nkeep\n" % fp)
                else:
                    f.write("# ucf-navedit v1 fp=%s\ngrow\n" % fp)
            with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
                f.write("")                       # 存在即关掉自动铺点
            man = {
                "name": name, "folder": folder, "level": lv, "label": lab, "fp": fp,
                "created": time.strftime("%Y-%m-%d %H:%M:%S"),
                "source": "console-keep" if keep else "console-grow",
                "grow": True, "keep": bool(keep),
                "note": ("keep 测试包：原生点一个都不动（原版路线照常走）+ 新点按 AddNode 新建"
                         if keep else
                         "grow 测试包（空白地图）：原生点全禁用 + 新点按 AddNode 新建（不受原生点数限制）"),
            }
            with open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8",
                      newline="\n") as f:
                json.dump(man, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except OSError as exc:
            self.set_status("建包失败：%s" % exc)
            return
        values = self._pack_values()
        self.opt_pack.configure(values=values)
        self.opt_pack.set(self.disp_of(pid))
        self.seg_mode.set("编辑中（packs·可写）")
        self.pack_on.set(True)
        self.on_pack_change()
        msg = "已建%s测试包 %s（%s · %s）" % (
            "「原版基础 + 新增」" if keep else "「空白地图」", name, lab, folder)
        if game_running():
            try:
                write_nav_cmd("apply", pid, fp)
                msg += "，已发送到运行中的游戏"
            except OSError:
                pass
        self.set_status(msg)

    # ---- 成品版本（多版本：一版 = 一整套数据，启动时选一个）----------------
    def final_selected(self):
        r"""下拉框里选中的成品版本名（没选中就退回台账里的 current）。"""
        if hasattr(self, "opt_final") and hasattr(self, "final_disp"):
            name = self.final_disp.get(self.opt_final.get(), "")
            if name:
                return name
        return final_current_name()

    def refresh_final_combo(self):
        r"""把成品版本刷进下拉框，顺手更新说明行和底部按钮。"""
        self.final_disp = {}
        vers = final_versions()
        for v in vers:
            nm = v["name"]
            if len(nm) <= 16:      # 老名字（v1/正式版A）短，补上时间和图数好认
                label = "%s · %s · %d 张图" % (nm, (v.get("created") or "-")[5:16],
                                               len(v.get("maps") or {}))
            else:                  # 版本名沿用测试包名（<场景>_<日期>_<时间>），原样显示，不截断
                label = nm
            if not v.get("exists"):
                label += "（目录缺失）"
            self.final_disp[label] = v["name"]
        if hasattr(self, "opt_final"):
            values = list(self.final_disp) or ["（还没有版本）"]
            self.opt_final.configure(values=values)
            cur = final_current_name()
            pick = ""
            for label, name in self.final_disp.items():
                if name == cur:
                    pick = label
                    break
            self.opt_final.set(pick or values[0])
        for btn in (getattr(self, "btn_rename_final", None),
                    getattr(self, "btn_delete_final", None)):
            if btn is not None:      # 没有版本时改名/删除点了也没用，直接灰掉
                try:
                    btn.configure(state="normal" if vers else "disabled")
                except Exception:     # noqa: BLE001
                    pass
        if hasattr(self, "lbl_final"):
            cur = self.final_selected()
            if not vers:
                self.lbl_final.configure(
                    text="成品里还没有任何版本：去「编辑中」页选一个测试包，点「发布到成品」建第一版。",
                    text_color="#f59f00")
            else:
                v = next((x for x in vers if x["name"] == cur), None) or {}
                note = str(v.get("note") or "")
                self.lbl_final.configure(
                    text="启动成品 = %s（%d 张图，更新于 %s）  final\\%s%s" % (
                        cur, len(v.get("maps") or {}), (v.get("updated") or "-")[:16], cur,
                        ("  ·  " + note) if note else ""),
                    text_color="#8ab4f8")
        self.update_mode_hint()
        self.refresh_game_button()

    def on_final_change(self):
        name = self.final_selected()
        if name:
            try:
                ND.final_set_current(name)
            except Exception:                 # noqa: BLE001
                pass
        self.refresh_final_combo()
        self.refresh_wp_status()
        self.refresh_compare()

    def open_final_dir(self):
        name = self.final_selected()
        d = os.path.join(FINAL_ROOT, name) if name else FINAL_ROOT
        if not os.path.isdir(d):
            d = FINAL_ROOT
            try:
                os.makedirs(d, exist_ok=True)
            except OSError:
                pass
        try:
            os.startfile(d)                    # noqa: S606  Windows 专用
        except OSError as exc:
            self.set_status("打不开目录：%s" % exc)

    def rename_final(self):
        old = self.final_selected()
        if not old:
            self.set_status("还没有成品版本，先发布一版")
            return
        new = self.ask_text("改成品版本名",
                            "当前：%s。改成什么名字？（只改目录名和台账，路线数据一个字节不动）" % old,
                            old)
        if not new or new == old:
            return
        self.run_navdata(["final", "rename", old, new], "改版本名")

    def delete_final(self):
        r"""删掉当前成品版本：真删 final\<版本>\ 整个目录（用户 2026-11-21 要求，不要归档）。"""
        name = self.final_selected()
        if not name:
            self.set_status("还没有成品版本")
            return
        if not messagebox.askyesno(
                "删除成品版本",
                "真的删掉成品版本「%s」？\n\n"
                "会连 final\\%s 整个目录一起删（里面所有图），删了找不回来。\n"
                "游戏正开着就先关掉。其它版本不受影响；删完自动切到剩下的某一版，\n"
                "全删光了就是「成品没有版本」= 启动原版，再发布一次就又有。\n\n继续？" % (name, name),
                parent=self):
            return
        self.run_navdata(["final", "rm", name], "删除成品版本")
