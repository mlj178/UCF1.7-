#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""静态自检 + 单元自检：原始轨迹采集（tools/ucf_trace.py + editor.c + 控制台）

为什么要有它：轨迹字段是「C 侧写、Python 侧读」的隐式契约 —— 两边任何一边
加/删一个字段，另一边的解析不会报错，只会悄悄少一列。这个测试把字段表
（editor.c header 的 fields 数组）和 ucf_trace.FIELDS 钉死在一起，再用一份
合成日志跑一遍增量读取 / 摘要。不需要游戏、窗口、网络。

跑法：python tests/test_trace.py
"""
import ast
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
PROJ = UCF_ROOT
for _p in (os.path.join(UCF_ROOT, "app", "core"), os.path.join(UCF_ROOT, "app"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ucf_trace  # noqa: E402

EDITOR = os.path.join(PROJ, "src", "editor.c")
CONSOLE = os.path.join(PROJ, "app", "控制台.pyw")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_c(editor):
    assert "static int trace_start(" in editor, "editor.c 没有 trace_start()"
    assert "static void trace_stop(" in editor, "editor.c 没有 trace_stop()"
    assert "static void trace_sample(" in editor, "editor.c 没有 trace_sample()"
    assert "static void trace_tick(" in editor, "editor.c 没有 trace_tick()"
    assert "void editor_rec_tick(void) { rec_tick(); trace_tick(); }" in editor, \
        "16 ms 定时器没同时驱动 rec 和 trace"
    assert "trace_tick();               /* 原始轨迹采集" in editor, \
        "editor_tick() 没调 trace_tick()"
    assert 'if (!strcmp(cmd, "trace"))' in editor, "navcmd 没接 cmd=trace"
    assert 'if (!strcmp(cmd, "stopall"))' in editor, "navcmd 没接 cmd=stopall"
    assert "trace_stop(\"restart\")" in editor, "trace_start 没先收掉上一份"
    assert "QueryPerformanceCounter" in editor, "trace 没用 QPC（60 Hz 时间太粗）"

    # header 的 fields 数组 = ucf_trace.FIELDS
    m = re.search(r"fields.*?\[(.*?)\]", editor, re.S)
    assert m, "editor.c header 里找不到 fields 数组"
    fields = tuple(re.findall(r'\\"([a-z]+)\\"', m.group(1)))
    assert fields == tuple(ucf_trace.FIELDS), \
        "字段表不一致：C=%s Python=%s" % (fields, ucf_trace.FIELDS)

    # 样本 fprintf 里必须有全部字段
    seg = editor.split("static void trace_sample(void)")[1].split("static void trace_tick")[0]
    for key in ucf_trace.FIELDS:
        assert ('\\"%s\\":' % key) in seg, "trace_sample 少了字段 %s" % key

    # 两个事件行：换图 / 换相机
    assert '\\"ev\\":\\"cam\\"' in seg, "trace_sample 没有 ev=cam"
    assert '\\"ev\\":\\"scene\\"' in seg, "trace_sample 没有 ev=scene"
    assert 'gy\\":%s' in seg and 'strcpy(gyb, "null")' in seg, "gy 没处理射线打空"


def check_console(console):
    for fn in ("build_trace_card", "on_trace_hz", "trace_start", "trace_poll",
               "trace_live", "trace_stop", "trace_finish", "trace_open_dir",
               "trace_open_file", "trace_copy_path"):
        assert ("def %s(self" % fn) in console, "控制台少了 %s()" % fn
    assert "import ucf_trace" in console, "控制台没导入 ucf_trace"
    assert "原始轨迹采集（给 AI 分析用）" in console, "「开发者选项」页没有轨迹卡片标题"
    # 2026-11-21 用户要求：卡片从「录制」搬到「开发者选项」，状态在卡片前单独备好
    assert "def init_trace_state(self" in console, "控制台少了 init_trace_state()"
    assert "self.init_trace_state()" in console, "建轨迹卡片前没初始化采集状态"
    assert "self.build_trace_card(body)" in console, "轨迹卡片没挂到「开发者选项」页"
    assert "打开日志文件夹" in console, "缺「打开日志文件夹」按钮"
    assert '"日志文件"' in console and '"日志目录"' in console, \
        "控制台没显示日志文件名 / 目录"
    assert "ucf_trace.DIR" in console, "目录没取 ucf_trace.DIR"
    assert "for h in ucf_trace.GEARS" in console, "档位不是从 ucf_trace.GEARS 生成"
    assert 'write_nav_cmd("trace"' in console, "没发 cmd=trace"
    assert '"stopall"' in console, "关窗口没发 stopall"
    assert "self.tr_file" in console and "os.startfile(ucf_trace.DIR)" in console, \
        "打开文件夹没接到 ucf_trace.DIR"
    # 档位文案必须覆盖全部档位
    for hz in ucf_trace.GEARS:
        assert str(hz) in " ".join(["%d Hz" % x for x in ucf_trace.GEARS])


def synth(path):
    head = {
        "kind": "trace", "schema": "ucf-trace/1", "hz": 20,
        "t0": "2026-11-21 15:00:00", "scene": "mp_test",
        "map": "level1", "label": "运输船", "pack": "01_TransportShip运输船/p",
        "fp": "n786-57a46e3465c847cb", "fields": list(ucf_trace.FIELDS),
    }
    lines = [json.dumps(head, ensure_ascii=False)]
    for i in range(41):
        t = round(i * 0.05, 3)
        airborne = 20 <= i < 30
        row = {"t": t, "dt": 0.05 if i else 0.0,
               "x": -50.0 + i * 0.2, "y": -16.64 + (0.8 if airborne else 0.0),
               "z": 6.0, "gy": -18.24,
               "fx": 0.0, "fy": 0.0, "fz": 1.0,
               "sp": 1 if airborne else 0, "ct": 1 if 30 <= i < 35 else 0,
               "sh": 0, "w": 1, "a": 0, "s": 0, "d": 0}
        lines.append(json.dumps(row, ensure_ascii=False))
    lines.append(json.dumps({"end": 1, "t": 2.0, "n": 41, "dist": 8.0, "missed": 0}))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def check_unit():
    tmp = tempfile.mkdtemp(prefix="ucf_trace_")
    path = os.path.join(tmp, "level1_20261121-150000.jsonl")
    synth(path)

    off, n, last, end = ucf_trace.scan(path, 0)
    assert (n, end is not None) == (41, True), (n, end)
    assert last and abs(last["t"] - 2.0) < 0.01, last
    assert off == os.path.getsize(path), (off, os.path.getsize(path))
    assert ucf_trace.scan(path, off)[0:2] == (off, 0), "增量读取重复计数"

    # 追加一行：只应读到 1 行
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps({"t": 2.05, "dt": 0.05, "x": -41.8, "y": -16.64,
                            "z": 6.0, "gy": -18.24, "fx": 0.0, "fy": 0.0,
                            "fz": 1.0, "sp": 0, "ct": 0, "sh": 0, "w": 1,
                            "a": 0, "s": 0, "d": 0}) + "\n")
    off2, n2, last2, _ = ucf_trace.scan(path, off)
    assert n2 == 1 and abs(last2["t"] - 2.05) < 1e-6, (n2, last2)

    hdr, rows, end = ucf_trace.read(path)
    assert hdr["map"] == "level1" and hdr["label"] == "运输船"
    assert len(rows) == 42, len(rows)
    assert rows[0]["gy"] == -18.24

    sm = ucf_trace.summary_rows(rows)
    assert sm["samples"] == 42 and 2.0 <= sm["duration"] <= 2.2, sm
    assert sm["jumps"] == 1, sm
    assert sm["dist"] > 8.0, sm
    assert sm["air"] > 0.4, sm
    assert sm["crouch"] > 0.2, sm
    assert 1.5 < sm["eye"] < 1.7, sm

    text = ucf_trace.summary_text(sm)
    assert "样本" in text and "空格 1 次" in text, text

    # make_path：同一个时间戳不覆盖（只改 DIR，别碰真实目录）
    real_dir = ucf_trace.DIR
    try:
        ucf_trace.DIR = tmp
        os.utime(path, (1, 1))               # 让合成日志变成「旧文件」
        a = ucf_trace.make_path("level1", "20261121-160000")
        assert a.endswith("level1_20261121-160000.jsonl"), a
        assert not os.path.exists(a), "make_path 只返回名字，不建文件"
        with open(a, "w", encoding="utf-8"):
            pass
        b = ucf_trace.make_path("level1", "20261121-160000")
        assert b.endswith("level1_20261121-160000_2.jsonl"), b
        assert ucf_trace.latest() == a, ucf_trace.latest()
    finally:
        ucf_trace.DIR = real_dir

    # CSV 导出（列顺序 = FIELDS）
    csv_path = os.path.join(tmp, "out.csv")
    ucf_trace.write_csv(csv_path, rows)
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        first = f.readline().strip()
    assert first == ",".join(ucf_trace.FIELDS), first


def _fprintf(block, pos=0):
    r"""取一个 fprintf(g_trFp, ...) 的格式串，并跳过字符串里的 ');'。

    返回 (格式串, 起始位置, 结束位置)。格式串 = 所有 "..." 片段按 C 转义还原后拼接。
    """
    i = block.index("fprintf(g_trFp,", pos)
    k = i
    in_str = False
    while k < len(block):
        c = block[k]
        if in_str:
            if c == "\\":
                k += 2
                continue
            if c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == ")" and block[k + 1] == ";":
            stmt = block[i:k + 2]
            lits = re.findall(r'"((?:[^"\\]|\\.)*)"', stmt)
            fmt = ""
            for s in lits:
                fmt += ast.literal_eval('"' + s + '"')
            return fmt, i, k + 2
        k += 1
    raise AssertionError("fprintf(g_trFp, ...) 没有结尾")


def check_c_format(editor):
    r"""C 写出来的 header / 样本行必须是合法 JSON，且键名和 FIELDS 一致。

    这条能抓住「少一个逗号 / 引号没转义 / %s 和参数对不上」——编译不会报，
    但 Python 侧会整份读不出来。
    """
    hdr_block = editor.split("static void tr_header(void)")[1].split("static void trace_stop")[0]
    hfmt, _, _ = _fprintf(hdr_block)
    hargs = (20, 2026, 11, 21, 15, 0, 0, "mp_x", "level1", "运输船", "pack", "fp")
    hobj = json.loads(hfmt % hargs)
    assert hobj["kind"] == "trace" and hobj["schema"] == "ucf-trace/1", hobj
    assert tuple(hobj["fields"]) == tuple(ucf_trace.FIELDS), hobj["fields"]
    assert hobj["label"] == "运输船" and hobj["map"] == "level1"
    assert hobj["t0"] == "2026-11-21 15:00:00", hobj["t0"]

    smp_block = editor.split("static void trace_sample(void)")[1].split("static void trace_tick")[0]
    pos = 0
    while True:
        sfmt, _, pos = _fprintf(smp_block, pos)
        if "dt" in sfmt:
            break

    sargs = (0.017, 0.017, 1.234, -18.59, -19.218, "-20.140",
             0.1234, 0.0, 0.9923, 0, 0, 0, 1, 0, 0, 0)
    obj = json.loads(sfmt % sargs)
    assert set(obj) == set(ucf_trace.FIELDS), (set(obj), set(ucf_trace.FIELDS))
    assert abs(obj["t"] - 0.017) < 1e-9 and obj["sp"] == 0 and obj["w"] == 1
    assert abs(obj["gy"] + 20.14) < 1e-9, obj["gy"]

    # 射线打空：gy 写 null，JSON 里必须是 None
    obj2 = json.loads(sfmt % (sargs[:5] + ("null",) + sargs[6:]))
    assert obj2["gy"] is None, obj2["gy"]


def main():
    editor = read(EDITOR)
    check_c(editor)
    check_c_format(editor)
    check_console(read(CONSOLE))
    check_unit()
    print("OK: trace 字段表 / navcmd / 控制台入口 / 增量读取 / 摘要 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
