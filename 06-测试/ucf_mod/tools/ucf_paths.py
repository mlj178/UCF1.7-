#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""工程端 / 部署端 路径解析 —— 全工具唯一的路径真相。

工程端（进 git）= 本文件所在 tools/ 的父目录
    src/      C 源码
    tools/    本目录
    docs/     文档（FEATURES / CHANGELOG / 各轮记录）
    geo/      *.npz 地形源 + web/*.bin（可重建）

部署端（不进 git）= 游戏目录里的 ucf_mod\\
    ucf_mod.dll / ucf_mod.json / ucf_mod.log
    nav/ markers/ maps/ vis/ backup/

部署端位置解析顺序：
    1) 环境变量 UCF_DEPLOY
    2) tools/deploy.json  {"deploy": "D:\\\\...\\\\ucf_mod"}
    3) 回退：工程端本身（旧行为：工程与部署合在一处）
"""
import json
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(TOOLS)
DOCS = os.path.join(PROJ, "docs")
GEO = os.path.join(PROJ, "geo")
DEPLOY_JSON = os.path.join(TOOLS, "deploy.json")


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
VIS = os.path.join(DEPLOY, "vis")
NAV = os.path.join(DEPLOY, "nav")
MAPS = os.path.join(DEPLOY, "maps")
BACKUP = os.path.join(DEPLOY, "backup")
NAMES_FILE = os.path.join(NAV, "names.json")


def doc(name):
    """docs/ 里的文档；找不到回退工程根（兼容旧布局）。"""
    p = os.path.join(DOCS, name)
    return p if os.path.exists(p) else os.path.join(PROJ, name)


def describe():
    """一行自检：给 --paths 之类的调试开关用。"""
    return "PROJ=%s\nDEPLOY=%s%s" % (
        PROJ, DEPLOY, "" if DEPLOY != PROJ else "  (回退：工程端=部署端)")
