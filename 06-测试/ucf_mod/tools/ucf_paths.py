#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""工程端 / 部署端 / 三版数据 的路径解析 —— 全工具唯一的路径真相。

三版（2026-11-17 起）：

  ---------------------------------------------------------------------------
  ① 备份版（原生，只读，永不编辑）
       工程端 navdata\native\
           maps\  nav\  vis\   README.md  SHA256SUMS.txt  .frozen.json
  ② 开发版（日常编辑改这里）
       工程端 navdata\dev\
           maps\  nav\  vis\
  ③ 部署版（游戏里的插件直接读这里）
       游戏目录 ucf_mod\
           maps\  nav\  vis\   ucf_mod.dll …
  ---------------------------------------------------------------------------

哪一版生效由环境变量 UCF_PROFILE 决定（默认 dev）：
    UCF_PROFILE=dev      -> 编辑器/工具读写 navdata\dev     （日常）
    UCF_PROFILE=native   -> 只读打开 navdata\native         （对照/救急，写会被拒绝）
    UCF_PROFILE=deploy   -> 直接读写游戏目录（等同 2026-11-17 之前的旧行为）

工程端（进 git）= 本文件所在 tools/ 的父目录
    src/      C 源码
    tools/    本目录
    docs/     文档（FEATURES / CHANGELOG / 各轮记录）
    geo/      *.npz 地形源 + web/*.bin（可重建）
    navdata/  三版数据（native / dev）

部署端（不进 git）= 游戏目录里的 ucf_mod\
    解析顺序：1) 环境变量 UCF_DEPLOY  2) tools/deploy.json  3) 回退工程端
"""
import json
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(TOOLS)
DOCS = os.path.join(PROJ, "docs")
GEO = os.path.join(PROJ, "geo")
DEPLOY_JSON = os.path.join(TOOLS, "deploy.json")

# ---------------------------------------------------------------- 三版目录
NATIVE = os.path.join(PROJ, "navdata", "native")   # ① 原生备份（只读）
DEV = os.path.join(PROJ, "navdata", "dev")         # ② 开发版（可编辑）

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

# 当前生效的数据根（maps/nav 读写这里）
DATA = {"native": NATIVE, "dev": DEV, "deploy": DEPLOY}[PROFILE]
MAPS = os.path.join(DATA, "maps")
NAV = os.path.join(DATA, "nav")

# 游戏导出目录：插件把新扫描/navmesh 写这里，任何版本都只读它
VIS = os.path.join(DEPLOY, "vis")
# 当前版本自带的可走面（原生备份里也有 navmesh）
DATAVIS = os.path.join(DATA, "vis")
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
        "gameVis": VIS,
    }


def doc(name):
    """docs/ 里的文档；找不到回退工程根（兼容旧布局）。"""
    p = os.path.join(DOCS, name)
    return p if os.path.exists(p) else os.path.join(PROJ, name)


def describe():
    """多行自检（--paths / 启动横幅用）。"""
    return ("PROJ=%s\nNATIVE=%s\nDEV=%s\nDEPLOY=%s\nPROFILE=%s (%s)\nDATA=%s%s" % (
        PROJ, NATIVE, DEV, DEPLOY, PROFILE, PROFILE_CN.get(PROFILE, PROFILE), DATA,
        "  [只读]" if READONLY else ""))
