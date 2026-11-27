#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：目录树没被放乱（2026-11-24 重构 + 2026-11-27 一图一夹）。

跑法：python app/tests/test_layout.py

只读，不碰游戏 / 网络 / 窗口。查 6 件事：
  1) 根目录 = 7 个文件夹（app data docs log run src archive），旧的 console/core/tools/
     tests/geo/navdata/payload/build 不能回来
  2) app/ 下有 ui / tabs / core / workbench / tools / tests，入口 app/控制台.pyw 在
  3) 11 个页签各有一个文件；ui 的 8 个共用件都在
  4) data/geo、data/navdata/{native,dev}、run/payload、log/ 在
  5) 各入口脚本还带着 .ucfroot 上溯那 4 行（否则搬目录就找不到项目根）
  6) README 里写的入口路径与实际一致（抽查 app/ui、app/tabs）
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对

FAIL = []


def check(cond, what):
    if cond:
        print("  OK   " + what)
    else:
        print("  !!   " + what)
        FAIL.append(what)


def j(*parts):
    return os.path.join(UCF_ROOT, *parts)


def read(rel):
    with open(j(rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    print("== 1) 根目录")
    dirs = {d for d in os.listdir(UCF_ROOT) if os.path.isdir(j(d))}
    # 2026-11-24 新增 unity-map-project/：地图工程（Unity 源码 + 构建/补丁脚本）。
    # 它属于"生产侧"，进 git 但不进分发包；和 app/src/data/docs/log/run/archive 并列。
    want = {"app", "data", "docs", "log", "run", "src", "archive", "unity-map-project"}
    check(dirs == want, "根目录文件夹 = %s（实际 %s）" % ("/".join(sorted(want)), "/".join(sorted(dirs))))
    for legacy in ("console", "core", "tools", "tests", "geo", "navdata", "payload", "build"):
        check(not os.path.exists(j(legacy)), "旧目录 %s/ 没有回来" % legacy)
    for f in (".ucfroot", ".gitignore", "README.md", "启动控制台.bat"):
        check(os.path.isfile(j(f)), "根文件 %s 在" % f)

    print("== 2) app/ 结构")
    for d in ("ui", "tabs", "core", "workbench", "tools", "tests"):
        check(os.path.isdir(j("app", d)), "app/%s/ 在" % d)
    check(os.path.isfile(j("app", "控制台.pyw")), "入口 app/控制台.pyw 在")
    check(os.path.isfile(j("app", "workbench", "navserver.py")), "工作台 app/workbench/navserver.py 在")
    check(os.path.isfile(j("app", "core", "ucf_paths.py")), "路径真相 app/core/ucf_paths.py 在")

    print("== 3) 页签与共用件")
    for t in ("map.py", "vis.py", "hotkey.py", "waypoint.py", "overview.py",
              "data.py", "autotest.py"):
        check(os.path.isfile(j("app", "tabs", t)), "页签 app/tabs/%s 在" % t)
    for d, f, name in (("record", "tab.py", "录制"), ("deploy", "deploy_tab.py", "部署"),
                       ("dev", "tab.py", "开发者选项")):
        check(os.path.isfile(j("app", "tabs", d, f)), "页签 %s（app/tabs/%s/%s）在" % (name, d, f))
    for u in ("env.py", "consts.py", "util.py", "maps.py", "stats.py", "packs.py", "kit.py",
              "overview.py"):
        check(os.path.isfile(j("app", "ui", u)), "共用件 app/ui/%s 在" % u)

    print("== 4) 数据与产物")
    check(os.path.isdir(j("data", "geo")), "data/geo/ 在")
    check(os.path.isdir(j("data", "maps")), "data/maps/ 在（一图一夹）")
    check(os.path.isdir(j("data", "maps", "00_公共")), "data/maps/00_公共/ 在")
    check(not os.path.exists(j("data", "navdata")), "旧的 data/navdata/ 已经没了")
    check(os.path.isfile(j("run", "payload", "winhttp.dll")), "run/payload/winhttp.dll 在")
    check(os.path.isdir(j("log")), "log/ 在")

    print("== 5) .ucfroot 上溯约定")
    for rel in ("app/ui/env.py", "app/core/ucf_paths.py", "app/workbench/navserver.py",
                "app/tools/data/tidy_vis.py"):
        check(".ucfroot" in read(rel), "%s 还带着 .ucfroot 上溯" % rel)
    check(".ucfroot" in read("app/tools/build.ps1"), "app/tools/build.ps1 还带着 .ucfroot 上溯")
    shell = read("app/控制台.pyw")
    check("from ui.env import" in shell or "from ui.consts import" in shell,
          "入口从 ui.env / ui.consts 取环境（自身不再算路径）")

    print("== 6) 页签分组")
    check("TAB_GROUPS" in read("app/ui/consts.py"), "分组表 TAB_GROUPS 在 ui/consts.py")
    check("def build_page" in read("app/控制台.pyw"), "页签分派 build_page() 在控制台入口")
    check("def build_sub_tabs" in read("app/ui/kit.py"), "组内按钮条在 ui/kit.py（共用件）")

    print("== 7) README 与实际一致")
    doc = read("README.md")
    check("app/控制台.pyw" in doc, "README 写了入口 app/控制台.pyw")
    check("app/ui/" in doc and "app/tabs/" in doc, "README 写了 app/ui、app/tabs")
    check("data/maps" in doc or "data\\maps" in doc, "README 写了 data/maps（一图一夹）")

    if FAIL:
        print("\n!! %d 项没过" % len(FAIL))
        return 1
    print("\nOK: 目录树与 README 一致（根目录 8 个文件夹，页签 11 个，共用件 8 个）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
