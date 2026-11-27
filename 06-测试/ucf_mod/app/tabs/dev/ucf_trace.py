#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""原始轨迹采集：落盘位置 / 增量读取 / 摘要 —— 控制台「开发者选项」页和命令行共用。

**2026-11-27 起是 ucf-trace/3（录制 / 采集同一套采样器）**，数据来源 src/editor.c 的 sess_tick()：

    header  {"kind":"trace","schema":"ucf-trace/3","who":"player","hz":30,"t0":"...","scene":"...",
             "map":"level1","label":"运输船","pack":"...","fp":"...",
             "src":"player","fields":["t","dt","x","y","z","g","vy","sp","ct"],
             "notes":"..."}
    样本    {"t":31.770,"dt":0.033,"x":-8.120,"y":-16.640,"z":-19.600,
             "g":1,"vy":0.02,"sp":0,"ct":0}
            xyz = 玩家脚底（世界坐标，不是相机）；g = 是否在地面；vy = 竖直速度 m/s
    跳事件  {"t":32.490,"ev":"jump","a":[-8.12,-16.64,-19.60],"b":[-6.05,-16.64,-18.42],
             "h":2.310,"rise":1.900,"air":0.720,"v0":10.5,"run":8.4,"kind":"gap"}
            a = 起跳点、b = 落点、h = 水平跳距、rise = 跳高（峰值 − 起跳）、
            air = 滞空、v0 = 起跳竖直速度、run = 起跳水平速度、
            kind = gap(跨缺口) / mount(跳上高台) / down(跳下) / hop(原地小跳)
    分段行  {"t":12.3,"ev":"cam"} / {"t":12.3,"ev":"scene","n":"..."}
    结束行  {"end":1,"t":42.0,"n":1260,"dist":128.4,"missed":0,"ticks":1250}

为什么换（2026-11-24）：旧版记的是相机坐标（比脚底高 2.29 m，蹲下还会变），
而且"脚下地面"是相机射线，会穿楼层一帧跳 9.5 m；跳高/落点只能靠离线猜。
新版坐标取 Player.characterContainer，落地由插件按 isGrounded + velData.y 结算，
所以跳距/跳高/滞空是**直接读出来的**，不是推出来的。

旧文件（ucf-trace/1）继续能读：字段少就按缺省值补，分析端会在报告里标出来。
**读文件的部分已经搬到 app/core/ucf_sample.py**（录制和采集共用一份解析，见那里的说明）；
本模块只保留「这个功能自己的东西」：目录 / 文件命名 / 摘要 / 报告入口。

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
DIR = os.path.join(P.INBOX, "trace")

#: 采样档位（Hz）。插件采样定时器 10 ms（USER_TIMER_MINIMUM），60 Hz 是最高档；
#: 实际上限≈游戏帧率（WM_TIMER 只在主循环泵消息时派发），跑不满时 summary 会标出来。
GEARS = (10, 20, 30, 60)

#: 样本字段 / 跳事件键 / 解析：唯一实现在 core/ucf_sample.py（录制也用它）
import ucf_sample  # noqa: E402
from ucf_sample import FIELDS, FIELDS_V1, JUMP_KEYS, KINDS, SCHEMAS  # noqa: E402,F401

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
    r"""一行 JSON -> 样本 dict（实现见 core/ucf_sample.row）。"""
    return ucf_sample.row(d)


def _jump(d):
    r"""一行 ev=jump -> 跳事件 dict（实现见 core/ucf_sample.jump）。"""
    return ucf_sample.jump(d)


def scan(path, offset=0):
    r"""增量读取（实现见 core/ucf_sample.scan；人机行不算进样本数）。"""
    return ucf_sample.scan(path, offset)


def read_full(path):
    r"""整个文件 -> (header, 样本列表, 跳事件列表, end 行)。

    实现在 core/ucf_sample.read_full：**header 按 kind/fields 判定**，所以录制
    （kind=rec）和采集（kind=trace）的文件用同一个函数读，不再各写一份。
    """
    return ucf_sample.read_full(path)


def read(path):
    r"""整个文件 -> (header, 样本列表, end 行) —— 不要跳事件时用它。"""
    return ucf_sample.read(path)


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
        gy = r.get("gy")
        if gy is not None and gy > -1000.0:
            g = r["y"] - gy
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
        if r.get("g") is not None:                 # 2 版：插件直接给 grounded
            if r["g"] == 0:
                out["air"] += dt
        elif r["gy"] is not None and (r["y"] - r["gy"]) > base + 0.25:
            out["air"] += dt                          # 1 版：只能靠射线 + 眼高猜
        if r["ct"]:
            out["crouch"] += dt
        if r["sh"]:
            out["run"] += dt
        prev = r
    return out


def summary(path):
    r"""文件 -> 摘要 dict；顺便带上 header 里的图名/包名/坐标来源。"""
    hdr, rows, jumps, end = read_full(path)
    sm = summary_rows(rows)
    sm["map"] = hdr.get("map") or ""
    sm["label"] = hdr.get("label") or ""
    sm["pack"] = hdr.get("pack") or ""
    sm["t0"] = hdr.get("t0") or ""
    sm["schema"] = hdr.get("schema") or ""
    sm["src"] = hdr.get("src") or ("camera" if hdr.get("schema") == "ucf-trace/1" else "")
    sm["hz_set"] = hdr.get("hz") or 0
    sm["ticks"] = (end or {}).get("ticks")     # 插件采样定时器派发次数（新 DLL 才有）
    sm["jumps"] = len(jumps)                   # 插件结算好的跳事件（2 版才有）
    sm["jump_kinds"] = {}
    for j in jumps:
        k = j.get("kind") or "?"
        sm["jump_kinds"][k] = sm["jump_kinds"].get(k, 0) + 1
    return sm


def starved(sm):
    r"""实测采样率明显低于档位（不足 75%）= 插件的采样定时器没跑起来。

    2026-11-24：档位 60 Hz、实测 4.0 Hz —— 采样只挂在 250 ms 心跳上，
    日志里却什么都看不出来。这个判定把「静默降级」变成一句人话。
    """
    if not sm or sm.get("samples", 0) < 2:
        return False
    try:
        hz = float(sm.get("hz") or 0.0)
        gear = float(sm.get("hz_set") or 0.0)
        dur = float(sm.get("duration") or 0.0)
    except (TypeError, ValueError):
        return False
    if gear <= 0.0 or hz <= 0.0 or dur < 1.0:
        return False
    return hz < gear * 0.75


def summary_text(sm):
    r"""一行中文摘要（控制台状态条 / 命令行共用）。"""
    if not sm or not sm.get("samples"):
        return "没有样本"
    txt = ("%d 样本 · %.1f s · 平均 %.1f Hz（档位 %s Hz） · 走 %.1f m · "
           "空格 %d 次 · 空中 %.1f s · Ctrl %.1f s · Shift %.1f s · 传送 %d"
           % (sm["samples"], sm["duration"], sm["hz"], sm.get("hz_set") or "?",
              sm["dist"], sm["jumps"], sm["air"], sm["crouch"], sm["run"],
              sm["warps"]))
    if sm.get("jumps"):
        kinds = sm.get("jump_kinds") or {}
        parts = ["%s %d" % (k, kinds[k]) for k in ("gap", "mount", "down", "hop") if kinds.get(k)]
        txt += " · 跳 %d 次%s" % (sm["jumps"], "（%s）" % "、".join(parts) if parts else "")
    if starved(sm):
        txt += (" · !!! 没跑满档位（只有 %.0f%%）：插件采样定时器没起来 —— "
                "确认跑的是新 ucf_mod.dll，并按控制台「部署」页重装一次"
                % (100.0 * sm["hz"] / max(1e-6, float(sm.get("hz_set") or 1))))
    if sm.get("src") == "camera":
        txt += " · 注意：这份是相机坐标（旧 DLL 或没找到玩家对象），跳高/落点有系统偏差"
    return txt


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
        hdr, rows, jumps, end = read_full(path)
    except OSError as exc:
        print("读不了 %s：%s" % (path, exc))
        return 2
    print("文件: %s" % path)
    for key in ("schema", "t0", "hz", "map", "label", "pack", "scene", "fp", "src"):
        val = hdr.get(key)
        if val not in (None, ""):
            print("  %-6s %s" % (key, val))
    sm = summary_rows(rows)
    sm["hz_set"] = hdr.get("hz") or 0
    sm["src"] = hdr.get("src") or ("camera" if hdr.get("schema") == "ucf-trace/1" else "")
    sm["ticks"] = (end or {}).get("ticks")
    sm["jumps"] = len(jumps)
    sm["jump_kinds"] = {}
    for j in jumps:
        k = j.get("kind") or "?"
        sm["jump_kinds"][k] = sm["jump_kinds"].get(k, 0) + 1
    print(summary_text(sm))
    if jumps:
        print("  跳事件（插件结算）：")
        for j in jumps:
            print("    t=%6.2f %-5s h=%5.2f m  rise=%5.2f m  air=%.2f s  v0=%.1f  run=%.1f  "
                  "a=(%.2f,%.2f,%.2f) b=(%.2f,%.2f,%.2f)"
                  % (j["t"], j["kind"] or "?", j["h"], j["rise"], j["air"], j["v0"],
                     j["run"], j["a"][0], j["a"][1], j["a"][2],
                     j["b"][0], j["b"][1], j["b"][2]))
    if end:
        print("  end     t=%.2f n=%s dist=%s missed=%s ticks=%s" % (
            float(end.get("t") or 0.0), end.get("n"), end.get("dist"),
            end.get("missed"), end.get("ticks")))
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
