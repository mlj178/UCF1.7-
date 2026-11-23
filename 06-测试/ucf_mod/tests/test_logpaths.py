#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：日志三级查找（工程端 log 为主，部署端两级兜底）。

为什么要有它：2026-11-23 把日志从游戏目录收进「工程端 log」，再用环境变量
UCF_LOG_DIR 把插件指过去 —— 日常游戏目录里不再生成日志。三层必须都对：

    1) 工程端 log\           控制台注入 UCF_LOG_DIR 时插件的落点（日常）
    2) <部署端>\log\         没走控制台启动、或别人只有部署包时
    3) <部署端>\             更老的部署（没有 log 子目录）

本测试只读源码 + 临时目录，不需要游戏、窗口或网络。

跑法：python tests/test_logpaths.py
"""
import importlib.util
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记
PROJ = UCF_ROOT
for _p in (os.path.join(PROJ, "core"), os.path.join(PROJ, "console"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

FAIL = []


def check(ok, what):
    if ok:
        print("  OK   " + what)
    else:
        FAIL.append(what)
        print("  !!   " + what)


def read(rel):
    with open(os.path.join(PROJ, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def load_console():
    spec = importlib.util.spec_from_file_location(
        "ucf_console_logpaths", os.path.join(PROJ, "console", "控制台.pyw"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def touch(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("x\n")


def main():
    tmp = tempfile.mkdtemp(prefix="ucf_logpath_")
    try:
        print("== 1) C 侧：UCF_LOG_DIR 优先 + 建目录 + 轮转 ==")
        h = read(os.path.join("src", "cfg.h"))
        c = read(os.path.join("src", "cfg.c"))
        check("ucf_log_file" in h and "ucf_log_dir" in h, "cfg.h 声明了日志路径助手")
        check("ucf_mkdir_p" in h, "cfg.h 声明了逐级建目录（工程端可能是多层路径）")
        check("UCF_LOG_DIR" in c, "cfg.c 读 UCF_LOG_DIR（控制台注入）")
        check("ucf_log_rotate" in h, "cfg.h 声明了 16 MB 轮转")
        editor = read(os.path.join("src", "editor.c"))
        check('ucf_log_file(g_pmPath' in editor, "editor.c 的 player_marks.txt 也走日志目录")
        check("static void mkdir_p" not in editor, "editor.c 不再自己实现 mkdir_p（统一用 ucf_mkdir_p）")
        at = read(os.path.join("src", "autotest.c"))
        check('ucf_log_file(g_atTxt' in at, "autotest.c 的 autotest.txt 也走日志目录")
        pl = read(os.path.join("src", "plugin.c"))
        check("log: dir=" in pl, "插件启动第一行写明日志落点（env/fallback）")
        proxy = read(os.path.join("src", "proxy", "proxy.c"))
        check('MOD_DIR "log' in proxy, "加载器失败日志也进日志目录")

        print("== 2) 控制台：三级查找 ==")
        con = load_console()
        check(os.path.dirname(con.PMARK_TXT) == con.LOG_DIR, "PMARK_TXT 在日志目录里")
        check(os.path.dirname(con.AUTOTEST_TXT) == con.LOG_DIR, "AUTOTEST_TXT 在日志目录里")
        check(os.path.normcase(con.LOG_DIR) == os.path.normcase(os.path.join(PROJ, "log")),
              "日志主目录 = 工程端 log")

        game = os.path.join(tmp, "game")            # 假装是部署端
        con.DEPLOY = game
        con.LOG_DIR = os.path.join(tmp, "proj", "log")
        con.GAME_LOG_DIR = os.path.join(game, "log")
        p1 = os.path.join(con.LOG_DIR, "ucf_mod.log")
        p2 = os.path.join(con.GAME_LOG_DIR, "ucf_mod.log")
        p3 = os.path.join(game, "ucf_mod.log")

        touch(p3)
        check(con.find_log("ucf_mod.log") == p3, "只有部署端根目录 -> 读那份（最老）")
        touch(p2)
        check(con.find_log("ucf_mod.log") == p2, "有部署端 log\\ -> 优先它")
        touch(p1)
        check(con.find_log("ucf_mod.log") == p1, "有工程端 log\\ -> 优先它（日常）")
        for f in (p1, p2, p3):
            os.remove(f)
        check(con.find_log("ucf_mod.log") == p1, "都没有 -> 指向工程端 log（写时自建）")

        print("== 3) navserver：同样三级 ==")
        import navserver as S
        S.LOG_FILE = p1
        S.GAME_LOG_DIR = con.GAME_LOG_DIR
        S.UCF = game
        check(S.log_file() == p1, "都没有 -> 工程端 log")
        touch(p3)
        check(S.log_file() == p3, "只有部署端根目录 -> 读那份")
        touch(p2)
        check(S.log_file() == p2, "有部署端 log\\ -> 优先它")
        touch(p1)
        check(S.log_file() == p1, "有工程端 log\\ -> 优先它")

        print("== 4) 启动通道都注入了 UCF_LOG_DIR ==")
        con_src = read(os.path.join("console", "控制台.pyw"))
        check('env["UCF_LOG_DIR"] = LOG_DIR' in con_src, "控制台启动游戏时注入 UCF_LOG_DIR")
        pw = read(os.path.join("tools", "autotest.ps1"))
        check("UCF_LOG_DIR" in pw, "命令行 autotest.ps1 也注入（否则车测日志会落回游戏端）")
        gi = read(".gitignore")
        check("log/" in gi, ".gitignore 忽略 log/")

        print("== 5) 卸载照旧清理三个位置 ==")
        un = read(os.path.join("payload", "ucf_mod", "uninstall.ps1"))
        check("'log'" in un, "uninstall.ps1 会删 log 目录")
        check("ucf_mod.prev_*.log" in un, "uninstall.ps1 认得车测的 prev_*.log")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if FAIL:
        print("")
        print("!! %d 项没过" % len(FAIL))
        for x in FAIL:
            print("   - " + x)
        return 1
    print("")
    print("OK: 日志三级查找（工程端 log / 部署端 log / 部署端根）+ 注入 + 轮转 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())