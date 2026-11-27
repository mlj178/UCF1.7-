#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""工程端 / 部署端 / 地图数据 的路径解析 —— 全工具唯一的路径真相。

一图一夹（2026-11-27 起；此前 ① 备份 / ② 开发 / 草稿 / 标记 分在 navdata\ 下四处）：

    data\maps\
        00_公共\                      names.json / _index.json / INDEX.md / SHA256SUMS.txt / .frozen.json
        01_TransportShip运输船\        同一张图的所有东西都在这一个文件夹里：
            map.json                  点图元数据（指纹 / 点数 / bbox）
            navmesh.bin               可走面（原生没有 NavMeshGraph 的图就没有这个文件）
            <指纹>.txt                 点图草稿（编辑中档读写这里）
            markers.txt               蹲守点 / 守卫区 / 守卫点 / 标签 / 出生点
            manifest.json             草稿状态（谁建的 / 什么时候 / grow|keep）
            native\                    ① 冻结副本：map.json + navmesh.bin（只读）
            final\<指纹>.txt           成品（成品档读这里，只读）
        04_NY_TM胜利广场\              原生没有点图，只有 navmesh.bin（native\ 里也是）
        07_DeathRing死亡擂台\          同上
        _inbox\                       插件写出来的可走面导出 / 录制轨迹（派生，可重建）
        _archive\                     删草稿 / 清标记 / 发布前快照 / 迁移日志（派生）

  文件夹名唯一来源：docs/guide/地图对照表.md（map_table.folder_name）。

  ---------------------------------------------------------------------------
  三档启动（控制台底部按钮决定，都从 data\maps 读，游戏目录不存数据）：
      成品    UCF_PACK_DIR=data\maps + UCF_NAV_SEARCH=1 + UCF_NAV_SUB=final
              插件按当前图指纹找 <图>\final\<指纹>.txt，markers 也跟着 <图>\markers.txt；只读
      编辑中  UCF_PACK_DIR=data\maps + UCF_PACK=<图>   一张图一个草稿，可写
      原版    插件总开关关                              插件待机，什么都不读

   ---------------------------------------------------------------------------
  部署端（运行时，只放加载器 + 本体补丁）
       游戏目录 winhttp.dll  winhttp_orig.dll
       （2026-11-25 起不再有 ucf_mod\；插件本体/配置/命令/日志/标记全在工程端）

  运行时状态（工程端，2026-11-25 起）：
      run\runtime\ucf_mod.json     配置（控制台读写，插件通过 UCF_MOD_DIR 读）
      run\runtime\ucf_navcmd.txt  控制台 ↔ 插件命令（插件每 ~0.5 s 查一次 seq）

  日志（工程端 log\，2026-11-27 起全部集中这一处；都不进 git）：
      ucf_mod.log / ucf_mod.prev.log      插件主日志（16 MB 轮转，保 1 代）
      ucf_mod.prev_HHMMSS.log             车测开跑前的备份
      autotest.txt / player_marks.txt     车测结果 / 玩家坐标记录
      navdata.log / navdata.prev.log      命令行 stdout 抄本（16 MB 轮转）
      publish.log                         成品发布流水（TSV）
  ---------------------------------------------------------------------------
  路径解析：
      导出收件箱 EXPORT     = UCF_EXPORT_DIR  > data\maps\_inbox\（插件写可走面 / 轨迹）
      草稿根 PACKS_DIR      = UCF_PACK_DIR    > data\maps\（<图>\<指纹>.txt）
      编辑标记 MARKERS      = UCF_MARKERS_DIR > data\maps\（<图>\markers.txt）
      部署根 DEPLOY         = UCF_DEPLOY      > tools/deploy.json

工程端（进 git）= 本文件所在目录向上找到 .ucfroot 的那一层
    app\core\    本模块 + map_table / navdata（路径与数据台账）
    app\ui\ app\tabs\ app\workbench\ app\tools\  控制台 / 页面 / 工具
    src\        C 源码
    data\maps\  地图数据（一图一夹）+ data\geo\（地形源）
    docs\      文档（guide / record）

部署端（不进 git）= 游戏目录本身
    解析顺序：1) 环境变量 UCF_DEPLOY  2) tools/deploy.json  3) 回退工程端
    2026-11-25 起游戏目录只放"必须有的文件"：winhttp.dll / winhttp_orig.dll + 本体补丁；
    插件本体、ucf_mod.json、ucf_navcmd.txt、日志、标记、地图数据全部在工程端，
    由 UCF_MOD_DIR / UCF_LOG_DIR / UCF_MARKERS_DIR / UCF_PACK 指过去。
"""
import json
import os
import re
import sys
import time

# 项目根靠 .ucfroot 标记向上找 —— 本文件在 core/ 里，以后整体搬地方也不用改这里。
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = HERE
while not os.path.isfile(os.path.join(PROJ, ".ucfroot")) and os.path.dirname(PROJ) != PROJ:
    PROJ = os.path.dirname(PROJ)
CORE = os.path.join(PROJ, "app", "core")
TOOLS = os.path.join(PROJ, "app", "tools")
TOOLS_GEO = os.path.join(TOOLS, "geo")
TOOLS_DATA = os.path.join(TOOLS, "data")
CONSOLE = os.path.join(PROJ, "app")
WEB = os.path.join(CONSOLE, "workbench", "web")
#: 日志主位置：控制台用 UCF_LOG_DIR 指给插件，控制台/工具自己那份也写这里
#: （ucf_mod.log / autotest.txt / player_marks.txt / navdata.log / publish.log）
LOG_DIR = os.path.join(PROJ, "log")
DOCS = os.path.join(PROJ, "docs")
DATA_ROOT = os.path.join(PROJ, "data")    # 2026-11-24：数据统一进 data（geo + navdata）
GEO = os.path.join(DATA_ROOT, "geo")
DEPLOY_JSON = os.path.join(TOOLS, "deploy.json")
if CORE not in sys.path:
    sys.path.insert(0, CORE)          # map_table 和本文件同目录（下面延迟 import 它）

# ---------------------------------------------------------------- 一图一夹（2026-11-27）
# 唯一源：data\maps\<序号_场景名中文名>\ —— 同一张图的点图 / 可走面 / 编辑标记 / 成品
# 全在这一个文件夹里（2026-11-27 之前分在 navdata\{native,dev,dev\packs,dev\markers} 四处）。
#
#   <图>\map.json            点图元数据（指纹 / 点数 / bbox）
#   <图>\navmesh.bin          可走面（原生就有 NavMeshGraph 的图才有）
#   <图>\<指纹>.txt           点图草稿（编辑中档读写这里）
#   <图>\markers.txt          蹲守点 / 守卫区 / 守卫点 / 标签 / 出生点
#   <图>\manifest.json        草稿状态（谁建的 / 什么时候 / grow|keep）
#   <图>\native\{map.json,navmesh.bin}   ① 冻结副本（只读，回滚用）
#   <图>\final\<指纹>.txt     成品（成品档读这里，只读）
#
# 派生目录（不属于任何一张图，可以随时重建）：
#   data\maps\_inbox\    插件写出来的可走面导出 / 录制轨迹（原来的 dev\vis）
#   data\maps\_archive\ 删草稿 / 清标记 / 发布前快照（原来的 dev\archive）
MAPS = os.path.join(DATA_ROOT, "maps")
COMMON = "00_公共"          # 公共文件（names / _index / 清单）：不属于任何一张图
NATIVE_SUB = "native"       # <图>\native\  ① 冻结副本
FINAL_SUB = "final"         # <图>\final\   成品
INBOX = os.path.join(MAPS, "_inbox")      # 导出收件箱
ARCHIVE = os.path.join(MAPS, "_archive")  # 回收站

# 兼容旧名（2026-11-27 之前是三个独立的数据根，现在同一个根）：
# 老调用点写 P.NATIVE / P.DEV / P.PACKS_DIR / P.MARKERS 都还指得动，
# 但"① 备份版"现在要用 native_files() / native_dir() 读 <图>\native\。
NATIVE = MAPS
DEV = MAPS
TEST = MAPS
DATA = MAPS

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

# 2026-11-25：运行时状态搬到工程端。插件启动时由控制台注入 UCF_MOD_DIR，
# 所以 ucf_mod.json / ucf_navcmd.txt 不再写游戏目录。
RUNTIME = os.path.abspath(os.environ.get("UCF_RUNTIME", "").strip()
                          or os.path.join(PROJ, "run", "runtime"))
CFG_PATH = os.path.join(RUNTIME, "ucf_mod.json")
NAVCMD = os.path.join(RUNTIME, "ucf_navcmd.txt")


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


def _norm_history(raw):
    r"""把 history 统一成 [{"game_dir", "name", "note"}]。

    2026-11-24 用户要求：每个位置可以起名字、写备注。老配置里 history 是
    纯字符串，读的时候按「没名字」兼容，写回去时统一成 dict。
    """
    out = []
    for item in (raw or []):
        if isinstance(item, dict):
            g = str(item.get("game_dir") or "").strip()
            name = str(item.get("name") or "").strip()
            note = str(item.get("note") or "").strip()
        else:
            g, name, note = str(item or "").strip(), "", ""
        if not g:
            continue
        out.append({"game_dir": os.path.abspath(g), "name": name, "note": note})
    return out


def load_history():
    r"""游戏位置列表：**当前生效的那一个永远排第一**，后面是历史记录。

    2026-11-22 用户要求：当前位置可能是程序逻辑解析出来的（环境变量 / 工程
    tools/deploy.json），不一定是我们写进用户配置的，但它同样要出现在列表里 ——
    否则第一次打开时下拉框空着，用户以为没配置。

    返回 [{"game_dir", "exists", "current", "source", "name", "note"}]
    """
    cur = os.path.abspath(game_dir_of())
    label = {it["game_dir"].lower(): (it["name"], it["note"])
             for it in _norm_history(load_user_cfg().get("history"))}
    out, seen = [], set()

    def add(path, source):
        g = os.path.abspath(str(path)) if path else ""
        if not g or g.lower() in seen:
            return
        seen.add(g.lower())
        name, note = label.get(g.lower(), ("", ""))
        out.append({
            "game_dir": g,
            "exists": os.path.isfile(os.path.join(g, "UnityCrossFire.exe")),
            "current": g.lower() == cur.lower(),
            "source": source,
            "name": name,
            "note": note,
        })

    add(cur, DEPLOY_SOURCE)
    for item in _norm_history(load_user_cfg().get("history")):
        add(item["game_dir"], "history")
    return out[:HISTORY_MAX]


def save_deploy(game_dir):
    """把用户选的游戏目录写进用户配置（并记入历史），返回写入路径。

    控制台选完 UnityCrossFire.exe 后调这里；写的是 %LOCALAPPDATA%\\UCFMod\\deploy.json，
    不动工程里的 tools/deploy.json。下次启动 ucf_paths 会优先读它。

    历史里的名字 / 备注按路径带过去 —— 换一次位置就把名字清掉的话，
    用户等于每切一次都要重新命名。
    """
    game_dir = os.path.abspath(str(game_dir))
    old = load_user_cfg()
    keep = {"name": "", "note": ""}
    history = []
    for item in _norm_history(old.get("history")):
        if item["game_dir"].lower() == game_dir.lower():
            keep["name"], keep["note"] = item["name"], item["note"]
        else:
            history.append(item)
    history.insert(0, {"game_dir": game_dir, "name": keep["name"], "note": keep["note"]})
    data = {
        "deploy": os.path.join(game_dir, "ucf_mod"),
        "game_dir": game_dir,
        "history": history[:HISTORY_MAX],
        "updated": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return _write_user_cfg(data)


def rename_history(game_dir, name, note=""):
    r"""给某个位置起名字 / 写备注；它不在历史里（比如当前这份是解析出来的）也照样记一条。"""
    game_dir = os.path.abspath(str(game_dir))
    cfg = load_user_cfg()
    hist = _norm_history(cfg.get("history"))
    for item in hist:
        if item["game_dir"].lower() == game_dir.lower():
            item["name"], item["note"] = name, note
            break
    else:
        hist.insert(0, {"game_dir": game_dir, "name": name, "note": note})
    cfg["history"] = hist[:HISTORY_MAX]
    return _write_user_cfg(cfg)


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
    cfg["history"] = [it for it in _norm_history(cfg.get("history"))
                      if it["game_dir"].lower() != game_dir.lower()]
    _write_user_cfg(cfg)
    return True


def _resolve_env_dir(env_name, default):
    """环境变量（控制台启动游戏时注入）优先，否则用 ② 开发版下的默认位置。"""
    p = os.environ.get(env_name, "").strip()
    if p:
        return os.path.abspath(p)
    return default


# 插件三档启动注入的三个根。一图一夹之后三者可以指向同一个 data\maps：
#   草稿  = <根>\<图>\<指纹>.txt        （UCF_PACK_DIR + UCF_PACK=<图>）
#   标记  = <根>\<图>\markers.txt        （UCF_MARKERS_DIR + UCF_PACK=<图>）
#   成品  = <根>\<图>\final\<指纹>.txt   （UCF_PACK_DIR=<根> + UCF_NAV_SEARCH=1，按指纹找图）
EXPORT = _resolve_env_dir("UCF_EXPORT_DIR", INBOX)
PACKS_DIR = _resolve_env_dir("UCF_PACK_DIR", MAPS)
MARKERS = _resolve_env_dir("UCF_MARKERS_DIR", MAPS)
FINAL = MAPS                    # 成品根：<图>\final\ 的父目录
NAV = MAPS                      # 旧的 nav\ 已经没有内容，只作回退名

# 导出根：插件把新扫描 / navmesh 写这里（② 开发版的收件箱）。
# 兼容旧名 VIS；2026-11-18 之前它指向 ③ 部署版。工具只读这里，不再碰 ③\vis。
VIS = EXPORT
GAME_VIS = os.path.join(DEPLOY, "vis")   # ③ 里的旧位置（迁移后只留 README）
LEGACY_VIS = GAME_VIS
# 当前版本自带的可走面（原生备份里也有 navmesh）
DATAVIS = INBOX
# ③ 里的回滚区：DLL 备份 + 历史导出快照。游戏不读，不算部署数据。
BACKUP = os.path.join(DEPLOY, "backup")
NAMES_FILE = os.path.join(MAPS, COMMON, "names.json")

# ---------------------------------------------------------------- 图文件夹（按地图分类）
# 2026-11-27：一张图一个文件夹（data\maps\序号_场景名中文名\），点图 / 可走面 / 编辑标记 /
# 成品 / 冻结副本全在里面。文件夹名以 docs/guide/地图对照表.md 为准。
# ① 备份版不再是独立的数据根：它是每张图自己的 native\ 子目录，用 native_dir()/native_files() 读。
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


def folder_dir(name, root=None):
    r"""图文件夹本身：data\maps\<序号_场景名中文名>\（传文件夹名，不传关卡）。"""
    return os.path.join(root or MAPS, str(name or ""))


def native_dir(name, root=None):
    r"""① 冻结副本：<图>\native\。"""
    return os.path.join(folder_dir(name, root), NATIVE_SUB)


def final_dir(name, root=None):
    r"""成品：<图>\final\。"""
    return os.path.join(folder_dir(name, root), FINAL_SUB)


def folder_names(root=None):
    r"""所有地图文件夹名（有 map.json 的才算；跳过 _inbox / _archive / 00_公共）。"""
    root = root or MAPS
    out = []
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return out
    for name in names:
        if name.startswith((".", "_")) or name == COMMON:
            continue
        if os.path.isfile(os.path.join(root, name, MAP_JSON)):
            out.append(name)
    return out


def native_files(root=None):
    r"""[(图文件夹/map.json, 绝对路径)] —— ① 冻结副本里的点图。"""
    root = root or MAPS
    out = []
    for name in folder_names(root):
        p = os.path.join(native_dir(name, root), MAP_JSON)
        if os.path.isfile(p):
            out.append((name + "/" + MAP_JSON, p))
    return out


def native_navmesh_files(root=None):
    r"""[(图文件夹/navmesh.bin, 绝对路径)] —— ① 冻结副本里的可走面。

    注意：有的图原生只有可走面、没有 PointGraph（胜利广场 / 死亡擂台），
    所以这里按目录扫，不能只按「有 map.json 的图」扫。
    """
    return navmesh_files(root or MAPS, NATIVE_SUB)


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


def common_dir(root=None):
    """公共文件目录：00_公共\（names / _index / 清单 / 冻结台账都在这一处）。"""
    return os.path.join(root or MAPS, COMMON)


def names_dir(root=None):
    """names.json 放哪：00_公共\\。"""
    return os.path.join(root or MAPS, COMMON)


def index_dir(root=None):
    """_index.json / INDEX.md 放哪：00_公共\\。"""
    return os.path.join(root or MAPS, COMMON)


def manifest_dir(root=None):
    """清单类文件（SHA256SUMS / README / .frozen.json）放哪：00_公共\\。"""
    return os.path.join(root or MAPS, COMMON)


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


def map_files(root=None, sub=""):
    r"""[(相对路径, 绝对路径)] —— 这个根下的所有地图 JSON。

    根 = data\maps，sub="" 读开发版（<图>\map.json），sub="native" 读 ① 冻结副本
    （<图>\native\map.json）。相对路径一律是「<图>/map.json」，搬过 native 之后
    调用方不用关心物理层级。
    """
    root = root or MAPS
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
        p = os.path.join(root, name, sub, MAP_JSON) if sub else os.path.join(root, name, MAP_JSON)
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


def navmesh_files(root=None, sub=""):
    r"""[(相对路径, 绝对路径)] —— 这个根下的全部可走面（比对 / 统计用）。

    sub="" 读 <图>\navmesh.bin；sub="native" 读 <图>\native\navmesh.bin。
    相对路径一律是「<图>/navmesh.bin」。
    """
    root = root or MAPS
    out = []
    if not root or not os.path.isdir(root):
        return out
    try:
        names = sorted(os.listdir(root))
    except OSError:
        return out
    for name in names:
        if name.startswith((".", "_")) or name == COMMON:
            continue
        d = os.path.join(root, name, sub) if sub else os.path.join(root, name)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if fn.startswith("navmesh") and fn.lower().endswith(".bin"):
                out.append((name + "/" + fn, os.path.join(d, fn)))
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


def tool(name):
    r"""命令行脚本的绝对路径：tools\ 根 → geo\ → data\ → _oneoff\ 依次找。

    脚本分目录以后，调用方只写脚本名（P.tool("geo2web.py")），不用跟着目录搬家。
    找不到就返回 tools\<name>，让调用方自己报"找不到"。
    """
    for sub in ("", "geo", "data", "_oneoff"):
        p = os.path.join(TOOLS, sub, name) if sub else os.path.join(TOOLS, name)
        if os.path.isfile(p):
            return p
    return os.path.join(TOOLS, name)
