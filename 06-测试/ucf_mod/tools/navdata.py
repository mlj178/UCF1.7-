#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""navdata.py —— 导航数据「四版」管理：① 备份  ② 开发  ③ 部署  ④ 测试

  ---------------------------------------------------------------------------
  ① 备份版  navdata/native/      UCF 原版数据，只读、永不编辑（本脚本之外没人写它）
  ② 开发版  navdata/dev/         日常在这里编辑（编辑器默认打开这一版）
  ③ 部署版  游戏目录 ucf_mod/     游戏里的插件读这一版，由 publish 从开发版推过去
  ④ 测试版  navdata/test/        插件导出 + 测试包 + 归档，脏了也不影响 ② ③
                                   vis\      导出收件箱（Ctrl+E / navmesh 落这里）
                                   packs\    测试包
                                   archive\  处理过的导出 / 只读还原点
  流水线：游戏导出 -> ④ ->（import）-> ② ->（publish）-> ③；① 随时 freeze
  ---------------------------------------------------------------------------

常用命令（在 tools/ 下跑）：

    python navdata.py status              # 四版各自在哪、各有几个文件、是否只读
    python navdata.py verify              # 校验备份版没被动过（SHA256 清单）
    python navdata.py restore             # 开发版 <- 备份版（丢掉开发版的改动）
    python navdata.py import              # 测试版 -> 开发版（可走面 + 原始导出）
    python navdata.py publish             # 部署版 <- 开发版（推给游戏）
    python navdata.py diff                # 开发版 vs 备份版 / 开发版 vs 部署版 差在哪
    python navdata.py freeze --force      # 用当前数据重建「备份版」（只在确认要重新冻结时用）

  测试包（④ 的一部分）：一份只对某一张图生效的路线改动，放在
  navdata\test\packs\<序号_场景名中文名>\<包名>\<指纹>.txt（序号见《地图对照表》）；
  插件用 UCF_PACK / UCF_FP 读它，
  正式版 nav\ 一个字节都不动。控制台启动前可以选"正式版 / 测试包 + 只对哪张图生效"。

    python navdata.py pack list                     # 有哪些测试包
    python navdata.py pack new chain_a --level 11   # 从开发版复制 level11 的改动做包
    python navdata.py pack diff chain_a             # 包 vs 开发版 / 部署版
    python navdata.py pack promote chain_a          # 包 -> 开发版（再手动「部署到游戏」）

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


def walk_files(root):
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            p = os.path.join(dirpath, fn)
            out.append(os.path.relpath(p, root).replace(os.sep, "/"))
    out.sort()
    return out


def summary(root):
    if not os.path.isdir(root):
        return {"path": root, "exists": False, "files": 0, "bytes": 0, "mtime": "-", "sub": {}}
    sub, files, size, latest = {}, 0, 0, 0.0
    for d in SUBS:
        p = os.path.join(root, d)
        sub[d] = len(walk_files(p)) if os.path.isdir(p) else 0
        files += sub[d]
    for rel in walk_files(root):
        p = os.path.join(root, rel.replace("/", os.sep))
        try:
            size += os.path.getsize(p)
            latest = max(latest, os.path.getmtime(p))
        except OSError:
            pass
    return {"path": root, "exists": True, "files": files, "bytes": size,
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

    if os.path.isdir(P.NATIVE) and walk_files(P.NATIVE):
        if not args.force:
            sys.exit("备份版已存在：%s\n要重建请加 --force（旧的会被删掉）" % P.NATIVE)
        for rel in walk_files(P.NATIVE):
            make_writable(os.path.join(P.NATIVE, rel.replace("/", os.sep)))
        shutil.rmtree(P.NATIVE, ignore_errors=True)

    tmp = P.NATIVE + ".tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    for d in SUBS:
        os.makedirs(os.path.join(tmp, d), exist_ok=True)

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
        if str(m.get("origin") or "") == "native-empty":
            # 之前生成的「原生为空」空档：原样保留，别当成「来源不明」再生成一遍
            save_json(os.path.join(tmp, "maps", fn), doc)
            kept.append({"file": fn, "level": level, "cn": str(m.get("label") or ""),
                         "scene": str(m.get("scene") or ""), "nodes": 0, "edges": 0,
                         "fp": "", "source": "native-empty"})
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
        save_json(os.path.join(tmp, "maps", fn), doc)
        kept.append({"file": fn, "level": level, "cn": str(m.get("label") or ""),
                     "scene": str(m.get("scene") or ""), "nodes": len(doc.get("nodes") or []),
                     "edges": len(doc.get("edges") or []),
                     "fp": str(m.get("fingerprint") or ""),
                     "source": str(m.get("source") or "")})

    for s in stubs:
        fn = "%s_%s.json" % (s["no"], s["cn"])
        save_json(os.path.join(tmp, "maps", fn), empty_stub(s["level"], s["cn"], s["scene"], s["why"]))
        kept.append({"file": fn, "level": s["level"], "cn": s["cn"], "scene": s["scene"],
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
    bins = []
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
                if fn.lower().endswith(".bin") and fn.startswith("navmesh"):
                    if fn in bins:
                        continue
                    shutil.copy2(os.path.join(base, fn), os.path.join(tmp, "vis", fn))
                    bins.append(fn)

    names = {}
    for r in load_table():
        names[r["level"]] = {"name": r["cn"], "level": r["level"]}
        if r["scene"]:
            names[r["scene"]] = {"name": r["cn"], "level": r["level"]}
    for k in kept:
        if k["fp"]:
            names[k["fp"]] = {"name": k["cn"] or table.get(k["level"], {}).get("cn", ""),
                              "level": k["level"]}
    save_json(os.path.join(tmp, "nav", "names.json"), names)

    sums = []
    for rel in walk_files(tmp):
        sums.append("%s  %s" % (sha256(os.path.join(tmp, rel.replace("/", os.sep))), rel))
    with open(os.path.join(tmp, "SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sums) + "\n")

    frozen = {
        "kind": "ucf-navdata-native",
        "frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": src,
        "rule": "只收 map.source == game 的导出；我们造的（ours/practice）一律不收，只在空档文件里记录原因",
        "maps": kept,
        "navmesh_bins": bins,
        "skipped": [{"file": f, "why": w} for f, w in skipped],
        "edits_dropped": [{"file": f, "firstLine": h} for f, h in edits],
        "manifest_sha256": hashlib.sha256("\n".join(sums).encode("utf-8")).hexdigest(),
    }
    save_json(os.path.join(tmp, ".frozen.json"), frozen)
    with open(os.path.join(tmp, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(native_readme(frozen, sums))
    for rel in walk_files(tmp):
        make_readonly(os.path.join(tmp, rel.replace("/", os.sep)))
    os.replace(tmp, P.NATIVE)

    print("① 备份版已生成：%s" % P.NATIVE)
    for k in kept:
        print("   收  %-22s %-8s %-6s %3d 点 / %3d 边  %s" % (
            k["file"], k["level"], k["cn"], k["nodes"], k["edges"], k["fp"] or "-"))
    for f, w in skipped:
        print("   丢  %-22s %s" % (f, w))
    for f, h in edits:
        print("   丢  nav/%-24s 编辑清单（第一个操作：%s）" % (f, h or "-"))
    for b in bins:
        print("   收  vis/%-24s 可走面" % b)
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
    L.append("| 文件 | 关卡 | 中文名 | 节点 | 边 | 指纹 |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for k in frozen["maps"]:
        L.append("| %s | %s | %s | %d | %d | %s |" % (
            k["file"], k["level"], k["cn"], k["nodes"], k["edges"], k["fp"] or "—"))
    L.append("")
    if frozen["navmesh_bins"]:
        L.append("可走面（NavMeshGraph 导出，游戏自己烘焙的网格）：%d 个 —— %s"
                 % (len(frozen["navmesh_bins"]), "、".join(frozen["navmesh_bins"])))
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
    L.append("python navdata.py status      # 三版在哪、多少文件")
    L.append("python navdata.py verify      # 校验这一版没被动过")
    L.append("python navdata.py restore     # 开发版 <- 这里（还原）")
    L.append("python navdata.py publish     # 部署版 <- 开发版（推给游戏）")
    L.append(fence)
    L.append("")
    L.append("清单：`SHA256SUMS.txt`（%d 个文件），机器可读信息：`.frozen.json`。" % len(sums))
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- ② verify
def cmd_verify(args):
    sums = os.path.join(P.NATIVE, "SHA256SUMS.txt")
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
    have = set(walk_files(P.NATIVE)) - {"SHA256SUMS.txt", "README.md", ".frozen.json"}
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
    """给 maps/_index.json + INDEX.md 重新生成一份（编辑器排序列要用）。"""
    table = load_table()
    rows = []
    maps_dir = os.path.join(root, "maps")
    by_level = {}
    if os.path.isdir(maps_dir):
        for fn in sorted(os.listdir(maps_dir)):
            if not fn.lower().endswith(".json") or fn in ("_index.json", "names.json"):
                continue
            try:
                doc = read_json(os.path.join(maps_dir, fn))
            except Exception:
                continue
            m = doc.get("map") or {}
            by_level[str(m.get("level") or "")] = {
                "file": fn, "fingerprint": str(m.get("fingerprint") or ""),
                "nodes": len(doc.get("nodes") or []), "edges": len(doc.get("edges") or []),
                "features": len(doc.get("features") or []),
                "exported": str(doc.get("generated") or ""),
                "source": str(m.get("source") or ""), "origin": str(m.get("origin") or ""),
            }
    for r in table:
        info = by_level.get(r["level"]) or {}
        rows.append({
            "no": r["no"], "level": r["level"], "name": r["cn"], "scene": r["scene"], "note": r["note"],
            "file": info.get("file", ""), "fingerprint": info.get("fingerprint", ""),
            "nodes": info.get("nodes", 0), "edges": info.get("edges", 0),
            "features": info.get("features", 0), "exported": info.get("exported", ""),
            "source": info.get("source", ""), "origin": info.get("origin", ""),
            "status": "有数据" if info.get("file") else "待采集",
        })
    doc = {"format": "ucf-map-index", "version": 1,
           "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
           "ucf": P.DATA,
           "note": "这份索引由 tools/navdata.py 按 docs/地图对照表.md 生成；节点/边是当前这一版里的原生数据。",
           "maps": rows, "extras": []}
    save_json(os.path.join(maps_dir, "_index.json"), doc)
    md = ["# 当前版本的地图数据（自动生成，勿手改）", "",
          "生成时间：" + doc["generated"], "",
          "| 序号 | 关卡 | 中文名 | 场景名 | 节点 | 边 | 文件 | 状态 |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for it in rows:
        md.append("| %s | %s | **%s** | %s | %s | %s | %s | %s |" % (
            it["no"], it["level"], it["name"], it["scene"] or "-",
            it["nodes"] or "-", it["edges"] or "-", it["file"] or "-", it["status"]))
    md += ["", "数据来源：UCF 原版（插件进图 Scan 导出）。我们手工加的点和编辑都不在这一版里。", ""]
    with open(os.path.join(maps_dir, "INDEX.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md))


def cmd_restore(args):
    if not walk_files(P.NATIVE):
        sys.exit("备份版是空的：%s\n先跑 python navdata.py freeze" % P.NATIVE)
    total_c, total_d = 0, 0
    for sub in ("maps", "nav"):
        c, d = mirror(os.path.join(P.NATIVE, sub), os.path.join(P.DEV, sub), strict=True)
        total_c += c
        total_d += d
    c2, _d2 = mirror(os.path.join(P.NATIVE, "vis"), os.path.join(P.DEV, "vis"), strict=False)
    rebuild_index(P.DEV)
    print("② 开发版已还原成原生：%s" % P.DEV)
    print("   maps/nav 写入 %d 个文件，删掉 %d 个（我们加的）；vis 补了 %d 个可走面" % (total_c, total_d, c2))
    return 0


def cmd_import(args):
    """④ 测试版 -> ② 开发版：可走面拷进 dev/vis，原始导出交给 organize_maps 改写到 dev/maps。

    这是四版里唯一「测试 -> 开发」的入口：插件只往 ④ 写，人决定哪些数据值得进 ②；
    进 ② 之后仍然要手动「部署到游戏」才会到 ③。--dry 只看会做什么。
    """
    devvis = os.path.join(P.DEV, "vis")
    roots = [P.VIS]
    if args.legacy and os.path.abspath(P.LEGACY_VIS) not in [os.path.abspath(x) for x in roots]:
        roots.append(P.LEGACY_VIS)
    copied = same = 0
    for root in roots:
        if not os.path.isdir(root):
            continue
        for base_dir, dirs, fns in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ("_state", "_noise", "raw")]
            for fn in sorted(fns):
                if not (fn.startswith("navmesh") and fn.lower().endswith(".bin")):
                    continue
                src = os.path.join(base_dir, fn)
                dst = os.path.join(devvis, fn)
                if os.path.isfile(dst) and sha256(dst) == sha256(src):
                    same += 1
                    continue
                if args.dry:
                    print("  [dry] 会拷贝可走面 %s" % fn)
                    continue
                os.makedirs(devvis, exist_ok=True)
                shutil.copy2(src, dst)
                copied += 1
    print("② 开发版可走面：%s %d 个 -> %s（已相同 %d 个）" % (
        "会新增/更新" if args.dry else "新增/更新", copied, devvis, same))

    script = os.path.join(HERE, "organize_maps.py")
    if not os.path.isfile(script):
        sys.exit("找不到 organize_maps.py：%s" % script)
    cmd = [sys.executable, "-u", script, "--archive"] + (["--dry"] if args.dry else [])
    print("")
    print("> python tools/organize_maps.py --archive%s" % (" --dry" if args.dry else ""))
    r = subprocess.run(cmd, cwd=HERE, capture_output=True)
    out = (r.stdout or b"").decode("utf-8", "replace").rstrip()
    err = (r.stderr or b"").decode("utf-8", "replace").rstrip()
    if out:
        print(out)
    if err:
        print(err)
    if r.returncode != 0:
        return r.returncode
    print("")
    print("④ 里处理过的原始导出归档到：%s" % P.ARCHIVE)
    print("下一步：控制台「部署到游戏 ②→③」（或 python navdata.py publish）")
    return 0


def cmd_publish(args):
    s = summary(P.DEV)
    if not s["exists"] or s["files"] == 0:
        sys.exit("开发版是空的：%s" % P.DEV)
    if args.dry:
        print("[dry] 会把 %s 的 maps/ nav/ 覆盖到 %s" % (P.DEV, P.DEPLOY))
        return 0
    total_c, total_d = 0, 0
    for sub in ("maps", "nav"):
        c, d = mirror(os.path.join(P.DEV, sub), os.path.join(P.DEPLOY, sub), strict=True, keep=KEEP_ALWAYS)
        total_c += c
        total_d += d
    rebuild_index(P.DEPLOY)
    print("③ 部署版已更新：%s" % P.DEPLOY)
    print("   写入 %d 个文件，删掉 %d 个（部署版里开发版没有的）" % (total_c, total_d))
    print("   游戏里的插件下次进图就会读这一版")
    return 0


def cmd_diff(args):
    def snap(root):
        out = {}
        for sub in ("maps", "nav"):
            base = os.path.join(root, sub)
            for rel in walk_files(base):
                q = os.path.join(base, rel.replace("/", os.sep))
                try:
                    out[sub + "/" + rel] = sha256(q)
                except OSError:
                    pass
        return out

    nat, dev, dep = snap(P.NATIVE), snap(P.DEV), snap(P.DEPLOY)
    for name, a, b in (("开发版 vs 备份版", dev, nat), ("开发版 vs 部署版", dev, dep)):
        print("== %s" % name)
        only_a = sorted(set(a) - set(b))
        only_b = sorted(set(b) - set(a))
        diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        print("   只在前者：%d" % len(only_a))
        for k in only_a[:20]:
            print("      + %s" % k)
        print("   只在后者：%d" % len(only_b))
        for k in only_b[:20]:
            print("      - %s" % k)
        print("   内容不同：%d" % len(diff))
        for k in diff[:20]:
            print("      ~ %s" % k)
    return 0


def cmd_status(args):
    print("UCF 导航数据 · 四版")
    print("")
    infos = [
        ("① 备份版（原生·只读）", P.NATIVE, "只读，永不编辑"),
        ("② 开发版（可编辑）", P.DEV, "编辑器默认读写这里"),
        ("③ 部署版（游戏目录）", P.DEPLOY, "游戏里的插件读这里"),
    ]
    for title, root, tip in infos:
        s = summary(root)
        print("%s  %s" % (title, s["path"]))
        print("    %s  文件 %d 个（maps %d / nav %d / vis %d）  %s  最近改动 %s" % (
            "存在" if s["exists"] else "不存在", s["files"],
            s["sub"].get("maps", 0), s["sub"].get("nav", 0), s["sub"].get("vis", 0),
            human(s["bytes"]), s["mtime"]))
        print("    %s" % tip)
        print("")
    n_files, t_last = _walk_count(P.VIS)
    n_json = _walk_count(P.VIS, lambda f: f.lower().endswith(".json"))[0]
    n_bin = _walk_count(P.VIS, lambda f: f.startswith("navmesh") and f.lower().endswith(".bin"))[0]
    packs = pack_ids()      # 真·测试包（地图文件夹只是分类目录，不算）
    print("④ 测试版（导出 + 测试包）  %s" % P.TEST)
    print("    %s  导出 %d 个文件（raw %d / 可走面 %d）  测试包 %d 个（%s）  最近改动 %s" % (
        "存在" if os.path.isdir(P.TEST) else "不存在", n_files, n_json, n_bin,
        len(packs), "、".join(packs) if packs else "无",
        time.strftime("%Y-%m-%d %H:%M", time.localtime(t_last)) if t_last else "-"))
    print("    导出根：%s" % P.VIS)
    print("    测试包：%s" % P.PACKS_DIR)
    print("    插件导出落在 ④；要进 ② 用「导入到开发版」，② 再由「部署到游戏」推 ③")
    print("")
    print("当前生效（UCF_PROFILE=%s）：%s" % (P.PROFILE, P.DATA))
    fz = os.path.join(P.NATIVE, ".frozen.json")
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
    for d in (os.path.join(P.DEPLOY, "maps"), P.MAPS):
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.endswith(".json") or fn.startswith("_"):
                continue
            try:
                m = (read_json(os.path.join(d, fn)) or {}).get("map") or {}
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
    print("用法：控制台里选「测试包」+ 包名 + 地图，再点开始游戏。")
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
    print("下一步：控制台 → 人机路点 → 测试包（选 %s/%s）→ 地图（%s）→ 开始游戏" % (
        folder, args.name, info["label"]))
    return 0


def cmd_pack_diff(args):
    pdir, man, fp = find_pack(args.name)
    pfile = os.path.join(pdir, fp + ".txt")
    print("测试包 %s（%s %s）  指纹 %s" % (args.name, man.get("level", "?"), man.get("label", ""), fp))
    print("")
    rows = [
        ("测试包 packs\\%s" % args.name, pfile),
        ("开发版 navdata\\dev\\nav", os.path.join(P.DEV, "nav", fp + ".txt")),
        ("部署版 <游戏目录>\\nav", os.path.join(P.DEPLOY, "nav", fp + ".txt")),
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
    pdir, man, fp = find_pack(args.name)
    src = os.path.join(pdir, fp + ".txt")
    if not os.path.isfile(src):
        sys.exit("包里没有 %s（先在里面写改动）" % (fp + ".txt"))
    try:
        with open(src, "r", encoding="utf-8", errors="replace") as f:
            lines = [ln.strip() for ln in f]
        # blank 是旧写法（现在等同于 grow），一起拦下来
        is_grow = any(ln in ("grow", "blank") for ln in lines)
        is_keep = any(ln == "keep" for ln in lines)
    except OSError:
        is_grow = is_keep = False
    if is_keep:
        sys.exit("这是 keep 测试包（原版基础 + 新增），不能升到正式版 nav\\："
                 "正式版只做增量改动，没有运行期新建节点的链路。")
    if is_grow:
        sys.exit("这是 grow 测试包（空白地图），不能升到正式版 nav\\："
                 "正式版走增量改动，节点只增不减，先把 grow 的套用逻辑做成正式链路再说。")
    # 四版纪律：包只升到 ② 开发版，再由「部署到游戏」统一推 ③。
    navdir = os.path.join(P.DEV, "nav")
    os.makedirs(navdir, exist_ok=True)
    dst = os.path.join(navdir, fp + ".txt")
    nd, ed = edit_counts(src)
    print("包 %s -> ② 开发版：%s" % (args.name, dst))
    print("  改动 node %d / edge %d   地图 %s %s" % (nd, ed, man.get("level", "?"), man.get("label", "")))
    if os.path.isfile(dst):
        bak = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S")
        if args.dry:
            print("  [dry] 会先备份成 %s" % os.path.basename(bak))
        else:
            shutil.copyfile(dst, bak)
            print("  旧文件已备份：%s" % os.path.basename(bak))
    else:
        print("  正式版原来没有这张图的改动（新文件）")
    if args.dry:
        print("  [dry] 不写盘")
        return 0
    shutil.copyfile(src, dst)
    print("  已写入 ② 开发版。要进游戏请在控制台点「部署到游戏 ②→③」"
          "（或 python navdata.py publish）")
    return 0


def main():
    _setup_console()
    print("")
    print("=== %s  navdata.py %s  (UCF_PROFILE=%s) ===" % (
        time.strftime("%Y-%m-%d %H:%M:%S"), " ".join(sys.argv[1:]) or "status", P.PROFILE))
    ap = argparse.ArgumentParser(description="导航数据四版管理（备份 / 开发 / 部署 / 测试）")
    sub = ap.add_subparsers(dest="cmd")

    q = sub.add_parser("freeze", help="用当前数据重建「备份版」（只收原生）")
    q.add_argument("--from", dest="src", help="源目录（默认部署版游戏目录）")
    q.add_argument("--force", action="store_true", help="已存在也重建")
    q.set_defaults(func=cmd_freeze)

    q = sub.add_parser("verify", help="校验备份版没被动过")
    q.set_defaults(func=cmd_verify)

    q = sub.add_parser("restore", help="开发版 <- 备份版（丢掉开发版改动）")
    q.set_defaults(func=cmd_restore)

    q = sub.add_parser("import", help="开发版 <- 测试版（可走面 + 原始导出）")
    q.add_argument("--legacy", action="store_true", help="顺带扫旧位置 ③\\vis（迁移过渡）")
    q.add_argument("--dry", action="store_true")
    q.set_defaults(func=cmd_import)

    q = sub.add_parser("publish", help="部署版 <- 开发版（推给游戏）")
    q.add_argument("--dry", action="store_true")
    q.set_defaults(func=cmd_publish)

    q = sub.add_parser("diff", help="开发版 vs 备份版 / 部署版")
    q.set_defaults(func=cmd_diff)

    q = sub.add_parser("status", help="四版状态")
    q.set_defaults(func=cmd_status)

    q = sub.add_parser("pack", help="测试包：只对一张图生效的路线数据（④ navdata\\test\\packs/）")
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
    q2 = ps.add_parser("diff", help="包 vs 开发版 / 部署版")
    q2.add_argument("name")
    q2.set_defaults(func=cmd_pack_diff)
    q2 = ps.add_parser("promote", help="包 -> 正式版 nav\\（先备份旧文件）")
    q2.add_argument("name")
    q2.add_argument("--dry", action="store_true")
    q2.set_defaults(func=cmd_pack_promote)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        return cmd_status(args)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
