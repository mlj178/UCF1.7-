#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 vis/ 里一堆历史扫描整理成「原始地图数据集」+ 只读还原点。

一句话：一张图只留一份、去掉我们自己的编辑、编号+中文名、再存一份永不改动的备份。

    python organize_maps.py                # 整理（不删任何东西）
    python organize_maps.py --archive      # 顺带把 vis/ 里处理过的历史 JSON 归档到 backup/
    python organize_maps.py --dry          # 只看会做什么

产出：
    ucf_mod/maps/NN_<中文名>.json         原始数据（游戏自己扫的，不含我们的编辑）
    ucf_mod/maps/_index.json / INDEX.md   11 张图的编号、中文名、是否已有数据
    ucf_mod/backup/maps_original_<日期>/  只读还原点（raw 原始导出 + canonical + MANIFEST）

为什么「原始」要挑节点最少的那份：
  游戏的 A* 点图是进图时现扫的，我们插件的编辑（nav/<指纹>.txt）是在扫描结果之上另加的。
  同一张图的多份导出里，节点最少的那份最早、最接近原图；本脚本按这个挑，并把
  「这份原图之上游戏还套着几条编辑」写进 _index.json。

中文名不是猜的：游戏 sharedassets0.assets 里的选图表是「模式名 / 场景名 / 中文名」三元组，
每个 levelN 场景文件里又能找到自己的场景名（TransportShip、Factory、Cebu_City、NY_TM、
Arena、GrimReaperKM、DesertFort、NanoResort、Nano_DawnVillage、DeathRing），两边一对即得。
level9 = Nano30_Storm（插件注入的隐藏图，游戏里显示「隐藏地图 暴风」）。
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import io
import json
import os
import re
import shutil
import sys
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)
from ucf_paths import DEPLOY as UCF, GEO, VIS, NAV, MAPS, BACKUP, NAMES_FILE, doc  # noqa: E402

TABLE_FILE = doc("地图对照表.md")
ROW_RE = re.compile(r"^\|\s*(\d{1,3})\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


def load_table(path=None):
    """从「地图对照表.md」读 [序号, 关卡, 中文名, 场景名, 备注]。读不到就返回 []。"""
    path = path or TABLE_FILE
    rows = []
    try:
        with io.open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = ROW_RE.match(line.strip())
                if not m:
                    continue
                name = m.group(3).strip()
                if not name:
                    continue
                rows.append((int(m.group(1)), m.group(2), name, m.group(4).strip(), m.group(5).strip()))
    except OSError:
        return []
    rows.sort()
    return rows


# 兜底表：地图对照表.md 缺失/损坏时才用（平时以那个 md 为准，见 load_levels）
_BUILTIN_LEVELS = [
    ("level1", "运输船", "TransportShip", ""),
    ("level2", "小型工厂", "Factory", ""),
    ("level3", "椰岛之巅", "Cebu_City", ""),
    ("level4", "胜利广场", "NY_TM", ""),
    ("level5", "竞技场", "Arena", ""),
    ("level6", "刀锋寨", "GrimReaperKM", ""),
    ("level7", "沙漠要塞", "DesertFort", ""),
    ("level8", "生化酒店", "NanoResort", ""),
    ("level9", "暴风", "Nano30_Storm", "隐藏地图（插件注入）"),
    ("level10", "新寂静村", "Nano_DawnVillage", ""),
    ("level11", "死亡擂台", "DeathRing", ""),
]


def load_levels():
    """优先用 mod 里的 地图对照表.md（手写、持久），没有再用内置兜底表。"""
    rows = load_table()
    if len(rows) >= 5:
        return [(lv, nm, sc or "", note) for (_no, lv, nm, sc, note) in rows]
    return list(_BUILTIN_LEVELS)


LEVELS = load_levels()
LEVEL_ORDER = {lv: i + 1 for i, (lv, *_r) in enumerate(LEVELS)}
NAME_OF = {lv: nm for lv, nm, *_r in LEVELS}
ASCII_OF = {lv: asc for lv, _nm, asc, *_r in LEVELS}
NOTE_OF = {lv: (r[0] if r else "") for lv, _nm, _asc, *r in LEVELS}
NO_OF = {lv: i + 1 for i, (lv, *_r) in enumerate(LEVELS)}
# 同一个场景可能以不同名字出现（隐藏图 Nano30_Storm 就是 level9）
ALIAS = {"nano30_storm": "level9", "nano30storm": "level9", "storm": "level9"}
MIN_NODES = 8          # 少于这个点数的导出当垃圾（n0 那种）
TRUST_NODES = 100      # 低于这个点数：多半是菜单/大厅场景采到的，只在索引里标「可疑」，不进数据集
SUSPECT_DIR = os.path.join(MAPS, "_suspect")   # 被移出 maps/ 的可疑整理文件放这（不删）
# 少数图本身路点就极少（椰岛之巅 Cebu_City 场景里只有 2 个 WayPoint 对象），
# 这些指纹即使低于 MIN_NODES 也要收，且直接指定关卡（几何匹配对小样本无效）。
KEEP_FP = {"n2-24a647eff15d6ca4": "level3"}


def norm_level(lv):
    lv = (lv or "").strip()
    return ALIAS.get(lv.lower(), lv)


def log(*a):
    print(*a)
    sys.stdout.flush()


def ensure_dirs():
    for d in (MAPS, BACKUP):
        os.makedirs(d, exist_ok=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path):
    with io.open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, obj, indent=1):
    tmp = path + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
        f.write("\n")
    os.replace(tmp, path)


def load_names():
    if os.path.isfile(NAMES_FILE):
        try:
            data = load_json(NAMES_FILE)
            if isinstance(data, dict):
                out = {}
                for k, v in data.items():
                    if isinstance(v, str):
                        out[k] = {"name": v, "level": ""}
                    elif isinstance(v, dict):
                        out[k] = {"name": str(v.get("name") or ""), "level": str(v.get("level") or "")}
                return out
        except Exception:
            pass
    return {}


def level_from_text(s):
    if not s:
        return ""
    m = re.match(r"^(level\d+)\b", s, re.I) or re.search(r"\b(level\d+)\b", s, re.I)
    return m.group(1).lower() if m else ""


def parse_ops(text):
    out = []
    for raw in (text or "").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        m = re.match(r"^node\s+(add|del)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)$", s)
        if m:
            out.append((m.group(1), [float(m.group(2)), float(m.group(3)), float(m.group(4))], None))
            continue
        m = re.match(r"^edge\s+(add|del)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s+"
                     r"(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)$", s)
        if m:
            out.append((m.group(1), [float(m.group(2)), float(m.group(3)), float(m.group(4))],
                        [float(m.group(5)), float(m.group(6)), float(m.group(7))]))
    return out


def count_txt(path):
    try:
        with io.open(path, "r", encoding="utf-8", errors="replace") as f:
            return len(parse_ops(f.read()))
    except OSError:
        return 0


def bbox_of(pts):
    if not pts:
        return [[0, 0, 0], [0, 0, 0]]
    lo = [min(p[i] for p in pts) for i in range(3)]
    hi = [max(p[i] for p in pts) for i in range(3)]
    return [[round(v, 2) for v in lo], [round(v, 2) for v in hi]]


def load_geo_points():
    """{level: 顶点数组}；没有 numpy 就返回 {}。"""
    try:
        import numpy as np
    except Exception:
        return {}
    out = {}
    if not os.path.isdir(GEO):
        return out
    for fn in sorted(os.listdir(GEO)):
        if not fn.endswith(".npz"):
            continue
        try:
            z = np.load(os.path.join(GEO, fn), allow_pickle=True)
            key = "p" if "p" in z.files else ("v" if "v" in z.files else None)
            if key is None:
                continue
            out[fn[:-4]] = np.asarray(z[key], dtype="float64")
        except Exception:
            continue
    return out


def guess_level_by_geometry(nodes, levels):
    """节点离哪个关卡的地形最近 -> 关卡。返回 (level, score) 或 (None, score)。"""
    if not nodes or not levels:
        return None, 0.0
    try:
        import numpy as np
    except Exception:
        return None, 0.0
    pts = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in nodes], dtype="float64")
    if len(pts) > 140:
        pts = pts[np.linspace(0, len(pts) - 1, 140).astype(int)]
    best, best_s, second = None, 0.0, 0.0
    for lv, P in levels.items():
        if len(P) == 0:
            continue
        hit = 0
        for i in range(0, len(pts), 8):
            chunk = pts[i:i + 8]
            d = ((chunk[:, None, :] - P[None, :, :]) ** 2).sum(axis=2)
            hit += int((d.min(axis=1) <= 6.25).sum())
        score = hit / float(len(pts))
        if score > best_s:
            second = best_s
            best_s, best = score, lv
        elif score > second:
            second = score
    if best_s >= 0.45 and (best_s - second) >= 0.03:
        return best, best_s
    if best_s >= 0.6:
        return best, best_s
    return None, best_s


def snapshot_info(path):
    try:
        doc = load_json(path)
    except Exception as exc:
        log("  !! 读不了 %s: %s" % (os.path.basename(path), exc))
        return None
    if (doc.get("format") or "") != "ucf-navgraph":
        return None
    pts = []
    for n in (doc.get("nodes") or []):
        if isinstance(n, dict) and isinstance(n.get("p"), list) and len(n["p"]) >= 3:
            pts.append(n["p"][:3])
        elif isinstance(n, list) and len(n) >= 3:
            pts.append(n[:3])
    mp = doc.get("map") or {}
    return {
        "path": path,
        "file": os.path.basename(path),
        "doc": doc,
        "nodes": len(doc.get("nodes") or []),
        "points": pts,
        "edges": len(doc.get("edges") or []),
        "features": len(doc.get("features") or []),
        "fp": str(mp.get("fingerprint") or ""),
        "mapName": str(mp.get("name") or ""),
        "generated": str(doc.get("generated") or ""),
        "source": str(mp.get("source") or ""),
        "size": os.path.getsize(path),
    }


def write_canonical(level, snap, names):
    idx = LEVEL_ORDER.get(level, 99)
    cn = NAME_OF.get(level) or names.get(snap["fp"], {}).get("name") or snap["mapName"] or "未知地图"
    fname = "%02d_%s.json" % (idx, cn)
    dst = os.path.join(MAPS, fname)
    doc = json.loads(json.dumps(snap["doc"]))
    mp = doc.setdefault("map", {})
    mp["fingerprint"] = snap["fp"]
    mp["node_count"] = snap["nodes"]
    mp["label"] = cn
    mp["level"] = level
    mp["scene"] = ASCII_OF.get(level, "")
    mp["origin"] = "mod-generated" if (snap.get("source") == "ours") else "game-scan"
    mp["generated_by"] = ("ucf_mod 自动铺点" if mp["origin"] == "mod-generated" else "游戏自己 Scan")
    mp["original"] = True
    mp["exported_from"] = snap["file"]
    mp["bbox"] = mp.get("bbox") or bbox_of(snap["points"])
    doc["plugin"] = doc.get("plugin") or "ucf_mod"
    doc.pop("edits", None)
    save_json(dst, doc)
    return dst, fname, cn


def build_index(rows, suspect=None, extras=None):
    suspect = suspect or {}
    extras = extras or []
    items = []
    for idx, (lv, cn, asc, note) in enumerate(LEVELS, 1):
        r = rows.get(lv) or {}
        items.append({
            "no": "%02d" % idx, "level": lv, "name": cn, "scene": asc, "note": note,
            "file": r.get("fname") or "", "fingerprint": r.get("fp") or "",
            "nodes": r.get("nodes") or 0, "edges": r.get("edges") or 0,
            "features": r.get("features") or 0, "source_file": r.get("src") or "",
            "exported": r.get("generated") or "", "edits_on_top": r.get("edits_on_top") or 0,
            "source": r.get("source") or "", "origin": r.get("origin") or "",
            "suspect": ({"file": (suspect.get(lv) or {}).get("file", ""),
                         "nodes": (suspect.get(lv) or {}).get("nodes", 0)}
                        if (lv in suspect) else None),
            "status": "有数据" if r.get("fname") else "待采集",
        })
    doc = {
        "format": "ucf-map-index", "version": 1,
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"), "ucf": UCF,
        "note": "原始数据 = 游戏自己扫描出来的点图，不含插件编辑；编辑数据在 ucf_mod/nav/<指纹>.txt",
        "maps": items,
        "extras": extras,
    }
    save_json(os.path.join(MAPS, "_index.json"), doc)
    md = ["# 原始地图数据集（自动生成，勿手改）", "",
          "生成时间：" + doc["generated"], "",
          "序号 / 关卡 / 中文名 / 场景名的**权威表**在 ../地图对照表.md（手写、持久）；",
          "本文件只是按那张表整理出来的结果，每次跑脚本都会重写。", "",
          "| 序号 | 关卡 | 中文名 | 场景名 | 节点 | 边 | 特征 | 文件 | 状态 | 备注 |",
          "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for it in items:
        note = it["note"]
        if it["source"] == "ours":
            note = (note + "；" if note else "") + "插件铺的点（游戏原图没有导航）"
        if it["file"] and 0 < it["nodes"] < 100:
            note = (note + "；" if note else "") + "样本很小，可能只扫到局部"
        if not note and it["edits_on_top"]:
            note = "游戏现在还会套 %d 条编辑" % it["edits_on_top"]
        if it.get("suspect") and not it["file"]:
            note = "现有导出只有 %d 点，疑似菜单/大厅数据（见 maps/_suspect/ 与 backup/review_*）" % it["suspect"]["nodes"]
        md.append("| %s | %s | **%s** | %s | %s | %s | %s | %s | %s | %s |" % (
            it["no"], it["level"], it["name"], it["scene"] or "-",
            it["nodes"] or "-", it["edges"] or "-", it["features"] or "-",
            it["file"] or "-", it["status"], note or ""))
    md += ["", "## 说明", "",
           "- **原始**：游戏进图时自己 Scan 出来的 A* 点图。同一张图有多份导出时取**节点最少**的那份，",
           "  因为插件编辑只会往原图上加点，最少的那份最接近原图。",
           "- 文件里的 map.fingerprint 就是游戏套编辑之前算的指纹，也是 nav/<指纹>.txt 用的那个。",
           "- edits_on_top：这份原图之上，游戏现在还套着几条编辑。",
           "- 想让游戏回到原图：删掉 ucf_mod/nav/<指纹>.txt，下次进图就是干净的原始点图。",
           "- 只读还原点：ucf_mod/backup/maps_original_<日期>/（含 sha256 清单）。",
           "- 已确认是菜单/大厅数据、不当地图用的导出在 ucf_mod/backup/review_20261116/（不进数据集）。",
           "- 序号/关卡/中文名/场景名以 ucf_mod/地图对照表.md 为准，本文件不定义名字。"]
    if extras:
        md += ["", "## maps/ 里的其它文件（不在对照表里，原样保留）", "",
               "| 文件 | 关卡 | 说明 | 节点 |", "| --- | --- | --- | --- |"]
        for e in extras:
            md.append("| %s | %s | %s | %s |" % (e["file"], e["level"] or "-", e["label"] or "-", e["nodes"]))
    with io.open(os.path.join(MAPS, "INDEX.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md) + "\n")
    return doc


def _find_raw_in_history(fp):
    """在 backup/vis_history_* 里按指纹找回最初的导出文件。"""
    if not fp:
        return ""
    for d in sorted(glob.glob(os.path.join(BACKUP, "vis_history_*")), reverse=True):
        try:
            names = sorted(os.listdir(d))
        except OSError:
            continue
        for fn in names:
            if not fn.lower().endswith(".json"):
                continue
            try:
                doc = load_json(os.path.join(d, fn))
            except Exception:
                continue
            if str((doc.get("map") or {}).get("fingerprint") or "") == fp:
                return os.path.join(d, fn)
    return ""


def _prev_raw_name(level):
    """从已有还原点的 MANIFEST 里查这张图原来导出的文件名。"""
    for prev in sorted(glob.glob(os.path.join(BACKUP, "maps_original_*")), reverse=True):
        man = os.path.join(prev, "MANIFEST.json")
        if not os.path.isfile(man):
            continue
        try:
            data = load_json(man)
        except Exception:
            continue
        for e in (data.get("maps") or []):
            if e.get("level") == level and (e.get("raw") or {}).get("file"):
                return e["raw"]["file"]
    return ""


def rebuild_backup(rows, dry=False):
    stamp = time.strftime("%Y%m%d")
    root = os.path.join(BACKUP, "maps_original_" + stamp)
    if os.path.isdir(root) and not dry:
        prev = 0
        try:
            with io.open(os.path.join(root, "MANIFEST.json"), "r", encoding="utf-8") as f:
                prev = len(json.load(f).get("maps") or [])
        except Exception:
            prev = 0
        if prev > len(rows):
            n = 2
            while os.path.isdir(os.path.join(BACKUP, "maps_original_%s_r%d" % (stamp, n))):
                n += 1
            root = os.path.join(BACKUP, "maps_original_%s_r%d" % (stamp, n))
            log("  同日旧备份有 %d 张图、这次只有 %d 张：写新目录 %s，旧的不动" % (prev, len(rows), root))
    if dry:
        log("[dry] 会重建备份目录 %s" % root)
        return root
    if os.path.isdir(root):
        for dirpath, _dirs, files in os.walk(root):
            for fn in files:
                try:
                    os.chmod(os.path.join(dirpath, fn), 0o666)
                except OSError:
                    pass
        shutil.rmtree(root)
    os.makedirs(os.path.join(root, "raw"), exist_ok=True)
    os.makedirs(os.path.join(root, "canonical"), exist_ok=True)
    entries = []
    for lv, r in sorted(rows.items(), key=lambda kv: LEVEL_ORDER.get(kv[0], 99)):
        src = r.get("path")
        if src and os.path.isfile(src) and os.path.abspath(os.path.dirname(src)) == os.path.abspath(MAPS):
            # 这次的源是 maps/ 里的整理结果（原始导出已归档）：先找旧还原点记录的 raw 文件名，
            # 再按指纹去历史归档里翻，最后才退回 maps/ 这份（保证还原点里的 raw 永远是"游戏导出的原件"）
            old_raw = _prev_raw_name(lv)
            if old_raw:
                for prev in sorted(glob.glob(os.path.join(BACKUP, "maps_original_*")), reverse=True):
                    cand = os.path.join(prev, "raw", old_raw)
                    if os.path.isfile(cand):
                        src = cand
                        break
            if r.get("fp"):
                found = _find_raw_in_history(r.get("fp"))
                if found:
                    src = found
        if (not src or not os.path.isfile(src)) and r.get("fp"):
            found = _find_raw_in_history(r.get("fp"))
            if found:
                src = found
        if not src or not os.path.isfile(src):
            # 原始导出已经被归档（不在 vis/ 了）：优先复用已有还原点里的 raw/，保证还原点不会越跑越少
            base_name = os.path.basename(r.get("src") or "")
            for prev in sorted(glob.glob(os.path.join(BACKUP, "maps_original_*")), reverse=True):
                cand = os.path.join(prev, "raw", base_name)
                if base_name and os.path.isfile(cand):
                    src = cand
                    break
        if not src or not os.path.isfile(src):
            log("  !! 备份跳过 %s（找不到原始导出）" % r.get("fname"))
            continue
        raw_dst = os.path.join(root, "raw", os.path.basename(src))
        shutil.copy2(src, raw_dst)
        canon_src = os.path.join(MAPS, r.get("fname") or "")
        canon_dst = ""
        if r.get("fname") and os.path.isfile(canon_src):
            canon_dst = os.path.join(root, "canonical", r["fname"])
            shutil.copy2(canon_src, canon_dst)
        entries.append({
            "level": lv, "name": NAME_OF.get(lv, ""), "scene": ASCII_OF.get(lv, ""),
            "fingerprint": r.get("fp", ""), "nodes": r.get("nodes", 0),
            "edges": r.get("edges", 0), "features": r.get("features", 0),
            "edits_on_top": r.get("edits_on_top", 0),
            "raw": {"file": os.path.basename(src), "bytes": os.path.getsize(raw_dst),
                    "sha256": sha256(raw_dst)},
            "canonical": ({"file": os.path.basename(canon_dst), "bytes": os.path.getsize(canon_dst),
                           "sha256": sha256(canon_dst)} if canon_dst else None),
        })
    manifest = {
        "format": "ucf-maps-backup", "version": 1,
        "created": time.strftime("%Y-%m-%d %H:%M:%S"), "ucf": UCF,
        "purpose": "只读还原点：游戏原始地图数据（未经插件编辑）。除非要还原，不要修改这里任何文件。",
        "tool": "tools/organize_maps.py", "maps": entries,
    }
    save_json(os.path.join(root, "MANIFEST.json"), manifest)
    readme = (
        "UCF 原始地图备份（只读还原点）\r\n"
        "生成：" + manifest["created"] + "\r\n\r\n"
        "这里放的是**游戏自己扫描出来的**原始导航数据，不含插件编辑。\r\n"
        "  raw/          游戏 Ctrl+E 导出的原始 JSON（原文件名，逐字节复制）\r\n"
        "  canonical/    整理后的编号版（和 ucf_mod/maps/ 里的一致）\r\n"
        "  MANIFEST.json 每个文件的 sha256、指纹、节点数、套用了几条编辑\r\n\r\n"
        "怎么用：\r\n"
        "  * 只是查看/对比：直接打开 canonical/ 里的 JSON。\r\n"
        "  * 还原某张图：把 canonical/ 里对应文件复制回 ucf_mod/maps/；\r\n"
        "    想让游戏也回到原始点图：删掉 ucf_mod/nav/<指纹>.txt。\r\n"
        "  * 校验没被动过：把文件算一遍 sha256，和 MANIFEST.json 里的对一下。\r\n\r\n"
        "注意：本目录文件是只读的。要改先去掉只读属性，或者复制一份出来再改。\r\n"
    )
    with io.open(os.path.join(root, "README.txt"), "w", encoding="utf-8", newline="") as f:
        f.write(readme)
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            try:
                os.chmod(os.path.join(dirpath, fn), 0o444)
            except OSError:
                pass
    return root


def archive_vis(files, dry=False):
    """把 vis/ 清空：传入的 JSON + 插件的 _seen_* 标记 + *.navmesh.bin + _noise 目录。"""
    stamp = time.strftime("%Y%m%d_%H%M%S")
    root = os.path.join(BACKUP, "vis_history_" + stamp)
    if dry:
        log("[dry] 会把这些文件归档到 %s" % root)
        for p in files:
            log("      ", os.path.basename(p))
        return root
    os.makedirs(root, exist_ok=True)
    extra = []
    if os.path.isdir(VIS):
        for fn in sorted(os.listdir(VIS)):
            p = os.path.join(VIS, fn)
            if os.path.isfile(p) and (fn.startswith("_seen_") or fn.endswith(".navmesh.bin")):
                extra.append(p)
    noise = os.path.join(VIS, "_noise")
    moved = 0
    only_vis = [p for p in (files + extra) if os.path.abspath(os.path.dirname(p)) == os.path.abspath(VIS)]
    for p in only_vis:
        dst = os.path.join(root, os.path.basename(p))
        try:
            os.replace(p, dst)
            moved += 1
        except OSError as exc:
            log("  !! 归档失败 %s: %s" % (os.path.basename(p), exc))
    if os.path.isdir(noise):
        try:
            shutil.move(noise, os.path.join(root, "_noise"))
        except OSError:
            pass
    with io.open(os.path.join(root, "README.txt"), "w", encoding="utf-8", newline="") as f:
        f.write("vis/ 历史导出归档（%s）\r\n\r\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
        f.write("这里存的是 vis/ 里原来的全部东西（逐字节复制/移动），共 %d 个文件：\r\n" % moved)
        f.write("  *.json          历次 Ctrl+E 导出的扫描结果\r\n")
        f.write("  *.navmesh.bin   A* NavMeshGraph 导出（真正的人机可走面）\r\n")
        f.write("  _seen_<指纹>    插件「同一指纹只导一次」的标记\r\n")
        f.write("  _noise/         扫描时被判定为噪声的点\r\n\r\n")
        f.write("整理后的原始数据集在 ucf_mod/maps/；只读还原点在 ucf_mod/backup/maps_original_*/。\r\n")
    return root


def main():
    ap = argparse.ArgumentParser(description="整理原始地图数据集 + 只读备份")
    ap.add_argument("--archive", action="store_true", help="把 vis/ 里的历史导出搬进 backup/（默认不动）")
    ap.add_argument("--dry", action="store_true", help="只显示会做什么")
    ap.add_argument("--no-backup", action="store_true", help="不重建备份")
    ap.add_argument("--no-geo", action="store_true", help="不按地形判关卡")
    ap.add_argument("--show-table", action="store_true", help="打印读到的地图对照表（md 为准）然后退出")
    args = ap.parse_args()
    if args.show_table:
        rows = load_table()
        srcs = "地图对照表.md" if rows else "内置兜底表（地图对照表.md 没读到）"
        log("来源：" + srcs + "（" + TABLE_FILE + "）")
        log("%-6s %-8s %-10s %-18s %s" % ("序号", "关卡", "中文名", "场景名", "备注"))
        for (no, lv, nm, sc, note) in (rows or [(i + 1, lv, nm, sc, note) for i, (lv, nm, sc, note) in enumerate(LEVELS)]):
            log("%-6s %-8s %-10s %-18s %s" % ("%02d" % no, lv, nm, sc or "-", note))
        return 0
    ensure_dirs()
    names = load_names()

    files = []
    for folder in (VIS, MAPS):
        if not os.path.isdir(folder):
            continue
        for fn in sorted(os.listdir(folder)):
            if fn.lower().endswith(".json") and fn not in ("names.json", "_index.json"):
                files.append(os.path.join(folder, fn))
    if not files:
        log("vis/ 里没有 JSON。先在游戏里 Ctrl+E 导出（或开 Ctrl+Shift+X 采集模式，进每张图自动导出）。")
        return 0

    snaps = []
    for p in files:
        info = snapshot_info(p)
        if not info:
            log("跳过（不是 ucf-navgraph / 老格式）：%s" % os.path.basename(p))
            continue
        info["from_maps"] = (os.path.dirname(p) == MAPS)
        snaps.append(info)
    n_fresh = sum(1 for s in snaps if not s["from_maps"])
    log("可用导出：%d 份（vis/ 新导出 %d + maps/ 已有 %d）" % (len(snaps), n_fresh, len(snaps) - n_fresh))
    if not snaps:
        return 1

    geo_pts = {} if args.no_geo else load_geo_points()
    for s in snaps:
        lv = str((s["doc"].get("map") or {}).get("level") or "") if s["from_maps"] else ""
        if not lv:
            for k in (s["fp"], s["mapName"]):
                if k and names.get(k, {}).get("level"):
                    lv = names[k]["level"]
                    break
        if not lv:
            lv = level_from_text(s["mapName"]) or level_from_text(s["file"])
        if not lv and s["fp"] in KEEP_FP:
            lv = KEEP_FP[s["fp"]]
        if not lv and geo_pts and s["nodes"] >= 20:
            g, score = guess_level_by_geometry(s["points"], geo_pts)
            if g:
                lv = g
                log("  地形匹配：%s -> %s（命中 %.0f%%）" % (s["file"], g, score * 100))
        s["level"] = norm_level(lv) if lv else ""

    unknown = [s for s in snaps if not s["level"]]
    if unknown:
        log("认不出关卡的（先跳过；在编辑器里存名后再跑一次即可）：")
        for s in unknown[:8]:
            log("   ", s["file"], "fp=" + (s["fp"] or "-"), "nodes=%d" % s["nodes"])

    best = {}
    for s in snaps:
        if not s["level"]:
            continue
        if s["nodes"] < MIN_NODES and s["fp"] not in KEEP_FP:
            log("  跳过样本太小：%s（%d 点）" % (s["file"], s["nodes"]))
            continue
        cur = best.get(s["level"])
        if cur is None or (s["nodes"], s["generated"]) < (cur["nodes"], cur["generated"]):
            best[s["level"]] = s
    for lv in sorted(best, key=lambda x: LEVEL_ORDER.get(x, 99)):
        s = best[lv]
        sibs = [x for x in snaps if x["level"] == lv and (x["nodes"] >= MIN_NODES or x["fp"] in KEEP_FP)]
        s["edits_on_top"] = count_txt(os.path.join(NAV, (s["fp"] or "x") + ".txt"))
        log("  %-8s %-8s 原始=%d 点 / %d 边（同图 %d 份导出，最多 %d 点）%s" % (
            lv, NAME_OF.get(lv, "?"), s["nodes"], s["edges"], len(sibs),
            max(x["nodes"] for x in sibs),
            ("，之上套着 %d 条编辑" % s["edits_on_top"]) if s["edits_on_top"] else ""))

    rows = {}
    for lv in sorted(best, key=lambda x: LEVEL_ORDER.get(x, 99)):
        s = best[lv]
        if args.dry:
            log("[dry] 会写 maps/%02d_%s.json  <- %s" % (LEVEL_ORDER.get(lv, 99), NAME_OF.get(lv, "?"), s["file"]))
            rows[lv] = {"fname": "%02d_%s.json" % (LEVEL_ORDER.get(lv, 99), NAME_OF.get(lv, "?")),
                        "fp": s["fp"], "nodes": s["nodes"], "edges": s["edges"],
                        "features": s["features"], "src": s["file"],
                        "generated": s["generated"], "edits_on_top": s.get("edits_on_top", 0),
                        "source": s["source"], "path": s["path"]}
            continue
        dst, fname, cn = write_canonical(lv, s, names)
        rows[lv] = {"fname": fname, "cn": cn, "fp": s["fp"], "nodes": s["nodes"],
                    "edges": s["edges"], "features": s["features"], "src": s["file"],
                    "generated": s["generated"], "edits_on_top": s.get("edits_on_top", 0),
                    "source": s["source"], "path": s["path"]}
        log("  写出 maps/%s（%d 点 / %d 边，指纹 %s）" % (fname, s["nodes"], s["edges"], s["fp"] or "-"))

    if not args.dry:
        moved = []
        if os.path.isdir(MAPS):
            for fn in sorted(os.listdir(MAPS)):
                p = os.path.join(MAPS, fn)
                if not os.path.isfile(p) or not fn.lower().endswith(".json") or fn.startswith("_"):
                    continue
                info = snapshot_info(p) or {}
                lv = str((info.get("doc", {}).get("map") or {}).get("level") or "")
                # 只处理「对照表里的关卡但这次没收」的旧文件；practice 这类自定义关卡原样保留
                if lv not in LEVEL_ORDER or lv in rows:
                    continue
                os.makedirs(SUSPECT_DIR, exist_ok=True)
                try:
                    shutil.move(p, os.path.join(SUSPECT_DIR, fn))
                    moved.append(fn)
                except OSError:
                    pass
        if moved:
            log("  移到 maps/_suspect/（低于可信线或不再采用，没删）：%s" % ", ".join(moved))
        extras = []
        if os.path.isdir(MAPS):
            for fn in sorted(os.listdir(MAPS)):
                p = os.path.join(MAPS, fn)
                if not os.path.isfile(p) or not fn.lower().endswith(".json") or fn.startswith("_"):
                    continue
                info = snapshot_info(p) or {}
                lv = str((info.get("doc", {}).get("map") or {}).get("level") or "")
                if lv not in LEVEL_ORDER:
                    extras.append({"file": fn, "level": lv,
                                   "label": str((info.get("doc", {}).get("map") or {}).get("label") or ""),
                                   "nodes": info.get("nodes", 0)})
        suspect = {}
        for s in snaps:
            lv = s.get("level") or ""
            if not lv or lv in rows or s["nodes"] < MIN_NODES or s["nodes"] >= TRUST_NODES:
                continue
            cur = suspect.get(lv)
            if cur is None or s["nodes"] > cur["nodes"]:
                suspect[lv] = s
        build_index(rows, suspect, extras)
        log("  索引：maps/_index.json + maps/INDEX.md")
        if not args.no_backup:
            root = rebuild_backup(rows)
            log("  只读备份：%s（%d 张图）" % (root, len(rows)))
        changed = False
        for lv, cn, asc, _note in LEVELS:
            want = {"name": cn, "level": lv}
            if names.get(lv) != want:
                names[lv] = want
                changed = True
            if asc and names.get(asc) != want:
                names[asc] = want
                changed = True
        for lv, r in rows.items():
            want = {"name": NAME_OF.get(lv, ""), "level": lv}
            if r["fp"] and names.get(r["fp"]) != want:
                names[r["fp"]] = want
                changed = True
        if changed:
            save_json(NAMES_FILE, dict(sorted(names.items())), indent=2)
            log("  nav/names.json 已更新（%d 条）" % len(names))

    if args.archive:
        vis_only = [p for p in files if os.path.dirname(p) == VIS]
        root = archive_vis(vis_only, args.dry)
        log("  历史导出归档：%s（%d 个文件）" % (root, len(vis_only)))

    missing = [lv for lv, *_ in LEVELS if lv not in rows]
    if missing:
        log("")
        log("还没有原始数据的关卡：" + "、".join("%s %s" % (lv, NAME_OF.get(lv, "")) for lv in missing))
        log("  采集办法：游戏里按 Ctrl+Shift+X 开采集模式（进图自动导出、不改任何东西），")
        log("  把缺的图各进一次，回来再跑一遍本脚本。")
    log("")
    log("完成。原始数据集：ucf_mod/maps/    还原点：ucf_mod/backup/maps_original_*/")
    return 0


if __name__ == "__main__":
    sys.exit(main())