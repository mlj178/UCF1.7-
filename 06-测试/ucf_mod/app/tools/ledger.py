#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""资产台账：run/gamepatch（我们负责的本体补丁）与各游戏副本的对账 —— 只读。

背景（2026-11-24）：
    以前改游戏本体（level9 / level12 / globalgamemanagers）是直接改游戏目录，工作区没有副本、
    git 里看不到，游戏目录一删就永久丢。现在所有"本体改动"都必须进 run/gamepatch\<图>\，
    patch.json 里写清"原版哈希 → 补丁后哈希"，这个工具负责回答三个问题：

      1. 我这台机器上有几份游戏？各自装了哪些补丁？（矩阵）
      2. 哪份副本里出现了 run/gamepatch 里没有的本体改动？（未纳管 = 可能会丢）
      3. 某个目录能不能直接开始玩？（verify）

用法：
    python ledger.py scan                    # 人读表格
    python ledger.py scan --json             # 机读（给控制台调）
    python ledger.py scan --write            # 同时写 run/ledger/drift.json + 快照
    python ledger.py verify --game "D:\...\UnityCrossFire1.7.1"   # 只看这份

退出码：
    0 全部对得上；1 有缺口（缺补丁 / 有未纳管的本体改动）
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJ = HERE
while not (PROJ / ".ucfroot").is_file() and PROJ.parent != PROJ:
    PROJ = PROJ.parent                      # 项目根：靠 .ucfroot，和 ucf_paths.py 同一套约定

PATCH_ROOT = PROJ / "run" / "gamepatch"
LEDGER_DIR = PROJ / "run" / "ledger"
SNAP_DIR = LEDGER_DIR / "snapshots"
GAME_DATA = "UnityCrossFire_Data"
GAME_EXE = "UnityCrossFire.exe"
# 原版 UnityCrossFire 1.7.1 的 Unity 资源文件时间戳：不是这天的 = 被动过
ORIG_STAMP = "2023-04-06"

MISSING, ORIG, PATCHED, OTHER = "缺失", "原版", "已打补丁", "被改过"
STATE_ORDER = {ORIG: 0, PATCHED: 1, OTHER: 2, MISSING: 3}


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
def load_packs():
    r"""读 run\gamepatch\*\patch.json → [{id, level, label, switch, files:[...]}]。

    只认 patch.json，不猜目录名：目录名是给人看的，patch.json 才是账。
    """
    packs = []
    if not PATCH_ROOT.is_dir():
        return packs
    for d in sorted(PATCH_ROOT.iterdir()):
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
    r"""patch.json 里的 path 用的是游戏内相对路径（UnityCrossFire_Data/level9）。"""
    return entry["path"].replace("/", os.sep)


def state_of(game_dir, entry):
    r"""单个文件在某个游戏目录里的状态：缺失 / 原版 / 已打补丁 / 被改过。"""
    p = Path(game_dir) / rel_of(entry)
    if not p.is_file():
        return MISSING
    got = sha256_file(str(p))
    if got == entry.get("sha256", ""):
        return PATCHED
    orig = (entry.get("orig") or {})
    if orig.get("sha256") and got == orig["sha256"]:
        return ORIG
    return OTHER


# ------------------------------------------------------------------ 副本
def known_copies(extra=()):
    r"""这台机器上"可能装着游戏"的位置：用户配置的历史 + 工程 tools\deploy.json + 命令行给的。

    只挑确实有 UnityCrossFire.exe 的；目录不存在也保留（标"离线"，那正是要报警的情况）。
    """
    out, seen = [], set()

    def add(path, source):
        if not path:
            return
        g = os.path.abspath(str(path))
        if g.lower() in seen:
            return
        seen.add(g.lower())
        out.append({
            "game_dir": g,
            "source": source,
            "exists": os.path.isdir(g),
            "has_exe": os.path.isfile(os.path.join(g, GAME_EXE)),
        })

    local = os.environ.get("LOCALAPPDATA") or os.path.expanduser(r"~\AppData\Local")
    cfg = load_json(os.path.join(local, "UCFMod", "deploy.json"), {}) or {}
    for item in (cfg.get("history") or []):
        g = item.get("game_dir") if isinstance(item, dict) else item
        add(g, "用户配置")
    add(cfg.get("game_dir"), "用户配置·当前")
    add(os.environ.get("UCF_DEPLOY", ""), "环境变量")
    pj = load_json(str(PROJ / "app" / "tools" / "deploy.json"), {}) or {}
    if pj.get("deploy"):
        add(os.path.dirname(pj["deploy"]), "工程 tools/deploy.json")
    for g in extra:
        add(g, "命令行")
    return out


def scan_copy(copy, packs):
    r"""一份副本 × 全部补丁包 → 每行的状态。"""
    rows = []
    for pack in packs:
        for entry in pack["files"]:
            rows.append({
                "pack": pack.get("id") or Path(pack["_dir"]).name,
                "level": pack.get("level", ""),
                "label": pack.get("label", ""),
                "switch": pack.get("switch", ""),
                "path": entry["path"],
                "bytes": entry.get("bytes", 0),
                "state": state_of(copy["game_dir"], entry),
            })
    return rows


def known_body_changes():
    r"""旧方案遗留 / 明确知道但不再分发的本体改动（_index.json 的 known_body_changes）。

    这类文件不是"未纳管"，而是"已知、且已经决定不这么做"。仍要列出来，因为：
      * 它让这份副本和原版不一样（比如顶掉了椰岛之巅）；
      * 它可能被误当成"我们的补丁"。
    """
    doc = load_json(PATCH_ROOT / "_index.json", {}) or {}
    out = {}
    for item in (doc.get("known_body_changes") or []):
        key = os.path.basename(str(item.get("path", ""))).lower()
        if key:
            out[key] = item
    return out


def unmanaged_changes(game_dir):
    r"""游戏本体里"不是原版、又不在 run\gamepatch 里"的文件 —— 这是会丢的东西。

    判据：UnityCrossFire_Data 顶层文件的 mtime 不是 2023-04-06（原版打包时间）。
    只扫顶层：这张游戏改动过的都是顶层文件（levelN / sharedassetsN / globalgamemanagers），
    子目录 il2cpp_data / Resources 原版就没动过。
    """
    data = Path(game_dir) / GAME_DATA
    known = set()
    for pack in load_packs():
        for entry in pack["files"]:
            known.add(os.path.basename(entry["path"]).lower())
    legacy = known_body_changes()
    out = []
    if not data.is_dir():
        return out
    for p in sorted(data.iterdir()):
        if not p.is_file():
            continue
        try:
            stamp = time.strftime("%Y-%m-%d", time.localtime(p.stat().st_mtime))
        except OSError:
            continue
        if stamp == ORIG_STAMP:
            continue
        key = p.name.lower()
        item = legacy.get(key)
        out.append({
            "file": p.name,
            "rel": "%s/%s" % (GAME_DATA, p.name),
            "bytes": p.stat().st_size,
            "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(p.stat().st_mtime)),
            "managed": key in known,
            "legacy": bool(item),
            "why": (item or {}).get("why", ""),
            "restore": (item or {}).get("restore", ""),
        })
    return out


# ------------------------------------------------------------------ 输出
def render(report):
    lines = []
    packs = report["packs"]
    lines.append("")
    lines.append("=" * 78)
    lines.append("UCF 资产台账 · run/gamepatch ⇄ 各游戏副本")
    lines.append("=" * 78)
    lines.append("补丁包 %d 个，文件 %d 个，合计 %s" % (
        len(packs), sum(len(p["files"]) for p in packs),
        human(sum(f.get("bytes", 0) for p in packs for f in p["files"]))))

    for copy in report["copies"]:
        tag = copy["game_dir"]
        if not copy["exists"]:
            lines.append("\n[离线] %s（目录已不存在）" % tag)
            for r in copy["rows"]:
                if r["state"] != MISSING:
                    lines.append("        %-34s %s" % (r["path"], r["state"]))
            continue
        lines.append("\n[副本] %s   ← %s" % (tag, copy["source"]))
        if copy["rows"]:
            for r in copy["rows"]:
                mark = {ORIG: "✗", PATCHED: "✓", OTHER: "!", MISSING: "-"}[r["state"]]
                lines.append("        %s %-10s %-34s %s" % (mark, r["label"] or r["level"], r["path"], r["state"]))
        um = copy["unmanaged"]
        old = [u for u in um if u["legacy"]]
        for u in old:
            lines.append("        △ 已知·旧方案遗留 %-14s  %s" % (u["file"], u["why"][:56]))
        loose = [u for u in um if not u["managed"] and not u["legacy"]]
        if loose:
            lines.append("        ⚠ 未纳管的本体改动 %d 个（不在 run/gamepatch 里，删了就没了）：" % len(loose))
            for u in loose:
                lines.append("            %-28s %10s  %s" % (u["file"], human(u["bytes"]), u["mtime"]))
        elif um:
            lines.append("        本体改动 %d 个，全部已纳管 ✓" % len(um))
        elif old:
            lines.append("        除上面这些旧方案遗留外，其余都是原版")
        else:
            lines.append("        本体改动 0 个（纯原版）")

    lines.append("\n判据：✓ 已打补丁   ✗ 原版（未装）   - 缺失   ! 被改过（不是原版也不是我们的）")
    lines.append("未纳管的处理：进 run/gamepatch 建一个包（patch.json + 原样文件），再跑一次本工具。")
    lines.append("")
    return "\n".join(lines)


def build_report(extra_copies):
    packs = load_packs()
    copies = []
    for copy in known_copies(extra_copies):
        row = dict(copy)
        if copy["exists"]:
            row["rows"] = scan_copy(copy, packs)
            row["unmanaged"] = unmanaged_changes(copy["game_dir"])
        else:
            row["rows"] = []
            row["unmanaged"] = []
        copies.append(row)
    return {
        "scanned": time.strftime("%Y-%m-%d %H:%M:%S"),
        "project": str(PROJ),
        "packs": [{"id": p.get("id"), "level": p.get("level"), "label": p.get("label"),
                   "switch": p.get("switch"), "files": p["files"]} for p in packs],
        "copies": copies,
    }


def gaps(report):
    r"""有缺口的情况：装了一半、被改过、有未纳管的本体改动。"""
    out = []
    for copy in report["copies"]:
        if not copy["exists"]:
            out.append("%s：目录不存在（离线副本）" % copy["game_dir"])
            continue
        for r in copy["rows"]:
            if r["state"] in (OTHER,):
                out.append("%s：%s 被改过（不是原版也不是我们的）" % (copy["game_dir"], r["path"]))
        for u in copy["unmanaged"]:
            if not u["managed"] and not u["legacy"]:
                out.append("%s：未纳管的本体改动 %s" % (copy["game_dir"], u["rel"]))
    return out


def write_report(report):
    LEDGER_DIR.mkdir(parents=True, exist_ok=True)
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    (LEDGER_DIR / "drift.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    stamp = time.strftime("%Y%m%d-%H%M%S")
    (SNAP_DIR / ("%s.json" % stamp)).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return LEDGER_DIR / "drift.json"


# ------------------------------------------------------------------ 入口
def main(argv=None):
    ap = argparse.ArgumentParser(description="UCF 资产台账：run/gamepatch ⇄ 游戏副本（只读）")
    sub = ap.add_subparsers(dest="cmd")

    ps = sub.add_parser("scan", help="列出副本矩阵 + 未纳管的本体改动")
    ps.add_argument("--json", action="store_true", help="输出 JSON（给控制台调）")
    ps.add_argument("--write", action="store_true", help="写 run/ledger/drift.json + 快照")
    ps.add_argument("--game", action="append", default=[], help="额外看这个游戏目录（可多次）")

    pv = sub.add_parser("verify", help="只看一份目录：补丁装齐没有")
    pv.add_argument("--game", required=True, help="游戏目录（含 UnityCrossFire.exe）")

    args = ap.parse_args(argv)
    if not args.cmd:
        ap.print_help()
        return 0

    extra = args.game if isinstance(args.game, list) else [args.game]
    report = build_report(extra)

    if args.cmd == "verify":
        target = os.path.abspath(args.game)
        mine = [c for c in report["copies"] if os.path.abspath(c["game_dir"]).lower() == target.lower()]
        if not mine:
            print("找不到这份目录：%s" % target)
            return 2
        ok = True
        for c in mine:
            print("\n%s" % c["game_dir"])
            for r in c["rows"]:
                good = r["state"] == PATCHED
                ok = ok and (good or r["state"] == MISSING)
                print("  %s %-34s %s" % ("[OK]" if good else "[--]", r["path"], r["state"]))
            for u in c["unmanaged"]:
                if not u["managed"]:
                    print("  [!!] 未纳管：%s" % u["rel"])
                    ok = False
        print("\n%s" % ("全部装齐" if ok else "有缺口"))
        return 0 if ok else 1

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render(report))

    if args.write:
        print("已写：%s" % write_report(report))

    bad = gaps(report)
    if bad and not args.json:
        print("缺口 %d 处：" % len(bad))
        for b in bad:
            print("  - %s" % b)
        print("")
    return 0 if not bad else 1


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())