#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：一键部署只铺"游戏目录必须有的文件"，不生成 ucf_mod\。

不启动游戏、不弹窗，用临时目录伪造：
    payload/winhttp.dll + 历史加载器哈希
    系统 winhttp
    gamepatch/<包>/patch.json + 补丁后文件 + orig/
    游戏目录里的原版文件
验证：
    1) 计划 = 加载器 + 启用的本体补丁（未启用的包跳过）；
    2) 部署只写游戏目录，ucf_mod\ 不出现；覆盖前备份进工程端；
    3) 重复部署幂等；
    4) 原版哈希对不上时拒绝，零写入；
    5) 卸载能还原原版 / 删除新增文件，并清掉部署清单。
"""

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(HERE)
for _p in (os.path.join(APP, "core"), os.path.join(APP, "tabs", "deploy")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import deploy_mod as D  # noqa: E402

FAIL = []


def check(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("  [X] " + msg)
    else:
        print("  [OK] " + msg)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if isinstance(data, bytes):
        with open(path, "wb") as f:
            f.write(data)
    else:
        with open(path, "w", encoding="utf-8") as f:
            f.write(data)


def build_fixture(tmp):
    game = os.path.join(tmp, "game")
    os.makedirs(game)
    write(os.path.join(game, "UnityCrossFire.exe"), b"exe")
    write(os.path.join(game, "UnityCrossFire_Data", "globalgamemanagers"), b"ggm")
    write(os.path.join(game, "UnityCrossFire_Data", "a.bin"), b"ORIG")

    payload = os.path.join(tmp, "payload")
    write(os.path.join(payload, "winhttp.dll"), b"LOADER")
    write(os.path.join(payload, "loader_history.json"),
          json.dumps({"sha256": [sha(b"OLD_LOADER")]}))

    sysdir = os.path.join(tmp, "sys")
    write(os.path.join(sysdir, "winhttp.dll"), b"SYSTEM")

    patch_root = os.path.join(tmp, "gamepatch")
    pdir = os.path.join(patch_root, "10_test")
    write(os.path.join(pdir, "UnityCrossFire_Data", "a.bin"), b"PATCHED")
    write(os.path.join(pdir, "UnityCrossFire_Data", "new.bin"), b"NEW")
    write(os.path.join(pdir, "orig", "UnityCrossFire_Data", "a.bin"), b"ORIG")
    doc = {
        "id": "10_test", "label": "测试图", "switch": "hidden_map",
        "default_enabled": True,
        "files": [
            {"path": "UnityCrossFire_Data/a.bin", "bytes": 7,
             "sha256": sha(b"PATCHED"),
             "orig": {"bytes": 4, "sha256": sha(b"ORIG")},
             "orig_file": "orig/UnityCrossFire_Data/a.bin",
             "role": "测试补丁"},
            {"path": "UnityCrossFire_Data/new.bin", "bytes": 3,
             "sha256": sha(b"NEW"), "orig": None, "role": "测试新增"},
        ],
    }
    write(os.path.join(pdir, "patch.json"), json.dumps(doc, ensure_ascii=False, indent=2))

    # 未启用的包：switch 在配置里是 false，默认也不启用
    p2 = os.path.join(patch_root, "11_disabled")
    write(os.path.join(p2, "UnityCrossFire_Data", "b.bin"), b"B")
    write(os.path.join(p2, "patch.json"), json.dumps({
        "id": "11_disabled", "label": "未启用", "switch": "map_longcheng",
        "default_enabled": False,
        "files": [{"path": "UnityCrossFire_Data/b.bin", "bytes": 1,
                   "sha256": sha(b"B"), "orig": None, "role": "未启用"}],
    }, ensure_ascii=False, indent=2))

    runtime = os.path.join(tmp, "runtime")
    write(os.path.join(runtime, "ucf_mod.json"),
          json.dumps({"features": {"hidden_map": True, "map_longcheng": False}},
                     ensure_ascii=False))

    D.PAYLOAD = Path(payload)
    D.LOADER_HISTORY = Path(payload) / "loader_history.json"
    D.GAMEPATCH = Path(patch_root)
    D.RUNTIME = Path(runtime)
    D.MANIFEST_DIR = Path(runtime) / "deploy"
    D.BACKUP_ROOT = Path(tmp) / "backup"
    D.RUNTIME_CFG = Path(runtime) / "ucf_mod.json"
    D.SYS_WINHTTP = Path(sysdir) / "winhttp.dll"
    return game


def main():
    with tempfile.TemporaryDirectory(prefix="ucf_deploy_") as tmp:
        game = build_fixture(tmp)
        steps = D.build_plan(game)
        states = {s["rel"]: st for s, st in D.plan_states(game, steps)}
        print("== 1) 计划 ==")
        check(states.get("winhttp.dll") == "新增", "加载器缺失 -> 新增")
        check(states.get("winhttp_orig.dll") == "新增", "winhttp_orig 缺失 -> 新增")
        check(states.get("UnityCrossFire_Data/a.bin") == "原版", "本体文件原版 -> 可打补丁")
        check(states.get("UnityCrossFire_Data/new.bin") == "新增", "新增文件 -> 缺失也可铺")
        check(states.get("UnityCrossFire_Data/b.bin") == "已禁用", "未启用的包标记为已禁用")

        print("== 2) 部署 ==")
        rc = D.run_deploy(game, steps)
        check(rc == 0, "部署返回 0")
        check(open(os.path.join(game, "winhttp.dll"), "rb").read() == b"LOADER",
              "加载器已写入")
        check(open(os.path.join(game, "winhttp_orig.dll"), "rb").read() == b"SYSTEM",
              "系统 winhttp 副本已写入")
        check(open(os.path.join(game, "UnityCrossFire_Data", "a.bin"), "rb").read() == b"PATCHED",
              "本体文件已打补丁")
        check(open(os.path.join(game, "UnityCrossFire_Data", "new.bin"), "rb").read() == b"NEW",
              "新增文件已铺")
        check(not os.path.exists(os.path.join(game, "ucf_mod")), "游戏目录没有 ucf_mod\\")
        manifest = os.path.join(D.MANIFEST_DIR, D.game_id(game) + ".json")
        check(os.path.isfile(manifest), "部署清单在工程端")

        print("== 3) 幂等 ==")
        rc = D.run_deploy(game, D.build_plan(game))
        check(rc == 0, "第二次部署返回 0")

        print("== 4) 冲突拒绝 ==")
        game2 = os.path.join(tmp, "game2")
        os.makedirs(game2)
        write(os.path.join(game2, "UnityCrossFire_Data", "a.bin"), b"OTHER")
        steps2 = D.build_plan(game2)
        rc = D.run_deploy(game2, steps2)
        check(rc == 2, "原版哈希不对 -> 返回 2")
        check(not os.path.exists(os.path.join(game2, "winhttp.dll")),
              "冲突时零写入（加载器也没写）")

        print("== 5) 旧加载器：可覆盖，卸载回“没有加载器” ==")
        game3 = os.path.join(tmp, "game3")
        os.makedirs(game3)
        write(os.path.join(game3, "UnityCrossFire_Data", "a.bin"), b"ORIG")
        write(os.path.join(game3, "winhttp.dll"), b"OLD_LOADER")
        steps3 = D.build_plan(game3)
        states3 = {s["rel"]: st for s, st in D.plan_states(game3, steps3)}
        check(states3.get("winhttp.dll") == "原版", "已知旧加载器 -> 原版（可覆盖）")
        check(D.run_deploy(game3, steps3) == 0, "旧加载器部署返回 0")
        check(open(os.path.join(game3, "winhttp.dll"), "rb").read() == b"LOADER",
              "旧加载器被替换成新加载器")
        check(D.run_uninstall(game3) == 0, "旧加载器卸载返回 0")
        check(not os.path.exists(os.path.join(game3, "winhttp.dll")),
              "卸载后没有加载器（不还原旧版）")

        print("== 6) 卸载还原 ==")
        rc = D.run_uninstall(game)
        check(rc == 0, "卸载返回 0")
        check(open(os.path.join(game, "UnityCrossFire_Data", "a.bin"), "rb").read() == b"ORIG",
              "有备份的本体文件还原成原版")
        check(not os.path.exists(os.path.join(game, "UnityCrossFire_Data", "new.bin")),
              "新增文件被删除")
        check(not os.path.exists(os.path.join(game, "winhttp.dll")), "加载器被删除")
        check(not os.path.exists(os.path.join(game, "winhttp_orig.dll")), "winhttp_orig 被删除")
        check(not os.path.exists(manifest), "部署清单被删除")

    if FAIL:
        print("\n!! %d 项没过" % len(FAIL))
        return 1
    print("\nOK: 一键部署 / 幂等 / 冲突拒绝 / 卸载还原 全部通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
