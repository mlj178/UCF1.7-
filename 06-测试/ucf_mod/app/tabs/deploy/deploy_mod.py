#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""UCF 一键部署 —— 只把"游戏目录必须有的文件"从工程端铺过去。

2026-11-25 改版（配合"工作区唯一事实源"）：
    * 插件本体 / ucf_mod.json / 日志 / 标记 / 地图数据 全部留在工程端，
      游戏目录不再生成 ucf_mod\；
    * 游戏目录必须有的只有两类：
        1) 加载器：winhttp.dll + winhttp_orig.dll（游戏只会从自己目录加载 DLL）
        2) 游戏本体补丁：run\gamepatch\<包>\patch.json 里登记的文件
    * 部署清单、覆盖前备份、卸载还原都放工程端 run\runtime\deploy / run\deploy_backup，
      游戏目录不落 manifest / backup；
    * patch.json 的 orig_file（包内原版副本）用于"现场没有备份"时还原。

用法：
    python deploy_mod.py --pick
    python deploy_mod.py --game-exe "D:/games/UnityCrossFire.exe"
    python deploy_mod.py --game-dir "D:/games" --dry-run
    python deploy_mod.py --game-exe ... --repair
    python deploy_mod.py --game-exe ... --verify
    python deploy_mod.py --game-exe ... --uninstall
    python deploy_mod.py --game-exe ... --all-packs     # 连未启用的地图补丁一起铺

退出码：
    0 成功 / 2 前置检查或状态不允许（一个文件都没写）/ 3 执行中途失败
"""

import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE
while not (PROJ / ".ucfroot").is_file() and PROJ.parent != PROJ:
    PROJ = PROJ.parent                      # 项目根：靠 .ucfroot 标记

_CORE = PROJ / "app" / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))
import gamepatch as GP  # noqa: E402

PAYLOAD = PROJ / "run" / "payload"
LOADER_HISTORY = PAYLOAD / "loader_history.json"
GAMEPATCH = PROJ / "run" / "gamepatch"
RUNTIME = PROJ / "run" / "runtime"
MANIFEST_DIR = RUNTIME / "deploy"
BACKUP_ROOT = PROJ / "run" / "deploy_backup"
RUNTIME_CFG = RUNTIME / "ucf_mod.json"

GAME_EXE_NAME = "unitycrossfire.exe"
GAME_DATA_DIR = "UnityCrossFire_Data"
GAME_DATA_MARKER = "globalgamemanagers"
GAMEASM_MD5 = "fab04426db6a014c0129ef2001530908"
MIN_FREE_MB = 50
PROTECTED_MARKERS = ("/program files/", "/program files (x86)/", "/windows/", "/system32/")

SYS_WINHTTP = Path(os.environ.get("WINDIR", r"C:\Windows")) / "SysWOW64" / "winhttp.dll"

OK, WARN, BAD = "[OK]", "[!!]", "[X]"

try:                                   # 让中文在 cp65001 控制台里也能打出来
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


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


def md5_file(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def human(num):
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024 or unit == "GB":
            return f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= 1024.0
    return str(num)


def game_id(game):
    """一份游戏目录的稳定短 id：清单 / 备份按它分目录。"""
    raw = str(Path(game).resolve()).lower().encode("utf-8", "replace")
    return hashlib.sha1(raw).hexdigest()[:12]


def display_rel(path):
    return str(path).replace(os.sep, "/")


def say(prefix, text):
    print(f"  {prefix} {text}")


def runtime_cfg():
    try:
        with open(RUNTIME_CFG, "r", encoding="utf-8-sig") as f:
            return json.load(f) or {}
    except (OSError, ValueError):
        return {}


def pack_enabled(pack, cfg):
    """patch.json 的 switch -> ucf_mod.json features；没配置就用 patch.json 的 default_enabled。"""
    sw = str(pack.get("switch") or "").strip()
    feats = (cfg or {}).get("features") or {}
    if sw and sw in feats:
        return bool(feats.get(sw))
    return bool(pack.get("default_enabled", False))


def loader_history():
    r"""当前 payload 加载器 + run\payload\loader_history.json 里的历史版本（都可安全覆盖）。"""
    out = set()
    try:
        with open(LOADER_HISTORY, "r", encoding="utf-8-sig") as f:
            for h in (json.load(f) or {}).get("sha256") or []:
                h = str(h).strip().lower()
                if h:
                    out.add(h)
    except (OSError, ValueError):
        pass
    p = PAYLOAD / "winhttp.dll"
    if p.is_file():
        out.add(sha256_file(p))
    return out


def orig_src_of(item):
    r"""清单里的 orig_file（相对工程根）-> 绝对路径；没有就 None。"""
    rel = str(item.get("orig_file") or "").strip()
    if not rel:
        return None
    p = Path(rel)
    return p if p.is_absolute() else (PROJ / p)


# ------------------------------------------------------------------ 计划
def _item(kind, src, game, rel, role, origin, *, sha256=None, bytes_=None,
          orig_sha256=None, orig_file=None, pack=None, enabled=True, allow_missing=True,
          replaceable_sha256=None):
    src = Path(src)
    if sha256 is None:
        if not src.is_file():
            raise FileNotFoundError(f"部署源缺文件：{src}")
        sha256 = sha256_file(src)
    if bytes_ is None:
        bytes_ = src.stat().st_size if src.is_file() else 0
    return {
        "kind": kind,
        "src": src,
        "dst": Path(game) / rel,
        "rel": rel,
        "role": role,
        "origin": origin,
        "sha256": str(sha256).lower(),
        "bytes": int(bytes_),
        "orig_sha256": (str(orig_sha256).lower() if orig_sha256 else None),
        "orig_file": (str(orig_file) if orig_file else ""),
        "pack": pack or "",
        "enabled": bool(enabled),
        "allow_missing": bool(allow_missing),
        "replaceable_sha256": [str(h).lower() for h in (replaceable_sha256 or [])],
    }


def build_plan(game, include_disabled=False):
    """返回游戏目录必须有的文件：加载器 + 游戏本体补丁。"""
    game = Path(game)
    cfg = runtime_cfg()
    steps = []

    # 1) 加载器（唯一必须留在游戏目录的入口）
    loader = PAYLOAD / "winhttp.dll"
    if not loader.is_file():
        raise FileNotFoundError(f"payload 缺加载器：{loader}")
    if not SYS_WINHTTP.is_file():
        raise FileNotFoundError(f"系统 winhttp 不存在：{SYS_WINHTTP}")
    steps.append(_item(
        "loader", loader, game, "winhttp.dll", "代理加载器", "payload",
        orig_sha256=None, allow_missing=True,
        replaceable_sha256=sorted(loader_history())))
    steps.append(_item(
        "loader", SYS_WINHTTP, game, "winhttp_orig.dll", "系统 winhttp 副本（转发目标）", "system",
        orig_sha256=None, allow_missing=True))

    # 2) 游戏本体补丁（run\gamepatch\<包>\patch.json）
    for pack in GP.load_packs(GAMEPATCH):
        pack_id = pack.get("id") or Path(pack["_dir"]).name
        enabled = include_disabled or pack_enabled(pack, cfg)
        for entry in pack.get("files") or []:
            src = GP.check_source(pack, entry)       # 源缺失 / 哈希不对 -> 抛异常
            orig = GP.orig_of(entry)
            orig_sha = str(orig.get("sha256") or "").lower() or None
            orig_path = GP.orig_source_of(pack, entry)
            orig_rel = ""
            if orig_path:
                if not orig_path.is_file():
                    raise FileNotFoundError(f"补丁包缺原版副本：{orig_path}")
                if orig_sha and sha256_file(orig_path) != orig_sha:
                    raise ValueError(f"补丁包原版副本哈希不对：{orig_path}")
                try:
                    orig_rel = display_rel(orig_path.relative_to(PROJ))
                except ValueError:
                    orig_rel = str(orig_path)
            steps.append(_item(
                "gamepatch", src, game, GP.rel_of(entry).replace(os.sep, "/"),
                str(entry.get("role") or pack.get("label") or pack_id),
                "gamepatch",
                sha256=entry.get("sha256"), bytes_=entry.get("bytes", src.stat().st_size),
                orig_sha256=orig_sha, orig_file=orig_rel, pack=pack_id,
                enabled=enabled, allow_missing=(orig_sha is None)))
    return steps


def classify_item(game, item):
    r"""一致 / 原版 / 新增 / 缺失 / 已禁用 / 冲突。"""
    if not item.get("enabled", True):
        return "已禁用"
    dst = Path(game) / item["rel"]
    if not dst.is_file():
        if item.get("allow_missing") or not item.get("orig_sha256"):
            return "新增"
        return "缺失"
    got = sha256_file(dst)
    if got == item["sha256"]:
        return "一致"
    if item.get("orig_sha256") and got == item["orig_sha256"]:
        return "原版"
    if got in (item.get("replaceable_sha256") or []):
        return "原版"
    return "冲突"


def plan_states(game, steps=None):
    steps = steps if steps is not None else build_plan(game)
    return [(s, classify_item(game, s)) for s in steps]


def plan_summary(game, steps=None):
    rows = plan_states(game, steps)
    out = {"total": len(rows), "ok": 0, "ready": 0, "missing": 0,
           "conflict": 0, "disabled": 0}
    for _s, st in rows:
        if st == "一致":
            out["ok"] += 1
        elif st in ("原版", "新增"):
            out["ready"] += 1
        elif st == "缺失":
            out["missing"] += 1
        elif st == "已禁用":
            out["disabled"] += 1
        else:
            out["conflict"] += 1
    return out


def all_current(game, steps=None):
    """游戏目录是否已经具备全部"必须有的文件"（禁用的包不算缺）。"""
    try:
        rows = plan_states(game, steps)
    except Exception:
        return False
    return all(st in ("一致", "已禁用") for _s, st in rows)


def print_plan(game, steps):
    game = Path(game)
    print(f"\n部署目标：{game}")
    print(f"备份目录：{BACKUP_ROOT / game_id(game)}")
    print(f"部署清单：{MANIFEST_DIR / (game_id(game) + '.json')}")
    print()
    print(f"  {'状态':<6}{'目标文件':<40}{'作用':<28}来源")
    for s, st in plan_states(game, steps):
        print(f"  {st:<6}{display_rel(s['rel']):<40}{s['role'][:26]:<28}{s['origin']}")
    print()
    print("  说明：插件本体/配置/日志/标记/地图数据都在工程端，不写 ucf_mod\\。")


# ------------------------------------------------------------------ 闸门
def game_running():
    """游戏进程是否在跑。优先 psutil，没有就退回 tasklist（重定向到文件，不用管道）。"""
    try:
        import psutil
        for proc in psutil.process_iter(["name"]):
            if (proc.info.get("name") or "").lower() == GAME_EXE_NAME:
                return True
        return False
    except Exception:
        pass
    try:
        import subprocess
        import tempfile
        out = Path(tempfile.gettempdir()) / f"ucf_tasklist_{os.getpid()}.txt"
        with open(out, "w", encoding="utf-8", errors="replace") as fh:
            subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {GAME_EXE_NAME}", "/NH"],
                           stdout=fh, stderr=subprocess.DEVNULL, timeout=20)
        text = out.read_text(encoding="utf-8", errors="replace").lower()
        out.unlink(missing_ok=True)
        return GAME_EXE_NAME in text
    except Exception:
        return False


def writable(path):
    probe = Path(path) / f".ucf_write_probe_{os.getpid()}"
    try:
        probe.write_text("x", encoding="utf-8")
        probe.unlink()
        return True
    except OSError:
        return False


def check_gates(game, allow_cjk=False, force=False):
    """返回 (ok, 闸门结果列表)。ok=False 时调用方必须中止且不写盘。"""
    game = Path(game)
    rows = []

    def add(ok, title, detail=""):
        rows.append((bool(ok), title, detail))
        return ok

    exe = game / "UnityCrossFire.exe"
    add(exe.is_file(), "游戏主程序存在", str(exe))

    data = game / GAME_DATA_DIR
    add((data / GAME_DATA_MARKER).is_file(), "游戏数据目录完整", str(data / GAME_DATA_MARKER))

    asm = game / "GameAssembly.dll"
    if asm.is_file():
        got = md5_file(asm)
        add(got == GAMEASM_MD5, "游戏版本匹配（GameAssembly.dll）",
            f"MD5 {got}" if got == GAMEASM_MD5 else f"MD5 {got}，期望 {GAMEASM_MD5}（只支持 UnityCrossFire 1.7.1）")
    else:
        add(False, "游戏版本匹配（GameAssembly.dll）", "文件不存在")

    running = game_running() if exe.is_file() else False
    add(not running, "游戏未在运行", "请先完全退出 UnityCrossFire.exe" if running else "")

    low = str(game).replace("\\", "/").lower()
    protected = any(m in low + "/" for m in PROTECTED_MARKERS)
    add(not protected, "不在受保护目录", "Program Files / Windows 下部署会被 UAC 拦" if protected else "")

    add(writable(game) if game.is_dir() else False, "游戏目录可写", "" if game.is_dir() else "目录不存在")

    cjk = any(ord(ch) > 127 for ch in str(game))
    add(not cjk or allow_cjk, "路径不含中文",
        "中文路径在插件侧（C + ANSI）有风险；确认要装请加 --allow-cjk" if (cjk and not allow_cjk) else ("已用 --allow-cjk 放行" if cjk else ""))

    try:
        free_mb = shutil.disk_usage(game).free // (1024 * 1024)
        add(free_mb >= MIN_FREE_MB, "磁盘空间充足", f"剩余 {free_mb} MB")
    except Exception:
        add(True, "磁盘空间充足", "无法读取，跳过")

    add(SYS_WINHTTP.is_file(), "系统 winhttp 可用（生成 winhttp_orig.dll）", str(SYS_WINHTTP))
    add((PAYLOAD / "winhttp.dll").is_file(), "payload 加载器存在", str(PAYLOAD / "winhttp.dll"))

    # 第三方 winhttp 冲突：只允许"当前 payload"或 loader_history.json 里的历史 UCF 加载器
    existing = game / "winhttp.dll"
    third_party = ""
    if existing.is_file():
        known = loader_history()
        got = sha256_file(existing)
        if got not in known:
            third_party = f"已是别人的 winhttp.dll（SHA256 {got[:8]}…，可能是 BepInEx），继续会覆盖"
    add(not third_party or force, "无第三方 winhttp.dll 冲突",
        third_party + ("；已用 --force 放行" if force and third_party else ""))

    # 启用中的补丁包：源文件必须齐全且哈希对
    try:
        cfg = runtime_cfg()
        for pack in GP.load_packs(GAMEPATCH):
            if not pack_enabled(pack, cfg):
                continue
            for entry in pack.get("files") or []:
                GP.check_source(pack, entry)
        add(True, "游戏本体补丁包完整", "run/gamepatch")
    except Exception as exc:
        add(False, "游戏本体补丁包完整", str(exc)[:160])

    return all(r[0] for r in rows), rows


# ------------------------------------------------------------------ 备份 / 清单
def backup_path(backup_root, rel):
    return Path(backup_root) / Path(rel)


def write_manifest(game, steps, backup_root):
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    target = MANIFEST_DIR / (game_id(game) + ".json")
    data = {
        "schema": 2,
        "tool": "deploy_mod.py",
        "deployed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "game_dir": str(Path(game)),
        "game_id": game_id(game),
        "backup_dir": display_rel(backup_root) if Path(backup_root).is_dir() else "",
        "items": [
            {
                "rel": s["rel"],
                "kind": s["kind"],
                "pack": s.get("pack", ""),
                "role": s["role"],
                "sha256": s["sha256"],
                "bytes": s["bytes"],
                "orig_sha256": s.get("orig_sha256"),
                "orig_file": s.get("orig_file", ""),
                "backup": display_rel(backup_path(backup_root, s["rel"]).relative_to(Path(backup_root)))
                if (Path(backup_root) / s["rel"]).is_file() else "",
            }
            for s in steps
        ],
    }
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, target)
    return target


def load_manifest(game):
    p = MANIFEST_DIR / (game_id(game) + ".json")
    if not p.is_file():
        return None, p
    try:
        return json.loads(p.read_text(encoding="utf-8")), p
    except (OSError, ValueError):
        return None, p


# ------------------------------------------------------------------ 部署
def run_deploy(game, steps=None, dry_run=False, repair=False, quiet=False, force=False):
    game = Path(game)
    steps = steps if steps is not None else build_plan(game)
    rows = []
    for s in steps:
        st = classify_item(game, s)
        # --force 只对加载器生效：允许覆盖第三方 winhttp.dll；本体补丁永远不盲打
        if force and s["rel"] == "winhttp.dll" and st == "冲突":
            st = "原版"
        rows.append((s, st))

    bad = [(s, st) for s, st in rows if st in ("冲突", "缺失")]
    if bad:
        print()
        for s, st in bad:
            say(BAD, f"{st}：{display_rel(s['rel'])}  {s['role']}")
        print("\n状态不对 —— 已中止，没有写入任何文件。")
        print("  冲突 = 目标既不是原版、也不是我们的补丁；缺失 = 原版文件不在了。")
        return 2

    todo = [(s, st) for s, st in rows
            if st in ("原版", "新增") or (repair and st == "一致")]
    skipped = [(s, st) for s, st in rows if st in ("一致", "已禁用") and (s, st) not in todo]

    print()
    if dry_run:
        print(f"（干跑）将要写入 {len(todo)} 个文件，跳过 {len(skipped)} 个：")
        for s, st in todo:
            act = "新增" if st == "新增" else "覆盖"
            print(f"  {act}  {display_rel(s['rel'])}  ← {display_rel(str(s['src']))}")
        if todo:
            print(f"  备份目录：{BACKUP_ROOT / game_id(game)}")
        return 0

    if not todo:
        print(f"  {OK} 游戏目录已经具备全部必须文件（{len(skipped)} 个一致/禁用），无需改动")
        return 0

    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup_root = BACKUP_ROOT / game_id(game) / stamp
    done = []
    try:
        for s, st in todo:
            dst = s["dst"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.is_file():
                bpath = backup_path(backup_root, s["rel"])
                bpath.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, bpath)
                say(OK, f"备份 {display_rel(s['rel'])} → {display_rel(bpath)}")
            shutil.copy2(s["src"], dst)
            got = sha256_file(dst)
            if got != s["sha256"]:
                raise IOError(f"写入后校验失败：{dst}\n  期望 {s['sha256']}\n  实际 {got}")
            done.append((s, st))
            say(OK, f"写入 {display_rel(s['rel'])}  sha256={got[:12]}…")
    except Exception as exc:
        print(f"\n{BAD} 部署失败：{exc}")
        for s, _st in reversed(done):
            dst = s["dst"]
            bpath = backup_path(backup_root, s["rel"])
            try:
                if bpath.is_file():
                    shutil.copy2(bpath, dst)
                elif dst.is_file():
                    dst.unlink()
            except OSError:
                pass
        print("  已回滚本次写入的文件。备份保留：" + str(backup_root))
        return 3

    target = write_manifest(game, [s for s, st in rows if st != "已禁用"], backup_root)
    say(OK, f"部署清单 → {display_rel(str(target))}")
    for s, st in skipped:
        if st == "已禁用":
            say("--", f"跳过 {display_rel(s['rel'])}（{s.get('pack') or ''} 未启用）")
        else:
            say("--", f"跳过 {display_rel(s['rel'])}（已一致）")
    print(f"\n完成：写入 {len(done)} 个，跳过 {len(skipped)} 个。")
    print("  游戏目录只放加载器/本体补丁；插件、配置、日志、标记、地图数据都在工程端。")
    return 0


# ------------------------------------------------------------------ 校验 / 卸载
def run_verify(game):
    game = Path(game)
    print(f"\n校验目标：{game}")
    try:
        steps = build_plan(game)
    except Exception as exc:
        print(f"  {BAD} {exc}")
        return 2
    rows = plan_states(game, steps)
    print()
    print(f"  {'状态':<6}{'目标文件':<40}{'作用':<28}哈希")
    bad = 0
    for s, st in rows:
        dst = s["dst"]
        got = sha256_file(dst) if dst.is_file() else ""
        if st in ("冲突", "缺失"):
            bad += 1
        print(f"  {st:<6}{display_rel(s['rel']):<40}{s['role'][:26]:<28}{got[:12] if got else '-'}")
    summary = plan_summary(game, steps)
    print()
    print(f"  一致 {summary['ok']} / 待部署 {summary['ready']} / 缺失 {summary['missing']} / "
          f"冲突 {summary['conflict']} / 禁用 {summary['disabled']}")
    if (game / "ucf_mod").is_dir():
        print(f"  {WARN} 发现旧部署目录：{game / 'ucf_mod'}（直读模式不需要，建议清理）")
    data, mpath = load_manifest(game)
    if data:
        print(f"  部署清单：{mpath}（{data.get('deployed_at', '?')}）")
    else:
        print(f"  部署清单：{mpath}（还没有）")
    return 0 if bad == 0 and summary["ready"] == 0 else 2


def run_uninstall(game, dry_run=False):
    game = Path(game)
    data, mpath = load_manifest(game)
    if not data:
        print(f"{BAD} 没有部署清单，无法安全卸载：{mpath}")
        print("   直读模式下游戏目录只有加载器/本体补丁；没有清单就不知道哪些是覆盖前备份。")
        return 2

    print(f"\n卸载目标：{game}")
    print(f"  部署时间：{data.get('deployed_at', '?')}")
    backup_dir = Path(data["backup_dir"]) if data.get("backup_dir") else None

    removed, restored, kept = [], [], []
    for item in data.get("items") or []:
        dst = game / Path(item["rel"])
        if not dst.is_file():
            continue
        got = sha256_file(dst)
        if got != item["sha256"]:
            if item.get("orig_sha256") and got == item["orig_sha256"]:
                continue                       # 已经是原版
            kept.append(item["rel"])
            continue
        if dry_run:
            say("(干跑)", f"处理 {item['rel']}")
            continue

        bpath = (backup_dir / item["rel"]) if (backup_dir and (backup_dir / item["rel"]).is_file()) else None
        osrc = orig_src_of(item)
        if bpath and item["rel"] == "winhttp.dll" and sha256_file(bpath) in loader_history():
            # 覆盖前那份也是我们自己的旧加载器：卸载时应该回到"没有加载器"，不是还原旧版
            dst.unlink()
            say(OK, f"删除 {display_rel(item['rel'])}（旧加载器，不还原）")
            removed.append(item["rel"])
        elif bpath:
            shutil.copy2(bpath, dst)
            say(OK, f"还原 {display_rel(item['rel'])} ← 备份")
            restored.append(item["rel"])
        elif osrc and osrc.is_file():
            shutil.copy2(osrc, dst)
            say(OK, f"还原 {display_rel(item['rel'])} ← 包内原件")
            restored.append(item["rel"])
        elif not item.get("orig_sha256"):
            dst.unlink()
            say(OK, f"删除 {display_rel(item['rel'])}（新增文件）")
            removed.append(item["rel"])
        else:
            kept.append(item["rel"])
            say(WARN, f"保留 {display_rel(item['rel'])}：没有备份也没有包内原件")

    if not dry_run:
        mpath.unlink(missing_ok=True)
        print(f"\n完成：还原 {len(restored)}，删除 {len(removed)}"
              + (f"，保留 {len(kept)}" if kept else ""))
        if kept:
            for p in kept:
                print(f"  {WARN} 未处理（哈希被改过或没有原件）：{p}")
    return 0 if not kept else 1


# ------------------------------------------------------------------ 入口
def resolve_game(target):
    """把用户给的路径（exe 或目录）统一成游戏目录。"""
    p = Path(target).expanduser()
    if p.is_dir():
        candidate = p / "UnityCrossFire.exe"
        return p if candidate.is_file() or (p / GAME_DATA_DIR).is_dir() else None
    if p.is_file():
        if p.name.lower() != GAME_EXE_NAME:
            return None
        return p.parent
    return None


def pick_exe():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        path = filedialog.askopenfilename(
            title="选择 UnityCrossFire.exe",
            filetypes=[("UnityCrossFire", "UnityCrossFire.exe"), ("可执行文件", "*.exe")],
        )
        root.destroy()
        return path or ""
    except Exception as exc:
        print(f"{BAD} 打不开文件选择框：{exc}")
        return ""


def main(argv=None):
    ap = argparse.ArgumentParser(description="UCF 一键部署（只部署游戏目录必须有的文件）")
    ap.add_argument("--game-exe", help="UnityCrossFire.exe 的完整路径")
    ap.add_argument("--game-dir", help="游戏目录（另一种给法）")
    ap.add_argument("--pick", action="store_true", help="弹窗选择 UnityCrossFire.exe")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不写盘")
    ap.add_argument("--repair", action="store_true", help="哈希相同也强制重拷")
    ap.add_argument("--verify", action="store_true", help="只校验")
    ap.add_argument("--uninstall", action="store_true", help="按部署清单卸载")
    ap.add_argument("--all-packs", action="store_true", help="连未启用的地图补丁一起铺")
    ap.add_argument("--yes", action="store_true", help="不询问，直接执行")
    ap.add_argument("--allow-cjk", action="store_true", help="允许中文路径")
    ap.add_argument("--force", action="store_true", help="允许覆盖别人的 winhttp.dll")
    args = ap.parse_args(argv)

    target = args.game_exe or args.game_dir
    if args.pick or not target:
        target = pick_exe()
        if not target:
            print("已取消：没有选择游戏。")
            return 2

    game = resolve_game(target)
    if game is None:
        print(f"{BAD} 这不是一个可用的游戏位置：{target}")
        print("   请选择 UnityCrossFire.exe，或者游戏目录（里面要有 UnityCrossFire_Data）。")
        return 2

    print("=" * 68)
    print("UCF 一键部署 · 只部署游戏目录必须有的文件")
    print("=" * 68)
    print(f"游戏目录：{game}")

    ok, rows = check_gates(game, allow_cjk=args.allow_cjk, force=args.force)
    print("\n前置检查：")
    for good, title, detail in rows:
        print(f"  {OK if good else BAD} {title:<34}{detail}")
    if not ok:
        print("\n前置检查未通过 —— 已中止，没有写入任何文件。")
        return 2

    try:
        steps = build_plan(game, include_disabled=args.all_packs)
    except Exception as exc:
        print(f"\n{BAD} {exc}")
        print("   payload / gamepatch 目录不完整，请重新取一份完整包。")
        return 3

    print_plan(game, steps)

    if args.uninstall:
        return run_uninstall(game, dry_run=args.dry_run)
    if args.verify:
        return run_verify(game)
    if args.dry_run:
        return run_deploy(game, steps, dry_run=True)

    if not args.yes:
        print()
        ans = input("回车开始部署，输入 q 取消：").strip().lower()
        if ans in ("q", "quit", "n", "no"):
            print("已取消。")
            return 2

    return run_deploy(game, steps, repair=args.repair, force=args.force)


if __name__ == "__main__":
    sys.exit(main())
