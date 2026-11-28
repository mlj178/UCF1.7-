#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：docs 里的文档被改名 / 再改号以后，代码不会静默读不到（2026-11-28）。

跑法：python app/tests/test_guide_docs.py

为什么要有这篇：guide 的 11 篇文档按创建时间加了 01–11 前缀，这些名字在代码里是
**字面量**（doc("07-地图对照表.md")）。doc() 找不到就一路退到内置兜底表，而兜底表
今天和真表内容一模一样 —— 界面上、日志里、别的测试里全看不出来。所以在这里钉死：

  1) 代码里 doc("…md") / "docs","guide","…md" 这些常量，文件必须真的在
  2) 《地图对照表》必须读到**文件**（不是 _BUILTIN 兜底），且条数和文件里对得上
  3) guide 顶层带号文档编号连续（01..N，不重号、不跳号）
  4) 带号文档里提到的 NN-xxx.md，目标文件存在（改名最容易断的就是这种链接）

只读，不碰游戏 / 网络 / 窗口。
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对

FAIL = []


def check(cond, what):
    if cond:
        print("  OK   " + what)
    else:
        print("  !!   " + what)
        FAIL.append(what)


def j(*parts):
    return os.path.join(UCF_ROOT, *parts)


def read(rel):
    with open(j(rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


# 和 ucf_paths.doc() 同一套找法：docs/ -> docs/guide/ -> docs/record/
def find_doc(name):
    for sub in ("", "guide", "record"):
        p = os.path.join(j("docs", sub, name)) if sub else j("docs", name)
        if os.path.isfile(p):
            return p
    return ""


DOC_CALL_RE = re.compile(r'\b_?doc\(\s*"([^"]+\.md)"\s*\)')
GUIDE_JOIN_RE = re.compile(r'"docs"\s*,\s*"guide"\s*,\s*"([^"]+\.md)"')
NUMBERED_RE = re.compile(r"^(\d{2})-.+\.md$")
MD_REF_RE = re.compile(r"(?<![\dA-Za-z_-])(\d{2}-[^\s/\\()\[\]<>|]+?\.md)")


def py_constants():
    """[(相对路径, 行号, 文档名)] —— 源码里按文件名打开文档的地方。"""
    out = []
    for root, dirs, files in os.walk(j("app")):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", "logs", ".git")]
        for fn in sorted(files):
            if not fn.endswith(".py"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, UCF_ROOT)
            with open(p, "r", encoding="utf-8", errors="replace") as f:
                for i, line in enumerate(f, 1):
                    for m in DOC_CALL_RE.finditer(line):
                        out.append((rel, i, m.group(1)))
                    for m in GUIDE_JOIN_RE.finditer(line):
                        out.append((rel, i, m.group(1)))
    return out


SKIP_DIRS = {"archive", "__pycache__", ".git", "node_modules", "logs", ".venv-build",
             "AssetStudio", "dist_release"}


def all_md_basenames():
    """工程里所有 .md 的文件名（跳过 archive/ 快照与历史版本）。"""
    names = set()
    roots = [os.path.join(UCF_ROOT, os.pardir, os.pardir)]     # 仓库根：guide 也往 01-游戏系统分析/ 那边指
    for base in roots:
        base = os.path.normpath(base)
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for fn in files:
                if fn.endswith(".md"):
                    names.add(fn)
    return names


def first_table_rows(text, row_re):
    """只数第一张表（map_table 读到表尾就停，后面的表不重复算）。"""
    n, started = 0, False
    for line in text.splitlines():
        if row_re.match(line):
            started, n = True, n + 1
        elif started:
            break
    return n


def main():
    print("== 1) 代码里的文档常量都指向真文件")
    consts = py_constants()
    check(len(consts) > 0, "扫到 %d 处 doc(\"*.md\") 常量" % len(consts))
    bad = ["%s:%d -> %s" % (rel, ln, name) for rel, ln, name in consts if not find_doc(name)]
    for b in bad:
        print("       " + b)
    check(not bad, "全部能按 docs/ -> docs/guide/ -> docs/record/ 找到（找不到 %d 处）" % len(bad))

    print("== 2) 《地图对照表》读的是文件，不是兜底表")
    sys.path.insert(0, j("app", "core"))
    import map_table                                   # noqa: E402
    check(map_table._doc is not None, "map_table 找到了 ucf_paths.doc（不是内置兜底模式）")
    tp = map_table.table_path()
    check(bool(tp) and os.path.isfile(tp), "表文件存在：%s" % (os.path.basename(tp) or "(空)"))
    rows = map_table.rows()
    if tp and os.path.isfile(tp):
        text = read(os.path.relpath(tp, UCF_ROOT))
        n_file = first_table_rows(text, map_table.ROW_RE)
        check(len(rows) == n_file,
              "条数一致：文件第一张表 %d 行 / rows() %d 行" % (n_file, len(rows)))
        check(len(rows) > 0, "解析出 %d 条（>0 才算读到）" % len(rows))

    print("== 3) guide 顶层文档编号连续")
    guide = j("docs", "guide")
    numbered = sorted(n for n in os.listdir(guide)
                      if n.endswith(".md") and NUMBERED_RE.match(n))
    nums = [int(NUMBERED_RE.match(n).group(1)) for n in numbered]
    check(bool(numbered), "带号文档 %d 篇" % len(numbered))
    check(nums == list(range(1, len(nums) + 1)),
          "编号从 01 连续到 %02d（实际 %s）" % (len(nums), ",".join("%02d" % n for n in nums)))
    for n in numbered:
        print("       " + n)

    print("== 4) 带号文档里的 NN-xxx.md 链接都有效")
    known = all_md_basenames()
    scanned = [j("README.md")] + [os.path.join(guide, n) for n in numbered]
    for d in ("record",):
        base = j("docs", d)
        if os.path.isdir(base):
            scanned += [os.path.join(base, f) for f in sorted(os.listdir(base)) if f.endswith(".md")]
    broken = []
    for p in scanned:
        if not os.path.isfile(p):
            continue
        rel = os.path.relpath(p, UCF_ROOT)
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f, 1):
                for m in MD_REF_RE.finditer(line):
                    if m.group(1) not in known:
                        broken.append("%s:%d -> %s" % (rel, i, m.group(1)))
    for b in broken[:20]:
        print("       " + b)
    check(not broken, "扫了 %d 个文件，断链 %d 处" % (len(scanned), len(broken)))

    if FAIL:
        print("\n!! %d 项没过" % len(FAIL))
        return 1
    print("\nOK: 文档改名后代码 / 表 / 编号 / 链接四处都对得上")
    return 0


if __name__ == "__main__":
    sys.exit(main())
