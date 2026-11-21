#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""navdata.py —— 导航数据「三区」管理：① 备份  ② 开发  ③ 部署

  ---------------------------------------------------------------------------
  ① 备份版  navdata/native/      UCF 原版数据，只读、永不编辑（本脚本之外没人写它）
  ② 开发版  navdata/dev/         唯一数据源（控制台三档启动都读这里）
                                   maps\ nav\ vis\   成品数据（成品档按包读 nav\）+ 导出收件箱
                                   packs\            编辑中（可写沙盒）；做完 promote 升进 nav\
                                   archive\          处理过的导出 / 只读还原点
  ③ 游戏目录 ucf_mod/           运行时：dll / ucf_mod.json / markers\（2026-11-21 起不放数据）
  流水线：游戏导出 -> ②\vis ->（import 整理）-> ②\maps ->（pack promote）-> ②\nav -> 成品
  ---------------------------------------------------------------------------

  三档启动（控制台底部按钮，不再往游戏目录搬数据）：
      成品    读 ②\nav\，但按「包」启动（UCF_PACK_DIR=②、UCF_PACK=nav）
              和编辑中走完全同一套加载逻辑：grow/keep 建点、0 点图都照常，
              所以发布进来的东西在成品档里的效果和编辑中一模一样（只读靠文件属性）
      编辑中  读 ②\packs\<包>（UCF_PACK），可写      调图、试路线、游戏内存回包里
      原版    插件待机，什么都不读                     对照原生行为

常用命令（在 tools/ 下跑）：

    python navdata.py status              # 三区各自在哪、各有几个文件、是否只读
    python navdata.py verify              # 校验备份版没被动过（SHA256 清单）
    python navdata.py restore             # 开发版 <- 备份版（丢掉开发版的改动）
    python navdata.py import              # 整理开发版：vis 归位 + 原始导出 -> maps
    python navdata.py diff                # 开发版 vs 备份版差在哪 + 成品里有几张图
    python navdata.py freeze --force      # 用当前数据重建「备份版」（只在确认要重新冻结时用）

  测试包 = 编辑中：一份只对某一张图生效的路线改动，放在
  navdata\dev\packs\<序号_场景名中文名>\<包名>\<指纹>.txt（序号见《地图对照表》）；
  插件用 UCF_PACK / UCF_FP 读它，成品 nav\ 一个字节都不动。

    python navdata.py pack list                     # 有哪些测试包
    python navdata.py pack new chain_a --level 11   # 从开发版复制 level11 的改动做包
    python navdata.py pack diff chain_a             # 包 vs 成品 nav / 原版
    python navdata.py pack promote chain_a          # 编辑中 -> 成品（版本名沿用包名；不碰游戏目录）

注意：freeze 只收【原生】内容 —— 判据是导出文件里 map.source
      （"game" 才算原生；"ours"/"practice" = 我们造的，一律不收），
      碰到我们造的图时按对照表写一份「原生为空」的空档文件说明原因。
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time

def _setup_console():
    """控制台（双击 bat）用系统编码（中文 Windows = cp936 才能显示中文）；
    管道/重定向时统一 UTF-8，方便别的程序读。顺带把输出抄一份到 navdata/_logs/navdata.log。"""
    out = sys.stdout
    enc = (getattr(out, "encoding", "") or "").lower().replace("-", "")
    try:
        if getattr(out, "isatty", lambda: False)() and enc not in ("utf8", "cp65001"):
            out.reconfigure(errors="replace")          # 就用控制台自己的编码
        else:
            out.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        logdir = os.path.join(P.PROJ, "navdata", "_logs")
        os.makedirs(logdir, exist_ok=True)
        sys.stdout = _Tee(out, os.path.join(logdir, "navdata.log"))
    except Exception:
        pass


class _Tee(object):
    """stdout 抄一份到日志文件（UTF-8），出问题时能直接把日志发出来。"""

    def __init__(self, stream, path):
        self.stream = stream
        self.path = path

    def write(self, s):
        try:
            self.stream.write(s)
        except Exception:
            pass
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(s)
        except OSError:
            pass
        return len(s)

    def flush(self):
        try:
            self.stream.flush()
        except Exception:
            pass

    def isatty(self):
        return False

    def __getattr__(self, name):
        return getattr(self.stream, name)

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import ucf_paths as P  # noqa: E402
import map_table  # noqa: E402  序号 + 文件夹命名（和《地图对照表》第一张表一致）

SUBS = ("maps", "nav", "vis")
KEEP_ALWAYS = {"nogen.txt", "collect.flag", "README.txt", "README.md", "INDEX.md", "_index.json"}
MAP_TABLE_RE = re.compile(r"^\|\s*(\d{1,3})\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


# ---------------------------------------------------------------- 小工具
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, obj, indent=1):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def load_table():
    """序号 / 关卡 / 中文名 / 场景名 / 备注 —— 只读 docs/地图对照表.md 的第一张表。"""
    path = P.doc("地图对照表.md")
    rows, started = [], False
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                if started:
                    break
                continue
            m = MAP_TABLE_RE.match(s)
            if not m:
                if started and not s.startswith("|"):
                    break
                continue
            started = True
            rows.append({"no": "%02d" % int(m.group(1)), "level": m.group(2),
                         "cn": m.group(3).strip(), "scene": m.group(4).strip(),
                         "note": m.group(5).strip()})
    rows.sort(key=lambda r: r["no"])
    return rows


def make_readonly(path):
    try:
        os.chmod(path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    except OSError:
        pass


def make_writable(path):
    try:
        os.chmod(path, 0o666)
    except OSError:
        pass


# ---------------------------------------------------------------- 成品（多版本）
# 2026-11-21：成品档「按包启动」（UCF_PACK_DIR=<爪根>、UCF_PACK=<版本名>），和编辑中
# 走同一套加载逻辑（grow/keep 建点、0 点图都照常），所以发布过来效果一模一样。
#
# 成品可以并存多个版本，**一版 = 一整套数据**（所有图一起，启动时只选一次）：
#
#   navdata\dev\final\
#     <包名>\  …           每个版本一个目录（插件按 <包根>\<包名> 读它）；
#                          名字默认沿用测试包名，重名 -2 / -3；旧数据还是 v1、v2
#       <指纹>.txt  nogen.txt
#     _index.json          台账：每版创建时间 / 继承自哪版 / 含哪些图 / 每图 sha、点边
#     _current.txt         当前选中的版本（控制台启动「成品」时读它）
#
# 发布默认「新建一版」：以当前版为底整套复制，再用这个包替换对应图；老版本一律保留，
# 新版本名 = 测试包名（--as 可改，重名自动加 -2）。不要的版本用 final rm 真删
# （控制台成品页「删除」同一个动作）；想留个后手才加 --keep（挪进 dev\archive\final_old\）。
FINAL_ROOT = os.path.join(P.DEV, "final")
FINAL_INDEX = os.path.join(FINAL_ROOT, "_index.json")
FINAL_CURRENT = os.path.join(FINAL_ROOT, "_current.txt")
FINAL_ARCHIVE = os.path.join(P.DEV, "archive", "final_old")
LEGACY_FINAL = os.path.join(P.DEV, "nav")      # 2026-11-21 之前成品放这儿（首次自动搬走）
_NAV_FP_RE = re.compile(r"^n\d+-[0-9a-f]{16}\.txt$", re.I)
FINAL_NAME_BAD = '\\/:*?"<>| '


def final_map_files(d):
    r"""某个版本目录里真正的路线文件（<指纹>.txt）；nogen.txt / _index.json 不算。"""
    if not d or not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if _NAV_FP_RE.match(f))


def final_ensure_nogen(d):
    r"""版本目录补一份 nogen.txt：空图不自动铺点（和编辑中的 grow/keep 包保持一致）。"""
    if not d:
        return
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "nogen.txt")
    if os.path.isfile(p):
        return
    try:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("")
        make_readonly(p)
    except OSError:
        pass


def final_version_path(name):
    return os.path.join(FINAL_ROOT, name) if name else ""


def final_index_read():
    idx = {}
    try:
        with open(FINAL_INDEX, "r", encoding="utf-8") as f:
            idx = json.load(f) or {}
    except (OSError, ValueError):
        idx = {}
    idx.setdefault("format", "ucf-final-versions")
    idx.setdefault("version", 1)
    idx.setdefault("seq", 0)
    idx.setdefault("current", "")
    idx.setdefault("versions", [])
    return idx


def final_index_write(idx):
    os.makedirs(FINAL_ROOT, exist_ok=True)
    write_json(FINAL_INDEX, idx)
    try:
        with open(FINAL_CURRENT, "w", encoding="utf-8", newline="\n") as f:
            f.write((idx.get("current") or "") + "\n")
    except OSError:
        pass


def final_scan_maps(d):
    r"""扫一个版本目录：{指纹: {file, sha256, node, edge, bytes, mtime}}"""
    out = {}
    for fn in final_map_files(d):
        p = os.path.join(d, fn)
        nd, ed = edit_counts(p)
        try:
            st = os.stat(p)
            mt, sz = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)), st.st_size
        except OSError:
            mt, sz = "", 0
        out[fn[:-4]] = {"file": fn, "sha256": sha256(p), "node": nd, "edge": ed,
                        "bytes": sz, "mtime": mt}
    return out


def final_versions():
    r"""所有成品版本（按台账顺序）。台账和磁盘对不上时以磁盘为准：
    目录没了标 exists=False，磁盘上多出来的目录当场补进来。"""
    idx = final_index_read()
    out, seen = [], set()
    for v in idx.get("versions") or []:
        name = (v.get("name") or "").strip()
        if not name:
            continue
        d = final_version_path(name)
        item = dict(v)
        item["name"] = name
        item["path"] = d
        item["exists"] = os.path.isdir(d)
        item["maps"] = dict(v.get("maps") or {})
        if item["exists"]:
            for fp, m in final_scan_maps(d).items():     # 磁盘上的实际内容优先
                item["maps"][fp] = dict(item["maps"].get(fp) or {}, **m)
        out.append(item)
        seen.add(name)
    if os.path.isdir(FINAL_ROOT):
        for name in sorted(os.listdir(FINAL_ROOT)):
            d = os.path.join(FINAL_ROOT, name)
            if name.startswith("_") or name in seen or not os.path.isdir(d):
                continue
            mt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(d).st_mtime))
            out.append({"name": name, "path": d, "exists": True, "created": mt, "updated": mt,
                        "base": "", "note": "（磁盘上多出来的目录，已自动登记）",
                        "maps": final_scan_maps(d)})
    return out


def final_current():
    r"""当前选中的成品版本名（没有就返回空串）。"""
    names = [v["name"] for v in final_versions() if v["exists"]]
    idx = final_index_read()
    for cand in ((idx.get("current") or "").strip(), final_current_file()):
        if cand and cand in names:
            return cand
    return names[-1] if names else ""


def final_current_file():
    try:
        with open(FINAL_CURRENT, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def final_set_current(name):
    idx = final_index_read()
    if name not in [v.get("name") for v in idx.get("versions") or []]:
        sys.exit("没有这个成品版本：%s" % name)
    idx["current"] = name
    final_index_write(idx)


def final_check_name(name):
    r"""版本名：字母数字下划线减号点、中文也行；不许路径分隔符 / 空格 / Windows 非法字符。"""
    n = (name or "").strip()
    if not n or len(n) > 48:
        return "版本名要 1~48 个字符"
    if n.startswith("_") or n in (".", ".."):
        return "版本名不能以下划线开头，也不能是 . / .."
    for ch in n:
        if ch in FINAL_NAME_BAD or ord(ch) < 32:
            return "版本名不能包含这些字符：\\ / : * ? \" < > | 空格"
    if os.path.isdir(final_version_path(n)):
        return "已经有这个版本目录了：%s" % n
    return ""


def final_next_name(idx=None):
    r"""自动版本号：v1 / v2 / v3……（改名了也不会撞号，seq 只增不减）"""
    idx = idx if idx is not None else final_index_read()
    seq = int(idx.get("seq") or 0)
    taken = set()
    for v in idx.get("versions") or []:
        taken.add(v.get("name"))
    while True:
        seq += 1
        name = "v%d" % seq
        if name not in taken and not os.path.isdir(final_version_path(name)):
            idx["seq"] = seq
            return name


def final_name_from_pack(pack):
    r"""版本名默认跟测试包同名：packs/<地图>/<包> -> <包>。

    包名只允许英文字母、数字、下划线和短横线（pack_id_ok 管着），本来就能当目录名；
    这里再按 final_check_name 的规则兜一遍，防止手工塞进来的怪名字。
    """
    leaf = str(pack or "").replace("\\", "/").strip("/").split("/")[-1]
    out = "".join("_" if (ch in FINAL_NAME_BAD or ord(ch) < 32) else ch for ch in leaf)
    return out.strip("._ ")[:48].strip("._ ")


def final_unique_name(base, idx=None):
    r"""想要的版本名被占了就往下排：<包名>、<包名>-2、<包名>-3……（不覆盖、不删任何版本）。"""
    idx = idx if idx is not None else final_index_read()
    base = (base or "").strip()
    if not base:
        return final_next_name(idx)          # 没有参照名（老成品迁移）才退回 v1/v2/v3
    taken = set(v.get("name") for v in idx.get("versions") or [])
    name, n = base, 1
    while name in taken or os.path.isdir(final_version_path(name)):
        n += 1
        name = ("%s-%d" % (base[:46], n))[:48]
    return name


def final_new_version(base=None, note="", name=""):
    r"""新建一版（默认以 base 版为底整套复制）。返回 (版本名, 复制了几个文件)。

    name 为空才自动编号 v1/v2/v3（老成品迁移用）；发布时传测试包名，
    所以成品版本默认就叫测试包的名字，重名自动 -2 / -3。
    """
    idx = final_index_read()
    name = final_unique_name(name, idx) if name else final_next_name(idx)
    d = final_version_path(name)
    os.makedirs(d, exist_ok=True)
    src_dir = final_version_path(base) if base else ""
    copied = 0
    if src_dir and os.path.isdir(src_dir):
        for fn in os.listdir(src_dir):
            s = os.path.join(src_dir, fn)
            if not os.path.isfile(s):
                continue
            t = os.path.join(d, fn)
            if os.path.exists(t):
                make_writable(t)
            shutil.copyfile(s, t)
            if fn.lower().endswith(".txt"):
                make_readonly(t)
            copied += 1
    final_ensure_nogen(d)
    maps_meta = {}
    if base:
        for v in idx.get("versions") or []:
            if v.get("name") == base:
                maps_meta = {k: dict(m) for k, m in (v.get("maps") or {}).items()}
                break
    for fp, m in final_scan_maps(d).items():
        maps_meta[fp] = dict(maps_meta.get(fp) or {}, **m)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    idx["versions"].append({"name": name, "created": now, "updated": now,
                            "base": base or "", "note": note, "maps": maps_meta})
    idx["current"] = name
    final_index_write(idx)
    return name, copied


def final_ensure_root():
    r"""第一次用：把旧成品目录 ②\nav\ 里的数据搬成 v1（搬完清空旧址）。
    没有旧数据就只建一个空台账，什么都不动。"""
    try:
        os.makedirs(FINAL_ROOT, exist_ok=True)
    except OSError:
        return
    idx = final_index_read()
    if idx.get("versions"):
        return
    legacy = final_map_files(LEGACY_FINAL)
    if not legacy:
        final_index_write(idx)
        return
    name = final_next_name(idx)
    d = final_version_path(name)
    os.makedirs(d, exist_ok=True)
    for fn in legacy:
        src = os.path.join(LEGACY_FINAL, fn)
        dst = os.path.join(d, fn)
        shutil.copyfile(src, dst)
        make_readonly(dst)
        try:
            make_writable(src)
            os.remove(src)          # 旧位置清空：成品只留 final\ 这一处
        except OSError:
            pass
    final_ensure_nogen(d)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    idx["versions"].append({"name": name, "created": now, "updated": now, "base": "",
                            "note": "从旧成品目录 nav\\ 自动迁过来", "maps": final_scan_maps(d)})
    idx["current"] = name
    final_index_write(idx)
    print("已把旧成品（② nav\\ %d 个文件）迁成成品版本 %s" % (len(legacy), name))


def pack_flags(path):
    r"""读包文件头里的 grow / keep（blank 是旧写法，等同 grow）。"""
    grow = keep = False
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for ln in f:
                s = ln.strip()
                if not s or s.startswith("#"):
                    continue
                if s in ("grow", "blank"):
                    grow = True
                elif s == "keep":
                    keep = True
                else:
                    break
    except OSError:
        pass
    return grow, keep


def walk_files(root):
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            p = os.path.join(dirpath, fn)
            out.append(os.path.relpath(p, root).replace(os.sep, "/"))
    out.sort()
    return out


def summary(root):
    """一版数据的概况：图 / 可走面 / 路线各几个，占多大，最近改动（只看数据，不算 packs/final）。"""
    if not os.path.isdir(root):
        return {"path": root, "exists": False, "files": 0, "bytes": 0, "mtime": "-", "sub": {}}
    maps = P.map_files(root)
    bins = P.navmesh_files(root)
    routes = P.route_files(root)
    sub = {"图": len(maps), "可走面": len(bins), "路线": len(routes)}
    size, latest = 0, 0
    for _key, path in list(maps) + list(bins) + list(routes):
        try:
            size += os.path.getsize(path)
            latest = max(latest, os.path.getmtime(path))
        except OSError:
            pass
    return {"path": root, "exists": True, "files": sum(sub.values()), "bytes": size,
            "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(latest)) if latest else "-",
            "sub": sub}


def _walk_count(root, pred=None):
    """(文件数, 最近 mtime)；pred 只统计某类文件。"""
    n, latest = 0, 0.0
    if os.path.isdir(root):
        for dp, _dirs, fns in os.walk(root):
            for fn in fns:
                if pred and not pred(fn):
                    continue
                n += 1
                try:
                    latest = max(latest, os.path.getmtime(os.path.join(dp, fn)))
                except OSError:
                    pass
    return n, latest


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%.0f %s" % (n, unit)) if unit == "B" else ("%.1f %s" % (n, unit))
        n /= 1024.0


# ---------------------------------------------------------------- 原生判据
def reject_reason(doc):
    """返回不是原生的原因；空串 = 原生，收。"""
    m = doc.get("map") or {}
    src = str(m.get("source") or "").lower()
    if src == "practice":
        return "沙盒（source=practice）"
    if src == "ours" or str(m.get("origin") or "") == "mod-generated":
        return "插件/我们造的（source=%s）" % (src or "ours")
    if src and src != "game":
        return "来源不明（source=%s）" % src
    return ""


def empty_stub(level, cn, scene, why):
    """原生内容为空时写一份说明性空档（不是数据，是记录）。"""
    return {
        "format": "ucf-navgraph",
        "version": 1,
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "plugin": "navdata.py freeze",
        "map": {
            "name": "%s_%s" % (level, scene or ""),
            "label": cn, "level": level, "scene": scene,
            "source": "native", "origin": "native-empty",
            "node_count": 0, "edge_count": 0, "fingerprint": "",
            "native_only": True,
            "note": "UCF 原版这张图没有原生导航数据：%s；"
                    "游戏里能跑的点是插件 auto_waypoints 运行时铺的（不落盘，不算原生）。" % why,
        },
        "counts": {"nodes": 0, "edges": 0, "features": 0},
        "nodes": [], "edges": [], "features": [],
        "lines": {"nano_neighbor": [], "entrance_escape": [], "jump": []},
    }


# ---------------------------------------------------------------- ① freeze
def cmd_freeze(args):
    src = os.path.abspath(args.src or P.DEPLOY)
    smaps = os.path.join(src, "maps")
    snav = os.path.join(src, "nav")
    svis = os.path.join(src, "vis")
    if not os.path.isdir(smaps):
        sys.exit("源目录里没有 maps 目录：%s" % smaps)
    try:
        n_src = len([f for f in os.listdir(smaps)
                     if f.lower().endswith(".json") and f not in ("_index.json", "names.json")])
    except OSError:
        n_src = 0
    if n_src == 0 and os.path.isdir(P.NATIVE):
        # 2026-11-21：③ 不再存数据；源目录空着跑 freeze 会把备份版洗成空壳，先拦住
        sys.exit("源目录里一张图都没有：%s\n③ 游戏目录已不存数据，备份版没有动。" % smaps)

    if os.path.isdir(P.NATIVE) and walk_files(P.NATIVE):
        if not args.force:
            sys.exit("备份版已存在：%s\n要重建请加 --force（旧的会被删掉）" % P.NATIVE)
        for rel in walk_files(P.NATIVE):
            make_writable(os.path.join(P.NATIVE, rel.replace("/", os.sep)))
        shutil.rmtree(P.NATIVE, ignore_errors=True)

    tmp = P.NATIVE + ".tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(os.path.join(tmp, P.COMMON), exist_ok=True)

    table = {r["level"]: r for r in load_table()}
    kept, skipped, stubs = [], [], []

    for fn in sorted(os.listdir(smaps)):
        if not fn.lower().endswith(".json") or fn in ("_index.json", "names.json"):
            continue
        srcfile = os.path.join(smaps, fn)
        if not os.path.isfile(srcfile):
            continue
        try:
            doc = read_json(srcfile)
        except Exception as exc:
            skipped.append((fn, "读不了：%s" % exc))
            continue
        m = doc.get("map") or {}
        level = str(m.get("level") or "")
        cn = str(m.get("label") or "")
        scene = str(m.get("scene") or "")
        # 文件夹名以《地图对照表》为准；表里没有这张图才退回 JSON 里的场景名
        folder = map_table.folder_name(level, scene, cn) or os.path.splitext(fn)[0]
        rel = folder + "/map.json"
        if str(m.get("origin") or "") == "native-empty":
            # 之前生成的「原生为空」空档：原样保留，别当成「来源不明」再生成一遍
            save_json(os.path.join(tmp, folder, "map.json"), doc)
            kept.append({"file": rel, "level": level, "cn": cn, "scene": scene,
                         "nodes": 0, "edges": 0, "fp": "", "source": "native-empty"})
            continue
        why = reject_reason(doc)
        if why:
            skipped.append((fn, why))
            row = table.get(level)
            if row and not any(x["level"] == level for x in stubs):
                stubs.append({"level": level, "cn": row["cn"], "scene": row["scene"],
                              "no": row["no"], "why": "原生 0 个路点、没有 NavMeshGraph（%s）" % why})
            continue
        doc.pop("edits", None)
        save_json(os.path.join(tmp, folder, "map.json"), doc)
        kept.append({"file": rel, "level": level, "cn": cn, "scene": scene,
                     "nodes": len(doc.get("nodes") or []),
                     "edges": len(doc.get("edges") or []),
                     "fp": str(m.get("fingerprint") or ""),
                     "source": str(m.get("source") or "")})

    for s in stubs:
        folder = map_table.folder_name(s["level"], s["scene"], s["cn"])
        rel = folder + "/map.json"
        save_json(os.path.join(tmp, folder, "map.json"),
                  empty_stub(s["level"], s["cn"], s["scene"], s["why"]))
        kept.append({"file": rel, "level": s["level"], "cn": s["cn"], "scene": s["scene"],
                     "nodes": 0, "edges": 0, "fp": "", "source": "native-empty"})

    edits = []
    if os.path.isdir(snav):
        for fn in sorted(os.listdir(snav)):
            if not fn.lower().endswith(".txt"):
                continue
            head = ""
            try:
                with open(os.path.join(snav, fn), "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        s = line.strip()
                        if s and not s.startswith("#"):
                            head = s
                            break
            except OSError:
                pass
            edits.append((fn, head))

    # 可走面：③\vis（旧位置）、④\vis、当前版本自带的 vis 都收，同名只看第一份。
    # 2026-11-18 起导出落在 ④，③\vis 只留迁移前的旧文件。
    # 可走面：文件名是 navmesh_nm<原生顶点数>-<指纹>.bin，按顶点数认是哪张图，
    # 收进 <图>\navmesh.bin（和点图放一个文件夹）。
    bins, bin_origin, bin_skipped = [], {}, []
    verts_level = {v: k for k, v in P.NATIVE_VERTS.items()}
    vis_roots = [svis, P.VIS, P.DATAVIS]
    seen_roots = []
    for root in vis_roots:
        if not os.path.isdir(root):
            continue
        key = os.path.abspath(root).lower()
        if key in seen_roots:
            continue
        seen_roots.append(key)
        for base, dirs, fns in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ("_state", "_noise")]
            for fn in sorted(fns):
                if not (fn.lower().endswith(".bin") and fn.startswith("navmesh")):
                    continue
                mnm = re.search(r"nm(\d+)-", fn)
                level = verts_level.get(int(mnm.group(1))) if mnm else ""
                if not level:
                    bin_skipped.append(fn)
                    continue
                rel = map_table.folder_name(level) + "/navmesh.bin"
                if rel in bins:
                    continue
                shutil.copy2(os.path.join(base, fn),
                             os.path.join(tmp, os.path.dirname(rel).replace("/", os.sep), "navmesh.bin"))
                bins.append(rel)
                bin_origin[rel] = fn

    names = {}
    for r in load_table():
        names[r["level"]] = {"name": r["cn"], "level": r["level"]}
        if r["scene"]:
            names[r["scene"]] = {"name": r["cn"], "level": r["level"]}
    for k in kept:
        if k["fp"]:
            names[k["fp"]] = {"name": k["cn"] or table.get(k["level"], {}).get("cn", ""),
                              "level": k["level"]}
    save_json(os.path.join(tmp, P.COMMON, "names.json"), names)

    sums = []
    for rel in walk_files(tmp):
        sums.append("%s  %s" % (sha256(os.path.join(tmp, rel.replace("/", os.sep))), rel))
    with open(os.path.join(tmp, P.COMMON, "SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sums) + "\n")

    frozen = {
        "kind": "ucf-navdata-native",
        "frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": src,
        "rule": "只收 map.source == game 的导出；我们造的（ours/practice）一律不收，只在空档文件里记录原因",
        "maps": kept,
        "navmesh_bins": bins,
        "navmesh_origin": bin_origin,
        "skipped": [{"file": f, "why": w} for f, w in skipped],
        "edits_dropped": [{"file": f, "firstLine": h} for f, h in edits],
        "manifest_sha256": hashlib.sha256("\n".join(sums).encode("utf-8")).hexdigest(),
    }
    save_json(os.path.join(tmp, P.COMMON, ".frozen.json"), frozen)
    with open(os.path.join(tmp, P.COMMON, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(native_readme(frozen, sums))
    for rel in walk_files(tmp):
        make_readonly(os.path.join(tmp, rel.replace("/", os.sep)))
    os.replace(tmp, P.NATIVE)

    print("① 备份版已生成：%s" % P.NATIVE)
    for k in kept:
        print("   收  %-34s %-8s %-6s %3d 点 / %3d 边  %s" % (
            k["file"], k["level"], k["cn"], k["nodes"], k["edges"], k["fp"] or "-"))
    for f, w in skipped:
        print("   丢  %-22s %s" % (f, w))
    for f, h in edits:
        print("   丢  nav/%-24s 编辑清单（第一个操作：%s）" % (f, h or "-"))
    for b in bins:
        print("   收  %-34s 可走面" % b)
    for b in bin_skipped:
        print("   丢  %-34s 可走面（认不出是哪张图）" % b)
    print("   共 %d 个文件，只读；清单 SHA256=%s" % (len(sums), frozen["manifest_sha256"][:16]))
    return cmd_verify(args)


def native_readme(frozen, sums):
    fence = chr(96) * 3
    L = []
    L.append("# ① 备份版 · UCF 原生导航数据（只读，永不编辑）")
    L.append("")
    L.append("冻结时间：%s　来源：`%s`" % (frozen["frozen_at"], frozen["source"]))
    L.append("")
    L.append("> 这里只能**只读**：文件带只读属性，`tools/navdata.py` 只往里读、从不往里写。")
    L.append("> 想编辑请改 **② 开发版** `navdata/dev/`；改坏了跑 `python tools/navdata.py restore` 一键还原。")
    L.append("")
    L.append("## 收进来的（原生）")
    L.append("")
    L.append("一张图一个文件夹（`<序号>_<场景><中文名>\\`），里面是 `map.json` + `navmesh.bin`；")
    L.append("不属于任何一张图的（对照表 / 清单 / 说明）都放在 `00_公共\\`。")
    L.append("")
    L.append("| 文件夹 | 点图 | 关卡 | 中文名 | 节点 | 边 | 指纹 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- |")
    for k in frozen["maps"]:
        folder, _sep, fn = str(k["file"]).partition("/")
        L.append("| %s | %s | %s | %s | %d | %d | %s |" % (
            folder, fn or "—", k["level"], k["cn"], k["nodes"], k["edges"], k["fp"] or "—"))
    L.append("")
    if frozen["navmesh_bins"]:
        L.append("可走面（NavMeshGraph 导出，游戏自己烘焙的网格）：%d 张图 ——" % len(frozen["navmesh_bins"]))
        L.append("")
        origin = frozen.get("navmesh_origin") or {}
        for b in frozen["navmesh_bins"]:
            L.append("- `%s`　原文件 `%s`" % (b, origin.get(b, "—")))
        L.append("")
    if frozen["skipped"]:
        L.append("## 丢掉的（不是原生）")
        L.append("")
        L.append("| 文件 | 原因 |")
        L.append("| --- | --- |")
        for s in frozen["skipped"]:
            L.append("| %s | %s |" % (s["file"], s["why"]))
        L.append("")
    if frozen["edits_dropped"]:
        L.append("## 丢掉的编辑清单（nav 目录里的 .txt）")
        L.append("")
        L.append("| 文件 | 第一个操作 |")
        L.append("| --- | --- |")
        for e in frozen["edits_dropped"]:
            L.append("| %s | `%s` |" % (e["file"], e["firstLine"] or "—"))
        L.append("")
    L.append("## 怎么用")
    L.append("")
    L.append(fence)
    L.append("cd tools")
    L.append("python navdata.py status      # 三区在哪、多少文件")
    L.append("python navdata.py verify      # 校验这一版没被动过")
    L.append("python navdata.py restore     # 开发版 <- 这里（还原）")
    L.append(fence)
    L.append("")
    L.append("清单：`SHA256SUMS.txt`（%d 个文件），机器可读信息：`.frozen.json`。" % len(sums))
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- ② verify
def cmd_verify(args):
    sums = os.path.join(P.manifest_dir(P.NATIVE), "SHA256SUMS.txt")
    if not os.path.isfile(sums):
        print("!! 没有 %s（备份版还没生成？跑 freeze）" % sums)
        return 1
    want = {}
    with open(sums, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            h, rel = line.split("  ", 1)
            want[rel] = h
    meta = {"SHA256SUMS.txt", "README.md", ".frozen.json"}
    meta |= {P.COMMON + "/" + n for n in ("SHA256SUMS.txt", "README.md", ".frozen.json")}
    have = set(walk_files(P.NATIVE)) - meta
    bad, missing = [], sorted(set(want) - have)
    for rel in sorted(have & set(want)):
        if sha256(os.path.join(P.NATIVE, rel.replace("/", os.sep))) != want[rel]:
            bad.append(rel)
    extra = sorted(have - set(want))
    ok = not (bad or missing or extra)
    print("%s备份版校验：%s（%d 个文件）" % ("OK " if ok else "!! ", "通过" if ok else "不一致", len(want)))
    for rel in bad:
        print("   被改过：%s" % rel)
    for rel in missing:
        print("   丢了：  %s" % rel)
    for rel in extra:
        print("   多出来：%s" % rel)
    if ok:
        ro = all(not (os.stat(os.path.join(P.NATIVE, r.replace("/", os.sep))).st_mode & stat.S_IWRITE)
                 for r in have)
        print("   只读属性：%s" % ("是" if ro else "否（跑 make_readonly）"))
    return 0 if ok else 1


# ---------------------------------------------------------------- 镜像
def mirror(src, dst, strict=True, keep=()):
    """把 dst 变成 src 的镜像（strict：删掉 dst 里 src 没有的普通文件）。"""
    copied, deleted = 0, 0
    if not os.path.isdir(src):
        return copied, deleted
    os.makedirs(dst, exist_ok=True)
    src_files = set(walk_files(src))
    for rel in sorted(src_files):
        s = os.path.join(src, rel.replace("/", os.sep))
        d = os.path.join(dst, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(d), exist_ok=True)
        if os.path.exists(d):
            make_writable(d)
        shutil.copy2(s, d)
        make_writable(d)
        copied += 1
    if strict:
        for rel in walk_files(dst):
            if rel in src_files or rel in keep or os.path.basename(rel) in keep:
                continue
            p = os.path.join(dst, rel.replace("/", os.sep))
            try:
                make_writable(p)
                os.remove(p)
                deleted += 1
            except OSError:
                pass
    return copied, deleted


def rebuild_index(root):
    r"""给 00_公共\_index.json + INDEX.md 重新生成一份（编辑器排序列要用）。"""
    table = load_table()
    rows = []
    by_level = {}
    for rel, path in P.map_files(root):
        try:
            doc = read_json(path)
        except Exception:
            continue
        m = doc.get("map") or {}
        by_level[str(m.get("level") or "")] = {
            "file": rel, "fingerprint": str(m.get("fingerprint") or ""),
            "nodes": len(doc.get("nodes") or []), "edges": len(doc.get("edges") or []),
            "features": len(doc.get("features") or []),
            "exported": str(doc.get("generated") or ""),
            "source": str(m.get("source") or ""), "origin": str(m.get("origin") or ""),
        }
    # 旧台账里有整理时才写得出来的字段（原始导出名 / 套着几条编辑 / 可疑样本），重建时保留
    prev_doc = {}
    try:
        with open(P.index_path(root), "r", encoding="utf-8") as f:
            prev_doc = json.load(f) or {}
    except (OSError, ValueError):
        prev_doc = {}
    prev_rows = {str(r.get("level") or ""): r for r in (prev_doc.get("maps") or [])}
    for r in table:
        info = by_level.get(r["level"]) or {}
        prev = prev_rows.get(r["level"]) or {}
        row = {
            "no": r["no"], "level": r["level"], "name": r["cn"], "scene": r["scene"], "note": r["note"],
            "file": info.get("file", ""), "fingerprint": info.get("fingerprint", ""),
            "nodes": info.get("nodes", 0), "edges": info.get("edges", 0),
            "features": info.get("features", 0), "exported": info.get("exported", ""),
            "source": info.get("source", ""), "origin": info.get("origin", ""),
            "status": "有数据" if info.get("file") else "待采集",
        }
        for k in ("source_file", "edits_on_top", "suspect"):
            if k in prev:
                row[k] = prev[k]
        rows.append(row)
    doc = {"format": "ucf-map-index", "version": 1,
           "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
           "ucf": P.DATA,
           "note": "这份索引由 tools/navdata.py 按 docs/地图对照表.md 生成；节点/边是当前这一版里的原生数据。",
           "maps": rows, "extras": prev_doc.get("extras") or []}
    out_dir = P.index_dir(root)
    os.makedirs(out_dir, exist_ok=True)
    save_json(os.path.join(out_dir, "_index.json"), doc)
    md = ["# 当前版本的地图数据（自动生成，勿手改）", "",
          "生成时间：" + doc["generated"], "",
          "| 序号 | 关卡 | 中文名 | 场景名 | 节点 | 边 | 文件 | 状态 |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for it in rows:
        md.append("| %s | %s | **%s** | %s | %s | %s | %s | %s |" % (
            it["no"], it["level"], it["name"], it["scene"] or "-",
            it["nodes"] or "-", it["edges"] or "-", it["file"] or "-", it["status"]))
    md += ["", "数据来源：UCF 原版（插件进图 Scan 导出）。我们手工加的点和编辑都不在这一版里。", ""]
    with open(os.path.join(out_dir, "INDEX.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md))


def cmd_restore(args):
    if not walk_files(P.NATIVE):
        sys.exit("备份版是空的：%s\n先跑 python navdata.py freeze" % P.NATIVE)
    want = {}
    for rel, src in list(P.map_files(P.NATIVE)) + list(P.navmesh_files(P.NATIVE)):
        want[rel] = src
    copied = 0
    for rel in sorted(want):
        dst = os.path.join(P.DEV, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            make_writable(dst)
        shutil.copy2(want[rel], dst)
        make_writable(dst)
        copied += 1
    # 开发版里多出来的点图 / 可走面（我们加的）删掉；packs / final / vis / archive 一律不碰。
    # 只有两边都是「一张图一个文件夹」的新布局才敢删——半迁移状态下删错就找不回来了。
    deleted = 0
    if P.is_folders(P.DEV) and P.is_folders(P.NATIVE):
        for rel, path in sorted(list(P.map_files(P.DEV)) + list(P.navmesh_files(P.DEV))):
            if rel in want:
                continue
            try:
                make_writable(path)
                os.remove(path)
                deleted += 1
            except OSError:
                pass
    src_names = P.names_path(P.NATIVE)
    if os.path.isfile(src_names):
        dst = os.path.join(P.names_dir(P.DEV), "names.json")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src_names, dst)
        make_writable(dst)
    rebuild_index(P.DEV)
    print("② 开发版已还原成原生：%s" % P.DEV)
    print("   写回 %d 个文件（点图 + 可走面），删掉 %d 个（我们加的）" % (copied, deleted))
    return 0


def _run_tool(script, extra, dry):
    """跑 tools/ 下的一个子脚本，把它的输出原样转出来；返回退出码。"""
    if not os.path.isfile(script):
        sys.exit("找不到 %s" % os.path.basename(script))
    cmd = [sys.executable, "-u", script] + list(extra) + (["--dry"] if dry else [])
    print("> python tools/%s%s%s" % (os.path.basename(script),
                                     (" " + " ".join(extra)) if extra else "",
                                     " --dry" if dry else ""))
    r = subprocess.run(cmd, cwd=HERE, capture_output=True)
    for blob in (r.stdout, r.stderr):
        text = (blob or b"").decode("utf-8", "replace").rstrip()
        if text:
            print(text)
    return r.returncode


def cmd_import(args):
    """整理开发版的导出收件箱：vis 归位（tidy_vis）+ 原始导出改写成 maps（organize_maps）。

    2026-11-21 四区改三区：收件箱和开发版已经是同一个目录（②\vis），
    不再有「从 ④ 拷到 ②」这一步，只剩「整理」两件事。--dry 只看会做什么。
    """
    rc = _run_tool(os.path.join(HERE, "tidy_vis.py"), (), args.dry)
    if rc != 0:
        return rc
    print("")
    rc = _run_tool(os.path.join(HERE, "organize_maps.py"), ("--archive",), args.dry)
    if rc != 0:
        return rc
    print("")
    print("② 开发版的图：%s" % P.DATA)
    print("   处理过的原始导出归档到：%s" % P.ARCHIVE)
    print("下一步：整理好的就是成品（dev\\<图>\\map.json、navmesh.bin）；"
          "测试包里的改动用 pack promote 发进成品")
    return 0



def cmd_diff(args):
    def snap(root):
        out = {}
        for rel, path in list(P.map_files(root)) + list(P.navmesh_files(root)):
            try:
                out[rel] = sha256(path)
            except OSError:
                pass
        for _fp, path in P.route_files(root):
            try:
                out[os.path.relpath(path, root).replace(os.sep, "/")] = sha256(path)
            except OSError:
                pass
        return out

    # 2026-11-21 三档启动后 ③ 不再存数据：只比 ② vs ①，另报成品里有哪些图。
    a, b = snap(P.DEV), snap(P.NATIVE)
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    print("== ② 开发版 vs ① 备份版")
    print("   只在开发版：%d" % len(only_a))
    for k in only_a[:20]:
        print("      + %s" % k)
    print("   只在备份版：%d" % len(only_b))
    for k in only_b[:20]:
        print("      - %s" % k)
    print("   内容不同：%d" % len(diff))
    for k in diff[:20]:
        print("      ~ %s" % k)
    print("")
    versions = final_versions()
    cur = final_current()
    print("== 成品：%d 个版本，当前启动 %s" % (len(versions), cur or "（没有）"))
    for v in versions:
        print("   %s %-12s %s  %d 张图" % (
            "●" if v["name"] == cur else " ", v["name"],
            (v.get("created") or "-")[:16], len(v.get("maps") or {})))
    if not versions:
        print("    （还没有成品版本 = 成品档没数据；编辑中做完用 pack promote 建第一版）")
    return 0


def cmd_status(args):
    print("UCF 导航数据 · 三区")
    print("")
    infos = [
        ("① 备份版（原生·只读）", P.NATIVE, "只读，永不编辑"),
        ("② 开发版（成品 + 收件箱 + 编辑中）", P.DEV, "final 是成品（多版本），packs 是编辑中"),
        ("③ 游戏目录（运行时·不放数据）", P.DEPLOY, "只放 dll / ucf_mod.json / markers\\"),
    ]
    for title, root, tip in infos:
        s = summary(root)
        print("%s  %s" % (title, s["path"]))
        print("    %s  数据 %d 个（图 %d / 可走面 %d / 路线 %d）  %s  最近改动 %s" % (
            "存在" if s["exists"] else "不存在", s["files"],
            s["sub"].get("图", 0), s["sub"].get("可走面", 0), s["sub"].get("路线", 0),
            human(s["bytes"]), s["mtime"]))
        print("    %s" % tip)
        print("")
    n_files, t_last = _walk_count(P.VIS)
    n_json = _walk_count(P.VIS, lambda f: f.lower().endswith(".json"))[0]
    n_bin = _walk_count(P.VIS, lambda f: f.startswith("navmesh") and f.lower().endswith(".bin"))[0]
    packs = pack_ids()      # 真·测试包（地图文件夹只是分类目录，不算）
    print("② 开发版的草稿区（导出 + 测试包）  %s" % P.VIS)
    print("    %s  导出 %d 个文件（raw %d / 可走面 %d）  测试包 %d 个（%s）  最近改动 %s" % (
        "存在" if os.path.isdir(P.EXPORT) else "不存在", n_files, n_json, n_bin,
        len(packs), "、".join(packs) if packs else "无",
        time.strftime("%Y-%m-%d %H:%M", time.localtime(t_last)) if t_last else "-"))
    print("    测试包：%s" % P.PACKS_DIR)
    versions = final_versions()
    cur = final_current()
    print("    成品版本：%d 个（当前启动 %s）  %s" % (
        len(versions), cur or "无", FINAL_ROOT))
    for v in versions[-5:]:
        print("      %s %-12s %s  %d 张图" % (
            "●" if v["name"] == cur else " ", v["name"],
            (v.get("created") or "-")[:16], len(v.get("maps") or {})))
    if len(versions) > 5:
        print("      …（只列最新 5 个，全部用 python navdata.py final list）")
    print("    导出先落这里；「整理导出」把它归进 <图>\\导出\\ + <图>\\map.json；"
          "编辑中做完用 pack promote 发进成品（默认新建一版）")
    print("")
    print("当前生效（UCF_PROFILE=%s）：%s" % (P.PROFILE, P.DATA))
    fz = os.path.join(P.manifest_dir(P.NATIVE), ".frozen.json")
    if os.path.isfile(fz):
        try:
            fr = read_json(fz)
            print("备份版冻结于 %s，%d 张图 / %d 个可走面" % (
                fr.get("frozen_at"), len(fr.get("maps") or []), len(fr.get("navmesh_bins") or [])))
        except Exception:
            pass
    return 0


# ---------------------------------------------------------------- ④ 测试包
# 测试包 = 一份「只对某一张图生效」的路线改动：
#   <游戏目录>\packs\<地图文件夹>\<包名>\<指纹>.txt
# 地图文件夹 = 地图英文场景名（TransportShip / Nano_DawnVillage …），按图归类。
# 插件靠环境变量 UCF_PACK（地图文件夹/包名）+ UCF_FP（只对哪张图套用）工作，
# 正式版 <游戏目录>\nav\ 一个字节都不动。两段都只允许 ASCII（插件是 C，用 ANSI 的
# CreateDirectoryA / fopen，中文路径没验证过）。
PACK_NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,48}$")


def packs_root():
    return P.PACKS_DIR


def _is_pack(path):
    if os.path.isfile(os.path.join(path, "manifest.json")):
        return True
    try:
        return any(re.match(r"^n\d+-[0-9a-fA-F]{16}\.txt$", fn) for fn in os.listdir(path))
    except OSError:
        return False


def pack_ids():
    r"""packs\ 下所有包 id（地图文件夹/包名）；根目录平铺的老包也算。"""
    root = packs_root()
    out = []
    try:
        entries = sorted(os.listdir(root))
    except OSError:
        return out
    for entry in entries:
        d = os.path.join(root, entry)
        if entry.startswith("_") or not os.path.isdir(d):
            continue
        if _is_pack(d):
            out.append(entry)
            continue
        try:
            subs = sorted(os.listdir(d))
        except OSError:
            continue
        for sub in subs:
            if os.path.isdir(os.path.join(d, sub)) and _is_pack(os.path.join(d, sub)):
                out.append("%s/%s" % (entry, sub))
    return out


def maps_index():
    """level -> {level, label, fp}；指纹只认 maps/*.json（游戏自己扫出来的）。"""
    out = {}
    for root in (P.DEPLOY, P.DATA):
        for _rel, path in P.map_files(root):
            try:
                m = (read_json(path) or {}).get("map") or {}
            except (OSError, ValueError):
                continue
            lv = str(m.get("level") or "")
            if not lv or lv in out:
                continue
            fp = str(m.get("fingerprint") or "")
            if not fp and lv == "level9":
                fp = "n0-0000000000000000"      # 暴风：原生 0 点，运行时就是这个指纹
            cn, _sc = map_table.row_of(lv)   # 中文名以《地图对照表》为准（暴风 JSON 里是旧名）
            out[lv] = {"level": lv, "label": cn or str(m.get("label") or m.get("scene") or lv),
                       "fp": fp, "scene": str(m.get("scene") or "")}
    return out


def edit_counts(path):
    """(node 行数, edge 行数)；文件不存在 = (0, 0)。"""
    node = edge = 0
    if not os.path.isfile(path):
        return (0, 0)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s.startswith("node "):
                node += 1
            elif s.startswith("edge "):
                edge += 1
    return (node, edge)


def write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def find_pack(name):
    r"""按 id（地图文件夹/包名）或只给包名找目录；只给包名时在各地图文件夹里找。"""
    root = packs_root()
    name = str(name or "").replace("\\", "/").strip("/")
    pdir = os.path.join(root, *name.split("/")) if name else ""
    if not pdir or not os.path.isdir(pdir):
        tail = name.split("/")[-1]
        hits = [x for x in pack_ids() if x.split("/")[-1] == tail]
        if len(hits) > 1:
            sys.exit("有多个同名测试包，请写全「地图文件夹/包名」：%s"
                     % ", ".join(hits))
        if hits:
            pdir = os.path.join(root, *hits[0].split("/"))
    if not pdir or not os.path.isdir(pdir):
        sys.exit("没有测试包 %r。先看 python navdata.py pack list" % name)
    man = {}
    try:
        man = read_json(os.path.join(pdir, "manifest.json")) or {}
    except (OSError, ValueError):
        pass
    fp = str(man.get("fp") or "")
    if not fp:
        txts = [f for f in os.listdir(pdir) if f.endswith(".txt")]
        fp = txts[0][:-4] if len(txts) == 1 else ""
    if not fp:
        sys.exit("包里没有指纹（manifest.json 缺 fp，目录里也没有唯一的 <指纹>.txt）：%s" % pdir)
    return pdir, man, fp


def cmd_pack_list(args):
    root = packs_root()
    print("测试包目录：%s" % root)
    names = pack_ids()
    if not names:
        print("（还没有任何测试包）")
        print("新建：python navdata.py pack new chain_a --level 11")
        return 0
    print("")
    print("| 测试包（地图文件夹/包名） | 地图 | 指纹 | 改动 | 建于 |")
    print("| --- | --- | --- | --- | --- |")
    for n in names:
        pdir = os.path.join(root, *n.split("/"))
        try:
            man = read_json(os.path.join(pdir, "manifest.json")) or {}
        except (OSError, ValueError):
            man = {}
        fp = str(man.get("fp") or "")
        if not fp:
            txts = [f for f in os.listdir(pdir) if f.endswith(".txt")]
            fp = txts[0][:-4] if txts else ""
        nd, ed = edit_counts(os.path.join(pdir, fp + ".txt")) if fp else (0, 0)
        print("| %s | %s %s | %s | node %d / edge %d%s | %s |" % (
            n, man.get("level", "?"), man.get("label", ""), fp or "-", nd, ed,
            (" · keep（原版+新增）" if man.get("keep") else
             (" · grow（空白地图）" if (man.get("grow") or man.get("blank")) else "")),
            man.get("created", "-")))
    print("")
    print("用法：控制台「人机路点」页 → 启动档「编辑中（packs·可写）」选包 + 地图，再点开始游戏；")
    print("      做完点「发布到成品」把 <指纹>.txt 拷进 ② 成品（final\\<包名>\\），成品档就能读到。")
    return 0


def cmd_pack_new(args):
    if not PACK_NAME_RE.match(args.name):
        sys.exit("包名只能用 ASCII 字母/数字/下划线/减号，1~48 字符：%r" % args.name)
    idx = maps_index()
    want = args.level if args.level.startswith("level") else "level" + args.level.strip("lL ")
    info = idx.get(want)
    if not info:
        extra = ""
        if want in ("level4", "level11"):
            extra = "\n  （%s 只有可走面、没有路点图 —— 点图改动对它不生效，测试包没有意义）" % want
        sys.exit("maps/*.json 里没有 %s 的路点数据。可用：%s%s" % (
            want, ", ".join("%s(%s)" % (k, v["label"]) for k, v in sorted(idx.items())), extra))
    fp = info["fp"]
    if not fp:
        sys.exit("%s 没有指纹（这张图没有路点图，测试包对它没有意义）" % args.level)
    srcroot = P.DEV if args.src == "dev" else P.DEPLOY
    src = os.path.join(srcroot, "nav", fp + ".txt")
    folder = map_table.folder_name(info["level"], info.get("scene") or "", info.get("label") or "")
    pdir = os.path.join(packs_root(), folder, args.name)
    os.makedirs(pdir, exist_ok=True)
    dst = os.path.join(pdir, fp + ".txt")
    grow = bool(getattr(args, "grow", False))
    keep = bool(getattr(args, "keep", False))
    if keep:
        # 原版基础 + 新增：原生点一个都不动，只把包里的 node add 建到图上。
        print("  keep 模式：原生点一个都不动（原版路线照常走），新点按 PointGraph.AddNode 新建")
    elif grow:
        # 空白地图：原生点由插件先全禁掉，包里的 node add / edge add 才是唯一路线。
        print("  grow 模式：原生点会全部标死，新点按 AddNode 新建（数量不受原生点数限制）")
    if keep:
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write("# ucf-navedit v1 fp=%s\nkeep\n" % fp)
        with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
            f.write("")
        print("已写 keep 包：%s（原生点原样保留；node 0 起步，进图后再加点）" % dst)
    elif grow:
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write("# ucf-navedit v1 fp=%s\ngrow\n" % fp)
        with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
            f.write("")                       # 存在即关掉自动铺点
        print("已写空白地图包：%s（node 0 / edge 0；原生点会在进图时全部禁用）" % dst)
    elif os.path.abspath(src) == os.path.abspath(dst):
        pass
    elif os.path.isfile(src):
        shutil.copyfile(src, dst)
        nd, ed = edit_counts(dst)
        print("从 %s 复制：node %d / edge %d" % (src, nd, ed))
    else:
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write("# ucf-navedit v1 fp=%s\n" % fp)
        print("%s 不存在（这张图还没有改动）—— 已建一份空清单，编辑器里改完再复制过来" % src)
    man = {
        "name": args.name,
        "folder": folder,
        "level": info["level"],
        "label": info["label"],
        "fp": fp,
        "scene": info.get("scene", ""),
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": ("keep" if keep else
                   "grow" if grow else ("dev" if args.src == "dev" else "deploy")),
        "grow": bool(grow),
        "keep": bool(keep),
        "note": ("keep 测试包：原生点一个都不动（原版路线照常走）+ 新点按 AddNode 新建" if keep
                 else "grow 测试包（空白地图）：原生点全禁用 + 新点按 AddNode 新建（不受原生点数限制）" if grow
                 else "测试包：只对 %s(%s) 生效；插件用 UCF_PACK + UCF_FP 读它" % (info["label"], info["level"])),
    }
    write_json(os.path.join(pdir, "manifest.json"), man)
    print("")
    print("已建测试包：%s" % pdir)
    print("  包名 %s   地图 %s(%s)   指纹 %s" % ("%s/%s" % (folder, args.name),
                                               info["label"], info["level"], fp))
    print("下一步：控制台 → 人机路点 → 编辑中（选 %s/%s）→ 地图（%s）→ 开始游戏" % (
        folder, args.name, info["label"]))
    return 0


def cmd_pack_diff(args):
    pdir, man, fp = find_pack(args.name)
    pfile = os.path.join(pdir, fp + ".txt")
    print("测试包 %s（%s %s）  指纹 %s" % (args.name, man.get("level", "?"), man.get("label", ""), fp))
    print("")
    cur = final_current()
    rows = [
        ("编辑中 packs\\%s" % args.name, pfile),
        ("成品 %s" % (cur or "（还没有版本）"), os.path.join(final_version_path(cur), fp + ".txt")),
    ]
    print("| 位置 | 文件 | node / edge | 大小 | sha256 |")
    print("| --- | --- | --- | --- | --- |")
    for title, f in rows:
        if not os.path.isfile(f):
            print("| %s | %s | - | 不存在 | - |" % (title, fp + ".txt"))
            continue
        nd, ed = edit_counts(f)
        print("| %s | %s | %d / %d | %s | %s |" % (
            title, fp + ".txt", nd, ed, human(os.path.getsize(f)), sha256(f)[:12]))
    return 0


def cmd_pack_promote(args):
    r"""编辑中 -> 成品：把 <指纹>.txt 发布进成品的一个版本。

    默认「新建一版」：以当前版本为底整套复制，再用这个包替换对应那张图，老版本不丢；
    新版本名 = 测试包名（--as 可改，重名自动加 -2）；--into <版本> 则是更新已有版本里的那一张图。
    成品档「按包启动」（UCF_PACK_DIR=final、UCF_PACK=<版本名>），和编辑中同一套加载
    逻辑，所以 grow / keep / 普通增量都能发，发过去效果一模一样。
    """
    pdir, man, fp = find_pack(args.name)
    src = os.path.join(pdir, fp + ".txt")
    if not os.path.isfile(src):
        sys.exit("包里没有 %s（先在里面写改动）" % (fp + ".txt"))
    grow, keep = pack_flags(src)
    nd, ed = edit_counts(src)
    note = (getattr(args, "note", "") or "").strip()
    into = (getattr(args, "into", "") or "").strip()
    if into and into not in [v["name"] for v in final_versions()]:
        sys.exit("没有这个成品版本：%s（现有：%s）" % (
            into, "、".join(v["name"] for v in final_versions()) or "无"))
    want = (getattr(args, "as_name", "") or "").strip() or final_name_from_pack(args.name)
    if args.dry:
        if into:
            print("  [dry] 会更新成品版本 %s 里的 %s.txt" % (into, fp))
        else:
            print("  [dry] 会新建一版 %s（以 %s 为底），写入 %s.txt" % (
                final_unique_name(want), final_current() or "空", fp))
        print("  [dry] 不写盘")
        return 0
    cur = final_current()
    if into:
        name = into
        print("包 %s -> 成品 %s（更新这一版）" % (args.name, name))
    else:
        name, copied = final_new_version(base=cur, note=note, name=want)
        print("包 %s -> 成品 %s（新建一版，版本名跟测试包；从 %s 继承 %d 个文件）" % (
            args.name, name, cur or "空", copied))
        if name != want:
            print("  已经有叫 %s 的版本了，这一版叫 %s（老版本一个没动）" % (want, name))
    d = final_version_path(name)
    os.makedirs(d, exist_ok=True)
    dst = os.path.join(d, fp + ".txt")
    if os.path.exists(dst):
        make_writable(dst)
    shutil.copyfile(src, dst)
    make_readonly(dst)
    final_ensure_nogen(d)
    idx = final_index_read()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    for v in idx.get("versions") or []:
        if v.get("name") != name:
            continue
        v["updated"] = now
        if note:
            v["note"] = note
        maps = v.setdefault("maps", {})
        meta = {"file": fp + ".txt", "level": man.get("level", ""), "label": man.get("label", ""),
                "from_pack": args.name, "published": now}
        meta.update(final_scan_maps(d)[fp])
        maps[fp] = dict(maps.get(fp) or {}, **meta)
        break
    idx["current"] = name
    final_index_write(idx)
    print("  改动 node %d / edge %d   地图 %s %s" % (nd, ed, man.get("level", "?"), man.get("label", "")))
    if keep:
        print("  原版 + 新增（keep）：成品档同样保留原生点，只加你画的点")
    elif grow:
        print("  空白地图（grow）：成品档同样禁用原生点 + AddNode 建点")
    print("  本图 sha %s   成品共 %d 个版本，当前启动 %s" % (
        sha256(dst)[:12], len(final_versions()), name))
    print("  控制台点「开始游戏 · 成品 %s」立即生效，不用再部署。" % name)
    return 0


# ---------------------------------------------------------------- 成品版本命令
def cmd_final_list(args):
    versions = final_versions()
    cur = final_current()
    if not versions:
        print("成品还没有任何版本。「人机路点」页 → 启动档「编辑中」→ 标签「发布到成品」就会建第一版。")
        print("  成品版本目录：%s" % FINAL_ROOT)
        return 0
    print("成品版本（%d 个）  %s" % (len(versions), FINAL_ROOT))
    for v in versions:
        print("  %s %-12s 建 %s  更新 %s  %d 张图  %s%s" % (
            "●" if v["name"] == cur else " ", v["name"], (v.get("created") or "-")[:16],
            (v.get("updated") or "-")[:16], len(v.get("maps") or {}),
            ("← 继承 %s" % v["base"]) if v.get("base") else "",
            ("  " + v["note"]) if v.get("note") else ""))
        if not v.get("exists"):
            print("      目录不见了：%s" % v.get("path"))
            continue
        for fp, m in sorted((v.get("maps") or {}).items()):
            print("      - %-22s %-10s %4d/%-4d sha %s  ← %s" % (
                (m.get("file") or fp + ".txt"), (m.get("label") or ""), m.get("node", 0),
                m.get("edge", 0), (m.get("sha256") or "")[:8], (m.get("from_pack") or "-")))
    print("")
    print("  ● = 当前启动的版本；换版本：python navdata.py final use <版本名>")
    return 0


def cmd_final_use(args):
    final_set_current(args.name)
    print("当前成品版本 = %s（控制台「开始游戏 · 成品」启动它）" % args.name)
    return 0


def cmd_final_rename(args):
    new = (args.new or "").strip()
    err = final_check_name(new)
    if err:
        sys.exit(err)
    idx = final_index_read()
    hit = None
    for v in idx.get("versions") or []:
        if v.get("name") == args.name:
            hit = v
            break
    if not hit:
        sys.exit("没有这个成品版本：%s" % args.name)
    olddir, newdir = final_version_path(args.name), final_version_path(new)
    if not os.path.isdir(olddir):
        sys.exit("版本目录不见了：%s" % olddir)
    os.rename(olddir, newdir)
    hit["name"] = new
    hit["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if idx.get("current") == args.name:
        idx["current"] = new
    final_index_write(idx)
    print("已改名：%s -> %s" % (args.name, new))
    return 0


def final_delete_dir(d):
    r"""物理删掉一个版本目录：先去掉只读属性（Windows 下只读文件删不掉），再 rmtree。"""
    if not d or not os.path.isdir(d):
        return False
    for root, _dirs, files in os.walk(d):
        for fn in files:
            try:
                make_writable(os.path.join(root, fn))
            except OSError:
                pass
    shutil.rmtree(d)
    return True


def cmd_final_rm(args):
    r"""删掉一个成品版本：默认**真删**（final\<版本>\ 整个目录，删了找不回来）；
    加 --keep 才是旧行为（挪进 dev\archive\final_old\，留个后手）。

    删到一版不剩也可以：成品变成「没有版本」，启动就是原版，下次发布又会有一版。
    """
    versions = final_versions()
    if args.name not in [v["name"] for v in versions]:
        sys.exit("没有这个成品版本：%s" % args.name)
    d = final_version_path(args.name)
    if getattr(args, "keep", False):
        os.makedirs(FINAL_ARCHIVE, exist_ok=True)
        dst = os.path.join(FINAL_ARCHIVE, "%s_%s" % (args.name, time.strftime("%Y%m%d_%H%M%S")))
        if os.path.isdir(d):
            shutil.move(d, dst)
        print("已挪走 %s -> %s（不是物理删除，想找回来去这儿拿）" % (args.name, dst))
    else:
        try:
            final_delete_dir(d)
        except OSError as exc:
            sys.exit("删不掉 %s：%s（游戏正开着读它？关掉游戏再删）" % (d, exc))
        print("已删除成品版本 %s（%s）" % (args.name, d))
    idx = final_index_read()
    idx["versions"] = [v for v in (idx.get("versions") or []) if v.get("name") != args.name]
    if idx.get("current") == args.name:
        idx["current"] = ""
    if not idx["versions"]:
        idx["seq"] = 0          # 全删光了：以后老成品迁移重新从 v1 编号
    final_index_write(idx)
    cur = final_current()
    if cur:
        final_set_current(cur)
        print("当前成品版本改为 %s" % cur)
    else:
        print("成品里已经没有版本了：启动成品 = 原版；发布一版就会重新有。")
    return 0


def cmd_pack_compare(args):
    pdir, man, fp = find_pack(args.name)
    src = os.path.join(pdir, fp + ".txt")
    ver = (getattr(args, "final", "") or "").strip() or final_current()
    versions = {v["name"]: v for v in final_versions()}
    if not ver or ver not in versions:
        sys.exit("没有这个成品版本：%s（现有：%s）" % (ver, "、".join(versions) or "无"))
    v = versions[ver]
    fmeta = (v.get("maps") or {}).get(fp) or {}
    pmeta = {"sha256": "", "node": 0, "edge": 0, "mtime": "-"}
    if os.path.isfile(src):
        nd, ed = edit_counts(src)
        pmeta = {"sha256": sha256(src), "node": nd, "edge": ed,
                 "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(src)))}
    print("成品 %s（建 %s）  vs  编辑中 %s（%s）" % (
        ver, (v.get("created") or "-")[:16], args.name, man.get("label", "")))
    print("")
    print("| 位置 | 时间 | 点 / 边 | sha256 |")
    print("| --- | --- | --- | --- |")
    print("| 编辑中 | %s | %d / %d | %s |" % (pmeta["mtime"], pmeta["node"], pmeta["edge"],
                                             (pmeta["sha256"] or "-")[:12]))
    if fmeta:
        print("| 成品 %s | %s | %d / %d | %s |" % (ver, fmeta.get("mtime", "-"), fmeta.get("node", 0),
                                                   fmeta.get("edge", 0), (fmeta.get("sha256") or "-")[:12]))
    else:
        print("| 成品 %s | - | - | 这一版里没有这张图 |" % ver)
    same = bool(pmeta["sha256"]) and pmeta["sha256"] == fmeta.get("sha256")
    print("")
    print("结论：%s" % ("一致（数据同一个文件，玩起来一样）" if same else "不一致（成品不是这个包发的，或发布后又改过）"))
    return 0


def main():
    _setup_console()
    print("")
    print("=== %s  navdata.py %s  (UCF_PROFILE=%s) ===" % (
        time.strftime("%Y-%m-%d %H:%M:%S"), " ".join(sys.argv[1:]) or "status", P.PROFILE))
    ap = argparse.ArgumentParser(description="导航数据三区管理（备份 / 开发 / 部署）")
    sub = ap.add_subparsers(dest="cmd")
    try:
        final_ensure_root()          # 首次运行：旧成品（②\nav）自动搬成 v1
    except OSError:
        pass

    q = sub.add_parser("freeze", help="用当前数据重建「备份版」（只收原生）")
    q.add_argument("--from", dest="src", help="源目录（默认 ③ 游戏目录；已清空，一般显式指定）")
    q.add_argument("--force", action="store_true", help="已存在也重建")
    q.set_defaults(func=cmd_freeze)

    q = sub.add_parser("verify", help="校验备份版没被动过")
    q.set_defaults(func=cmd_verify)

    q = sub.add_parser("restore", help="开发版 <- 备份版（丢掉开发版改动）")
    q.set_defaults(func=cmd_restore)

    q = sub.add_parser("import", help="整理开发版：vis 归位 + 原始导出 -> maps")
    q.add_argument("--dry", action="store_true")
    q.set_defaults(func=cmd_import)


    q = sub.add_parser("diff", help="开发版 vs 备份版 + 成品里有几张图")
    q.set_defaults(func=cmd_diff)

    q = sub.add_parser("status", help="三区状态")
    q.set_defaults(func=cmd_status)

    q = sub.add_parser("final", help="成品版本：列表 / 选启动版本 / 改名 / 删除")
    q.set_defaults(func=cmd_final_list)
    fs_ = q.add_subparsers(dest="final_cmd")
    f2 = fs_.add_parser("list", help="列出成品所有版本")
    f2.set_defaults(func=cmd_final_list)
    f2 = fs_.add_parser("use", help="选这次启动哪个版本")
    f2.add_argument("name")
    f2.set_defaults(func=cmd_final_use)
    f2 = fs_.add_parser("rename", help="给版本改名（自动 v1/v2 之外的方案）")
    f2.add_argument("name")
    f2.add_argument("new")
    f2.set_defaults(func=cmd_final_rename)
    f2 = fs_.add_parser("rm", help="删掉一个版本（真删目录；--keep 才挪进 archive）")
    f2.add_argument("name")
    f2.add_argument("--keep", action="store_true",
                    help="不真删：挪进 archive\\final_old\\（留个后手）")
    f2.set_defaults(func=cmd_final_rm)

    q = sub.add_parser("pack", help="测试包：只对一张图生效的路线数据（② navdata\\dev\\packs/）")
    q.set_defaults(func=cmd_pack_list)
    ps = q.add_subparsers(dest="pack_cmd")
    q2 = ps.add_parser("list", help="列出测试包")
    q2.set_defaults(func=cmd_pack_list)
    q2 = ps.add_parser("new", help="新建测试包（复制该图现有的改动）")
    q2.add_argument("name")
    q2.add_argument("--level", required=True, help="levelN 或纯数字，例：--level 11")
    q2.add_argument("--from", dest="src", choices=["dev", "deploy"], default="dev")
    q2.add_argument("--grow", action="store_true",
                    help="空白地图：原生点全禁用 + 新点按 AddNode 新建（数量不受原生点数限制）")
    q2.add_argument("--keep", action="store_true",
                    help="原版基础 + 新增：原生点一个都不动，只把新点按 AddNode 建上去")
    q2.set_defaults(func=cmd_pack_new)
    q2 = ps.add_parser("diff", help="包 vs 成品 nav")
    q2.add_argument("name")
    q2.set_defaults(func=cmd_pack_diff)
    q2 = ps.add_parser("promote", help="编辑中 -> 成品（默认新建一版，老版本保留）")
    q2.add_argument("name")
    q2.add_argument("--into", metavar="版本", default="",
                    help="更新指定的成品版本（默认：以当前版本为底新建一版）")
    q2.add_argument("--note", default="", help="这一版的备注（建新版本时记进台账）")
    q2.add_argument("--as", dest="as_name", metavar="版本名", default="",
                    help="自定义版本名（默认沿用测试包名，重名自动加 -2）")
    q2.add_argument("--dry", action="store_true")
    q2.set_defaults(func=cmd_pack_promote)
    q2 = ps.add_parser("compare", help="一个包 vs 某个成品版本（默认当前版本）")
    q2.add_argument("name")
    q2.add_argument("--final", default="", help="成品版本名（默认当前启动的那版）")
    q2.set_defaults(func=cmd_pack_compare)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        return cmd_status(args)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
