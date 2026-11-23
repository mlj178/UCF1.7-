#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""地图对照表读取：序号 / 关卡 / 中文名 / 场景名 —— 测试包文件夹编号的唯一来源。

权威表是 docs/guide/地图对照表.md 的**第一张表**（5 列）；读不到才退回内置 11 条。
本模块只干两件事：
    rows()                      -> [(序号, 关卡, 中文名, 场景名)]，按序号排好
    folder_name(关卡, 场景名, 中文名) -> "01_TransportShip运输船"（测试包的地图文件夹名）

为什么要有它：packs\\ 下按图分文件夹，名字里带对照表的序号，序号变了文件夹跟着变；
控制台和命令行（navdata.py）都从这里取名，免得两边各写一份表、迟早对不上。
"""
import io
import re

try:
    from ucf_paths import doc as _doc
except Exception:                                   # 单独 import 时（测试脚本）也不炸
    _doc = None

ROW_RE = re.compile(r"^\|\s*(\d{1,3})\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|")

# 兜底表：地图对照表.md 缺失/损坏时才用（顺序 = 序号）
_BUILTIN = [
    ("level1", "运输船", "TransportShip"),
    ("level2", "小型工厂", "Factory"),
    ("level3", "椰岛之巅", "Cebu_City"),
    ("level4", "胜利广场", "NY_TM"),
    ("level5", "竞技场", "Arena"),
    ("level6", "刀锋寨", "GrimReaperKM"),
    ("level11", "死亡擂台", "DeathRing"),
    ("level7", "沙漠要塞", "DesertFort"),
    ("level8", "生化酒店", "NanoResort"),
    ("level9", "飓风危城", "Nano30_Storm"),
    ("level10", "新寂静村", "Nano_DawnVillage"),
]

_cache = None


def table_path():
    if _doc is not None:
        try:
            return _doc("地图对照表.md")
        except Exception:
            pass
    return ""


def rows():
    r"""[(序号, 关卡, 中文名, 场景名)]；永远返回 11 条（读不到表就用兜底表）。"""
    global _cache
    if _cache is not None:
        return _cache
    out = []
    path = table_path()
    if path:
        try:
            with io.open(path, "r", encoding="utf-8") as f:
                started = False
                for line in f:
                    s = line.strip()
                    if not s:
                        if started:
                            break                       # 空行 = 第一张表结束
                        continue
                    m = ROW_RE.match(s)
                    if not m:
                        if started and not s.startswith("|"):
                            break
                        continue
                    started = True
                    out.append((int(m.group(1)), m.group(2), m.group(3).strip(), m.group(4).strip()))
        except OSError:
            out = []
    if len(out) < 5:                                    # 表丢了/格式变了：用兜底表
        out = [(i + 1, lv, cn, sc) for i, (lv, cn, sc) in enumerate(_BUILTIN)]
    out.sort()
    _cache = out
    return out


def no_of(level):
    """关卡 -> 序号（int）；不在表里返回 0。"""
    lv = str(level or "").strip().lower()
    for no, l, _cn, _sc in rows():
        if l.lower() == lv:
            return no
    return 0


def row_of(level):
    """关卡 -> (中文名, 场景名)；不在表里返回 ("", "")。"""
    lv = str(level or "").strip().lower()
    for _no, l, cn, sc in rows():
        if l.lower() == lv:
            return cn, sc
    return "", ""


def safe_name(text):
    r"""去掉 Windows 非法字符（插件用 ANSI 路径，空格也别留）。"""
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", str(text or "")).strip(" .")


def folder_name(level, scene="", label=""):
    r"""测试包的地图文件夹名：序号 + 场景名 + 中文名，如 01_TransportShip运输船。

    表里有这张图就**以表为准**：暴风那关的地图 JSON 里 label 还是旧名「暴风」，
    按 JSON 建目录会跑出 10_Nano30_Storm暴风，和表里的「飓风危城」不一致。
    关卡不在表里的才用传进来的场景名/中文名，也不加序号。
    """
    lv = str(level or "").strip()
    cn, sc = row_of(lv)
    scene = sc or scene
    label = cn or label
    base = safe_name("%s%s" % (scene or lv or "blank", label)) or lv or "blank"
    no = no_of(lv)
    return ("%02d_%s" % (no, base)) if no else base
