#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""录制轨迹的解析 / 重采样 / 事件识别 —— 控制台「录制」页只读这里。

数据来源：src/editor.c 的 rec_tick()，20 Hz 往一个 jsonl 里追加一行：

    {"t":12.345,"x":-52.80,"y":-15.02,"z":3.63,"gy":-16.59,
     "fx":0.71,"fy":0.02,"fz":0.70,"sp":0,"ct":0}

    t        从开始录制算起的秒数（控制台点「开始录制」那一刻 = 0）
    x y z    相机（玩家眼睛）位置
    gy       相机正下方射线打到的地面高度；没打到写 -9999
    fx fy fz 相机朝向（单位向量）
    sp       空格按下（跳跃）
    ct       Ctrl 按下（蹲下）
    最后一行 {"end":1,"t":..,"n":..,"dist":..}

这里只做纯计算（不读文件、不碰 tkinter），方便 tools/test_ucf_rec.py 离线跑。

识别规则（2026-11-21 与设计稿一致，改阈值只改这一段常量）：
    跳跃   空格 + 离地 > 0.30 m，落点水平 >= 1.50 m   -> jump add + A→B 边
    落下   没按空格，下降 >= 1.5 m 且落差 >= 2.0 m     -> 单向 A→B 边
    岔路   2.5 m 内第二次经过（绕回）                  -> 标黄候选，保存仍按双向
    蹲点   Ctrl > 0.8 s 且位移 < 1 m                   -> 只提示，不落点
    静止   2 s 不动                                    -> 采样照常，复盘里只写一句
    传送   单帧位移 > 15 m                             -> 断段，段间不连边
"""
import json
import math

# ---- 阈值（改这里；控制台「录制」页的说明文字按这几行写）----
JUMP_RISE = 0.30       # 离地高度（眼睛相对站立高度抬起多少算起跳）
JUMP_MIN_H = 1.50      # 跳链最短水平距离
JUMP_MAX_T = 2.00      # 一次跳跃最长 2 s，超了就当没落地（断段）
DROP_MIN = 1.50        # 单次下降至少这么多
DROP_TOTAL = 2.00      # 落差（起跳点地面 - 落点地面）
DROP_HURT = 6.00       # 落差超过 6 m 标「可能摔伤」
BRANCH_NEAR = 2.50     # 2.5 m 内第二次经过 = 岔路候选
CROUCH_TIME = 0.80     # 蹲 >= 0.8 s
CROUCH_MOVE = 1.00     # 且位移 < 1 m
STATIC_TIME = 2.00     # 2 s 没位移
WARP_DIST = 15.00      # 单帧位移 > 15 m = 传送
EDGE_MAX = 4.60        # 边长超过这个值在复盘里标出来
NODE_MIN_GAP = 0.60    # 重采样后两个节点至少隔这么远
CORNER_DEG = 55.0      # 转角超过 55° 强制补一个节点
CORNER_REACH = 1.20    # 判断转角时前后各看 1.2 m

SWITCHES = (
    ("jump",   "自动识别跳跃", "空格 + 离地 > 0.3 m、水平 >= 1.5 m → 跳链"),
    ("drop",   "自动识别落下", "没按空格、下降 >= 1.5 m、落差 >= 2 m → 单向边"),
    ("branch", "自动识别岔路", "2.5 m 内第二次经过 → 标黄待确认"),
    ("crouch", "记录蹲点位置", "蹲 > 0.8 s 且位移 < 1 m → 只提示"),
    ("static", "静止暂停采样", "2 s 没位移 → 复盘里写一句"),
    ("warp",   "传送断段", "单帧位移 > 15 m → 断段、不连边"),
)
SW_DEFAULT = {key: True for key, _l, _d in SWITCHES}
STEP_OPTIONS = (2.5, 4.0, 6.0)
STEP_DEFAULT = 4.0


def norm_switch(sw):
    out = dict(SW_DEFAULT)
    if isinstance(sw, dict):
        for key in out:
            if key in sw:
                out[key] = bool(sw[key])
    return out


def dist2(a, b):
    return math.hypot(a[0] - b[0], a[2] - b[2])


def dist3(a, b):
    r"""三维距离：上下层两个点水平只差 1 m 也不能当成同一个点。"""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def parse_lines(lines):
    r"""jsonl 行 -> 样本列表（按 t 排序；坏行直接跳过）。"""
    out = []
    for raw in lines:
        s = (raw or "").strip()
        if not s or s[0] != "{":
            continue
        try:
            d = json.loads(s)
        except ValueError:
            continue
        if not isinstance(d, dict) or "x" not in d:
            continue
        try:
            out.append({
                "t": float(d.get("t") or 0.0),
                "x": float(d["x"]), "y": float(d["y"]), "z": float(d["z"]),
                "gy": float(d.get("gy", -9999.0)),
                "fx": float(d.get("fx", 0.0)), "fy": float(d.get("fy", 0.0)),
                "fz": float(d.get("fz", 0.0)),
                "sp": int(d.get("sp") or 0), "ct": int(d.get("ct") or 0),
            })
        except (TypeError, ValueError):
            continue
    out.sort(key=lambda s: s["t"])
    clean = []
    for s in out:
        if clean and abs(s["t"] - clean[-1]["t"]) < 0.002:
            clean[-1] = s
        else:
            clean.append(s)
    return clean


def _eye_base(seg):
    r"""站立时眼睛离地高度：取「地面有效且高度合理」样本的中位数。"""
    gaps = []
    for s in seg:
        if s["gy"] > -1000.0:
            g = s["y"] - s["gy"]
            if 0.6 <= g <= 3.0:
                gaps.append(g)
    if not gaps:
        return 1.60
    gaps.sort()
    base = gaps[len(gaps) // 2]
    return base if base > 0.6 else 1.60


def _feet(seg, base):
    r"""每个样本的脚下高度：优先用射线打到的地面；悬空时沿用上一段地面。"""
    out = []
    last = None
    for s in seg:
        if s["gy"] > -1000.0:
            last = s["gy"]
            out.append(s["gy"])
        elif last is not None:
            out.append(last)
        else:
            out.append(s["y"] - base)
    return out


def _segments(samples, sw):
    r"""传送 / 长暂停断段：段间不连边。"""
    if not samples:
        return []
    segs = []
    cur = [samples[0]]
    for prev, s in zip(samples, samples[1:]):
        jump = math.hypot(s["x"] - prev["x"], s["z"] - prev["z"])
        dt = s["t"] - prev["t"]
        cut = (sw["warp"] and jump > WARP_DIST) or dt > 3.0
        if cut:
            if len(cur) >= 2:
                segs.append(cur)
            cur = [s]
        else:
            cur.append(s)
    if len(cur) >= 2:
        segs.append(cur)
    return segs


def _find_jumps(seg, feet, base, sw):
    r"""空格 + 离地 -> (起跳样本, 落点样本, 抬升)。返回的切点已按 JUMP_MIN_H 过滤。"""
    out = []
    if not sw["jump"]:
        return out
    n = len(seg)
    i = 1
    while i < n - 1:
        s = seg[i]
        # 用「眼睛 - 脚下地面」算离地高度：越过壕沟时脚下打不到射线，
        # feet[] 沿用起跳前的地面，照样能看出人已经离地。
        gap = s["y"] - feet[i]
        pressed = bool(s["sp"] or seg[i - 1]["sp"] or (i + 1 < n and seg[i + 1]["sp"]))
        if gap > base + JUMP_RISE and pressed:
            k = i
            top = gap
            while k + 1 < n:
                k += 1
                g2 = seg[k]["y"] - feet[k]
                top = max(top, g2)
                if g2 < base + 0.15:
                    break
                if seg[k]["t"] - s["t"] > JUMP_MAX_T:
                    break
            if k > i:
                # 落点取样到第一个重新打到地面的样本（脚刚落地那一帧可能还是空）
                b = k
                while b + 1 < n and seg[b]["gy"] <= -1000.0:
                    b += 1
                if seg[b]["gy"] <= -1000.0:
                    i = k + 1
                    continue
                a = i - 1
                while a > 0 and (seg[a]["y"] - feet[a]) > base + 0.08:
                    a -= 1        # 起跳点 = 离地前最后一个还在地面的样本
                ax, az = seg[a]["x"], seg[a]["z"]
                bx, bz = seg[b]["x"], seg[b]["z"]
                h = math.hypot(bx - ax, bz - az)
                if h >= JUMP_MIN_H:
                    out.append({"kind": "jump", "a": a, "b": b, "h": h,
                                "rise": max(0.0, top - base)})
                i = b + 1
                continue
        i += 1
    return out


def _find_drops(seg, feet, jumps, sw):
    r"""没按空格、地面掉 >= 1.5 m 且总落差 >= 2 m -> 单向边。

    只在「地面开始往下掉」的那一帧起算，往后追到落地为止（最长 1.2 s）；
    下降前、落地后都要求地面基本是平的，避免把楼梯 / 斜坡当成高台落下。
    """
    out = []
    if not sw["drop"]:
        return out
    n = len(seg)
    in_jump = set()
    for j in jumps:
        in_jump.update(range(max(0, j["a"] - 1), min(n, j["b"] + 1)))
    i = 2
    while i < n - 2:
        if i in in_jump:
            i += 1
            continue
        if feet[i] < feet[i - 1] - 0.12:
            a = i - 1
            head = [feet[q] for q in range(max(0, a - 8), a + 1)]
            pre = (max(head) - min(head)) < 0.5
            best = i
            k = i + 1
            while k < n and seg[k]["t"] - seg[a]["t"] <= 1.2:
                if feet[k] < feet[best]:
                    best = k
                elif k - best >= 4:
                    break
                k += 1
            drop = feet[a] - feet[best]
            tail = [feet[q] for q in range(best, min(n, best + 8))]
            flat = (max(tail) - min(tail)) < 0.6
            if drop >= DROP_TOTAL and pre and flat:
                out.append({"kind": "drop", "a": a, "b": best, "drop": drop})
                i = best + 2
                continue
        i += 1
    return out


def _merge_cuts(cuts, n):
    r"""起跳/落下切点合并：重叠时保留先出现的那次，a < b 才有效。"""
    out = []
    for c in sorted(cuts, key=lambda c: (c["a"], c["b"])):
        if c["a"] < 0 or c["b"] <= c["a"] or c["b"] >= n:
            continue
        if out and c["a"] <= out[-1]["b"]:
            # 重叠：跳优先；同类型保留水平距离大的
            prev = out[-1]
            if c["kind"] == "jump" and prev["kind"] == "drop":
                out[-1] = c
            continue
        out.append(c)
    return out


def _resample(pts, step, forced):
    r"""按 step 重采样；forced 里的点（转角/端点）一定落成节点。"""
    nodes = [pts[0]]
    acc = 0.0
    for i in range(1, len(pts)):
        a = nodes[-1]
        b = pts[i]
        d = math.hypot(b[0] - a[0], b[2] - a[2])
        while d > 1e-6 and acc + d >= step:
            need = step - acc
            t = need / d
            p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t,
                 a[2] + (b[2] - a[2]) * t)
            nodes.append(p)
            a = p
            d = math.hypot(b[0] - a[0], b[2] - a[2])
            acc = 0.0
        acc += d
        if i in forced and dist2(nodes[-1], b) >= NODE_MIN_GAP:
            nodes.append(b)
            acc = 0.0
    if dist2(nodes[-1], pts[-1]) > 0.05:
        nodes.append(pts[-1])
    # 收尾去重：中间点太近就丢；最后一个点（落点）永远保留
    out = [nodes[0]]
    for k in range(1, len(nodes)):
        p = nodes[k]
        last = k == len(nodes) - 1
        if dist2(out[-1], p) < NODE_MIN_GAP * 0.5 and not last:
            continue
        out.append(p)
    return out


def _corner_index(pts):
    r"""XZ 平面转角 > 55° 的样本下标（前后各看 CORNER_REACH 米）。"""
    n = len(pts)
    if n < 5:
        return set()
    out = set()
    for i in range(2, n - 2):
        j = i
        back = 0.0
        while j > 0 and back < CORNER_REACH:
            back += math.hypot(pts[j][0] - pts[j - 1][0], pts[j][2] - pts[j - 1][2])
            j -= 1
        k = i
        fwd = 0.0
        while k < n - 1 and fwd < CORNER_REACH:
            fwd += math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][2] - pts[k][2])
            k += 1
        if j == i or k == i:
            continue
        v1 = (pts[i][0] - pts[j][0], pts[i][2] - pts[j][2])
        v2 = (pts[k][0] - pts[i][0], pts[k][2] - pts[i][2])
        n1 = math.hypot(*v1)
        n2 = math.hypot(*v2)
        if n1 < 0.05 or n2 < 0.05:
            continue
        cosv = (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)
        cosv = max(-1.0, min(1.0, cosv))
        if math.degrees(math.acos(cosv)) > CORNER_DEG:
            out.add(i)
    return out


def _piece(seg, feet, i0, i1, step):
    r"""一段连续走路 -> 节点链 + 边（双向）。"""
    pts = [(seg[k]["x"], feet[k], seg[k]["z"]) for k in range(i0, i1 + 1)]
    if len(pts) < 2:
        return {"nodes": [pts[0]] if pts else [], "walk": [], "from": i0, "to": i1}
    forced = {0, len(pts) - 1}
    forced |= {i for i in _corner_index(pts) if 0 < i < len(pts) - 1}
    nodes = _resample(pts, max(0.5, float(step)), forced)
    walk = [(i, i + 1) for i in range(len(nodes) - 1)
            if dist2(nodes[i], nodes[i + 1]) >= 0.30]
    return {"nodes": nodes, "walk": walk, "from": i0, "to": i1}


def _find_crouch(seg, sw):
    r"""Ctrl > 0.8 s 且位移 < 1 m：只提示不落点。"""
    out = []
    if not sw["crouch"]:
        return out
    n = len(seg)
    i = 0
    while i < n:
        if not seg[i]["ct"]:
            i += 1
            continue
        j = i
        moved = 0.0
        while j + 1 < n and seg[j + 1]["ct"]:
            moved += math.hypot(seg[j + 1]["x"] - seg[j]["x"], seg[j + 1]["z"] - seg[j]["z"])
            j += 1
        dur = seg[j]["t"] - seg[i]["t"]
        if dur >= CROUCH_TIME and moved < CROUCH_MOVE:
            out.append({"p": (seg[i]["x"], seg[i]["y"], seg[i]["z"]), "t": dur})
        i = j + 1
    return out


def _find_static(seg, sw):
    r"""2 s 没位移：复盘里写一句（采样不停，节点也不会多）。"""
    out = []
    if not sw["static"]:
        return out
    n = len(seg)
    i = 0
    while i < n:
        j = i
        while j + 1 < n:
            if math.hypot(seg[j + 1]["x"] - seg[j]["x"], seg[j + 1]["z"] - seg[j]["z"]) > 0.06:
                break
            j += 1
        dur = seg[j]["t"] - seg[i]["t"]
        if dur >= STATIC_TIME:
            out.append({"p": (seg[i]["x"], seg[i]["y"], seg[i]["z"]), "t": dur})
        i = j + 1
    return out


def _route_len(nodes, i, j):
    total = 0.0
    for k in range(i, j):
        total += dist2(nodes[k], nodes[k + 1])
    return total


def analyse(samples, step=STEP_DEFAULT, sw=None):
    r"""轨迹 -> 节点/双向边/跳链/落下/岔路/蹲点 + 问题清单。"""
    sw = norm_switch(sw)
    step = float(step or STEP_DEFAULT)
    out = {
        "ok": False, "why": "", "step": step, "sw": sw,
        "samples": len(samples or []), "duration": 0.0, "dist": 0.0,
        "pieces": [], "links": [], "jumps": [], "drops": [], "branches": [],
        "crouches": [], "statics": [], "segments": 1,
        "issues": [], "skipped_jump": 0, "warp": 0,
    }
    samples = samples or []
    if len(samples) < 6:
        out["why"] = "样本太少（可能游戏没进图，或插件不是带录制接口的版本）"
        return out
    segs = _segments(samples, sw)
    if not segs:
        out["why"] = "没有有效样本（全被传送/长暂停切掉了）"
        return out
    out["segments"] = len(segs)
    out["duration"] = samples[-1]["t"] - samples[0]["t"]
    for seg in segs:
        for a, b in zip(seg, seg[1:]):
            out["dist"] += math.hypot(b["x"] - a["x"], b["z"] - a["z"])
    for seg in segs:
        base = _eye_base(seg)
        feet = _feet(seg, base)
        jumps = _find_jumps(seg, feet, base, sw)
        drops = _find_drops(seg, feet, jumps, sw)
        cuts = _merge_cuts(jumps + drops, len(seg))
        # 走路段：cut 的两端各留一个样本（起跳点 / 落点）
        start = 0
        pieces = []
        for c in cuts:
            if c["a"] > start:
                pieces.append(_piece(seg, feet, start, c["a"], step))
            elif pieces:
                # 起跳点紧贴上一段端点：把上一段端点当成起跳点
                pass
            start = c["b"]
        if start <= len(seg) - 1:
            pieces.append(_piece(seg, feet, start, len(seg) - 1, step))
        # links
        for c in cuts:
            a_i, b_i = c["a"], c["b"]
            A = (seg[a_i]["x"], feet[a_i], seg[a_i]["z"])
            B = (seg[b_i]["x"], feet[b_i], seg[b_i]["z"])
            h = math.hypot(B[0] - A[0], B[2] - A[2])
            if c["kind"] == "jump":
                out["jumps"].append({"a": A, "b": B, "h": h, "rise": c.get("rise", 0.0)})
                out["links"].append({"kind": "jump", "a": A, "b": B, "h": h})
            else:
                drop = c.get("drop", 0.0)
                out["drops"].append({"a": A, "b": B, "drop": drop,
                                     "hurt": drop >= DROP_HURT})
                out["links"].append({"kind": "drop", "a": A, "b": B, "h": h})
        out["pieces"].extend(pieces)
        out["crouches"].extend(_find_crouch(seg, sw))
        out["statics"].extend(_find_static(seg, sw))
    # ---- 岔路候选：2.5 m 内第二次经过，且中间绕了 8 m 以上 ----
    if sw["branch"]:
        flat = []
        for pi, piece in enumerate(out["pieces"]):
            for ni, p in enumerate(piece["nodes"]):
                flat.append((pi, ni, p))
        for i in range(len(flat)):
            for j in range(i + 3, len(flat)):
                if flat[j][0] != flat[i][0]:
                    continue
                if dist3(flat[i][2], flat[j][2]) <= BRANCH_NEAR:
                    gap = _route_len(out["pieces"][flat[i][0]]["nodes"], flat[i][1], flat[j][1])
                    if gap >= 8.0:
                        out["branches"].append({
                            "p": flat[i][2], "pi": flat[i][0], "ni": flat[i][1],
                            "gap": gap})
                        break
    # ---- 统计 ----
    nodes = sum(len(p["nodes"]) for p in out["pieces"])
    edges = sum(len(p["walk"]) for p in out["pieces"])
    long_edges = 0
    for piece in out["pieces"]:
        for i, j in piece["walk"]:
            if dist2(piece["nodes"][i], piece["nodes"][j]) > EDGE_MAX:
                long_edges += 1
    out["nodes"] = nodes
    out["edges"] = edges
    out["long_edges"] = long_edges
    out["ok"] = nodes >= 2
    if not out["ok"]:
        out["why"] = "重采样后不到 2 个节点：走得太短，或采样没进来"
    # ---- 问题清单 ----
    iss = out["issues"]
    if len(segs) > 1:
        iss.append("传送/换图断开 %d 段，段间不连边" % len(segs))
    if long_edges:
        iss.append("%d 条边长于 %.1f m：人机可能绕不过去" % (long_edges, EDGE_MAX))
    for d in out["drops"]:
        if d["hurt"]:
            iss.append("落差 %.1f m（> %.0f m）可能摔伤" % (d["drop"], DROP_HURT))
    if out["crouches"]:
        iss.append("%d 处蹲点：只提示，不落点" % len(out["crouches"]))
    if out["statics"]:
        iss.append("静止 %d 段：采样照常，没有多出来的节点" % len(out["statics"]))
    if out["branches"]:
        iss.append("%d 处岔路候选：保存时按双向边落" % len(out["branches"]))
    if out["jumps"]:
        for j in out["jumps"]:
            if j["h"] < JUMP_MIN_H:
                iss.append("跳链 %.1f m < %.1f m，未计入" % (j["h"], JUMP_MIN_H))
    return out


def summary(result):
    r"""一行字：时长 / 距离 / 节点 / 事件（控制台复盘标题用）。"""
    if not result or not result.get("ok"):
        return (result or {}).get("why") or "没有可复盘的数据"
    return ("%d 分 %02d 秒 · %.1f m · %d 节点 / %d 边 · 跳 %d / 落 %d / 岔 %d" % (
        int(result["duration"] // 60), int(result["duration"] % 60),
        result["dist"], result["nodes"], result["edges"],
        len(result["jumps"]), len(result["drops"]), len(result["branches"])))


def _fmt(p):
    return "%.3f %.3f %.3f" % (p[0], p[1], p[2])


def save_lines(result, allow_both=True):
    r"""复盘结果 -> 包 txt 的增量行（只增不覆盖；去重由调用方做）。

    走路的边双向；跳链 jump add + A→B；落下只 A→B。
    allow_both=True 时跳链/落下也补反向边（同一处能走回来）。
    """
    lines = []
    if not result or not result.get("ok"):
        return lines
    seen_nodes = set()

    def add_node(p):
        key = "%.2f|%.2f|%.2f" % (p[0], p[1], p[2])
        if key in seen_nodes:
            return
        seen_nodes.add(key)
        lines.append("node add " + _fmt(p))

    for piece in result["pieces"]:
        for p in piece["nodes"]:
            add_node(p)
    for piece in result["pieces"]:
        for i, j in piece["walk"]:
            a, b = piece["nodes"][i], piece["nodes"][j]
            lines.append("edge add %s %s" % (_fmt(a), _fmt(b)))
            lines.append("edge add %s %s" % (_fmt(b), _fmt(a)))
    for link in result["links"]:
        a, b = link["a"], link["b"]
        if link["kind"] == "jump":
            lines.append("jump add %s %s" % (_fmt(a), _fmt(b)))
        lines.append("edge add %s %s" % (_fmt(a), _fmt(b)))
        if allow_both:
            lines.append("edge add %s %s" % (_fmt(b), _fmt(a)))
    return lines


def dedupe_lines(lines, existing_text, near=0.35):
    r"""把增量行和包 txt 现有内容比对：节点/边落在 near 米内就不再写一遍。"""
    nodes = []
    edges = set()
    jumps = set()
    for raw in (existing_text or "").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        bits = s.split()
        if len(bits) >= 5 and bits[0] == "node" and bits[1] == "add":
            try:
                nodes.append((float(bits[2]), float(bits[3]), float(bits[4])))
            except ValueError:
                pass
        elif len(bits) >= 8 and bits[0] == "edge" and bits[1] in ("add", "out", "in"):
            try:
                a = (float(bits[2]), float(bits[3]), float(bits[4]))
                b = (float(bits[5]), float(bits[6]), float(bits[7]))
                edges.add(_edge_key(a, b))
            except ValueError:
                pass
        elif len(bits) >= 8 and bits[0] == "jump" and bits[1] == "add":
            try:
                a = (float(bits[2]), float(bits[3]), float(bits[4]))
                b = (float(bits[5]), float(bits[6]), float(bits[7]))
                jumps.add(_edge_key(a, b))
            except ValueError:
                pass
    out = []
    batch = []
    for ln in lines or []:
        bits = ln.split()
        if len(bits) >= 5 and bits[0] == "node" and bits[1] == "add":
            try:
                p = (float(bits[2]), float(bits[3]), float(bits[4]))
            except ValueError:
                continue
            if any(dist3(p, q) <= near for q in nodes + batch):
                continue
            batch.append(p)
            out.append(ln)
        elif len(bits) >= 5 and bits[0] == "jump" and bits[1] == "add":
            try:
                a = (float(bits[2]), float(bits[3]), float(bits[4]))
                b = (float(bits[5]), float(bits[6]), float(bits[7]))
            except (ValueError, IndexError):
                continue
            key = _edge_key(a, b)
            if key in jumps:
                continue
            jumps.add(key)
            out.append(ln)
        elif len(bits) >= 8 and bits[0] == "edge" and bits[1] == "add":
            try:
                a = (float(bits[2]), float(bits[3]), float(bits[4]))
                b = (float(bits[5]), float(bits[6]), float(bits[7]))
            except ValueError:
                continue
            key = _edge_key(a, b)
            if key in edges:
                continue
            edges.add(key)
            out.append(ln)
    return out


def _edge_key(a, b):
    return ("%.1f,%.1f,%.1f>%.1f,%.1f,%.1f"
            % (a[0], a[1], a[2], b[0], b[1], b[2]))