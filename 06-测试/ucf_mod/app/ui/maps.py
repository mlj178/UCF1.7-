#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""地图对照表与图文件夹：序号_场景名中文名、map.json / navmesh.bin 的定位。

2026-11-24 目录重构：从 app/控制台.pyw 拆出，方法体原样搬，只换文件位置。
"""


import json
import os
import re

from ui.env import DEPLOY, DEV, MAP_MD, P, map_folder_name, map_row, map_table_rows


def load_maps():
    r"""[(level, 中文名, 指纹)] —— 指纹来自每张图的 map.json（游戏自己扫出来的，不能手猜）。

    一个图文件夹一份：<序号>_<场景><中文名>\map.json。部署端没有数据时退回开发版。
    飓风危城（level9）原生 0 点、没有指纹，运行时就是 n0-0000000000000000。
    """
    out, seen = [], set()
    for root in (DEPLOY, DEV):
        for _rel, path in P.map_files(root):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, ValueError):
                continue
            m = doc.get("map") or {}
            lv = str(m.get("level") or "")
            if not lv or lv in seen:
                continue
            fp = str(m.get("fingerprint") or "")
            if not fp and lv == "level9":
                fp = "n0-0000000000000000"
            if not fp:
                continue                      # 没指纹 = 这张图没有路点图，测不了
            seen.add(lv)
            cn, _sc = map_row(lv)             # 中文名以《地图对照表》为准（暴风 JSON 里是旧名）
            out.append((lv, cn or str(m.get("label") or m.get("scene") or lv), fp))
    out.sort(key=lambda r: int("".join(ch for ch in r[0] if ch.isdigit()) or 0))
    return out


def _navmesh_name(level):
    r"""可走面在文档 / 日志里的叫法：nm716（716 个网格顶点）；不知道就写 navmesh.bin。"""
    verts = getattr(P, "NATIVE_VERTS", {}).get(str(level or ""))
    return ("nm%d" % verts) if verts else P.NAVMESH


def maps_not_listed(shown_levels):
    r"""[(序号, level, 中文名, 有没有可走面)] —— 对照表里有、但地图下拉里没有的图。

    为什么会有：load_maps 只收「有路点图（map.json + 指纹）」的图，而胜利广场 /
    死亡擂台在场景里原生没有 PointGraph（0 个路点、只有可走面 nm716 / nm60），
    永远导不出 map.json，于是永远不进下拉 —— 不是漏采，是这两张图没路点可编。
    界面上不解释，看起来就像少了两张图（2026-11-21 用户进过胜利广场后问的）。
    """
    shown = set(shown_levels or ())
    out = []
    try:
        rows = map_table_rows()
    except Exception:                     # noqa: BLE001  表读不了就什么都不提示
        return out
    for no, lv, cn, _sc in rows:
        if lv in shown:
            continue
        out.append((no, lv, cn, os.path.isfile(
            os.path.join(P.map_dir(DEV, lv), P.NAVMESH))))
    return out


def find_map_doc(fp):
    r"""(doc, path) —— 按指纹找这张图的 map.json；部署端优先，退回开发版。

    人机路点页用它算节点 / 边 / 出生点数量；不写任何文件。
    """
    if not fp:
        return None, ""
    for root in (DEPLOY, DEV):
        for _rel, path in P.map_files(root):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (OSError, ValueError):
                continue
            if str((doc.get("map") or {}).get("fingerprint") or "") == fp:
                return doc, path
    return None, ""


def load_scene_counts():
    r"""{level: {jump, crouch, guard, area, tag}} —— 读《地图对照表》第二张表。

    地图 JSON 是运行期导出（只有 PointGraph + spawn/tag），
    守点/聚集区/蹲点只在场景组件统计里，所以页签显示以这张表为准。
    """
    out = {}
    try:
        with open(MAP_MD, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return out

    def num(text):
        try:
            return int("".join(ch for ch in str(text) if ch.isdigit()) or 0)
        except ValueError:
            return 0

    for line in lines:
        s = line.strip()
        if not s.startswith("| level"):
            continue
        parts = [x.strip() for x in s.strip("|").split("|")]
        if len(parts) < 11:
            continue
        out[parts[0]] = {
            "name": parts[1], "scene": parts[2],
            "jump": num(parts[3]), "nodelink": num(parts[4]),
            "nodelink2": num(parts[5]), "crouch": num(parts[6]),
            "guard": num(parts[7]), "area": num(parts[8]), "tag": num(parts[9]),
        }
    return out


def map_scene(lv, fp=""):
    r"""地图英文场景名（默认包名前缀用）：maps\*.json 的 scene，缺了查《地图对照表》。"""
    doc, _p = find_map_doc(fp)
    scene = str(((doc or {}).get("map") or {}).get("scene") or "")
    if not scene:
        scene = str((load_scene_counts().get(lv) or {}).get("scene") or "")
    scene = re.sub(r"[^A-Za-z0-9_-]+", "_", scene).strip("_-")
    return scene or str(lv or "blank")


def folder_alias(name):
    r"""去掉文件夹名的序号前缀：01_TransportShip运输船 → TransportShip运输船。

    只用于认「同一个地图的老文件夹」（没序号/纯英文），名字本身不改。
    """
    return re.sub(r"^\d{2,3}_", "", str(name or ""))


def map_folder(lv, fp=""):
    r"""测试包文件夹名：序号_英文场景名中文名，如 01_TransportShip运输船。

    序号来自《地图对照表》第一张表（map_table 统一读），排序和 maps\NN_中文名.json 一致；
    Windows 支持中英混排，插件的 ANSI 路径在本机（代码页 936）能读中文，
    所以目录用「序号+英文+中文」，包名仍用英文（navcmd / 日志更稳）。
    """
    doc, _p = find_map_doc(fp)
    m = (doc or {}).get("map") or {}
    scene = str(m.get("scene") or "")
    label = str(m.get("label") or "")
    if not scene or not label:
        row = load_scene_counts().get(lv) or {}
        scene = scene or str(row.get("scene") or "")
        label = label or str(row.get("name") or "")
    return map_folder_name(lv, scene, label)


_MAP_ROW = re.compile(r"^\|\s*\d{1,3}\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|")


_LEVELS_FALLBACK = [
    ("level1", "运输船"), ("level2", "小型工厂"), ("level3", "椰岛之巅"),
    ("level4", "胜利广场"), ("level5", "竞技场"), ("level6", "刀锋寨"),
    ("level7", "沙漠要塞"), ("level8", "生化酒店"), ("level9", "暴风"),
    ("level10", "新寂静村"), ("level11", "死亡擂台"),
]


def load_level_table():
    r"""[(level, 中文名)] —— 只读 docs\地图对照表.md 第一张表（唯一权威表）。
    车测传的是 buildIndex，也就是 levelN 的 N，**不是** maps\NN_中文名.json 的序号：
    序号 07 是死亡擂台、它的关卡是 level11，两者不能混。"""
    out = []
    started = False
    try:
        with open(MAP_MD, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s:
                    if started:
                        break            # 空行 = 第一张表结束（后面还有别的表，不能一起读）
                    continue
                m = _MAP_ROW.match(s)
                if m:
                    started = True
                    out.append((m.group(1), m.group(2).strip()))
                elif started and not s.startswith("|"):
                    break
    except OSError:
        pass
    if len(out) < 5:
        out = list(_LEVELS_FALLBACK)
    out.sort(key=lambda r: int("".join(ch for ch in r[0] if ch.isdigit()) or 0))
    return out
