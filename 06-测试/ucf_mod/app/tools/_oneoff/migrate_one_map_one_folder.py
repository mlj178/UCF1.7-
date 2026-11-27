#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""把 navdata 的四处（native / dev / packs / markers）并成「一张图一个文件夹」。

    python app/tools/_oneoff/migrate_one_map_one_folder.py            # 默认 dry-run：只打印要搬什么
    python app/tools/_oneoff/migrate_one_map_one_folder.py --apply     # 真搬：逐文件比 sha256
    python app/tools/_oneoff/migrate_one_map_one_folder.py --undo      # 按上一次日志原路退回

搬成什么样（2026-11-27「一图一夹」）：

    data\navdata\dev\<图>\map.json            -> data\maps\<图>\map.json
    data\navdata\dev\<图>\navmesh.bin         -> data\maps\<图>\navmesh.bin
    data\navdata\dev\packs\<图>\<指纹>.txt      -> data\maps\<图>\<指纹>.txt     （点图草稿）
    data\navdata\dev\packs\<图>\manifest.json  -> data\maps\<图>\manifest.json
    data\navdata\dev\markers\<图>\markers.txt  -> data\maps\<图>\markers.txt     （蹲守/守卫区/守卫点/标签/出生点）
    data\navdata\native\<图>\map.json          -> data\maps\<图>\native\map.json  （① 冻结副本）
    data\navdata\native\<图>\navmesh.bin       -> data\maps\<图>\native\navmesh.bin
    data\navdata\dev\00_公共\*                 -> data\maps\00_公共\*
    data\navdata\native\00_公共\*              -> data\maps\00_公共\*（names.json 撞名存为 names.native.json）
    data\navdata\dev\vis\*                     -> data\maps\_inbox\*
    data\navdata\dev\archive\*                 -> data\maps\_archive\*

搬完还会改两份清单里的路径前缀（<图>/map.json -> <图>/native/map.json），
搬前搬后都算 sha256 逐个比对；日志写在 data\maps\_archive\migrate_onemap_<时间>.json。
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

NAVDATA = os.path.join(UCF_ROOT, "data", "navdata")
MAPS = os.path.join(UCF_ROOT, "data", "maps")
COMMON = "00_公共"
NATIVE = "native"
# dev\ 下面这些是"功能目录"，不是地图文件夹（地图文件夹里一定有 map.json 或 navmesh.bin）
SKIP_DIRS = {"final", "nav", "packs", "markers", "vis", "archive", COMMON}
SKIP_NAMES = {".gitkeep"}


# ---------------------------------------------------------------- 小工具
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def make_writable(p):
    try:
        os.chmod(p, os.stat(p).st_mode | stat.S_IWRITE)
    except OSError:
        pass


def rel_to_root(p):
    return os.path.relpath(p, UCF_ROOT).replace(os.sep, "/")


def is_map_dirname(d):
    r"""d 是地图文件夹吗：名字正常 + 里面真有 map.json / navmesh.bin。"""
    name = os.path.basename(d)
    if not name or name.startswith(("_", ".")) or name in SKIP_DIRS:
        return False
    return os.path.isfile(os.path.join(d, "map.json")) or os.path.isfile(os.path.join(d, "navmesh.bin"))


def walk_files(root):
    out = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for fn in sorted(files):
            p = os.path.join(base, fn)
            out.append(os.path.relpath(p, root).replace(os.sep, "/"))
    return sorted(out)


# ---------------------------------------------------------------- 计划
def build_plan():
    r"""[(src, dst)]，只读磁盘，不动任何东西。"""
    moves = []

    def add_tree(src_root, dst_root):
        if not os.path.isdir(src_root):
            return
        for rel in walk_files(src_root):
            if rel.split("/")[-1] in SKIP_NAMES:
                continue
            src = os.path.join(src_root, rel.replace("/", os.sep))
            dst = os.path.join(dst_root, rel.replace("/", os.sep))
            moves.append((src, dst))

    dev = os.path.join(NAVDATA, "dev")
    native = os.path.join(NAVDATA, "native")

    # ② 开发版：图文件夹本体
    for name in sorted(os.listdir(dev)) if os.path.isdir(dev) else []:
        d = os.path.join(dev, name)
        if not os.path.isdir(d) or not is_map_dirname(d):
            continue
        add_tree(d, os.path.join(MAPS, name))

    # ② 草稿（点图）
    for name in sorted(os.listdir(os.path.join(dev, "packs"))) if os.path.isdir(os.path.join(dev, "packs")) else []:
        add_tree(os.path.join(dev, "packs", name), os.path.join(MAPS, name))

    # ② 编辑标记（蹲守点 / 守卫区 / 守卫点 / 标签 / 出生点）
    for name in sorted(os.listdir(os.path.join(dev, "markers"))) if os.path.isdir(os.path.join(dev, "markers")) else []:
        add_tree(os.path.join(dev, "markers", name), os.path.join(MAPS, name))

    # ① 冻结副本 -> <图>\native\
    for name in sorted(os.listdir(native)) if os.path.isdir(native) else []:
        d = os.path.join(native, name)
        if not os.path.isdir(d) or not is_map_dirname(d):
            continue
        add_tree(d, os.path.join(MAPS, name, NATIVE))

    # 公共文件：② 的先进，① 的同名改存 names.native.json
    for base, tag in ((os.path.join(dev, COMMON), "dev"), (os.path.join(native, COMMON), "native")):
        if not os.path.isdir(base):
            continue
        for fn in sorted(os.listdir(base)):
            p = os.path.join(base, fn)
            if not os.path.isfile(p) or fn in SKIP_NAMES:
                continue
            dst = os.path.join(MAPS, COMMON, fn)
            if os.path.exists(dst):
                stem, ext = os.path.splitext(fn)
                dst = os.path.join(MAPS, COMMON, "%s.%s%s" % (stem, tag, ext))
            moves.append((p, dst))

    # 收件箱 / 回收站
    add_tree(os.path.join(dev, "vis"), os.path.join(MAPS, "_inbox"))
    add_tree(os.path.join(dev, "archive"), os.path.join(MAPS, "_archive"))
    return moves


# ---------------------------------------------------------------- 清单改写
def rewrite_sums():
    r"""ShA256SUMS：<图>/map.json -> <图>/native/map.json，哈希不变（内容没改）。"""
    p = os.path.join(MAPS, COMMON, "SHA256SUMS.txt")
    if not os.path.isfile(p):
        return None
    with io.open(p, "r", encoding="utf-8") as f:
        old = f.read()
    lines = []
    for line in old.splitlines():
        if not line.strip():
            continue
        h, rel = line.split("  ", 1)
        if rel == COMMON + "/names.json":
            continue                       # ① 自己的 names.json 已经另存，不再进清单
        if "/" in rel and not rel.split("/")[0] in (COMMON, "_inbox", "_archive"):
            head, tail = rel.split("/", 1)
            rel = "%s/%s/%s" % (head, NATIVE, tail)
        lines.append("%s  %s" % (h, rel))
    new = "\n".join(lines) + "\n"
    return p, old, new, lines


def rewrite_frozen(lines):
    p = os.path.join(MAPS, COMMON, ".frozen.json")
    if not os.path.isfile(p):
        return None
    with io.open(p, "r", encoding="utf-8") as f:
        old = f.read()
    doc = json.loads(old)
    for m in doc.get("maps") or []:
        head, tail = str(m.get("file") or "").split("/", 1)
        m["file"] = "%s/%s/%s" % (head, NATIVE, tail)
    doc["navmesh_bins"] = ["%s/%s/%s" % (str(b).split("/", 1)[0], NATIVE, str(b).split("/", 1)[1])
                           for b in (doc.get("navmesh_bins") or []) if "/" in str(b)]
    origin = {}
    for k, v in (doc.get("navmesh_origin") or {}).items():
        if "/" in str(k):
            head, tail = str(k).split("/", 1)
            origin["%s/%s/%s" % (head, NATIVE, tail)] = v
    doc["navmesh_origin"] = origin
    doc["layout"] = "one-map-one-folder"
    doc["migrated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    doc["manifest_sha256"] = hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
    new = json.dumps(doc, ensure_ascii=False, indent=1) + "\n"
    return p, old, new


# ---------------------------------------------------------------- 动作
def do_apply(moves):
    os.makedirs(os.path.join(MAPS, COMMON), exist_ok=True)
    log = {"format": "ucf-migrate-onemap", "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
           "moves": [], "rewritten": []}
    bad = []
    for src, dst in moves:
        if not os.path.isfile(src):
            continue
        if os.path.exists(dst):
            if sha(src) == sha(dst):
                print("  跳过（目标已有同内容）：%s" % rel_to_root(dst))
                make_writable(src)
                os.remove(src)
                continue
            # 撞名但内容不同：按来源加后缀存下来（① 的 names.json -> names.native.json），不覆盖别人
            tag = "native" if (os.sep + "native" + os.sep) in src else "dup"
            stem, ext = os.path.splitext(dst)
            alt = "%s.%s%s" % (stem, tag, ext)
            while os.path.exists(alt):
                stem, ext = os.path.splitext(alt)
                alt = "%s_%s%s" % (stem, tag, ext)
            print("  撞名，改存为 %s" % rel_to_root(alt))
            dst = alt
        before = sha(src)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        make_writable(dst)
        after = sha(dst)
        if before != after:
            bad.append((src, dst, "sha256 不一致 %s -> %s" % (before[:16], after[:16])))
            continue
        make_writable(src)
        os.remove(src)
        log["moves"].append({"src": rel_to_root(src), "dst": rel_to_root(dst),
                             "sha256": before, "bytes": os.path.getsize(dst)})
    if bad:
        print("")
        print("!! 有 %d 个文件没搬成功（其余已搬，可 --undo 回滚）：" % len(bad))
        for src, dst, why in bad:
            print("   %s -> %s  %s" % (rel_to_root(src), rel_to_root(dst), why))
        return None

    sums = rewrite_sums()
    lines = sums[3] if sums else []
    for item in (sums[:3] if sums else (), rewrite_frozen(lines) or ()):
        p, old, new = item
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(new)
        log["rewritten"].append({"path": rel_to_root(p), "before": old, "after": new})

    # 老目录：搬空了就删（dev/final、dev/nav 这种原本就空的也一起清）
    gone = []
    for d in (os.path.join(NAVDATA, "dev", "packs"), os.path.join(NAVDATA, "dev", "markers"),
              os.path.join(NAVDATA, "dev", "vis"), os.path.join(NAVDATA, "dev", "archive"),
              os.path.join(NAVDATA, "native"), os.path.join(NAVDATA, "dev")):
        if os.path.isdir(d):
            left = [f for f in walk_files(d)]
            if left:
                print("   留着（还有 %d 个文件）：%s" % (len(left), rel_to_root(d)))
                continue
            for base, dirs, files in os.walk(d, topdown=False):
                try:
                    os.rmdir(base)
                except OSError:
                    pass
            gone.append(rel_to_root(d))
    if os.path.isdir(NAVDATA) and not walk_files(NAVDATA) and not os.listdir(NAVDATA):
        try:
            os.rmdir(NAVDATA)
            gone.append(rel_to_root(NAVDATA))
        except OSError:
            pass
    log["removed_dirs"] = gone

    os.makedirs(os.path.join(MAPS, "_archive"), exist_ok=True)
    logp = os.path.join(MAPS, "_archive", "migrate_onemap_%s.json" % time.strftime("%Y%m%d_%H%M%S"))
    with io.open(logp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(log, f, ensure_ascii=False, indent=1)
    print("")
    print("搬完：%d 个文件；清单改写 %d 份；日志 %s" % (
        len(log["moves"]), len(log["rewritten"]), rel_to_root(logp)))
    return logp


def do_undo():
    arch = os.path.join(MAPS, "_archive")
    logs = sorted(f for f in os.listdir(arch) if f.startswith("migrate_onemap_")) if os.path.isdir(arch) else []
    if not logs:
        sys.exit("没有迁移日志：%s\\migrate_onemap_*.json" % rel_to_root(arch))
    logp = os.path.join(arch, logs[-1])
    with io.open(logp, "r", encoding="utf-8") as f:
        log = json.load(f)
    print("按日志退回：%s（%d 个文件）" % (rel_to_root(logp), len(log["moves"])))
    n = 0
    for m in reversed(log["moves"]):
        src = os.path.join(UCF_ROOT, m["src"].replace("/", os.sep))
        dst = os.path.join(UCF_ROOT, m["dst"].replace("/", os.sep))
        if not os.path.isfile(dst):
            continue
        os.makedirs(os.path.dirname(src), exist_ok=True)
        shutil.copy2(dst, src)
        make_writable(src)
        if sha(src) != m["sha256"]:
            print("   !! 哈希对不上：%s" % m["src"])
        make_writable(dst)
        os.remove(dst)
        n += 1
    for item in log.get("rewritten") or []:
        p = os.path.join(UCF_ROOT, item["path"].replace("/", os.sep))
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with io.open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(item["before"])
    print("退回 %d 个文件，清单已还原。" % n)
    return 0


def do_dry(moves):
    print("dry-run：%d 个文件会搬（--apply 才真搬）" % len(moves))
    print("")
    by_dst = {}
    for src, dst in moves:
        by_dst.setdefault(os.path.dirname(dst), []).append(os.path.basename(dst))
    for d in sorted(by_dst):
        print("  %s/" % rel_to_root(d))
        for fn in sorted(by_dst[d]):
            print("      %s" % fn)
    print("")
    bt = 0
    for src, _dst in moves:
        try:
            bt += os.path.getsize(src)
        except OSError:
            pass
    print("合计 %.1f MB" % (bt / 1048576.0))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="真搬（默认 dry-run）")
    ap.add_argument("--undo", action="store_true", help="按上一次日志退回")
    args = ap.parse_args()
    if args.undo:
        return do_undo()
    moves = build_plan()
    if not moves:
        print("没有要搬的东西（已经是一图一夹了？）")
        return 0
    if not args.apply:
        return do_dry(moves)
    logp = do_apply(moves)
    return 0 if logp else 1


if __name__ == "__main__":
    sys.exit(main())
