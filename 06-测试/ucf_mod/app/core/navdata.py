#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""navdata.py —— 地图数据「一图一夹」管理：① 冻结副本  ② 开发数据  ③ 部署端

  ---------------------------------------------------------------------------
  ① 冻结副本  data/maps/<图>/native/   UCF 原版点图 + 可走面，只读、永不编辑
                                        清单：00_公共/SHA256SUMS.txt + .frozen.json
  ② 开发数据  data/maps/<图>/          唯一数据源（控制台三档启动都读这里）
                                         map.json / navmesh.bin / <指纹>.txt / markers.txt
                                         manifest.json；成品在 <图>/final/<指纹>.txt
  派生目录    data/maps/_inbox/        插件写出来的导出收件箱
              data/maps/_archive/      删草稿 / 清标记 / 发布前快照 / 迁移日志
  ③ 游戏目录                          运行时：winhttp.dll / winhttp_orig.dll + 本体补丁
                                        （2026-11-25 起不建 ucf_mod/）
  流水线：游戏导出 -> _inbox ->（import 整理）-> <图>/map.json ->（pack promote）-> <图>/final/
  ---------------------------------------------------------------------------

  三档启动（控制台底部按钮，不往游戏目录搬数据）：
      成品    按指纹找 <图>/final/<指纹>.txt（UCF_PACK_DIR=data/maps + UCF_NAV_SEARCH=1
              + UCF_NAV_SUB=final），markers 也跟着 <图>/markers.txt；只读靠文件属性
      编辑中  UCF_PACK=<图>，读写 <图>/<指纹>.txt（可写）  调图、试路线、游戏内存回草稿
      原版    插件待机，什么都不读                        对照原生行为

常用命令（在 app/core/ 下跑）：

    python navdata.py status              # ①②③ 各自在哪、各有几个文件、是否只读
    python navdata.py verify              # 校验冻结副本没被动过（SHA256 清单）
    python navdata.py restore             # 开发数据 <- 冻结副本（丢掉开发改动）
    python navdata.py import              # 整理收件箱：vis 归位 + 原始导出 -> <图>/map.json
    python navdata.py diff                # 开发数据 vs 冻结副本差在哪 + 成品里有几张图
    python navdata.py freeze --force      # 用当前数据重建「冻结副本」（确认要重新冻结时才用）

  草稿 = 编辑中：一份只对某一张图生效的路线改动，就在那张图的文件夹里
  （data/maps/<序号_场景名中文名>/<指纹>.txt，序号见《地图对照表》）；
  插件用 UCF_PACK / UCF_FP 读它，别的一张图一个字节都不动。

    python navdata.py pack list                     # 有哪些草稿
    python navdata.py pack new --level 11 --grow    # 给 level11 建空白底图草稿
    python navdata.py pack promote <图文件夹>        # 编辑中 -> 成品（<图>/final/<指纹>.txt）

注意：freeze 只收【原生】内容 —— 判据是导出文件里 map.source
      （"game" 才算原生；"ours"/"practice" = 我们造的，一律不收），
      碰到我们造的图时按对照表写一份「原生为空」的空档文件说明原因。
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time

def _setup_console():
    """控制台（双击 bat）用系统编码（中文 Windows = cp936 才能显示中文）；
    管道/重定向时统一 UTF-8，方便别的程序读。

    顺带把输出抄一份到**工程端 log\\navdata.log** —— 2026-11-27 起，以前在
    data\\navdata\\_logs\\，跟插件日志分两处，排查要在两个目录来回翻。
    老位置那份历史日志第一次启动时并进来（navdata_migrate_log），不会从空白开始。
    环境变量 UCF_NO_LOG_TEE=1 可整体关掉抄写（自检用，免得污染真日志）。"""
    out = sys.stdout
    enc = (getattr(out, "encoding", "") or "").lower().replace("-", "")
    try:
        if getattr(out, "isatty", lambda: False)() and enc not in ("utf8", "cp65001"):
            out.reconfigure(errors="replace")          # 就用控制台自己的编码
        else:
            out.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        if os.environ.get("UCF_NO_LOG_TEE"):
            return
        os.makedirs(P.LOG_DIR, exist_ok=True)
        navdata_migrate_log()               # 老位置的历史日志并一次
        rotate_log(NAVDATA_LOG)             # 超 16 MB 先轮转，再接着写
        sys.stdout = _Tee(out, NAVDATA_LOG)
    except Exception:
        pass


class _Tee(object):
    """stdout 抄一份到日志文件（UTF-8），出问题时能直接把日志发出来。"""

    def __init__(self, stream, path):
        self.stream = stream
        self.path = path

    def write(self, s):
        try:
            self.stream.write(s)
        except Exception:
            pass
        try:
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(s)
        except OSError:
            pass
        return len(s)

    def flush(self):
        try:
            self.stream.flush()
        except Exception:
            pass

    def isatty(self):
        return False

    def __getattr__(self, name):
        return getattr(self.stream, name)

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
for _p in (os.path.join(UCF_ROOT, "app", "core"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import ucf_paths as P  # noqa: E402
import map_table  # noqa: E402  序号 + 文件夹命名（和《地图对照表》第一张表一致）

# ---------------------------------------------------------------- 日志落点（工程端 log\）
# 2026-11-27：控制台/工具自己的日志也收进工程端 log\，跟插件的 ucf_mod.log / autotest.txt
# 同一个目录。以前 stdout 抄本在 data\navdata\_logs\、发布流水在 dev\final\_publish.log，
# 加上插件日志一共三处，排查时要挨个翻 —— 用户要求集中。
NAVDATA_LOG = os.path.join(P.LOG_DIR, "navdata.log")
#: 和 cfg.c 的 UCF_LOG_MAX_BYTES 对齐：超了轮转，只保 1 代
LOG_MAX_BYTES = 16 * 1024 * 1024
#: 迁移前的老位置：只用于「第一次并进 log\」，之后不再写
LEGACY_NAVDATA_LOG = os.path.join(P.DATA_ROOT, "navdata", "_logs", "navdata.log")


def rotate_log(path):
    r"""path 超过 16 MB 就改名成 <名>.prev.log（只保 1 代），返回是否转了。

    stdout 抄写没人管大小的话会一直涨，跑久了是几百 MB，还拖慢 tail。
    命名跟插件的 ucf_mod.log -> ucf_mod.prev.log 一致。
    """
    try:
        if os.path.getsize(path) < LOG_MAX_BYTES:
            return False
    except OSError:
        return False
    stem, ext = os.path.splitext(path)              # navdata.log -> navdata
    prev = stem + ".prev" + (ext or ".log")         # navdata.prev.log
    try:
        os.replace(path, prev)
        return True
    except OSError:
        return False


def _append_file(src, dst):
    r"""把 src 的字节追加到 dst 后面（不解析、不改编码），成功后删掉 src。

    字节级搬运：老日志是 UTF-8，新日志也是，中间不掺任何解码 —— 省得碰上
    半行截断或旧的 cp936 内容时整个文件读不出来。
    """
    try:
        with open(src, "rb") as f:
            data = f.read()
        if not data:
            os.remove(src)
            return True
        d = os.path.dirname(dst)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(dst, "ab") as f:
            f.write(data)
        os.remove(src)
        return True
    except OSError:
        return False


def navdata_migrate_log():
    r"""把老位置 data\navdata\_logs\navdata.log 并进 log\navdata.log（做一次就没了）。

    不并的话历史日志孤零零躺在旧目录，新日志从空白开始 —— 排查时
    「最后一次正常」那半段就丢了。
    """
    if not os.path.isfile(LEGACY_NAVDATA_LOG):
        return False
    ok = _append_file(LEGACY_NAVDATA_LOG, NAVDATA_LOG)
    try:                                            # 目录空了就顺手删掉
        d = os.path.dirname(LEGACY_NAVDATA_LOG)
        if os.path.isdir(d) and not os.listdir(d):
            os.rmdir(d)
    except OSError:
        pass
    return ok


SUBS = ("maps", "nav", "vis")
KEEP_ALWAYS = {"nogen.txt", "collect.flag", "README.txt", "README.md", "INDEX.md", "_index.json"}
MAP_TABLE_RE = re.compile(r"^\|\s*(\d{1,3})\s*\|\s*(level\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|")


# ---------------------------------------------------------------- 小工具
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, obj, indent=1):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def load_table():
    """序号 / 关卡 / 中文名 / 场景名 / 备注 —— 只读 docs/地图对照表.md 的第一张表。"""
    path = P.doc("地图对照表.md")
    rows, started = [], False
    if not os.path.exists(path):
        return rows
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                if started:
                    break
                continue
            m = MAP_TABLE_RE.match(s)
            if not m:
                if started and not s.startswith("|"):
                    break
                continue
            started = True
            rows.append({"no": "%02d" % int(m.group(1)), "level": m.group(2),
                         "cn": m.group(3).strip(), "scene": m.group(4).strip(),
                         "note": m.group(5).strip()})
    rows.sort(key=lambda r: r["no"])
    return rows


def make_readonly(path):
    try:
        os.chmod(path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
    except OSError:
        pass


def make_writable(path):
    try:
        os.chmod(path, 0o666)
    except OSError:
        pass


# ---------------------------------------------------------------- 成品（多版本）
# 2026-11-21：成品档「按包启动」（UCF_PACK_DIR=<爪根>、UCF_PACK=<版本名>），和编辑中
# 走同一套加载逻辑（grow/keep 建点、0 点图都照常），所以发布过来效果一模一样。
#
# 成品可以并存多个版本，**一版 = 一整套数据**（所有图一起，启动时只选一次）：
#
#   navdata\dev\final\
#     <包名>\  …           每个版本一个目录（插件按 <包根>\<包名> 读它）；
#                          名字默认沿用测试包名，重名 -2 / -3；旧数据还是 v1、v2
#       <指纹>.txt  nogen.txt
#     _index.json          台账：每版创建时间 / 继承自哪版 / 含哪些图 / 每图 sha、点边
#     _current.txt         当前选中的版本（控制台启动「成品」时读它）
#
# 发布默认「新建一版」：以当前版为底整套复制，再用这个包替换对应图；老版本一律保留，
# 新版本名 = 测试包名（--as 可改，重名自动加 -2）。不要的版本用 final rm 真删
# （控制台成品页「删除」同一个动作）；想留个后手才加 --keep（挪进 dev\archive\final_old\）。
# 2026-11-27 一图一夹：成品进 <图>\final\<指纹>.txt（不再是平铺的 final\<指纹>.txt）。
#   发布 = 覆盖这张图那一份；覆盖前旧成品进 _archive\final_prev\<指纹>\（每图留最近 5 份）。
#   台账 00_公共\final_index.json 记 level / label / 发布时刻 / sha256。
FINAL_INDEX = os.path.join(P.MAPS, P.COMMON, "final_index.json")
# 旧的多版本成品机制（2026-11-24 已废）：只读兼容，挪到回收站目录下，不再参与运行
LEGACY_FINAL_ROOT = os.path.join(P.ARCHIVE, "final_versions_legacy")
FINAL_ROOT = LEGACY_FINAL_ROOT
FINAL_CURRENT = os.path.join(FINAL_ROOT, "_current.txt")
FINAL_ARCHIVE = os.path.join(P.ARCHIVE, "final_old")
LEGACY_FINAL = os.path.join(P.ARCHIVE, "nav_legacy")
_NAV_FP_RE = re.compile(r"^n\d+-[0-9a-f]{16}\.txt$", re.I)
FINAL_NAME_BAD = '\\/:*?"<>| '


def final_map_files(d):
    r"""某个版本目录里真正的路线文件（<指纹>.txt）；nogen.txt / _index.json 不算。"""
    if not d or not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if _NAV_FP_RE.match(f))


def final_ensure_nogen(d):
    r"""版本目录补一份 nogen.txt：空图不自动铺点（和编辑中的 grow/keep 包保持一致）。"""
    if not d:
        return
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "nogen.txt")
    if os.path.isfile(p):
        return
    try:
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write("")
        make_readonly(p)
    except OSError:
        pass


def final_version_path(name):
    return os.path.join(FINAL_ROOT, name) if name else ""


def final_index_read():
    idx = {}
    try:
        with open(FINAL_INDEX, "r", encoding="utf-8") as f:
            idx = json.load(f) or {}
    except (OSError, ValueError):
        idx = {}
    idx.setdefault("format", "ucf-final-versions")
    idx.setdefault("version", 1)
    idx.setdefault("seq", 0)
    idx.setdefault("current", "")
    idx.setdefault("versions", [])
    return idx


def final_index_write(idx):
    os.makedirs(FINAL_ROOT, exist_ok=True)
    write_json(FINAL_INDEX, idx)
    try:
        with open(FINAL_CURRENT, "w", encoding="utf-8", newline="\n") as f:
            f.write((idx.get("current") or "") + "\n")
    except OSError:
        pass


def final_scan_maps(d):
    r"""扫一个版本目录：{指纹: {file, sha256, node, edge, bytes, mtime}}"""
    out = {}
    for fn in final_map_files(d):
        p = os.path.join(d, fn)
        nd, ed = edit_counts(p)
        try:
            st = os.stat(p)
            mt, sz = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)), st.st_size
        except OSError:
            mt, sz = "", 0
        out[fn[:-4]] = {"file": fn, "sha256": sha256(p), "node": nd, "edge": ed,
                        "bytes": sz, "mtime": mt}
    return out


def final_versions():
    r"""所有成品版本（按台账顺序）。台账和磁盘对不上时以磁盘为准：
    目录没了标 exists=False，磁盘上多出来的目录当场补进来。"""
    idx = final_index_read()
    out, seen = [], set()
    for v in idx.get("versions") or []:
        name = (v.get("name") or "").strip()
        if not name:
            continue
        d = final_version_path(name)
        item = dict(v)
        item["name"] = name
        item["path"] = d
        item["exists"] = os.path.isdir(d)
        item["maps"] = dict(v.get("maps") or {})
        if item["exists"]:
            for fp, m in final_scan_maps(d).items():     # 磁盘上的实际内容优先
                item["maps"][fp] = dict(item["maps"].get(fp) or {}, **m)
        out.append(item)
        seen.add(name)
    if os.path.isdir(FINAL_ROOT):
        for name in sorted(os.listdir(FINAL_ROOT)):
            d = os.path.join(FINAL_ROOT, name)
            if name.startswith("_") or name in seen or not os.path.isdir(d):
                continue
            mt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(d).st_mtime))
            out.append({"name": name, "path": d, "exists": True, "created": mt, "updated": mt,
                        "base": "", "note": "（磁盘上多出来的目录，已自动登记）",
                        "maps": final_scan_maps(d)})
    return out


def final_current():
    r"""当前选中的成品版本名（没有就返回空串）。"""
    names = [v["name"] for v in final_versions() if v["exists"]]
    idx = final_index_read()
    for cand in ((idx.get("current") or "").strip(), final_current_file()):
        if cand and cand in names:
            return cand
    return names[-1] if names else ""


def final_current_file():
    try:
        with open(FINAL_CURRENT, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def final_set_current(name):
    idx = final_index_read()
    if name not in [v.get("name") for v in idx.get("versions") or []]:
        sys.exit("没有这个成品版本：%s" % name)
    idx["current"] = name
    final_index_write(idx)


def final_check_name(name):
    r"""版本名：字母数字下划线减号点、中文也行；不许路径分隔符 / 空格 / Windows 非法字符。"""
    n = (name or "").strip()
    if not n or len(n) > 48:
        return "版本名要 1~48 个字符"
    if n.startswith("_") or n in (".", ".."):
        return "版本名不能以下划线开头，也不能是 . / .."
    for ch in n:
        if ch in FINAL_NAME_BAD or ord(ch) < 32:
            return "版本名不能包含这些字符：\\ / : * ? \" < > | 空格"
    if os.path.isdir(final_version_path(n)):
        return "已经有这个版本目录了：%s" % n
    return ""


def final_next_name(idx=None):
    r"""自动版本号：v1 / v2 / v3……（改名了也不会撞号，seq 只增不减）"""
    idx = idx if idx is not None else final_index_read()
    seq = int(idx.get("seq") or 0)
    taken = set()
    for v in idx.get("versions") or []:
        taken.add(v.get("name"))
    while True:
        seq += 1
        name = "v%d" % seq
        if name not in taken and not os.path.isdir(final_version_path(name)):
            idx["seq"] = seq
            return name


def final_name_from_pack(pack):
    r"""版本名默认跟测试包同名：packs/<地图>/<包> -> <包>。

    包名只允许英文字母、数字、下划线和短横线（pack_id_ok 管着），本来就能当目录名；
    这里再按 final_check_name 的规则兜一遍，防止手工塞进来的怪名字。
    """
    leaf = str(pack or "").replace("\\", "/").strip("/").split("/")[-1]
    out = "".join("_" if (ch in FINAL_NAME_BAD or ord(ch) < 32) else ch for ch in leaf)
    return out.strip("._ ")[:48].strip("._ ")


def final_unique_name(base, idx=None):
    r"""想要的版本名被占了就往下排：<包名>、<包名>-2、<包名>-3……（不覆盖、不删任何版本）。"""
    idx = idx if idx is not None else final_index_read()
    base = (base or "").strip()
    if not base:
        return final_next_name(idx)          # 没有参照名（老成品迁移）才退回 v1/v2/v3
    taken = set(v.get("name") for v in idx.get("versions") or [])
    name, n = base, 1
    while name in taken or os.path.isdir(final_version_path(name)):
        n += 1
        name = ("%s-%d" % (base[:46], n))[:48]
    return name


def final_new_version(base=None, note="", name=""):
    r"""新建一版（默认以 base 版为底整套复制）。返回 (版本名, 复制了几个文件)。

    name 为空才自动编号 v1/v2/v3（老成品迁移用）；发布时传测试包名，
    所以成品版本默认就叫测试包的名字，重名自动 -2 / -3。
    """
    idx = final_index_read()
    name = final_unique_name(name, idx) if name else final_next_name(idx)
    d = final_version_path(name)
    os.makedirs(d, exist_ok=True)
    src_dir = final_version_path(base) if base else ""
    copied = 0
    if src_dir and os.path.isdir(src_dir):
        for fn in os.listdir(src_dir):
            s = os.path.join(src_dir, fn)
            if not os.path.isfile(s):
                continue
            t = os.path.join(d, fn)
            if os.path.exists(t):
                make_writable(t)
            shutil.copyfile(s, t)
            if fn.lower().endswith(".txt"):
                make_readonly(t)
            copied += 1
    final_ensure_nogen(d)
    maps_meta = {}
    if base:
        for v in idx.get("versions") or []:
            if v.get("name") == base:
                maps_meta = {k: dict(m) for k, m in (v.get("maps") or {}).items()}
                break
    for fp, m in final_scan_maps(d).items():
        maps_meta[fp] = dict(maps_meta.get(fp) or {}, **m)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    idx["versions"].append({"name": name, "created": now, "updated": now,
                            "base": base or "", "note": note, "maps": maps_meta})
    idx["current"] = name
    final_index_write(idx)
    return name, copied


def final_ensure_root():
    r"""第一次用：把旧成品目录 ②\nav\ 里的数据搬成 v1（搬完清空旧址）。
    没有旧数据就只建一个空台账，什么都不动。"""
    try:
        os.makedirs(FINAL_ROOT, exist_ok=True)
    except OSError:
        return
    idx = final_index_read()
    if idx.get("versions"):
        return
    legacy = final_map_files(LEGACY_FINAL)
    if not legacy:
        final_index_write(idx)
        return
    name = final_next_name(idx)
    d = final_version_path(name)
    os.makedirs(d, exist_ok=True)
    for fn in legacy:
        src = os.path.join(LEGACY_FINAL, fn)
        dst = os.path.join(d, fn)
        shutil.copyfile(src, dst)
        make_readonly(dst)
        try:
            make_writable(src)
            os.remove(src)          # 旧位置清空：成品只留 final\ 这一处
        except OSError:
            pass
    final_ensure_nogen(d)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    idx["versions"].append({"name": name, "created": now, "updated": now, "base": "",
                            "note": "从旧成品目录 nav\\ 自动迁过来", "maps": final_scan_maps(d)})
    idx["current"] = name
    final_index_write(idx)
    print("已把旧成品（② nav\\ %d 个文件）迁成成品版本 %s" % (len(legacy), name))


# ---------------------------------------------------------------- 成品（单份）
# 2026-11-24：一张图只有一份成品。final\<指纹>.txt 平铺，不再有版本目录，也不再有
# _current.txt。发布 = 覆盖同图那份；覆盖前把旧成品复制到 archive\final_prev\<指纹>\
# （每张图只留最近 5 份，界面上不出现，只用于误发布时找回）。
FINAL_PREV = os.path.join(P.ARCHIVE, "final_prev")
#: 发布流水（TSV）：2026-11-27 起集中到工程端 log\\publish.log，跟插件日志同目录。
#: 每张图的权威发布信息仍在 final\\_index.json（published / sha256 / from），
#: 这里只是一条按时间排的流水账 —— 所以 log\\ 被清掉也不影响成品追溯。
PUBLISH_LOG = os.path.join(P.LOG_DIR, "publish.log")
#: 迁移前的老位置：只用于「第一次并进 log\\」
LEGACY_PUBLISH_LOG = os.path.join(FINAL_ROOT, "_publish.log")


def publish_log_migrate():
    r"""把老位置 final\\_publish.log 并进 log\\publish.log（做一次就没了）。"""
    if not os.path.isfile(LEGACY_PUBLISH_LOG):
        return False
    return _append_file(LEGACY_PUBLISH_LOG, PUBLISH_LOG)


def _store_index_read():
    idx = {}
    try:
        with open(FINAL_INDEX, "r", encoding="utf-8") as f:
            idx = json.load(f) or {}
    except (OSError, ValueError):
        idx = {}
    if not isinstance(idx, dict) or idx.get("format") != "ucf-final-single":
        idx = {"format": "ucf-final-single", "version": 2, "maps": {}}
    idx.setdefault("maps", {})
    return idx


def _store_index_write(idx):
    os.makedirs(os.path.dirname(FINAL_INDEX), exist_ok=True)
    write_json(FINAL_INDEX, idx)


_FP_FOLDER = {}


def _fp_to_folder():
    r"""{指纹: 图文件夹名} —— 成品要落到 <图>inal，靠每张图 map.json 里的指纹认图。"""
    out = {}
    for name in P.folder_names():
        try:
            doc = read_json(os.path.join(P.folder_dir(name), P.MAP_JSON))
        except Exception:                  # noqa: BLE001  读不了就跳过，不影响别的图
            continue
        fp = str((doc.get("map") or {}).get("fingerprint") or "")
        if fp:
            out[fp] = name
    return out


def final_dir_of(fp):
    r"""这张图的成品目录 <图>inal；认不出图就返回空串。"""
    fp = str(fp or "").strip()
    if not fp:
        return ""
    if fp not in _FP_FOLDER:
        _FP_FOLDER.clear()
        _FP_FOLDER.update(_fp_to_folder())
    name = _FP_FOLDER.get(fp)
    return P.final_dir(name) if name else ""


def final_store_files():
    r"""成品里每个地图一份：[(指纹, 路径)] —— 扫每张图的 <图>inal。"""
    out = []
    for name in P.folder_names():
        d = P.final_dir(name)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            if _NAV_FP_RE.match(fn):
                out.append((fn[:-4], os.path.join(d, fn)))
    return out


def final_store_map(fp):
    fp = str(fp or "").strip()
    d = final_dir_of(fp)
    return os.path.join(d, fp + ".txt") if (d and fp) else ""


def final_store_has(fp):
    p = final_store_map(fp)
    return bool(p) and os.path.isfile(p)


def final_store_meta():
    r"""{指纹: {path,node,edge,bytes,mtime,sha256,level,label,published,...}}。

    磁盘上的实际文件优先；台账只补 level/label/发布时间。sha256 每次现算
    （成品最多 11 个文件，几十 KB，界面刷新无压力）。
    """
    idx = _store_index_read()
    ledger = idx.get("maps") or {}
    out = {}
    for fp, p in final_store_files():
        try:
            st = os.stat(p)
        except OSError:
            continue
        nd, ed = edit_counts(p)
        item = {"fp": fp, "path": p, "file": os.path.basename(p),
                "node": nd, "edge": ed, "bytes": st.st_size,
                "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)),
                "sha256": sha256(p)}
        item.update({k: v for k, v in (ledger.get(fp) or {}).items()
                     if k in ("level", "label", "published", "created", "from", "note")})
        out[fp] = item
    return out


def final_store_stats():
    meta = final_store_meta()
    latest = ""
    for m in meta.values():
        latest = max(latest, str(m.get("published") or m.get("mtime") or ""))
    return {"n": len(meta), "maps": meta, "latest": latest}


def _store_prune_prev(d, keep=5):
    try:
        files = sorted((os.path.join(d, fn) for fn in os.listdir(d)
                        if fn.lower().endswith(".txt")),
                       key=os.path.getmtime, reverse=True)
    except OSError:
        return
    for p in files[keep:]:
        try:
            make_writable(p)
            os.remove(p)
        except OSError:
            pass


def final_store_publish(pid, note=""):
    r"""草稿 -> 成品：覆盖同指纹的那一份，返回 (fp, 路径, 点数, 边数, sha256)。"""
    pdir, man, fp = find_pack(pid)
    src = os.path.join(pdir, fp + ".txt")
    if not os.path.isfile(src):
        sys.exit("草稿里没有 %s（先在里面写路线）" % (fp + ".txt"))
    dst = final_store_map(fp)
    if not dst:
        sys.exit("认不出 %s 是哪张图（map.json 里没有这个指纹）" % fp)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isfile(dst):
        bdir = os.path.join(FINAL_PREV, fp)
        try:
            os.makedirs(bdir, exist_ok=True)
            make_writable(dst)
            shutil.copy2(dst, os.path.join(bdir, time.strftime("%Y%m%d_%H%M%S") + ".txt"))
            _store_prune_prev(bdir, 5)
        except OSError:
            pass
        make_writable(dst)
    tmp = dst + ".tmp"
    shutil.copyfile(src, tmp)
    os.replace(tmp, dst)
    make_readonly(dst)
    final_ensure_nogen(os.path.dirname(dst))
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    nd, ed = edit_counts(dst)
    sha = sha256(dst)
    idx = _store_index_read()
    idx["maps"][fp] = {
        "file": fp + ".txt", "level": man.get("level", ""), "label": man.get("label", ""),
        "published": now, "node": nd, "edge": ed, "bytes": os.path.getsize(dst),
        "sha256": sha, "from": str(pid), "created": man.get("created", ""),
    }
    if note:
        idx["maps"][fp]["note"] = note
    _store_index_write(idx)
    try:
        publish_log_migrate()               # 老位置那份先并进来（只有第一次有用）
        os.makedirs(P.LOG_DIR, exist_ok=True)
        with open(PUBLISH_LOG, "a", encoding="utf-8", newline="\n") as f:
            f.write("%s\t%s\t%s\t%d/%d\t%s\t%s\n" % (
                now, fp, man.get("label", ""), nd, ed, sha[:12], note))
    except OSError:
        pass
    return fp, dst, nd, ed, sha


def final_store_remove(fp):
    p = final_store_map(fp)
    if not p or not os.path.isfile(p):
        return False
    make_writable(p)
    os.remove(p)
    idx = _store_index_read()
    idx["maps"].pop(str(fp), None)
    _store_index_write(idx)
    return True


def final_store_ensure():
    r"""一图一夹：成品目录是 <图>\final\，不预先建（没有成品就是没有这个文件夹）。

    这里只负责清掉旧机制留在回收站里的 _current.txt，顺手把老 final\ 里的成品搬进各图。
    """
    p = os.path.join(FINAL_ROOT, "_current.txt")
    if os.path.isfile(p):
        try:
            make_writable(p)
            os.remove(p)
        except OSError:
            pass


def pack_flags(path):
    r"""读包文件头里的 grow / keep（blank 是旧写法，等同 grow）。"""
    grow = keep = False
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for ln in f:
                s = ln.strip()
                if not s or s.startswith("#"):
                    continue
                if s in ("grow", "blank"):
                    grow = True
                elif s == "keep":
                    keep = True
                else:
                    break
    except OSError:
        pass
    return grow, keep


def walk_files(root):
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for fn in files:
            p = os.path.join(dirpath, fn)
            out.append(os.path.relpath(p, root).replace(os.sep, "/"))
    out.sort()
    return out


def summary(root, sub=""):
    """一版数据的概况：图 / 可走面 / 路线各几个，占多大，最近改动（只看数据，不算草稿/成品）。

    sub="native" 只看 ① 冻结副本（<图>/native/），空串看 ② 开发数据（<图>/ 根下）。
    """
    if not os.path.isdir(root):
        return {"path": root, "exists": False, "files": 0, "bytes": 0, "mtime": "-", "sub": {}}
    maps = P.map_files(root, sub)
    bins = P.navmesh_files(root, sub)
    routes = [] if sub else P.route_files(root)
    sub = {"图": len(maps), "可走面": len(bins), "路线": len(routes)}
    size, latest = 0, 0
    for _key, path in list(maps) + list(bins) + list(routes):
        try:
            size += os.path.getsize(path)
            latest = max(latest, os.path.getmtime(path))
        except OSError:
            pass
    return {"path": root, "exists": True, "files": sum(sub.values()), "bytes": size,
            "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(latest)) if latest else "-",
            "sub": sub}


def _walk_count(root, pred=None):
    """(文件数, 最近 mtime)；pred 只统计某类文件。"""
    n, latest = 0, 0.0
    if os.path.isdir(root):
        for dp, _dirs, fns in os.walk(root):
            for fn in fns:
                if pred and not pred(fn):
                    continue
                n += 1
                try:
                    latest = max(latest, os.path.getmtime(os.path.join(dp, fn)))
                except OSError:
                    pass
    return n, latest


def human(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return ("%.0f %s" % (n, unit)) if unit == "B" else ("%.1f %s" % (n, unit))
        n /= 1024.0


# ---------------------------------------------------------------- 原生判据
def reject_reason(doc):
    """返回不是原生的原因；空串 = 原生，收。"""
    m = doc.get("map") or {}
    src = str(m.get("source") or "").lower()
    if src == "practice":
        return "沙盒（source=practice）"
    if src == "ours" or str(m.get("origin") or "") == "mod-generated":
        return "插件/我们造的（source=%s）" % (src or "ours")
    if src and src != "game":
        return "来源不明（source=%s）" % src
    return ""


def empty_stub(level, cn, scene, why):
    """原生内容为空时写一份说明性空档（不是数据，是记录）。"""
    return {
        "format": "ucf-navgraph",
        "version": 1,
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "plugin": "navdata.py freeze",
        "map": {
            "name": "%s_%s" % (level, scene or ""),
            "label": cn, "level": level, "scene": scene,
            "source": "native", "origin": "native-empty",
            "node_count": 0, "edge_count": 0, "fingerprint": "",
            "native_only": True,
            "note": "UCF 原版这张图没有原生导航数据：%s；"
                    "游戏里能跑的点是插件 auto_waypoints 运行时铺的（不落盘，不算原生）。" % why,
        },
        "counts": {"nodes": 0, "edges": 0, "features": 0},
        "nodes": [], "edges": [], "features": [],
        "lines": {"nano_neighbor": [], "entrance_escape": [], "jump": []},
    }


# ---------------------------------------------------------------- ① freeze
def _rmtree_force(d):
    r"""删目录：先把只读位去掉（① 冻结副本每个文件都是只读的，rmtree 会失败）。"""
    if not os.path.isdir(d):
        return
    for base, _dirs, files in os.walk(d):
        for fn in files:
            make_writable(os.path.join(base, fn))
    shutil.rmtree(d, ignore_errors=True)


def _native_tmp():
    return os.path.join(P.MAPS, "_tmp_freezenative")


def _native_existing():
    r"""① 现在已有的文件：[(<图>/model, 路径)]（含可走面）。"""
    return list(P.native_files()) + list(P.native_navmesh_files())


def _merge_native(tmp):
    r"""把 tmp\<图>\native\ 并进 data\maps\<图>\native\，公共清单进 00_公共\。"""
    os.makedirs(os.path.join(P.MAPS, P.COMMON), exist_ok=True)
    n = 0
    for folder in sorted(os.listdir(tmp)):
        if folder == P.COMMON:
            continue
        src = os.path.join(tmp, folder, P.NATIVE_SUB)
        if not os.path.isdir(src):
            continue
        dst = P.native_dir(folder)
        _rmtree_force(dst)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copytree(src, dst)
        n += 1
    for fn in sorted(os.listdir(os.path.join(tmp, P.COMMON))):
        s = os.path.join(tmp, P.COMMON, fn)
        if os.path.isfile(s):
            shutil.copy2(s, os.path.join(P.MAPS, P.COMMON, fn))
    _rmtree_force(tmp)
    return n


def cmd_freeze(args):
    src = os.path.abspath(args.src or P.DEPLOY)
    smaps = os.path.join(src, "maps")
    snav = os.path.join(src, "nav")
    svis = os.path.join(src, "vis")
    if not os.path.isdir(smaps):
        sys.exit("源目录里没有 maps 目录：%s" % smaps)
    try:
        n_src = len([f for f in os.listdir(smaps)
                     if f.lower().endswith(".json") and f not in ("_index.json", "names.json")])
    except OSError:
        n_src = 0
    if n_src == 0 and _native_existing():
        # 2026-11-21：③ 不再存数据；源目录空着跑 freeze 会把备份版洗成空壳，先拦住
        sys.exit("源目录里一张图都没有：%s\n③ 游戏目录已不存数据，备份版没有动。" % smaps)

    if _native_existing():
        if not args.force:
            sys.exit("备份版已存在（%s\\<图>\\%s\\）\n要重建请加 --force（旧的会被删掉）"
                     % (P.MAPS, P.NATIVE_SUB))
        for _rel, path in _native_existing():
            make_writable(path)
        for name in P.folder_names():
            _rmtree_force(P.native_dir(name))

    tmp = _native_tmp()
    _rmtree_force(tmp)
    os.makedirs(os.path.join(tmp, P.COMMON), exist_ok=True)

    table = {r["level"]: r for r in load_table()}
    kept, skipped, stubs = [], [], []

    for fn in sorted(os.listdir(smaps)):
        if not fn.lower().endswith(".json") or fn in ("_index.json", "names.json"):
            continue
        srcfile = os.path.join(smaps, fn)
        if not os.path.isfile(srcfile):
            continue
        try:
            doc = read_json(srcfile)
        except Exception as exc:
            skipped.append((fn, "读不了：%s" % exc))
            continue
        m = doc.get("map") or {}
        level = str(m.get("level") or "")
        cn = str(m.get("label") or "")
        scene = str(m.get("scene") or "")
        # 文件夹名以《地图对照表》为准；表里没有这张图才退回 JSON 里的场景名
        folder = map_table.folder_name(level, scene, cn) or os.path.splitext(fn)[0]
        rel = folder + "/" + P.NATIVE_SUB + "/map.json"
        if str(m.get("origin") or "") == "native-empty":
            # 之前生成的「原生为空」空档：原样保留，别当成「来源不明」再生成一遍
            save_json(os.path.join(tmp, folder, P.NATIVE_SUB, "map.json"), doc)
            kept.append({"file": rel, "level": level, "cn": cn, "scene": scene,
                         "nodes": 0, "edges": 0, "fp": "", "source": "native-empty"})
            continue
        why = reject_reason(doc)
        if why:
            skipped.append((fn, why))
            row = table.get(level)
            if row and not any(x["level"] == level for x in stubs):
                stubs.append({"level": level, "cn": row["cn"], "scene": row["scene"],
                              "no": row["no"], "why": "原生 0 个路点、没有 NavMeshGraph（%s）" % why})
            continue
        doc.pop("edits", None)
        save_json(os.path.join(tmp, folder, P.NATIVE_SUB, "map.json"), doc)
        kept.append({"file": rel, "level": level, "cn": cn, "scene": scene,
                     "nodes": len(doc.get("nodes") or []),
                     "edges": len(doc.get("edges") or []),
                     "fp": str(m.get("fingerprint") or ""),
                     "source": str(m.get("source") or "")})

    for s in stubs:
        folder = map_table.folder_name(s["level"], s["scene"], s["cn"])
        rel = folder + "/" + P.NATIVE_SUB + "/map.json"
        save_json(os.path.join(tmp, folder, P.NATIVE_SUB, "map.json"),
                  empty_stub(s["level"], s["cn"], s["scene"], s["why"]))
        kept.append({"file": rel, "level": s["level"], "cn": s["cn"], "scene": s["scene"],
                     "nodes": 0, "edges": 0, "fp": "", "source": "native-empty"})

    edits = []
    if os.path.isdir(snav):
        for fn in sorted(os.listdir(snav)):
            if not fn.lower().endswith(".txt"):
                continue
            head = ""
            try:
                with open(os.path.join(snav, fn), "r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        s = line.strip()
                        if s and not s.startswith("#"):
                            head = s
                            break
            except OSError:
                pass
            edits.append((fn, head))

    # 可走面：③\vis（旧位置）、④\vis、当前版本自带的 vis 都收，同名只看第一份。
    # 2026-11-18 起导出落在 ④，③\vis 只留迁移前的旧文件。
    # 可走面：文件名是 navmesh_nm<原生顶点数>-<指纹>.bin，按顶点数认是哪张图，
    # 收进 <图>\navmesh.bin（和点图放一个文件夹）。
    bins, bin_origin, bin_skipped = [], {}, []
    verts_level = {v: k for k, v in P.NATIVE_VERTS.items()}
    vis_roots = [svis, P.VIS, P.DATAVIS]
    seen_roots = []
    for root in vis_roots:
        if not os.path.isdir(root):
            continue
        key = os.path.abspath(root).lower()
        if key in seen_roots:
            continue
        seen_roots.append(key)
        for base, dirs, fns in os.walk(root):
            dirs[:] = [d for d in dirs if d not in ("_state", "_noise")]
            for fn in sorted(fns):
                if not (fn.lower().endswith(".bin") and fn.startswith("navmesh")):
                    continue
                mnm = re.search(r"nm(\d+)-", fn)
                level = verts_level.get(int(mnm.group(1))) if mnm else ""
                if not level:
                    bin_skipped.append(fn)
                    continue
                rel = map_table.folder_name(level) + "/" + P.NATIVE_SUB + "/navmesh.bin"
                if rel in bins:
                    continue
                dstp = os.path.join(tmp, rel.replace("/", os.sep))
                os.makedirs(os.path.dirname(dstp), exist_ok=True)
                shutil.copy2(os.path.join(base, fn), dstp)
                bins.append(rel)
                bin_origin[rel] = fn

    names = {}
    for r in load_table():
        names[r["level"]] = {"name": r["cn"], "level": r["level"]}
        if r["scene"]:
            names[r["scene"]] = {"name": r["cn"], "level": r["level"]}
    for k in kept:
        if k["fp"]:
            names[k["fp"]] = {"name": k["cn"] or table.get(k["level"], {}).get("cn", ""),
                              "level": k["level"]}
    save_json(os.path.join(tmp, P.COMMON, "names.json"), names)

    sums = []
    for rel in walk_files(tmp):
        sums.append("%s  %s" % (sha256(os.path.join(tmp, rel.replace("/", os.sep))), rel))
    with open(os.path.join(tmp, P.COMMON, "SHA256SUMS.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(sums) + "\n")

    frozen = {
        "kind": "ucf-navdata-native",
        "frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "source": src,
        "rule": "只收 map.source == game 的导出；我们造的（ours/practice）一律不收，只在空档文件里记录原因",
        "maps": kept,
        "navmesh_bins": bins,
        "navmesh_origin": bin_origin,
        "skipped": [{"file": f, "why": w} for f, w in skipped],
        "edits_dropped": [{"file": f, "firstLine": h} for f, h in edits],
        "manifest_sha256": hashlib.sha256("\n".join(sums).encode("utf-8")).hexdigest(),
    }
    save_json(os.path.join(tmp, P.COMMON, ".frozen.json"), frozen)
    with open(os.path.join(tmp, P.COMMON, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(native_readme(frozen, sums))
    for rel in walk_files(tmp):
        make_readonly(os.path.join(tmp, rel.replace("/", os.sep)))
    _merge_native(tmp)

    print("① 备份版已生成（每张图自己的 native\\）：%s" % P.MAPS)
    for k in kept:
        print("   收  %-34s %-8s %-6s %3d 点 / %3d 边  %s" % (
            k["file"], k["level"], k["cn"], k["nodes"], k["edges"], k["fp"] or "-"))
    for f, w in skipped:
        print("   丢  %-22s %s" % (f, w))
    for f, h in edits:
        print("   丢  nav/%-24s 编辑清单（第一个操作：%s）" % (f, h or "-"))
    for b in bins:
        print("   收  %-34s 可走面" % b)
    for b in bin_skipped:
        print("   丢  %-34s 可走面（认不出是哪张图）" % b)
    print("   共 %d 个文件，只读；清单 SHA256=%s" % (len(sums), frozen["manifest_sha256"][:16]))
    return cmd_verify(args)


def native_readme(frozen, sums):
    fence = chr(96) * 3
    L = []
    L.append("# ① 备份版 · UCF 原生导航数据（只读，永不编辑）")
    L.append("")
    L.append("冻结时间：%s　来源：`%s`" % (frozen["frozen_at"], frozen["source"]))
    L.append("")
    L.append("> 这里只能**只读**：文件带只读属性，`core/navdata.py` 只往里读、从不往里写。")
    L.append("> 想编辑请改 **② 开发版** `navdata/dev/`；改坏了跑 `python core/navdata.py restore` 一键还原。")
    L.append("")
    L.append("## 收进来的（原生）")
    L.append("")
    L.append("一张图一个文件夹（`<序号>_<场景><中文名>\\`），里面是 `map.json` + `navmesh.bin`；")
    L.append("不属于任何一张图的（对照表 / 清单 / 说明）都放在 `00_公共\\`。")
    L.append("")
    L.append("| 文件夹 | 点图 | 关卡 | 中文名 | 节点 | 边 | 指纹 |")
    L.append("| --- | --- | --- | --- | --- | --- | --- |")
    for k in frozen["maps"]:
        folder, _sep, fn = str(k["file"]).partition("/")
        L.append("| %s | %s | %s | %s | %d | %d | %s |" % (
            folder, fn or "—", k["level"], k["cn"], k["nodes"], k["edges"], k["fp"] or "—"))
    L.append("")
    if frozen["navmesh_bins"]:
        L.append("可走面（NavMeshGraph 导出，游戏自己烘焙的网格）：%d 张图 ——" % len(frozen["navmesh_bins"]))
        L.append("")
        origin = frozen.get("navmesh_origin") or {}
        for b in frozen["navmesh_bins"]:
            L.append("- `%s`　原文件 `%s`" % (b, origin.get(b, "—")))
        L.append("")
    if frozen["skipped"]:
        L.append("## 丢掉的（不是原生）")
        L.append("")
        L.append("| 文件 | 原因 |")
        L.append("| --- | --- |")
        for s in frozen["skipped"]:
            L.append("| %s | %s |" % (s["file"], s["why"]))
        L.append("")
    if frozen["edits_dropped"]:
        L.append("## 丢掉的编辑清单（nav 目录里的 .txt）")
        L.append("")
        L.append("| 文件 | 第一个操作 |")
        L.append("| --- | --- |")
        for e in frozen["edits_dropped"]:
            L.append("| %s | `%s` |" % (e["file"], e["firstLine"] or "—"))
        L.append("")
    L.append("## 怎么用")
    L.append("")
    L.append(fence)
    L.append("cd tools")
    L.append("python navdata.py status      # 三区在哪、多少文件")
    L.append("python navdata.py verify      # 校验这一版没被动过")
    L.append("python navdata.py restore     # 开发版 <- 这里（还原）")
    L.append(fence)
    L.append("")
    L.append("清单：`SHA256SUMS.txt`（%d 个文件），机器可读信息：`.frozen.json`。" % len(sums))
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- ② verify
def _native_rel_map():
    r"""{清单里的相对路径: 绝对路径} —— <图>/native/<文件>（SHA256SUMS 就是按这个写的）。"""
    out = {}
    for name in P.folder_names():
        d = P.native_dir(name)
        if not os.path.isdir(d):
            continue
        for fn in sorted(os.listdir(d)):
            p = os.path.join(d, fn)
            if os.path.isfile(p):
                out["%s/%s/%s" % (name, P.NATIVE_SUB, fn)] = p
    return out


def cmd_verify(args):
    sums = os.path.join(P.manifest_dir(P.NATIVE), "SHA256SUMS.txt")
    if not os.path.isfile(sums):
        print("!! 没有 %s（备份版还没生成？跑 freeze）" % sums)
        return 1
    want = {}
    with open(sums, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            h, rel = line.split("  ", 1)
            want[rel] = h
    files = _native_rel_map()
    have = set(files)
    bad, missing = [], sorted(set(want) - have)
    for rel in sorted(have & set(want)):
        if sha256(files[rel]) != want[rel]:
            bad.append(rel)
    extra = sorted(have - set(want))
    ok = not (bad or missing or extra)
    print("%s备份版校验：%s（%d 个文件）" % ("OK " if ok else "!! ", "通过" if ok else "不一致", len(want)))
    for rel in bad:
        print("   被改过：%s" % rel)
    for rel in missing:
        print("   丢了：  %s" % rel)
    for rel in extra:
        print("   多出来：%s" % rel)
    if ok:
        ro = all(not (os.stat(files[r]).st_mode & stat.S_IWRITE) for r in have)
        print("   只读属性：%s" % ("是" if ro else "否（跑 make_readonly）"))
    return 0 if ok else 1


def rebuild_index(root):
    r"""给 00_公共\_index.json + INDEX.md 重新生成一份（编辑器排序列要用）。"""
    table = load_table()
    rows = []
    by_level = {}
    for rel, path in P.map_files(root):
        try:
            doc = read_json(path)
        except Exception:
            continue
        m = doc.get("map") or {}
        by_level[str(m.get("level") or "")] = {
            "file": rel, "fingerprint": str(m.get("fingerprint") or ""),
            "nodes": len(doc.get("nodes") or []), "edges": len(doc.get("edges") or []),
            "features": len(doc.get("features") or []),
            "exported": str(doc.get("generated") or ""),
            "source": str(m.get("source") or ""), "origin": str(m.get("origin") or ""),
        }
    # 旧台账里有整理时才写得出来的字段（原始导出名 / 套着几条编辑 / 可疑样本），重建时保留
    prev_doc = {}
    try:
        with open(P.index_path(root), "r", encoding="utf-8") as f:
            prev_doc = json.load(f) or {}
    except (OSError, ValueError):
        prev_doc = {}
    prev_rows = {str(r.get("level") or ""): r for r in (prev_doc.get("maps") or [])}
    for r in table:
        info = by_level.get(r["level"]) or {}
        prev = prev_rows.get(r["level"]) or {}
        row = {
            "no": r["no"], "level": r["level"], "name": r["cn"], "scene": r["scene"], "note": r["note"],
            "file": info.get("file", ""), "fingerprint": info.get("fingerprint", ""),
            "nodes": info.get("nodes", 0), "edges": info.get("edges", 0),
            "features": info.get("features", 0), "exported": info.get("exported", ""),
            "source": info.get("source", ""), "origin": info.get("origin", ""),
            "status": "有数据" if info.get("file") else "待采集",
        }
        for k in ("source_file", "edits_on_top", "suspect"):
            if k in prev:
                row[k] = prev[k]
        rows.append(row)
    doc = {"format": "ucf-map-index", "version": 1,
           "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
           "ucf": P.DATA,
           "note": "这份索引由 core/navdata.py 按 docs/地图对照表.md 生成；节点/边是当前这一版里的原生数据。",
           "maps": rows, "extras": prev_doc.get("extras") or []}
    out_dir = P.index_dir(root)
    os.makedirs(out_dir, exist_ok=True)
    save_json(os.path.join(out_dir, "_index.json"), doc)
    md = ["# 当前版本的地图数据（自动生成，勿手改）", "",
          "生成时间：" + doc["generated"], "",
          "| 序号 | 关卡 | 中文名 | 场景名 | 节点 | 边 | 文件 | 状态 |",
          "| --- | --- | --- | --- | --- | --- | --- | --- |"]
    for it in rows:
        md.append("| %s | %s | **%s** | %s | %s | %s | %s | %s |" % (
            it["no"], it["level"], it["name"], it["scene"] or "-",
            it["nodes"] or "-", it["edges"] or "-", it["file"] or "-", it["status"]))
    md += ["", "数据来源：UCF 原版（插件进图 Scan 导出）。我们手工加的点和编辑都不在这一版里。", ""]
    with open(os.path.join(out_dir, "INDEX.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(md))


def cmd_restore(args):
    r"""② 开发数据 <- ① 冻结副本：把 <图>\native\ 里的 map.json / navmesh.bin 抄回 <图>\ 根下。

    草稿（<指纹>.txt）/ markers.txt / manifest.json 都不动 —— 那些不是"原生数据"。
    """
    native = _native_rel_map()
    if not native:
        sys.exit("备份版是空的（每张图的 %s\\ 里没有文件）\n先跑 python navdata.py freeze" % P.NATIVE_SUB)
    want = {}
    for rel, srcp in sorted(native.items()):
        parts = rel.split("/")            # <图>/native/<文件>
        if len(parts) < 3:
            continue
        want[parts[0] + "/" + "/".join(parts[2:])] = srcp
    copied = 0
    for rel, srcp in sorted(want.items()):
        dst = os.path.join(P.MAPS, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst):
            make_writable(dst)
        shutil.copy2(srcp, dst)
        make_writable(dst)
        copied += 1
    # 开发版里多出来的点图 / 可走面（我们加的）删掉；草稿 / 标记 / 成品 / 收件箱 一律不碰。
    deleted = 0
    for rel, path in sorted(list(P.map_files(P.MAPS)) + list(P.navmesh_files(P.MAPS))):
        if rel in want:
            continue
        try:
            make_writable(path)
            os.remove(path)
            deleted += 1
        except OSError:
            pass
    rebuild_index(P.MAPS)
    print("② 开发数据已还原成原生：%s" % P.MAPS)
    print("   写回 %d 个文件（点图 + 可走面），删掉 %d 个（我们加的）" % (copied, deleted))
    return 0


def _run_tool(script, extra, dry):
    """跑 tools/ 下的一个子脚本（P.tool 解析绝对路径），把输出原样转出来；返回退出码。"""
    script = P.tool(os.path.basename(script))
    if not os.path.isfile(script):
        sys.exit("找不到 %s" % os.path.basename(script))
    cmd = [sys.executable, "-u", script] + list(extra) + (["--dry"] if dry else [])
    rel = os.path.relpath(script, P.PROJ).replace("\\", "/")
    print("> python %s%s%s" % (rel,
                               (" " + " ".join(extra)) if extra else "",
                               " --dry" if dry else ""))
    r = subprocess.run(cmd, cwd=os.path.dirname(script), capture_output=True)
    for blob in (r.stdout, r.stderr):
        text = (blob or b"").decode("utf-8", "replace").rstrip()
        if text:
            print(text)
    return r.returncode


def cmd_import(args):
    """整理开发版的导出收件箱：vis 归位（tidy_vis）+ 原始导出改写成 maps（organize_maps）。

    2026-11-21 四区改三区：收件箱和开发版已经是同一个目录（②\vis），
    不再有「从 ④ 拷到 ②」这一步，只剩「整理」两件事。--dry 只看会做什么。
    """
    rc = _run_tool("tidy_vis.py", (), args.dry)
    if rc != 0:
        return rc
    print("")
    rc = _run_tool("organize_maps.py", ("--archive",), args.dry)
    if rc != 0:
        return rc
    print("")
    print("② 开发版的图：%s" % P.DATA)
    print("   处理过的原始导出归档到：%s" % P.ARCHIVE)
    print("下一步：整理好的就是成品（dev\\<图>\\map.json、navmesh.bin）；"
          "测试包里的改动用 pack promote 发进成品")
    return 0



def cmd_diff(args):
    def snap(sub=""):
        out = {}
        for rel, path in list(P.map_files(P.MAPS, sub)) + list(P.navmesh_files(P.MAPS, sub)):
            try:
                out[rel] = sha256(path)
            except OSError:
                pass
        if not sub:                       # 草稿只在开发版里有意义
            for _fp, path in P.route_files(P.MAPS):
                try:
                    out[os.path.relpath(path, P.MAPS).replace(os.sep, "/")] = sha256(path)
                except OSError:
                    pass
        return out

    # 一图一夹：只比「开发数据」vs「① 冻结副本」，另报成品里有哪些图。
    a, b = snap(), snap(P.NATIVE_SUB)
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))
    diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
    print("== ② 开发版 vs ① 备份版")
    print("   只在开发版：%d" % len(only_a))
    for k in only_a[:20]:
        print("      + %s" % k)
    print("   只在备份版：%d" % len(only_b))
    for k in only_b[:20]:
        print("      - %s" % k)
    print("   内容不同：%d" % len(diff))
    for k in diff[:20]:
        print("      ~ %s" % k)
    print("")
    meta = final_store_meta()
    print("== 成品：%d 张图（每图一份，没有版本）" % len(meta))
    for fp, m in sorted(meta.items(), key=lambda kv: (str(kv[1].get("level") or ""), kv[0])):
        print("   %-22s %-8s %4d/%-4d 发布 %s" % (
            fp, m.get("level", "?"), m.get("node", 0), m.get("edge", 0),
            (m.get("published") or m.get("mtime") or "-")[:16]))
    if not meta:
        print("    （成品为空；编辑中做完用 pack promote 发布，成品 = 每张图一份）")
    return 0


def cmd_status(args):
    print("UCF 导航数据 · 三区")
    print("")
    infos = [
        ("① 备份版（每张图的 native\\，只读）", P.MAPS, P.NATIVE_SUB, "只读，永不编辑；restore 从这里抄回"),
        ("② 开发数据（每张图的根目录）", P.MAPS, "", "map.json / navmesh.bin / 草稿 / markers.txt 都在这"),
        ("③ 游戏目录（运行时·不放数据）", P.game_dir_of(), "", 
         "只放加载器 + 本体补丁；插件 / 配置 / 日志 / 标记在工程端"),
    ]
    for title, root, sub, tip in infos:
        s = summary(root, sub)
        print("%s  %s" % (title, s["path"]))
        print("    %s  数据 %d 个（图 %d / 可走面 %d / 路线 %d）  %s  最近改动 %s" % (
            "存在" if s["exists"] else "不存在", s["files"],
            s["sub"].get("图", 0), s["sub"].get("可走面", 0), s["sub"].get("路线", 0),
            human(s["bytes"]), s["mtime"]))
        print("    %s" % tip)
        print("")
    n_files, t_last = _walk_count(P.VIS)
    n_json = _walk_count(P.VIS, lambda f: f.lower().endswith(".json"))[0]
    n_bin = _walk_count(P.VIS, lambda f: f.startswith("navmesh") and f.lower().endswith(".bin"))[0]
    packs = pack_ids()      # 有草稿的地图文件夹（一张图一个）
    print("② 开发版的草稿区（导出 + 草稿）  %s" % P.VIS)
    print("    %s  导出 %d 个文件（raw %d / 可走面 %d）  草稿 %d 个（%s）  最近改动 %s" % (
        "存在" if os.path.isdir(P.EXPORT) else "不存在", n_files, n_json, n_bin,
        len(packs), "、".join(packs) if packs else "无",
        time.strftime("%Y-%m-%d %H:%M", time.localtime(t_last)) if t_last else "-"))
    print("    草稿：%s" % P.PACKS_DIR)
    meta = final_store_meta()
    print("    成品：%d 张图（每张图 <图>\\final\\<指纹>.txt）  %s" % (len(meta), P.MAPS))
    for fp, m in sorted(meta.items(), key=lambda kv: (str(kv[1].get("level") or ""), kv[0]))[-5:]:
        print("      %s %-8s %4d/%-4d 发布 %s" % (
            fp, m.get("level", "?"), m.get("node", 0), m.get("edge", 0),
            (m.get("published") or m.get("mtime") or "-")[:16]))
    print("    导出先落这里；「整理导出」把它归进 <图>\\导出\\ + <图>\\map.json；"
          "编辑中做完用 pack promote 发布（覆盖同图那一份）")
    print("")
    print("当前生效（UCF_PROFILE=%s）：%s" % (P.PROFILE, P.DATA))
    fz = os.path.join(P.manifest_dir(P.NATIVE), ".frozen.json")
    if os.path.isfile(fz):
        try:
            fr = read_json(fz)
            print("备份版冻结于 %s，%d 张图 / %d 个可走面" % (
                fr.get("frozen_at"), len(fr.get("maps") or []), len(fr.get("navmesh_bins") or [])))
        except Exception:
            pass
    return 0


# ---------------------------------------------------------------- ④ 测试包
# 测试包 = 一份「只对某一张图生效」的路线改动：
#   <游戏目录>\packs\<地图文件夹>\<包名>\<指纹>.txt
# 地图文件夹 = 地图英文场景名（TransportShip / Nano_DawnVillage …），按图归类。
# 插件靠环境变量 UCF_PACK（地图文件夹/包名）+ UCF_FP（只对哪张图套用）工作，
# 正式版 <游戏目录>\nav\ 一个字节都不动。两段都只允许 ASCII（插件是 C，用 ANSI 的
# CreateDirectoryA / fopen，中文路径没验证过）。
PACK_NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,48}$")


def packs_root():
    return P.PACKS_DIR


# 删草稿不真删：整份目录挪进 archive\pack_trash\（和发布前快照 final_prev\ 一个思路），
# 界面上不出现，误删能从那儿挪回来。UCF_PACK_TRASH 只给自检指临时目录用。
PACK_TRASH = (os.environ.get("UCF_PACK_TRASH", "").strip()
              or os.path.join(P.ARCHIVE, "pack_trash"))


def _is_pack(path):
    if os.path.isfile(os.path.join(path, "manifest.json")):
        return True
    try:
        return any(re.match(r"^n\d+-[0-9a-fA-F]{16}\.txt$", fn) for fn in os.listdir(path))
    except OSError:
        return False


def pack_ids():
    r"""packs\ 下有草稿的地图文件夹（一张图一个草稿）。

    2026-11-24 起不再有「包名」这一层：packs\<地图文件夹>\ 里直接放
    manifest.json + <指纹>.txt + nogen.txt，所以这里只返回目录名。
    兼容旧的 packs\<图>\<包>\：如果发现这种布局，也返回「图/包」。
    """
    root = packs_root()
    out = []
    try:
        entries = sorted(os.listdir(root))
    except OSError:
        return out
    for entry in entries:
        d = os.path.join(root, entry)
        if entry.startswith("_") or not os.path.isdir(d):
            continue
        if _is_pack(d):
            out.append(entry)
            continue
        try:
            subs = sorted(os.listdir(d))
        except OSError:
            continue
        for sub in subs:
            if os.path.isdir(os.path.join(d, sub)) and _is_pack(os.path.join(d, sub)):
                out.append("%s/%s" % (entry, sub))
    return out


def maps_index():
    """level -> {level, label, fp}；指纹只认 maps/*.json（游戏自己扫出来的）。"""
    out = {}
    for root in (P.DEPLOY, P.DATA):
        for _rel, path in P.map_files(root):
            try:
                m = (read_json(path) or {}).get("map") or {}
            except (OSError, ValueError):
                continue
            lv = str(m.get("level") or "")
            if not lv or lv in out:
                continue
            fp = str(m.get("fingerprint") or "")
            if not fp and lv == "level9":
                fp = "n0-0000000000000000"      # 暴风：原生 0 点，运行时就是这个指纹
            cn, _sc = map_table.row_of(lv)   # 中文名以《地图对照表》为准（暴风 JSON 里是旧名）
            out[lv] = {"level": lv, "label": cn or str(m.get("label") or m.get("scene") or lv),
                       "fp": fp, "scene": str(m.get("scene") or "")}
    return out


def edit_counts(path):
    """(node 行数, edge 行数)；文件不存在 = (0, 0)。"""
    node = edge = 0
    if not os.path.isfile(path):
        return (0, 0)
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            s = line.strip()
            if s.startswith("node "):
                node += 1
            elif s.startswith("edge "):
                edge += 1
    return (node, edge)


def write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def find_pack(name):
    r"""按地图文件夹名（或旧写法「图/包」）找草稿目录。

    2026-11-24 起一张图只有一个草稿，所以 name 就是 packs\ 下的一级目录名；
    只给中文名/关卡名时先在 pack_ids 里按尾名匹配一次，匹配不到就报错。
    """
    root = packs_root()
    name = str(name or "").replace("\\", "/").strip("/")
    pdir = os.path.join(root, *[s for s in name.split("/") if s]) if name else ""
    if not pdir or not os.path.isdir(pdir):
        tail = name.split("/")[-1]
        hits = [x for x in pack_ids() if x == tail or x.endswith("/" + tail)]
        if len(hits) > 1:
            sys.exit("有多个同名草稿，请写全「地图文件夹/包名」：%s" % ", ".join(hits))
        if hits:
            pdir = os.path.join(root, *hits[0].split("/"))
    if not pdir or not os.path.isdir(pdir):
        sys.exit("这张图还没有草稿：%r。先看 python navdata.py pack list" % name)
    man = {}
    try:
        man = read_json(os.path.join(pdir, "manifest.json")) or {}
    except (OSError, ValueError):
        pass
    fp = str(man.get("fp") or "")
    if not fp:
        txts = [f for f in os.listdir(pdir) if f.endswith(".txt")]
        fp = txts[0][:-4] if len(txts) == 1 else ""
    if not fp:
        sys.exit("草稿里没有指纹（manifest.json 缺 fp，目录里也没有唯一的 <指纹>.txt）：%s" % pdir)
    return pdir, man, fp


def cmd_pack_list(args):
    root = packs_root()
    print("草稿目录（一张图一个）：%s" % root)
    names = pack_ids()
    if not names:
        print("（还没有草稿）")
        print("新建：python navdata.py pack new --level 11 --grow")
        return 0
    print("")
    print("| 地图文件夹 | 名称（含创建日期） | 地图 | 指纹 | 改动 | 创建 |")
    print("| --- | --- | --- | --- | --- | --- |")
    for n in names:
        pdir = os.path.join(root, *n.split("/"))
        try:
            man = read_json(os.path.join(pdir, "manifest.json")) or {}
        except (OSError, ValueError):
            man = {}
        fp = str(man.get("fp") or "")
        if not fp:
            txts = [f for f in os.listdir(pdir) if f.endswith(".txt")]
            fp = txts[0][:-4] if txts else ""
        nd, ed = edit_counts(os.path.join(pdir, fp + ".txt")) if fp else (0, 0)
        print("| %s | %s | %s %s | %s | node %d / edge %d%s | %s |" % (
            n, man.get("name", "-"), man.get("level", "?"), man.get("label", ""), fp or "-", nd, ed,
            (" · keep（原版+新增）" if man.get("keep") else
             (" · grow（空白地图）" if (man.get("grow") or man.get("blank")) else "")),
            man.get("created", "-")))
    print("")
    print("用法：控制台「人机路点」页 → 启动档「编辑中」→ 选地图 → 开始游戏；")
    print("      做完点「发布这张图到成品」，成品里同图那份会被覆盖（旧成品自动留 1 份快照）。")
    return 0


def cmd_pack_new(args):
    r"""给一张图建唯一草稿：packs\<地图文件夹>\。

    默认从成品复制（接着上次改）；--grow 空白地图，--keep 原版基础 + 新增。
    已经存在就报错，重做必须加 --force（会覆盖这张图的草稿，成品不动）。
    """
    idx = maps_index()
    want = args.level if args.level.startswith("level") else "level" + str(args.level).strip("lL ")
    info = idx.get(want)
    if not info:
        extra = ""
        if want in ("level4", "level11"):
            extra = "\n  （%s 只有可走面、没有路点图 —— 点图改动对它不生效，草稿没有意义）" % want
        sys.exit("maps/*.json 里没有 %s 的路点数据。可用：%s%s" % (
            want, ", ".join("%s(%s)" % (k, v["label"]) for k, v in sorted(idx.items())), extra))
    fp = info["fp"]
    if not fp:
        sys.exit("%s 没有指纹（这张图没有路点图，草稿对它没有意义）" % args.level)
    folder = map_table.folder_name(info["level"], info.get("scene") or "", info.get("label") or "")
    pdir = os.path.join(packs_root(), folder)
    if os.path.isdir(pdir) and _is_pack(pdir) and not getattr(args, "force", False):
        sys.exit("这张图已经有草稿：%s\n要重做请加 --force（只覆盖草稿，成品不受影响）" % pdir)
    os.makedirs(pdir, exist_ok=True)
    dst = os.path.join(pdir, fp + ".txt")
    grow = bool(getattr(args, "grow", False))
    keep = bool(getattr(args, "keep", False))
    if grow and keep:
        sys.exit("--grow 和 --keep 只能选一个")
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    source = ""
    if keep:
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write("# ucf-navedit v1 fp=%s\nkeep\n" % fp)
        source = "keep"
        print("  keep：原生点一个都不动（原版路线照常走），新点按 PointGraph.AddNode 新建")
    elif grow:
        with open(dst, "w", encoding="utf-8", newline="\n") as f:
            f.write("# ucf-navedit v1 fp=%s\ngrow\n" % fp)
        source = "grow"
        print("  grow：原生点全部禁用，新点按 AddNode 新建（数量不受原生点数限制）")
    else:
        src = final_store_map(fp)
        if os.path.isfile(src):
            shutil.copyfile(src, dst)
            source = "copy-final"
            nd, ed = edit_counts(dst)
            print("从成品复制：node %d / edge %d（接着上次改）" % (nd, ed))
        else:
            with open(dst, "w", encoding="utf-8", newline="\n") as f:
                f.write("# ucf-navedit v1 fp=%s\n" % fp)
            source = "empty"
            print("成品里还没有这张图：已建一份空清单")
    with open(os.path.join(pdir, "nogen.txt"), "w", encoding="utf-8") as f:
        f.write("")
    man = {
        "name": "%s_%s" % (info.get("scene") or info["level"], time.strftime("%Y%m%d")),
        "folder": folder,
        "level": info["level"],
        "label": info["label"],
        "fp": fp,
        "scene": info.get("scene", ""),
        "created": now,
        "updated": now,
        "source": source,
        "grow": bool(grow or (source == "copy-final" and pack_flags(dst)[0])),
        "keep": bool(keep or (source == "copy-final" and pack_flags(dst)[1])),
        "note": ("grow 草稿：原生点全禁用 + 新点按 AddNode 新建" if grow else
                 "keep 草稿：原生点一个都不动 + 新点按 AddNode 新建" if keep else
                 "草稿：只对 %s(%s) 生效" % (info["label"], info["level"])),
    }
    write_json(os.path.join(pdir, "manifest.json"), man)
    print("")
    print("已建草稿：%s" % pdir)
    print("  名称 %s   地图 %s(%s)   指纹 %s" % (man["name"], info["label"], info["level"], fp))
    print("下一步：控制台 → 人机路点 → 编辑中 → 地图（%s）→ 开始游戏" % info["label"])
    return 0


def cmd_pack_diff(args):
    pdir, man, fp = find_pack(args.name)
    pfile = os.path.join(pdir, fp + ".txt")
    ffile = final_store_map(fp)
    print("草稿 %s（%s %s）  指纹 %s" % (args.name, man.get("level", "?"), man.get("label", ""), fp))
    print("")
    rows = [("编辑中 packs\\%s" % args.name, pfile),
            ("成品 final\\%s.txt" % fp, ffile)]
    print("| 位置 | 文件 | node / edge | 大小 | sha256 |")
    print("| --- | --- | --- | --- | --- |")
    for title, f in rows:
        if not os.path.isfile(f):
            print("| %s | %s | - | 不存在 | - |" % (title, fp + ".txt"))
            continue
        nd, ed = edit_counts(f)
        print("| %s | %s | %d / %d | %s | %s |" % (
            title, fp + ".txt", nd, ed, human(os.path.getsize(f)), sha256(f)[:12]))
    same = (os.path.isfile(pfile) and os.path.isfile(ffile)
            and sha256(pfile) == sha256(ffile))
    print("")
    print("结论：%s" % ("一致（草稿已发布，字节相同）" if same else "不一致（成品不是这份草稿，或发布后又改过）"))
    return 0


def cmd_pack_promote(args):
    r"""草稿 -> 成品：覆盖 final\<指纹>.txt，覆盖前旧成品自动留一份快照（最近 5 份）。

    成品档「按包启动」（UCF_PACK_DIR=dev、UCF_PACK=final），和编辑中同一套加载逻辑，
    所以 grow / keep / 普通增量发过去效果一模一样。
    """
    pdir, man, fp = find_pack(args.name)
    src = os.path.join(pdir, fp + ".txt")
    if not os.path.isfile(src):
        sys.exit("草稿里没有 %s（先在里面写改动）" % (fp + ".txt"))
    if getattr(args, "into", "") or getattr(args, "as_name", ""):
        print("  提示：--into / --as 已废弃（成品不再有版本），本次忽略。")
    if args.dry:
        print("  [dry] 会覆盖成品 %s" % final_store_map(fp))
        print("  [dry] 不写盘")
        return 0
    fp, dst, nd, ed, sha = final_store_publish(args.name, (getattr(args, "note", "") or "").strip())
    print("草稿 %s -> 成品 %s" % (args.name, dst))
    print("  node %d / edge %d   地图 %s %s" % (nd, ed, man.get("level", "?"), man.get("label", "")))
    print("  本图 sha %s   成品共 %d 张图" % (sha[:12], final_store_stats()["n"]))
    print("  控制台点「开始游戏 · 成品」立即生效，不用再部署。")
    return 0


# ---------------------------------------------------------------- 成品版本命令
def cmd_final_list(args):
    stats = final_store_stats()
    meta = stats["maps"]
    print("成品（每张图一份，在各图 final\\ 里）  %s" % P.MAPS)
    if not meta:
        print("  （空的 = 启动成品时所有图走原生。去「编辑中」发布一张图就有了）")
        return 0
    print("")
    print("| 指纹 | 地图 | 点 / 边 | 发布于 | sha256 |")
    print("| --- | --- | --- | --- | --- |")
    for fp, m in sorted(meta.items(), key=lambda kv: (str(kv[1].get("level") or ""), kv[0])):
        print("| %s | %s %s | %d / %d | %s | %s |" % (
            fp, m.get("level", "?"), m.get("label", ""), m.get("node", 0), m.get("edge", 0),
            (m.get("published") or m.get("mtime") or "-")[:16], (m.get("sha256") or "")[:12]))
    print("")
    print("启动成品 = 这些图一起加载；没发布的图走原生。发布用 python navdata.py pack promote <地图文件夹>")
    return 0


def cmd_final_use(args):
    final_set_current(args.name)
    print("当前成品版本 = %s（控制台「开始游戏 · 成品」启动它）" % args.name)
    return 0


def cmd_final_rename(args):
    new = (args.new or "").strip()
    err = final_check_name(new)
    if err:
        sys.exit(err)
    idx = final_index_read()
    hit = None
    for v in idx.get("versions") or []:
        if v.get("name") == args.name:
            hit = v
            break
    if not hit:
        sys.exit("没有这个成品版本：%s" % args.name)
    olddir, newdir = final_version_path(args.name), final_version_path(new)
    if not os.path.isdir(olddir):
        sys.exit("版本目录不见了：%s" % olddir)
    os.rename(olddir, newdir)
    hit["name"] = new
    hit["updated"] = time.strftime("%Y-%m-%d %H:%M:%S")
    if idx.get("current") == args.name:
        idx["current"] = new
    final_index_write(idx)
    print("已改名：%s -> %s" % (args.name, new))
    return 0


def final_delete_dir(d):
    r"""物理删掉一个版本目录：先去掉只读属性（Windows 下只读文件删不掉），再 rmtree。"""
    if not d or not os.path.isdir(d):
        return False
    for root, _dirs, files in os.walk(d):
        for fn in files:
            try:
                make_writable(os.path.join(root, fn))
            except OSError:
                pass
    shutil.rmtree(d)
    return True


def pack_store_remove(name, hard=False):
    r"""删掉一张图的草稿（packs\<地图文件夹>\ 整份目录）。

    默认不真删：整份挪到 archive\pack_trash\<文件夹>__<时间>\，返回
    (原目录, 挪到哪, node 数, edge 数)；hard=True 才物理删除（返回的「挪到哪」为空）。
    成品 final\ 一个字节都不碰 —— 要撤发布用 final rm。
    """
    pdir, _man, fp = find_pack(name)
    nd, ed = edit_counts(os.path.join(pdir, fp + ".txt"))
    if hard:
        final_delete_dir(pdir)
        return pdir, "", nd, ed
    os.makedirs(PACK_TRASH, exist_ok=True)
    base = os.path.basename(os.path.normpath(pdir))
    dst = os.path.join(PACK_TRASH, "%s__%s" % (base, time.strftime("%Y%m%d_%H%M%S")))
    n = 2
    while os.path.exists(dst):           # 同一秒删两张：加 -2 / -3，别互相覆盖
        dst = os.path.join(PACK_TRASH, "%s__%s-%d" % (base, time.strftime("%Y%m%d_%H%M%S"), n))
        n += 1
    try:
        shutil.move(pdir, dst)
    except OSError:
        shutil.copytree(pdir, dst)       # 跨盘 / 占用：复制成功再删原目录
        final_delete_dir(pdir)
    return pdir, dst, nd, ed


def cmd_pack_rm(args):
    r"""删除一张图的草稿：默认整份挪到 archive\pack_trash\，--hard 才真删。

    删完这张图回到「还没有草稿」；成品（已发布的 final\<指纹>.txt）不受影响。
    """
    name = str(args.name or "").strip()
    pdir, where, nd, ed = pack_store_remove(name, hard=bool(getattr(args, "hard", False)))
    print("已删除草稿：%s" % pdir)
    print("  node %d / edge %d（这张图现在「还没有草稿」）" % (nd, ed))
    if where:
        print("  目录已移到：%s" % where)
        print("  误删找回：把那个目录整个挪回 packs\\ 下（同名即可），状态就回来了。")
    else:
        print("  --hard：目录已物理删除，不保留（重做点控制台「开始编辑这张图」）。")
    print("  成品不受影响：已发布的 final\\<指纹>.txt 还在，要撤发布用 final rm。")
    return 0


def cmd_final_rm(args):
    r"""撤销一张图的发布：真删 final\<指纹>.txt（不归档，发布前快照仍在 archive\final_prev\）。

    name 可以是指纹，也可以是地图文件夹（01_TransportShip运输船）。
    """
    name = str(args.name or "").strip()
    fp = name if final_store_has(name) else ""
    if not fp:
        try:
            _pdir, _man, fp = find_pack(name)
        except SystemExit:
            fp = ""
    if not fp or not final_store_has(fp):
        sys.exit("成品里没有这张图：%s（先看 python navdata.py final list）" % name)
    d = final_store_map(fp)
    try:
        final_store_remove(fp)
    except OSError as exc:
        sys.exit("删不掉 %s：%s（游戏正开着读它？关掉游戏再删）" % (d, exc))
    print("已撤销发布：%s（%s）" % (fp, d))
    print("启动成品时这张图会走原生；草稿不受影响。")
    return 0


def cmd_pack_compare(args):
    pdir, man, fp = find_pack(args.name)
    src = os.path.join(pdir, fp + ".txt")
    fmeta = final_store_meta().get(fp) or {}
    pmeta = {"sha256": "", "node": 0, "edge": 0, "mtime": "-"}
    if os.path.isfile(src):
        nd, ed = edit_counts(src)
        pmeta = {"sha256": sha256(src), "node": nd, "edge": ed,
                 "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(src)))}
    print("草稿 %s（%s）  vs  成品 %s" % (args.name, man.get("label", ""), fp))
    print("")
    print("| 位置 | 时间 | 点 / 边 | sha256 |")
    print("| --- | --- | --- | --- |")
    print("| 编辑中 | %s | %d / %d | %s |" % (pmeta["mtime"], pmeta["node"], pmeta["edge"],
                                             (pmeta["sha256"] or "-")[:12]))
    if fmeta:
        print("| 成品 | %s | %d / %d | %s |" % (fmeta.get("published") or fmeta.get("mtime", "-"),
                                                  fmeta.get("node", 0), fmeta.get("edge", 0),
                                                  (fmeta.get("sha256") or "-")[:12]))
    else:
        print("| 成品 | - | - | 这张图还没发布 |")
    same = bool(pmeta["sha256"]) and pmeta["sha256"] == fmeta.get("sha256")
    print("")
    print("结论：%s" % ("一致（数据同一个文件，玩起来一样）" if same else "不一致（成品不是这份草稿发的，或发布后又改过）"))
    return 0


def main():
    _setup_console()
    print("")
    print("=== %s  navdata.py %s  (UCF_PROFILE=%s) ===" % (
        time.strftime("%Y-%m-%d %H:%M:%S"), " ".join(sys.argv[1:]) or "status", P.PROFILE))
    ap = argparse.ArgumentParser(description="导航数据三区管理（备份 / 开发 / 部署）")
    sub = ap.add_subparsers(dest="cmd")
    try:
        final_store_ensure()         # 建好 final\ + nogen.txt，清掉旧版 _current.txt
    except OSError:
        pass

    q = sub.add_parser("freeze", help="用当前数据重建「备份版」（只收原生）")
    q.add_argument("--from", dest="src", help="源目录（默认 ③ 游戏目录；已清空，一般显式指定）")
    q.add_argument("--force", action="store_true", help="已存在也重建")
    q.set_defaults(func=cmd_freeze)

    q = sub.add_parser("verify", help="校验备份版没被动过")
    q.set_defaults(func=cmd_verify)

    q = sub.add_parser("restore", help="开发版 <- 备份版（丢掉开发版改动）")
    q.set_defaults(func=cmd_restore)

    q = sub.add_parser("import", help="整理开发版：vis 归位 + 原始导出 -> maps")
    q.add_argument("--dry", action="store_true")
    q.set_defaults(func=cmd_import)


    q = sub.add_parser("diff", help="开发版 vs 备份版 + 成品里有几张图")
    q.set_defaults(func=cmd_diff)

    q = sub.add_parser("status", help="三区状态")
    q.set_defaults(func=cmd_status)

    q = sub.add_parser("final", help="成品：列表 / 撤销某张图的发布")
    q.set_defaults(func=cmd_final_list)
    fs_ = q.add_subparsers(dest="final_cmd")
    f2 = fs_.add_parser("list", help="列出成品里每张图那一份")
    f2.set_defaults(func=cmd_final_list)
    f2 = fs_.add_parser("rm", help="撤销一张图的发布（真删 final\\<指纹>.txt）")
    f2.add_argument("name", help="指纹或地图文件夹")
    f2.add_argument("--keep", action="store_true", help="已废弃，忽略")
    f2.set_defaults(func=cmd_final_rm)

    q = sub.add_parser("pack", help="草稿：一张图一个（② navdata\\dev\\packs/）")
    q.set_defaults(func=cmd_pack_list)
    ps = q.add_subparsers(dest="pack_cmd")
    q2 = ps.add_parser("list", help="列出草稿")
    q2.set_defaults(func=cmd_pack_list)
    q2 = ps.add_parser("new", help="新建草稿（默认从成品复制；一张图一个）")
    q2.add_argument("name", nargs="?", default="", help="已废弃：现在按 --level 定位，一张图一个草稿")
    q2.add_argument("--level", required=True, help="levelN 或纯数字，例：--level 11")
    q2.add_argument("--from", dest="src", choices=["dev", "deploy"], default="dev",
                    help="已废弃，忽略")
    q2.add_argument("--grow", action="store_true",
                    help="空白地图：原生点全禁用 + 新点按 AddNode 新建（数量不受原生点数限制）")
    q2.add_argument("--keep", action="store_true",
                    help="原版基础 + 新增：原生点一个都不动，只把新点按 AddNode 建上去")
    q2.add_argument("--force", action="store_true", help="这张图已有草稿也重建（覆盖草稿，成品不动）")
    q2.set_defaults(func=cmd_pack_new)
    q2 = ps.add_parser("diff", help="草稿 vs 成品（同一张图）")
    q2.add_argument("name")
    q2.set_defaults(func=cmd_pack_diff)
    q2 = ps.add_parser("promote", help="草稿 -> 成品（覆盖同图那一份，旧成品留快照）")
    q2.add_argument("name")
    q2.add_argument("--into", metavar="版本", default="", help="已废弃，忽略")
    q2.add_argument("--note", default="", help="记进发布日志（可选）")
    q2.add_argument("--as", dest="as_name", metavar="版本名", default="", help="已废弃，忽略")
    q2.add_argument("--dry", action="store_true")
    q2.set_defaults(func=cmd_pack_promote)
    q2 = ps.add_parser("rm", help="删除草稿（整份挪到 archive\\pack_trash\\，成品不动）")
    q2.add_argument("name", help="地图文件夹，例：10_Nano30_Storm飓风危城")
    q2.add_argument("--hard", action="store_true", help="真删，不进 archive（不可恢复）")
    q2.set_defaults(func=cmd_pack_rm)
    q2 = ps.add_parser("compare", help="草稿 vs 成品（同一张图）")
    q2.add_argument("name")
    q2.add_argument("--final", default="", help="已废弃，忽略")
    q2.set_defaults(func=cmd_pack_compare)

    args = ap.parse_args()
    if not getattr(args, "func", None):
        ap.print_help()
        return cmd_status(args)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
