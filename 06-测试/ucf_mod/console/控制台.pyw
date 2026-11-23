#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UCF 控制台 —— ucf_mod.json 的可视化开关面板

为什么要有它：ucf_mod 的功能开关以前散落成 collect.flag / nav\nogen.txt 之类
的标记文件，而且 ucf_mod.json 压根没被读。现在整份配置只有一个文件，
这个窗口就是它的人话界面：勾选即写盘，游戏下次启动生效。

启动游戏时会带上环境变量 UCF_MOD=1 —— 插件看到它才工作；
直接双击 UnityCrossFire.exe 没有这枚令牌，插件立刻返回，游戏就是原版。

只依赖 customtkinter（本机已有 5.2.2），不联网、不监听端口。
"""
import hashlib
import json
import os
import queue
import re
import shutil
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "core"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ucf_paths as P  # noqa: E402   图文件夹 <图>\map.json、可走面、路线都从这取
from ucf_paths import DEPLOY, DEV, NATIVE, TEST, PACKS_DIR, doc  # noqa: E402  三区里的根（TEST 是 DEV 的旧名）
from map_table import folder_name as map_folder_name, row_of as map_row  # noqa: E402  序号_场景名中文名
from map_table import rows as map_table_rows  # noqa: E402  对照表全 11 行（含下拉里没有的纯面图）
import navdata as ND          # noqa: E402  成品版本台账 / 包对比（只读调用；改数据仍走子进程命令行）
import ucf_rec              # noqa: E402  录制轨迹：解析 / 重采样 / 跳跃·落下·岔路识别
import ucf_trace            # noqa: E402  原始轨迹采集：目录 / 增量读取 / 摘要

CFG_PATH = os.path.join(DEPLOY, "ucf_mod.json")
# 2026-11-23：日志的主位置在**工程端** log\（ucf_mod.log / autotest.txt / player_marks.txt），
# 启动游戏时用 UCF_LOG_DIR 指给插件，所以游戏目录不再生成日志。
# 没走控制台启动时插件会落到 <部署端>\log\，更老的部署还在部署端根目录 —— 读的时候三级都看。
LOG_DIR = P.LOG_DIR                            # 主：工程端 log\
GAME_LOG_DIR = os.path.join(DEPLOY, "log")     # 备：没走控制台的落点
LOG_PATH = os.path.join(LOG_DIR, "ucf_mod.log")
AUTOTEST_TXT = os.path.join(LOG_DIR, "autotest.txt")   # 车测：每张图 OK + 最后 RESULT 写这里
MAP_MD = doc("地图对照表.md")
GAME_EXE = os.path.join(os.path.dirname(DEPLOY), "UnityCrossFire.exe")
NAVSERVER = os.path.join(HERE, "navserver.py")
NAVDATA = os.path.join(P.CORE, "navdata.py")   # 数据版本命令（部署/还原/校验/状态），库在 core/
TIDY = P.tool("tidy_vis.py")                   # 整理 ② vis：raw/<地图>/ + navmesh/ + _state/
PACKS = PACKS_DIR                              # ② 测试包：<包名>\<指纹>.txt + manifest.json
TEST_VIS = os.path.join(DEV, "vis")            # ② 导出收件箱（和递给游戏的那个路径一致）
REC_RAW = os.path.join(TEST_VIS, "rec")        # 录制原始轨迹：dev\vis\rec\*.jsonl（插件按控制台给的路径写）
FINAL_ROOT = os.path.join(DEV, "final")        # ② 成品版本集合：每版一个目录，插件按 UCF_PACK=<版本名> 读
FINAL_NAV = os.path.join(DEV, "nav")           # 旧成品目录：2026-11-21 起首次运行自动迁进 final\vN
_FINAL_FP_RE = re.compile(r"^n\d+-[0-9a-f]{16}\.txt$", re.I)   # 成品版本里的真图（不含 nogen.txt）
NAVCMD = os.path.join(DEPLOY, "ucf_navcmd.txt")  # 运行中命令：插件每 ~0.5 s 查一次 seq
PMARK_TXT = os.path.join(LOG_DIR, "player_marks.txt")  # 玩家坐标记录：插件追加，控制台删除
_CMD_SEQ = 0


def find_log(name):
    r"""日志在哪：工程端 log\ → <部署端>\log\ → 部署端根目录（越往后越老）。"""
    for p in (os.path.join(LOG_DIR, name),
              os.path.join(GAME_LOG_DIR, name),
              os.path.join(DEPLOY, name)):
        if os.path.isfile(p):
            return p
    return os.path.join(LOG_DIR, name)


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


def load_maps():
    r"""[(level, 中文名, 指纹)] —— 指纹来自每张图的 map.json（游戏自己扫出来的，不能手猜）。

    一个图文件夹一份：<序号>_<场景><中文名>\map.json。部署端没有数据时退回开发版。
    飓风危城（level9）原生 0 点、没有指纹，运行时就是 n0-0000000000000000。
    """
    out, seen = [], set()
    for root in (DEPLOY, DEV):
        for _rel, path in P.map_files(root):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, ValueError):
                continue
            m = doc.get("map") or {}
            lv = str(m.get("level") or "")
            if not lv or lv in seen:
                continue
            fp = str(m.get("fingerprint") or "")
            if not fp and lv == "level9":
                fp = "n0-0000000000000000"
            if not fp:
                continue                      # 没指纹 = 这张图没有路点图，测不了
            seen.add(lv)
            cn, _sc = map_row(lv)             # 中文名以《地图对照表》为准（暴风 JSON 里是旧名）
            out.append((lv, cn or str(m.get("label") or m.get("scene") or lv), fp))
    out.sort(key=lambda r: int("".join(ch for ch in r[0] if ch.isdigit()) or 0))
    return out


def _navmesh_name(level):
    r"""可走面在文档 / 日志里的叫法：nm716（716 个网格顶点）；不知道就写 navmesh.bin。"""
    verts = getattr(P, "NATIVE_VERTS", {}).get(str(level or ""))
    return ("nm%d" % verts) if verts else P.NAVMESH


def maps_not_listed(shown_levels):
    r"""[(序号, level, 中文名, 有没有可走面)] —— 对照表里有、但地图下拉里没有的图。

    为什么会有：load_maps 只收「有路点图（map.json + 指纹）」的图，而胜利广场 /
    死亡擂台在场景里原生没有 PointGraph（0 个路点、只有可走面 nm716 / nm60），
    永远导不出 map.json，于是永远不进下拉 —— 不是漏采，是这两张图没路点可编。
    界面上不解释，看起来就像少了两张图（2026-11-21 用户进过胜利广场后问的）。
    """
    shown = set(shown_levels or ())
    out = []
    try:
        rows = map_table_rows()
    except Exception:                     # noqa: BLE001  表读不了就什么都不提示
        return out
    for no, lv, cn, _sc in rows:
        if lv in shown:
            continue
        out.append((no, lv, cn, os.path.isfile(
            os.path.join(P.map_dir(DEV, lv), P.NAVMESH))))
    return out


def find_map_doc(fp):
    r"""(doc, path) —— 按指纹找这张图的 map.json；部署端优先，退回开发版。

    人机路点页用它算节点 / 边 / 出生点数量；不写任何文件。
    """
    if not fp:
        return None, ""
    for root in (DEPLOY, DEV):
        for _rel, path in P.map_files(root):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, ValueError):
                continue
            if str((doc.get("map") or {}).get("fingerprint") or "") == fp:
                return doc, path
    return None, ""


def load_scene_counts():
    r"""{level: {jump, crouch, guard, area, tag}} —— 读《地图对照表》第二张表。

    地图 JSON 是运行期导出（只有 PointGraph + spawn/tag），
    守点/聚集区/蹲点只在场景组件统计里，所以页签显示以这张表为准。
    """
    out = {}
    try:
        with open(MAP_MD, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return out

    def num(text):
        try:
            return int("".join(ch for ch in str(text) if ch.isdigit()) or 0)
        except ValueError:
            return 0

    for line in lines:
        s = line.strip()
        if not s.startswith("| level"):
            continue
        parts = [x.strip() for x in s.strip("|").split("|")]
        if len(parts) < 11:
            continue
        out[parts[0]] = {
            "name": parts[1], "scene": parts[2],
            "jump": num(parts[3]), "nodelink": num(parts[4]),
            "nodelink2": num(parts[5]), "crouch": num(parts[6]),
            "guard": num(parts[7]), "area": num(parts[8]), "tag": num(parts[9]),
        }
    return out


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


def map_scene(lv, fp=""):
    r"""地图英文场景名（默认包名前缀用）：maps\*.json 的 scene，缺了查《地图对照表》。"""
    doc, _p = find_map_doc(fp)
    scene = str(((doc or {}).get("map") or {}).get("scene") or "")
    if not scene:
        scene = str((load_scene_counts().get(lv) or {}).get("scene") or "")
    scene = re.sub(r"[^A-Za-z0-9_-]+", "_", scene).strip("_-")
    return scene or str(lv or "blank")


def folder_alias(name):
    r"""去掉文件夹名的序号前缀：01_TransportShip运输船 → TransportShip运输船。

    只用于认「同一个地图的老文件夹」（没序号/纯英文），名字本身不改。
    """
    return re.sub(r"^\d{2,3}_", "", str(name or ""))


def map_folder(lv, fp=""):
    r"""测试包文件夹名：序号_英文场景名中文名，如 01_TransportShip运输船。

    序号来自《地图对照表》第一张表（map_table 统一读），排序和 maps\NN_中文名.json 一致；
    Windows 支持中英混排，插件的 ANSI 路径在本机（代码页 936）能读中文，
    所以目录用「序号+英文+中文」，包名仍用英文（navcmd / 日志更稳）。
    """
    doc, _p = find_map_doc(fp)
    m = (doc or {}).get("map") or {}
    scene = str(m.get("scene") or "")
    label = str(m.get("label") or "")
    if not scene or not label:
        row = load_scene_counts().get(lv) or {}
        scene = scene or str(row.get("scene") or "")
        label = label or str(row.get("name") or "")
    return map_folder_name(lv, scene, label)


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


# 版本对比的状态色（人机路点最下面那块面板用；唯一判据 = sha256 相同）
CMP_COLOR = {"same": "#2f9e44", "diff": "#f59f00", "only_pack": "#4c6ef5",
             "only_final": "#868e96", "fp_bad": "#e03131"}
CMP_TEXT = {"same": "✔ 一致", "diff": "⚠ 不一致", "only_pack": "○ 只在编辑中",
            "only_final": "◇ 只在成品", "fp_bad": "✖ 指纹不匹配"}
CMP_SHORT = {"same": "✔ 一致", "diff": "⚠ 不一致", "only_pack": "○ 待发布",
             "only_final": "◇ 只在成品", "fp_bad": "✖ 指纹失效"}


def _cut(text, n):
    r"""长名字截断（表格列宽固定，别让一行把整张表撑歪）。"""
    text = str(text or "")
    return text if len(text) <= n else text[:max(1, n - 1)] + "…"


def file_sha256(path):
    r"""小文件的 sha256（几毫秒）；读不了返回空串。"""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for blk in iter(lambda: f.read(65536), b""):
                h.update(blk)
        return h.hexdigest()
    except OSError:
        return ""


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

def compact_path(path, limit=52):
    r"""路径太长就省略：只留盘符 + 末尾若干层（区分信息通常在尾巴上）。
    D:\BaiduNetdiskDownload\test-1\UnityCrossFire1.7.1\UnityCrossFire.exe -> D:\…\test-1\UnityCrossFire1.7.1\UnityCrossFire.exe
    """
    path = str(path or "")
    if len(path) <= limit:
        return path
    drive, rest = os.path.splitdrive(path)
    keep = limit - len(drive) - 2
    if keep <= 8:
        return path[: limit - 1] + "…"
    return drive + "\\…" + rest[-keep:]


def game_tag(game_exe):
    r"""底部按钮上「这是哪一份游戏」的短标签：从游戏目录往上，跳过像游戏名的层级。
    ...\BaiduNetdiskDownload\test-1\UnityCrossFire1.7.1\...\UnityCrossFire.exe -> test-1
    ...\BaiduNetdiskDownload\UnityCrossFire1.7.1\...\UnityCrossFire.exe          -> BaiduNetdiskDownload
    """
    try:
        game_dir = os.path.dirname(os.path.abspath(game_exe))
        parts = [p for p in game_dir.replace("/", "\\").split("\\") if p]
        i = len(parts) - 1
        while i >= 0 and parts[i].lower().startswith("unitycrossfire"):
            i -= 1
        if i >= 0:
            return parts[i]
        return os.path.basename(game_dir) or game_dir
    except Exception:
        return ""


def _python():
    r"""跑 navdata.py 用的解释器：控制台是 .pyw，sys.executable 可能是 pythonw.exe，
    那样子进程没有控制台、输出不好收，优先换成同目录的 python.exe。"""
    exe = sys.executable or "python"
    if exe.lower().endswith("pythonw.exe"):
        cand = os.path.join(os.path.dirname(exe), "python.exe")
        if os.path.isfile(cand):
            return cand
    return exe


def _listdir(path):
    try:
        return os.listdir(path)
    except OSError:
        return []


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%d %s" % (n, unit)) if unit == "B" else ("%.1f %s" % (n, unit))
        n /= 1024.0
    return "%.1f GB" % n


def fmt_time(ts):
    if not ts:
        return "（空）"
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))


def fmt_short(ts):
    r"""行内用的短时间：11-21 10:41（数据页按块报数，不再占一长串年份）。

    日期和时间之间用不换行空格：Tk 的自动换行只在空格处断行，
    普通空格会让「最近 11-21 12:16」断成两行、时间字悬在下一行。"""
    if not ts:
        return "—"
    t = time.localtime(ts)
    return time.strftime("%m-%d", t) + "\u00a0" + time.strftime("%H:%M", t)


def dir_bytes(root):
    r"""整个目录递归的 (字节数, 最新写入时间)；读不动就当 0 / 空。
    和 dir_stats 的区别：dir_stats 只数 maps/nav/vis，这个连 final、packs 一起算。"""
    total = 0
    latest = 0.0
    for base, _dirs, files in os.walk(root):
        for fn in files:
            try:
                st = os.stat(os.path.join(base, fn))
            except OSError:
                continue
            total += st.st_size
            latest = max(latest, st.st_mtime)
    return total, latest


def dir_stats(root):
    r"""这一版数据的 (文件数, 字节数, 最新写入时间)：每张图的 map.json + navmesh.bin + 路线 txt。

    ② 的 packs、final 不在这里算（成品 / 编辑中 两行各自报数），不然数字会混。"""
    n = total = 0
    latest = 0.0
    for _key, path in list(P.map_files(root)) + list(P.navmesh_files(root)) + list(P.route_files(root)):
        try:
            st = os.stat(path)
        except OSError:
            continue
        n += 1
        total += st.st_size
        latest = max(latest, st.st_mtime)
    return n, total, latest


def latest_export(root):
    r"""最新一份导出 JSON：<图>\导出\ 与收件箱 vis\（认不出关卡的会留在收件箱）。
    返回 (文件名, 完整路径, 修改时间戳)；没有则 None。"""
    best = None
    scan = [os.path.join(root, "vis")]
    for _rel, path in P.map_files(root):
        scan.append(os.path.join(os.path.dirname(path), "导出"))
    for d in scan:
        if not os.path.isdir(d):
            continue
        for base, dirs, files in os.walk(d):
            dirs[:] = [x for x in dirs if x not in ("navmesh", "_state", "_noise")]
            for fn in files:
                if fn.startswith("_seen_") or not fn.endswith(".json"):
                    continue
                p = os.path.join(base, fn)
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                if not os.path.isfile(p):
                    continue
                if best is None or st.st_mtime > best[2]:
                    best = (fn, p, st.st_mtime)
    return best


def vis_raw_dir(root):
    r"""新结构优先打开 vis\raw（按地图分好）；旧结构回退 vis 根。"""
    raw = os.path.join(root, "vis", "raw")
    return raw if os.path.isdir(raw) else os.path.join(root, "vis")


def data_counts(root):
    r"""(图数, 路线文件数, 路线条数, 可走面数) —— 只看每张图文件夹里的数据。"""
    maps = len(P.map_files(root))
    routes = P.route_files(root)
    lines = 0
    for _fp, path in routes:
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                lines += len([ln for ln in f if ln.strip() and not ln.lstrip().startswith("#")])
        except OSError:
            pass
    return maps, len(routes), lines, len(P.navmesh_files(root))


def test_stats(root):
    r"""② 开发版收件箱：(导出 JSON 数, 可走面数, 测试包数, 字节数, 最新写入时间)。"""
    vis = os.path.join(root, "vis")
    n_json = n_bin = total = 0
    latest = 0.0
    for base_dir, dirs, files in os.walk(vis):
        dirs[:] = [x for x in dirs if x not in ("_state", "_noise")]
        for fn in files:
            p = os.path.join(base_dir, fn)
            try:
                st = os.stat(p)
            except OSError:
                continue
            if not os.path.isfile(p):
                continue
            total += st.st_size
            latest = max(latest, st.st_mtime)
            if fn.startswith("navmesh_") and fn.endswith(".bin"):
                n_bin += 1
            elif fn.endswith(".json"):
                n_json += 1
    packs = 0
    pk_dir = os.path.join(root, "packs")
    try:
        for entry in os.listdir(pk_dir):
            d = os.path.join(pk_dir, entry)
            if not os.path.isdir(d):
                continue
            if _is_pack_dir(d):
                packs += 1
                continue
            for sub in _listdir(d):
                if os.path.isdir(os.path.join(d, sub)) and _is_pack_dir(os.path.join(d, sub)):
                    packs += 1
    except OSError:
        pass
    return n_json, n_bin, packs, total, latest


def export_filed(root):
    r"""已经归位到各图文件夹的导出份数：<图>\导出\*.json。"""
    n = 0
    for _rel, path in P.map_files(root):
        d = os.path.join(os.path.dirname(path), "导出")
        if os.path.isdir(d):
            n += len([f for f in os.listdir(d) if f.endswith(".json")])
    return n


def tree_hashes(root):
    r"""每张图的 map.json + 路线 txt 的 sha1：判断两版是不是同一份数据。
    名字注册表 names.json 与自动生成的索引不算（格式差异不影响游戏）。"""
    out = {}
    for rel, path in P.map_files(root):
        try:
            with open(path, "rb") as f:
                out[rel] = hashlib.sha1(f.read()).hexdigest()
        except OSError:
            pass
    for fp, path in P.route_files(root):
        try:
            with open(path, "rb") as f:
                out[fp + ".txt"] = hashlib.sha1(f.read()).hexdigest()
        except OSError:
            pass
    return out


def diff_count(a, b):
    keys = set(a) | set(b)
    return sum(1 for k in keys if a.get(k) != b.get(k))


CREATE_NO_WINDOW = 0x08000000
FONT = ("Microsoft YaHei UI", 13)
FONT_S = ("Microsoft YaHei UI", 12)
FONT_B = ("Microsoft YaHei UI", 15, "bold")

# ---- 开关定义：(key, 标题, 说明, 默认值) --------------------------------
GROUPS = [
    ("地图", "房间选图列表里要不要多一张「暴风」；关掉后就是原版列表", [
        ("hidden_map", "加载暴风地图", "把隐藏图 Nano30_Storm 插进房间下拉框；关掉后选不到暴风", True),
    ]),
    # 2026-11-19 用户要求：可视化按数据类别拆成勾选框，一颗开关同时管「读不读」和「画不画」；
    # 总开关（visualizer）排在本页顶部。「导出」页那 6 个 export_* 是另一套，互不影响。
    ("可视化", "进图时读什么、画什么都在这一页；关掉哪类就不读也不画（不影响 Ctrl+E 导出）。"
                "给开发用的玩家坐标记录 / 原始轨迹采集在最后一页「开发者选项」", [
        ("visualizer", "可视化总开关（Visualizer）", "整套彩色点线的总开关；关掉后进图不画（可走面独立，不受影响）；Ctrl+V 随时开关", False),
        ("vis_nodes", "路点 / 连线（PointNode / Connection）", "浅蓝点 = 普通路点，橙点 = 带标签，红点 = 禁走点；蓝线 = 连线", True),
        ("vis_crouch", "蹲守点（Bot_CrouchPos）", "红色实心小方块（两阵营同色）", True),
        ("vis_guard", "守卫区 / 守卫点（Bot_GuardArea / Bot_GuardPos）", "紫色线框区 + 橙色实心点", True),
        ("vis_nano", "幽灵守区 / 幽灵守点（Bot_NanoGuardArea / Bot_NanoGuardPos）", "绿色线框区 + 青色实心点", True),
        ("vis_born", "出生点（SpawnPoint）", "潜伏者(蓝)/保卫者(红)/中立点(灰)；个人竞技用中立点、全员敌对；生化/剑客与补给箱混布，叠色偏粉紫", True),
        ("vis_supply", "补给箱（SupplyBox / RedBox / BlueBox）", "金/粉/青实心高柱 = 补给/红/蓝", True),
        ("vis_jump", "跳点（Bot_JumpLink）", "黄色连线（没有点标记）", True),
        ("vis_tag", "标签区（PointNodeTagModifier）", "橙色线框小方块", True),
        ("navmesh_show", "可走面（NavMeshGraph）", "绿色三角网线框（人机真正在上面跑的面）；Ctrl+Shift+6 随时开关；与可视化总开关无关", True),
        # 2026-11-20 用户要求：工作台 / 3D 查看器 / 游戏里都要有「东南西北」，方向约定三处统一。
        ("vis_compass", "方向罗盘（东南西北）", "汉字罗盘：北 = 世界 -Z（和工作台平面图一致）、东 = +X、南 = +Z、西 = -X；圈心金字 = 你正对着哪；Ctrl+Shift+7 开关；与可视化总开关无关", True),
    ]),
    # 2026-11-18：导出单独成页 —— 一个总开关 + 六项内容，默认全勾
    ("导出", "Ctrl+E 导出的总开关与内容（与可视化开关互相独立）", [
        ("export_enabled", "启用导出", "总开关；关掉后下面勾选全部不生效，Ctrl+E 不读也不写", True),
        ("export_nodes", "路点 / 连线", "JSON 主体；关掉后只导特征点（文件名 f<特征数>，不写 _seen 去重）", True),
        ("export_crouch", "人类蹲守点", "读人类蹲守点；关掉后 JSON 里 crouch=0", True),
        ("export_area", "幽灵守区 / 守点", "读幽灵守区与幽灵守点；关掉后 nano_area/nano_pos=0", True),
        ("export_guard", "守卫区 / 守卫点", "读守卫区与守卫点；关掉后 guard=0", True),
        ("export_spawn", "出生点 / 补给箱", "读出生点与补给箱；关掉后 spawn=0", True),
        ("export_tags", "跳点 / 标签区", "读跳点与标签区；关掉后 jump/tag=0", True),
    ]),
    # 2026-11-19：文字标签控件已删除；这一页保留游戏内热键速查。
    ("快捷键", "游戏内热键速查（屏幕不再显示数据面板和文字标签）", []),
    # 2026-11-19 用户要求：删除「自动铺设」整块（auto_waypoints / auto_crouch / ghost_areas）。
    # 2026-11-19 用户要求：删除「允许游戏内编辑」（editor），C 侧键保留（默认开）。
    # 2026-11-19 用户要求：整个「手动」页删除（collect_only 入口随之去掉，功能仍可用
    # collect.flag / Ctrl+Shift+X）。
]

# 2026-11-21 用户要求：给开发 / 离线分析用的入口单独成页「开发者选项」（页签排最后），
# 从「可视化」「录制」里搬出来 —— 正常玩图那几页不再掺这些。
# 这里的开关和 GROUPS 走同一套自检（cfg.c 里有 -> 面板里必须能关、默认值一致）。
DEV_ITEMS = [
    ("vis_player_marks", "玩家坐标记录", "金色方块 = 本次（这张图这一局）记下的玩家脚下位置；换图 / 重开游戏就不画了，也不连折线；坐标只留在 player_marks.txt 当日志，记录 / 删除在下面「玩家坐标记录」卡片里", True),
]

# 「可视化」页各类数据的图例色块：游戏里画成什么颜色（照抄 src/editor.c 的 COL_* 与 vis_draw）。
# 顺序与 GROUPS 里各项的说明文字一一对应；C 侧改颜色这里要一起改。
VIS_COLORS = {
    "vis_nodes": ("#CCE0FF", "#FF8C0D", "#FF261F", "#4073F2"),
    "vis_crouch": ("#FF261F",),
    "vis_guard": ("#BF59FF", "#FF8C0D"),
    "vis_nano": ("#1AFF40", "#1AF2F2"),
    "vis_born": ("#2666FF", "#FF261F", "#B3B3B3"),
    "vis_supply": ("#FFD933", "#FF59B3", "#1AF2F2"),
    "vis_jump": ("#FFE00D",),
    "vis_tag": ("#FF8C0D",),
    "vis_player_marks": ("#FFD933",),
    "navmesh_show": ("#26FF8C",),
    "vis_compass": ("#F2CC47", "#A3BDE0"),
}

# 游戏内热键速查（控制台专用文档；游戏里不再显示这块）。按功能分组，组间空一行。
HUD_KEYS = (
    "【可视化】\n"
    "Ctrl+V 可视化总开关   Ctrl+Shift+6 可走面   Ctrl+Shift+7 方向罗盘\n"
    "\n"
    "【导出与采集】\n"
    "Ctrl+E 手动导出   Ctrl+Shift+X 只读采集（不创建对象）\n"
    "\n"
    "【标记】\n"
    "Delete 删除准星最近标记   Ctrl+0 显示/隐藏已放标记\n"
    "\n"
    "【编辑模式】\n"
    "Ctrl+1 编辑模式   Ctrl+2 放蹲守点   Ctrl+4 建守卫区\n"
    "Ctrl+5 撤销   Ctrl+6 保存   Ctrl+7 重载   Ctrl+8 阵营   Ctrl+9 状态写日志\n"
    "\n"
    "【路点编辑（Ctrl+Shift+字母）】\n"
    "Ctrl+Shift+A 选A点   Ctrl+Shift+N 加点   Ctrl+Shift+J A↔点 连/断\n"
    "Ctrl+Shift+D 禁用点   Ctrl+Shift+Z 撤销   Ctrl+Shift+S 手动保存   Ctrl+Shift+R 重套用\n"
    "\n"
    "【F2 路点菜单】\n"
    "F2 开关 / 长按 E 备用\n"
    "1-9 直选   小键盘 8/2 上下   5 确认   Esc/0 返回   左键确认 / 右键返回\n"
    "连续编辑：选好类型后停在类型页，5 可以一直放，1-6 随时换类型；Esc 只退一级，不会关菜单"
)

HUD_NOTES = (
    "· 游戏内数据面板和文字标签已删除；节点/守区等计数看 log\\ucf_mod.log 里的 [vis] 行，"
    "或控制台「上次运行」日志框。"
)


def load_cfg():
    try:
        with open(CFG_PATH, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_cfg(cfg):
    tmp = CFG_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, CFG_PATH)


_PROC_CACHE = {"t": 0.0, "v": False}


def _game_running_fast():
    r"""Toolhelp 快照枚举进程（约 2 ms）。tasklist 子进程要 300+ ms，
    切「编辑中 / 成品」两页时会明显顿一下，所以这里绕开子进程。
    不是 Windows / 结构对不上时返回 None，调用方退回 tasklist。"""
    try:
        import ctypes
        from ctypes import wintypes

        class PROCESSENTRY32W(ctypes.Structure):
            _fields_ = [("dwSize", wintypes.DWORD),
                        ("cntUsage", wintypes.DWORD),
                        ("th32ProcessID", wintypes.DWORD),
                        ("th32DefaultHeapID", ctypes.c_size_t),
                        ("th32ModuleID", wintypes.DWORD),
                        ("cntThreads", wintypes.DWORD),
                        ("th32ParentProcessID", wintypes.DWORD),
                        ("pcPriClassBase", ctypes.c_long),
                        ("dwFlags", wintypes.DWORD),
                        ("szExeFile", wintypes.WCHAR * 260)]

        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
        k32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE
        k32.Process32FirstW.argtypes = [wintypes.HANDLE,
                                        ctypes.POINTER(PROCESSENTRY32W)]
        k32.Process32FirstW.restype = wintypes.BOOL
        k32.Process32NextW.argtypes = [wintypes.HANDLE,
                                       ctypes.POINTER(PROCESSENTRY32W)]
        k32.Process32NextW.restype = wintypes.BOOL
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        k32.CloseHandle.restype = wintypes.BOOL

        snap = k32.CreateToolhelp32Snapshot(0x00000002, 0)   # TH32CS_SNAPPROCESS
        if not snap or snap == ctypes.c_void_p(-1).value:
            return None
        try:
            entry = PROCESSENTRY32W()
            entry.dwSize = ctypes.sizeof(PROCESSENTRY32W)
            ok = k32.Process32FirstW(snap, ctypes.byref(entry))
            while ok:
                if str(entry.szExeFile).lower() == "unitycrossfire.exe":
                    return True
                ok = k32.Process32NextW(snap, ctypes.byref(entry))
            return False
        finally:
            k32.CloseHandle(snap)
    except Exception:                   # noqa: BLE001  退回 tasklist
        return None


def game_running(fresh=False, ttl=1.0):
    r"""游戏在不在跑？1 s 内复用上次结果（切页、4 s 状态定时器都会问）。
    fresh=True 强制作一次真扫描（kill_game 等游戏退出时用）。"""
    now = time.time()
    if not fresh and now - _PROC_CACHE["t"] < ttl:
        return _PROC_CACHE["v"]
    fast = _game_running_fast()
    if fast is None:
        try:
            out = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq UnityCrossFire.exe", "/NH"],
                capture_output=True, text=True, errors="replace", timeout=5,
                creationflags=CREATE_NO_WINDOW)
            fast = "UnityCrossFire.exe" in (out.stdout or "")
        except Exception:
            fast = False
    _PROC_CACHE["t"] = now
    _PROC_CACHE["v"] = bool(fast)
    return bool(fast)


def kill_game(wait=8.0):
    r"""车测前必须关掉游戏：UCF_AUTOTEST 只对**新进程**生效。
    返回 True = 确认已退出；False = 8 秒还没关掉（可能卡死，交给用户处理）。"""
    try:
        subprocess.run(["taskkill", "/F", "/IM", "UnityCrossFire.exe"],
                       capture_output=True, creationflags=CREATE_NO_WINDOW)
    except OSError:
        return False
    deadline = time.time() + wait
    while time.time() < deadline:
        if not game_running(fresh=True):
            return True
        time.sleep(0.3)
    return not game_running(fresh=True)


def read_log_from(path, offset):
    r"""从字节偏移接着读日志；文件被轮转/改小而 offset 超了，就从头再读。"""
    try:
        size = os.path.getsize(path)
    except OSError:
        return "", 0
    if size < offset:
        offset = 0
    try:
        with open(path, "rb") as f:
            f.seek(offset)
            data = f.read()
    except OSError:
        return "", offset
    return data.decode("utf-8", "replace"), offset + len(data)


_MAP_ROW = re.compile(r"^\|\s*\d{1,3}\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|")
_LEVELS_FALLBACK = [
    ("level1", "运输船"), ("level2", "小型工厂"), ("level3", "椰岛之巅"),
    ("level4", "胜利广场"), ("level5", "竞技场"), ("level6", "刀锋寨"),
    ("level7", "沙漠要塞"), ("level8", "生化酒店"), ("level9", "暴风"),
    ("level10", "新寂静村"), ("level11", "死亡擂台"),
]


# 车测页底部的「车测是干什么的」：用户不熟车测，按「能 / 不能 / 注意」逐条列清楚
AT_CAN = [
    ("1. 崩溃回归（主用途）", "改完 DLL 跑一遍，没有 !!! crash = 没破坏加载链路；崩了日志里有崩溃栈"),
    ("2. 采数据", "进图时自动落 vis/navmesh_*.bin（可走面）；路线 JSON 要在地图里按 Ctrl+E 手动导"),
    ("3. 验数据链路", "日志 naved: grow / keep / pack: skip / pack: nav 证明编辑中、空白地图、成品切换真的生效"),
    ("4. 核对图号映射", "scene[0..15] + LOAD levelN + OK (map='沙漠要塞') 确认 buildIndex 对应哪张图"),
    ("5. 看导航数据", "[nav] diag: graphs=1 / waiting for PointGraph 看出这张图有没有 PointGraph / NavMeshGraph"),
    ("6. 版本对比", "同一组参数跑旧版和新版，日志逐行对照，哪张图开始不一样一目了然"),
    ("7. 批量扫图", "一次勾 11 张，不用手动进 11 次图、不用点大厅"),
]
AT_CANNOT = [
    "人机行为、路线对不对（车测没人机）",
    "正常开局路径（大厅 → 房间 → 开始比赛）",
    "画面 / UI / 帧率 / 手感",
    "玩法逻辑（击杀、胜负、经济）",
]
AT_NOTE = ("PASS 也可能是假通过：settle 太小（20 tick = 5 秒），问题还没触发就判过了；"
           "勾的图太少，也可能刚好全避开。")
AT_SUMMARY = ("车测 = 自动进图跑一圈的快速回归 + 数据采集；核心产出「哪张图会崩」，"
              "次要产出「数据用没用上、图号对不对」。")
AT_QUICK = "日志速记：看开头 armed、数中间 OK、看结尾 RESULT。"


def load_level_table():
    r"""[(level, 中文名)] —— 只读 docs\地图对照表.md 第一张表（唯一权威表）。
    车测传的是 buildIndex，也就是 levelN 的 N，**不是** maps\NN_中文名.json 的序号：
    序号 07 是死亡擂台、它的关卡是 level11，两者不能混。"""
    out = []
    started = False
    try:
        with open(MAP_MD, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    if started:
                        break            # 空行 = 第一张表结束（后面还有别的表，不能一起读）
                    continue
                m = _MAP_ROW.match(s)
                if m:
                    started = True
                    out.append((m.group(1), m.group(2).strip()))
                elif started and not s.startswith("|"):
                    break
    except OSError:
        pass
    if len(out) < 5:
        out = list(_LEVELS_FALLBACK)
    out.sort(key=lambda r: int("".join(ch for ch in r[0] if ch.isdigit()) or 0))
    return out



def tail_log(n=6):
    try:
        with open(find_log("ucf_mod.log"), "rb") as f:
            f.seek(0, os.SEEK_END)
            size = f.tell()
            f.seek(max(0, size - 65536))
            data = f.read().decode("utf-8", "replace")
    except OSError:
        return []
    lines = [ln for ln in data.splitlines() if ln.strip()]
    return lines[-n:]


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
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
        # 2026-11-19 用户要求：右上角加「窗口置顶」勾选 + 折叠成小条的开关。
        self.btn_fold = ctk.CTkButton(self.head, text="折叠", width=52, height=24,
                                      font=FONT_S, fg_color="#3a3f47", hover_color="#4a5058",
                                      command=self.toggle_fold)
        self.btn_fold.pack(side="right", padx=(10, 0))
        self.master_var = tk.BooleanVar(value=bool(self.cfg.get("enabled", True)))
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

        self.intro = ctk.CTkLabel(
            self,
            text="只有从本窗口「开始游戏」才会加载 mod；直接双击 UnityCrossFire.exe 是原版。\n"
                 "开关改完存进 ucf_mod.json，下次启动生效（游戏开着时要重开）。\n"
                 "启动档（编辑中 / 成品）是「人机路点」页顶部的两页；数据路径 / 还原 / 校验：切到「数据」页。\n"
                 "路点数据只读查看在工作台；现场编辑在「人机路点」页（游戏内 F2 菜单）。",
            font=FONT_S, text_color="#9aa0a6", justify="left")
        self.intro.pack(anchor="w", padx=20)

        # ---- 按钮 / 状态：先按底边占位，窗口再矮也不会被页签挤没 ----
        self.bar = ctk.CTkFrame(self, fg_color="transparent")
        self.bar.pack(side="bottom", fill="x", padx=14, pady=(0, 12))
        self.btn_game = ctk.CTkButton(self.bar, text="开始游戏（加载 mod）", font=FONT, height=42,
                                      fg_color="#2f6fdb", hover_color="#255bb4",
                                      command=self.launch_game)
        self.btn_game.pack(side="left", fill="x", expand=True, padx=(0, 6))
        ctk.CTkButton(self.bar, text="路点工作台（查看）", font=FONT, height=42,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.open_workbench).pack(side="left", fill="x", expand=True, padx=(6, 0))

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

        # 地图 / 可视化 / 导出 / 快捷键 / 人机路点 / 数据 / 车测 —— 全部页签切换，上方不再压一块常驻面板。
        self.tabview = ctk.CTkTabview(self, corner_radius=10, command=self.on_tab)
        self.tabview.pack(fill="both", expand=True, padx=14, pady=(8, 4))
        self.tab_titles = []
        for title, hint, items in GROUPS:
            self.tab_titles.append(title)
            tab = self.tabview.add(title)
            if title == "导出":
                self.build_export_tab(tab, hint, items)  # 总开关 + 六项勾选（一行多个）+ 最近导出
            elif title == "快捷键":
                self.build_hotkey_tab(tab, hint)          # 热键速查（游戏内已不显示）
            elif title == "可视化":
                self.build_vis_tab(tab, hint, items)     # 总开关 + 十类数据（勾选）
            else:
                self.build_group_tab(tab, hint, items)
        # 人机路点要在「数据」「车测」之前：后两页读它建的 opt_pack / opt_map。
        wp_tab = self.tabview.add("人机路点")               # SyPB 式现场编辑入口
        self.build_waypoint_tab(wp_tab)
        rec_tab = self.tabview.add("录制")                  # 走一遍就把路线录下来（只写 ② 编辑中）
        self.build_record_tab(rec_tab)
        self.build_data_tab(self.tabview.add("数据"))       # 三区路径/时间 + 部署/还原/校验
        # 2026-11-22：部署页 —— 选游戏位置 + 一键把 dll 迁进游戏目录（取代了原来的独立部署脚本）
        deploy_view = self.tabview.add("部署")
        try:
            import deploy_tab
            self.deploy_tab = deploy_tab.build_deploy_tab(self, deploy_view)
        except Exception as exc:                     # 部署页坏了也别把整个控制台带崩
            ctk.CTkLabel(deploy_view, text="部署页加载失败：%s" % exc,
                         font=FONT_S, text_color="#c92a2a").pack(padx=12, pady=12)
        self.build_autotest_tab(self.tabview.add("车测"))   # 不用鼠标键盘：插件自己在进程内切图
        # 2026-11-21 用户要求：开发者选项单独成页，排在所有页签最后
        # （玩家坐标记录从「可视化」、原始轨迹采集从「录制」搬进来）
        self.build_dev_tab(self.tabview.add("开发者选项"))
        self.tab_titles += ["人机路点", "录制", "数据", "部署", "车测", "开发者选项"]

        # 回到上次停留的页签；记住的页签已经不存在（改版删页）就落在默认第一页
        saved_tab = str(self.ui.get("tab") or "")
        if saved_tab in self.tab_titles:
            self.tabview.set(saved_tab)
            self.on_tab(saved_tab, persist=False)

        self.refresh_status()
        self.after(4000, self.refresh_status)

    # ---- 页签内容：一组开关 = 一页 ----
    def switch_card(self, parent, key, label, desc, default):
        r"""一个开关 + 一行说明；「可视化」等页共用这份样式。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
        self.vars[key] = var
        ctk.CTkSwitch(box, text=label, variable=var, font=FONT,
                      progress_color="#2f9e44",
                      command=lambda k=key: self.on_toggle(k)).pack(
            anchor="w", padx=12, pady=(10, 0))
        ctk.CTkLabel(box, text=desc, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=600).pack(
            fill="x", padx=12, pady=(2, 10))

    def build_group_tab(self, tab, hint, items):
        r"""页内再套一层滚动区：窗口压矮时开关仍然够得着。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        for key, label, desc, default in items:
            self.switch_card(body, key, label, desc, default)

    # ---- 「可视化」页：总开关 + 各类数据（勾选）----
    # 2026-11-19 用户要求：一颗开关同时管「读不读」和「画不画」；总开关排最上面。
    # 2026-11-21 用户要求：玩家坐标记录搬到「开发者选项」页，这一页只留「进图要看什么」。
    def build_vis_tab(self, tab, hint, items):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        by = {k: (label, desc, default) for k, label, desc, default in items}
        if "visualizer" in by:
            self.switch_card(body, "visualizer", *by["visualizer"])
        # 2026-11-20 用户要求：罗盘单独排到最后一排，前面拉一条虚线隔开
        tail = [k for k in ("vis_compass",) if k in by]
        keys = [k for k in by if k != "visualizer" and k not in tail] + tail
        box = ctk.CTkFrame(body, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(box, text="画哪些数据", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=(2, 4))
        # 2026-11-19 用户要求：并列展示；英文类名太长就在勾选项里换行，不排成一行一个。
        # CTkCheckBox 的文字不会换行，所以勾选框留空，文字用旁边可换行的 CTkLabel 画。
        txts, legends = [], []
        grow, gcol = 0, 0
        sep_done = False
        for key in keys:
            if key in tail and not sep_done:
                if gcol:                      # 虚线要独占一行：先把当前行封口
                    grow, gcol = grow + 1, 0
                self.vis_dashed_sep(grid, grow)
                grow += 1
                sep_done = True
            label, desc, default = by[key]
            var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
            self.vars[key] = var
            cell = ctk.CTkFrame(grid, fg_color="transparent")
            # sticky="nw"：同一行里说明长短不一时顶对齐，不再垂直居中错开（罗盘那排）
            cell.grid(row=grow, column=gcol, sticky="nw", padx=(0, 18), pady=6)
            row = ctk.CTkFrame(cell, fg_color="transparent")
            row.pack(anchor="w")
            cb = ctk.CTkCheckBox(row, text="", width=24, variable=var,
                                 command=lambda k=key: self.on_toggle(k))
            cb.pack(side="left", anchor="n")
            txt = ctk.CTkLabel(row, text=label, font=FONT_S, anchor="w",
                               justify="left", wraplength=200, cursor="hand2")
            txt.pack(side="left", padx=(4, 0), anchor="n")
            txt.bind("<Button-1>", lambda _e, c=cb: c.toggle())
            txts.append(txt)
            legends.append(self.vis_legend_row(cell, key, desc))
            gcol += 1
            if gcol >= 3:
                grow, gcol = grow + 1, 0
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)
        self.after(120, lambda: self.wrap_cells(body, txts, legends, 1.0))
        ctk.CTkLabel(box, text="勾上 = 进图时读这一类并画出来；关掉 = 不读也不画（少一次可能出事的读取）。\n"
                              "只影响画面，不影响 Ctrl+E 导出（导出读什么由「导出」页那 6 项决定），"
                              "也不改动游戏本身。改完重启游戏生效。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=600).pack(
            fill="x", padx=12, pady=(8, 10))

    # ---- 「开发者选项」页（2026-11-21 用户要求：单独成页，排在最后）----
    # 只放给开发 / 离线分析用的东西，正常玩图不需要：
    #   1) 开关：玩家坐标记录（要不要在本次场景画金色方块）
    #   2) 玩家坐标记录卡片：记一条 / 看列表 / 删（写 player_marks.txt，只是日志）
    #   3) 原始轨迹采集：逐帧 JSONL，交给 AI 找「跳跃 / 蹲行 / 传送」的识别阈值
    def build_dev_tab(self, tab):
        r"""控制台「开发者选项」页：可视化开关 + 玩家坐标记录 + 原始轨迹采集。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(
            body,
            text="给开发 / 离线分析用的入口，正常玩图用不到。这里只做两件事："
                 "记玩家坐标、采逐帧轨迹；都不改游戏本身，也不影响人机跑图。",
            font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
            wraplength=620).pack(fill="x", padx=12, pady=(8, 2))
        for key, label, desc, default in DEV_ITEMS:
            self.switch_card(body, key, label, desc, default)
        self.build_pmark_card(body)
        self.init_trace_state()          # 轨迹采集的运行态先备好，卡片里直接用
        self.build_trace_card(body)

    # ---- 玩家坐标记录（2026-11-21 用户要求：从「可视化」搬到「开发者选项」页）----
    def build_pmark_card(self, parent, row=None, col=None):
        r"""记录当前位置 / 列表 / 单条删除 / 全部删除。

        数据流：按钮 -> ucf_navcmd.txt 的 cmd=mark -> 插件向下打射线取脚下地面点
        -> 追加 player_marks.txt（不覆盖）-> 插件在**当前场景**画一个金色方块。
        2026-11-21 用户要求：方块只显示本次、不连折线，换图 / 重开游戏不再显示；
        文件只是日志（本卡片负责查看 / 删除）。删改由控制台直接写文件。
        """
        box = ctk.CTkFrame(parent, corner_radius=8)
        if row is None:
            box.pack(fill="x", padx=10, pady=(10, 10))
        else:
            box.grid(row=row, column=col, sticky="nsew")
        ctk.CTkLabel(box, text="玩家坐标记录", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(box, text="点一次记一条，只追加不覆盖。游戏里只在本次记下时画一个金色方块（不连折线），"
                              "换图 / 重开游戏就不再显示；坐标留在 player_marks.txt 当日志。"
                              "记录的是你脚下站的那个点（和路点同一套口径）。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w", justify="left",
                     wraplength=600).pack(fill="x", padx=12, pady=(0, 6))
        brow = ctk.CTkFrame(box, fg_color="transparent")
        brow.pack(fill="x", padx=12, pady=(0, 8))
        brow.grid_columnconfigure(0, weight=1)
        brow.grid_columnconfigure(1, weight=1)
        ctk.CTkButton(brow, text="记录当前位置",
                      command=self.pmark_record).grid(
            row=0, column=0, sticky="ew", padx=(0, 4), pady=(0, 6))
        ctk.CTkButton(brow, text="刷新", fg_color="#3a3f45", hover_color="#4a5058",
                      command=self.pmark_refresh).grid(
            row=0, column=1, sticky="ew", padx=(4, 0), pady=(0, 6))
        ctk.CTkButton(brow, text="全部删除", fg_color="#8a2b2b", hover_color="#a83232",
                      command=self.pmark_clear).grid(
            row=1, column=0, sticky="ew", padx=(0, 4))
        ctk.CTkButton(brow, text="打开文件", fg_color="#3a3f45", hover_color="#4a5058",
                      command=self.pmark_open_file).grid(
            row=1, column=1, sticky="ew", padx=(4, 0))
        self.pmark_box = ctk.CTkScrollableFrame(box, height=180, corner_radius=6)
        self.pmark_box.pack(fill="x", padx=12, pady=(0, 10))
        self.pmark_refresh()

    def pmark_read(self):
        r"""[(序号, x, y, z, 时间)] —— 空文件或没有文件都返回 []。"""
        out = []
        try:
            with open(find_log("player_marks.txt"), "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    if len(parts) < 4:
                        continue
                    try:
                        out.append((int(parts[0]), float(parts[1]), float(parts[2]),
                                    float(parts[3]), " ".join(parts[4:])))
                    except ValueError:
                        continue
        except OSError:
            pass
        return out

    def pmark_write(self, rows):
        r"""原子替换：插件正在读也不会读到半截。"""
        lines = ["# ucf player marks  x y z  time"]
        for idx, x, y, z, ts in rows:
            lines.append("%d %.3f %.3f %.3f %s" % (idx, x, y, z, ts))
        tmp = PMARK_TXT + ".tmp"
        try:
            d = os.path.dirname(PMARK_TXT)
            if d:
                os.makedirs(d, exist_ok=True)
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write("\n".join(lines) + "\n")
            os.replace(tmp, PMARK_TXT)
            return True
        except OSError as exc:
            self.set_status("写 player_marks.txt 失败：%s" % exc)
            return False

    def pmark_open_file(self):
        r"""用系统默认程序打开 player_marks.txt（文件不存在就先建一个带表头的）。"""
        if not os.path.exists(PMARK_TXT):
            try:
                d = os.path.dirname(PMARK_TXT)
                if d:
                    os.makedirs(d, exist_ok=True)
                with open(PMARK_TXT, "w", encoding="utf-8", newline="\n") as f:
                    f.write("# ucf player marks  x y z  time\n")
            except OSError as exc:
                self.set_status("创建 player_marks.txt 失败：%s" % exc)
                return
        try:
            os.startfile(PMARK_TXT)
        except OSError as exc:
            self.set_status("打开 player_marks.txt 失败：%s" % exc)
        else:
            self.set_status("已打开 player_marks.txt")

    def pmark_refresh(self):
        box = getattr(self, "pmark_box", None)
        if box is None:
            return
        for w in box.winfo_children():
            w.destroy()
        rows = self.pmark_read()
        if not rows:
            ctk.CTkLabel(box, text="还没有记录。进游戏站好位置，点「记录当前位置」。",
                         font=FONT_S, text_color="#9aa0a6", anchor="w").pack(
                fill="x", padx=8, pady=6)
            return
        for idx, x, y, z, ts in rows:
            line = ctk.CTkFrame(box, fg_color="transparent")
            line.pack(fill="x", pady=2)
            ctk.CTkButton(line, text="删", width=30, height=22,
                          fg_color="#5a2626", hover_color="#7a3030",
                          command=lambda i=idx: self.pmark_del(i)).pack(side="right", padx=(4, 0))
            col = ctk.CTkFrame(line, fg_color="transparent")
            col.pack(side="left", fill="x", expand=True, padx=(4, 0))
            ctk.CTkLabel(col, text="#%d  (%.2f, %.2f, %.2f)" % (idx, x, y, z),
                         font=FONT_S, anchor="w").pack(fill="x")
            ctk.CTkLabel(col, text=ts, font=("Microsoft YaHei UI", 11),
                         text_color="#8a9098", anchor="w").pack(fill="x")

    def pmark_record(self):
        try:
            write_nav_cmd("mark")
            self.set_status("已发送记录命令：切回游戏约 0.5 秒内记下你脚下这个点")
        except OSError as exc:
            self.set_status("写命令失败：%s" % exc)
        self.after(1200, self.pmark_refresh)

    def pmark_del(self, idx):
        rows = [r for r in self.pmark_read() if r[0] != idx]
        if self.pmark_write(rows):
            self.pmark_refresh()
            self.set_status("已删除 #%d" % idx)

    def pmark_clear(self):
        if not self.pmark_read():
            self.set_status("本来就没有记录")
            return
        if not messagebox.askyesno("全部删除", "删掉 player_marks.txt 里所有玩家坐标记录？"
                                   "已经画出来的方块要换图才会消失。"):
            return
        if self.pmark_write([]):
            self.pmark_refresh()
            self.set_status("已清空全部玩家坐标记录")

    def wrap_cells(self, body, txts, legends, frac=1.0):
        r"""按滚动区可见宽度给勾选项文字定换行；量的是画布，不是会被长文字撑大的内层。
        frac = 勾选区占整页宽度的比例（默认占满；旁边并排卡片时才 < 1）。"""
        w = body._parent_canvas.winfo_width()
        if w <= 1:                                  # 还没显示出来，下一拍再量
            self.after(120, lambda: self.wrap_cells(body, txts, legends, frac))
            return
        # 逻辑宽度扣掉：卡片左右 10、网格左右 12、滚动条余量 6；再按 frac 折算、按 3 列分
        logical = (w / self._get_window_scaling() - (10 * 2 + 12 * 2 + 6)) * frac
        textw = max(96, int(logical / 3 - 18 - 30 - 12))  # 18 列距 / 30 勾选框 / 12 余量
        for txt in txts:
            txt.configure(wraplength=textw)
        for lg in legends:                          # 图例前面还有缩进和色块，留 30
            lg.configure(wraplength=max(120, textw - 30))

    def vis_dashed_sep(self, parent, row):
        r"""跨三列的虚线分隔行：Tk 没有原生虚线，用 Canvas 一段段画。"""
        wrap = ctk.CTkFrame(parent, fg_color="transparent")
        wrap.grid(row=row, column=0, columnspan=3, sticky="ew", pady=(12, 6))
        bg = self._app_bg(wrap)
        kw = {"height": 2, "highlightthickness": 0, "bd": 0}
        if bg:
            kw["bg"] = bg
        cv = tk.Canvas(wrap, **kw)
        cv.pack(fill="x")

        def redraw(_e=None):
            cv.delete("all")
            w = cv.winfo_width()
            for x in range(0, max(w, 1), 10):
                cv.create_line(x, 1, x + 5, 1, fill="#5f6670", width=1)
        cv.bind("<Configure>", redraw)

    def _app_bg(self, widget):
        r"""往上找一个不透明的背景色，给 Canvas 当底色（Canvas 不支持 transparent）。"""
        w = widget
        while w is not None:
            try:
                c = w.cget("fg_color")
            except Exception:
                c = None
            if c and c != "transparent":
                try:
                    return w._apply_appearance_mode(c)
                except Exception:
                    return c
            w = w.master
        return None

    def vis_legend_row(self, parent, key, text):
        r"""图例行：色块 + 游戏里的形状说明（颜色和形状照抄 editor.c 的 vis_draw）。"""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(anchor="w", padx=(24, 0), pady=(2, 0))
        for c in VIS_COLORS.get(key, ()):
            ctk.CTkFrame(row, width=12, height=12, corner_radius=2,
                         fg_color=c).pack(side="left", padx=(0, 3))
        lbl = ctk.CTkLabel(row, text=text, font=FONT_S, text_color="#9aa0a6",
                           anchor="w", justify="left", wraplength=230)
        lbl.pack(side="left")
        return lbl

    # ---- 「导出」页：总开关（开关）+ 六项内容（一行多个勾选框）+ 最近导出 ----
    def build_export_tab(self, tab, hint, items):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        by = {k: (label, desc, default) for k, label, desc, default in items}
        if "export_enabled" in by:
            self.switch_card(body, "export_enabled", *by["export_enabled"])
        keys = [k for k in by if k != "export_enabled"]
        self.export_checkboxes(body, keys, by)
        self.build_export_info(body)

    def export_checkboxes(self, parent, keys, by):
        r"""导出内容：纯勾选框，一行放 3 个（用户 2026-11-18 要求）。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(box, text="导出内容", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(fill="x", padx=12, pady=(8, 2))
        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=12, pady=(2, 4))
        for idx, key in enumerate(keys):
            label, _desc, default = by[key]
            var = tk.BooleanVar(value=bool(self.feats.get(key, default)))
            self.vars[key] = var
            ctk.CTkCheckBox(grid, text=label, variable=var, font=FONT_S,
                            command=lambda k=key: self.on_toggle(k)).grid(
                row=idx // 3, column=idx % 3, sticky="w", padx=(0, 18), pady=6)
        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)
        ctk.CTkLabel(box, text="勾上 = Ctrl+E 时导出这一类；只影响导出，不影响画面。",
                     font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=590).pack(
            fill="x", padx=12, pady=(0, 10))

    # ---- 「导出」页底部：最近一次导出的文件信息 ----
    def build_export_info(self, parent):
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(12, 12))
        head = ctk.CTkFrame(box, fg_color="transparent")
        head.pack(fill="x", padx=12, pady=(8, 2))
        ctk.CTkLabel(head, text="最近一次导出", font=("Microsoft YaHei UI", 12, "bold"),
                     anchor="w").pack(side="left")
        ctk.CTkButton(head, text="打开文件夹", width=88, height=22, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=lambda: self.open_folder(vis_raw_dir(TEST))).pack(
            side="right")
        ctk.CTkButton(head, text="整理", width=56, height=22, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.tidy_vis).pack(side="right", padx=(0, 6))
        self.exp_name = ctk.CTkLabel(box, text="（还没有导出）", font=FONT_S,
                                     anchor="w", justify="left", wraplength=600)
        self.exp_name.pack(fill="x", padx=12, pady=(4, 0))
        self.exp_path = ctk.CTkLabel(box, text="", font=("Consolas", 12),
                                     anchor="w", justify="left", wraplength=600)
        self.exp_path.pack(fill="x", padx=12, pady=(4, 0))
        self.exp_time = ctk.CTkLabel(box, text="", font=FONT_S, text_color="#9aa0a6",
                                     anchor="w", justify="left", wraplength=600)
        self.exp_time.pack(fill="x", padx=12, pady=(4, 10))
        self.refresh_export_info()

    def refresh_export_info(self):
        r"""刷新「最近一次导出」：文件名 / 完整路径 / 修改时间；每 4 s 跟着状态一起刷。"""
        if not hasattr(self, "exp_name"):
            return
        hit = latest_export(TEST)
        if not hit:
            self.exp_name.configure(text="（还没有导出）")
            self.exp_path.configure(text="路径：%s（② 开发版 收件箱）" % TEST_VIS)
            self.exp_time.configure(text="修改时间：—")
            return
        fn, path, mtime = hit
        self.exp_name.configure(text="文件名：%s" % fn)
        self.exp_path.configure(text="路径：%s" % path)
        self.exp_time.configure(text="修改时间：%s" % fmt_time(mtime))

    def tidy_vis(self):
        r"""把 vis 里的导出按地图归类（tidy_vis.py 可反复跑，已归位的不会动）。"""
        if not os.path.isfile(TIDY):
            self.set_status("找不到 tidy_vis.py")
            return
        if not messagebox.askyesno(
                "整理导出",
                "把 vis 里的导出按地图归类：\n"
                "  raw\\<级别_中文名>\\<时间>_<指纹>.json\n"
                "  navmesh\\ 去重后的可走面\n"
                "  _state\\ 去重标记\n\n"
                "会删除与全局可走面完全相同的副本。继续？", parent=self):
            return
        try:
            env = dict(os.environ, PYTHONIOENCODING="utf-8")
            r = subprocess.run([sys.executable, "-u", TIDY], cwd=HERE,
                               capture_output=True, timeout=120, env=env)
            out = (r.stdout or b"").decode("utf-8", "replace").strip()
            err = (r.stderr or b"").decode("utf-8", "replace").strip()
            last = (out.splitlines() or ["(无输出)"])[-1]
            self.set_status("整理完成：%s" % (last if r.returncode == 0 else (err or last)))
        except Exception as exc:  # noqa: BLE001
            self.set_status("整理失败：%r" % exc)
            return
        self.refresh_export_info()

    # ---- 小标题（车测页用） ----
    def section_title(self, parent, text):
        ctk.CTkLabel(parent, text=text, font=("Microsoft YaHei UI", 12, "bold"),
                     text_color="#c9d1d9", anchor="w").pack(
            fill="x", padx=14, pady=(12, 0))

    # ---- 「快捷键」页：只读速查表 ----
    def text_card(self, parent, title, text, height):
        r"""深色只读文本框（和「上次运行」日志同一套配色），插完内容立刻锁死。"""
        box = ctk.CTkFrame(parent, corner_radius=8)
        box.pack(fill="x", padx=10, pady=(8, 0))
        ctk.CTkLabel(box, text=title, font=FONT, anchor="w").pack(
            fill="x", padx=12, pady=(8, 0))
        tb = ctk.CTkTextbox(box, height=height, font=("Consolas", 12),
                            fg_color="#141414", wrap="word")
        tb.pack(fill="x", padx=12, pady=(4, 10))
        tb.insert("1.0", text)
        tb.configure(state="disabled")
        return tb

    def build_hotkey_tab(self, tab, hint):
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text=hint, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=12, pady=(8, 2))
        self.text_card(body, "游戏内热键", HUD_KEYS, 330)
        ctk.CTkLabel(body, text=HUD_NOTES, font=FONT_S, text_color="#9aa0a6",
                     anchor="w", justify="left", wraplength=620).pack(
            fill="x", padx=14, pady=(10, 12))

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

    # ---- 「录制」页：录前准备 → 录制中 → 复盘（只写 ② 开发版 · 编辑中）----
    # 设计：design/record-mode.html。控制台只做三件事：
    #   1) 把 rec start/stop/pause 写进 ucf_navcmd.txt（插件的 src/editor.c rec_tick 采样）；
    #   2) 每 0.3 s 读 jsonl，调 ucf_rec 做重采样 / 跳跃 / 落下 / 岔路识别；
    #   3) 复盘确认后，把增量行追加进 ② packs\<图>\<包>\<指纹>.txt（只增不覆盖）。
    def build_record_tab(self, tab):
        r"""控制台「录制」页：录前准备 / 录制中 / 复盘三态，卡片样式跟人机路点一致。"""
        rec = self.cfg.get("rec")
        if not isinstance(rec, dict):
            rec = {}
            self.cfg["rec"] = rec
        sw = rec.get("sw")
        rec["sw"] = ucf_rec.norm_switch(sw if isinstance(sw, dict) else {})
        try:
            step = float(rec.get("step") or ucf_rec.STEP_DEFAULT)
        except (TypeError, ValueError):
            step = ucf_rec.STEP_DEFAULT
        rec["step"] = step if step in ucf_rec.STEP_OPTIONS else ucf_rec.STEP_DEFAULT
        self.rec = rec
        self.rec_state = "ready"
        self.rec_file = ""
        self.rec_samples = []
        self.rec_result = None
        self.rec_paused = False
        self.rec_busy = False
        self.rec_t0 = 0.0
        self.rec_saved = False
        self.rec_error = ""
        self.rec_sw_vars = {}
        # 原始轨迹采集的卡片在「开发者选项」页（2026-11-21 用户要求搬走），
        # 它和录制互不影响，状态由 init_trace_state() 备好。

        # 顶部常驻条：状态 + 主操作（页面再长，「开始 / 结束 / 保存」都点得到）
        top = ctk.CTkFrame(tab, corner_radius=8, fg_color="#232323",
                           border_width=1, border_color="#3a3f47")
        top.pack(fill="x", padx=10, pady=(8, 0))
        self.rec_top = top
        self.rec_badge = ctk.CTkLabel(top, text="① 录前准备", width=118, height=26,
                                      corner_radius=6, font=("Microsoft YaHei UI", 12, "bold"),
                                      fg_color="#1f2a1f", text_color="#9be09b")
        self.rec_badge.pack(side="left", padx=(10, 8), pady=9)
        self.rec_head = ctk.CTkLabel(top, text="", font=FONT_S, text_color="#9aa0a6",
                                     anchor="w", justify="left", wraplength=380)
        self.rec_head.pack(side="left", fill="x", expand=True, pady=9)
        self.rec_primary = ctk.CTkButton(
            top, text="开始录制", width=132, height=30, font=FONT,
            fg_color="#2f6fdb", hover_color="#255bb4", command=self.rec_start)
        self.rec_primary.pack(side="right", padx=(8, 10), pady=8)
        self.rec_aux = ctk.CTkButton(
            top, text="打开游戏", width=88, height=30, font=FONT_S,
            fg_color="#3a3f47", hover_color="#4a5058", command=self.launch_game)
        self.rec_aux.pack(side="right", padx=(0, 4), pady=8)
        self.rec_btn_start = self.rec_primary      # 预检按住这颗禁用/启用

        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        self.rec_body = body

        self.rec_holder = ctk.CTkFrame(body, fg_color="transparent")
        self.rec_holder.pack(fill="x")
        self.rec_ready = ctk.CTkFrame(self.rec_holder, fg_color="transparent")
        self.rec_live = ctk.CTkFrame(self.rec_holder, fg_color="transparent")
        self.rec_done = ctk.CTkFrame(self.rec_holder, fg_color="transparent")
        self.build_rec_ready(self.rec_ready)
        self.build_rec_live(self.rec_live)
        self.build_rec_done(self.rec_done)
        self.show_rec_state("ready")
        # 2026-11-21 用户要求：原始轨迹采集已搬到「开发者选项」页，这里不再放卡片

    def build_rec_ready(self, frame):
        # ① 启动条件（和人机路点共用同一份 pack_on / pack_name / pack_map）
        box = self.wp_card(frame, "启动条件", "包和地图跟「人机路点」共用；录制固定写开发版")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="启动档", font=FONT_S, text_color="#9aa0a6",
                     width=48, anchor="w").pack(side="left", padx=(0, 6))
        # 录制只写 ② 开发版（编辑中），成品档是只读的，没有第二种选法：
        # 这里只显示当前档位；万一全局停在成品，给一颗「切到编辑中」。
        self.rec_mode_lbl = ctk.CTkLabel(
            row, text="编辑中（packs·可写）", width=172, height=26,
            corner_radius=6, font=("Microsoft YaHei UI", 12, "bold"),
            fg_color="#1f2a1f", text_color="#9be09b")
        self.rec_mode_lbl.pack(side="left")
        self.rec_mode_tip = ctk.CTkLabel(
            row, text="录制只写开发版；成品档只读，录不了",
            font=("Microsoft YaHei UI", 11), text_color="#8a8f96", anchor="w")
        self.rec_mode_tip.pack(side="left", padx=(10, 0))
        self.rec_mode_btn = ctk.CTkButton(
            row, text="切到编辑中", width=88, height=26, font=FONT_S,
            fg_color="#3a3f47", hover_color="#4a5058", command=self.rec_use_edit)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="开发包", font=FONT_S, text_color="#9aa0a6",
                     width=48, anchor="w").pack(side="left", padx=(0, 6))
        self.rec_opt_pack = ctk.CTkOptionMenu(
            row, values=self._pack_values(), font=FONT_S, width=300,
            command=self.on_rec_pack)
        self.rec_opt_pack.pack(side="left")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="地图", font=FONT_S, text_color="#9aa0a6",
                     width=48, anchor="w").pack(side="left", padx=(0, 6))
        self.rec_opt_map = ctk.CTkOptionMenu(
            row, values=list(self.map_disp) or ["（没有可测的路点图）"],
            font=FONT_S, width=252, command=self.on_rec_map)
        self.rec_opt_map.pack(side="left", padx=(0, 8))
        ctk.CTkCheckBox(row, text="只对这张图生效", variable=self.pack_only,
                        font=FONT_S, checkbox_width=18, checkbox_height=18,
                        command=self.on_pack_change).pack(side="left")
        self.rec_meta = ctk.CTkLabel(box, text="", font=("Microsoft YaHei UI", 11),
                                     text_color="#9aa0a6", anchor="w",
                                     justify="left", wraplength=600)
        self.rec_meta.pack(fill="x", padx=12, pady=(6, 8))

        # ② 采样与自动识别
        box = self.wp_card(frame, "自动识别", "按这套阈值判定；关掉就不再产生这类事件")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="采样间距", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.rec_step_seg = ctk.CTkSegmentedButton(
            row, values=["2.5 m", "4 m", "6 m"], width=210, height=28,
            dynamic_resizing=False, font=FONT_S,
            selected_color="#2f6fdb", selected_hover_color="#255bb4",
            unselected_color="#2a2f36", unselected_hover_color="#343a42",
            command=self.on_rec_step)
        self.rec_step_seg.pack(side="left")
        self.rec_step_seg.set({2.5: "2.5 m", 4.0: "4 m", 6.0: "6 m"}[self.rec["step"]])
        ctk.CTkLabel(row, text="走得越细节点越多；4 m 是默认", font=FONT_S,
                     text_color="#8a8f96").pack(side="left", padx=(10, 0))

        grid = ctk.CTkFrame(box, fg_color="transparent")
        grid.pack(fill="x", padx=8, pady=(4, 4))
        for idx, (key, label, desc) in enumerate(ucf_rec.SWITCHES):
            cell = ctk.CTkFrame(grid, fg_color="transparent")
            cell.grid(row=idx // 2, column=idx % 2, sticky="nw",
                      padx=(6, 10), pady=5)
            var = tk.BooleanVar(value=bool(self.rec["sw"].get(key, True)))
            self.rec_sw_vars[key] = var
            ctk.CTkSwitch(cell, text=label, variable=var, font=FONT_S,
                          progress_color="#2f9e44",
                          command=lambda k=key: self.on_rec_switch(k)).pack(anchor="w")
            ctk.CTkLabel(cell, text=desc, font=("Microsoft YaHei UI", 11),
                         text_color="#8a8f96", anchor="w", justify="left",
                         wraplength=250).pack(anchor="w", padx=(2, 0))
        for c in range(2):
            grid.grid_columnconfigure(c, weight=1)

        # ③ 开始
        box = self.wp_card(frame, "开始录制", "控制台只发命令、读文件；走路和起跳都在游戏里")
        self.rec_pre = ctk.CTkLabel(box, text="", font=FONT_S, text_color="#9aa0a6",
                                    anchor="w", justify="left", wraplength=600)
        self.rec_pre.pack(fill="x", padx=12, pady=(6, 2))
        ctk.CTkButton(box, text="刷新状态", width=88, height=26, font=FONT_S,
                      fg_color="#2a2f36", hover_color="#343a42",
                      command=self.refresh_rec_ready).pack(anchor="w", padx=12, pady=(0, 2))
        ctk.CTkLabel(
            box,
            text="写 ② 开发版 · 编辑中：dev\\vis\\rec\\*.jsonl（原始轨迹）→ 复盘后追加进 "
                 "dev\\packs\\<图>\\<包>\\<指纹>.txt；成品 / ③ 不动。",
            font=("Consolas", 11), text_color="#8a8f96", anchor="w",
            justify="left", wraplength=600).pack(fill="x", padx=12, pady=(2, 10))

    def build_rec_live(self, frame):
        box = self.wp_card(frame, "实时轨迹", "游戏里照常走；这里只看数字")
        self.rec_big = ctk.CTkLabel(box, text="00:00 · 0.0 m", anchor="w",
                                    font=("Consolas", 22, "bold"), text_color="#f0f0f0")
        self.rec_big.pack(fill="x", padx=14, pady=(8, 0))
        self.rec_sub = ctk.CTkLabel(box, text="等第一个样本…", anchor="w",
                                    font=FONT_S, text_color="#9aa0a6")
        self.rec_sub.pack(fill="x", padx=14, pady=(0, 4))
        self.rec_live_cv = tk.Canvas(box, width=340, height=180, bg="#161616",
                                     highlightthickness=0, bd=0)
        self.rec_live_cv.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_live_cv.bind("<Configure>",
                              lambda _e: self.rec_draw(self.rec_live_cv, self.rec_result))
        self.rec_ev = ctk.CTkLabel(box, text="（还没有事件）", anchor="w", justify="left",
                                   font=("Consolas", 11), text_color="#9aa0a6",
                                   wraplength=600)
        self.rec_ev.pack(fill="x", padx=14, pady=(0, 4))
        ctk.CTkLabel(box, text="暂停 / 结束都在右上角；结束会先让插件写 end 行，再整份识别",
                     font=FONT_S, text_color="#8a8f96", anchor="w",
                     justify="left", wraplength=600).pack(fill="x", padx=14, pady=(0, 10))

    def build_rec_done(self, frame):
        box = self.wp_card(frame, "轨迹与问题", "先看图和问题，再决定存不存")
        self.rec_sum = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                    font=FONT_S, text_color="#dce4ee", wraplength=600)
        self.rec_sum.pack(fill="x", padx=14, pady=(8, 2))
        self.rec_done_cv = tk.Canvas(box, width=340, height=160, bg="#161616",
                                     highlightthickness=0, bd=0)
        self.rec_done_cv.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_done_cv.bind("<Configure>",
                              lambda _e: self.rec_draw(self.rec_done_cv, self.rec_result))
        self.rec_issue = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                      font=FONT_S, text_color="#f7cd74", wraplength=600)
        self.rec_issue.pack(fill="x", padx=14, pady=(2, 2))
        self.rec_done_ev = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                        font=("Consolas", 11), text_color="#9aa0a6",
                                        wraplength=600)
        self.rec_done_ev.pack(fill="x", padx=14, pady=(0, 6))
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_both = tk.BooleanVar(value=bool(self.rec.get("allow_both", False)))
        ctk.CTkCheckBox(row, text="跳链 / 落下也建反向边（同一处能走回来）",
                        variable=self.rec_both, font=FONT_S,
                        checkbox_width=18, checkbox_height=18,
                        command=self.on_rec_both).pack(side="left")
        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=14, pady=(2, 4))
        self.rec_btn_save = self.rec_primary      # 保存 / 重新采样都在顶部条
        ctk.CTkButton(row, text="重新录制", width=96, height=30, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=self.rec_reset).pack(side="left", padx=(8, 0))
        ctk.CTkButton(row, text="放弃", width=64, height=30, font=FONT_S,
                      fg_color="#8a1c1c", hover_color="#a32424",
                      command=self.rec_reset).pack(side="left", padx=(8, 0))
        self.rec_save_info = ctk.CTkLabel(box, text="", anchor="w", justify="left",
                                          font=FONT_S, text_color="#8a8f96",
                                          wraplength=600)
        self.rec_save_info.pack(fill="x", padx=14, pady=(0, 10))

    # ---- 录制页：状态 / 同步 / 预检 ------------------------------------
    def show_rec_state(self, state):
        self.rec_state = state
        for name, frame in (("ready", self.rec_ready), ("rec", self.rec_live),
                            ("done", self.rec_done)):
            if name == state:
                frame.pack(fill="x")
            else:
                frame.pack_forget()
        self.rec_head.configure(text={
            "ready": "选包 → 开始录制 → 进游戏走一遍路线",
            "rec": "在游戏里照目标走；空格起跳、Ctrl 蹲下都会自动记下",
            "done": "确认节点 / 边 / 跳链没问题，再写进开发包",
        }.get(state, ""))
        style = {
            "ready": ("#1f2a1f", "#9be09b"),
            "rec": ("#3a1c1c", "#ff9d9d"),
            "done": ("#1a2433", "#9cc3ff"),
        }.get(state, ("#242424", "#dce4ee"))
        self.rec_badge.configure(
            text={"ready": "① 录前准备", "rec": "● 录制中", "done": "③ 复盘"}[state],
            fg_color=style[0], text_color=style[1])
        conf = {
            "ready": ("开始录制", self.rec_start, "#2f6fdb", "#255bb4"),
            "rec": ("结束并复盘", self.rec_finish, "#2f9e44", "#37b24d"),
            "done": ("保存增量", self.rec_save, "#2f9e44", "#37b24d"),
        }.get(state)
        if conf:
            self.rec_primary.configure(text=conf[0], command=conf[1],
                                       fg_color=conf[2], hover_color=conf[3],
                                       state="normal")
        aux = {
            "ready": ("打开游戏", self.launch_game),
            "rec": ("继续" if self.rec_paused else "暂停", self.rec_pause_toggle),
            "done": ("重新采样", self.rec_review_retry),
        }.get(state)
        if aux:
            self.rec_aux.configure(text=aux[0], command=aux[1], state="normal")
            if state != "rec" or not self.rec_paused:
                self.rec_aux.configure(fg_color="#3a3f47")
            if not self.rec_aux.winfo_ismapped():
                self.rec_aux.pack(side="right", padx=(0, 4), pady=8)
        if state == "ready":
            self.refresh_rec_ready()

    def rec_sync_from_wp(self):
        r"""人机路点改了包 / 图，录制页的下拉框跟着改（两个下拉读同一个状态）。"""
        if not hasattr(self, "rec_opt_pack"):
            return
        try:
            self.rec_show_mode()
            vals = self._pack_values()
            self.rec_opt_pack.configure(values=vals)
            cur = self.opt_pack.get() if hasattr(self, "opt_pack") else ""
            if cur:
                self.rec_opt_pack.set(cur)
            self.rec_opt_map.configure(values=list(self.map_disp))
            cur = self.opt_map.get() if hasattr(self, "opt_map") else ""
            if cur:
                self.rec_opt_map.set(cur)
            state = "normal" if self.pack_on.get() else "disabled"
            self.rec_opt_pack.configure(state=state)
            self.rec_opt_map.configure(state=state)
        except Exception:
            pass

    def rec_blockers(self):
        r"""开始录制前必须满足的条件；返回人话列表（空 = 可以开始）。"""
        out = []
        if not bool(self.master_var.get()):
            out.append("插件总开关关着")
        if not self.pack_on.get():
            out.append("成品档只读，先点上面「切到编辑中」")
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        if not name:
            out.append("没选开发包")
        if not self.selected_fp():
            out.append("没选地图")
        if not game_running():
            out.append("游戏没开（先点「打开游戏」）")
        return out

    def refresh_rec_ready(self):
        if not hasattr(self, "rec_pre"):
            return
        if self.rec_state != "ready":
            return          # 录制中/复盘时别去改顶部那颗「结束 / 保存」按钮
        self.rec_sync_from_wp()
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        block = self.rec_blockers()
        if block:
            self.rec_pre.configure(text_color="#f7cd74",
                                   text="还不能开始：\n· " + "\n· ".join(block))
            self.rec_btn_start.configure(state="disabled", fg_color="#3a3f47",
                                         hover_color="#3a3f47")
        else:
            if self.rec_error:
                self.rec_pre.configure(text_color="#ff9d9d", text=self.rec_error)
            else:
                self.rec_pre.configure(
                    text_color="#9be09b",
                    text="可以开始：插件在跑，只写 ② 开发版 · 编辑中。"
                         "进游戏后点「开始录制」，走完回来点「结束并复盘」。")
            self.rec_btn_start.configure(state="normal", fg_color="#2f6fdb",
                                         hover_color="#255bb4")
        path = "dev\\packs\\" + name.replace("/", "\\") if name else "dev\\packs\\—"
        self.rec_meta.configure(
            text="指纹 %s · %s · 只写 ② 开发版（编辑中）" % (fp or "—", path))

    def rec_show_mode(self):
        r"""启动档只显示、不给选：录制只写开发版；全局停在成品时给一键切回。"""
        if not hasattr(self, "rec_mode_lbl"):
            return
        if self.pack_on.get():
            self.rec_mode_lbl.configure(text="编辑中（packs·可写）", width=172,
                                        fg_color="#1f2a1f", text_color="#9be09b")
            self.rec_mode_tip.configure(text="录制只写开发版；成品档只读，录不了")
            if self.rec_mode_btn.winfo_manager():
                self.rec_mode_btn.pack_forget()
        else:
            self.rec_mode_lbl.configure(text="成品（只读）", width=104,
                                        fg_color="#3a2c0d", text_color="#f7cd74")
            self.rec_mode_tip.configure(text="成品档不能录；切到编辑中就能开始")
            if not self.rec_mode_btn.winfo_manager():
                self.rec_mode_btn.pack(side="right")

    def rec_use_edit(self):
        r"""从录制页一键回到编辑中（和人机路点共用同一个启动档）。"""
        self.pack_on.set(True)
        self.seg_mode.set("编辑中（packs·可写）")
        self.on_page_change()
        self.refresh_rec_ready()
        self.set_status("已切到「编辑中」：录制只写 ② 开发版")

    def on_rec_pack(self, disp):
        if hasattr(self, "opt_pack"):
            self.opt_pack.set(disp)
        self.on_pack_change()

    def on_rec_map(self, disp):
        if hasattr(self, "opt_map"):
            self.opt_map.set(disp)
        self.on_pack_change()

    def on_rec_step(self, disp):
        try:
            step = float(str(disp).split()[0])
        except (TypeError, ValueError):
            step = ucf_rec.STEP_DEFAULT
        self.rec["step"] = step
        self.persist("录制采样间距")
        if self.rec_state == "done":
            self.rec_review_retry()

    def on_rec_switch(self, key):
        self.rec["sw"][key] = bool(self.rec_sw_vars[key].get())
        self.persist("录制识别开关")
        if self.rec_state == "done":
            self.rec_review_retry()

    def on_rec_both(self):
        self.rec["allow_both"] = bool(self.rec_both.get())
        self.persist("录制跳链方向")

    # ---- 录制：开始 / 轮询 / 暂停 / 结束 ---------------------------------
    def rec_start(self):
        if self.rec_state != "ready" or self.rec_busy:
            return
        block = self.rec_blockers()
        if block:
            self.set_status("还不能开始：" + block[0])
            self.refresh_rec_ready()
            return
        self.rec_error = ""
        name = self.selected_pack()
        fp = self.selected_fp()
        lv = self.map_disp.get(self.opt_map.get(), ("", "", ""))[0]
        tail = re.sub(r"[^0-9A-Za-z_-]+", "_", name.split("/")[-1])[:32] or "pack"
        try:
            os.makedirs(REC_RAW, exist_ok=True)
        except OSError as exc:
            self.set_status("建不了录制目录：%s" % exc)
            return
        self.rec_file = os.path.join(
            REC_RAW, "%s_%s_%s.jsonl" % (lv or "map", tail,
                                         time.strftime("%Y%m%d-%H%M%S")))
        self.rec_samples = []
        self.rec_result = None
        self.rec_saved = False
        self.rec_paused = False
        self.rec_busy = True
        try:
            seq = write_nav_cmd("rec", "", "", {"act": "start", "out": self.rec_file,
                                                "hz": 20})
        except OSError as exc:
            self.rec_busy = False
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.rec_error = ""
        self.rec_t0 = time.time()
        self.set_status("已发送 #%d：等插件开始录（%s）" % (seq, os.path.basename(self.rec_file)))
        self.show_rec_state("rec")
        self.rec_aux.configure(text="暂停", fg_color="#3a3f47")
        self.rec_big.configure(text="00:00 · 等待插件…")
        self.rec_sub.configure(text="插件每 0.5 s 看一次命令；还没写文件就是还没开始")
        self.rec_ev.configure(text="（还没有事件）")
        self.rec_live_cv.delete("all")
        self.after(400, self.rec_wait_start)

    def rec_wait_start(self):
        r"""等插件建文件 / 等第一个样本。

        插件一收到命令就会 fopen 建文件（哪怕人在大厅还没进图），所以：
          · 文件在、还是 0 字节 = 插件支持录制，在等进图 -> 最多等 90 s；
          · 文件一直没出现 = 插件没收到/没这个命令 -> 8 s 后报错（能认出旧 DLL）。
        """
        if self.rec_state != "rec":
            return
        try:
            size = os.path.getsize(self.rec_file)
        except OSError:
            size = -1
        elapsed = time.time() - self.rec_t0
        if size >= 0:
            self.rec_busy = False        # 文件建出来了就算开始成功，随时可以「结束」
        if size > 0:
            self.set_status("录制中：写 %s" % os.path.basename(self.rec_file))
            self.after(250, self.rec_poll)
            return
        if not game_running(fresh=True):
            self.rec_start_fail("游戏关掉了：录制停止（已录到的样本还在文件里）")
            return
        if size == 0:
            if elapsed < 90.0:
                self.rec_big.configure(text="等待进图…")
                self.rec_sub.configure(
                    text="插件已建文件（%d s）；进图后第一个样本就会开始写" % int(elapsed))
                self.after(500, self.rec_wait_start)
                return
            self.rec_start_fail("文件建了但 90 s 没有样本：确认已经进图（大厅没有可录的位置）")
            return
        if elapsed < 8.0:
            self.rec_sub.configure(text="已发命令，等插件建文件…")
            self.after(300, self.rec_wait_start)
            return
        tip = tail_log(30) or ""
        if "unknown cmd 'rec'" in tip:
            self.rec_start_fail(
                "插件不是带录制接口的版本：这个 ucf_mod.dll 里没有 rec 命令。"
                "先跑 tools\\build.ps1 -Deploy 再启动游戏。")
        else:
            self.rec_start_fail(
                "插件没开始录：确认游戏已进图、插件总开关开着；"
                "再看 log\\ucf_mod.log 的 navcmd / rec 行。")

    def rec_start_fail(self, msg):
        self.rec_busy = False
        self.rec_error = msg
        try:
            write_nav_cmd("rec", "", "", {"act": "stop"})
        except OSError:
            pass
        self.set_status(msg)
        self.show_rec_state("ready")

    def rec_poll(self):
        if self.rec_state != "rec":
            return
        try:
            with open(self.rec_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            lines = []
        samples = ucf_rec.parse_lines(lines)
        self.rec_samples = samples
        if samples:
            res = ucf_rec.analyse(samples, step=self.rec["step"], sw=self.rec["sw"])
            self.rec_result = res
            self.rec_update_live(res, samples)
        if not game_running(fresh=True):
            self.rec_finish(auto=True)
            return
        self.after(350, self.rec_poll)

    def rec_update_live(self, res, samples):
        if not samples:
            return
        dur = samples[-1]["t"] - samples[0]["t"]
        self.rec_big.configure(text="%02d:%02d · %.1f m" % (
            int(dur // 60), int(dur % 60), res.get("dist", 0.0)))
        if res.get("ok"):
            self.rec_sub.configure(text="%d 样本 · %d 节点 / %d 边 · 跳 %d / 落 %d / 岔 %d%s" % (
                res["samples"], res["nodes"], res["edges"], len(res["jumps"]),
                len(res["drops"]), len(res["branches"]),
                (" · 已暂停" if self.rec_paused else "")))
        else:
            self.rec_sub.configure(text="%d 样本 · %s" % (
                res["samples"], res.get("why") or "还在识别"))
        self.rec_ev.configure(text="\n".join(self.rec_event_lines(res)))
        self.rec_draw(self.rec_live_cv, res)

    def rec_event_lines(self, res):
        ev = []
        for j in res.get("jumps", [])[-2:]:
            ev.append("跳箱 · 水平 %.1f m · 按空格" % j["h"])
        for d in res.get("drops", [])[-2:]:
            ev.append("落下 · 下降 %.1f m%s" % (
                d["drop"], " · 可能摔伤" if d.get("hurt") else " · 落差 ≥ 2 m"))
        for b in res.get("branches", [])[:2]:
            ev.append("岔路候选 · 2.5 m 内回访 · 绕 %.0f m" % b["gap"])
        for c in res.get("crouches", [])[:2]:
            ev.append("蹲点 · 蹲 %.1f s · 位移 < 1 m" % c["t"])
        for st in res.get("statics", [])[:1]:
            ev.append("静止 %.1f s · 采样照常" % st["t"])
        return ev[-4:] or ["（还没有事件）"]

    def rec_pause_toggle(self):
        if self.rec_state != "rec" or not self.rec_file:
            return
        self.rec_paused = not self.rec_paused
        act = "pause" if self.rec_paused else "resume"
        try:
            write_nav_cmd("rec", "", "", {"act": act})
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            self.rec_paused = not self.rec_paused
            return
        self.rec_aux.configure(
            text="继续" if self.rec_paused else "暂停",
            fg_color="#8a5a1c" if self.rec_paused else "#3a3f47")
        self.set_status("已暂停录制（jsonl 不再追加）" if self.rec_paused else "继续录制")

    def rec_finish(self, auto=False):
        if self.rec_state != "rec":
            return
        self.rec_busy = False            # 等待进图时也能直接结束（会提示没录到东西）
        try:
            write_nav_cmd("rec", "", "", {"act": "stop"})
        except OSError:
            pass
        if auto:
            self.set_status("游戏已退出，自动收尾…")
        self.after(700, self.rec_review_from_file)

    def rec_review_from_file(self):
        self.rec_busy = False
        try:
            with open(self.rec_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except OSError:
            lines = []
        samples = ucf_rec.parse_lines(lines)
        self.rec_samples = samples
        res = ucf_rec.analyse(samples, step=self.rec["step"], sw=self.rec["sw"])
        self.rec_result = res
        if not res.get("ok"):
            self.rec_error = "这次没录到东西：%s" % (res.get("why") or "没有数据")
            self.set_status("复盘失败：%s" % (res.get("why") or "没有数据"))
            self.show_rec_state("ready")
            return
        self.rec_saved = False
        self.show_rec_state("done")
        self.rec_fill_done(res)
        self.set_status("复盘完成：%s" % ucf_rec.summary(res))

    def rec_fill_done(self, res):
        self.rec_sum.configure(text=ucf_rec.summary(res))
        lines = self.rec_event_lines(res)
        self.rec_done_ev.configure(text="\n".join(lines))
        iss = res.get("issues") or []
        self.rec_issue.configure(text=("· " + "\n· ".join(iss)) if iss else "没有发现问题")
        self.rec_draw(self.rec_done_cv, res)
        self.rec_btn_save.configure(state="normal", fg_color="#2f9e44",
                                    hover_color="#37b24d")
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        self.rec_save_info.configure(
            text="目标：dev\\packs\\%s\\%s.txt · 只增不覆盖 → 失败自动回滚"
                 % (name.replace("/", "\\") if name else "—", fp or "—"))

    def rec_review_retry(self):
        if not self.rec_samples:
            return
        res = ucf_rec.analyse(self.rec_samples, step=self.rec["step"], sw=self.rec["sw"])
        self.rec_result = res
        if res.get("ok"):
            self.rec_saved = False
            self.rec_fill_done(res)
            self.set_status("已按当前阈值重新采样：%s" % ucf_rec.summary(res))
        else:
            self.set_status("重新采样失败：%s" % (res.get("why") or "没有数据"))

    def rec_reset(self):
        self.rec_result = None
        self.rec_samples = []
        self.rec_paused = False
        self.rec_busy = False
        self.rec_saved = False
        self.rec_error = ""
        self.show_rec_state("ready")

    def rec_save(self):
        if self.rec_state != "done" or not self.rec_result:
            return
        if self.rec_saved:
            return
        name = self.selected_pack() if hasattr(self, "opt_pack") else ""
        fp = self.selected_fp() if hasattr(self, "opt_map") else ""
        if not name or not fp:
            self.set_status("先选开发包和地图")
            return
        if not self.pack_on.get():
            self.set_status("成品档只读：切回「编辑中」再保存")
            return
        lines = ucf_rec.save_lines(self.rec_result, allow_both=bool(self.rec_both.get()))
        if not lines:
            self.set_status("没有可保存的节点 / 边")
            return
        path = pack_txt(name, fp)
        if not path:
            path = os.path.join(pack_dir(name), fp + ".txt")
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            existing = ""
            if os.path.isfile(path):
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    existing = f.read()
            new = ucf_rec.dedupe_lines(lines, existing)
            if not new:
                self.set_status("这些节点 / 边包里已经有了（按 0.35 m 去重）")
                self.rec_saved = True
                self.rec_save_info.configure(text="没有新增：包里已经有这条路线")
                return
            prefix = ""
            if not existing:
                man = pack_manifest(name)
                mode = "grow" if (man.get("grow") or man.get("blank")) else "keep"
                prefix = "# ucf-navedit v1 fp=%s\n%s\n" % (fp, mode)
            ts = time.strftime("%Y%m%d-%H%M%S")
            if os.path.isfile(path):
                shutil.copy2(path, path + ".bak-rec-" + ts)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                f.write(existing or prefix)
                if not (existing or prefix).endswith("\n"):
                    f.write("\n")
                f.write("\n".join(new) + "\n")
            os.replace(tmp, path)
        except OSError as exc:
            self.set_status("保存失败（原文件没动）：%s" % exc)
            return
        self.rec_saved = True
        self.rec_primary.configure(state="disabled", fg_color="#2a332a",
                                   hover_color="#2a332a")
        rel = "dev\\packs\\%s\\%s.txt" % (name.replace("/", "\\"), fp)
        self.rec_save_info.configure(text="已保存 %d 行 → %s" % (len(new), rel))
        self.set_status("已保存到开发包：%s（+%d 行）" % (rel, len(new)))
        if game_running():
            try:
                write_nav_cmd("apply", name, fp)
                self.set_status("已保存到开发包并通知插件重新载入（%s）" % rel)
            except OSError:
                pass

    # ---- 开发者选项页：原始轨迹采集（2026-11-21 用户要求：原先在录制页，已搬走）----
    # 录制 = 走一遍 -> 重采样成路点；这里 = 把每一帧原样写下来，交给离线分析
    # （AI）找「跳跃 / 跳下 / 蹲行 / 上梯 / 传送」到底该用哪些信号识别。
    def init_trace_state(self):
        r"""轨迹采集的运行态（和录制互不影响，自己一份；建卡片前必须先调）。"""
        trace = self.cfg.get("trace")
        if not isinstance(trace, dict):
            trace = {}
            self.cfg["trace"] = trace
        try:
            thz = int(trace.get("hz") or 20)
        except (TypeError, ValueError):
            thz = 20
        trace["hz"] = thz if thz in ucf_trace.GEARS else 20
        self.trace = trace
        self.tr_state = "idle"
        self.tr_file = ""
        self.tr_off = 0
        self.tr_lines = 0
        self.tr_last_t = 0.0
        self.tr_t0 = 0.0
        self.tr_hz = 0                 # 正在采的这份日志的档位（改档位不影响它）

    def build_trace_card(self, parent):
        r"""「开发者选项」页的「原始轨迹采集」卡：档位 / 开始停止 / 文件名 / 目录。"""
        box = self.wp_card(parent, "原始轨迹采集（给 AI 分析用）",
                           "不重采样、不生成路点；每个样本一行 JSON")

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="频率档位", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.tr_seg = ctk.CTkSegmentedButton(
            row, values=["%d Hz" % h for h in ucf_trace.GEARS], width=250, height=28,
            dynamic_resizing=False, font=FONT_S,
            selected_color="#2f6fdb", selected_hover_color="#255bb4",
            unselected_color="#2a2f36", unselected_hover_color="#343a42",
            command=self.on_trace_hz)
        self.tr_seg.pack(side="left")
        self.tr_seg.set("%d Hz" % self.trace["hz"])
        ctk.CTkLabel(row, text="越高越细；10 Hz ≈ 7 MB/小时，60 Hz ≈ 40 MB",
                     font=FONT_S, text_color="#8a8f96").pack(side="left", padx=(10, 0))

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(8, 0))
        self.tr_btn_start = ctk.CTkButton(
            row, text="开始采集", width=100, height=30, font=FONT,
            fg_color="#2f6fdb", hover_color="#255bb4", command=self.trace_start)
        self.tr_btn_start.pack(side="left")
        self.tr_btn_stop = ctk.CTkButton(
            row, text="停止", width=72, height=30, font=FONT_S,
            fg_color="#3a3f47", hover_color="#4a5058", state="disabled",
            command=self.trace_stop)
        self.tr_btn_stop.pack(side="left", padx=(8, 0))
        self.tr_btn_dir = ctk.CTkButton(
            row, text="打开日志文件夹", width=124, height=30, font=FONT_S,
            fg_color="#2a2f36", hover_color="#343a42", command=self.trace_open_dir)
        self.tr_btn_dir.pack(side="right")
        self.tr_btn_file = ctk.CTkButton(
            row, text="打开日志", width=84, height=30, font=FONT_S,
            fg_color="#2a2f36", hover_color="#343a42", command=self.trace_open_file)
        self.tr_btn_file.pack(side="right", padx=(0, 6))
        ctk.CTkButton(
            row, text="复制路径", width=84, height=30, font=FONT_S,
            fg_color="#2a2f36", hover_color="#343a42",
            command=self.trace_copy_path).pack(side="right", padx=(0, 6))

        self.tr_stat = ctk.CTkLabel(box, text="未开始", font=FONT_S,
                                    text_color="#9aa0a6", anchor="w",
                                    justify="left", wraplength=600)
        self.tr_stat.pack(fill="x", padx=12, pady=(6, 0))

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 0))
        ctk.CTkLabel(row, text="日志文件", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.tr_file_lbl = ctk.CTkLabel(
            row, text="（还没有）", font=("Consolas", 11), text_color="#dce4ee",
            anchor="w", justify="left", wraplength=520)
        self.tr_file_lbl.pack(side="left", fill="x", expand=True)

        row = ctk.CTkFrame(box, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(4, 0))
        ctk.CTkLabel(row, text="日志目录", font=FONT_S, text_color="#9aa0a6",
                     width=64, anchor="w").pack(side="left", padx=(0, 6))
        self.tr_dir_lbl = ctk.CTkLabel(
            row, text=ucf_trace.DIR, font=("Consolas", 11), text_color="#8a8f96",
            anchor="w", justify="left", wraplength=520)
        self.tr_dir_lbl.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            box,
            text="每行：t 相对秒 / dt 距上一样本 / x,y,z 相机 / gy 脚下地面（null=没打到）/ "
                 "fx,fy,fz 朝向 / sp 空格 ct Ctrl sh Shift / w a s d 方向键。"
                 "首行 header 记地图 / 包 / 频率；换图会插一行 ev=scene。",
            font=("Microsoft YaHei UI", 11), text_color="#8a8f96", anchor="w",
            justify="left", wraplength=600).pack(fill="x", padx=12, pady=(6, 10))

        last = ucf_trace.latest()
        if last:
            self.trace_show_file(last)
            self.tr_stat.configure(text="上次日志还在目录里：%s"
                                   % os.path.basename(last))

    def on_trace_hz(self, disp):
        try:
            hz = int(str(disp).split()[0])
        except (TypeError, ValueError):
            hz = 20
        if hz not in ucf_trace.GEARS:
            hz = 20
        self.trace["hz"] = hz
        try:
            save_cfg(self.cfg)
        except OSError:
            pass
        self.set_status("轨迹采集频率：%d Hz（下一份日志生效）" % hz)
        if self.tr_state in ("starting", "running", "stopping"):
            self.tr_stat.configure(text="档位改动从下一份日志生效（当前这份按开始时的频率写）")

    def trace_start(self):
        if self.tr_state in ("starting", "running", "stopping"):
            return
        if not game_running(fresh=True):
            self.set_status("游戏没跑：先开游戏再点「开始采集」（插件只在游戏进程里写文件）")
            return
        lv, lab, fp = self.map_disp.get(self.opt_map.get(), ("", "", ""))
        pid = self.selected_pack() if hasattr(self, "opt_pack") else ""
        try:
            os.makedirs(ucf_trace.DIR, exist_ok=True)
        except OSError as exc:
            self.set_status("建不了轨迹目录：%s" % exc)
            return
        self.tr_file = ucf_trace.make_path(lv or "map")
        self.tr_hz = self.trace["hz"]
        self.tr_off = 0
        self.tr_lines = 0
        self.tr_last_t = 0.0
        self.tr_t0 = time.time()
        try:
            seq = write_nav_cmd("trace", pid, fp or self.selected_fp(),
                                {"act": "start", "out": self.tr_file,
                                 "hz": self.trace["hz"],
                                 "map": lv or "", "label": lab or ""})
        except OSError as exc:
            self.set_status("写不进 ucf_navcmd.txt：%s" % exc)
            return
        self.tr_state = "starting"
        self.tr_btn_start.configure(state="disabled")
        self.tr_btn_stop.configure(state="normal")
        self.trace_show_file(self.tr_file)
        self.tr_stat.configure(
            text="已发命令 #%d（%d Hz），等插件建文件…" % (seq, self.trace["hz"]),
            text_color="#9aa0a6")
        self.set_status("轨迹采集：等插件开始写 %s" % os.path.basename(self.tr_file))
        self.after(400, self.trace_poll)

    def trace_poll(self):
        if self.tr_state not in ("starting", "running", "stopping"):
            return
        try:
            size = os.path.getsize(self.tr_file)
        except OSError:
            size = -1
        if size < 0:
            if self.tr_state == "starting" and time.time() - self.tr_t0 < 8.0:
                self.after(400, self.trace_poll)
                return
            if self.tr_state == "starting":
                self.trace_fail(
                    "插件没建文件：确认游戏在跑，且 DLL 是带 trace 的新版"
                    "（先 tools\\build.ps1 -Deploy，再重开游戏）")
                return
            self.after(600, self.trace_poll)
            return
        if self.tr_state == "starting":
            self.tr_state = "running"
        try:
            off, n, last, end = ucf_trace.scan(self.tr_file, self.tr_off)
        except OSError:
            off, n, last, end = self.tr_off, 0, None, None
        self.tr_off = off
        self.tr_lines += n
        if last is not None:
            self.tr_last_t = float(last.get("t") or 0.0)
        if size == 0:
            if not game_running(fresh=True):
                self.trace_finish(auto=True)
                return
            self.tr_stat.configure(text="等待进图…（插件已建文件；进图后写第一个样本）")
            self.after(700, self.trace_poll)
            return
        self.trace_live(size)
        if end is not None:
            self.trace_finish(auto=True)
            return
        if not game_running(fresh=True):
            self.trace_finish(auto=True)
            return
        self.after(500, self.trace_poll)

    def trace_live(self, size):
        dur = max(0.0, self.tr_last_t)
        hz = (self.tr_lines - 1) / dur if dur > 0.5 and self.tr_lines > 1 else 0.0
        self.tr_stat.configure(
            text="● 采集中 %02d:%02d · %d 样本 · %.1f KB · 实测 %.1f Hz（档位 %d Hz）"
                 % (int(dur) // 60, int(dur) % 60, self.tr_lines, size / 1024.0,
                    hz, self.tr_hz or self.trace["hz"]),
            text_color="#ff9d9d")

    def trace_stop(self):
        if self.tr_state not in ("starting", "running"):
            return
        try:
            write_nav_cmd("trace", "", "", {"act": "stop"})
        except OSError:
            pass
        self.tr_state = "stopping"
        self.tr_btn_stop.configure(state="disabled")
        self.tr_stat.configure(text="正在收尾（插件写 end 行）…", text_color="#9aa0a6")
        self.after(600, self.trace_finish)

    def trace_finish(self, auto=False):
        if self.tr_state in ("idle", "stopped"):
            return
        if self.tr_file:
            try:
                off, n, last, _end = ucf_trace.scan(self.tr_file, self.tr_off)
                self.tr_off = off
                self.tr_lines += n
                if last is not None:
                    self.tr_last_t = float(last.get("t") or 0.0)
            except OSError:
                pass
        self.tr_state = "stopped"
        self.tr_btn_start.configure(state="normal")
        self.tr_btn_stop.configure(state="disabled")
        if self.tr_lines <= 0:
            self.tr_stat.configure(
                text="已停止：没有样本（人没进图，或插件不是带 trace 的版本）",
                text_color="#f7cd74")
            self.set_status("轨迹采集停止：没有样本")
            return
        try:
            sm = ucf_trace.summary(self.tr_file)
            txt = ucf_trace.summary_text(sm)
        except OSError:
            txt = "%d 样本" % self.tr_lines
        head = "已收尾 · " if auto else "已停止 · "
        self.tr_stat.configure(text=head + txt, text_color="#9aa0a6")
        self.set_status(head + txt + " → " + os.path.basename(self.tr_file))

    def trace_fail(self, msg):
        self.tr_state = "idle"
        self.tr_btn_start.configure(state="normal")
        self.tr_btn_stop.configure(state="disabled")
        self.tr_stat.configure(text=msg, text_color="#f7cd74")
        self.set_status(msg)

    def trace_show_file(self, path):
        self.tr_file = path or ""
        self.tr_file_lbl.configure(text=os.path.basename(path) if path else "（还没有）")

    def trace_open_dir(self):
        try:
            os.makedirs(ucf_trace.DIR, exist_ok=True)
        except OSError as exc:
            self.set_status("建不了轨迹目录：%s" % exc)
            return
        try:
            os.startfile(ucf_trace.DIR)      # noqa: S606  Windows 专用
        except OSError as exc:
            self.set_status("打不开目录：%s" % exc)
            return
        self.set_status("已打开轨迹目录：%s" % ucf_trace.DIR)

    def trace_open_file(self):
        path = self.tr_file
        if not path or not os.path.isfile(path):
            self.set_status("还没有轨迹文件：先点「开始采集」")
            return
        try:
            os.startfile(path)               # noqa: S606  Windows 专用
        except OSError as exc:
            self.set_status("打不开日志：%s" % exc)

    def trace_copy_path(self):
        path = self.tr_file
        if not path:
            self.set_status("还没有轨迹文件")
            return
        try:
            self.clipboard_clear()
            self.clipboard_append(path)
        except tk.TclError:
            pass
        self.set_status("已复制路径：%s" % path)

    def rec_draw(self, cv, res, live=False):
        r"""复盘 / 录制中的 2D 图：走路绿线、跳链黄虚线、落下橙虚线、节点蓝点。"""
        try:
            cv.delete("all")
            w = int(cv.winfo_width())
            h = int(cv.winfo_height())
            if w <= 10:
                w = 340
            if h <= 10:
                h = 170
            if not res or not res.get("ok") or not res.get("pieces"):
                cv.create_text(w // 2, h // 2, text="还没有轨迹",
                               fill="#6b7280", font=("Microsoft YaHei UI", 11))
                return
            pts = []
            for piece in res["pieces"]:
                pts.extend(piece["nodes"])
            if not pts:
                return
            minx = min(p[0] for p in pts)
            maxx = max(p[0] for p in pts)
            minz = min(p[2] for p in pts)
            maxz = max(p[2] for p in pts)
            pad = 16
            spanx = max(0.001, maxx - minx)
            spanz = max(0.001, maxz - minz)
            s = min((w - pad * 2) / spanx, (h - pad * 2) / spanz, 40.0)
            x0 = (w - spanx * s) / 2.0
            z0 = (h - spanz * s) / 2.0

            def P(p):
                return (x0 + (p[0] - minx) * s, h - z0 - (p[2] - minz) * s)

            for piece in res["pieces"]:
                nodes = piece["nodes"]
                for i, j in piece.get("walk", []):
                    a, b = P(nodes[i]), P(nodes[j])
                    cv.create_line(a[0], a[1], b[0], b[1], fill="#3f6b52", width=2)
            for link in res.get("links", []):
                a, b = P(link["a"]), P(link["b"])
                jump = link["kind"] == "jump"
                cv.create_line(a[0], a[1], b[0], b[1],
                               fill="#f2cc47" if jump else "#ff8c0d",
                               width=2, dash=(5, 3))
            for p in pts:
                x, y = P(p)
                cv.create_oval(x - 2, y - 2, x + 2, y + 2,
                               fill="#cfe0ff", outline="")
            for j in res.get("jumps", []):
                x, y = P(j["a"])
                cv.create_oval(x - 4, y - 4, x + 4, y + 4, outline="#f2cc47", width=2)
            for d in res.get("drops", []):
                x, y = P(d["a"])
                cv.create_oval(x - 4, y - 4, x + 4, y + 4, outline="#ff8c0d", width=2)
            for b in res.get("branches", []):
                x, y = P(b["p"])
                cv.create_oval(x - 5, y - 5, x + 5, y + 5, outline="#ffd43b")
            if pts:
                x, y = P(pts[0])
                cv.create_oval(x - 4, y - 4, x + 4, y + 4, fill="#2f9e44", outline="")
        except tk.TclError:
            pass

    # ---- 「人机路点」页内：编辑中 / 成品 两页 ------------------------------
    def build_sub_tabs(self, parent, names):
        r"""页内标签：一行按钮 + 一组内容框，一次只显示一个。

        没用 CTkTabview：对比表是运行时重建的，Tabview 的高度不会跟着内容长。
        """
        bar = ctk.CTkFrame(parent, fg_color="transparent")
        bar.pack(fill="x", padx=10, pady=(8, 0))
        holder = ctk.CTkFrame(parent, fg_color="transparent")
        holder.pack(fill="x")
        btns, frames = {}, {}
        for name in names:
            frames[name] = ctk.CTkFrame(holder, fg_color="transparent")
            btns[name] = ctk.CTkButton(bar, text=name, width=112, height=28,
                                       font=FONT_S, corner_radius=6)
            btns[name].pack(side="left", padx=(0, 6))

        def show(name):
            for key, frame in frames.items():
                if key == name:
                    frame.pack(fill="x")
                else:
                    frame.pack_forget()
            for key, btn in btns.items():
                on = key == name
                btn.configure(fg_color="#2f6fdb" if on else "#2a2f36",
                              hover_color="#255bb4" if on else "#343a42",
                              text_color="#ffffff" if on else "#9aa0a6")
        for name in names:
            btns[name].configure(command=lambda n=name: show(n))
        show(names[0])
        return frames, show

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

    # ---- 数据页：三区在哪 / 什么时候写的 / 一致不一致（原来三个 .bat 的活）----
    def build_data_tab(self, tab):
        r"""① 备份版 / ② 开发版 / ③ 游戏目录（运行时）的路径、最近写入时间、条数，
        外加 发布到成品（编辑中→成品）/ 还原 ①→② / 校验 ① 的按钮。"""
        body = ctk.CTkScrollableFrame(tab, corner_radius=0, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=2, pady=2)
        ctk.CTkLabel(body, text="① 只读快照；② 唯一数据源：一张图一个文件夹（map.json + navmesh.bin），另有 final 成品、packs 编辑中、vis 收件箱；"
                               "③ 游戏目录只当运行环境，不放数据。\n"
                               "数据流：游戏导出 → ② vis →（整理导出）→ ② <图>\\导出\\ + <图>\\map.json；"
                               "测试包做完 →（发布到成品）→ ② final\\<版本>（每次发布默认新增一版）。",
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
            self.lbl_same.configure(text="一致性：读不动某个版本")
            return
        n12 = diff_count(d1, d2)
        n_exp = test_stats(DEV)[0]
        _vers = final_versions()
        n_fin = len((next((v for v in _vers if v["name"] == final_current_name()), None) or {}
                     ).get("maps") or {}) if _vers else 0
        self.lbl_same.configure(
            text=r"一致性（只比每张图的 map.json 与路线 txt，索引与 names.json 不算）："
                 + ("①=②（工作区还没改动）" if n12 == 0 else "① vs ② 有 %d 个文件不同" % n12)
                 + " · 成品 %d 个版本（当前版 %d 张图）" % (len(_vers), n_fin)
                 + " · " + ("收件箱没有导出" if n_exp == 0
                            else "收件箱有 %d 份导出待整理" % n_exp))

    def refresh_dev_rows(self):
        r"""② 卡拆三块报数（成品 / 编辑中 / 收件箱），各算各的，别再挤成一行：
        以前「9 图」是 maps 里的、「8 可走面」是 vis 里的，看着像同一份数据。"""
        rows = getattr(self, "dev_rows", None)
        if not rows:
            return
        # —— 成品：几个版本 / 当前那版几张图 / 所有版本占多大 ——
        vers = final_versions()
        cur = final_current_name()
        n_maps = n_bytes = 0
        latest = 0.0
        for v in vers:
            size, mt = dir_bytes(os.path.join(FINAL_ROOT, str(v.get("name") or "")))
            n_bytes += size
            latest = max(latest, mt)
            if str(v.get("name") or "") == cur:
                n_maps = len(v.get("maps") or {})
        if vers:
            rows["final"].configure(text="%d 个版本 · 当前 %s · %d 张图 · %s · 最近\u00a0%s" % (
                len(vers), (cur or "没选（启动 = 原版）"), n_maps,
                human_size(n_bytes), fmt_short(latest)))
        else:
            rows["final"].configure(
                text="没有版本（启动成品 = 原版）· 去「编辑中」选包 → 发布到成品，就有第一版")

        # —— 编辑中：几个测试包 / 包里几张图 / 占多大 + 包名 ——
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
            # 包名之间用「、 」隔开（后面留个空格）：Tk 只在空格处断行，
            # 连写「、」会变成一个超长单词，窄窗口下把包名从中间劈开。
            shown = [x.split("/")[-1] for x in names[:4]]
            if len(names) > len(shown):
                shown.append("等 %d 个" % len(names))
            rows["packs"].configure(text="%d 个测试包 · %d 张图 · %s · 最近\u00a0%s\n%s" % (
                len(names), n_txt, human_size(p_bytes), fmt_short(p_latest),
                "、 ".join(shown)))
        else:
            rows["packs"].configure(
                text="没有测试包（「人机路点」页选张图，画完保存就是一个包）")

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

    def open_file(self, path, what):
        if not os.path.isfile(path):
            self.set_status("还没有 %s" % what)
            return
        try:
            os.startfile(path)      # noqa: SLF001  Windows 资源管理器
            self.set_status("已打开 %s" % what)
        except OSError as exc:
            self.set_status("打不开 %s：%s" % (what, exc))

    def refresh_at(self):
        r"""autotest.txt 最后一条 RESULT → 「上一次车测」；没有 RESULT 说明中途被杀/崩了。"""
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

    def _at_int(self, var, default):
        try:
            return max(0, int(str(var.get()).strip()))
        except (TypeError, ValueError):
            return default

    def run_autotest(self):
        if self.at_busy:
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

    def on_tab(self, name=None, persist=True):
        r"""页签切换：刷新这一页的数据，并把「上次停在哪」写进 ucf_mod.json。
        CTkTabview 的 command 不传参数，name 为空时自己读当前页签。"""
        if not name:
            name = self.tabview.get()
        self.save_autotest_ui()          # 离开车测页时把改过的参数带走
        self.ui["tab"] = name
        if persist:
            try:
                save_cfg(self.cfg)
            except OSError:
                pass
        if name == "数据":
            self.refresh_data()
        elif name == "导出":
            self.refresh_export_info()
        elif name == "车测":
            self.refresh_at()
        elif name == "录制":
            self.rec_sync_from_wp()
            self.refresh_rec_ready()
        elif name == "开发者选项":
            self.pmark_refresh()         # 文件可能被编辑器 / 手改过，进来重读
        elif name == "人机路点":
            if hasattr(self, "opt_pack"):
                cur = self.selected_pack()
                self.opt_pack.configure(values=self._pack_values())   # 编辑器新存的包也刷进来
                if cur and self.disp_of(cur):
                    self.opt_pack.set(self.disp_of(cur))
            self.refresh_wp_tab()

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

    # ---- 写盘 ----
    def persist(self, note=""):
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
        if game_running():
            msg += " · 游戏在运行，重启游戏才生效"
        self.set_status(msg)

    def on_toggle(self, key):
        self.persist(key)

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
        再点「展开」按原尺寸、原位置回来。折叠条宽度按标题行实际内容收窄，不留空档。"""
        if not self._folded:
            self._geom_saved = str(self.tk.call("wm", "geometry", self))
            self._folded = True
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

    def on_close(self):
        r"""关窗口 = 最后一次落盘：正停在哪个页签、车测输入框里没失焦的数字都不丢。"""
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
        tab = self.tabview.get()
        if tab:
            self.ui["tab"] = tab
        try:
            save_cfg(self.cfg)
        except OSError:
            pass
        self.destroy()

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

    def open_folder(self, path):
        r"""数据页每张卡旁边的「打开文件夹」：不存在就提示，不替用户创建。"""
        if not os.path.isdir(path):
            self.set_status("目录不存在：%s" % path)
            return
        try:
            os.startfile(path)      # noqa: SLF001  Windows 资源管理器
        except OSError as exc:
            self.set_status("打不开目录：%s" % exc)
            return
        self.set_status("已打开：%s" % path)

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
        self.refresh_export_info()
        if hasattr(self, "wp_meta"):
            self.refresh_wp_status()
        self.refresh_launch_strip(running)
        self.after(4000, self.refresh_status)

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

    def ask_text(self, title, prompt, initial=""):
        r"""一句话输入框（成品版本改名用）；取消返回空串。"""
        out = {"v": ""}
        top = ctk.CTkToplevel(self)
        top.title(title)
        top.resizable(False, False)
        top.transient(self)
        if bool(self.topmost_var.get()):
            top.attributes("-topmost", True)
        try:
            top.grab_set()
        except tk.TclError:
            top.after(150, lambda: top.winfo_exists() and top.grab_set())
        top.bind("<Escape>", lambda _e: top.destroy())
        ctk.CTkLabel(top, text=title, font=("Microsoft YaHei UI", 16, "bold"),
                     anchor="w").pack(fill="x", padx=18, pady=(16, 2))
        ctk.CTkLabel(top, text=prompt, font=FONT_S, text_color="#9aa0a6", anchor="w",
                     justify="left", wraplength=430).pack(fill="x", padx=18)
        ent = ctk.CTkEntry(top, font=FONT, width=400)
        ent.pack(fill="x", padx=18, pady=(8, 4))
        ent.insert(0, initial)
        ent.focus_set()
        ctk.CTkLabel(top, text="字母 / 数字 / 中文 / 下划线 / 减号 / 点都行；不能有空格和 \\ / : * ? \" < > |",
                     font=("Consolas", 11), text_color="#8a8f96", anchor="w",
                     justify="left", wraplength=430).pack(fill="x", padx=18)
        bar = ctk.CTkFrame(top, fg_color="transparent")
        bar.pack(fill="x", padx=18, pady=(12, 16))

        def ok(_e=None):
            out["v"] = ent.get().strip()
            top.destroy()

        ent.bind("<Return>", ok)
        ctk.CTkButton(bar, text="取消", width=90, height=32, font=FONT_S,
                      fg_color="#3a3f47", hover_color="#4a5058",
                      command=top.destroy).pack(side="right")
        ctk.CTkButton(bar, text="确定", width=100, height=32, font=FONT,
                      fg_color="#2f6fdb", hover_color="#255bb4",
                      command=ok).pack(side="right", padx=(0, 8))
        self.wait_window(top)
        return out["v"]

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
            self.btn_game.configure(text="开始游戏 · 编辑中 %s" % pk["name"].split("/")[-1] + suffix,
                                    state="normal",
                                    fg_color="#a86a12", hover_color="#bf7c17")
        else:
            ver = self.final_selected() if hasattr(self, "opt_final") else final_current_name()
            if not ver:
                self.btn_game.configure(text="开始游戏 · 成品（还没有版本）" + suffix, state="disabled",
                                        fg_color="#3a3f47", hover_color="#49505a")
            else:
                self.btn_game.configure(text="开始游戏 · 成品 %s（只读）" % ver + suffix, state="normal",
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
            ver = self.final_selected() if hasattr(self, "opt_final") else final_current_name()
            return {"mode": "final", "badge": "成品",
                    "title": ("本次启动加载 成品 %s（只读整版）" % ver) if ver
                             else "本次启动加载 成品（还没有版本 = 原版）",
                    "sub": "只读：游戏内改动不落盘；要改就切到「编辑中（packs）」",
                    "go": "去人机路点改"}
        name = pk["name"]
        short = name.split("/")[-1]
        man = pack_manifest(name)
        summ = pack_summary(name, pack_target_fp(name))
        ops = summ["nadd"] + summ["ndel"] + summ["eadd"] + summ["edel"]
        grow = bool(man.get("grow") or man.get("blank") or summ["grow"])
        keepn = bool(man.get("keep") or summ["keep"])
        kind = "原版 + 新增" if keepn else ("空白地图" if grow else "增量")
        label = str(man.get("label") or pk.get("label") or pk.get("map") or "")
        scope = ("只对 %s 生效" % label) if (pk.get("only_map") and label) else "全部地图生效"
        title = "%s · %s · %s" % (self.disp_of(name) or short, kind, scope)
        if keepn:
            sub = "包内 %d 处改动；原生点原样保留，原版路线照常走，只按 AddNode 追加新点" % ops
        elif grow and ops == 0:
            sub = "包内 0 处改动：原生点全禁用又没新建节点，人机没有可走路点"
        elif grow:
            sub = "包内 %d 处改动；原生点全禁用，节点按 AddNode 新建（不受原生点数限制）" % ops
        else:
            sub = "包内 %d 处改动，套在原生点上执行" % ops
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
                        "sub": "直接双击 UnityCrossFire.exe 是原版（无 mod）；要加载版本请关掉游戏再点底部按钮",
                        "go": "去人机路点"}
            else:
                info = dict(self._strip_run)
                info["badge"] = "运行中 · " + info["badge"]
                info["sub"] += " · 改版本只影响下次启动"
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
        if not bool(self.master_var.get()):
            self.master_var.set(True)
            self.on_master()
            return
        self.jump_to_pick()

    def jump_to_pick(self):
        r"""跳到「人机路点」→「编辑中」页 →「选包与地图」，并闪一下边框。"""
        try:
            self.tabview.set("人机路点")
        except Exception:
            pass
        try:
            if not self.seg_mode.get().startswith("编辑中"):
                self.seg_mode.set("编辑中（packs·可写）")
                self.on_pack_change()
            self.show_page("编辑中")
            if hasattr(self, "page_edit_tabs"):
                self.page_edit_tabs("选包与地图")
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
        scope = "只对这张图生效" if pk.get("only_map") else "全部地图生效"
        if keepn:
            alert = ("原版基础 + 新增（keep）：原生点一个都不动，原版路线照常能走；"
                     "包内 %d 处改动只按 AddNode 追加新点，数量不限。" % ops)
        elif grow and ops == 0:
            alert = ("注意：空白地图（grow）+ 包内 0 处改动。进图后原生点全部禁用、"
                     "又不会新建节点，人机没有可走路点，不会移动。")
        elif grow:
            alert = ("空白地图（grow）：原生点全部禁用，节点按 AddNode 新建，"
                     "包内 %d 处改动不受原生点数限制。" % ops)
        else:
            alert = "增量改动：包内 %d 处改动，套在原生点上执行。" % ops

        top = ctk.CTkToplevel(self)
        top.title("启动预检 · 测试包模式")
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
        cells = [("数据版本", "② 测试包（packs）"),
                 ("测试包", self.disp_of(name) or name.split("/")[-1]),
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
          UCF_EXPORT_DIR     -> ② 开发版 vis（Ctrl+E 导出、navmesh、_seen_ 都写这里）
          UCF_PACK_DIR       -> ② 开发版 packs（编辑中）
          成品：UCF_PACK_DIR=②\final + UCF_PACK=<版本名> —— 一版一目录，和编辑中同一套逻辑
          编辑中：UCF_PACK=<包>（可写，游戏内存回包里）
          原版：总开关关，插件待机
        """
        env = dict(os.environ)
        env["UCF_MOD"] = "1"
        env["UCF_EXPORT_DIR"] = TEST_VIS
        env["UCF_PACK_DIR"] = PACKS
        # 2026-11-23：日志写到工程端 log\，游戏目录不再生成；插件建不出目录才落回游戏端
        env["UCF_LOG_DIR"] = LOG_DIR
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
        except OSError:
            pass
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        enabled = bool(self.master_var.get()) if hasattr(self, "master_var") else True
        note = "mod 已启用"
        if not enabled:
            # 总开关关 = 插件加载但待机（plugin.c）；状态行别再写「mod + 测试包」
            note = "插件总开关关闭：插件待机（不读 nav、不出菜单）"
        elif pk.get("on") and pk.get("name"):
            env["UCF_PACK"] = pk["name"]           # 地图文件夹/包名，插件按子目录读
            env.pop("UCF_NAV_READONLY", None)      # 测试包允许游戏内保存
            note = "mod + 编辑中 %s" % pk["name"].split("/")[-1]
            if pk.get("only_map") and pk.get("fp"):
                env["UCF_FP"] = pk["fp"]
                env["UCF_FPLABEL"] = pk.get("label") or pk["map"]
                note += "（只对 %s）" % (pk.get("label") or pk["map"])
        else:
            # 成品：读 ②\final\<版本>\，而且**按「包」启动** —— UCF_PACK_DIR=final +
            # UCF_PACK=<版本名>，插件走和编辑中完全相同的加载路径（grow/keep 建点、
            # 0 点图都照常），所以在成品档里玩起来和编辑中一模一样。
            # 只读靠文件属性（prepare_final_dir 每次启动前设好），游戏内保存会失败。
            ver = self.final_selected() if hasattr(self, "opt_final") else final_current_name()
            d = prepare_final_dir(ver)
            if d:
                env["UCF_PACK_DIR"] = FINAL_ROOT
                env["UCF_PACK"] = ver
                env["UCF_NAV_DIR"] = d             # 万一包名被挡：退回同一个目录
                env["UCF_NAV_READONLY"] = "1"
                for k in ("UCF_FP", "UCF_FPLABEL"):
                    env.pop(k, None)
                note = "mod + 成品 %s（只读）" % ver
            else:
                # 成品里还没有版本：不读任何路线数据（等于原版）
                for k in ("UCF_PACK", "UCF_FP", "UCF_FPLABEL", "UCF_NAV_DIR"):
                    env.pop(k, None)
                note = "mod + 成品（还没有版本，等于原版）"
        return env, note

    def launch_game(self):
        if not os.path.isfile(GAME_EXE):
            self.set_status("找不到 %s" % GAME_EXE)
            return
        # 2026-11-19：测试包模式先过一道预检（正式版 / 插件待机直接放行）
        pk = self.pack_dict() if hasattr(self, "seg_mode") else {}
        if (bool(self.master_var.get()) and pk.get("on") and pk.get("name")
                and not self._mute_preflight):
            if not self.preflight_start():
                self.set_status("已取消启动（测试包 %s）" % pk.get("name"))
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
    if not os.path.isdir(DEPLOY) or not os.path.isfile(GAME_EXE):
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
    App().mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main())
