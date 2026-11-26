#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ucf_rec.py 的离线自检：造一条「走路 → 跳上箱子 → 走路 → 超长跨跳 → 走路 → 跳下高台 → 静止」的轨迹。

2026-11-24 起录制数据是 ucf-trace/2（插件给玩家脚底坐标 + grounded/vy + 落地结算的 ev=jump），
所以这里也按那个格式造数据：样本带 g/vy，跳事件单独给，和游戏里跑出来的一模一样。

验证：走路节点链、跳链 3D 1.5~3.0 过滤（超长只标不建）、落下单向边、静止提示、
蹲点/传送断段已删除、去重、采样间距。
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


def s(t, x, y, z, g=1, vy=0.0, sp=0, ct=0):
    return {"t": round(t, 3), "dt": 0.033, "x": round(x, 3), "y": round(y, 3),
            "z": round(z, 3), "g": g, "vy": vy, "sp": sp, "ct": ct}


def walk(out, t0, x0, x1, y, speed=5.0, step=0.033):
    n = max(2, int(abs(x1 - x0) / (speed * step)))
    for i in range(n):
        out.append(s(t0 + i * step, x0 + (x1 - x0) * i / n, y, 0.0))
    return t0 + n * step


def build():
    samples, events = [], []
    t = walk(samples, 0.0, 0.0, 30.0, 0.0)          # 平地走 30 m
    # 跳上箱子：水平 1.2 m、高差 +1.9 m（3D ≈ 2.25，落在 1.5~3.0）
    n = 12
    for i in range(n):
        u = i / float(n - 1)
        samples.append(s(t + i * 0.033, 30.0 + 1.2 * u, 1.9 * u + (0.8 * (1 - abs(2 * u - 1))),
                         0.0, g=0, vy=10.0 if i == 0 else 5.0, sp=1 if i < 2 else 0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [30.0, 0.0, 0.0], "b": [31.2, 1.9, 0.0],
                   "h": 1.2, "rise": 1.9, "air": 0.4, "v0": 10.5, "run": 3.0,
                   "kind": "mount"})
    t = walk(samples, t, 31.2, 45.0, 1.9)
    # 超长跨跳：水平 6 m（3D ≈ 6.0，超出 3.0 -> 不许建链）
    n = 16
    for i in range(n):
        u = i / float(n - 1)
        samples.append(s(t + i * 0.033, 45.0 + 6.0 * u, 1.9 + 1.4 * (1 - abs(2 * u - 1)),
                         0.0, g=0, vy=10.0 if i == 0 else 4.0, sp=1 if i < 2 else 0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [45.0, 1.9, 0.0], "b": [51.0, 1.9, 0.0],
                   "h": 6.0, "rise": 1.4, "air": 0.8, "v0": 10.5, "run": 8.0,
                   "kind": "gap"})
    t = walk(samples, t, 51.0, 60.0, 1.9)
    # 跳下 4 m（down 事件）
    n = 14
    for i in range(n):
        u = i / float(n - 1)
        samples.append(s(t + i * 0.033, 60.0 + 0.8 * u, 1.9 - 4.0 * u,
                         0.0, g=0, vy=-2.0, sp=0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [60.0, 1.9, 0.0], "b": [60.8, -2.1, 0.0],
                   "h": 0.8, "rise": 0.2, "air": 0.46, "v0": 0.0, "run": 1.8,
                   "kind": "down"})
    t = walk(samples, t, 60.8, 70.0, -2.1)
    # 静止 2.5 s
    for i in range(75):
        samples.append(s(t + i * 0.033, 70.0, -2.1, 0.0))
    return samples, events


def build_two_close_jumps():
    r"""两跳只隔 0.5 m：第 2 跳的起点紧挨第 1 跳的落点。

    2026-11-26 之前：起点会被吸到落点上，3D 2.73 m 变成 3.16 m（> 3.0）被丢掉，
    两跳只剩一跳。现在两个跳点原样保留，两跳都要在。
    """
    samples, events = [], []
    t = walk(samples, 0.0, 0.0, 9.0, 0.0)
    # 第 1 跳：a1=(10,0,0) -> b1=(12.7,1.2,0.4)，3D 2.97
    n = 10
    for i in range(n):
        u = i / float(n - 1)
        samples.append(s(t + i * 0.033, 10.0 + 2.7 * u,
                         1.2 * u + 0.3 * (1 - abs(2 * u - 1)), 0.4 * u,
                         g=0, vy=10.0 if i == 0 else 4.0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [10.0, 0.0, 0.0], "b": [12.7, 1.2, 0.4],
                   "h": 2.73, "rise": 1.2, "air": 0.33, "v0": 10.0, "run": 9.0,
                   "kind": "mount"})
    # 落点走 0.5 m 到下一跳起点 a2=(13.2,1.2,0.5)
    for i in range(6):
        u = i / 5.0
        samples.append(s(t + i * 0.033, 12.7 + 0.5 * u, 1.2, 0.4 + 0.1 * u))
    t += 6 * 0.033
    # 第 2 跳：a2 -> b2=(15.4,2.8,0.75)，3D 2.73
    for i in range(10):
        u = i / 9.0
        samples.append(s(t + i * 0.033, 13.2 + 2.2 * u,
                         1.2 + 1.6 * u + 0.3 * (1 - abs(2 * u - 1)), 0.5 + 0.25 * u,
                         g=0, vy=10.0 if i == 0 else 4.0))
    t += 10 * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [13.2, 1.2, 0.5], "b": [15.4, 2.8, 0.75],
                   "h": 2.22, "rise": 1.6, "air": 0.33, "v0": 10.0, "run": 4.0,
                   "kind": "mount"})
    walk(samples, t, 15.4, 24.0, 2.8)
    return samples, events


def build_long_jump():
    r"""一跳 5.9 m：默认（上限 5.5）丢并报断口；打开「超长跳也建链」后要建上。"""
    samples, events = [], []
    t = walk(samples, 0.0, 0.0, 20.0, 0.0)
    n = 18
    for i in range(n):
        u = i / float(n - 1)
        samples.append(s(t + i * 0.033, 20.0 + 5.7 * u,
                         1.2 * u + 0.6 * (1 - abs(2 * u - 1)), 1.0 * u,
                         g=0, vy=10.0 if i == 0 else 4.0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [20.0, 0.0, 0.0], "b": [25.7, 1.2, 1.0],
                   "h": 5.79, "rise": 1.2, "air": 0.59, "v0": 10.0, "run": 9.0,
                   "kind": "gap"})
    walk(samples, t, 25.7, 34.0, 1.2)
    return samples, events


def main():
    samples, events = build()
    res = ucf_rec.analyse(samples, step=4.0, events=events)
    print("summary:", ucf_rec.summary(res))
    print("nodes=%d edges=%d jumps=%d links_bad=%d drops=%d static=%d" % (
        res["nodes"], res["edges"], len(res["jumps"]), res["links_bad"],
        len(res["drops"]), len(res["statics"])))
    for i in res["issues"]:
        print("  issue:", i)
    assert res["ok"], res.get("why")
    # 只有 1.5~3.0 的那一跳能建链；6 m 的只标问题
    assert len(res["jumps"]) == 1, "应只建 1 条跳链，实际 %d" % len(res["jumps"])
    j = res["jumps"][0]
    assert j["kind"] == "mount" and abs(j["l3"] - 2.25) < 0.1, j
    assert res["links_bad"] == 1, res["links_bad"]
    assert any("太长" in i for i in res["issues"]), res["issues"]
    # 落下：单向边
    assert len(res["drops"]) == 1 and abs(res["drops"][0]["drop"] - 4.0) < 0.3, res["drops"]
    # 蹲点已经删掉：结果里永远是空
    assert res["crouches"] == [], res["crouches"]
    assert len(res["statics"]) >= 1, res["statics"]
    assert res["nodes"] >= 12, res["nodes"]

    lines = ucf_rec.save_lines(res)
    text = "\n".join(lines)
    assert "node add " in text and "edge add " in text
    assert text.count("jump add") == 1, "只该有 1 条 jump add"
    print("save lines: %d（node %d / edge %d / jump %d）" % (
        len(lines), text.count("node add"), text.count("edge add"), text.count("jump add")))

    # 去重：同一份再存一遍不该冒出节点/边（jump 行按坐标去重，也应为 0）
    extra = ucf_rec.dedupe_lines(lines, text)
    assert not extra, "第二次保存不该再冒出行：%s" % extra[:3]
    print("dedupe: 第二次保存 0 行")

    # 开关：关掉跳跃 -> 没有跳链；关掉落 -> 没有落下
    sw = dict(ucf_rec.SW_DEFAULT)
    sw["jump"] = False
    r2 = ucf_rec.analyse(samples, step=4.0, sw=sw, events=events)
    assert not r2["jumps"] and not any(l.startswith("jump") for l in ucf_rec.save_lines(r2))
    sw = dict(ucf_rec.SW_DEFAULT)
    sw["drop"] = False
    r3 = ucf_rec.analyse(samples, step=4.0, sw=sw, events=events)
    assert not r3["drops"], r3["drops"]
    print("switch off jump / drop -> ok")

    # 采样间距 1.5 / 2.5 / 4 / 6 m 节点数随之间隔变化
    assert ucf_rec.STEP_OPTIONS[0] == 1.5, ucf_rec.STEP_OPTIONS
    assert min(ucf_rec.STEP_OPTIONS) >= 1.2, "比 MERGE_NEAR(1.05) 还密会并点"
    counts = [ucf_rec.analyse(samples, step=st, events=events)["nodes"]
              for st in (1.5, 2.5, 4.0, 6.0)]
    print("step 1.5 / 2.5 / 4 / 6 -> nodes", counts)
    assert counts[0] >= counts[1] >= counts[2] >= counts[3], counts

    # 没有事件时（旧文件兜底）也不能崩
    r4 = ucf_rec.analyse(samples, step=4.0)
    print("no-events fallback -> jumps=%d est=%s" % (len(r4["jumps"]), r4.get("est")))
    assert r4["ok"]

    # 旧格式（1 版）样本也能读，不崩
    legacy = [{"t": i * 0.05, "x": i * 0.25, "y": 1.6, "z": 0.0, "gy": 0.0, "sp": 0, "ct": 0}
              for i in range(80)]
    r5 = ucf_rec.analyse(legacy, step=4.0)
    assert r5["ok"], r5.get("why")
    print("legacy v1 rows -> nodes=%d" % r5["nodes"])

    # 跳点保护：两跳只隔 0.5 m 时都要保留（以前第 2 跳会被吸超 3 m 丢掉）
    s2, e2 = build_two_close_jumps()
    r6 = ucf_rec.analyse(s2, step=1.5, events=e2)
    l3 = sorted(round(j["l3"], 2) for j in r6["jumps"])
    print("two close jumps -> links %d %s" % (len(r6["jumps"]), l3))
    assert len(r6["jumps"]) == 2, r6["issues"]
    assert l3 == [2.73, 2.97] or (abs(l3[0] - 2.73) < 0.12 and abs(l3[1] - 2.97) < 0.12), l3
    starts = [tuple(round(v, 2) for v in j["a"]) for j in r6["jumps"]]
    assert (13.2, 1.2, 0.5) in starts, "第 2 跳起点被吸走了：%s" % (starts,)
    txt = "\n".join(ucf_rec.save_lines(r6))
    assert txt.count("jump add") == 2, txt
    assert not ucf_rec.dedupe_lines(ucf_rec.save_lines(r6), txt), "两跳不该被去重掉"

    # 断口：被拒的 6 m 跳要报出来，不能静默
    assert len(res["gaps"]) >= 1, res["gaps"]
    # 连通性：覆盖率 100%，没有孤立点
    assert res["coverage"] >= 95.0, res["coverage"]
    assert res["orphans"] == [], res["orphans"]

    # 超长跳开关：5.5 m 默认丢（上限 5.0）、报断口；打开后建链
    s3, e3 = build_long_jump()
    r7 = ucf_rec.analyse(s3, step=1.5, events=e3)
    print("long jump default -> links %d gaps %d" % (len(r7["jumps"]), len(r7["gaps"])))
    assert not r7["jumps"] and len(r7["gaps"]) == 1, (r7["jumps"], r7["gaps"])
    assert any("断开" in i for i in r7["issues"]), r7["issues"]
    sw2 = dict(ucf_rec.SW_DEFAULT)
    sw2["long_jump"] = True
    r8 = ucf_rec.analyse(s3, step=1.5, events=e3, sw=sw2)
    print("long jump switch on -> links %d gaps %d" % (len(r8["jumps"]), len(r8["gaps"])))
    assert len(r8["jumps"]) == 1 and not r8["gaps"], (r8["jumps"], r8["gaps"])

    print("OK: ucf_rec 自检通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
