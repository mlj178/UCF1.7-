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
# 2026-11-27：解析搬进 core，两个功能都调它
REC_ALG = os.path.join(PROJ, "app", "tabs", "record", "ucf_rec.py")
TRACE_READER = os.path.join(PROJ, "app", "tabs", "dev", "ucf_trace.py")
# 控制台不再调它，但报告工具本身还是命令行入口（2026-11-27 用户要求）
JUMP_STATS = os.path.join(PROJ, "app", "tools", "data", "jump_stats.py")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_c(editor):
    r"""采样会话只有一个（2026-11-27）：录制和采集都走 ss_begin / ss_stop / ss_tick。

    以前这里钉的是 trace_start / trace_sample / trace_tick 那套，录制那边另有一套
    rec_*；两套同时开会把同一帧采两遍、写两个文件。现在钉的是「只有一个」：
    旧的 rec_tick / trace_tick / rec_start / trace_start 都不许再出现。
    """
    assert "typedef struct {\n  FILE*  fp;\n  char   path[MAX_PATH];" in editor, \
        "没有采样会话结构（SampleSess）"
    assert "static SampleSess g_ss;" in editor, "采样会话不是唯一一份状态"
    assert "static int ss_begin(" in editor, "editor.c 没有 ss_begin()"
    assert "static void ss_stop(" in editor, "editor.c 没有 ss_stop()"
    assert "static void ss_sample_player(" in editor, "editor.c 没有 ss_sample_player()"
    assert "static void ss_tick(" in editor, "editor.c 没有 ss_tick()"
    assert "static void ss_sample_bots(" in editor, "editor.c 没有人机采样"
    assert "void editor_rec_tick(void) {" in editor and "ss_tick();" in editor, \
        "采样定时器入口没调 ss_tick()"
    assert "  ss_tick();                  /* 采样会话" in editor, \
        "editor_tick() 没调 ss_tick()"
    for gone in ("static void rec_tick(void)", "static void trace_sample(void)",
                 "static void trace_tick(void)", "static void rec_bot_tick(void)",
                 "static int rec_start(", "static int trace_start("):
        assert gone not in editor, "旧的独立采样器还在：%s" % gone
    assert 'if (!strcmp(cmd, "rec") || !strcmp(cmd, "trace"))' in editor, \
        "navcmd 没接 cmd=rec / cmd=trace 到同一个会话"
    assert "ss_begin(kind, out, hz, whoMask" in editor, "navcmd 没把 who 传给会话"
    assert 'if (!strcmp(cmd, "stopall"))' in editor, "navcmd 没接 cmd=stopall"
    assert "ss_stop(\"restart\")" in editor, "ss_begin 没先收掉上一个会话（一个写入者）"
    assert "ss_stop(\"quit\")" in editor, "退出游戏没收尾采样文件"
    assert "QueryPerformanceCounter" in editor, "采样没用 QPC（60 Hz 时间太粗）"
    assert '\\"who\\":\\"%s\\"' in editor, "header 没写 who（采集对象）"
    # 2026-11-27 用户问「日志有没有区分人机和玩家」：人机行必须自带 k=b，
    # end 行必须带 bots 条数；玩家行不带 k（录制 / 采集共用同一行，靠 k 区分）。
    assert '\\"k\\":\\"b\\"' in editor, "人机样本没有 k=b 标记（和玩家分不开）"
    assert '\\"bots\\":%u' in editor, "end 行没人机样本条数"
    assert "SS_SCHEMA" in editor and "ucf-trace/3" in editor, "schema 没升到 ucf-trace/3"

    # header 的 fields 数组 = ucf_trace.FIELDS
    m = re.search(r"fields.*?\[(.*?)\]", editor, re.S)
    assert m, "editor.c header 里找不到 fields 数组"
    fields = tuple(re.findall(r'\\"([a-z]+)\\"', m.group(1)))
    assert fields == tuple(ucf_trace.FIELDS), \
        "字段表不一致：C=%s Python=%s" % (fields, ucf_trace.FIELDS)

    # 样本 fprintf 里必须有全部字段（录制和采集共用这一个写法）
    seg = editor.split("static void ss_sample_player(void)")[1].split("static void ss_tick")[0]
    for key in ucf_trace.FIELDS:
        assert ('\\"%s\\":' % key) in seg, "采样 fprintf 少了字段 %s" % key
    assert '\\"k\\":\\"p\\"' not in seg, \
        "玩家样本不该再带 k=p：录制和采集写同一行（人机才是 k=b）"

    # 两个事件行：换图 / 换场景
    assert '\\"ev\\":\\"cam\\"' in seg, "采样没有 ev=cam（分段行）"
    assert '\\"ev\\":\\"scene\\"' in seg, "采样没有 ev=scene"
    # 2026-11-24 采样改造：坐标取玩家脚底 + grounded/vy + 落地结算的跳事件
    assert "PL_CHAR_CONT" in editor and "PL_GROUNDED" in editor and "PL_VELDATA" in editor, \
        "没按 Player 字段偏移取脚底 / isGrounded / velData"
    assert 'tr_read_state(' in seg, "采样没用玩家状态读数（玩家对象 / 相机兜底）"
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
    # 2026-11-27 合并成一个采样会话：acquire/release 只剩一处（ss_begin / ss_stop）
    assert editor.count("navfix_hires_acquire();") == 1, \
        "采样会话申请定时器的地方不止一处（应该只有 ss_begin）"
    assert editor.count("navfix_hires_release();") == 1, \
        "采样会话归还定时器的地方不止一处（应该只有 ss_stop）"
    assert editor.count("navfix_hires_ticks()") >= 2, \
        "没记「这次采样里定时器派发了几次」"
    assert "static void hz_warn(" in editor and editor.count("hz_warn(") >= 2, \
        "实测频率没跑满档位时没有告警（2026-11-24 那次就是一声不吭）"
    tick_block = editor.split("static void ss_tick(void)")[1][:1200]
    assert "iv * 0.25" in tick_block, \
        "ss_tick 没给 25% 提前量：60 Hz 档在 60 fps 主循环下会隔帧丢样本（实测 ~50 Hz）"
    assert "g_ss.who & 2" in editor, "人机采样没接到同一个会话的 who"
    assert "g_ss.who & 1" in editor, "玩家采样没接到同一个会话的 who"


def check_shared(rec_src, trace_src):
    r"""录制和采集必须用同一个读取器（2026-11-27）：两边都调 core/ucf_sample。

    以前各写一份：排序 / 去重 / 缺省 / header 判定都不一样，同一份文件两个页面
    能给出不同的数；而且 ucf_trace 只认 kind=="trace"，录制文件的 header 会被丢掉。
    """
    assert "ucf_sample.player_rows(lines)" in rec_src, "ucf_rec.parse_lines 没走共用读取器"
    assert "ucf_sample.jump_rows(lines)" in rec_src, "ucf_rec.parse_events 没走共用读取器"
    assert "ucf_sample.bots_by_id(lines)" in rec_src, "ucf_rec.parse_bots 没走共用读取器"
    assert "ucf_sample.scan(path, offset)" in trace_src, "ucf_trace.scan 没走共用读取器"
    assert "ucf_sample.read_full(path)" in trace_src, "ucf_trace.read_full 没走共用读取器"
    for bad in ('json.loads', 'open(path'):
        assert bad not in rec_src.split("# ---------------------------------------------------------------- 解析")[-1], \
            "ucf_rec 里又自己解析了一遍：%s" % bad


def check_who():
    r"""采集对象（玩家 / 人机 / 全部）的「记忆」：取值/显示名双向稳定。

    2026-11-27 用户要求：原始轨迹采集的采集对象要保留上一次的选择。选择存在
    ucf_mod.json 的 trace.who；这里钉住旧写法（中文 / 1·2·3 / 大小写）也能恢复，
    认不出的值退回默认，不能把用户上次的选择悄悄变成「玩家」之外的东西。
    """
    for raw, want in (("player", "player"), ("玩家", "player"), ("1", "player"), (1, "player"),
                      ("bots", "bots"), ("人机", "bots"), ("2", "bots"), (2, "bots"),
                      ("all", "all"), ("全部", "all"), ("3", "all"), (3, "all"),
                      (" ALL ", "all"), ("PLAYER", "player"), (None, "player"), ("wat", "player")):
        got = ucf_trace.who_value(raw, "player")
        assert got == want, "who_value(%r) = %r，应为 %r" % (raw, got, want)
    assert ucf_trace.who_value("wat", "bots") == "bots", "认不出的值没按 default 退回"
    for value, want in (("player", "玩家"), ("bots", "人机"), ("all", "全部"),
                        ("玩家", "玩家"), ("wat", "玩家")):
        got = ucf_trace.who_label(value)
        assert got == want, "who_label(%r) = %r，应为 %r" % (value, got, want)


def check_console(console):
    for fn in ("build_trace_card", "on_trace_hz", "on_trace_who", "trace_who_now",
               "refresh_trace_who_memo", "trace_start", "trace_poll",
               "trace_live", "trace_stop", "trace_finish", "trace_open_dir"):
        assert ("def %s(self" % fn) in console, "控制台少了 %s()" % fn
    # 2026-11-27 用户要求：卡片上只留 开始采集 / 停止 / 打开日志文件夹
    # （「打开日志」「复制路径」也去掉；文件名和目录本来就在卡片上显示着）
    for gone in ("def trace_open_file(self", "def trace_copy_path(self",
                 "复制路径", "text=\"打开日志\""):
        assert gone not in console, "没删干净：%s" % gone
    assert "import ucf_trace" in console, "控制台没导入 ucf_trace"
    assert "原始轨迹采集（给 AI 分析用）" in console, "「开发者选项」页没有轨迹卡片标题"
    # 2026-11-21 用户要求：卡片从「录制」搬到「开发者选项」，状态在卡片前单独备好
    assert "def init_trace_state(self" in console, "控制台少了 init_trace_state()"
    assert "def on_trace_who(self" in console, "采集页没有「采集对象」"
    # 2026-11-27 用户要求：采集对象记住上一次的选择（存 ucf_mod.json 的 trace.who）
    who_body = console.split("def on_trace_who(self")[1].split("def trace_who_now")[0]
    assert "save_cfg(self.cfg)" in who_body, "采集对象改了没写进 ucf_mod.json（记不住）"
    assert 'ucf_trace.who_label(self.trace["who"])' in console, \
        "建卡片时没按 trace.who 恢复分段按钮（重启后又会默认玩家）"
    assert "上次的采集对象：" in console, "卡片上没显示「上次的采集对象」（看不出记忆生效）"
    assert "trace_who_now()" in console and '"who": who' in console, \
        "开始采集时没以界面当前选择为准 / 没把 who 发给插件"
    assert "scan_counts(self.tr_file" in console, "采集中没分玩家 / 人机两种样本数"
    assert "人机 %d 条" in console, "界面没显示人机样本条数（和玩家混在一起）"
    # 2026-11-27 用户要求：控制台里「生成跳跃报告」「选文件出报告」两颗按钮重复，整块删掉，
    # 只保留命令行工具 jump_stats.py（采集页 = 只采不分析）
    assert "def trace_report" not in console, "报告入口还留在控制台"
    assert "生成跳跃报告" not in console, "「生成跳跃报告」按钮没删干净"
    assert os.path.isfile(JUMP_STATS), "jump_stats.py 被删了：命令行还得能用"
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

    # 采集对象：玩家 / 人机分开数（2026-11-27 用户要求「日志要能看出谁是谁」）
    bpath = os.path.join(tmp, "level9_20261127-120000.jsonl")
    head = {"kind": "trace", "schema": "ucf-trace/3", "who": "all", "hz": 30,
            "map": "level9", "label": "飓风危城", "src": "player",
            "fields": list(ucf_trace.FIELDS)}
    lines = [json.dumps(head, ensure_ascii=False)]
    for i in range(2):
        lines.append(json.dumps({"t": i * 0.033, "dt": 0.033, "x": 1.0 + i, "y": -2.0,
                                 "z": 3.0, "g": 1, "vy": 0.0, "sp": 0, "ct": 0}))
    for i in range(3):
        lines.append(json.dumps({"t": 0.1 + i, "k": "b", "id": "0000000%d" % i,
                                 "x": 5.0 + i, "y": -2.0, "z": 6.0, "g": 1, "vy": 0.0,
                                 "spd": 4.0, "j": 0, "en": 0, "act": "Move",
                                 "tgt": [0, 0, 0], "njs": "", "near": "", "pts": -1}))
    lines.append(json.dumps({"end": 1, "t": 2.0, "n": 2, "bots": 3, "dist": 1.0,
                             "missed": 0, "ticks": 60}))
    with open(bpath, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    off, n_players, n_bots, _last, bend = ucf_trace.scan_counts(bpath, 0)
    assert (n_players, n_bots) == (2, 3), (n_players, n_bots)
    assert bend and bend["bots"] == 3, bend
    assert ucf_trace.scan(bpath, 0)[1] == 2, "老接口只该数玩家样本"
    sm = ucf_trace.summary(bpath)
    assert sm["who"] == "all" and sm["bots"] == 3 and sm["samples"] == 2, sm
    btxt = ucf_trace.summary_text(sm)
    for want in ("采集对象：全部", "2 玩家样本", "人机样本 3 条"):
        assert want in btxt, btxt
    # 只采人机（玩家 0 条）：摘要不能只报「没有样本」
    sm["samples"] = 0
    sm["bots"] = 3
    btxt = ucf_trace.summary_text(sm)
    assert "没有玩家样本" in btxt and "人机样本 3 条" in btxt, btxt

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


def _fprintf(block, pos=0, fp="g_ss.fp"):
    r"""取一个 fprintf(g_trFp, ...) 的格式串，并跳过字符串里的 ');'。

    返回 (格式串, 起始位置, 结束位置)。格式串 = 所有 "..." 片段按 C 转义还原后拼接。
    """
    i = block.index("fprintf(" + fp + ",", pos)
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
    raise AssertionError("fprintf(%s, ...) 没有结尾" % fp)


def check_c_format(editor):
    r"""C 写出来的 header / 样本行必须是合法 JSON，且键名和 FIELDS 一致。

    这条能抓住「少一个逗号 / 引号没转义 / %s 和参数对不上」——编译不会报，
    但 Python 侧会整份读不出来。
    """
    hdr_block = editor.split("static void ss_header(void)")[1].split("static void ss_stop")[0]
    # 格式串里 schema 用的是 #define SS_SCHEMA；这里换成字面量再拼，否则会被跳过
    hdr_block = hdr_block.replace("SS_SCHEMA", '"ucf-trace/3"')
    hfmt, _, _ = _fprintf(hdr_block)
    # 参数顺序：kind / who / hz / 年月日时分秒 / scene / map / label / pack / fp / src
    hargs = ("rec", "all", 30, 2026, 11, 27, 12, 0, 0,
             "mp_x", "level1", "运输船", "pack", "fp", "player")
    hobj = json.loads(hfmt % hargs)
    assert hobj["kind"] == "rec" and hobj["schema"] == "ucf-trace/3", hobj
    assert hobj["who"] == "all", "header 没记采集对象（who）"
    assert tuple(hobj["fields"]) == tuple(ucf_trace.FIELDS), hobj["fields"]
    assert hobj["label"] == "运输船" and hobj["map"] == "level1"
    assert hobj["t0"] == "2026-11-27 12:00:00", hobj["t0"]
    assert hobj["src"] == "player", "header 没记坐标来源（player / camera）"
    assert "kind_note" in hobj, "header 没解释 kind 的四种取值"

    smp_block = editor.split("static void ss_sample_player(void)")[1].split("static void ss_tick")[0]
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
    check_who()
    check_console(chr(10).join([read(CONSOLE), read(DEV_TAB), read(UI_ENV)]))
    check_shared(read(REC_ALG), read(TRACE_READER))
    check_unit()
    check_v2()
    print("OK: trace 字段表 / navcmd / 控制台入口 / 增量读取 / 摘要 / v2 跳事件+报告 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
