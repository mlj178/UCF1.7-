#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""采样文件（ucf-trace/1·2·3）的唯一读取器 —— 「录制」和「原始轨迹采集」共用。

## 为什么有这个模块（2026-11-27）

录制 v2（2026-11-24）起，录制文件和采集文件就是**同一个格式**，但读取器各写了一份：
`app/tabs/dev/ucf_trace.py` 一份、`app/tabs/record/ucf_rec.py` 一份。两份的排序 /
去重 / 缺省 / header 判定都不一样 —— 同一份文件在两个页面可以给出不同的样本数。
现在解析只有这一份实现，两边都调它：

    ucf_trace.FIELDS / scan / read_full / read   → 这里（保留原名字）
    ucf_rec.parse_lines / parse_events / parse_bots → 这里（保留原名字）

## 文件长什么样

    第 1 行（header，第一个样本落盘时才写）
    {"kind":"rec"|"trace","schema":"ucf-trace/3","who":"player|bots|all","hz":30,
     "t0":"2026-11-27 12:00:00","scene":"...","map":"level1","label":"运输船",
     "pack":"...","fp":"...","src":"player|"camera",
     "fields":["t","dt","x","y","z","g","vy","sp","ct"], "notes":"...", "kind_note":"..."}

    玩家样本（每帧一行，键集合 = fields）
    {"t":12.345,"dt":0.033,"x":-52.80,"y":-16.59,"z":3.63,"g":1,"vy":0.02,"sp":0,"ct":0}

    人机样本（10 Hz，k="b"；只在 who=all|bots 时才有）
    {"t":12.4,"k":"b","id":"0a1b2c3d","x":..,"y":..,"z":..,"g":1,"vy":0.0,
     "spd":6.2,"j":0,"en":0,"act":"Move|Chase","tgt":[..],"njs":"..","near":"..","pts":12}

    跳事件（落地那一帧由插件结算） / 分段 / 场景 / 结束
    {"t":12.9,"ev":"jump","a":[..],"b":[..],"h":..,"rise":..,"air":..,"v0":..,"run":..,"kind":"mount"}
    {"t":12.3,"ev":"cam"} / {"t":12.3,"ev":"scene","n":"..."}
    {"end":1,"t":42.0,"n":1260,"dist":128.4,"missed":0,"ticks":1250,"jumps":4}

## 版本兼容

* ucf-trace/1（2026-11-21~23）：相机坐标 + gy + 相机朝向 + wasd；没有 g/vy/跳事件。
  字段缺就按缺省补，老日志照样能读、能出报告（报告里标「估算」）。
* ucf-trace/2（2026-11-24~27）：玩家脚底 + g/vy，插件结算 ev=jump。
* ucf-trace/3（2026-11-27）：和 2 版**样本行完全一样**，只是 header 多了 who
  （采集对象）并且 rec / trace 改成同一套采样器。读取不需要区分 2 和 3。

只做纯计算（不读 tkinter），tests/test_trace.py / tests/test_ucf_rec.py 可以离线跑。
"""
import json

#: 3 版样本字段 —— 必须和 editor.c 的 fields 数组一一对应（tests/test_trace.py 钉住）
FIELDS = ("t", "dt", "x", "y", "z", "g", "vy", "sp", "ct")

#: 1 版字段；只为读历史日志，新日志不会再用
FIELDS_V1 = ("t", "dt", "x", "y", "z", "gy", "fx", "fy", "fz",
             "sp", "ct", "sh", "w", "a", "s", "d")

#: 跳事件行里的键（和 editor.c 的 sess_jump_line 对齐）
JUMP_KEYS = ("a", "b", "h", "rise", "air", "v0", "run", "kind")

#: header 的 kind 取值 = 会话类型
KINDS = ("trace", "rec")

#: 已知 schema；读的时候只用来标「旧格式估算」，不拒绝未知版本
SCHEMAS = ("ucf-trace/1", "ucf-trace/2", "ucf-trace/3")

#: 同一个采样时刻附近两行算重复（插件不会写，人手工合并文件时会出现）
DUP_WINDOW = 0.002


def is_header(d):
    r"""header 行：有 kind（或 fields）、没有 x。1/2/3 版都适用。"""
    if not isinstance(d, dict) or "x" in d:
        return False
    return "kind" in d or "fields" in d


def is_bot(d):
    return isinstance(d, dict) and d.get("k") == "b"


def row(d):
    r"""一行 JSON -> 玩家样本 dict。缺的键按缺省补（1 版没有 g/vy，2 版没有 gy/fx...）。"""
    gy = d.get("gy")
    g = d.get("g")
    vy = d.get("vy")
    return {
        "t": float(d.get("t") or 0.0),
        "dt": float(d.get("dt") or 0.0),
        "x": float(d["x"]), "y": float(d["y"]), "z": float(d["z"]),
        "g": None if g is None else int(g),
        "vy": None if vy is None else float(vy),
        "gy": None if gy is None else float(gy),
        "fx": float(d.get("fx") or 0.0), "fy": float(d.get("fy") or 0.0),
        "fz": float(d.get("fz") or 0.0),
        "sp": int(d.get("sp") or 0), "ct": int(d.get("ct") or 0),
        "sh": int(d.get("sh") or 0),
        "w": int(d.get("w") or 0), "a": int(d.get("a") or 0),
        "s": int(d.get("s") or 0), "d": int(d.get("d") or 0),
    }


def jump(d):
    r"""一行 ev=jump -> 跳事件 dict；字段不全就返回 None（不抛）。"""
    try:
        a, b = d.get("a"), d.get("b")
        if not (isinstance(a, (list, tuple)) and isinstance(b, (list, tuple))):
            return None
        return {
            "t": float(d.get("t") or 0.0),
            "a": (float(a[0]), float(a[1]), float(a[2])),
            "b": (float(b[0]), float(b[1]), float(b[2])),
            "h": float(d.get("h") or 0.0),
            "rise": float(d.get("rise") or 0.0),
            "air": float(d.get("air") or 0.0),
            "v0": float(d.get("v0") or 0.0),
            "run": float(d.get("run") or 0.0),
            "kind": str(d.get("kind") or ""),
        }
    except (TypeError, ValueError, IndexError):
        return None


def bot_row(d):
    r"""一行 k="b" -> 人机样本 dict（键和 editor.c 的 sess_bot_line 对齐）。"""
    return {
        "t": float(d.get("t") or 0.0),
        "x": float(d["x"]), "y": float(d["y"]), "z": float(d["z"]),
        "g": int(d.get("g", -1)), "vy": float(d.get("vy") or 0.0),
        "spd": float(d.get("spd") or 0.0), "j": int(d.get("j") or 0),
        "en": int(d.get("en") or 0), "act": str(d.get("act") or ""),
        "tgt": list(d.get("tgt") or (0, 0, 0)),
        "njs": str(d.get("njs") or ""), "near": str(d.get("near") or ""),
        "pts": int(d.get("pts", -1)),
    }


# ---------------------------------------------------------------- 行级
def iter_objs(lines):
    r"""行 -> dict，坏行跳过（插件正在写的半行、编码问题都不抛）。"""
    for raw in lines:
        s = (raw or "").strip()
        if not s or s[0] != "{":
            continue
        try:
            d = json.loads(s)
        except ValueError:
            continue
        if isinstance(d, dict):
            yield d


def player_rows(lines):
    r"""玩家样本：按 t 排序，去掉 0.002 s 内的重复行（人机行不算）。"""
    out = []
    for d in iter_objs(lines):
        if "x" not in d or "ev" in d or is_bot(d) or is_header(d):
            continue
        try:
            out.append(row(d))
        except (TypeError, ValueError):
            continue
    out.sort(key=lambda s: s["t"])
    clean = []
    for s in out:
        if clean and abs(s["t"] - clean[-1]["t"]) < DUP_WINDOW:
            clean[-1] = s
        else:
            clean.append(s)
    return clean


def jump_rows(lines):
    r"""跳事件：按 t 排序。"""
    out = []
    for d in iter_objs(lines):
        if d.get("ev") != "jump":
            continue
        j = jump(d)
        if j:
            out.append(j)
    out.sort(key=lambda e: e["t"])
    return out


def bots_by_id(lines):
    r"""人机样本：按 id 分组、组内按 t 排序。"""
    out = {}
    for d in iter_objs(lines):
        if not is_bot(d):
            continue
        try:
            bid = str(d.get("id") or "?")
            out.setdefault(bid, []).append(bot_row(d))
        except (TypeError, ValueError, KeyError):
            continue
    for v in out.values():
        v.sort(key=lambda s: s["t"])
    return out


# ---------------------------------------------------------------- 文件级
def split_file(path):
    r"""整个文件 -> (header, 玩家样本, 跳事件, 人机样本, end 行)。"""
    hdr, end = {}, None
    rows, jumps, bots = [], [], []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.readlines()
    for d in iter_objs(lines):
        if d.get("end"):
            end = d
        elif d.get("ev") == "jump":
            j = jump(d)
            if j:
                jumps.append(j)
        elif is_header(d):
            hdr = d
        elif is_bot(d):
            try:
                bots.append(dict(bot_row(d), id=str(d.get("id") or "?")))
            except (TypeError, ValueError, KeyError):
                pass
        elif "x" in d and "ev" not in d:
            try:
                rows.append(row(d))
            except (TypeError, ValueError):
                pass
    rows.sort(key=lambda s: s["t"])
    clean = []
    for s in rows:
        if clean and abs(s["t"] - clean[-1]["t"]) < DUP_WINDOW:
            clean[-1] = s
        else:
            clean.append(s)
    jumps.sort(key=lambda e: e["t"])
    return hdr, clean, jumps, bots, end


def read_full(path):
    r"""整个文件 -> (header, 样本列表, 跳事件列表, end 行)。老接口，测试和报告都用它。"""
    hdr, rows, jumps, _bots, end = split_file(path)
    return hdr, rows, jumps, end


def read(path):
    r"""整个文件 -> (header, 样本列表, end 行) —— 不要跳事件时用它。"""
    hdr, rows, _jumps, _bots, end = split_file(path)
    return hdr, rows, end


def scan(path, offset=0):
    r"""从 offset 往后读新写完的行（控制台 0.5 s 一次，不重读整个文件）。

    返回 (新 offset, 新样本数, 最后一个样本, end 行或 None)。
    只处理以换行结尾的行：插件正在写的那一行留到下次。
    人机行 / 事件行 / header 都不算进样本数（控制台的「样本数 / 实测 Hz」只按玩家算）。
    """
    try:
        with open(path, "rb") as f:
            f.seek(offset)
            blob = f.read()
    except OSError:
        return offset, 0, None, None
    cut = blob.rfind(b"\n")
    if cut < 0:
        return offset, 0, None, None
    chunk = blob[:cut + 1]
    new_off = offset + len(chunk)
    count, last, end = 0, None, None
    for raw in chunk.split(b"\n"):
        s = raw.strip()
        if not s or not s.startswith(b"{"):
            continue
        try:
            d = json.loads(s.decode("utf-8", "replace"))
        except ValueError:
            continue
        if not isinstance(d, dict):
            continue
        if d.get("end"):
            end = d
            continue
        if "x" not in d or "ev" in d or is_bot(d) or is_header(d):
            continue
        try:
            r = row(d)
        except (TypeError, ValueError):
            continue
        count += 1
        last = r
    return new_off, count, last, end
