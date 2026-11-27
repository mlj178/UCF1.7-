#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ucf_rec.py 的离线自检：造一条「走路 → 跳上箱子 → 走路 → 超长跨跳 → 走路 → 跳下高台 → 静止」的轨迹。

2026-11-24 起录制数据是 ucf-trace/2（插件给玩家脚底坐标 + grounded/vy + 落地结算的 ev=jump），
所以这里也按那个格式造数据：样本带 g/vy，跳事件单独给，和游戏里跑出来的一模一样。

验证：走路节点链、跳链下限 1.5 m（2026-11-27 起不设上限）、落下单向边（含 < 2 m 的小落差）、
主动起跳不记 down、蹲的起止落盘、静止提示、蹲点/传送断段已删除、去重、采样间距。
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
    r"""一跳 5.9 m：2026-11-27 起默认就建链（上限取消），也不再提示「人机做不了」。"""
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


def build_small_drop():
    r"""走下 0.735 m 的小落差。

    2026-11-27 之前：down 事件落差 < 2 m 就什么都不建、也不写 issues —— 静默消失。
    现在要建一条 A->B 单向边，并在 issues 里提一句。
    """
    samples, events = [], []
    t = walk(samples, 0.0, 0.0, 12.0, 0.0)
    n = 6
    for i in range(n):
        u = i / float(n - 1)
        samples.append(s(t + i * 0.033, 12.0 + 0.6 * u, -0.735 * u, 0.0, g=0, vy=-2.0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [12.0, 0.0, 0.0], "b": [12.6, -0.735, 0.0],
                   "h": 0.6, "rise": 0.1, "air": 0.2, "v0": 0.0, "run": 1.5,
                   "kind": "down"})
    walk(samples, t, 12.6, 22.0, -0.735)
    return samples, events


def build_crouch_jump():
    r"""2026-11-27 风暴那次蹲跳的真实数值：跳过 6.93 m 缺口、落点低 0.735 m、空中按蹲。

    以前：判成 down -> 落差 0.735 < 2 m -> 一个点一条边都不建（静默消失）。
    现在：主动起跳 -> gap -> 建链（只留 A->B），蹲的起止写进 jump add 第 10~12 列。
    """
    samples, events = [], []
    t = walk(samples, 0.0, -2.0, 4.88, 9.9)
    n = 23
    for i in range(n):
        u = i / float(n - 1)
        y = 9.9 + 1.925 * (1 - (2 * u - 1) ** 2) - 0.735 * u
        samples.append(s(t + i * 0.033, 4.88 + 6.93 * u, y, -39.05,
                         g=0, vy=9.5 if i == 0 else 5.0, sp=1 if i == 0 else 0,
                         ct=1 if u > 0.6 else 0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [4.88, 9.9, -39.05], "b": [11.81, 9.165, -39.03],
                   "h": 6.93, "rise": 1.925, "air": 0.73, "v0": 9.5, "run": 8.2,
                   "kind": "gap", "ct": [0.57, -1.0], "ctb": 0})
    walk(samples, t, 11.81, 18.0, 9.165)
    return samples, events


def build_big_drop_jump():
    r"""跳下高台：水平 9.9 m、净下落 8.7 m（2026-11-27 19:14 那次真实录制）。

    以前按「主动起跳」判成 gap，建出一条 13.2 m 的跳链 —— 人机真会去跳它。
    现在：净下落 >= 3 m 只写单向边，不建跳链。
    """
    samples, events = [], []
    t = walk(samples, 0.0, -2.0, 4.0, 9.9)
    n = 20
    for i in range(n):
        u = i / float(n - 1)
        y = 9.9 + 1.9 * (1 - (2 * u - 1) ** 2) - 8.71 * u
        samples.append(s(t + i * 0.033, 4.0 + 9.88 * u, y, 0.0,
                         g=0, vy=9.5 if i == 0 else -5.0, sp=1 if i == 0 else 0))
    t += n * 0.033
    events.append({"t": round(t, 3), "ev": "jump",
                   "a": [4.0, 9.9, 0.0], "b": [13.88, 1.19, 0.0],
                   "h": 9.88, "rise": 1.917, "air": 1.2, "v0": 9.5, "run": 8.8,
                   "kind": "gap"})
    walk(samples, t, 13.88, 22.0, 1.19)
    return samples, events


def check_bots():
    r"""录制文件也要能分出玩家 / 人机（2026-11-27）。

    人机行靠 k="b"；玩家行不带 k（老录制日志可能带 k="p"，读取器也认）。
    录制页只把玩家样本送进路点分析，人机只做台数 / 条数观察 —— 这个测试钉住
    「解析不混、界面有计数、控制台真的把 who 发给插件」。
    """
    head = {"kind": "rec", "schema": "ucf-trace/3", "who": "all", "hz": 30,
            "fields": ["t", "dt", "x", "y", "z", "g", "vy", "sp", "ct"]}
    lines = [
        json.dumps(head),
        json.dumps({"t": 0.0, "k": "p", "dt": 0.0, "x": 0.0, "y": 0.0, "z": 0.0,
                    "g": 1, "vy": 0.0, "sp": 0, "ct": 0}),
        json.dumps({"t": 0.1, "k": "b", "id": "a", "x": 1.0, "y": 0.0, "z": 0.0,
                    "g": 1, "vy": 0.0, "spd": 4.0, "j": 0, "en": 0, "act": "Move"}),
        json.dumps({"t": 0.2, "k": "b", "id": "a", "x": 1.2, "y": 0.0, "z": 0.0,
                    "g": 1, "vy": 0.0, "spd": 4.0, "j": 0, "en": 0, "act": "Move"}),
        json.dumps({"t": 0.15, "k": "b", "id": "b", "x": 5.0, "y": 0.0, "z": 0.0,
                    "g": 1, "vy": 0.0, "spd": 3.0, "j": 0, "en": 0, "act": "Chase"}),
    ]
    bots = ucf_rec.parse_bots(lines)
    assert sorted(bots) == ["a", "b"], bots.keys()
    assert [len(bots["a"]), len(bots["b"])] == [2, 1], bots
    samples, events = ucf_rec.parse_rec(lines)
    assert len(samples) == 1 and not events, (len(samples), events)
    print("parse_bots: a=2 b=1；玩家样本 1（人机不混进路点）")

    tab = ""
    path = os.path.join(UCF_ROOT, "app", "tabs", "record", "tab.py")
    with open(path, "r", encoding="utf-8") as f:
        tab = f.read()
    assert "self.rec_bots = {}" in tab, "录制页没初始化人机计数（会 AttributeError）"
    assert "ucf_rec.parse_bots(lines)" in tab, "录制页没解析人机行"
    assert '"who": self.rec_who_active' in tab, "录制开始没把 who 发给插件"
    assert "def rec_bot_stats" in tab and "人机 %d 台 / %d 条" in tab, \
        "录制页没显示人机台数 / 条数"


def main():
    check_bots()
    samples, events = build()
    res = ucf_rec.analyse(samples, step=4.0, events=events)
    print("summary:", ucf_rec.summary(res))
    print("nodes=%d edges=%d jumps=%d links_bad=%d drops=%d static=%d" % (
        res["nodes"], res["edges"], len(res["jumps"]), res["links_bad"],
        len(res["drops"]), len(res["statics"])))
    for i in res["issues"]:
        print("  issue:", i)
    assert res["ok"], res.get("why")
    # 2026-11-27 起不设上限：2.25 m 和 6.0 m 两跳都要建链，不再有「太长」
    assert len(res["jumps"]) == 2, "应建 2 条跳链，实际 %d" % len(res["jumps"])
    j = [x for x in res["jumps"] if x["kind"] == "mount"][0]
    assert abs(j["l3"] - 2.25) < 0.1, j
    assert res["links_bad"] == 0, res["links_bad"]
    assert not any("太长" in i for i in res["issues"]), res["issues"]
    # 落下：单向边
    assert len(res["drops"]) == 1 and abs(res["drops"][0]["drop"] - 4.0) < 0.3, res["drops"]
    # 蹲点已经删掉：结果里永远是空
    assert res["crouches"] == [], res["crouches"]
    assert len(res["statics"]) >= 1, res["statics"]
    assert res["nodes"] >= 12, res["nodes"]

    lines = ucf_rec.save_lines(res)
    text = "\n".join(lines)
    assert "node add " in text and "edge add " in text
    assert text.count("jump add") == 2, "两跳两条 jump add"
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

    # 断口：6 m 跳现在建链了，所以四段路应当首尾相连，一个断口都没有
    assert len(res["gaps"]) == 0, res["gaps"]
    # 连通性：覆盖率 100%，没有孤立点
    assert res["coverage"] >= 95.0, res["coverage"]
    assert res["orphans"] == [], res["orphans"]

    # 5.9 m 的跳：2026-11-27 起默认就建链（上限取消），也不再提示「人机做不了」
    s3, e3 = build_long_jump()
    r7 = ucf_rec.analyse(s3, step=1.5, events=e3)
    print("long jump -> links %d gaps %d" % (len(r7["jumps"]), len(r7["gaps"])))
    assert len(r7["jumps"]) == 1 and not r7["gaps"], (r7["jumps"], r7["gaps"])
    assert not any("太长" in i or "人机做不了" in i for i in r7["issues"]), r7["issues"]

    # 主动起跳判据（2026-11-27 风暴 6.93 m 蹲跳：落点低 0.735 m，以前被判成 down 后静默丢掉）
    assert ucf_rec._kind(6.93, -0.735, 9.5, 0.73) == "gap", "主动起跳不该记成 down"
    assert ucf_rec._kind(6.93, -0.735, 0.0, 0.73) == "down", "没起跳速度就是跳下"
    assert ucf_rec._kind(6.93, -0.735, 9.5, 0.1) == "down", "滞空太短不算主动跳"
    assert ucf_rec._kind(1.0, 1.9, 10.0, 0.4) == "mount", "往上跳还是 mount"
    assert ucf_rec._kind(0.2, 0.0, 10.0, 0.4) == "hop", "原地小跳"

    # 小落差 down（0.735 m）：以前什么都不建也不吭声，现在要建单向边 + 提一句
    s4, e4 = build_small_drop()
    r9 = ucf_rec.analyse(s4, step=4.0, events=e4)
    print("small drop -> drops %d issues %s" % (
        len(r9["drops"]), [i for i in r9["issues"] if "落下" in i][:1]))
    assert len(r9["drops"]) == 1 and r9["drops"][0]["small"], r9["drops"]
    assert any("落下" in i for i in r9["issues"]), r9["issues"]
    txt9 = "\n".join(ucf_rec.save_lines(r9))
    a9, b9 = r9["drops"][0]["a"], r9["drops"][0]["b"]
    one = "edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (a9[0], a9[1], a9[2], b9[0], b9[1], b9[2])
    back = "edge add %.3f %.3f %.3f %.3f %.3f %.3f" % (b9[0], b9[1], b9[2], a9[0], a9[1], a9[2])
    assert one in txt9 and back not in txt9, "落下只该有 A->B 单向边"

    # 跳下高台（净下落 8.7 m）：只写单向边，不建跳链
    s6, e6 = build_big_drop_jump()
    r11 = ucf_rec.analyse(s6, step=4.0, events=e6)
    print("big drop jump -> jumps %d drops %d" % (len(r11["jumps"]), len(r11["drops"])))
    assert not r11["jumps"] and len(r11["drops"]) == 1, (r11["jumps"], r11["drops"])
    assert any("跳下" in i for i in r11["issues"]), r11["issues"]
    assert not any(l.startswith("jump add") for l in ucf_rec.save_lines(r11))

    # 控制台是常驻进程：这个模块刚从磁盘加载，code_stale() 必须是 False
    assert ucf_rec.code_stale() is False, "刚加载的模块不该被判成旧代码"

    # 蹲：事件带 ct -> jump add 第 10~12 列；插件 nav_load 能读回来
    s5, e5 = build_crouch_jump()
    r10 = ucf_rec.analyse(s5, step=4.0, events=e5)
    assert len(r10["jumps"]) == 1, r10["issues"]
    cj = r10["jumps"][0]
    assert abs(cj["ct0"] - 0.57) < 1e-6 and cj["ct1"] < 0 and cj["ctb"] == 0, cj
    line10 = [l for l in ucf_rec.save_lines(r10) if l.startswith("jump add")][0]
    assert line10.endswith(" 0.57 -1.00 0"), line10
    print("crouch jump -> %s" % line10)
    # 净下落的主动跳只留单向边
    assert cj["oneway"], cj

    print("OK: ucf_rec 自检通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
