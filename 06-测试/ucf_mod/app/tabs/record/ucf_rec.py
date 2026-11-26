#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""录制轨迹的解析 / 重采样 / 事件识别 —— 控制台「录制」页只读这里。

数据来源（2026-11-24 起，和轨迹采集同一套 ucf-trace/2）：

    header {"kind":"rec","schema":"ucf-trace/2","hz":30,"t0":"...","src":"player",
            "fields":["t","dt","x","y","z","g","vy","sp","ct"]}
    样本   {"t":12.345,"dt":0.033,"x":-52.80,"y":-16.59,"z":3.63,
            "g":1,"vy":0.02,"sp":0,"ct":0}
           xyz = 玩家**脚底**世界坐标；g = 是否在地面；vy = 竖直速度
    跳事件 {"t":12.9,"ev":"jump","a":[起跳点],"b":[落点],"h":水平跳距,
            "rise":跳高,"air":滞空,"v0":起跳竖直速度,"run":起跳水平速度,
            "kind":"gap|mount|down|hop"}
           落地由插件按 isGrounded + 竖直速度结算，这里**不再猜**

识别规则（2026-11-24 按真实采集数据重做；改阈值只改下面常量）：

    跳链    插件给的 gap / mount 事件，**3D 长度 1.5~3.0 m** 才落链
            （游戏硬规则：两端 1 m 内吸附、两点之间要有 A->B 边、原生最长 2.91 m）。
            超长 / 太短的不建链，写进 issues —— 让人一眼看到「这一跳人机做不了」。
    落下    down 事件（落点比起点低 >= 2 m）-> 单向边，不建跳链。
    岔路    2.5 m 内第二次经过 -> 标黄候选（保存仍按双向边）。
    静止    2 s 没位移 -> 复盘里写一句，不影响节点。
    蹲点    **不再识别**（2026-11-24 用户要求删除：没用）。
    传送    **不再单独断段**（同上）；只把单帧位移 > 15 m 的那条边跳过。

只做纯计算（不读文件、不碰 tkinter），tests/test_ucf_rec.py 可以离线跑。
"""
import json
import math

# ---- 阈值（改这里；控制台「录制」页的说明文字按这几行写）----
LINK_MIN = 1.5        # 游戏跳链最短 3D 长度（再短人机就「原地跳」）
# 游戏跳链最长 3D 长度。
# 2026-11-26 实测（风暴 10 Hz 人机录制）：人机在 9 m/s 助跑下真的跨过了 5.22 m 的链，
# 一路连跳到 13.99；原生 41 条最长 2.91 m 只是作者摆得短，不是引擎上限。
LINK_MAX = 5.5
LINK_MAX_LONG = 6.0   # 「超长跳也建链」打开时的上限：只给实测用，不确定人机真能跳
# 连续两跳合并（落点 = 下一起点）后的上限：固定 3.0，不跟着 LINK_MAX 放宽。
# 理由：合并会把「两次 2.5 m 的小跳」接成一条 4~5 m 的链，人机只会跳一次 —— 危险。
MERGE_MAX_L3 = 3.0
RISE_TYP = (1.2, 2.6)  # 常规跳高（实测 1.2~2.3；游戏 JumpPower=10.5 决定约 1.9 m）
DROP_MIN = 2.0        # down 事件落点低多少算「落下」
BRANCH_NEAR = 2.5     # 2.5 m 内第二次经过 = 岔路候选
STATIC_TIME = 2.0     # 2 s 没位移
WARP_STEP = 15.0      # 单帧位移 > 15 m：这一条边不建（不猜传送，也不断段）
EDGE_MAX = 4.6        # 边长超过这个值在复盘里标出来
NODE_MIN_GAP = 0.60   # 重采样后两个节点至少隔这么远
MERGE_NEAR = 1.05     # 同层两个节点近于这个距离就合并。**必须略大于游戏的吸附半径 1 m**：
                      # 否则 1 m 内有两个路点时，路径排到哪个、跳链挂到哪个可能不是同一个，
                      # 人机就会在两点之间来回转头（2026-11-24 现场）
CHAIN_NEAR = 1.5      # 上一跳落点 B 与下一跳起点 A 的水平距离 ≤ 这个值：合并成同一个点
CHAIN_DY = 0.5        # 上面那条的高差上限；超过说明不在同一层，不合并
CORNER_DEG = 55.0     # 转角超过 55° 强制补一个节点
CORNER_REACH = 1.20   # 判断转角时前后各看 1.2 m

SWITCHES = (
    ("jump",   "自动识别跳跃 / 跳上高台",
     "插件结算的跳事件；3D 长度 1.5~3.0 m 才建跳链，超出的只标出来"),
    ("drop",   "自动识别落下",
     "落点比起点低 >= 2 m -> 单向边（不建跳链）"),
    ("branch", "自动识别岔路",
     "2.5 m 内第二次经过 -> 标黄待确认"),
    ("static", "静止提示",
     "2 s 没位移 -> 复盘里写一句，不加节点"),
    ("long_jump", "超长跳也建链（实测用）",
     "5.5~6 m 的跳也生成 jump；人机能不能跳过去得进游戏看，默认关"),
    ("need_speed", "跳链写助跑速度（实测用）",
     "needSpeed 写成录到的助跑速度（run），而不是 0；人机会不会因此先加速要进游戏验证"),
)
SW_DEFAULT = {key: True for key, _l, _d in SWITCHES}
# 「超长跳也建链」是实测开关，默认关：3 m 以上能不能跳过去还没验证过
SW_DEFAULT["long_jump"] = False
SW_DEFAULT["need_speed"] = False
# 采样间距：1.5 给窄道 / 拐角多的图，4 是默认。
# 2026-11-26 实测（风暴 50.9 m 轨迹）：2.5 m 时折线偏离真实脚步 p90 9 cm / 最大 40 cm，
# 1.5 m 时降到 p90 4.5 cm / 最大 25 cm，节点数 25 -> 35；再往下（<=1.05 m）会被
# MERGE_NEAR 去重半径吃成近点对（1.0 m 时 45 对），跳链端点也会被并到走路节点上，
# 所以 1.5 是给出的最细档，不要轻易再降。
STEP_OPTIONS = (1.5, 2.5, 4.0, 6.0)
STEP_DEFAULT = 4.0
# 2026-11-26：路点不再「每 step 米放一个」，改成「形状误差超过 DP_EPS 才放点」，
# 再用 step 当最大段长上限（3D 距离）。实测 09:07 风暴：46 点 / 最大偏差 0.25 m
# → DP ε=0.10 + 2.5 m 上限是 34 点 / 最大偏差 0.088 m。
DP_EPS = 0.10
COVER_R = 2.5     # 轨迹覆盖率：走路的采样点到最近节点 <= 这个距离算「覆盖到了」

KIND_CN = {"gap": "跨缺口", "mount": "跳上高台", "down": "跳下", "hop": "原地小跳"}


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


# ---------------------------------------------------------------- 解析
def parse_lines(lines):
    r"""jsonl 行 -> 样本列表（按 t 排序；坏行跳过）。兼容 1 版（只有相机坐标）。"""
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
        if d.get("k") == "b":          # 人机样本：走 parse_bots，不混进玩家轨迹
            continue
        try:
            out.append({
                "t": float(d.get("t") or 0.0),
                "dt": float(d.get("dt") or 0.0),
                "x": float(d["x"]), "y": float(d["y"]), "z": float(d["z"]),
                "g": None if d.get("g") is None else int(d["g"]),
                "vy": None if d.get("vy") is None else float(d["vy"]),
                "gy": None if d.get("gy") is None else float(d["gy"]),
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


def parse_events(lines):
    r"""jsonl 行 -> 插件结算的跳事件（按 t 排序）。"""
    out = []
    for raw in lines:
        s = (raw or "").strip()
        if not s.startswith("{"):
            continue
        try:
            d = json.loads(s)
        except ValueError:
            continue
        if not isinstance(d, dict) or d.get("ev") != "jump":
            continue
        try:
            a, b = d["a"], d["b"]
            out.append({
                "t": float(d.get("t") or 0.0),
                "a": (float(a[0]), float(a[1]), float(a[2])),
                "b": (float(b[0]), float(b[1]), float(b[2])),
                "h": float(d.get("h") or 0.0),
                "rise": float(d.get("rise") or 0.0),
                "air": float(d.get("air") or 0.0),
                "v0": float(d.get("v0") or 0.0),
                "run": float(d.get("run") or 0.0),
                "kind": str(d.get("kind") or ""),
            })
        except (KeyError, TypeError, ValueError, IndexError):
            continue
    out.sort(key=lambda e: e["t"])
    return out


def parse_rec(lines):
    r"""一次读全套：-> (样本, 跳事件)。控制台录制页用这个。"""
    lines = list(lines)
    return parse_lines(lines), parse_events(lines)


def parse_bots(lines):
    r"""人机样本（k="b"）-> 按 id 分组的列表。

    2026-11-26 起录制可以选「人机 / 全部」，每台 10 Hz 一行：
    t / id / xyz / g / vy / spd / j(空中) / en(有敌人) / act(行为名|分隔) / tgt(闲逛目标)。
    """
    out = {}
    for raw in lines or []:
        s = (raw or "").strip()
        if not s or s[0] != "{" or '"k":"b"' not in s:
            continue
        try:
            d = json.loads(s)
        except ValueError:
            continue
        try:
            bid = str(d.get("id") or "?")
            out.setdefault(bid, []).append({
                "t": float(d.get("t") or 0.0),
                "x": float(d["x"]), "y": float(d["y"]), "z": float(d["z"]),
                "g": int(d.get("g", -1)), "vy": float(d.get("vy") or 0.0),
                "spd": float(d.get("spd") or 0.0), "j": int(d.get("j") or 0),
                "en": int(d.get("en") or 0), "act": str(d.get("act") or ""),
                "tgt": list(d.get("tgt") or (0, 0, 0)),
            })
        except (TypeError, ValueError, KeyError):
            continue
    for v in out.values():
        v.sort(key=lambda s: s["t"])
    return out


def _grounded(s):
    if s.get("g") is not None:
        return s["g"] == 1
    return True          # 1 版没有 g：整条都当走路（只在读旧文件时退化）


def _eye_base(samples):
    gaps = []
    for s in samples:
        gy = s.get("gy")
        if gy is not None and gy > -1000.0:
            g = s["y"] - gy
            if 0.6 <= g <= 3.0:
                gaps.append(g)
    if not gaps:
        return None
    gaps.sort()
    return gaps[len(gaps) // 2]


def detect_events(samples):
    r"""没有事件行时的兜底识别（读旧文件 / 插件没结算时）。

    2 版：用 vy > 5 m/s 起跳 + 落地（g 由假变真）复算；
    1 版：只有相机 y，用竖直速度 + 连续 3 帧速度≈0 估落地。
    """
    if len(samples) < 6:
        return []
    eye = _eye_base(samples)
    out = []
    i = 1
    while i < len(samples) - 3:
        dt = samples[i]["t"] - samples[i - 1]["t"]
        if dt <= 0.0005:
            i += 1
            continue
        v = samples[i].get("vy")
        if v is None or abs(v) < 0.01:
            v = (samples[i]["y"] - samples[i - 1]["y"]) / dt
        if v <= 5.0:
            i += 1
            continue
        k = i
        apex = samples[i]["y"]
        while k + 1 < len(samples):
            vy = samples[k + 1].get("vy")
            if vy is None:
                d = samples[k + 1]["t"] - samples[k]["t"]
                vy = (samples[k + 1]["y"] - samples[k]["y"]) / d if d > 0.0005 else 0.0
            k += 1
            apex = max(apex, samples[k]["y"])
            if _grounded(samples[k]) and (samples[k]["t"] - samples[i]["t"]) > 0.06:
                break
            if samples[k]["t"] - samples[i]["t"] > 3.0:
                break
        A, B = samples[i - 1], samples[k]
        h = math.hypot(B["x"] - A["x"], B["z"] - A["z"])
        dy = B["y"] - A["y"]
        if h < 0.5:
            kind = "hop"
        elif dy > 0.5:
            kind = "mount"
        elif dy < -0.5:
            kind = "down"
        else:
            kind = "gap"
        out.append({"t": B["t"], "a": (A["x"], A["y"], A["z"]), "b": (B["x"], B["y"], B["z"]),
                    "h": h, "rise": apex - A["y"], "air": B["t"] - A["t"],
                    "v0": v, "run": 0.0, "kind": kind, "est": True})
        i = k + 1
    return out


# ---------------------------------------------------------------- 几何
def _resample(pts, step, forced):
    r"""按 step 重采样；forced 里的点（转角/端点）一定落成节点。"""
    nodes = [pts[0]]
    acc = 0.0
    prev = pts[0]
    for i in range(1, len(pts)):
        b = pts[i]
        seg = dist2(prev, b)              # 只用「上一个样本 → 这个样本」的增量
        while seg > 1e-6 and acc + seg >= step:
            need = step - acc
            t = need / seg
            p = (prev[0] + (b[0] - prev[0]) * t, prev[1] + (b[1] - prev[1]) * t,
                 prev[2] + (b[2] - prev[2]) * t)
            nodes.append(p)
            prev = p
            seg = dist2(prev, b)
            acc = 0.0
        acc += seg
        prev = b
        if i in forced and dist2(nodes[-1], b) >= NODE_MIN_GAP:
            nodes.append(b)
            acc = 0.0
    if dist2(nodes[-1], pts[-1]) > 0.05:
        nodes.append(pts[-1])
    out = [nodes[0]]
    for k in range(1, len(nodes)):
        p = nodes[k]
        last = k == len(nodes) - 1
        if dist2(out[-1], p) < NODE_MIN_GAP * 0.5 and not last:
            continue
        out.append(p)
    return out


def _corner_index(pts):
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
        cosv = max(-1.0, min(1.0, (v1[0] * v2[0] + v1[1] * v2[1]) / (n1 * n2)))
        if math.degrees(math.acos(cosv)) > CORNER_DEG:
            out.add(i)
    return out


def _seg_dev(p, a, b):
    r"""点到 3D 线段 ab 的距离（用来判断这段直线能不能代表轨迹）。"""
    ax, ay, az = a
    dx, dy, dz = b[0] - ax, b[1] - ay, b[2] - az
    L2 = dx * dx + dy * dy + dz * dz
    if L2 < 1e-12:
        return dist3(p, a)
    t = ((p[0] - ax) * dx + (p[1] - ay) * dy + (p[2] - az) * dz) / L2
    t = max(0.0, min(1.0, t))
    return dist3(p, (ax + dx * t, ay + dy * t, az + dz * t))


def _dp_simplify(points, eps=DP_EPS):
    r"""Douglas–Peucker：折线偏离真实轨迹超过 eps 才保留拐点。

    为什么不用「每 N 米放一个」：距离法在缓弯处切角（实测最大 0.25 m）、
    在斜坡上会把 3D 间距拉长；误差上限也没法保证。
    DP 的是「离这条直线最远的点」，天然把拐点留在节点上，
    直线段一个多余的点都不放，误差有硬上限。
    """
    n = len(points)
    if n <= 2:
        return list(points)
    keep = {0, n - 1}
    stack = [(0, n - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        a, b = points[i], points[j]
        best, bi = -1.0, -1
        for k in range(i + 1, j):
            d = _seg_dev(points[k], a, b)
            if d > best:
                best, bi = d, k
        if best > eps:
            keep.add(bi)
            stack.append((i, bi))
            stack.append((bi, j))
    return [points[k] for k in sorted(keep)]


def _cap_segments(nodes, maxlen):
    r"""把长于 maxlen 的段等分（用人机侧希望每段都别太长）。按 3D 长度算。"""
    if not nodes or maxlen <= 0:
        return list(nodes)
    out = [nodes[0]]
    for p in nodes[1:]:
        a = out[-1]
        d = dist3(a, p)
        if d > maxlen:
            k = int(math.ceil(d / maxlen))
            for m in range(1, k):
                t = m / float(k)
                out.append((a[0] + (p[0] - a[0]) * t,
                            a[1] + (p[1] - a[1]) * t,
                            a[2] + (p[2] - a[2]) * t))
        out.append(p)
    return out


def _piece(points, step):
    r"""一段连续走路 -> 节点链 + 双向边（DP 形状误差 + 最大段长）。"""
    if len(points) < 2:
        return {"nodes": list(points), "walk": [], "from": 0, "to": 0}
    nodes = _dp_simplify(points, DP_EPS)
    nodes = _cap_segments(nodes, max(0.5, float(step)))
    out = [nodes[0]]
    for p in nodes[1:]:
        if dist3(out[-1], p) < 0.30:      # 极近的点会让人机来回转头
            continue
        out.append(p)
    walk = [(i, i + 1) for i in range(len(out) - 1)
            if dist2(out[i], out[i + 1]) >= 0.30]
    return {"nodes": out, "walk": walk, "from": 0, "to": 0}


def _merge_nodes(pieces, links, drops, near=MERGE_NEAR, max_dy=0.5, lmax=LINK_MAX):
    r"""把靠得太近的节点合并成一个。

    为什么必须合并：游戏的跳链是**按「最近的路点」吸附**的（吸附半径 1 m），
    1 m 内有两个路点时，路径排到哪个、跳链挂在哪个，就可能不是同一个 ——
    人机表现为「走到跳点来回转头、不跳」。录制里「落点」和「下一跳起点」
    往往只隔 0.5~0.7 m，就是最典型的例子。

    2026-11-26 跳点保护：人机真正的起跳点常常离最近的路点 0.4~0.7 m，
    以前会被吸过去 —— 3.00 m 的跳吸成 3.50 m、2.82 m 吸成 3.29 m，
    超过游戏 1.5~3.0 m 的窗口就整条丢掉（08:48 风暴：4 跳只活了 1 条）。
    现在的规则：
      * 每一个「录到时本来就合格」的跳，两端坐标原样保留（不吸）；
      * 附近的走路节点反过来并到精确跳点上（路径仍然经过它）；
      * 两个精确跳点互相靠得近时不合并，留给 analyse 报一句警告。
    不合格的跳（例如 4.16 m）不保护，照旧合并 / 丢弃。
    """
    def find_in(kept, p):
        best, bd = None, near
        for q in kept:
            if abs(q[1] - p[1]) > max_dy:
                continue
            d = dist3(q, p)
            if d <= bd:
                bd, best = d, q
        return best

    def build(protected):
        kept = list(protected)
        out = []
        for piece in pieces:
            nodes = []
            for p in piece["nodes"]:
                q = find_in(kept, p)
                if q is None:
                    kept.append(p)
                    nodes.append(p)
                elif not nodes or nodes[-1] != q:
                    nodes.append(q)
            if not nodes:
                continue
            walk = [(i, i + 1) for i in range(len(nodes) - 1)
                    if dist2(nodes[i], nodes[i + 1]) >= 0.30]
            out.append({"nodes": nodes, "walk": walk, "from": 0, "to": 0})
        return kept, out

    # 录到时本来就在 1.5~3.0 窗口里的跳，两端原样保留（后面的去重也不再吸）。
    # 不合格的跳（例如 4.16 m）不保护，照旧合并、最后由窗口过滤掉。
    prot = []
    for ln in links:
        if not (LINK_MIN <= dist3(ln["a"], ln["b"]) <= lmax):
            continue
        for p in (ln["a"], ln["b"]):
            if not any(dist3(p, q) <= 1e-3 for q in prot):
                prot.append(p)
    kept, new_pieces = build(prot)

    def snap(p):
        q = find_in(kept, p)
        return q if q is not None else p

    for ln in links:
        ln["a"], ln["b"] = snap(ln["a"]), snap(ln["b"])
        ln["l3"] = dist3(ln["a"], ln["b"])
        ln["h"] = dist2(ln["a"], ln["b"])
    for d in drops:
        d["a"], d["b"] = snap(d["a"]), snap(d["b"])
    return new_pieces


def _find_falls(samples, walk_mask):
    r"""「离地 → 落到更低的平面」但**没有跳事件**的段落（走下落差）。

    2026-11-24：这类段落以前完全没记录，前后两段走路链就断在那儿了
    （地道口跳下去、从箱子上跳出来都是这种）。这里补一条**单向落地边**。
    """
    out = []
    n = len(samples)
    i = 0
    while i < n:
        if walk_mask[i]:
            i += 1
            continue
        j = i
        while j < n and not walk_mask[j]:
            j += 1
        if i > 0 and j < n:
            a, b = samples[i - 1], samples[j]
            drop = a["y"] - b["y"]
            if drop >= DROP_MIN:
                out.append({"t": b["t"], "a": (a["x"], a["y"], a["z"]),
                            "b": (b["x"], b["y"], b["z"]), "drop": drop,
                            "hurt": drop >= 6.0, "kind": "fall"})
        i = j
    return out


def _static_spans(samples, sw):
    out = []
    if not sw["static"]:
        return out
    n = len(samples)
    i = 0
    while i < n:
        j = i
        while j + 1 < n:
            if math.hypot(samples[j + 1]["x"] - samples[j]["x"],
                          samples[j + 1]["z"] - samples[j]["z"]) > 0.06:
                break
            j += 1
        dur = samples[j]["t"] - samples[i]["t"]
        if dur >= STATIC_TIME:
            out.append({"p": (samples[i]["x"], samples[i]["y"], samples[i]["z"]), "t": dur})
        i = j + 1
    return out


def _route_len(nodes, i, j):
    total = 0.0
    for k in range(i, j):
        total += dist2(nodes[k], nodes[k + 1])
    return total


def _walk_mask(samples, events):
  r"""哪些样本算「在地上走路」。

  插件给的 g 是权威的，但相机兜底模式下射线会偶尔打空（站在台阶边/斜坡上），
  短暂的地面丢失如果当成空中，走路链会被切成好几段、人机走不过去。
  所以：**不在任何跳事件时间窗内、且丢地不超过 0.25 s** 的片段补回走路。
  """
  n = len(samples)
  spans = []
  for e in events or []:
    air = float(e.get("air") or 0.0)
    if air > 0.0:
      spans.append((e["t"] - air - 0.10, e["t"] + 0.10))
  mask = [_grounded(s) for s in samples]
  i = 0
  while i < n:
    if mask[i]:
      i += 1
      continue
    j = i
    while j < n and not mask[j]:
      j += 1
    dur = (samples[j - 1]["t"] - samples[i]["t"]) if j > i else 0.0
    mid = samples[(i + j) // 2]["t"] if j > i else 0.0
    in_jump = any(a <= mid <= b for a, b in spans)
    if dur <= 0.25 and not in_jump:
      for k in range(i, j):
        mask[k] = True
    i = j
  return mask


# ---------------------------------------------------------------- 主分析
def analyse(samples, step=STEP_DEFAULT, sw=None, events=None):
    r"""轨迹 -> 走路节点链 + 跳链 + 落下 + 岔路 + 问题清单。

    events 给了就用插件结算的（准），没给才用 detect_events 兜底。
    """
    sw = norm_switch(sw)
    step = float(step or STEP_DEFAULT)
    lmax = LINK_MAX_LONG if sw.get("long_jump") else LINK_MAX
    out = {
        "ok": False, "why": "", "step": step, "sw": sw,
        "samples": len(samples or []), "duration": 0.0, "dist": 0.0,
        "pieces": [], "links": [], "jumps": [], "drops": [], "branches": [],
        "crouches": [], "statics": [], "segments": 1, "issues": [],
        "skipped_jump": 0, "warp": 0, "nodes": 0, "edges": 0, "long_edges": 0,
        "links_bad": 0, "rise_typical": RISE_TYP, "est": False, "merged": 0,
    }
    samples = samples or []
    if len(samples) < 6:
        out["why"] = "样本太少（可能游戏没进图，或插件不是带录制接口的版本）"
        return out
    if events is None:
        events = detect_events(samples)
        out["est"] = True
    out["duration"] = samples[-1]["t"] - samples[0]["t"]
    for a, b in zip(samples, samples[1:]):
        step_len = math.hypot(b["x"] - a["x"], b["z"] - a["z"])
        if step_len <= WARP_STEP:
            out["dist"] += step_len
        else:
            out["warp"] += 1

    # ---- 走路段：把「在地面」的样本连成折线，空中不落点（短暂的射线打空会补回来）----
    walk_mask = _walk_mask(samples, events)
    runs = []
    cur = []
    for idx, s in enumerate(samples):
        if walk_mask[idx]:
            cur.append((s["x"], s["y"], s["z"]))
        elif cur:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)

    for pts in runs:
        piece = _piece(pts, step)
        if piece["nodes"]:
            out["pieces"].append(piece)

    # ---- 跳链 / 落下：直接用插件结算的事件 ----
    for e in events:
        a, b = e["a"], e["b"]
        l3 = dist3(a, b)
        dy = b[1] - a[1]
        rec = {"a": a, "b": b, "h": e["h"], "rise": e["rise"], "air": e["air"],
               "v0": e["v0"], "run": e["run"], "kind": e["kind"], "l3": l3,
               "est": bool(e.get("est"))}
        if e["kind"] == "down":
            if not sw["drop"]:
                continue
            if -dy >= DROP_MIN:
                out["drops"].append(dict(rec, drop=-dy, hurt=(-dy) >= 6.0))
            continue
        if not sw["jump"]:
            continue
        if LINK_MIN <= l3 <= lmax:
            out["jumps"].append(rec)
            out["links"].append({"kind": "jump", "a": a, "b": b, "h": e["h"], "l3": l3})
        else:
            out["links_bad"] += 1
            why = "太短（< %.1f m）" % LINK_MIN if l3 < LINK_MIN else "太长（> %.1f m）" % lmax
            out["skipped_jump"] += 1
            out["issues"].append(
                "第 %.1f s 那一跳 %s：%s，3D %.2f m —— 人机用不了，没建跳链"
                % (e["t"], KIND_CN.get(e["kind"], e["kind"]), why, l3))

    # ---- 走下落差（没跳事件的离地）也要连上：单向落地边 ----
    if sw["drop"]:
        for d in _find_falls(samples, walk_mask):
            dup = any(dist3(d["a"], e["a"]) <= 1.0 and dist3(d["b"], e["b"]) <= 1.0
                      for e in out["drops"])
            if not dup:
                out["drops"].append(d)

    # ---- 合并靠得太近的节点（1 m 内两个路点会抢吸附，人机会在原地打转）----
    before = sum(len(p["nodes"]) for p in out["pieces"])
    out["pieces"] = _merge_nodes(out["pieces"], out["jumps"], out["drops"], lmax=lmax)
    out["merged"] = max(0, before - sum(len(p["nodes"]) for p in out["pieces"]))

    # ---- 连续跳链：上一跳的落点 = 下一跳的起点（2026-11-25）----
    # 分开成两个点时，人机落在两点之间的台阶/栏杆上就既不在起点（JumpCheck 不跳）、
    # 也回不到落点（被几何挡住），2026-11-25 运输船现场卡了 15 s+。
    chain_merged = 0
    for i in range(len(out["jumps"]) - 1):
        cur, nxt = out["jumps"][i], out["jumps"][i + 1]
        if abs(cur["b"][1] - nxt["a"][1]) > CHAIN_DY:
            continue
        if dist2(cur["b"], nxt["a"]) > CHAIN_NEAR:
            continue
        # 合并后下一跳不能超出 1.5~3.0 窗口，否则本来 2.5 m 的两跳会被接成 4 m
        new_l3 = dist3(cur["b"], nxt["b"])
        if not (LINK_MIN <= new_l3 <= MERGE_MAX_L3):
            continue
        nxt["a"] = cur["b"]
        nxt["l3"] = new_l3
        nxt["h"] = dist2(nxt["a"], nxt["b"])
        chain_merged += 1
    if chain_merged:
        out["issues"].append("%d 处「上一跳落点 / 下一跳起点」已合并成同一个路点" % chain_merged)

    # 合并后跳链长度可能变了一点，重新按窗口分一遍
    if out["jumps"]:
        keep = []
        for j in out["jumps"]:
            if LINK_MIN <= j["l3"] <= lmax:
                keep.append(j)
            else:
                out["links_bad"] += 1
                out["skipped_jump"] += 1
                out["issues"].append("合并后这一跳 3D %.2f m 超出 1.5~3.0，没建跳链" % j["l3"])
        out["jumps"] = keep
    out["links"] = [{"kind": "jump", "a": j["a"], "b": j["b"],
                     "h": j["h"], "l3": j["l3"],
                     "run": float(j.get("run") or 0.0)} for j in out["jumps"]]

    # 2026-11-26：两跳的「落点 / 下一起点」靠得很近却没能合并，说明合并后会超过 3 m。
    # 各自保留精确点两条都能成立，但人机可能在这 0.5~1 m 之间来回转头 —— 提醒一句。
    for i in range(len(out["jumps"]) - 1):
        cur, nxt = out["jumps"][i], out["jumps"][i + 1]
        gap = dist2(cur["b"], nxt["a"])
        if 0.30 <= gap < MERGE_NEAR and abs(cur["b"][1] - nxt["a"][1]) <= CHAIN_DY:
            out["issues"].append(
                "第 %d / %d 跳的落点与下一起点只隔 %.2f m（< %.2f m）：已各自保留精确点，"
                "人机若在这里来回转头，重录时跳完先走开 1.5 m 再跳"
                % (i + 1, i + 2, gap, MERGE_NEAR))

    # ---- 断口：相邻两段路之间没有跳链/落地边接上（人机会停在这里）----
    out["gaps"] = []
    ends = [(tuple(j["a"]), tuple(j["b"])) for j in out["jumps"]] + \
           [(tuple(d["a"]), tuple(d["b"])) for d in out["drops"]]

    def linked(a, b):
        r"""从 a 出发沿跳链/落地边最多走 8 步，能不能到 b 附近。

        连续两跳（落地就是下一跳起点）时，单条 link 盖不住整段，
        以前会误报断口；这里按链走一遍。
        """
        stack = [y for x, y in ends if dist3(a, x) <= 1.2]
        seen = 0
        while stack and seen < 8:
            p = stack.pop()
            seen += 1
            if dist3(p, b) <= 1.2:
                return True
            for x, y in ends:
                if dist3(p, x) <= 1.2:
                    stack.append(y)
        return False

    for i in range(len(out["pieces"]) - 1):
        a = out["pieces"][i]["nodes"][-1]
        b = out["pieces"][i + 1]["nodes"][0]
        if dist3(a, b) <= 0.60:
            continue
        if not linked(a, b):
            out["gaps"].append({"a": a, "b": b, "d": dist3(a, b)})

    # ---- 连通性：孤儿点（没有边的节点）+ 轨迹覆盖率 ----
    used = set()
    for pc in out["pieces"]:
        for i, j in pc["walk"]:
            used.add(tuple(pc["nodes"][i]))
            used.add(tuple(pc["nodes"][j]))
    for j in out["jumps"]:
        used.add(tuple(j["a"]))
        used.add(tuple(j["b"]))
    for d in out["drops"]:
        used.add(tuple(d["a"]))
        used.add(tuple(d["b"]))
    all_nodes = [tuple(n) for pc in out["pieces"] for n in pc["nodes"]]
    out["orphans"] = [n for n in all_nodes if n not in used]
    walk_pts = [(s["x"], s["y"], s["z"]) for i, s in enumerate(samples) if walk_mask[i]]
    hit, worst = 0, 0.0
    for p in walk_pts:
        d = min((dist3(p, n) for n in all_nodes), default=1e9)
        if d <= COVER_R:
            hit += 1
        elif d < 1e8:
            worst = max(worst, d)
    out["coverage"] = (100.0 * hit / len(walk_pts)) if walk_pts else 100.0
    out["cover_worst"] = worst
    # 孤立点对人是没用的（写进包里也只是个摆设），直接从路点里去掉；
    # 典型来源：录完一跳立刻按停止，落地后只有 1 个样本 -> 1 个节点 0 条边。
    if out["orphans"]:
        out["pieces"] = [pc for pc in out["pieces"]
                         if len(pc["nodes"]) >= 2 and pc["walk"]]
        out["orphan_dropped"] = len(out["orphans"])
        out["orphans"] = []

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
                        out["branches"].append({"p": flat[i][2], "pi": flat[i][0],
                                                "ni": flat[i][1], "gap": gap})
                        break

    out["statics"] = _static_spans(samples, sw)

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

    iss = out["issues"]
    if out.get("orphan_dropped"):
        iss.append("丢掉 %d 个孤立点（没有边，人机走不到；录完一跳马上停、落地只有 1 个样本时会出现）"
                   % out["orphan_dropped"])
    if out["coverage"] < 95.0:
        iss.append("轨迹覆盖率 %.0f%%：最远有 %.1f m 的地方没有节点（人机会绕开或卡住）"
                   % (out["coverage"], out["cover_worst"]))
    if out["gaps"]:
        iss.append("路线在 %d 处断开（%s）：这里没有人机可用的跳链或边，"
                   "要么把跳分成两跳，要么打开「超长跳也建链」实测"
                   % (len(out["gaps"]),
                      " / ".join("%.1f m" % g["d"] for g in out["gaps"])))
    if long_edges:
        iss.append("%d 条边长于 %.1f m：人机可能绕不过去" % (long_edges, EDGE_MAX))
    for d in out["drops"]:
        if d["hurt"]:
            iss.append("落差 %.1f m（> 6 m）可能摔伤" % d["drop"])
    if out["statics"]:
        iss.append("静止 %d 段：采样照常，没有多出来的节点" % len(out["statics"]))
    if out["branches"]:
        iss.append("%d 处岔路候选：保存时按双向边落" % len(out["branches"]))
    lo, hi = RISE_TYP
    odd = [j for j in out["jumps"] if not (lo <= j["rise"] <= hi)]
    if odd:
        iss.append("%d 跳的跳高不在常规值 %.1f~%.1f m（可能有台阶/斜坡混进来）"
                   % (len(odd), lo, hi))
    return out


def summary(result):
    r"""一行字：时长 / 距离 / 节点 / 事件（控制台复盘标题用）。"""
    if not result or not result.get("ok"):
        return (result or {}).get("why") or "没有可复盘的数据"
    gaps = len(result.get("gaps") or [])
    orphans = len(result.get("orphans") or [])
    return ("%d 分 %02d 秒 · %.1f m · %d 节点 / %d 边 · 跳链 %d（没用 %d）/ 落 %d / 岔 %d%s%s%s" % (
        int(result["duration"] // 60), int(result["duration"] % 60),
        result["dist"], result["nodes"], result["edges"],
        len(result["jumps"]), result.get("links_bad", 0),
        len(result["drops"]), len(result["branches"]),
        (" · 断口 %d" % gaps) if gaps else "",
        " · 覆盖 %.0f%%" % result.get("coverage", 100.0),
        (" · 孤儿 %d" % orphans) if orphans else ""))


def _fmt(p):
    return "%.3f %.3f %.3f" % (p[0], p[1], p[2])


def save_lines(result, allow_both=True):
    r"""复盘结果 -> 包 txt 的增量行（只增不覆盖；去重由调用方做）。

    走路的边双向；跳链 = jump add + A->B（参数固定 0 / 0.5，和竞技场原生跳链一致）；
    落下只 A->B。只有通过 3D 1.5~3.0 体检的跳才会写进来（超长的已经在 issues 里）。
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
        add_node(a)
        add_node(b)
        if link["kind"] == "jump":
            # 和竞技场原生跳链一致：accuracy=0.5（朝向阈值降到 0，只有反向走才会失败）
            # needSpeed：默认 0 = 不要求助跑速度；打开「跳链写助跑速度」后写录到的 run，
            # 让游戏自己去卡「够快才起跳」（语义未逆证，属于实测开关）。
            need = 0.0
            if (result.get("sw") or {}).get("need_speed"):
                need = max(0.0, min(9.9, round(float(link.get("run") or 0.0), 1)))
            lines.append("jump add %s %s %.1f 0.5 0" % (_fmt(a), _fmt(b), need))
        lines.append("edge add %s %s" % (_fmt(a), _fmt(b)))
        if allow_both:
            lines.append("edge add %s %s" % (_fmt(b), _fmt(a)))
    # 高处落地：只写 A->B 的**单向**边（人机走过去自然掉下去，不需要跳链）
    for d in result.get("drops") or []:
        a, b = d["a"], d["b"]
        add_node(a)
        add_node(b)
        lines.append("edge add %s %s" % (_fmt(a), _fmt(b)))
    return lines


def dedupe_lines(lines, existing_text, near=MERGE_NEAR):
    r"""把增量行和包 txt 现有内容比对：节点落在 near 米内就不再写一遍。

    2026-11-25：near 从 0.35 提到 MERGE_NEAR（1.05）。跨次录制时只按 0.35 去重，
    第二次沿同一条路录会在 0.5~1.5 m 处生成近点（抢吸附）。提高去重半径的同时，
    被去掉的节点坐标会被**改写到保留下来的节点**上，边 / 跳链一起改写，
    否则端点对不上（插件按 0.35 m 找点），边会被静默丢掉。
    """
    nodes, edges, jumps = [], set(), set()
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
                edges.add(_edge_key((float(bits[2]), float(bits[3]), float(bits[4])),
                                    (float(bits[5]), float(bits[6]), float(bits[7]))))
            except ValueError:
                pass
        elif len(bits) >= 8 and bits[0] == "jump" and bits[1] == "add":
            try:
                jumps.add(_edge_key((float(bits[2]), float(bits[3]), float(bits[4])),
                                    (float(bits[5]), float(bits[6]), float(bits[7]))))
            except ValueError:
                pass

    out = []
    batch = []
    snap = {}

    def node_key(p):
        return (round(p[0], 3), round(p[1], 3), round(p[2], 3))

    def nearest(q):
        best, bd = None, near
        for r in nodes + batch:
            d = dist3(q, r)
            if d <= bd:
                bd, best = d, r
        return best

    # 2026-11-26：跳点端点原样保留。以前这里会把离已有节点 1.05 m 内的跳点
    # 吸过去，3.00 m 的跳变成 3.50 m 就废了（见 _merge_nodes 的说明）。
    keep_exact = set()
    for ln in lines or []:
        bits = ln.split()
        if len(bits) >= 8 and bits[0] == "jump" and bits[1] == "add":
            try:
                keep_exact.add(node_key((float(bits[2]), float(bits[3]), float(bits[4]))))
                keep_exact.add(node_key((float(bits[5]), float(bits[6]), float(bits[7]))))
            except ValueError:
                pass
    have = {node_key(r) for r in nodes}

    def snap_pt(q):
        if node_key(q) in keep_exact:
            return q
        if node_key(q) in snap:
            return snap[node_key(q)]
        r = nearest(q)
        return r if r is not None else q

    for ln in lines or []:
        bits = ln.split()
        if len(bits) >= 5 and bits[0] == "node" and bits[1] == "add":
            try:
                p = (float(bits[2]), float(bits[3]), float(bits[4]))
            except ValueError:
                continue
            k = node_key(p)
            if k in keep_exact:
                if k in have:
                    continue
                have.add(k)
                batch.append(p)
                out.append(ln)
                continue
            q = nearest(p)
            if q is not None:
                snap[k] = q
                continue
            batch.append(p)
            have.add(k)
            out.append(ln)
        elif len(bits) >= 5 and bits[0] == "jump" and bits[1] == "add":
            try:
                a = (float(bits[2]), float(bits[3]), float(bits[4]))
                b = (float(bits[5]), float(bits[6]), float(bits[7]))
            except (ValueError, IndexError):
                continue
            a, b = snap_pt(a), snap_pt(b)
            if dist3(a, b) < 0.3:
                continue
            key = _edge_key(a, b)
            if key in jumps:
                continue
            jumps.add(key)
            # 保留可选参数（needSpeed / accuracy / direction），只改写端点
            line = "jump add %s %s" % (_fmt(a), _fmt(b))
            if len(bits) > 8:
                line += " " + " ".join(bits[8:])
            out.append(line)
        elif len(bits) >= 8 and bits[0] == "edge" and bits[1] == "add":
            try:
                a = (float(bits[2]), float(bits[3]), float(bits[4]))
                b = (float(bits[5]), float(bits[6]), float(bits[7]))
            except ValueError:
                continue
            a, b = snap_pt(a), snap_pt(b)
            if dist3(a, b) < 0.3:
                continue
            key = _edge_key(a, b)
            if key in edges:
                continue
            edges.add(key)
            out.append("edge add %s %s" % (_fmt(a), _fmt(b)))
    return out


def _edge_key(a, b):
    return ("%.1f,%.1f,%.1f>%.1f,%.1f,%.1f"
            % (a[0], a[1], a[2], b[0], b[1], b[2]))
