#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""工程端路径与环境 —— 控制台各模块的公共底座。

2026-11-24 目录重构时从 app/控制台.pyw 顶部抽出：第三方 import、sys.path 引导、
三区路径常量都集中在这里。页签模块一律 `from ui.env import ...`，不各自算路径。

工程端目录（进 git）：
    app/控制台.pyw   窗口壳（入口）
    app/ui/          共用件：env / consts / util / maps / stats / packs / kit
    app/tabs/        一个页签一个文件（部署 / 录制 / 开发者选项 各带自己的子模块）
    app/core/        ucf_paths（路径真相）/ map_table / navdata（数据台账）
    app/workbench/   navserver.py + web/（只读网页工作台）
    app/tools/       命令行工具（build.ps1 / autotest.ps1 / geo / data / _oneoff）
    app/tests/       静态自检
    data/            geo（地形源）+ navdata（三区数据）
    run/             payload（部署弹药库）+ build（编译产物）
    log/             运行日志（见下面「路径常量」：插件 + 控制台 + 工具全写这一处）
"""
import os
import re
import sys

_UI_DIR = os.path.dirname(os.path.abspath(__file__))   # app\ui
APP = os.path.dirname(_UI_DIR)                          # app\
HERE = APP          # 兼容原 控制台.pyw 的语义：控制台“所在目录”= app\（子进程 cwd / 相对路径基准）
UCF_ROOT = APP
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "app", "core"), UCF_ROOT, APP,
           os.path.join(APP, "tabs", "deploy"),
           os.path.join(APP, "tabs", "record"),
           os.path.join(APP, "tabs", "dev")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import ucf_paths as P  # noqa: E402   图文件夹 <图>\map.json、可走面、路线都从这取
from ucf_paths import DEPLOY, DEV, NATIVE, TEST, PACKS_DIR, doc  # noqa: E402  三区里的根（TEST 是 DEV 的旧名）
from map_table import folder_name as map_folder_name, row_of as map_row  # noqa: E402  序号_场景名中文名
from map_table import rows as map_table_rows  # noqa: E402  对照表全 11 行（含下拉里没有的纯面图）
import navdata as ND          # noqa: E402  成品版本台账 / 包对比（只读调用；改数据仍走子进程命令行）
import ucf_rec                # noqa: E402  录制轨迹：解析 / 重采样 / 跳跃·落下·岔路识别
import ucf_trace              # noqa: E402  原始轨迹采集：目录 / 增量读取 / 摘要

# ---- 路径常量（原来在 控制台.pyw 顶部，现在全项目只这一份）----
# 2026-11-25：配置 / 命令也搬到工程端 run\runtime\，游戏目录不再生成 ucf_mod\。
RUNTIME = P.RUNTIME
CFG_PATH = P.CFG_PATH
# 2026-11-23：日志的主位置是**工程端** log\（ucf_mod.log / autotest.txt / player_marks.txt），
# 启动游戏时用 UCF_LOG_DIR 指给插件，所以游戏目录不再生成日志。
# 没走控制台启动时插件会落到 <部署端>\log\，更老的部署还在部署端根目录 —— 读的时候三级都看。
# 2026-11-27：控制台/工具自己的两份日志也收进来了（以前散在 data\navdata\_logs\ 和
# dev\final\），所以 log\ 现在是一处看全：ucf_mod.log / autotest.txt / player_marks.txt /
# navdata.log / publish.log。
LOG_DIR = P.LOG_DIR                            # 主：工程端 log\
GAME_LOG_DIR = os.path.join(DEPLOY, "log")     # 备：没走控制台的落点
LOG_PATH = os.path.join(LOG_DIR, "ucf_mod.log")
AUTOTEST_TXT = os.path.join(LOG_DIR, "autotest.txt")   # 车测：每张图 OK + 最后 RESULT 写这里
MAP_MD = doc("07-地图对照表.md")
GAME_EXE = os.path.join(os.path.dirname(DEPLOY), "UnityCrossFire.exe")
NAVSERVER = os.path.join(APP, "workbench", "navserver.py")
NAVDATA = os.path.join(P.CORE, "navdata.py")   # 数据版本命令（部署/还原/校验/状态），库在 core/
TIDY = P.tool("tidy_vis.py")                   # 整理 ② vis：raw/<地图>/ + navmesh/ + _state/
PACKS = PACKS_DIR                              # 草稿根 = data\maps（<图>\<指纹>.txt + manifest.json）
TEST_VIS = P.INBOX                             # 导出收件箱 data\maps\_inbox（和递给游戏的那个路径一致）
#: 开发直读：控制台启动游戏时把 UCF_MOD_DLL 指到这里，游戏直接加载最新编译的插件
BUILD_DLL = os.path.join(UCF_ROOT, "run", "build", "ucf_mod.dll")
#: 干净检出 / 没编译过时的兜底：部署弹药库里那份插件（仍是工程端文件，游戏目录不读）
PAYLOAD_DLL = os.path.join(UCF_ROOT, "run", "payload", "ucf_mod", "ucf_mod.dll")
#: 编辑标记根目录 = data\maps（标记在 <图>\markers.txt）；启动时用 UCF_MARKERS_DIR 注入插件
MARKERS = P.MARKERS
REC_RAW = os.path.join(TEST_VIS, "rec")        # 录制原始轨迹：_inbox\rec\*.jsonl
FINAL_ROOT = P.MAPS                            # 成品：每张图一份 <图>\final\<指纹>.txt（没有版本）
FINAL_NAV = os.path.join(P.ARCHIVE, "nav")     # 旧成品目录（历史遗留，不再写入）
NAVCMD = P.NAVCMD                             # 运行中命令：插件每 ~0.5 s 查一次 seq
PMARK_TXT = os.path.join(LOG_DIR, "player_marks.txt")  # 玩家坐标记录：插件追加，控制台删除
