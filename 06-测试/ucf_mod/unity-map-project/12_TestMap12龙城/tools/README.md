# 龙城的工具脚本（存档 + 待参数化）

这些脚本**就是龙城的源码**。2026-11-24 从 `D:\ucf_unity\` 根目录抢救进来 —— 在此之前它们不在任何 git 里，
而且 `globalgamemanagers` 的 13 条名册、`sharedassets0.assets` 的 19 字节注册表补丁**根本没有对应脚本**，
是某次会话里手工改掉的。这就是"改动只存在于游戏目录"的真实代价。

| 脚本 | 干什么 | 依赖 |
| --- | --- | --- |
| `patch_a.py` | 从 Unity 构建产物生成 `sharedassets12.assets`（改名 + 修 `.resS` 路径） | UnityPy |
| `repatch.py` | `level0` 的外部依赖名 `sharedassets0` → `sharedassets12` | 无 |
| `patch_final.py` | 借 `level11` 骨架、换 56 个网格/材质、抬 16 个出生点 | UnityPy |
| `make_final.py` | 只做 `level0` 改名（patch_a/repatch 的子集，保留作对照） | 无 |
| `check_ress2.py` / `find_ress.py` / `find_ext.py` | 查 `.resS` / external 引用 | 无 |
| `final_check.py` / `verify_patch.py` / `verify_final.py` | 产物校验（对象数 / 名册 / 哈希） | UnityPy |
| `walk_glb.py` / `inspect_glb.py` / `render_glb.py` | GLB 检查与渲染预览 | pygltflib / trimesh |
| `gt.ps1` / `runtest.ps1` / `launch.ps1` | 自动进图测试（DPI + 窗口句柄两个坑） | 无 |

**路径写死提醒**：这批脚本里 `GAME`、`OUT`、`SRCB` 指向的是 2026-11-22 的临时位置
（`D:\ucf_test_level12\game`、`D:\ucf_unity\build`、`D:\ucf_unity\out_final`）。
现在当"存档/证据"用；要重跑先改这三个变量，或者等参数化的 `build.py` 落地。
