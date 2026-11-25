#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""地图总览的数据层：把 11 张图的备份① / 草稿 / 成品 / 游戏加载状态算成一份只读快照。

这里不写任何文件，也不启动子进程：
  * ① 备份 = navdata\native\<图>\map.json（没有 map.json 的图只有可走面）+ 发布快照份数
  * 编辑中 = navdata\dev\packs\<图>\ 下唯一草稿
  * 成品   = navdata\dev\final\<指纹>.txt（平铺，一张图一份）
  * 游戏   = 当前启动档（成品 / 编辑中）下，这张图实际会被加载哪一份

界面层（tabs/overview.py）只负责把本模块返回的 rows 画成矩阵 / 卡片 / 看板。
"""
import hashlib
import json
import os
import re
import time

from ui.env import DEV, NATIVE, PACKS, ND, P, map_folder_name, map_table_rows

NAV_FP_RE = re.compile(r"^n\d+-[0-9a-f]{16}\.txt$", re.I)

MODE_LABEL = {
    "grow": "空白地图",
    "keep": "原版 + 新增",
    "delta": "增量",
}

STATUS_LABEL = {
    "drafting": "编辑中",
    "sync": "已同步",
    "publish": "待发布",
    "finalonly": "只有成品",
    "idle": "未开始",
    "nograph": "无点图",
}


def _read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def _sha256(path):
    h = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    except OSError:
        return ""
    return h.hexdigest()


def _fmt_time(value):
    if not value:
        return ""
    if isinstance(value, (int, float)):
        try:
            return time.strftime("%Y-%m-%d %H:%M", time.localtime(value))
        except (OSError, ValueError, OverflowError):
            return ""
    return str(value)[:16]


def _mtime(path):
    try:
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(path)))
    except OSError:
        return ""


def _size(path):
    try:
        return os.path.getsize(path)
    except OSError:
        return 0


def parse_nav(path, base_nodes=0, base_edges=0):
    r"""读一个路线 txt：返回点数/边数/改动数/mode/sha256/时间。

    grow（空白地图）以 0 为底；keep / 增量以原生底图为底。
    node add 是新建，node del 是删除；边同理。点数夹在 0 以上，不返回负数。
    文件不存在返回 None。
    """
    if not path or not os.path.isfile(path):
        return None
    grow = keep = False
    nadd = ndel = eadd = edel = 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                if s in ("grow", "blank"):
                    grow = True
                elif s == "keep":
                    keep = True
                elif s.startswith("node add "):
                    nadd += 1
                elif s.startswith("node del "):
                    ndel += 1
                elif s.startswith("edge "):
                    bits = s.split()
                    verb = bits[1] if len(bits) > 1 else ""
                    if verb in ("add", "out", "in"):
                        eadd += 1
                    elif verb in ("del", "delout", "delin"):
                        edel += 1
    except OSError:
        return None
    base_n = 0 if grow else max(0, int(base_nodes or 0))
    base_e = 0 if grow else max(0, int(base_edges or 0))
    mode = "grow" if grow else ("keep" if keep else "delta")
    return {
        "path": path,
        "file": os.path.basename(path),
        "nodes": max(0, base_n + nadd - ndel),
        "edges": max(0, base_e + eadd - edel),
        "nadd": nadd, "ndel": ndel, "eadd": eadd, "edel": edel,
        "changes": nadd + ndel + eadd + edel,
        "mode": mode,
        "mode_label": MODE_LABEL[mode],
        "grow": grow,
        "keep": keep,
        "sha256": _sha256(path),
        "mtime": _mtime(path),
        "at": _mtime(path),
        "bytes": _size(path),
    }


def status_for(has_map, draft, final):
    r"""状态只看有没有点图和草稿/成品是否同一份文件，不看日期。"""
    if not has_map:
        return "nograph"
    if draft and final:
        if draft.get("sha256") and draft.get("sha256") == final.get("sha256"):
            return "sync"
        if not draft.get("changes"):
            return "drafting"
        return "publish"
    if draft:
        return "publish" if draft.get("changes") else "drafting"
    if final:
        return "finalonly"
    return "idle"


def _native_info(folder, level):
    r"""原生底图：map.json 的指纹与点数/边数；没有 map.json 的图只有 navmesh。"""
    doc = {}
    path = ""
    for root in (NATIVE, DEV):
        p = os.path.join(root, folder, "map.json")
        doc = _read_json(p)
        if doc:
            path = p
            break
    navmesh = ""
    for root in (NATIVE, DEV):
        p = os.path.join(root, folder, P.NAVMESH)
        if os.path.isfile(p):
            navmesh = p
            break
    if not doc:
        return {
            "has_map": False, "path": "", "fp": "", "nodes": 0, "edges": 0,
            "navmesh": navmesh, "navmesh_name": _navmesh_name(level), "at": "",
        }
    m = doc.get("map") or {}
    counts = doc.get("counts") or {}
    fp = str(m.get("fingerprint") or "")
    if not fp and str(m.get("level") or level) == "level9":
        fp = "n0-0000000000000000"
    nodes = counts.get("nodes")
    edges = counts.get("edges")
    if nodes is None:
        nodes = m.get("node_count") or len(doc.get("nodes") or [])
    if edges is None:
        edges = m.get("edge_count") or len(doc.get("edges") or [])
    return {
        "has_map": True,
        "path": path,
        "fp": fp,
        "nodes": int(nodes or 0),
        "edges": int(edges or 0),
        "navmesh": navmesh,
        "navmesh_name": _navmesh_name(level),
        "at": _mtime(path),
    }


def _navmesh_name(level):
    verts = getattr(P, "NATIVE_VERTS", {}) or {}
    try:
        n = verts.get(str(level or ""))
    except AttributeError:
        n = None
    return ("nm%d" % n) if n else P.NAVMESH


def _draft_info(folder, fp, native):
    r"""一张图唯一草稿：manifest.json + <指纹>.txt；没有 txt 当作没有草稿。"""
    pdir = os.path.join(PACKS, folder)
    if not os.path.isdir(pdir):
        return None
    man = _read_json(os.path.join(pdir, "manifest.json"))
    use_fp = str(fp or man.get("fp") or "")
    path = os.path.join(pdir, use_fp + ".txt") if use_fp else ""
    if not os.path.isfile(path):
        try:
            names = [fn for fn in os.listdir(pdir) if NAV_FP_RE.match(fn)]
        except OSError:
            names = []
        if len(names) == 1:
            path = os.path.join(pdir, names[0])
            use_fp = names[0][:-4]
        else:
            path = ""
    info = parse_nav(path, native.get("nodes", 0), native.get("edges", 0))
    if not info:
        return None
    info.update({
        "folder": folder,
        "dir": pdir,
        "fp": use_fp,
        "name": str(man.get("name") or ""),
        "created": _fmt_time(man.get("created")),
        "updated": _fmt_time(man.get("updated")) or info["mtime"],
        "source": str(man.get("source") or ""),
        "manifest": man,
    })
    info["at"] = info["updated"] or info["mtime"]
    if man.get("grow") and not info["grow"]:
        info["grow"] = True
        info["mode"] = "grow"
        info["mode_label"] = MODE_LABEL["grow"]
    elif man.get("keep") and not info["keep"]:
        info["keep"] = True
        info["mode"] = "keep"
        info["mode_label"] = MODE_LABEL["keep"]
    return info


def _final_info(meta, native):
    if not meta or not meta.get("path"):
        return None
    info = parse_nav(meta["path"], native.get("nodes", 0), native.get("edges", 0))
    if not info:
        return None
    info.update({
        "fp": meta.get("fp") or "",
        "published": _fmt_time(meta.get("published") or meta.get("mtime") or info["mtime"]),
        "from": str(meta.get("from") or ""),
        "manifest": meta,
    })
    info["at"] = info["published"]
    return info


def snapshots_of(fp):
    r"""发布前快照：archive\final_prev\<指纹>\*.txt，最多 5 份；返回新到旧。"""
    if not fp:
        return []
    d = os.path.join(ND.FINAL_PREV, fp)
    out = []
    try:
        names = os.listdir(d)
    except OSError:
        return out
    for fn in names:
        if not fn.lower().endswith(".txt"):
            continue
        p = os.path.join(d, fn)
        try:
            mt = os.path.getmtime(p)
        except OSError:
            continue
        out.append({"path": p, "name": fn, "at": _mtime(p), "_m": mt})
    out.sort(key=lambda x: x["_m"], reverse=True)
    for item in out:
        item.pop("_m", None)
    return out


def deployment_status():
    r"""全局部署状态：游戏目录必须有的文件（加载器 + 启用的本体补丁）是否齐全。

    插件本体/配置/数据不写游戏目录（直读模式），所以这里只算加载器和 gamepatch；
    总览这一列讲的是「游戏里会加载哪份地图数据」，全局状态单独放顶部卡片。
    """
    game = os.path.abspath(P.game_dir_of())
    exe = os.path.join(game, "UnityCrossFire.exe")
    base = {"game": game, "ok": 0, "total": 0, "missing": 0, "bad": 0,
            "state": "none", "text": "未配置", "sub": "没有找到 UnityCrossFire.exe"}
    if not os.path.isfile(exe):
        return base
    try:
        import deploy_mod as D
        summary = D.plan_summary(game)
        total = summary["total"] - summary["disabled"]
        ok = summary["ok"]
        ready = summary["ready"]
        missing = summary["missing"]
        bad = summary["conflict"]
    except Exception as exc:                 # noqa: BLE001
        base.update({"state": "bad", "text": "检查失败",
                     "sub": str(exc)[:100] or "payload 读不了"})
        return base
    if total and ok == total:
        state, text = "ok", "已部署"
    elif ok == 0 and ready + missing == total:
        state, text = "none", "未部署"
    elif bad:
        state, text = "bad", "有冲突"
    elif missing:
        state, text = "warn", "部分缺失"
    else:
        state, text = "warn", "待部署"
    sub = "%d/%d 个必须文件一致" % (ok, total)
    if ready:
        sub += " · %d 个待部署" % ready
    if bad:
        sub += " · %d 个冲突" % bad
    if missing:
        sub += " · %d 个缺失" % missing
    return {"game": game, "ok": ok, "total": total, "missing": missing,
            "bad": bad, "state": state, "text": text, "sub": sub}


def _game_load(row, start_mode, current_level):
    r"""按当前启动档，这张图实际会加载哪一份。"""
    status = row["status"]
    if status == "nograph":
        return {"label": "可走面", "state": "nograph", "sub": "没有 PointGraph"}
    has_final = bool(row.get("final"))
    has_draft = bool(row.get("draft"))
    if start_mode == "edit" and row["level"] == current_level:
        if has_draft:
            return {"label": "编辑中", "state": "edit", "sub": "当前启动档"}
        return {"label": "原生", "state": "native", "sub": "这张图没有草稿"}
    if start_mode == "final":
        if has_final:
            if has_draft and row["draft"].get("sha256") != row["final"].get("sha256"):
                return {"label": "成品（旧）", "state": "warn", "sub": "草稿更新，未发布"}
            return {"label": "成品", "state": "ok", "sub": "启动成品时加载"}
        return {"label": "原生", "state": "native",
                "sub": "草稿未发布，游戏没有" if has_draft else "没有成品"}
    return {"label": "原生", "state": "native",
            "sub": "切成品档才用成品" if has_final else "编辑中档不加载"}


def collect_overview(start_mode="final", current_level=""):
    r"""返回 {rows, counts, deployment, ...}；所有路径都是本机现算，不写盘。"""
    try:
        final_meta = ND.final_store_meta()
    except Exception:                       # noqa: BLE001
        final_meta = {}
    rows = []
    for no, level, label, scene in map_table_rows():
        folder = map_folder_name(level, scene, label)
        native = _native_info(folder, level)
        fp = native.get("fp") or ""
        draft = _draft_info(folder, fp, native)
        fmeta = final_meta.get(fp) if fp else None
        final = _final_info(fmeta, native)
        snaps = snapshots_of(fp)
        row = {
            "no": int(no),
            "level": level,
            "label": label,
            "scene": scene,
            "folder": folder,
            "native": native,
            "draft": draft,
            "final": final,
            "snapshots": snaps,
            "status": "nograph",
        }
        row["status"] = status_for(native.get("has_map"), draft, final)
        row["game"] = _game_load(row, start_mode, current_level)
        rows.append(row)
    counts = {k: 0 for k in STATUS_LABEL}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    finals = [r["final"] for r in rows if r.get("final")]
    latest = max((f.get("published") or "" for f in finals), default="")
    current = next((r for r in rows if r["level"] == current_level), None)
    return {
        "rows": rows,
        "counts": counts,
        "deployment": deployment_status(),
        "draft_count": sum(1 for r in rows if r.get("draft")),
        "final_count": len(finals),
        "snapshot_count": sum(len(r.get("snapshots") or []) for r in rows),
        "latest_publish": latest,
        "start_mode": start_mode,
        "current_level": current_level,
        "current_label": (current or {}).get("label", ""),
        "current_no": (current or {}).get("no", 0),
    }
