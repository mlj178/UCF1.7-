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

    # 采样间距 2.5 / 4 / 6 m 节点数随之间隔变化
    counts = [ucf_rec.analyse(samples, step=st, events=events)["nodes"]
              for st in (2.5, 4.0, 6.0)]
    print("step 2.5 / 4 / 6 -> nodes", counts)
    assert counts[0] >= counts[1] >= counts[2], counts

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

    print("OK: ucf_rec 自检通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
