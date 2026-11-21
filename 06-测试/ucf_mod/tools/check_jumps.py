# -*- coding: utf-8 -*-
"""跳链体检：跳点必须「两端都是图上的路点 + 两点之间在图上连着」，否则人机永远不会用它。

用法：
    python tools/check_jumps.py                  # 体检 ② 测试包里所有 *.txt
    python tools/check_jumps.py <包目录或 .txt>   # 只体检一个包/一个文件
    python tools/check_jumps.py --native         # 顺带体检 navdata/native/maps/*.json 的原生跳链

判据来自 gameassembly 反汇编：
    Bot.OnPathComplete 遍历路径节点，只有「路径里 起点节点 的下一个节点 正好是该跳链的
    endNode」时才插跳跃段（Bot_JumpLink.GetLink + GetLinkEndByGraphNode）。
    => 跳链两点之间必须有一条 A->B 的边，否则 A* 永远不会把这两个点连着排，
       跳链一次都不会触发。两端解析到同一个节点 / 有一端没有节点，同样永远不触发。
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import ucf_paths as P                       # noqa: E402  图文件夹 / 测试包的唯一来源

PACKS = P.PACKS_DIR                          # ② navdata\dev\packs\<图>\<包>
NATIVE = P.NATIVE                            # ① 备份版：一张图一个文件夹

SNAP = 1.0          # 端点吸附到路点的最大距离（对齐游戏 OnLatePostScan 的 GetNearest，别用 3 m 放宽）
MIN_LEN = 1.5       # 短于这个距离的跳链没意义
MAX_LEN = 3.0       # 长于这个距离 Bot 跳不过去：原生 21+2+18 条跳链最长 2.91 m


def parse_pack(path):
    nodes, edges, jumps = [], [], []
    for lineno, raw in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        t = raw.split()
        if not t:
            continue
        if t[0] == "node" and len(t) >= 5 and t[1] == "add":
            nodes.append((float(t[2]), float(t[3]), float(t[4])))
        elif t[0] == "edge" and len(t) >= 8:
            edges.append((t[1], (float(t[2]), float(t[3]), float(t[4])),
                          (float(t[5]), float(t[6]), float(t[7]))))
        elif t[0] == "jump" and len(t) >= 8 and t[1] == "add":
            jumps.append(((float(t[2]), float(t[3]), float(t[4])),
                          (float(t[5]), float(t[6]), float(t[7])), lineno))
    return nodes, edges, jumps


def nearest(pos, pt, maxd):
    best, bd = -1, maxd * maxd
    for i, q in enumerate(pos):
        d = (pt[0] - q[0]) ** 2 + (pt[1] - q[1]) ** 2 + (pt[2] - q[2]) ** 2
        if d < bd:
            bd, best = d, i
    return best, (math.sqrt(bd) if best >= 0 else None)


def degree_of(edges, node, snap=0.15):
    """这个路点连了几条边（无向计）。0 = Bot 走不到；跳链只加一条 = 死胡同。"""
    n = 0
    for _kind, ea, eb in edges:
        if math.dist(ea, node) <= snap or math.dist(eb, node) <= snap:
            n += 1
    return n


def has_edge(edges, pa, pb, snap=0.15):
    """边按坐标匹配：传进来的是解析出来的路点坐标，不是跳链原始端点。"""
    for _kind, ea, eb in edges:
        if math.dist(ea, pa) <= snap and math.dist(eb, pb) <= snap:
            return True
        if math.dist(eb, pa) <= snap and math.dist(ea, pb) <= snap:
            return True
    return False


def check_pack(path):
    nodes, edges, jumps = parse_pack(path)
    print("=" * 78)
    print("包: %s" % path)
    print("    路点 %d · 边 %d · 跳链 %d" % (len(nodes), len(edges), len(jumps)))
    if not jumps:
        return 0
    ok = bad_same = bad_miss = bad_noedge = bad_short = bad_long = 0
    bad_start = bad_dead = 0
    for a, b, lineno in jumps:
        ia, _ = nearest(nodes, a, SNAP)
        ib, _ = nearest(nodes, b, SNAP)
        length = math.dist(a, b)
        if ia >= 0 and ib >= 0 and ia == ib and length < MIN_LEN:
            bad_short += 1
            print("  行%-4d 太短 %.2f m（<%.1f，两端还落在同一个路点）→ 不会触发"
                  % (lineno, length, MIN_LEN))
        elif ia < 0 or ib < 0:
            bad_miss += 1
            print("  行%-4d 端点在 %.1f m 内没有路点（起点=%s 落点=%s）→ 不会触发"
                  % (lineno, SNAP, "有" if ia >= 0 else "无", "有" if ib >= 0 else "无"))
        elif ia == ib:
            bad_same += 1
            print("  行%-4d 两端是同一个路点 #%d（落点只隔 %.2f m）→ 不会触发"
                  % (lineno, ia, length))
        elif not has_edge(edges, nodes[ia], nodes[ib]):
            bad_noedge += 1
            print("  行%-4d 路点 #%d -> #%d 之间没有边 → A* 不会连着排这两个点，不会触发"
                  % (lineno, ia, ib))
        elif length > MAX_LEN:
            bad_long += 1
            print("  行%-4d 跳距 %.2f m（>%.1f，原生最长 2.91 m）→ 会触发但跳不过去，"
                  "中间补路点拆成两段" % (lineno, length, MAX_LEN))
        else:
            ok += 1
            dstart = degree_of(edges, nodes[ia])
            dend = degree_of(edges, nodes[ib])
            note = ""
            if dstart <= 0:
                note += "  [起点没有任何边，Bot 走不到]"
                bad_start += 1
            if dend <= 1:
                note += "  [落点只连着起点：跳过去继续走不了，除非落点就是目标]"
                bad_dead += 1
            print("  行%-4d 路点 #%d(%d条边) -> #%d(%d条边)  %.2f m  OK%s"
                  % (lineno, ia, dstart, ib, dend, length, note))
    print("  合计: 能触发 %d / %d   无效: 同点 %d · 缺路点 %d · 无连线 %d · 太短 %d · 超长 %d"
          % (ok, len(jumps), bad_same, bad_miss, bad_noedge, bad_short, bad_long))
    if bad_start or bad_dead:
        print("  注意: 有 %d 条起点没连边（Bot 走不到）、%d 条落点是死胡同（跳过去走不了）"
              % (bad_start, bad_dead))
    return ok


def vec3(v):
    if isinstance(v, dict):
        v = v.get("value", [0, 0, 0])
    return (float(v[0]), float(v[1]), float(v[2]))


def check_native():
    total_ok = total = 0
    for rel, path in P.map_files(NATIVE):
        name = rel.replace("/map.json", "")
        j = json.load(open(path, encoding="utf-8"))
        jumps = ((j.get("lines") or {}).get("jump") or [])
        if not jumps:
            continue
        nodes = [tuple(n["p"][:3]) for n in (j.get("nodes") or [])]
        ids = [n["id"] for n in (j.get("nodes") or [])]
        eset = set()
        for e in (j.get("edges") or []):
            if len(e) >= 2:
                eset.add((e[0], e[1]))
                eset.add((e[1], e[0]))
        edges = []
        for e in (j.get("edges") or []):
            if len(e) >= 2:
                ia = ids.index(e[0]) if e[0] in ids else -1
                ib = ids.index(e[1]) if e[1] in ids else -1
                if ia >= 0 and ib >= 0:
                    edges.append(("add", nodes[ia], nodes[ib]))
        stat = {"ok": 0, "same": 0, "miss": 0, "noedge": 0}
        for a, b in jumps:
            A, B = vec3(a), vec3(b)
            ia, _ = nearest(nodes, A, 4.0)
            ib, _ = nearest(nodes, B, 4.0)
            total += 1
            if ia < 0 or ib < 0:
                stat["miss"] += 1
            elif ia == ib:
                stat["same"] += 1
            elif (ids[ia], ids[ib]) in eset:
                stat["ok"] += 1
                total_ok += 1
            else:
                stat["noedge"] += 1
        print("%-28s 跳链 %2d -> 有边 %2d · 同点 %2d · 缺路点 %2d · 无连线 %2d"
              % (name, len(jumps), stat["ok"], stat["same"], stat["miss"], stat["noedge"]))
    print("原生跳链合计: 有边 %d / %d" % (total_ok, total))


def iter_pack_files(arg):
    if arg:
        p = os.path.abspath(arg)
        if os.path.isfile(p):
            yield p
            return
        for dirpath, _dirs, files in os.walk(p):
            for f in files:
                if f.endswith(".txt") and f != "nogen.txt":
                    yield os.path.join(dirpath, f)
        return
    if not os.path.isdir(PACKS):
        return
    for dirpath, _dirs, files in os.walk(PACKS):
        for f in files:
            if f.endswith(".txt") and f != "nogen.txt":
                yield os.path.join(dirpath, f)


def main():
    ap = argparse.ArgumentParser(description="跳链体检：跳点两端要有路点、两点之间还要有边")
    ap.add_argument("path", nargs="?", help="包目录或 nav 编辑文件（默认扫 navdata/dev/packs）")
    ap.add_argument("--native", action="store_true", help="顺带体检原生图导出的跳链")
    args = ap.parse_args()
    if args.native:
        print("---- 原生图（navdata/native/<图>/map.json）----")
        check_native()
    files = list(iter_pack_files(args.path))
    if not files:
        print("没有找到包文件")
        return 0
    good = 0
    for f in files:
        good += check_pack(f)
    return 0


if __name__ == "__main__":
    sys.exit(main())
