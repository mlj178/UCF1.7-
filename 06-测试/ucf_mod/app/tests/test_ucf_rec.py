#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ucf_rec.py 的离线自检：造一条「走路 → 跳箱 → 走路 → 跳下高台 → 蹲 → 传送 → 走路」的轨迹。

不启动游戏、不读真实文件；只验证重采样 / 跳跃 / 落下 / 蹲点 / 断段 / 去重。
跑法：python tests/test_ucf_rec.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (HERE, os.path.join(UCF_ROOT, "app", "core"), os.path.join(UCF_ROOT, "app"),
           os.path.join(UCF_ROOT, "app", "tabs", "record")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import ucf_rec


def s(t, x, y, z, gy, sp=0, ct=0):
    return {"t": round(t, 3), "x": x, "y": y, "z": z, "gy": gy,
            "fx": 1.0, "fy": 0.0, "fz": 0.0, "sp": sp, "ct": ct}


def walk(out, t0, x0, x1, gy, speed=5.0, y=None, step=0.25):
    n = max(2, int(abs(x1 - x0) / (speed * step)))
    for i in range(n):
        x = x0 + (x1 - x0) * i / n
        out.append(s(t0 + i * step, x, (gy + 1.6) if y is None else y, 0.0, gy))
    return t0 + n * step


def build():
    out = []
    t = walk(out, 0.0, 0.0, 30.0, 0.0)          # 平地走 30 m（6 s）
    # 跳箱：0.7 s 腾空，水平 6 m（30 -> 36），脚下射线打空
    n = 14
    for i in range(n):
        u = i / float(n - 1)
        out.append(s(t + i * 0.05, 30.0 + 6.0 * u, 1.6 + 1.2 * (1 - abs(2 * u - 1)), 0.0,
                     -9999.0, sp=1 if i < 3 else 0))
    t += n * 0.05
    t = walk(out, t, 36.0, 60.0, 0.0)           # 再走 24 m
    # 跳下高台：0.5 s 从 0 掉到 -4，水平 1 m
    n = 10
    for i in range(n):
        u = i / float(n - 1)
        gy = -4.0 * u
        out.append(s(t + i * 0.05, 60.0 + 1.0 * u, gy + 1.6, 0.0, gy))
    t += n * 0.05
    t = walk(out, t, 61.0, 80.0, -4.0)          # 下层走 19 m
    # 蹲 1.5 s（不动）
    n = 30
    for i in range(n):
        out.append(s(t + i * 0.05, 80.0, -4.0 + 1.2, 0.0, -4.0, ct=1))
    t += n * 0.05
    # 静止 2.5 s
    n = 50
    for i in range(n):
        out.append(s(t + i * 0.05, 80.0, -4.0 + 1.6, 0.0, -4.0))
    t += n * 0.05
    # 传送：直接到 x=100（单帧 20 m）
    t = walk(out, t, 100.0, 110.0, 0.0)
    return out


def main():
    samples = build()
    res = ucf_rec.analyse(samples, step=4.0)
    print("summary:", ucf_rec.summary(res))
    print("segments=%d nodes=%d edges=%d jumps=%d drops=%d crouch=%d static=%d branch=%d" % (
        res["segments"], res.get("nodes"), res.get("edges"), len(res["jumps"]),
        len(res["drops"]), len(res["crouches"]), len(res["statics"]),
        len(res["branches"])))
    for i in res["issues"]:
        print("  issue:", i)
    assert res["ok"], res.get("why")
    assert res["segments"] == 2, "传送应断成 2 段，实际 %d" % res["segments"]
    assert len(res["jumps"]) == 1, "应识别 1 次跳箱，实际 %d" % len(res["jumps"])
    assert abs(res["jumps"][0]["h"] - 6.0) < 0.4
    assert len(res["drops"]) == 1, "应识别 1 次落下，实际 %d" % len(res["drops"])
    assert abs(res["drops"][0]["drop"] - 4.0) < 0.4
    assert len(res["crouches"]) == 1, "应识别 1 处蹲点"
    assert len(res["statics"]) >= 1, "应识别 1 段静止"
    assert res["nodes"] >= 12

    lines = ucf_rec.save_lines(res)
    text = "\n".join(lines)
    assert "node add " in text and "edge add " in text and "jump add " in text
    print("save lines: %d（node %d / edge %d / jump %d）" % (
        len(lines), text.count("node add"), text.count("edge add"), text.count("jump add")))

    # 去重：把增量当现有内容，再存一遍应当一行都不剩（跳链除外：jump 行不去重）
    extra = ucf_rec.dedupe_lines(lines, text)
    left = [ln for ln in extra if not ln.startswith("jump ")]
    assert not left, "第二次保存不该再冒出节点/边：%s" % left[:3]
    print("dedupe: 第二次保存新增节点/边 0 行（jump 行保留 %d）" % (len(extra) - len(left)))

    # 开关：关掉跳跃识别，跳链就不该出现
    sw = dict(ucf_rec.SW_DEFAULT)
    sw["jump"] = False
    res2 = ucf_rec.analyse(samples, step=4.0, sw=sw)
    assert not res2["jumps"], "关掉跳跃后不应再有跳链"
    assert not any(ln.startswith("jump") for ln in ucf_rec.save_lines(res2))
    print("switch off jump -> jumps=0")

    # 采样间距 2.5 / 6 m 节点数随之间隔变化
    counts = []
    for step in (2.5, 4.0, 6.0):
        r = ucf_rec.analyse(samples, step=step)
        counts.append(r["nodes"])
    print("step 2.5 / 4 / 6 -> nodes", counts)
    assert counts[0] > counts[1] > counts[2], counts
    print("OK: ucf_rec 自检通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
