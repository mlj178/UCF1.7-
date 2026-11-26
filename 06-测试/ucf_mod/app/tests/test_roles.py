#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""自检：身份（用户 / 开发者）与页表的对应关系。

跑法：python app/tests/test_roles.py

只读，不开窗口。查 6 件事：
  1) normalize_role 认得 user/dev/用户/开发者/大小写，认不出返回空串
  2) UCF_ROLE 环境变量优先
  3) USER_PAGES = 地图 / 部署，而且是开发页的子集
  4) 开发页 11 个、一组一个不重不漏；TAB_OLD_MAP 覆盖全部页名
  5) 控制台入口有 on_flat_tab / switch_role / App(role=...)；ui/role.py 有 ask_role
  6) 用户页里没有开发页（防止手滑把「人机路点」塞进用户身份）
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
UCF_ROOT = HERE
while not os.path.isfile(os.path.join(UCF_ROOT, ".ucfroot")) and os.path.dirname(UCF_ROOT) != UCF_ROOT:
    UCF_ROOT = os.path.dirname(UCF_ROOT)      # 项目根：靠 .ucfroot 标记，本文件搬到哪都对
APP = os.path.join(UCF_ROOT, "app")
for _p in (os.path.join(APP, "core"), APP):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ui import role as R          # noqa: E402
from ui.consts import TAB_GROUPS, TAB_OLD_MAP, USER_PAGES  # noqa: E402

FAIL = []


def check(cond, what):
    if cond:
        print("  OK   " + what)
    else:
        print("  !!   " + what)
        FAIL.append(what)


def read(rel):
    with open(os.path.join(UCF_ROOT, rel), "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def main():
    print("== 1) normalize_role")
    for raw, want in (("user", "user"), ("DEV", "dev"), ("用户", "user"), ("开发者", "dev"),
                      (" 2 ", "dev"), ("xx", ""), ("", ""), (None, "")):
        check(R.normalize_role(raw) == want, "normalize_role(%r) = %r" % (raw, want))

    print("== 2) UCF_ROLE 环境变量")
    old = os.environ.get("UCF_ROLE")
    try:
        os.environ["UCF_ROLE"] = "开发者"
        check(R.env_role() == "dev", "UCF_ROLE=开发者 -> dev")
        os.environ.pop("UCF_ROLE", None)
        check(R.env_role() == "", "没设 UCF_ROLE -> 空（回落到配置 / 弹窗）")
    finally:
        if old is None:
            os.environ.pop("UCF_ROLE", None)
        else:
            os.environ["UCF_ROLE"] = old

    print("== 3) 用户身份的两页")
    dev_pages = [p for _g, pages in TAB_GROUPS for p in pages]
    check(tuple(USER_PAGES) == ("地图", "部署"), "USER_PAGES = 地图 / 部署（实际 %s）" % (USER_PAGES,))
    check(set(USER_PAGES) <= set(dev_pages), "用户的两页都在开发页里（超集关系）")
    check(not (set(USER_PAGES) & {"地图总览", "人机路点", "录制", "数据", "可视化",
                                  "快捷键", "车测", "开发者选项"}),
          "用户身份里没有开发页")

    print("== 4) 开发身份的 10 页")
    # 2026-11-26：「导出」页连同 Ctrl+E 导出一起删了，10 页
    check(len(dev_pages) == len(set(dev_pages)) == 10, "开发页 10 个、不重不漏（实际 %d）" % len(dev_pages))
    check([g[0] for g in TAB_GROUPS] == ["插件开关", "路点数据", "部署与测试", "开发调试"],
          "4 个功能组的名字和顺序")
    check(all(p in TAB_OLD_MAP for p in dev_pages), "TAB_OLD_MAP 覆盖全部页名（旧配置能迁移）")

    print("== 5) 入口与模块")
    con = read(os.path.join("app", "控制台.pyw"))
    check("def on_flat_tab" in con, "控制台有 on_flat_tab()（用户身份两页平铺）")
    check("def switch_role" in con, "控制台有 switch_role()")
    check("App(role=role)" in con, "main() 按身份创建窗口")
    check("def ask_role" in read(os.path.join("app", "ui", "role.py")), "ui/role.py 有 ask_role()")

    print("== 6) 身份写在配置里")
    ui = read(os.path.join("app", "ui", "role.py"))
    check('ui["role"]' in ui and "UCF_ROLE" in ui, "role.py 读写 ui.role / UCF_ROLE")

    if FAIL:
        print("\n!! %d 项没过" % len(FAIL))
        return 1
    print("\nOK: 身份两页 / 开发十一页 / 组名 / 旧配置迁移 都对得上")
    return 0


if __name__ == "__main__":
    sys.exit(main())
