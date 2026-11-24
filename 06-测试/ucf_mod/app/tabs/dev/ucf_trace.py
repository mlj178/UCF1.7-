#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""原始轨迹采集：落盘位置 / 增量读取 / 摘要 —— 控制台「录制」页和命令行共用。

数据来源：src/editor.c 的 trace_tick()（控制台写 cmd=trace）。每个样本一行：

    {"t":0.017,"dt":0.017,"x":1.234,"y":-18.590,"z":-19.218,"gy":-20.140,
     "fx":0.1234,"fy":0.0,"fz":0.9923,"sp":0,"ct":0,"sh":0,"w":1,"a":0,"s":0,"d":0}

    第一行 header：
      {"kind":"trace","schema":"ucf-trace/1","hz":20,"t0":"2026-11-21 14:45:00",
       "scene":"...","map":"level1","label":"运输船","pack":"...","fp":"...",
       "fields":[...],"notes":"..."}
    事件行：{"t":12.3,"ev":"cam"} / {"t":12.3,"ev":"scene","n":"..."}
    结束行：{"end":1,"t":42.0,"n":1260,"dist":128.4,"missed":0}

设计目的（2026-11-21 用户要求）：把玩家操作原样记下来交给离线分析 / AI，
找出「跳跃 / 跳下 / 蹲行 / 上梯 / 传送」这些情景到底该用哪些信号和阈值识别，
而不是先猜一组阈值再对着失败案例改。所以这里不推断，只提供数据。

只做纯计算（不读 tkinter），tests/test_trace.py 可以离线跑。
"""
import csv
import json
import os
import re
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

#: 轨迹目录：② 开发版 vis\trace（和录制的 vis\rec 并列，都是插件写的原始档）
DIR = os.path.join(P.DEV, "vis", "trace")

#: 采样档位（Hz）。插件定时器 16 ms，60 Hz 是上限；再高只会记成 ~62 Hz。
GEARS = (10, 20, 30, 60)

#: 样本字段（必须和 editor.c 里 header 的 fields 一一对应）
FIELDS = ("t", "dt", "x", "y", "z", "gy", "fx", "fy", "fz",
          "sp", "ct", "sh", "w", "a", "s", "d")

#: 站立时眼睛离地高度的兜底值（识别不出来时用）
EYE_DEFAULT = 1.60


def make_path(level, when=None):
    r"""新日志的绝对路径：<图>_<yyyyMMdd-HHmmss>.jsonl；同秒重复就加 _2。"""
    ts = when or time.strftime("%Y%m%d-%H%M%S")
    stem = re.sub(r"[^0-9A-Za-z_-]+", "_", str(level or "map"))[:24] or "map"
    base = os.path.join(DIR, "%s_%s" % (stem, ts))
    path = base + ".jsonl"
    n = 2
    while os.path.exists(path):
        path = "%s_%d.jsonl" % (base, n)
        n += 1
    return path


def latest():
    r"""目录里最新的 .jsonl；没有就返回空串。"""
    try:
        names = [n for n in os.listdir(DIR) if n.endswith(".jsonl")]
    except OSError:
        return ""
    best, best_t = "", -1.0
    for name in names:
        path = os.path.join(DIR, name)
        try:
            mt = os.path.getmtime(path)
        except OSError:
            continue
        if mt > best_t:
            best, best_t = path, mt
    return best


def _row(d):
    r"""一行 JSON -> 样本 dict；gy 可能是 null（射线没打到）。"""
    gy = d.get("gy")
    return {
        "t": float(d.get("t") or 0.0),
        "dt": float(d.get("dt") or 0.0),
        "x": float(d["x"]), "y": float(d["y"]), "z": float(d["z"]),
        "gy": None if gy is None else float(gy),
        "fx": float(d.get("fx") or 0.0), "fy": float(d.get("fy") or 0.0),
        "fz": float(d.get("fz") or 0.0),
        "sp": int(d.get("sp") or 0), "ct": int(d.get("ct") or 0),
        "sh": int(d.get("sh") or 0),
        "w": int(d.get("w") or 0), "a": int(d.get("a") or 0),
        "s": int(d.get("s") or 0), "d": int(d.get("d") or 0),
    }


def scan(path, offset=0):
    r"""从 offset 往后读新写完的行（控制台 0.5 s 一次，不重读整个文件）。

    返回 (新 offset, 新样本数, 最后一个样本, end 行或 None)。
    只处理以换行结尾的行：插件正在写的那一行留到下次。
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
        if d.get("kind") == "trace" or "ev" in d or "x" not in d:
            continue
        try:
            row = _row(d)
        except (TypeError, ValueError):
            continue
        count += 1
        last = row
    return new_off, count, last, end


def read(path):
    r"""整个文件 -> (header, 样本列表, end 行)。坏行跳过，不抛。"""
    hdr, rows, end = {}, [], None
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            s = raw.strip()
            if not s.startswith("{"):
                continue
            try:
                d = json.loads(s)
            except ValueError:
                continue
            if not isinstance(d, dict):
                continue
            if d.get("kind") == "trace":
                hdr = d
                continue
            if d.get("end"):
                end = d
                continue
            if "x" not in d or "ev" in d:
                continue
            try:
                rows.append(_row(d))
            except (TypeError, ValueError):
                continue
    return hdr, rows, end


def _median(xs):
    xs = sorted(xs)
    if not xs:
        return 0.0
    m = len(xs) // 2
    return xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2.0


def summary_rows(rows):
    r"""一组样本 -> 数字摘要（控制台停止后显示；命令行也用它）。"""
    out = {
        "samples": len(rows or []), "duration": 0.0, "hz": 0.0, "dist": 0.0,
        "jumps": 0, "air": 0.0, "crouch": 0.0, "run": 0.0, "warps": 0,
        "eye": EYE_DEFAULT, "max_speed": 0.0,
    }
    if not rows:
        return out
    out["duration"] = rows[-1]["t"] - rows[0]["t"]
    if out["duration"] > 0.05:
        out["hz"] = max(0.0, (len(rows) - 1) / out["duration"])
    gaps = []
    for r in rows:
        if r["gy"] is not None and r["gy"] > -1000.0:
            g = r["y"] - r["gy"]
            if 0.6 <= g <= 3.0:
                gaps.append(g)
    base = _median(gaps) if gaps else EYE_DEFAULT
    out["eye"] = base
    prev = None
    for r in rows:
        dt = r["dt"] if r["dt"] > 0.0 else 0.0
        if prev is not None:
            d2 = ((r["x"] - prev["x"]) ** 2 + (r["z"] - prev["z"]) ** 2) ** 0.5
            if dt > 0.0 and dt < 0.5 and d2 < 8.0:
                out["dist"] += d2
                out["max_speed"] = max(out["max_speed"], d2 / dt)
            elif d2 >= 8.0:
                out["warps"] += 1
            if prev["sp"] == 0 and r["sp"] == 1:
                out["jumps"] += 1
        else:
            dt = 0.0
        if r["gy"] is not None and (r["y"] - r["gy"]) > base + 0.25:
            out["air"] += dt
        if r["ct"]:
            out["crouch"] += dt
        if r["sh"]:
            out["run"] += dt
        prev = r
    return out


def summary(path):
    r"""文件 -> 摘要 dict；顺便带上 header 里的图名/包名。"""
    hdr, rows, _end = read(path)
    sm = summary_rows(rows)
    sm["map"] = hdr.get("map") or ""
    sm["label"] = hdr.get("label") or ""
    sm["pack"] = hdr.get("pack") or ""
    sm["t0"] = hdr.get("t0") or ""
    sm["hz_set"] = hdr.get("hz") or 0
    return sm


def summary_text(sm):
    r"""一行中文摘要（控制台状态条 / 命令行共用）。"""
    if not sm or not sm.get("samples"):
        return "没有样本"
    return ("%d 样本 · %.1f s · 平均 %.1f Hz（档位 %s Hz） · 走 %.1f m · "
            "空格 %d 次 · 空中 %.1f s · Ctrl %.1f s · Shift %.1f s · 传送 %d"
            % (sm["samples"], sm["duration"], sm["hz"], sm.get("hz_set") or "?",
               sm["dist"], sm["jumps"], sm["air"], sm["crouch"], sm["run"],
               sm["warps"]))


def write_csv(path, rows):
    r"""导出 CSV（Excel 能直接开）；列顺序和 FIELDS 一致。"""
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(FIELDS)
        for r in rows:
            w.writerow(["" if r.get(k) is None else r.get(k) for k in FIELDS])


def main(argv=None):
    args = list(argv if argv is not None else sys.argv[1:])
    csv_path = ""
    if "--csv" in args:
        i = args.index("--csv")
        if i + 1 >= len(args):
            print("--csv 后面要跟输出路径")
            return 2
        csv_path = args[i + 1]
        del args[i:i + 2]
    path = args[0] if args else latest()
    if not path:
        print("没有轨迹文件：%s" % DIR)
        return 2
    try:
        hdr, rows, end = read(path)
    except OSError as exc:
        print("读不了 %s：%s" % (path, exc))
        return 2
    print("文件: %s" % path)
    for key in ("t0", "hz", "map", "label", "pack", "scene", "fp"):
        val = hdr.get(key)
        if val not in (None, ""):
            print("  %-6s %s" % (key, val))
    sm = summary_rows(rows)
    print(summary_text(sm))
    if end:
        print("  end     t=%.2f n=%s dist=%s missed=%s" % (
            float(end.get("t") or 0.0), end.get("n"), end.get("dist"),
            end.get("missed")))
    if csv_path:
        try:
            write_csv(csv_path, rows)
        except OSError as exc:
            print("写不进 CSV：%s" % exc)
            return 2
        print("CSV -> %s（%d 行）" % (csv_path, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
