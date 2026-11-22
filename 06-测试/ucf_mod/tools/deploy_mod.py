#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""UCF mod 一键部署 —— 把 payload 里的运行件搬进游戏目录。

用法：
    python deploy_mod.py --pick                          # 弹窗选 UnityCrossFire.exe
    python deploy_mod.py --game-exe "D:/games/UnityCrossFire.exe"
    python deploy_mod.py --game-dir "D:/games"
    python deploy_mod.py --game-exe ... --dry-run        # 只打印，不写盘
    python deploy_mod.py --game-exe ... --repair         # 哈希相同也强制重拷
    python deploy_mod.py --game-exe ... --verify         # 只校验，不写盘
    python deploy_mod.py --game-exe ... --uninstall      # 按部署清单卸载

退出码：
    0 成功 / 2 前置检查未通过（一个文件都没写）/ 3 执行中途失败

设计要点：
    * 只认一个入口：用户选 UnityCrossFire.exe，游戏目录由它推出，部署点是 <游戏目录>/ucf_mod。
    * 六道闸门全过才动盘；任何一道不过就整体中止、零写入。
    * 幂等：目标文件 sha256 与 payload 一致就跳过，所以重复点 = 修复。
    * 覆盖前先备份到 ucf_mod/backup/deploy_<时间戳>/，卸载能还原。
    * 部署清单落在 ucf_mod/deploy_manifest.json，卸载只删清单里登记过、且哈希没被改过的文件。
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
PROJ = HERE.parent
PAYLOAD = PROJ / "payload"

GAME_EXE_NAME = "unitycrossfire.exe"
GAME_DATA_DIR = "UnityCrossFire_Data"
GAME_DATA_MARKER = "globalgamemanagers"
# UnityCrossFire 1.7.1 的 GameAssembly.dll；换版本必须改这里
GAMEASM_MD5 = "fab04426db6a014c0129ef2001530908"
# 我们自己那份代理外壳（payload/winhttp.dll）
OUR_LOADER_MD5 = "c5c6fe25314532c010785e481d28507b"

MOD_DIR = "ucf_mod"
MANIFEST_NAME = "deploy_manifest.json"
BACKUP_DIR_NAME = "backup"

MIN_FREE_MB = 50
PROTECTED_MARKERS = ("/program files/", "/program files (x86)/", "/windows/", "/system32/")

try:                                   # 让中文在 cp65001 控制台里也能打出来
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


# ------------------------------------------------------------------ 小工具
def human(num):
    for unit in ("B", "KB", "MB", "GB"):
        if num < 1024 or unit == "GB":
            return f"{num:.0f} {unit}" if unit == "B" else f"{num:.1f} {unit}"
        num /= 1024.0
    return str(num)


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


def say(tag, text):
    print(f"  {tag} {text}")


OK, WARN, BAD = "[OK]", "[!!]", "[X]"


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

    sys_wh = Path(os.environ.get("WINDIR", "C:/Windows")) / "SysWOW64" / "winhttp.dll"
    add(sys_wh.is_file(), "系统 winhttp 可用（用来生成 winhttp_orig.dll）", str(sys_wh))

    existing = game / "winhttp.dll"
    third_party = ""
    if existing.is_file():
        got = md5_file(existing)
        if got not in (OUR_LOADER_MD5, md5_file(sys_wh) if sys_wh.is_file() else ""):
            third_party = f"已是别人的 winhttp.dll（MD5 {got[:8]}…，可能是 BepInEx），继续会覆盖"
    add(not third_party or force, "无第三方 winhttp.dll 冲突", third_party + ("；已用 --force 放行" if force and third_party else ""))

    return all(r[0] for r in rows), rows


# ------------------------------------------------------------------ 计划
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


def display_rel(path):
    return path.replace(os.sep, "/")


def build_plan(game):
    """返回部署步骤：每步 = {src, dst, sha256, bytes, role, origin}"""
    game = Path(game)
    steps = []

    def add(src, dst, role, origin):
        if not src.is_file():
            raise FileNotFoundError(f"payload 缺文件：{src}")
        steps.append({
            "src": src,
            "dst": dst,
            "sha256": sha256_file(src),
            "bytes": src.stat().st_size,
            "role": role,
            "origin": origin,
        })

    mod = game / MOD_DIR
    add(PAYLOAD / "winhttp.dll", game / "winhttp.dll",
        "代理加载器", "payload")
    add(PAYLOAD / MOD_DIR / "ucf_mod.dll", mod / "ucf_mod.dll",
        "插件本体", "payload")
    add(PAYLOAD / MOD_DIR / "uninstall.ps1", mod / "uninstall.ps1",
        "卸载脚本", "payload")
    add(PAYLOAD / MOD_DIR / "README.txt", mod / "README.txt",
        "用户说明", "payload")

    sys_wh = Path(os.environ.get("WINDIR", "C:/Windows")) / "SysWOW64" / "winhttp.dll"
    add(sys_wh, game / "winhttp_orig.dll",
        "系统 winhttp 副本（代理转发目标）", "system")
    return steps


def print_plan(game, steps):
    print(f"\n部署目标：{game}")
    print(f"部署目录：{game / MOD_DIR}")
    print()
    print(f"  {'作用':<26}{'目标文件':<24}{'来源':<10}大小")
    for s in steps:
        print(f"  {s['role']:<26}{display_rel(str(s['dst'].relative_to(game))):<24}{s['origin']:<10}{human(s['bytes'])}")


# ------------------------------------------------------------------ 部署
def backup_path(backup_root, game, dst):
    rel = dst.relative_to(game)
    return backup_root / rel


def run_deploy(game, steps, dry_run=False, repair=False, quiet=False):
    game = Path(game)
    mod = game / MOD_DIR
    stamp = time.strftime("%Y%m%d_%H%M%S")
    backup_root = mod / BACKUP_DIR_NAME / f"deploy_{stamp}"

    todo, skipped = [], []
    for s in steps:
        dst = s["dst"]
        if dst.is_file() and not repair and sha256_file(dst) == s["sha256"]:
            skipped.append(s)
        else:
            todo.append(s)

    print()
    if dry_run:
        print(f"（干跑）将要写入 {len(todo)} 个文件，跳过 {len(skipped)} 个已一致的文件")
        for s in todo:
            act = "覆盖" if s["dst"].exists() else "新增"
            print(f"  {act}  {display_rel(str(s['dst']))}")
        if todo:
            print(f"  备份目录：{backup_root}（覆盖的文件会先存这里）")
        return 0

    if not todo:
        print(f"  {OK} 全部已是最新（{len(skipped)} 个文件哈希一致），无需改动")
        write_manifest(game, steps, backup_root, deployed=False)
        return 0

    done = []
    try:
        for s in todo:
            dst = s["dst"]
            dst.parent.mkdir(parents=True, exist_ok=True)
            if dst.is_file():
                bpath = backup_path(backup_root, game, dst)
                bpath.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(dst, bpath)
                say(OK, f"备份 {display_rel(str(dst.relative_to(game)))} → {display_rel(str(bpath.relative_to(game)))}")
            shutil.copy2(s["src"], dst)
            got = sha256_file(dst)
            if got != s["sha256"]:
                raise IOError(f"写入后校验失败：{dst} 期望 {s['sha256'][:12]}… 实际 {got[:12]}…")
            done.append(s)
            say(OK, f"写入 {display_rel(str(dst.relative_to(game)))}  sha256={got[:12]}…")

        write_manifest(game, steps, backup_root, deployed=True)
        say(OK, f"部署清单 → {display_rel(str((mod / MANIFEST_NAME).relative_to(game)))}")
        for s in skipped:
            say("--", f"跳过 {display_rel(str(s['dst'].relative_to(game)))}（已一致）")
        print(f"\n完成：写入 {len(done)} 个，跳过 {len(skipped)} 个。")
        print("下一步：用控制台「开始游戏」启动（它会带 UCF_MOD=1），直接双击 UnityCrossFire.exe 是原版。")
        return 0
    except Exception as exc:
        print(f"\n{BAD} 部署失败：{exc}")
        for s in reversed(done):
            try:
                s["dst"].unlink()
            except OSError:
                pass
        print("  已回滚本次写入的文件。备份目录保留：" + str(backup_root))
        return 3


def write_manifest(game, steps, backup_root, deployed):
    mod = game / MOD_DIR
    mod.mkdir(parents=True, exist_ok=True)
    data = {
        "schema": 1,
        "tool": "deploy_mod.py",
        "deployed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "game_dir": str(game),
        "game_exe_md5": md5_file(game / "UnityCrossFire.exe") if (game / "UnityCrossFire.exe").is_file() else "",
        "gameassembly_md5": md5_file(game / "GameAssembly.dll") if (game / "GameAssembly.dll").is_file() else "",
        "backup_dir": display_rel(str(backup_root.relative_to(game))) if backup_root.exists() else "",
        "files": [
            {
                "path": display_rel(str(s["dst"].relative_to(game))),
                "sha256": s["sha256"],
                "bytes": s["bytes"],
                "role": s["role"],
                "origin": s["origin"],
            }
            for s in steps
        ],
    }
    target = mod / MANIFEST_NAME
    tmp = target.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, target)


# ------------------------------------------------------------------ 校验 / 卸载
def run_verify(game):
    game = Path(game)
    mod = game / MOD_DIR
    manifest = mod / MANIFEST_NAME
    print(f"\n校验目标：{game}")
    if not manifest.is_file():
        print(f"  {WARN} 没有部署清单（{manifest}），改按 payload 比对")
        try:
            steps = build_plan(game)
        except FileNotFoundError as exc:
            print(f"  {BAD} {exc}")
            return 2
    else:
        data = json.loads(manifest.read_text(encoding="utf-8"))
        steps = [{"dst": game / Path(f["path"]), "sha256": f["sha256"], "role": f["role"]} for f in data["files"]]
        print(f"  部署时间：{data.get('deployed_at', '?')}")

    bad = 0
    print(f"\n  {'状态':<6}{'文件':<26}{'作用':<26}哈希")
    for s in steps:
        dst = s["dst"]
        if not dst.is_file():
            print(f"  {'缺失':<6}{display_rel(str(dst.relative_to(game))):<26}{s['role']:<26}-")
            bad += 1
            continue
        got = sha256_file(dst)
        same = got == s["sha256"]
        bad += 0 if same else 1
        print(f"  {('一致' if same else '不一致'):<6}{display_rel(str(dst.relative_to(game))):<26}{s['role']:<26}{got[:12]}…")
    print()
    print(f"  {'全部一致' if bad == 0 else f'{bad} 个文件有问题'}")
    return 0 if bad == 0 else 2


def run_uninstall(game, dry_run=False):
    game = Path(game)
    mod = game / MOD_DIR
    manifest = mod / MANIFEST_NAME
    if not manifest.is_file():
        print(f"{BAD} 没有部署清单，无法安全卸载：{manifest}")
        print("   （只能手工删 winhttp.dll / winhttp_orig.dll / ucf_mod 目录）")
        return 2

    data = json.loads(manifest.read_text(encoding="utf-8"))
    print(f"\n卸载目标：{game}")
    print(f"  部署时间：{data.get('deployed_at', '?')}")

    removed, kept = [], []
    for f in data["files"]:
        dst = game / Path(f["path"])
        if not dst.is_file():
            continue
        if sha256_file(dst) != f["sha256"]:
            kept.append(f["path"])
            continue
        removed.append(dst)
        if dry_run:
            say("(干跑) 将删除", display_rel(f["path"]))
        else:
            dst.unlink()
            say(OK, f"删除 {display_rel(f['path'])}")

    backup_dir = data.get("backup_dir", "")
    if backup_dir:
        broot = game / Path(backup_dir)
        if broot.is_dir() and not dry_run:
            for src in sorted(broot.rglob("*")):
                if not src.is_file():
                    continue
                rel = src.relative_to(broot)
                target = game / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
                say(OK, f"还原 {display_rel(str(rel))}")

    if not dry_run:
        manifest.unlink(missing_ok=True)
        # 只在完全空的时候删 ucf_mod 目录，markers/backup 有内容就留着
        try:
            if mod.is_dir() and not any(mod.iterdir()):
                mod.rmdir()
        except OSError:
            pass

    print(f"\n完成：删除 {len(removed)} 个" + (f"，保留 {len(kept)} 个（哈希被改过，未动）" if kept else ""))
    if kept:
        for p in kept:
            print(f"  {WARN} 未删除（已被改动）：{p}")
    return 0


def all_current(game, steps=None):
    """目标目录里的文件是否已经和 payload 完全一致（= 部署已完成、可直接用）。"""
    game = Path(game)
    if steps is None:
        try:
            steps = build_plan(game)
        except FileNotFoundError:
            return False
    try:
        return all(s["dst"].is_file() and sha256_file(s["dst"]) == s["sha256"] for s in steps)
    except OSError:
        return False


# ------------------------------------------------------------------ 入口
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
    ap = argparse.ArgumentParser(description="UCF mod 一键部署")
    ap.add_argument("--game-exe", help="UnityCrossFire.exe 的完整路径")
    ap.add_argument("--game-dir", help="游戏目录（另一种给法）")
    ap.add_argument("--pick", action="store_true", help="弹窗选择 UnityCrossFire.exe")
    ap.add_argument("--dry-run", action="store_true", help="只打印计划，不写盘")
    ap.add_argument("--repair", action="store_true", help="哈希相同也强制重拷")
    ap.add_argument("--verify", action="store_true", help="只校验")
    ap.add_argument("--uninstall", action="store_true", help="按部署清单卸载")
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
    print("UCF mod 一键部署")
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
        steps = build_plan(game)
    except FileNotFoundError as exc:
        print(f"\n{BAD} {exc}")
        print("   payload 目录不完整，请重新取一份完整包。")
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

    return run_deploy(game, steps, repair=args.repair)


if __name__ == "__main__":
    sys.exit(main())
