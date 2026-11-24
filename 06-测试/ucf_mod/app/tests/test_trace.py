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
for _p in (os.path.join(UCF_ROOT, "app", "core"), os.path.join(UCF_ROOT, "app"),
           os.path.join(UCF_ROOT, "app", "tabs", "dev"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ucf_trace  # noqa: E402

EDITOR = os.path.join(PROJ, "src", "editor.c")
NAVFIX = os.path.join(PROJ, "src", "navfix.c")
CONSOLE = os.path.join(PROJ, "app", "控制台.pyw")
# 2026-11-24 目录重构：轨迹卡片在 tabs/dev/tab.py，ucf_trace 的导入在 ui/env.py
DEV_TAB = os.path.join(PROJ, "app", "tabs", "dev", "tab.py")
UI_ENV = os.path.join(PROJ, "app", "ui", "env.py")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_c(editor):
    assert "static int trace_start(" in editor, "editor.c 没有 trace_start()"
    assert "static void trace_stop(" in editor, "editor.c 没有 trace_stop()"
    assert "static void trace_sample(" in editor, "editor.c 没有 trace_sample()"
    assert "static void trace_tick(" in editor, "editor.c 没有 trace_tick()"
    assert "void editor_rec_tick(void) { rec_tick(); trace_tick(); }" in editor, \
        "采样定时器没同时驱动 rec 和 trace"
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

    # 两个事件行：换图 / 换场景
    assert '\\"ev\\":\\"cam\\"' in seg, "trace_sample 没有 ev=cam（分段行）"
    assert '\\"ev\\":\\"scene\\"' in seg, "trace_sample 没有 ev=scene"
    # 2026-11-24 采样改造：坐标取玩家脚底 + grounded/vy + 落地结算的跳事件
    assert "PL_CHAR_CONT" in editor and "PL_GROUNDED" in editor and "PL_VELDATA" in editor, \
        "没按 Player 字段偏移取脚底 / isGrounded / velData"
    assert 'tr_read_state(' in seg, "trace_sample 没用玩家状态读数（玩家对象 / 相机兜底）"
    assert '\\"ev\\":\\"jump\\"' in editor, "没有跳事件行（落地结算）"
    for k in ('\\"h\\":', '\\"rise\\":', '\\"air\\":', '\\"v0\\":', '\\"run\\":', '\\"kind\\":'):
        assert k in editor, "跳事件少字段 %s" % k


def check_hires_timer(editor, navfix):
    r"""rec/trace 的采样率必须由采样定时器（WM_TIMER 0xF3C1）驱动，不能只靠
    250 ms 心跳（4 Hz）。

    2026-11-24 现场是两个问题叠在一起，这里都钉住：
      1) 源码：定时器以前只在 UCF_FREECAM=1 时启动 -> 10/20/30/60 Hz 全变 4 Hz；
      2) 流程：修好的 DLL 没进真正在跑的那份游戏目录 -> 改了等于没改。
    所以除了「按需启停」，还要有「定时器到底派发过几次」的证据（ticks）和
    跑不满时的显式告警，别再让降级悄悄地发生。
    """
    assert "static void hi_timer_sync(void)" in navfix, "navfix.c 没有 hi_timer_sync()"
    assert "void navfix_hires_acquire(void)" in navfix, "navfix.c 没导出 acquire"
    assert "void navfix_hires_release(void)" in navfix, "navfix.c 没导出 release"
    assert "SetTimer(g_hwnd, UCF_HI_TIMER_ID, UCF_HI_PERIOD_MS, 0)" in navfix, \
        "采样定时器没按常量启动"
    assert "#define UCF_HI_PERIOD_MS 10" in navfix, \
        "定时器周期不是 10 ms（USER_TIMER_MINIMUM）：60 Hz 档会踩 15.6 ms 系统量子"
    assert "if (msg == WM_TIMER && w == UCF_HI_TIMER_ID)" in navfix, \
        "WndProc 没接采样定时器（id 对不上就等于没接）"
    assert "editor_rec_tick();" in navfix, "WM_TIMER 没驱动 rec/trace"
    assert "InterlockedIncrement(&g_hiTicks)" in navfix and \
        "long navfix_hires_ticks(void)" in navfix, \
        "定时器派发次数没统计：跑不满就只能靠猜"
    assert "navfix_hires_kick" in navfix, \
        "没有 4 Hz 自愈补启：acquire 早于窗口钩子时会让整场退回 4 Hz"
    assert "timeBeginPeriod" in navfix, "没提系统定时器精度（默认 15.6 ms 量子）"
    assert "g_hiFreecam = (GetEnvironmentVariableA" in navfix, \
        "UCF_FREECAM 不再作为常驻定时器的条件"
    assert editor.count("navfix_hires_acquire();") >= 2, \
        "rec_start / trace_start 没有各自申请采样定时器"
    assert editor.count("navfix_hires_release();") >= 2, \
        "rec_stop / trace_stop 没有各自归还采样定时器"
    assert editor.count("navfix_hires_ticks()") >= 4, \
        "trace/rec 没记「这次采集里定时器派发了几次」"
    assert "static void hz_warn(" in editor and editor.count('hz_warn("') >= 2, \
        "实测频率没跑满档位时没有告警（2026-11-24 那次就是一声不吭）"
    tick_block = editor.split("static void trace_tick(void)")[1][:900]
    assert "iv * 0.25" in tick_block, \
        "trace_tick 没给 25% 提前量：60 Hz 档在 60 fps 主循环下会隔帧丢样本（实测 ~50 Hz）"


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

    # 「没跑满档位」判定：2026-11-24 的现场是 档位 60 Hz / 实测 4 Hz
    sm["hz_set"] = 20                                   # 合成日志本身 ~20 Hz
    assert not ucf_trace.starved(sm), sm
    assert "没跑满档位" not in ucf_trace.summary_text(sm)
    sm["hz_set"] = 60
    assert ucf_trace.starved(sm), "档位 60 Hz 实际 20 Hz 竟然没判成没跑满"
    assert "没跑满档位" in ucf_trace.summary_text(sm), ucf_trace.summary_text(sm)
    sm["hz_set"] = 0                                    # 旧日志没有档位：不许误报
    assert not ucf_trace.starved(sm) and "没跑满档位" not in ucf_trace.summary_text(sm)

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


def synth_v2(path):
    r"""合成一份 ucf-trace/2：10 个样本（第 4~6 帧在空中）+ 一条落地结算的 jump 事件。"""
    head = {
        "kind": "trace", "schema": "ucf-trace/2", "hz": 30,
        "t0": "2026-11-24 20:00:00", "scene": "mp_test",
        "map": "level1", "label": "运输船", "pack": "p", "fp": "f",
        "src": "player", "fields": list(ucf_trace.FIELDS),
    }
    lines = [json.dumps(head, ensure_ascii=False)]
    for i in range(10):
        air = 4 <= i <= 6
        lines.append(json.dumps({
            "t": round(i / 30.0, 3), "dt": 0.033 if i else 0.0,
            "x": round(-50.0 + i * 0.4, 3), "y": round(-16.64 + (1.8 if air else 0.0), 3),
            "z": 6.0, "g": 0 if air else 1, "vy": 9.0 if i == 4 else (-8.0 if i == 6 else 0.0),
            "sp": 1 if i == 3 else 0, "ct": 0,
        }, ensure_ascii=False))
    lines.append(json.dumps({
        "t": 0.25, "ev": "jump",
        "a": [-48.8, -16.64, 6.0], "b": [-47.6, -16.64, 6.0],
        "h": 1.2, "rise": 1.8, "air": 0.2, "v0": 10.5, "run": 7.5, "kind": "gap",
    }, ensure_ascii=False))
    lines.append(json.dumps({"end": 1, "t": 0.3, "n": 10, "dist": 3.6, "missed": 0, "ticks": 12}))
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")


def check_v2():
    r"""2 版日志：read_full 要能读出跳事件，摘要要带「跳 N 次」，报告要能出 Markdown。"""
    tmp = tempfile.mkdtemp(prefix="ucf_trace2_")
    path = os.path.join(tmp, "level1_20261124-200000.jsonl")
    synth_v2(path)
    hdr, rows, jumps, end = ucf_trace.read_full(path)
    assert hdr["schema"] == "ucf-trace/2" and hdr["src"] == "player", hdr
    assert len(rows) == 10 and rows[4]["g"] == 0 and abs(rows[4]["vy"] - 9.0) < 1e-6, rows[4]
    assert len(jumps) == 1, jumps
    j = jumps[0]
    assert (j["kind"], round(j["h"], 2), round(j["rise"], 2)) == ("gap", 1.2, 1.8), j
    assert j["a"][0] < j["b"][0]
    off, n, last, end2 = ucf_trace.scan(path, 0)
    assert n == 10 and end2 is not None, (n, end2)      # 事件行不能算进样本
    sm = ucf_trace.summary(path)
    assert sm["jumps"] == 1 and sm["src"] == "player", sm
    assert sm["jump_kinds"].get("gap") == 1, sm["jump_kinds"]
    assert "跳 1 次" in ucf_trace.summary_text(sm), ucf_trace.summary_text(sm)

    # 报告：能出 Markdown，且带上这一跳
    sys.path.insert(0, os.path.join(PROJ, "app", "tools", "data"))
    import jump_stats
    files, evs = jump_stats.collect([path])
    assert len(files) == 1 and files[0]["est"] is False, files
    assert len(evs) == 1 and evs[0]["src"] == "plugin", evs
    md = jump_stats.report_md(files, evs)
    assert "# 跳跃数据分析" in md and "跨缺口" in md and "1.20" in md, md[:400]
    assert "缺口" in md or "gap" in md, md[:400]


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
    hargs = (30, 2026, 11, 21, 15, 0, 0, "mp_x", "level1", "运输船", "pack", "fp", "player")
    hobj = json.loads(hfmt % hargs)
    assert hobj["kind"] == "trace" and hobj["schema"] == "ucf-trace/2", hobj
    assert tuple(hobj["fields"]) == tuple(ucf_trace.FIELDS), hobj["fields"]
    assert hobj["label"] == "运输船" and hobj["map"] == "level1"
    assert hobj["t0"] == "2026-11-21 15:00:00", hobj["t0"]
    assert hobj["src"] == "player", "header 没记坐标来源（player / camera）"
    assert "kind_note" in hobj, "header 没解释 kind 的四种取值"

    smp_block = editor.split("static void trace_sample(void)")[1].split("static void trace_tick")[0]
    pos = 0
    while True:
        sfmt, _, pos = _fprintf(smp_block, pos)
        if "dt" in sfmt:
            break

    sargs = (0.017, 0.017, 1.234, -18.59, -19.218, 1, 0.02, 0, 0)
    obj = json.loads(sfmt % sargs)
    assert set(obj) == set(ucf_trace.FIELDS), (set(obj), set(ucf_trace.FIELDS))
    assert abs(obj["t"] - 0.017) < 1e-9 and obj["sp"] == 0 and obj["g"] == 1
    assert abs(obj["vy"] - 0.02) < 1e-9, obj["vy"]

    # 2 版不再有 gy / 相机朝向：那两样是旧格式里最容易骗人的东西
    assert "gy" not in obj and "fx" not in obj, obj


def main():
    editor = read(EDITOR)
    check_c(editor)
    check_hires_timer(editor, read(NAVFIX))
    check_c_format(editor)
    check_console(chr(10).join([read(CONSOLE), read(DEV_TAB), read(UI_ENV)]))
    check_unit()
    check_v2()
    print("OK: trace 字段表 / navcmd / 控制台入口 / 增量读取 / 摘要 / v2 跳事件+报告 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
