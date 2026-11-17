#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自检：控制台 → 运行中插件的命令文件 + 测试包摘要。

为什么要有它：控制台现在能在游戏运行时切包（ucf_navcmd.txt），但插件只认
seq/cmd/pack/fp 四行 ASCII。这里不启动窗口、不碰游戏，只验证：
  · 包摘要读得对（blank / 加点 / 加边 / 删点 / 删边）；
  · manifest.fp 优先，文件名指纹兜底；
  · 命令文件是原子替换、seq 单调递增、没有中文/多余字段。

跑法：python tools/test_console_packcmd.py
"""
import importlib.util
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CONSOLE = os.path.join(HERE, "控制台.pyw")


def load_console():
    sys.path.insert(0, HERE)
    spec = importlib.util.spec_from_file_location("ucf_console_packcmd", CONSOLE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    m = load_console()
    with tempfile.TemporaryDirectory() as tmp:
        m.PACKS = os.path.join(tmp, "packs")
        m.NAVCMD = os.path.join(tmp, "ucf_navcmd.txt")
        m._CMD_SEQ = 0
        fp = "n786-57a46e3465c847cb"
        pdir = os.path.join(m.PACKS, "blank_a")
        os.makedirs(pdir)
        with open(os.path.join(pdir, fp + ".txt"), "w", encoding="utf-8") as f:
            f.write("# ucf-navedit v1 fp=%s\nblank\n" % fp)
            f.write("node add 1.000 2.000 3.000\n")
            f.write("node add 4.000 5.000 6.000\n")
            f.write("edge add 1.000 2.000 3.000 4.000 5.000 6.000\n")
            f.write("node del 7.000 8.000 9.000\n")
        with open(os.path.join(pdir, "manifest.json"), "w", encoding="utf-8") as f:
            f.write('{"name":"blank_a","level":"level1","label":"运输船","fp":"%s"}\n' % fp)

        assert m.pack_name_ok("blank_a")
        assert not m.pack_name_ok("空白")
        assert m.pack_target_fp("blank_a") == fp

        s = m.pack_summary("blank_a", fp)
        assert s["blank"] and s["nadd"] == 2 and s["eadd"] == 1
        assert s["ndel"] == 1 and s["edel"] == 0
        assert s["path"].endswith(fp + ".txt")

        seq1 = m.write_nav_cmd("apply", "blank_a", fp)
        seq2 = m.write_nav_cmd("reload", "blank_a", fp)
        assert seq2 > seq1, (seq1, seq2)
        with open(m.NAVCMD, "r", encoding="ascii") as f:
            lines = f.read().splitlines()
        assert lines[0] == "seq=%d" % seq2, lines
        assert lines[1] == "cmd=reload", lines
        assert lines[2] == "pack=blank_a", lines
        assert lines[3] == "fp=" + fp, lines
        assert len(lines) == 4, lines
        assert not os.path.exists(m.NAVCMD + ".tmp")

        seq3 = m.write_nav_cmd("off")
        assert seq3 > seq2
        with open(m.NAVCMD, "r", encoding="ascii") as f:
            assert f.read().splitlines() == ["seq=%d" % seq3, "cmd=off"]
    print("OK: pack summary + ucf_navcmd.txt")


if __name__ == "__main__":
    main()
