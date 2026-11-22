#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""工程端 / 部署端 / 三区数据 的路径解析 —— 全工具唯一的路径真相。

三区（2026-11-21 起；此前是"四版"，④ 测试版已并入 ② 开发版）：

  三档启动（控制台底部按钮决定，都从 ② 读，游戏目录不再存数据）：
      成品    UCF_PACK_DIR=②\final + UCF_PACK=<版本>  一版一整套数据（v1/v2…），启动时选；
                                                        和编辑中同一套加载逻辑（grow/keep 也生效）
      编辑中  UCF_PACK=②\packs\<图>\<包>              可写，调图 / 试路线
      原版    插件总开关关                             插件待机，什么都不读

  ---------------------------------------------------------------------------
  2026-11-21 起：① 备份 / ② 开发 都按**地图分文件夹**（和 ② packs 同一套命名）：

    <数据根>\
        00_公共\                      names.json / _index.json / INDEX.md / 清单（不属于某张图）
        01_TransportShip运输船\        map.json  navmesh.bin  <指纹>.txt（② 还有 导出\）
        02_Factory小型工厂\            …
        04_NY_TM胜利广场\              原生没有点图，只有 navmesh.bin
        07_DeathRing死亡擂台\          同上

  文件夹名唯一来源：docs/guide/地图对照表.md（map_table.folder_name）。
  旧布局（maps\*.json + nav\ + vis\）仍然能读——下面的地图函数都兼容两种，迁移期间不会翻车。

   ---------------------------------------------------------------------------
  ① 备份版（原生，只读，永不编辑）
       工程端 navdata\native\   <图>\{map.json, navmesh.bin} + 00_公共\
  ② 开发版（唯一数据源：成品 + 收件箱 + 测试包）
       工程端 navdata\dev\      <图>\{map.json, navmesh.bin, 导出\} + 00_公共\
           packs\<图>\<包名>\       编辑中（可写沙盒）；做完用 pack promote 升进成品
           final\<版本>\<指纹>.txt  成品（一版一整套）
           vis\                     导出收件箱（插件临时落点，整理后进 <图>\导出\）
           archive\                 处理过的导出 / 只读还原点
  ③ 游戏目录（运行时，不放数据）
       游戏目录 ucf_mod\
           ucf_mod.dll  ucf_mod.json  markers\    （nav\ maps\ 2026-11-21 清空）
  ---------------------------------------------------------------------------
  路径解析：
      导出根 EXPORT   = UCF_EXPORT_DIR  > ② vis\      （插件 Ctrl+E / navmesh 写这里）
      测试包 PACKS_DIR = UCF_PACK_DIR    > ② packs\
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
    navdata/  三区数据（native / dev）

部署端（不进 git）= 游戏目录里的 ucf_mod\
    解析顺序：1) 环境变量 UCF_DEPLOY  2) tools/deploy.json  3) 回退工程端
    部署端只放运行时要读的东西（DLL / ucf_mod.json / markers）；数据全在 ②，
    由 UCF_PACK（成品 = ②\nav、编辑中 = ②\packs\…）指过去，游戏目录不再放数据。
"""
import json
import os
import re
import time

TOOLS = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(TOOLS)
DOCS = os.path.join(PROJ, "docs")
GEO = os.path.join(PROJ, "geo")
DEPLOY_JSON = os.path.join(TOOLS, "deploy.json")

# ---------------------------------------------------------------- 三区目录
# ① 备份版 navdata\native   冻结、只读
# ② 开发版 navdata\dev      唯一数据源：maps\nav 成品，vis 收件箱，packs 编辑中
# ③ 游戏目录 <ucf_mod>      运行时：dll / 配置 / markers（2026-11-21 起不放数据）
NATIVE = os.path.join(PROJ, "navdata", "native")   # ① 原生备份（只读）
DEV = os.path.join(PROJ, "navdata", "dev")         # ② 开发版（正式数据 + 收件箱 + 测试包）
# 2026-11-21 四区改三区：原 navdata\test 已改名为 dev（内容原样保留），
# TEST 只剩别名作用——老的调用点（EXPORT / PACKS_DIR / ARCHIVE）不用改指向。
TEST = DEV

_PROFILE_ALIAS = {
    "dev": "dev", "develop": "dev", "开发": "dev",
    "native": "native", "backup": "native", "frozen": "native", "原生": "native",
    "deploy": "deploy", "game": "deploy", "部署": "deploy",
}
PROFILE = _PROFILE_ALIAS.get((os.environ.get("UCF_PROFILE") or "dev").strip().lower(), "dev")


# 用户级配置：用户在「首次设置」里选的游戏位置写这里，和开发机的 tools/deploy.json 分开。
#   优先级：UCF_DEPLOY 环境变量 > 用户配置 > tools/deploy.json（开发机） > 工程根
USER_CFG = os.path.join(
    os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local"),
    "UCFMod", "deploy.json",
)
DEPLOY_SOURCE_CN = {
    "env": "环境变量 UCF_DEPLOY",
    "switch": "本次运行内切换",
    "user": "用户设置（控制台选过游戏）",
    "project": "工程内 tools/deploy.json（开发机）",
    "default": "未配置，回退到工程根",
}


def _read_deploy_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return ((json.load(f) or {}).get("deploy") or "").strip()
    except (OSError, ValueError):
        return ""


def _resolve_deploy():
    """返回 (部署根, 来源)。部署根 = <游戏目录>\\ucf_mod。"""
    p = os.environ.get("UCF_DEPLOY", "").strip()
    if p:
        return os.path.abspath(p), "env"
    p = _read_deploy_json(USER_CFG)
    if p:
        return os.path.abspath(p), "user"
    p = _read_deploy_json(DEPLOY_JSON)
    if p:
        return os.path.abspath(p), "project"
    return PROJ, "default"


DEPLOY, DEPLOY_SOURCE = _resolve_deploy()


def game_dir_of(deploy_root=None):
    """部署根（<游戏>\\ucf_mod）→ 游戏目录。"""
    return os.path.dirname(os.path.abspath(deploy_root or DEPLOY))


HISTORY_MAX = 6            # 最近用过的游戏位置，留几个够挑就行


def load_user_cfg():
    """读用户配置（deploy / game_dir / history）；读不到就返回空 dict。"""
    try:
        with open(USER_CFG, "r", encoding="utf-8") as f:
            data = json.load(f) or {}
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def load_history():
    r"""最近用过的游戏目录，最近的在前。[{"game_dir": ..., "exists": bool}]"""
    out, seen = [], set()
    for item in (load_user_cfg().get("history") or []):
        g = (item.get("game_dir") if isinstance(item, dict) else item) or ""
        g = os.path.abspath(g) if g else ""
        if not g or g.lower() in seen:
            continue
        seen.add(g.lower())
        out.append({"game_dir": g, "exists": os.path.isfile(os.path.join(g, "UnityCrossFire.exe"))})
    return out[:HISTORY_MAX]


def save_deploy(game_dir):
    """把用户选的游戏目录写进用户配置（并记入历史），返回写入路径。

    控制台选完 UnityCrossFire.exe 后调这里；写的是 %LOCALAPPDATA%\\UCFMod\\deploy.json，
    不动工程里的 tools/deploy.json。下次启动 ucf_paths 会优先读它。
    """
    game_dir = os.path.abspath(str(game_dir))
    old = load_user_cfg()
    history = [game_dir]
    for item in (old.get("history") or []):
        g = (item.get("game_dir") if isinstance(item, dict) else item) or ""
        if g and os.path.abspath(g).lower() != game_dir.lower():
            history.append(os.path.abspath(g))
        if len(history) >= HISTORY_MAX:
            break
    data = {
        "deploy": os.path.join(game_dir, "ucf_mod"),
        "game_dir": game_dir,
        "history": history,
        "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return _write_user_cfg(data)


def _write_user_cfg(data):
    d = os.path.dirname(USER_CFG)
    os.makedirs(d, exist_ok=True)
    tmp = USER_CFG + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, USER_CFG)
    return USER_CFG


def forget_history(game_dir):
    """从历史里删掉一条记录（当前正在用的那条不给删）。"""
    game_dir = os.path.abspath(str(game_dir))
    cfg = load_user_cfg()
    current = os.path.abspath(str(cfg.get("game_dir") or ""))
    if game_dir.lower() == current.lower() or not current:
        return False
    cfg["history"] = [g for g in (cfg.get("history") or [])
                      if os.path.abspath(str(g)).lower() != game_dir.lower()]
    _write_user_cfg(cfg)
    return True


def rebind(game_dir):
    """进程内换游戏位置：重算本模块所有跟 DEPLOY 有关的全局量。

    注意：ucf_paths 的调用方大多在 import 时就把 DEPLOY 绑成局部名了，
    所以换位置后仍建议重启进程；这个函数是给"不想重启"的实验路径留的。
    """
    global DEPLOY, DEPLOY_SOURCE, GAME_VIS, LEGACY_VIS, BACKUP, DATA, MAPS, NAV, NAMES_FILE
    game_dir = os.path.abspath(str(game_dir))
    DEPLOY = os.path.join(game_dir, "ucf_mod")
    DEPLOY_SOURCE = "switch"
    GAME_VIS = os.path.join(DEPLOY, "vis")
    LEGACY_VIS = GAME_VIS
    BACKUP = os.path.join(DEPLOY, "backup")
    DATA = {"native": NATIVE, "dev": DEV, "deploy": DEPLOY}[PROFILE]
    MAPS = os.path.join(DATA, "maps")
    NAV = os.path.join(DATA, "nav")
    NAMES_FILE = os.path.join(NAV, "names.json")
    return DEPLOY


def _resolve_env_dir(env_name, default):
    """环境变量（控制台启动游戏时注入）优先，否则用 ② 开发版下的默认位置。"""
    p = os.environ.get(env_name, "").strip()
    if p:
        return os.path.abspath(p)
    return default


# ② 开发版里的草稿区：导出收件箱 / 测试包 / 已处理导出的归档（都不会进 ③）
EXPORT = _resolve_env_dir("UCF_EXPORT_DIR", os.path.join(DEV, "vis"))
PACKS_DIR = _resolve_env_dir("UCF_PACK_DIR", os.path.join(DEV, "packs"))
ARCHIVE = os.path.join(DEV, "archive")
FINAL = os.path.join(DEV, "final")          # ② 成品版本集合：<FINAL>\<版本名>\<指纹>.txt（一版一整套）

# 当前生效的数据根（maps/nav 读写这里）
DATA = {"native": NATIVE, "dev": DEV, "deploy": DEPLOY}[PROFILE]
MAPS = os.path.join(DATA, "maps")
NAV = os.path.join(DATA, "nav")

# 导出根：插件把新扫描 / navmesh 写这里（② 开发版的收件箱）。
# 兼容旧名 VIS；2026-11-18 之前它指向 ③ 部署版。工具只读这里，不再碰 ③\vis。
VIS = EXPORT
GAME_VIS = os.path.join(DEPLOY, "vis")   # ③ 里的旧位置（迁移后只留 README）
LEGACY_VIS = GAME_VIS
# 当前版本自带的可走面（原生备份里也有 navmesh）
DATAVIS = os.path.join(DATA, "vis")
# ③ 里的回滚区：DLL 备份 + 历史导出快照。游戏不读，不算部署数据。
BACKUP = os.path.join(DEPLOY, "backup")
NAMES_FILE = os.path.join(NAV, "names.json")

# ---------------------------------------------------------------- 图文件夹（按地图分类）
# 2026-11-21：① 备份 / ② 开发 从「maps\ nav\ vis\ 三块平铺」改成「一张图一个文件夹」，
# 和 ② packs\ 共用一套名字（docs/guide/地图对照表.md 的 序号_场景名中文名）。
# 旧布局仍然能读：下面每个函数先找新布局，找不到再回退 maps\ / nav\ / vis\。
# 原生 A* 顶点数（网格顶点去重后）：旧布局的 navmesh 文件名 navmesh_nm<顶点数>-<指纹>.bin
# 就是按这个对号的，见 docs/guide/地图对照表.md §「原生可通行空间（A* 图）」。
# 运输船 / 生化酒店 / 飓风危城 原生没有 NavMeshGraph，不在表里。
NATIVE_VERTS = {
    "level2": 840, "level3": 532, "level4": 716, "level5": 683,
    "level6": 559, "level7": 919, "level10": 944, "level11": 60,
}

COMMON = "00_公共"          # 公共文件（names / _index / 清单）：不属于任何一张图
MAP_JSON = "map.json"       # 图文件夹里的点图（原 maps\NN_中文名.json）
NAVMESH = "navmesh.bin"     # 图文件夹里的可走面（原 vis\navmesh_nm<顶点>-<指纹>.bin）

_FOLDER = {}


def map_folder(level):
    r"""关卡 -> 图文件夹名，如 level1 -> 01_TransportShip运输船。

    名字以《地图对照表》为准（表里没有就原样用关卡名，不编序号）。
    """
    key = str(level or "").strip()
    if key in _FOLDER:
        return _FOLDER[key]
    name = key
    try:
        import map_table
        name = map_table.folder_name(key) or key
    except Exception:                 # noqa: BLE001  单独 import 时也不炸
        name = key
    _FOLDER[key] = name
    return name


def is_folders(root):
    r"""这个数据根是不是「一张图一个文件夹」的新布局。

    判据：有 00_公共\，或者已经有某个 <图>\map.json。都没有 = 旧布局。
    """
    if not root or not os.path.isdir(root):
        return False
    if os.path.isdir(os.path.join(root, COMMON)):
        return True
    try:
        for name in os.listdir(root):
            if os.path.isfile(os.path.join(root, name, MAP_JSON)):
                return True
    except OSError:
        pass
    return False


def map_dir(root, level):
    """一张图的数据文件夹（不一定存在）。"""
    return os.path.join(root, map_folder(level))


def map_json(root, level):
    r"""一张图的点图 JSON：<图>\map.json。"""
    return os.path.join(map_dir(root, level), MAP_JSON)


def common_dir(root):
    """公共文件目录：新布局 00_公共\，旧布局 nav\（names.json 原来在这）。"""
    d = os.path.join(root, COMMON)
    if os.path.isdir(d):
        return d
    return os.path.join(root, "nav")


def names_dir(root):
    """names.json 该放哪个目录：新布局 00_公共\\，旧布局 nav\\。"""
    return os.path.join(root, COMMON) if is_folders(root) else os.path.join(root, "nav")


def index_dir(root):
    """_index.json / INDEX.md 该放哪个目录：新布局 00_公共\\，旧布局 maps\\。"""
    return os.path.join(root, COMMON) if is_folders(root) else os.path.join(root, "maps")


def manifest_dir(root):
    """清单类文件（SHA256SUMS / README / .frozen.json）放哪：新布局 00_公共\\，旧布局根目录。"""
    d = os.path.join(root, COMMON)
    return d if os.path.isdir(d) else root


def names_path(root):
    """names.json（指纹/场景名 -> 关卡中文名）：新 00_公共\，旧 nav\。"""
    for p in (os.path.join(root, COMMON, "names.json"),
              os.path.join(root, "nav", "names.json")):
        if os.path.isfile(p):
            return p
    return os.path.join(root, COMMON, "names.json")


def index_path(root):
    """地图台账 _index.json：新 00_公共\，旧 maps\。"""
    for p in (os.path.join(root, COMMON, "_index.json"),
              os.path.join(root, "maps", "_index.json")):
        if os.path.isfile(p):
            return p
    return os.path.join(root, COMMON, "_index.json")


def map_files(root):
    r"""[(相对路径, 绝对路径)] —— 这一版的所有地图 JSON。

    新布局：01_TransportShip运输船/map.json；旧布局：01_运输船.json。
    """
    out = []
    if not root or not os.path.isdir(root):
        return out
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return out
    for name in names:
        if name.startswith((".", "_")):
            continue
        p = os.path.join(root, name, MAP_JSON)
        if os.path.isfile(p):
            out.append((name + "/" + MAP_JSON, p))
    if out:
        return out
    legacy = os.path.join(root, "maps")          # 迁移前的平铺
    if os.path.isdir(legacy):
        for name in sorted(os.listdir(legacy)):
            if not name.lower().endswith(".json") or name.startswith("_"):
                continue
            p = os.path.join(legacy, name)
            if os.path.isfile(p):
                out.append((name, p))
    return out


def map_docs(root):
    r"""[(level, 中文名, 路径)] —— 读得出来的地图 JSON（空档图也给一条，level 就在）。"""
    out = []
    for _rel, p in map_files(root):
        try:
            with open(p, "r", encoding="utf-8") as f:
                doc = json.load(f)
        except (OSError, ValueError):
            continue
        m = doc.get("map") or {}
        out.append((str(m.get("level") or ""), str(m.get("label") or ""), p))
    return out


def _fingerprint_of(root, level):
    """这张图的指纹（读它的 map.json）；读不到空串。"""
    try:
        with open(map_json(root, level), "r", encoding="utf-8") as f:
            m = (json.load(f) or {}).get("map") or {}
    except (OSError, ValueError):
        return ""
    return str(m.get("fingerprint") or "")


def navmesh_file(root, level):
    r"""这张图的可走面文件（.bin）；没有就 None。

    新布局：<图>\navmesh.bin（也认 navmesh_nm*.bin）；
    旧布局：<根>\vis\navmesh_<指纹>.bin 或 vis\navmesh\ 里同名文件。
    """
    d = map_dir(root, level)
    if os.path.isdir(d):
        p = os.path.join(d, NAVMESH)
        if os.path.isfile(p):
            return p
        for name in sorted(os.listdir(d)):
            if name.startswith("navmesh") and name.lower().endswith(".bin"):
                return os.path.join(d, name)
    # 旧布局：vis\navmesh_<指纹>.bin 或 vis\navmesh\ 下同名（插件落盘用 nm<顶点数> 指纹）
    bases = (os.path.join(root, "vis"), os.path.join(root, "vis", "navmesh"))
    prefixes = []
    fp = _fingerprint_of(root, level)
    if fp:
        prefixes.append("navmesh_%s" % fp)
    verts = NATIVE_VERTS.get(str(level or "").strip())
    if verts:
        prefixes.append("navmesh_nm%d-" % verts)
    for base in bases:
        if not os.path.isdir(base):
            continue
        for name in sorted(os.listdir(base)):
            if not name.lower().endswith(".bin"):
                continue
            for pre in prefixes:
                if name.startswith(pre):
                    return os.path.join(base, name)
    return None


def navmesh_files(root):
    r"""[(相对路径, 绝对路径)] —— 这一版的全部可走面（比对 / 统计用）。"""
    out = []
    if not root or not os.path.isdir(root):
        return out
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return out
    for name in names:
        if name.startswith((".", "_")):
            continue
        d = os.path.join(root, name)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.startswith("navmesh") and fn.lower().endswith(".bin"):
                out.append((name + "/" + fn, os.path.join(d, fn)))
    if out:
        return out
    for base, rel in ((os.path.join(root, "vis"), "vis"),
                      (os.path.join(root, "vis", "navmesh"), "vis/navmesh")):
        if not os.path.isdir(base):
            continue
        for fn in sorted(os.listdir(base)):
            if fn.startswith("navmesh") and fn.lower().endswith(".bin"):
                out.append((rel + "/" + fn, os.path.join(base, fn)))
    return out


def route_files(root):
    r"""[(指纹, 路径)] —— 这个数据根里的路线 txt。

    新布局：<图>\<指纹>.txt；旧布局：nav\<指纹>.txt。
    """
    out, seen = [], set()
    fp_re = re.compile(r"^n\d+-[0-9a-fA-F]{16}$")      # 路线文件就叫 <指纹>.txt
    roots = []
    if is_folders(root):
        try:
            for name in sorted(os.listdir(root)):
                d = os.path.join(root, name)
                if os.path.isdir(d) and not name.startswith(("_", ".")):
                    roots.append(d)
        except OSError:
            pass
    roots.append(os.path.join(root, "nav"))
    for d in roots:
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if not fn.lower().endswith(".txt"):
                continue
            fp = fn[:-4]
            if not fp_re.match(fp) or fp in seen:
                continue
            p = os.path.join(d, fn)
            if os.path.isfile(p):
                seen.add(fp)
                out.append((fp, p))
    return out


# 备份版 = 只读：所有写操作都要先看这个
READONLY = (PROFILE == "native")

PROFILE_CN = {"native": "备份版（原生·只读）", "dev": "开发版",
              "deploy": "游戏目录（运行时·不放数据）"}


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
    """docs/ 里的文档；按 docs/ → docs/guide/ → docs/record/ 顺序找，最后回退工程根（兼容旧布局）。"""
    for sub in ("", "guide", "record"):
        p = os.path.join(DOCS, sub, name) if sub else os.path.join(DOCS, name)
        if os.path.exists(p):
            return p
    return os.path.join(PROJ, name)


def describe():
    """多行自检（--paths / 启动横幅用）。"""
    return ("PROJ=%s\nNATIVE=%s\nDEV=%s\nDEPLOY=%s\nEXPORT=%s\nPACKS=%s\n"
            "PROFILE=%s (%s)\nDATA=%s%s" % (
                PROJ, NATIVE, DEV, DEPLOY, EXPORT, PACKS_DIR,
                PROFILE, PROFILE_CN.get(PROFILE, PROFILE), DATA,
                "  [只读]" if READONLY else ""))
