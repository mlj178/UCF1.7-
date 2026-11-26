#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：控制台的定时链只能是「一条」，折叠时停、展开时续、关窗时摘。

2026-11-26 卡死的根因是定时链发散：
  - refresh_status 结尾自己 after(4000, self.refresh_status)；
  - _safe_status 又每 4 s 调一次 refresh_status。
两条叠在一起，每 tick 多一条链；跑十分钟能堆出上百条，
主线程永远走不出 refresh_status，窗口就「未响应」（事件日志 AppHangB1）。
折叠只是让它更明显：窗口收起来放一边，回来时链已经堆满。

本测试只读源码，不需要游戏 / 网络 / 窗口。跑法：
    python app/tests/test_console_timers.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)

CONSOLE = os.path.join(UCF_ROOT, "app", "控制台.pyw")
FAIL = []


def check(cond, what):
    print(("  OK   " if cond else "  !!   ") + what)
    if not cond:
        FAIL.append(what)


def read(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def func_body(src, name):
    r"""按缩进取出某个 def 的函数体（找到下一个缩进 <= def 的行就停）。"""
    lines = src.splitlines()
    out, inside, indent = [], False, 0
    for ln in lines:
        if not inside:
            m = re.match(r"^(\s*)def " + re.escape(name) + r"\(", ln)
            if m:
                inside = True
                indent = len(m.group(1))
            continue
        if ln.strip():
            cur = len(ln) - len(ln.lstrip())
            if cur <= indent:
                break
        out.append(ln)
    return "\n".join(out)


def main():
    src = read(CONSOLE)

    print("== 1) refresh_status 不再自己排程")
    rs = func_body(src, "refresh_status")
    check(bool(rs), "找到 refresh_status()")
    # 只认代码里的 self.after(；注释里提到旧写法不算（旧注释确实写着这一行）
    code = "\n".join(ln for ln in rs.splitlines() if not ln.strip().startswith("#"))
    check("self.after(" not in code,
          "refresh_status 里没有 self.after(...)（排程只允许 _safe_status 一处）")

    print("== 2) _safe_status 是唯一的状态链")
    ss = func_body(src, "_safe_status")
    check(bool(ss), "找到 _safe_status()")
    check(ss.count("self.after(") == 1,
          "_safe_status 里只有一处 self.after(...)（实际 %d）" % ss.count("self.after("))
    check("self._safe_status" in ss,
          "_safe_status 排的是自己（一条链）")
    check("STATUS_EVERY" in ss, "间隔走 STATUS_EVERY 常量")

    print("== 3) _start_status 去重 / _stop_status 能摘")
    st = func_body(src, "_start_status")
    check("_status_job" in st and "return" in st,
          "_start_status 看到已排队就 return（不会叠第二条链）")
    sp = func_body(src, "_stop_status")
    check("after_cancel" in sp, "_stop_status 用 after_cancel 摘定时器")

    print("== 4) 折叠停链、展开续链")
    tf = func_body(src, "toggle_fold")
    check(tf.count("self._stop_status()") == 1, "折叠分支停状态链")
    check(tf.count("self._stop_pump()") == 1, "折叠分支停建页链")
    check(tf.count("self._start_status()") == 1, "展开分支重启状态链")

    print("== 5) 折叠时建页链不再空转")
    pp = func_body(src, "_pump_pages")
    check('if getattr(self, "_folded", False):' in pp and
          re.search(r'if getattr\(self, "_folded", False\):\s*\n\s*return', pp) is not None,
          "折叠时 _pump_pages 直接 return（不再 after(500) 空转）")

    print("== 6) 关窗前摘掉两条链")
    oc = func_body(src, "on_close")
    check("self._stop_status()" in oc, "on_close 停状态链")
    check("self._stop_pump()" in oc, "on_close 停建页链")

    print("== 7) 启动入口走 _start_status")
    init = func_body(src, "__init__")
    check("self._start_status()" in init, "__init__ 用 _start_status() 起链")
    check("self._safe_status()" not in init, "__init__ 不再直接调 _safe_status()")

    if FAIL:
        print("\n!! %d 项没过" % len(FAIL))
        return 1
    print("\nOK: 定时链只有一条；折叠停 / 展开续 / 关窗摘")
    return 0


if __name__ == "__main__":
    sys.exit(main())
