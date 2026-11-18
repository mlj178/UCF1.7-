#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""工程端 / 部署端 / 四版数据 的路径解析 —— 全工具唯一的路径真相。

四版（2026-11-18 起；之前是"三版 + 部署端里的 packs"）：

  ---------------------------------------------------------------------------
  ① 备份版（原生，只读，永不编辑）
       工程端 navdata\native\
           maps\  nav\  vis\   README.md  SHA256SUMS.txt  .frozen.json
  ② 开发版（日常编辑改这里）
       工程端 navdata\dev\
           maps\  nav\  vis\
  ③ 部署版（游戏里的插件直接读这里；只有 publish 写 maps/nav）
       游戏目录 ucf_mod\
           maps\  nav\  ucf_mod.dll …      （vis\ 迁走后只剩 README）
  ④ 测试版（插件导出 / 测试包 / 归档，脏了也不影响 ③）
       工程端 navdata\test\
           vis\raw\  vis\navmesh\  vis\_state\   packs\<包名>\   archive\
  ---------------------------------------------------------------------------
  路径解析：
      导出根 EXPORT   = UCF_EXPORT_DIR  > ④ vis\      （插件 Ctrl+E / navmesh 写这里）
      测试包 PACKS_DIR = UCF_PACK_DIR    > ④ packs\
      部署根 DEPLOY   = UCF_DEPLOY       > tools/deploy.json

哪一版生效由环境变量 UCF_PROFILE 决定（默认 dev）：
    UCF_PROFILE=dev      -> 编辑器/工具读写 navdata\dev     （日常）
    UCF_PROFILE=native   -> 只读打开 navdata\native         （对照/救急，写会被拒绝）
    UCF_PROFILE=deploy   -> 直接读写游戏目录（等同 2026-11-17 之前的旧行为）

工程端（进 git）= 本文件所在 tools/ 的父目录
    src/      C 源码
    tools/    本目录
    docs/     文档（FEATURES / CHANGELOG / 各轮记录）
    geo/      *.npz 地形源 + web/*.bin（可重建）
    navdata/  四版数据（native / dev / test）

部署端（不进 git）= 游戏目录里的 ucf_mod\
    解析顺序：1) 环境变量 UCF_DEPLOY  2) tools/deploy.json  3) 回退工程端
    部署端只放游戏要读的东西（DLL / ucf_mod.json / nav\<指纹>.txt / markers / packs 由 ④ 提供）。
"""
import json
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(TOOLS)
DOCS = os.path.join(PROJ, "docs")
GEO = os.path.join(PROJ, "geo")
DEPLOY_JSON = os.path.join(TOOLS, "deploy.json")

# ---------------------------------------------------------------- 四版目录
# ① 备份版 navdata\native   冻结、只读
# ② 开发版 navdata\dev      编辑器唯一写入口，只收整理过的原生数据
# ③ 部署版 <游戏目录>        只有「部署到游戏」(publish) 能写 maps\ nav\
# ④ 测试版 navdata\test      插件 Ctrl+E 导出 + 测试包 + 归档，随便脏
NATIVE = os.path.join(PROJ, "navdata", "native")   # ① 原生备份（只读）
DEV = os.path.join(PROJ, "navdata", "dev")         # ② 开发版（可编辑）
TEST = os.path.join(PROJ, "navdata", "test")       # ④ 测试版（工程端）

_PROFILE_ALIAS = {
    "dev": "dev", "develop": "dev", "开发": "dev",
    "native": "native", "backup": "native", "frozen": "native", "原生": "native",
    "deploy": "deploy", "game": "deploy", "部署": "deploy",
}
PROFILE = _PROFILE_ALIAS.get((os.environ.get("UCF_PROFILE") or "dev").strip().lower(), "dev")


def _resolve_deploy():
    p = os.environ.get("UCF_DEPLOY", "").strip()
    if p:
        return os.path.abspath(p)
    try:
        with open(DEPLOY_JSON, "r", encoding="utf-8") as f:
            p = (json.load(f) or {}).get("deploy", "")
        if p:
            return os.path.abspath(p)
    except (OSError, ValueError):
        pass
    return PROJ


DEPLOY = _resolve_deploy()


def _resolve_env_dir(env_name, default):
    """环境变量（控制台启动游戏时注入）优先，否则用 ④ 测试版下的默认位置。"""
    p = os.environ.get(env_name, "").strip()
    if p:
        return os.path.abspath(p)
    return default


# ④ 测试版：导出收件箱 / 测试包 / 已处理导出的归档
EXPORT = _resolve_env_dir("UCF_EXPORT_DIR", os.path.join(TEST, "vis"))
PACKS_DIR = _resolve_env_dir("UCF_PACK_DIR", os.path.join(TEST, "packs"))
ARCHIVE = os.path.join(TEST, "archive")

# 当前生效的数据根（maps/nav 读写这里）
DATA = {"native": NATIVE, "dev": DEV, "deploy": DEPLOY}[PROFILE]
MAPS = os.path.join(DATA, "maps")
NAV = os.path.join(DATA, "nav")

# 导出根：插件把新扫描 / navmesh 写这里（④ 测试版）。
# 兼容旧名 VIS；2026-11-18 之前它指向 ③ 部署版。工具只读这里，不再碰 ③\vis。
VIS = EXPORT
GAME_VIS = os.path.join(DEPLOY, "vis")   # ③ 里的旧位置（迁移后只留 README）
LEGACY_VIS = GAME_VIS
# 当前版本自带的可走面（原生备份里也有 navmesh）
DATAVIS = os.path.join(DATA, "vis")
# ③ 里的回滚区：DLL 备份 + 历史导出快照。游戏不读，不算部署数据。
BACKUP = os.path.join(DEPLOY, "backup")
NAMES_FILE = os.path.join(NAV, "names.json")

# 备份版 = 只读：所有写操作都要先看这个
READONLY = (PROFILE == "native")

PROFILE_CN = {"native": "备份版（原生·只读）", "dev": "开发版", "deploy": "部署版"}


def profile_info():
    """给 /api/maps 和启动横幅用的一行版本信息。"""
    return {
        "profile": PROFILE,
        "cn": PROFILE_CN.get(PROFILE, PROFILE),
        "readonly": READONLY,
        "data": DATA,
        "maps": MAPS,
        "nav": NAV,
        "native": NATIVE,
        "dev": DEV,
        "deploy": DEPLOY,
        "test": TEST,
        "export": EXPORT,
        "packs": PACKS_DIR,
        "gameVis": GAME_VIS,
    }


def doc(name):
    """docs/ 里的文档；找不到回退工程根（兼容旧布局）。"""
    p = os.path.join(DOCS, name)
    return p if os.path.exists(p) else os.path.join(PROJ, name)


def describe():
    """多行自检（--paths / 启动横幅用）。"""
    return ("PROJ=%s\nNATIVE=%s\nDEV=%s\nDEPLOY=%s\nTEST=%s\nEXPORT=%s\nPACKS=%s\n"
            "PROFILE=%s (%s)\nDATA=%s%s" % (
                PROJ, NATIVE, DEV, DEPLOY, TEST, EXPORT, PACKS_DIR,
                PROFILE, PROFILE_CN.get(PROFILE, PROFILE), DATA,
                "  [只读]" if READONLY else ""))
