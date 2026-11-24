#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""把 ① 备份 / ② 开发 从「maps\ nav\ vis\ 三块平铺」改成「一张图一个文件夹」。

    python tools/_oneoff/migrate_map_folders.py            # 默认 dry-run：只打印会搬什么
    python tools/_oneoff/migrate_map_folders.py --apply    # 真搬：每个文件搬前搬后算 sha256，逐个比对
    python tools/_oneoff/migrate_map_folders.py --undo     # 按上一次的日志原路退回

搬成什么样（和 ② packs 同一套名字，出处 docs/guide/地图对照表.md）：

    <数据根>\01_TransportShip运输船\map.json           <- maps\01_运输船.json
    <数据根>\02_Factory小型工厂\navmesh.bin            <- vis\navmesh_nm840-<指纹>.bin
    <数据根>\00_公共\names.json / _index.json / ...    <- nav\names.json / maps\_index.json ...
    ② 另收：vis\raw\<地图>\*.json -> <图>\导出\*.json

packs\ final\ archive\ 一概不碰（它们本来就是 图\包、一版一整套、历史归档）。
迁完再跑 python navdata.py verify / diff 复核。
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import stat
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "app", "core"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import ucf_paths as P  # noqa: E402
import map_table  # noqa: E402

NAVDATA = os.path.join(P.PROJ, "navdata")
META_NAMES = ("SHA256SUMS.txt", "README.md", ".frozen.json")
DOC_EXTS = (".json",)


# ---------------------------------------------------------------- 小工具
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(p, obj, indent=1):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with io.open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
        f.write("\n")
    os.replace(tmp, p)


def writable(p):
    try:
        os.chmod(p, os.stat(p).st_mode | stat.S_IWRITE)
    except OSError:
        pass


def readonly(p):
    try:
        os.chmod(p, os.stat(p).st_mode & ~stat.S_IWRITE)
    except OSError:
        pass


def rel(root, p):
    return os.path.relpath(p, root).replace(os.sep, "/")


def level_of_json(p):
    try:
        m = (load_json(p) or {}).get("map") or {}
    except (OSError, ValueError):
        return ""
    return str(m.get("level") or "")


def bin_level(fn):
    r"""navmesh_nm840-<指纹>.bin -> level2（按原生 A* 顶点数对号）。"""
    import re
    m = re.search(r"nm(\d+)-", fn)
    if not m:
        return ""
    return {v: k for k, v in P.NATIVE_VERTS.items()}.get(int(m.group(1)), "")


def fp_level_map(root):
    r"""指纹 -> 关卡：优先读这一版的 _index.json，其次扫地图 JSON。"""
    out = {}
    idx = P.index_path(root)
    if os.path.isfile(idx):
        try:
            for row in (load_json(idx).get("maps") or []):
                fp = str(row.get("fingerprint") or "")
                if fp and row.get("level"):
                    out[fp] = row["level"]
        except (OSError, ValueError):
            pass
    for _rel, p in P.map_files(root):
        try:
            m = (load_json(p) or {}).get("map") or {}
        except (OSError, ValueError):
            continue
        fp, lv = str(m.get("fingerprint") or ""), str(m.get("level") or "")
        if fp and lv:
            out.setdefault(fp, lv)
    return out


# ---------------------------------------------------------------- 计划
def plan_root(name, root):
    r"""[(src, dst, kind, note)] —— kind: map / bin / meta / export / companion。"""
    ops = []
    if not os.path.isdir(root):
        return ops
    if P.is_folders(root) and os.path.isdir(os.path.join(root, P.COMMON)):
        return ops                      # 已经迁过了

    # 1) 地图 JSON -> <图>\map.json
    legacy = os.path.join(root, "maps")
    if os.path.isdir(legacy):
        for fn in sorted(os.listdir(legacy)):
            if not fn.lower().endswith(".json") or fn in ("_index.json", "names.json"):
                continue
            src = os.path.join(legacy, fn)
            if not os.path.isfile(src):
                continue
            lv = level_of_json(src)
            folder = P.map_folder(lv) if lv else os.path.splitext(fn)[0]
            ops.append((src, os.path.join(root, folder, P.MAP_JSON), "map", fn))

    # 2) 可走面 -> <图>\navmesh.bin
    for base in bins_dirs(name, root):
        for fn in sorted(os.listdir(base)):
            if not (fn.startswith("navmesh") and fn.lower().endswith(".bin")):
                continue
            src = os.path.join(base, fn)
            if not os.path.isfile(src):
                continue
            lv = bin_level(fn)
            if not lv:
                continue
            ops.append((src, os.path.join(root, P.map_folder(lv), P.NAVMESH), "bin", fn))

    # 3) 公共文件 / 清单 -> 00_公共\
    pairs = [
        (os.path.join(root, "nav", "names.json"), "names.json"),
        (os.path.join(root, "nav", "nogen.txt"), "nogen.txt"),
        (os.path.join(root, "maps", "_index.json"), "_index.json"),
        (os.path.join(root, "maps", "INDEX.md"), "INDEX.md"),
    ]
    if name == "native":
        for fn in META_NAMES:
            pairs.append((os.path.join(root, fn), fn))
    for src, fn in pairs:
        if os.path.isfile(src):
            ops.append((src, os.path.join(root, P.COMMON, fn), "meta", fn))
    sus = os.path.join(root, "maps", "_suspect")
    if os.path.isdir(sus):
        ops.append((sus, os.path.join(root, P.COMMON, "_suspect"), "meta", "_suspect"))

    # 4) 开发版收件箱：认得出的导出 -> <图>\导出\
    if name == "dev":
        fplv = fp_level_map(root)
        vis = os.path.join(root, "vis")
        for base, dirs, files in os.walk(vis):
            dirs[:] = [d for d in dirs if d not in ("_state", "_noise", "navmesh")]
            for fn in sorted(files):
                if not fn.lower().endswith(".json") or fn in ("names.json", "_index.json"):
                    continue
                src = os.path.join(base, fn)
                try:
                    fp = str(((load_json(src) or {}).get("map") or {}).get("fingerprint") or "")
                except (OSError, ValueError):
                    continue
                lv = fplv.get(fp)
                if not lv:
                    continue                 # 认不出：留在收件箱，不删
                dst = os.path.join(root, P.map_folder(lv), "导出", fn)
                ops.append((src, dst, "export", fn))
                comp = os.path.splitext(src)[0] + ".navmesh.bin"
                if os.path.isfile(comp):
                    ops.append((comp, os.path.splitext(dst)[0] + ".navmesh.bin", "companion", fn))
    # 同一个目标只留第一条
    seen, out = set(), []
    for op in ops:
        key = os.path.normcase(os.path.abspath(op[1]))
        if key in seen:
            continue
        seen.add(key)
        out.append(op)
    return out


def bins_dirs(name, root):
    r"""可走面原来放哪：① vis\，② vis\navmesh\。"""
    if name == "dev":
        cands = [os.path.join(root, "vis", "navmesh")]
    else:
        cands = [os.path.join(root, "vis")]
    return [d for d in cands if os.path.isdir(d)]


# ---------------------------------------------------------------- 元数据
def rewrite_native_frozen(frozen_path, root, moved):
    frozen = load_json(frozen_path)
    origin = dict(frozen.get("navmesh_origin") or {})
    bins = []
    for src, dst, kind, note in moved:
        if kind == "bin":
            r = rel(root, dst)
            bins.append(r)
            origin[r] = note
    for m in (frozen.get("maps") or []):
        lv = str(m.get("level") or "")
        if lv:
            m["file"] = P.map_folder(lv) + "/map.json"
            cn, _sc = map_table.row_of(lv)      # 中文名以对照表为准（暴风 -> 飓风危城）
            if cn:
                m["cn"] = cn
    frozen["navmesh_bins"] = sorted(set(bins))
    frozen["navmesh_origin"] = origin
    frozen["layout"] = "mapfolders"
    frozen["migrated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    save_json(frozen_path, frozen)
    return frozen


def regen_sums(root):
    rows = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith("_") or d == "_suspect"]
        for fn in files:
            p = os.path.join(base, fn)
            r = rel(root, p)
            # 清单本身不算数据（和 freeze 的口径一致：三个清单写在 sums 之后）
            if os.path.dirname(r) in ("", P.COMMON) and os.path.basename(r) in META_NAMES:
                continue
            if r.startswith(P.COMMON + "/_suspect/"):
                continue
            rows.append((r, sha(p)))
    rows.sort()
    sums = ["%s  %s" % (h, r) for r, h in rows]
    dst = os.path.join(root, P.COMMON, "SHA256SUMS.txt")
    with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sums) + "\n")
    return sums


def rewrite_dev_index(root):
    path = P.index_path(root)
    if not os.path.isfile(path):
        return None
    doc = load_json(path)
    for row in (doc.get("maps") or []):
        lv = str(row.get("level") or "")
        if not lv:
            continue
        folder = P.map_folder(lv)
        row["file"] = folder + "/map.json" if os.path.isfile(
            os.path.join(root, folder, P.MAP_JSON)) else ""
        row["status"] = "有数据" if row["file"] else "待采集"
        if os.path.isfile(os.path.join(root, folder, P.NAVMESH)):
            row["navmesh"] = {"file": P.NAVMESH}
    doc["layout"] = "mapfolders"
    doc["ucf"] = root
    save_json(path, doc)
    return doc


def rewrite_index_md(root, old_new):
    r"""INDEX.md 里把旧文件名换成 "<图>/map.json"。"""
    path = os.path.join(P.common_dir(root), "INDEX.md")
    if not os.path.isfile(path):
        return
    with io.open(path, "r", encoding="utf-8") as f:
        text = f.read()
    for old, new in old_new.items():
        text = text.replace("| %s |" % old, "| %s |" % new)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def rewrite_native_readme(root, frozen, sums):
    path = os.path.join(root, P.COMMON, "README.md")
    try:
        import navdata                              # noqa: WPS433  只为了复用同一个 README 生成器
        text = navdata.native_readme(frozen, sums)
    except Exception:                               # noqa: BLE001
        return
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ---------------------------------------------------------------- 迁移 / 回滚
def run(args):
    stamp = time.strftime("%Y%m%d_%H%M%S")
    log = {"created": stamp, "apply": bool(args.apply), "undo": bool(args.undo),
           "roots": {}, "meta_backup": ""}

    if args.undo:
        return undo()

    plans = {"native": plan_root("native", P.NATIVE), "dev": plan_root("dev", P.DEV)}
    total = sum(len(v) for v in plans.values())
    for name, ops in plans.items():
        root = P.NATIVE if name == "native" else P.DEV
        print("== %s  %s  （%d 项）" % ("① 备份" if name == "native" else "② 开发", root, len(ops)))
        for src, dst, kind, note in ops:
            print("   %-6s %-46s -> %s" % (kind, rel(root, src), rel(root, dst)))
    if total == 0:
        print("没有要搬的（可能已经迁过了）。")
        return 0
    if not args.apply:
        print("\n[dry] 共 %d 项。确认无误后加 --apply 执行。" % total)
        return 0

    # 1) 预检：源在、目标不冲突
    for name, ops in plans.items():
        for src, dst, _kind, _note in ops:
            if not os.path.exists(src):
                sys.exit("源不在了：%s" % src)
            if os.path.exists(dst):
                sys.exit("目标已存在，先人工确认：%s" % dst)

    # 2) 备份元数据（回滚用）
    meta_dir = os.path.join(NAVDATA, "_migrate_mapfolders_%s_meta" % stamp)
    os.makedirs(meta_dir, exist_ok=True)
    log["meta_backup"] = meta_dir
    for name, root in (("native", P.NATIVE), ("dev", P.DEV)):
        for fn in list(META_NAMES) + ["_index.json", "INDEX.md", "names.json"]:
            for cand in (os.path.join(root, fn), os.path.join(root, P.COMMON, fn)):
                if os.path.isfile(cand):
                    dst = os.path.join(meta_dir, name + "__" + os.path.basename(cand))
                    shutil.copy2(cand, dst)
                    writable(dst)

    # 3) 擦只读属性（① 的文件是只读的，不擦搬不动）
    ro_files = []
    for _name, root in (("native", P.NATIVE), ("dev", P.DEV)):
        if not os.path.isdir(root):
            continue
        for base, dirs, files in os.walk(root):
            writable(base)
            for fn in files:
                p = os.path.join(base, fn)
                if not (os.stat(p).st_mode & stat.S_IWRITE):
                    ro_files.append(p)
                writable(p)

    # 4) 搬
    moved = {"native": [], "dev": []}
    for name, ops in plans.items():
        root = P.NATIVE if name == "native" else P.DEV
        for src, dst, kind, note in ops:
            h = sha(src)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
            if sha(dst) != h:
                sys.exit("!! 搬完 sha256 不一致，停：%s" % dst)
            moved[name].append((src, dst, kind, note))
            print("   %s -> %s" % (rel(root, src), rel(root, dst)))
    log["roots"] = {k: [[a, b, c, d] for a, b, c, d in v] for k, v in moved.items()}

    # 5) 元数据
    frozen = None
    if os.path.isdir(os.path.join(P.NATIVE, P.COMMON)):
        fres = os.path.join(P.NATIVE, P.COMMON, ".frozen.json")
        if os.path.isfile(fres):
            frozen = rewrite_native_frozen(fres, P.NATIVE, moved["native"])
            sums = regen_sums(P.NATIVE)
            if frozen is not None:
                frozen["manifest_sha256"] = hashlib.sha256(
                    "\n".join(sums).encode("utf-8")).hexdigest()
                save_json(fres, frozen)
                rewrite_native_readme(P.NATIVE, frozen, sums)
    if os.path.isdir(os.path.join(P.DEV, P.COMMON)):
        rewrite_dev_index(P.DEV)
        old_new = {note: P.map_folder(level_of_json(dst)) + "/map.json"
                   for src, dst, kind, note in moved["dev"] if kind == "map"}
        rewrite_index_md(P.DEV, old_new)

    # 6) 清掉空的旧目录
    for name, root in (("native", P.NATIVE), ("dev", P.DEV)):
        for sub in ("maps", "nav", "vis", os.path.join("vis", "navmesh")):
            d = os.path.join(root, sub)
            if os.path.isdir(d) and not os.listdir(d):
                try:
                    os.rmdir(d)
                except OSError:
                    pass

    # 7) ① 恢复只读
    for base, dirs, files in os.walk(P.NATIVE):
        for fn in files:
            readonly(os.path.join(base, fn))
        readonly(base)

    path = os.path.join(NAVDATA, "_migrate_mapfolders_%s.json" % stamp)
    save_json(path, log)
    save_json(os.path.join(NAVDATA, "_migrate_mapfolders_last.json"), log)
    print("\n完成。日志：%s" % path)
    print("下一步：python navdata.py status / verify / diff 复核；控制台和网页编辑器都用新布局。")
    return 0


def undo():
    last = os.path.join(NAVDATA, "_migrate_mapfolders_last.json")
    if not os.path.isfile(last):
        sys.exit("没有迁移日志，没法退：%s" % last)
    log = load_json(last)
    for name in ("dev", "native"):
        root = P.DEV if name == "dev" else P.NATIVE
        for src, dst, _kind, _note in reversed(log["roots"].get(name) or []):
            if not os.path.exists(dst):
                print("   跳过（已经不在了）：%s" % dst)
                continue
            os.makedirs(os.path.dirname(src), exist_ok=True)
            h = sha(dst)
            writable(dst)
            shutil.move(dst, src)
            if sha(src) != h:
                sys.exit("!! 退回去 sha256 不一致，停：%s" % src)
            print("   %s <- %s" % (rel(root, src), rel(root, dst)))
    meta = log.get("meta_backup") or ""
    for name, root in (("native", P.NATIVE), ("dev", P.DEV)):
        for fn in list(META_NAMES) + ["_index.json", "INDEX.md", "names.json"]:
            cand = os.path.join(meta, name + "__" + fn)
            if not os.path.isfile(cand):
                continue
            for target in (os.path.join(root, fn), os.path.join(root, P.COMMON, fn)):
                if os.path.isfile(target):
                    writable(target)
                    shutil.copy2(cand, target)
                    break
    print("已按 %s 退回。" % last)
    return 0


def main():
    ap = argparse.ArgumentParser(description="一趟搬完：maps/nav/vis -> 一张图一个文件夹")
    ap.add_argument("--apply", action="store_true", help="真的执行（默认只看）")
    ap.add_argument("--undo", action="store_true", help="按上一次的日志退回去")
    return run(ap.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
