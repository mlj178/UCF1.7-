# Fixed Point Teleport Hotkeys Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将定点瞬移点位2固定快捷键改为 F1/F2，并删除 F3、Alt+3、Alt+4 快捷键入口。

**Architecture:** 保持定点瞬移 RPC 和 Frida 实现不变，仅修改 Python 快捷键配置、Tk 事件映射及功能界面文案。设置页从核心配置动态派生，无需新增分支逻辑。

**Tech Stack:** Python 3、CustomTkinter、keyboard、unittest

---

### Task 1: 添加快捷键布局回归测试

**Files:**
- Create: `core/test_fixed_point_teleport_hotkeys.py`

- [x] 断言 F1/F2 是点位2固定动作。
- [x] 断言 F3、Alt+3、Alt+4 不在可用槽位和 Tk 监听中。
- [x] 断言功能清单、面板和说明文档显示 F1/F2 且不再显示 Alt+3/Alt+4。
- [x] 运行测试并确认因旧映射而失败。

### Task 2: 实施最小快捷键和文案修改

**Files:**
- Modify: `core/config.py`
- Modify: `ui/app.py`
- Modify: `features/31_fixed_point_teleport/manifest.json`
- Modify: `features/31_fixed_point_teleport/panel.py`
- Modify: `features/31_fixed_point_teleport/定点瞬移-简要说明.md`

- [x] 将点位2固定动作映射到 F1/F2。
- [x] 从快捷键槽位和 Tk 映射移除 F3、Alt+3、Alt+4。
- [x] 同步所有用户可见文案。
- [x] 运行回归测试并确认通过。

### Task 3: 完整验证

**Files:**
- Verify only: all modified Python and JSON files

- [x] 运行快捷键测试及现有定点瞬移文档断言。
- [x] 运行 Python 编译、JavaScript 语法与 JSON 解析检查。
- [x] 搜索确认运行时代码和文案中没有 F3、Alt+3、Alt+4 残留。
- [x] 检查 Git diff，确认没有覆盖用户的手雷模式改动。

> 注：旧静态测试中其余 12 项仍引用已删除的 `AAAAA-fixed_point_teleport_min.js` 和 `AAAAA-fixed_point_teleport_ui.py`，属于本次改动前已存在的测试基础设施问题，不纳入本次快捷键调整范围。
