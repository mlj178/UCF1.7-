#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""跳跃数据 -> Markdown 报告（控制台「开发者选项 → 轨迹采集」旁边的按钮也调它）。

用法：
    python app/tools/data/jump_stats.py                      # 目录里全部 .jsonl
    python app/tools/data/jump_stats.py a.jsonl b.jsonl      # 指定文件
    python app/tools/data/jump_stats.py --out 报告.md
    python app/tools/data/jump_stats.py --v1 warn            # 旧格式估算是开还是关

跳事件从哪来：
  * ucf-trace/2（2026-11-24 起）：插件在落地那一帧就写好一行 ev=jump，
    h / rise / air / v0 / run / kind 全是实测结算，本脚本只汇总，不猜；
  * ucf-trace/1（旧日志）：只有相机坐标、没有 grounded / 竖直速度，
    这里用「竖直速度 > 5 m/s 起跳 + 连续 3 帧竖直速度接近 0 落地」估算，
    报告里会标成「（估）」，并提示用新 DLL 重采。

只读原始日志、只写 Markdown。
"""
import argparse
import os
import statistics
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = HERE
while not os.path.isfile(os.path.join(PROJ, ".ucfroot")) and os.path.dirname(PROJ) != PROJ:
    PROJ = os.path.dirname(PROJ)          # 工程根：靠 .ucfroot 标记

for _p in (os.path.join(PROJ, "app", "tabs", "dev"), os.path.join(PROJ, "app", "core")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ucf_trace  # noqa: E402

KIND_CN = {"gap": "跨缺口", "mount": "跳上高台", "down": "跳下", "hop": "原地小跳"}
KIND_ORDER = ("gap", "mount", "down", "hop")


# ---------------------------------------------------------------- 旧格式估算
def _v1_eye(rows):
    r"""旧格式：站立眼高的中位数（相机 y − 脚下地面 y）。"""
    gaps = []
    for r in rows:
        gy = r.get("gy")
        if gy is not None and gy > -1000.0:
            g = r["y"] - gy
            if 0.6 <= g <= 3.0:
                gaps.append(g)
    return statistics.median(gaps) if gaps else 1.60


def jumps_v1(rows):
    r"""旧格式没有事件行：用竖直速度估算。返回跳 dict 列表（src = v1-est）。"""
    if len(rows) < 6:
        return []
    eye = _v1_eye(rows)
    out = []
    i = 1
    while i < len(rows) - 3:
        dt = rows[i]["t"] - rows[i - 1]["t"]
        if dt <= 0.0005:
            i += 1
            continue
        v0 = (rows[i]["y"] - rows[i - 1]["y"]) / dt
        if v0 <= 5.0:
            i += 1
            continue

        def vy(k):
            d = rows[k + 1]["t"] - rows[k]["t"]
            return (rows[k + 1]["y"] - rows[k]["y"]) / d if d > 0.0005 else 0.0

        k = i
        apex = rows[i]["y"]
        while k + 1 < len(rows) and vy(k) > -0.5:
            k += 1
            apex = max(apex, rows[k]["y"])
        land = -1
        for m in range(k, len(rows) - 3):
            if abs(vy(m)) < 0.6 and abs(vy(m + 1)) < 0.6 and abs(vy(m + 2)) < 0.6:
                land = m
                break
            if rows[m]["t"] - rows[i]["t"] > 2.5:
                break
        if land <= 0:
            i = k + 1
            continue
        A, B = rows[i - 1], rows[land]
        h = ((B["x"] - A["x"]) ** 2 + (B["z"] - A["z"]) ** 2) ** 0.5
        air = B["t"] - A["t"]
        rise = apex - A["y"]
        dy = B["y"] - A["y"]
        run = 0.0
        d = rows[i]["t"] - A["t"]
        if d > 0.0005:
            run = ((rows[i]["x"] - A["x"]) ** 2 + (rows[i]["z"] - A["z"]) ** 2) ** 0.5 / d
        pressed = any(rows[q]["sp"] for q in range(max(0, i - 3), min(len(rows), land + 2)))
        if pressed and 0.06 < air < 1.6 and rise > 0.3:
            if h < 0.5:
                kind = "hop"
            elif dy > 0.5:
                kind = "mount"
            elif dy < -0.5:
                kind = "down"
            else:
                kind = "gap"
            out.append({"t": B["t"], "kind": kind, "h": h, "rise": rise, "air": air,
                        "v0": v0, "run": run,
                        "a": (A["x"], A["y"] - eye, A["z"]),
                        "b": (B["x"], B["y"] - eye, B["z"]), "src": "v1-est"})
        i = land + 1
    return out


# ---------------------------------------------------------------- 收集
def collect(paths, allow_v1=True):
    r"""-> (files, jumps)；files 是每份日志的概览，jumps 是合并后的逐跳记录。"""
    files, jumps = [], []
    for p in paths:
        try:
            hdr, rows, evs, end = ucf_trace.read_full(p)
        except OSError as exc:
            files.append({"path": p, "err": str(exc), "jumps": []})
            continue
        schema = hdr.get("schema") or "?"
        src = hdr.get("src") or ("camera" if schema == "ucf-trace/1" else "")
        dur = (end or {}).get("t") or (rows[-1]["t"] if rows else 0.0)
        item = {
            "path": p, "schema": schema, "src": src,
            "map": hdr.get("map") or "", "label": hdr.get("label") or "",
            "pack": hdr.get("pack") or "",
            "gear": hdr.get("hz") or 0, "n": len(rows), "dur": dur,
            "hz": (len(rows) - 1) / dur if dur > 1.0 and len(rows) > 1 else 0.0,
            "ticks": (end or {}).get("ticks"),
            "est": False, "jumps": [],
        }
        if evs:
            item["jumps"] = [dict(j, src="plugin") for j in evs]
        elif schema == "ucf-trace/1" and allow_v1:
            item["jumps"] = jumps_v1(rows)
            item["est"] = True
        files.append(item)
        for j in item["jumps"]:
            jumps.append(dict(j, file=os.path.basename(p), map=item["map"],
                              label=item["label"]))
    jumps.sort(key=lambda j: (j.get("file") or "", j["t"]))
    return files, jumps


# ---------------------------------------------------------------- 报告
def _m(xs):
    return statistics.median(xs) if xs else 0.0


def _mx(xs):
    return max(xs) if xs else 0.0


def _p(x):
    return "(%.2f, %.2f, %.2f)" % (x[0], x[1], x[2])


def report_md(files, jumps):
    L = []
    L.append("# 跳跃数据分析 · %s" % time.strftime("%Y-%m-%d %H:%M"))
    L.append("")
    L.append("坐标口径：x/y/z 是**玩家脚底**的世界坐标；"
             "跳高 = 峰值脚底 − 起跳脚底；跳距 = 起跳点与落点的水平距离；"
             "滞空 = 起跳 → 落地的时间。")
    L.append("")
    L.append("## 1. 数据源")
    L.append("")
    L.append("| 文件 | 图 | 包 | 档位 | 实测 | 样本 | 时长 | 坐标源 | 跳 | 备注 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for f in files:
        if f.get("err"):
            L.append("| %s | - | - | - | - | - | - | - | - | 读不了：%s |"
                     % (os.path.basename(f["path"]), f["err"]))
            continue
        note = "旧格式，跳是估算" if f.get("est") else ""
        if f["src"] == "camera":
            note = (note + "；" if note else "") + "相机坐标，有系统偏差"
        L.append("| %s | %s %s | %s | %d Hz | %.1f Hz | %d | %.1f s | %s | %d | %s |"
                 % (os.path.basename(f["path"]), f["map"], f["label"], f.get("pack") or "-",
                    f["gear"], f["hz"], f["n"], f["dur"], f["src"] or "?",
                    len(f["jumps"]), note))
    L.append("")

    if not jumps:
        L.append("## 2. 逐跳明细")
        L.append("")
        L.append("没有跳事件：采样期间可能没跳，或者是旧 DLL 的日志（用新 DLL 采一次就有）。")
        L.append("")
        return chr(10).join(L) + chr(10)

    est = any(j.get("src") == "v1-est" for j in jumps)
    L.append("## 2. 逐跳明细%s" % ("（含估算）" if est else ""))
    L.append("")
    L.append("| # | 文件 | t (s) | 类型 | 跳距 (m) | 跳高 (m) | 滞空 (s) | 起跳 v0 | 助跑 (m/s) | 起跳点 | 落点 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for n, j in enumerate(jumps, 1):
        kind = KIND_CN.get(j.get("kind"), j.get("kind") or "?")
        if j.get("src") == "v1-est":
            kind += "（估）"
        L.append("| %d | %s | %.2f | %s | %.2f | %.2f | %.2f | %.1f | %.1f | %s | %s |"
                 % (n, j.get("file", ""), j["t"], kind, j["h"], j["rise"], j["air"],
                    j["v0"], j["run"], _p(j["a"]), _p(j["b"])))
    L.append("")

    L.append("## 3. 分类统计")
    L.append("")
    L.append("| 类型 | 次数 | 跳距 中位 / 最大 | 跳高 中位 | 滞空 中位 / 最大 | 助跑 中位 |")
    L.append("| --- | --- | --- | --- | --- | --- |")
    for kind in KIND_ORDER:
        js = [j for j in jumps if j.get("kind") == kind]
        if not js:
            continue
        hs = [j["h"] for j in js]
        rs = [j["rise"] for j in js]
        airs = [j["air"] for j in js]
        runs = [j["run"] for j in js]
        L.append("| %s | %d | %.2f / %.2f | %.2f | %.2f / %.2f | %.1f |"
                 % (KIND_CN[kind], len(js), _m(hs), _mx(hs), _m(rs), _m(airs), _mx(airs),
                    _m(runs)))
    L.append("")
    allv0 = [j["v0"] for j in jumps if j.get("v0")]
    if allv0:
        L.append("起跳竖直速度：中位 **%.1f m/s**（%.1f ~ %.1f）—— 和游戏里 "
                 "JumpPower = 10.5 对得上。" % (_m(allv0), min(allv0), max(allv0)))
        L.append("")

    L.append("## 4. 对「录制」的参数建议（由这批数据推出来）")
    L.append("")
    airs = [j["air"] for j in jumps if j["air"] > 0]
    if airs:
        L.append("- **采样档位**：最短滞空 %.2f s。要在一跳里留够 8 帧，需要 ≥ %.0f Hz；"
                 "建议 **30 Hz 起步，60 Hz 用于连跳/短跳**。"
                 % (min(airs), 8.0 / max(0.05, min(airs))))
    gaps_ = [j for j in jumps if j.get("kind") == "gap"]
    mounts = [j for j in jumps if j.get("kind") == "mount"]
    if gaps_:
        hs = [j["h"] for j in gaps_]
        L.append("- **跳链长度**：跨缺口跳距中位 %.2f m、最大 %.2f m。游戏原生跳链 ≤ 2.91 m，"
                 "所以自动建链只上 1.5~2.9 m；更远的要补中间落脚点或标「待实测」。"
                 % (_m(hs), _mx(hs)))
    if mounts:
        L.append("- **跳上高台**：%d 次（高差中位 %.2f m）。这类不是跳链，是「从一个面跳到另一个面」，"
                 "落点要落在台面上，不要写成 jump add。"
                 % (len(mounts), _m([j["rise"] for j in mounts])))
    L.append("- **判定口径**：起跳看竖直速度（> 6 m/s）且 isGrounded 由真到假；落地看 isGrounded。"
             "不要再用「离地 0.3 m」，那是旧格式靠相机射线估出来的办法。")
    L.append("")
    L.append("---")
    L.append("")
    L.append("判定口径：ucf-trace/2 的跳事件由插件在落地瞬间结算（a/b/h/rise/air/v0/run/kind）；"
             "标了「（估）」的是旧格式，本脚本用相机高度反推，只作参考。")
    return chr(10).join(L) + chr(10)


def default_paths():
    d = ucf_trace.DIR
    try:
        names = sorted(n for n in os.listdir(d) if n.endswith(".jsonl"))
    except OSError:
        return []
    return [os.path.join(d, n) for n in names]


def main(argv=None):
    ap = argparse.ArgumentParser(description="轨迹日志 -> 跳跃分析 Markdown 报告")
    ap.add_argument("files", nargs="*", help="要分析的 .jsonl；不给就用轨迹目录里全部")
    ap.add_argument("--out", default="", help="Markdown 输出路径")
    ap.add_argument("--no-v1", action="store_true", help="旧格式不做估算，只统计")
    args = ap.parse_args(argv)
    paths = args.files or default_paths()
    if not paths:
        print("没有轨迹文件：%s" % ucf_trace.DIR)
        return 2
    files, jumps = collect(paths, allow_v1=not args.no_v1)
    md = report_md(files, jumps)
    out = args.out or os.path.join(ucf_trace.DIR,
                                   "跳跃报告_%s.md" % time.strftime("%Y%m%d-%H%M%S"))
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline=chr(10)) as f:
        f.write(md)
    print("报告：%s（%d 份日志，%d 次跳）" % (out, len(files), len(jumps)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
