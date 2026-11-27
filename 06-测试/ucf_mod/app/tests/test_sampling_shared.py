#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""录制 / 采集共用一套解析和一套格式（2026-11-27）。

为什么要有它：这两个功能以前各写一个读取器 —— 排序、去重、缺省值、header 判定都不一样，
同一份文件在两个页面可以给出不同的样本数；而且 ucf_trace 只认 kind=="trace"，
把**录制**文件喂给报告工具时 header 会被静默丢掉。

这个测试只做两件事：
  1) 三个入口（ucf_sample / ucf_trace / ucf_rec）对同一份数据给出同一个结果；
  2) 文件级读取认得 kind=rec，人机行不算进玩家样本，录制日志能直接出报告。

跑法：python app/tests/test_sampling_shared.py
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "app", "core"),
           os.path.join(UCF_ROOT, "app", "tabs", "dev"),
           os.path.join(UCF_ROOT, "app", "tabs", "record"),
           os.path.join(UCF_ROOT, "app", "tools", "data")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import jump_stats  # noqa: E402
import ucf_rec  # noqa: E402
import ucf_sample  # noqa: E402
import ucf_trace  # noqa: E402


def rec_lines():
    r"""一份 kind=rec / who=all 的日志：4 条玩家样本、1 条人机、1 条跳事件。"""
    return [
        {"kind": "rec", "schema": "ucf-trace/3", "who": "all", "hz": 30,
         "t0": "2026-11-27 12:00:00", "scene": "mp_x", "map": "level1",
         "label": "运输船", "pack": "p", "fp": "f", "src": "player",
         "fields": list(ucf_sample.FIELDS)},
        {"t": 0.0, "dt": 0.0, "x": 0.0, "y": 0.0, "z": 0.0, "g": 1, "vy": 0.0, "sp": 0, "ct": 0},
        {"t": 0.033, "dt": 0.033, "x": 0.2, "y": 0.0, "z": 0.0, "g": 1, "vy": 0.0, "sp": 1, "ct": 0},
        {"t": 0.066, "dt": 0.033, "x": 0.4, "y": 1.9, "z": 0.0, "g": 0, "vy": 10.5, "sp": 0, "ct": 0},
        {"t": 0.099, "dt": 0.033, "x": 0.6, "y": 2.1, "z": 0.0, "g": 1, "vy": 0.0, "sp": 0, "ct": 0},
        {"t": 0.1, "k": "b", "id": "0a1b2c3d", "x": 9.0, "y": 0.0, "z": 9.0, "g": 1,
         "vy": 0.0, "spd": 6.0, "j": 0, "en": 1, "act": "Move", "tgt": [1, 2, 3]},
        {"t": 0.12, "ev": "jump", "a": [0.2, 0.0, 0.0], "b": [0.6, 2.1, 0.0],
         "h": 0.4, "rise": 2.1, "air": 0.087, "v0": 10.5, "run": 6.0, "kind": "mount"},
        {"end": 1, "t": 0.2, "n": 4, "bots": 1, "dist": 0.7, "missed": 0, "ticks": 20, "jumps": 1},
    ]


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def check_same_reading(rows):
    r"""ucf_sample / ucf_rec 两个入口对同一份数据给同一个答案。"""
    lines = [json.dumps(r, ensure_ascii=False) for r in rows]
    samples = ucf_sample.player_rows(lines)
    assert samples == ucf_rec.parse_lines(lines), "两个读取器给出的样本不一样"
    assert len(samples) == 4, [s["t"] for s in samples]
    jumps = ucf_sample.jump_rows(lines)
    assert jumps == ucf_rec.parse_events(lines) and len(jumps) == 1
    bots = ucf_sample.bots_by_id(lines)
    assert bots == ucf_rec.parse_bots(lines) and list(bots) == ["0a1b2c3d"]

    # 同一时刻两行：保留后一行（和以前 ucf_rec 的去重规则一样）
    dup = [json.dumps({"t": 1.0, "x": 0, "y": 0, "z": 0, "ct": 0}),
           json.dumps({"t": 1.0, "x": 1, "y": 0, "z": 0, "ct": 1})]
    got = ucf_sample.player_rows(dup)
    assert len(got) == 1 and got[0]["ct"] == 1, got

    # 1 版老日志：缺 g/vy 也要读出来，gy 还在
    v1 = [json.dumps({"t": 0.0, "x": 0.0, "y": 1.6, "z": 0.0, "gy": 0.0,
                      "fx": 0.0, "fy": 0.0, "fz": 1.0, "sp": 0, "ct": 0,
                      "sh": 0, "w": 1, "a": 0, "s": 0, "d": 0})]
    r1 = ucf_sample.player_rows(v1)
    assert r1[0]["g"] is None and r1[0]["gy"] == 0.0 and r1[0]["w"] == 1

    # header 判定：rec 和 trace 都认（以前只认 trace，录制文件的 header 会被丢掉）
    assert ucf_sample.is_header({"kind": "rec", "schema": "ucf-trace/3"})
    assert ucf_sample.is_header({"kind": "trace", "schema": "ucf-trace/2"})
    assert not ucf_sample.is_header({"t": 0.0, "x": 1.0})


def check_file(tmp):
    path = os.path.join(tmp, "level1_pack_20261127-120000.jsonl")
    write_jsonl(path, rec_lines())

    # 1) 录制文件现在能读出 header（kind=rec）
    hdr, rows, jumps, end = ucf_trace.read_full(path)
    assert hdr.get("kind") == "rec" and hdr.get("who") == "all", hdr
    assert hdr.get("schema") == "ucf-trace/3", hdr
    assert len(rows) == 4 and len(jumps) == 1, (len(rows), jumps)
    assert end["bots"] == 1 and end["jumps"] == 1, end

    # 2) scan 只数玩家样本（人机行不算进「样本数 / 实测 Hz」）
    off, n, last, end2 = ucf_trace.scan(path, 0)
    assert (off, n) == (os.path.getsize(path), 4), (off, n, os.path.getsize(path))
    assert end2 is not None and abs(last["t"] - 0.099) < 1e-6, (end2, last)

    # 3) 摘要认得 who / 人机行数 / 跳事件
    sm = ucf_trace.summary(path)
    assert sm["map"] == "level1" and sm["src"] == "player", sm
    assert sm["samples"] == 4 and sm["bots"] == 1, sm
    assert sm["jumps"] == 1 and sm["jump_kinds"].get("mount") == 1, sm

    # 4) 报告工具能吃录制文件（同一套格式，不用重录）
    files, evs = jump_stats.collect([path])
    assert len(files) == 1 and files[0]["est"] is False, files
    assert files[0]["map"] == "level1" and files[0]["gear"] == 30, files[0]
    assert len(evs) == 1 and evs[0]["src"] == "plugin", evs
    md = jump_stats.report_md(files, evs)
    assert "# 跳跃数据分析" in md and "跳上高台" in md, md[:300]

    # 5) 目录也能当参数
    got = jump_stats.expand([tmp])
    assert got == [path], got


def check_static_sources():
    r"""两边都不许再自己解析（防止下次又分叉）。"""
    record = os.path.join(UCF_ROOT, "app", "tabs", "record", "ucf_rec.py")
    trace = os.path.join(UCF_ROOT, "app", "tabs", "dev", "ucf_trace.py")
    rec_src = open(record, encoding="utf-8").read()
    tr_src = open(trace, encoding="utf-8").read()
    assert "ucf_sample.player_rows(lines)" in rec_src
    assert "ucf_sample.jump_rows(lines)" in rec_src
    assert "ucf_sample.bots_by_id(lines)" in rec_src
    assert "ucf_sample.scan(path, offset)" in tr_src
    assert "ucf_sample.read_full(path)" in tr_src


def main():
    check_static_sources()
    check_same_reading(rec_lines())
    tmp = tempfile.mkdtemp(prefix="ucf_shared_")
    try:
        check_file(tmp)
    finally:
        for name in ("level1_pack_20261127-120000.jsonl",):
            p = os.path.join(tmp, name)
            try:
                os.remove(p)
            except OSError:
                pass
        try:
            os.rmdir(tmp)
        except OSError:
            pass
    print("OK: 录制 / 采集共用一套格式 + 解析；录制日志能直接出报告")
    return 0


if __name__ == "__main__":
    sys.exit(main())
