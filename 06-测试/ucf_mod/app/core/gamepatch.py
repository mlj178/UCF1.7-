#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""run\gamepatch 的唯一解析 / 分类器 —— 部署器与资产台账共用。

目录约定（见 run\gamepatch\README.md）：
    run\gamepatch\<序号>_<场景名><中文名>\
        patch.json              唯一权威：目标文件、原版哈希、补丁后哈希
        UnityCrossFire_Data\   按"游戏内相对路径"摆的补丁后文件
        orig\                   可选：原版副本，卸载时没有现场备份就靠它还原

patch.json 的 files[]：
    path        游戏内相对路径，如 UnityCrossFire_Data/level9
    bytes       补丁后大小
    sha256      补丁后 SHA256
    orig        {bytes, sha256} 原版；null = 新增文件（原版没有这个文件）
    orig_file   可选，包内原版副本的相对路径（相对 patch.json 所在目录）

状态：
    缺失    目标不存在（orig 为 null 时表示可以新增；否则缺原版，不能打）
    原版    目标哈希 == orig.sha256，可以备份后覆盖
    已打补丁 目标哈希 == sha256，幂等跳过
    被改过  两者都不是，拒绝盲打
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent          # app\core
PROJ = HERE
while not (PROJ / ".ucfroot").is_file() and PROJ.parent != PROJ:
    PROJ = PROJ.parent                           # 项目根：靠 .ucfroot 标记

PATCH_ROOT = PROJ / "run" / "gamepatch"
GAME_DATA = "UnityCrossFire_Data"

MISSING = "缺失"
ORIG = "原版"
PATCHED = "已打补丁"
OTHER = "被改过"

STATE_ORDER = {PATCHED: 0, ORIG: 1, MISSING: 2, OTHER: 3}


# ------------------------------------------------------------------ 小工具
def sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_json(path, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%d B" % n) if unit == "B" else ("%.1f %s" % (n, unit))
        n /= 1024.0
    return str(n)


# ------------------------------------------------------------------ 补丁包
def load_packs(root=None):
    r"""读 run\gamepatch\*\patch.json -> [{..., "_dir": 包目录, "files": [...]}]。

    只认 patch.json，不猜目录名：目录名是给人看的，patch.json 才是账。
    """
    root = Path(root) if root else PATCH_ROOT
    packs = []
    if not root.is_dir():
        return packs
    for d in sorted(root.iterdir()):
        if not d.is_dir():
            continue
        doc = load_json(d / "patch.json")
        if not doc:
            continue
        doc["_dir"] = str(d)
        doc.setdefault("files", [])
        packs.append(doc)
    return packs


def rel_of(entry):
    r"""patch.json 的 path 用游戏内相对路径（UnityCrossFire_Data/level9）。"""
    return str(entry["path"]).replace("/", os.sep)


def source_of(pack, entry):
    """补丁后文件在包里的位置。"""
    return Path(pack["_dir"]) / rel_of(entry)


def orig_source_of(pack, entry):
    """原版副本在包里的位置（没有就返回 None）。"""
    rel = str(entry.get("orig_file") or "").strip()
    if not rel:
        return None
    return Path(pack["_dir"]) / rel.replace("/", os.sep)


def orig_of(entry):
    return entry.get("orig") or {}


def is_new(entry):
    """orig 为 null = 原版没有这个文件，部署时是新增。"""
    return not bool(orig_of(entry).get("sha256"))


def check_source(pack, entry):
    """确认包里的补丁文件存在且哈希对得上；不对就抛异常，绝不盲打。"""
    src = source_of(pack, entry)
    if not src.is_file():
        raise FileNotFoundError("补丁包缺文件：%s" % src)
    want = str(entry.get("sha256") or "").lower()
    if want:
        got = sha256_file(src)
        if got != want:
            raise ValueError("补丁包文件哈希不对：%s\n  期望 %s\n  实际 %s" % (src, want, got))
    return src


def state_of(game_dir, entry):
    r"""单个文件在某个游戏目录里的状态：缺失 / 原版 / 已打补丁 / 被改过。"""
    p = Path(game_dir) / rel_of(entry)
    if not p.is_file():
        return MISSING
    got = sha256_file(p)
    if got == str(entry.get("sha256") or "").lower():
        return PATCHED
    orig = orig_of(entry)
    if orig.get("sha256") and got == str(orig["sha256"]).lower():
        return ORIG
    return OTHER


def iter_entries(packs=None):
    """(pack, entry) 平铺，部署器和台账共用。"""
    for pack in (packs if packs is not None else load_packs()):
        for entry in pack.get("files") or []:
            yield pack, entry
