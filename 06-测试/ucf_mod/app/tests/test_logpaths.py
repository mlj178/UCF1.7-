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

# 自检会 import ui.env -> navdata，而 navdata 一 import 就会把 stdout 抄进 log\navdata.log。
# 关掉抄写，免得跑一次测试就往真日志里糊一屏 OK（也会连带触发老位置迁移）。
os.environ["UCF_NO_LOG_TEE"] = "1"

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记
PROJ = UCF_ROOT
for _p in (os.path.join(PROJ, "app", "core"), os.path.join(PROJ, "app"),
           os.path.join(PROJ, "app", "workbench"), HERE):
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
        "ucf_console_logpaths", os.path.join(PROJ, "app", "控制台.pyw"))
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
        check("UCF_MOD_DLL" in proxy, "加载器只认控制台注入的 UCF_MOD_DLL")
        check("GetTempPathA" in proxy and "ucf_mod_proxy.log" in proxy,
              "加载器载入失败只写 %TEMP%，不碰游戏目录")
        check("MOD_DIR" not in proxy, "加载器不再引用游戏目录 ucf_mod\\")

        print("== 2) 控制台：三级查找 ==")
        # 2026-11-24 目录重构：常量在 app/ui/env.py，find_log 在 app/ui/util.py
        import ui.env as E
        import ui.util as U
        check(os.path.dirname(E.PMARK_TXT) == E.LOG_DIR, "PMARK_TXT 在日志目录里")
        check(os.path.dirname(E.AUTOTEST_TXT) == E.LOG_DIR, "AUTOTEST_TXT 在日志目录里")
        check(os.path.normcase(E.LOG_DIR) == os.path.normcase(os.path.join(PROJ, "log")),
              "日志主目录 = 工程端 log")

        game = os.path.join(tmp, "game")            # 假装是部署端
        U.DEPLOY = game
        U.LOG_DIR = os.path.join(tmp, "proj", "log")
        U.GAME_LOG_DIR = os.path.join(game, "log")
        p1 = os.path.join(U.LOG_DIR, "ucf_mod.log")
        p2 = os.path.join(U.GAME_LOG_DIR, "ucf_mod.log")
        p3 = os.path.join(game, "ucf_mod.log")

        touch(p3)
        check(U.find_log("ucf_mod.log") == p3, "只有部署端根目录 -> 读那份（最老）")
        touch(p2)
        check(U.find_log("ucf_mod.log") == p2, "有部署端 log\\ -> 优先它")
        touch(p1)
        check(U.find_log("ucf_mod.log") == p1, "有工程端 log\\ -> 优先它（日常）")
        for f in (p1, p2, p3):
            os.remove(f)
        check(U.find_log("ucf_mod.log") == p1, "都没有 -> 指向工程端 log（写时自建）")

        print("== 3) navserver：同样三级 ==")
        import navserver as S
        S.LOG_FILE = p1
        S.GAME_LOG_DIR = U.GAME_LOG_DIR
        S.UCF = game
        check(S.log_file() == p1, "都没有 -> 工程端 log")
        touch(p3)
        check(S.log_file() == p3, "只有部署端根目录 -> 读那份")
        touch(p2)
        check(S.log_file() == p2, "有部署端 log\\ -> 优先它")
        touch(p1)
        check(S.log_file() == p1, "有工程端 log\\ -> 优先它")

        print("== 4) 启动通道都注入了 UCF_LOG_DIR ==")
        con_src = read(os.path.join("app", "控制台.pyw"))
        check('env["UCF_LOG_DIR"] = LOG_DIR' in con_src, "控制台启动游戏时注入 UCF_LOG_DIR")
        pw = read(os.path.join("app", "tools", "autotest.ps1"))
        check("UCF_LOG_DIR" in pw, "命令行 autotest.ps1 也注入（否则车测日志会落回游戏端）")
        gi = read(".gitignore")
        check("log/" in gi, ".gitignore 忽略 log/")

        print("== 5) 卸载照旧清理三个位置 ==")
        un = read(os.path.join("run", "payload", "ucf_mod", "uninstall.ps1"))
        check("'log'" in un, "uninstall.ps1 会删 log 目录")
        check("ucf_mod.prev_*.log" in un, "uninstall.ps1 认得车测的 prev_*.log")

        print("== 6) 控制台 / 工具自己的日志也集中到 log\\ ==")
        # 2026-11-27：navdata.log 从 data/navdata/_logs/、publish.log 从 dev/final/ 收进 log/
        import navdata as ND
        check(os.path.normcase(ND.NAVDATA_LOG) ==
              os.path.normcase(os.path.join(PROJ, "log", "navdata.log")),
              "navdata.py 的 stdout 抄本 = 工程端 log/navdata.log")
        check(os.path.normcase(ND.PUBLISH_LOG) ==
              os.path.normcase(os.path.join(PROJ, "log", "publish.log")),
              "成品发布流水 = 工程端 log/publish.log")
        check(not hasattr(ND, "FINAL_PUBLISH_LOG"), "旧的 FINAL_PUBLISH_LOG 常量已移除（别再写回 final/）")
        check("UCF_NO_LOG_TEE" in read(os.path.join("app", "core", "navdata.py")),
              "自检可关掉日志抄写（UCF_NO_LOG_TEE）")

        # 轮转 + 老位置合并都真跑一遍（临时目录，不碰真日志）
        logs = os.path.join(tmp, "logs")
        os.makedirs(logs, exist_ok=True)
        big = os.path.join(logs, "navdata.log")
        with open(big, "wb") as f:
            f.write(b"x" * (ND.LOG_MAX_BYTES + 1))
        rotated = ND.rotate_log(big)
        check(rotated and os.path.isfile(os.path.join(logs, "navdata.prev.log")),
              "超过 16 MB 轮转成 navdata.prev.log（只保 1 代）")

        old_log = os.path.join(tmp, "old", "_logs", "navdata.log")
        new_log = os.path.join(logs, "merged.log")
        os.makedirs(os.path.dirname(old_log), exist_ok=True)
        with open(old_log, "w", encoding="utf-8") as f:
            f.write("legacy-line\n")
        saved = (ND.NAVDATA_LOG, ND.LEGACY_NAVDATA_LOG)
        ND.NAVDATA_LOG, ND.LEGACY_NAVDATA_LOG = new_log, old_log
        try:
            merged = ND.navdata_migrate_log()
        finally:
            ND.NAVDATA_LOG, ND.LEGACY_NAVDATA_LOG = saved
        with open(new_log, "r", encoding="utf-8") as f:
            got = f.read()
        check(merged and not os.path.exists(old_log) and got.endswith("legacy-line\n"),
              "老位置 data/navdata/_logs/ 的历史日志并进 log/（只做一次）")
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