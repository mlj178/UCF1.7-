#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""全量语法自检：app 下每个 .py / .pyw 都能编译。

为什么单独有这一条：界面模块（tabs\*.py、控制台.pyw）在别的自检里**不会被 import**
（要么要 tkinter 窗口、要么要游戏进程），所以写坏一个字符串转义（比如路径里的
"\u"）能让控制台双击直接闪退，而 28 个自检全绿。
2026-11-27 就这么把控制台弄崩过一次（"run\build\..." 里的 \u 是非法转义）。

跑法：python tests/test_syntax.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)

SKIP_DIRS = {"__pycache__", ".venv", "node_modules"}


def main():
    app = os.path.join(UCF_ROOT, "app")
    bad = []
    n = 0
    for root, dirs, files in os.walk(app):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if not (name.endswith(".py") or name.endswith(".pyw")):
                continue
            path = os.path.join(root, name)
            n += 1
            try:
                with open(path, "rb") as f:
                    compile(f.read(), path, "exec")
            except SyntaxError as exc:
                bad.append("%s:%s: %s" % (os.path.relpath(path, UCF_ROOT), exc.lineno, exc.msg))
            except ValueError as exc:
                bad.append("%s: %s" % (os.path.relpath(path, UCF_ROOT), exc))
    if bad:
        print("语法错误 %d 处：" % len(bad))
        for b in bad:
            print("  " + b)
        return 1
    print("OK: %d 个 .py/.pyw 全部编译通过" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
