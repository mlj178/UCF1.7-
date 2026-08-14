# Fixed Point Teleport Cross-Round Retention Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在同一房间内跨回合保留定点瞬移点位，同时阻止 pending 动作跨回合执行。

**Architecture:** 保留回合生命周期 Hook，但将其改为只清除 `pending.saveSlot` 与 `pending.teleportSlot`。完整的 `handleRoundBoundary()` 仅由模式实例变化和房间销毁触发，因此 `roomGeneration` 只在真正房间边界变化。

**Tech Stack:** Frida JavaScript、Python unittest 静态测试、Markdown

---

### Task 1: 添加跨回合生命周期回归测试

**Files:**
- Modify: `features/31_fixed_point_teleport/test_fixed_point_teleport_static.py`

- [ ] **Step 1: 修改生命周期测试**

断言存在 `clearPendingRoundActions(reason)`，两个回合 Hook 调用该函数且对应 Hook 代码段不调用 `handleRoundBoundary`；继续断言 `mode_base_changed` 和 `game_manager_destroy` 调用完整边界清理。

- [ ] **Step 2: 运行测试并确认 RED**

Run: `python -m unittest features.31_fixed_point_teleport.test_fixed_point_teleport_static.FixedPointTeleportStaticTests.test_js_preserves_saved_points_across_round_lifecycle -v`

Expected: FAIL，因为脚本尚未包含 `clearPendingRoundActions`。

### Task 2: 实现回合轻量清理

**Files:**
- Modify: `features/31_fixed_point_teleport/script.js`

- [ ] **Step 1: 添加轻量清理函数**

新增 `clearPendingRoundActions(reason)`，仅将两个 pending 槽位置零并记录日志，不调用 `resetRuntime()`、不清空 `savedPoints`、不递增 `roomGeneration`。

- [ ] **Step 2: 替换两个回合 Hook 的处理**

让 `GameManager.GameRoundEnd` 和 `GameManager.NewGameRoundStart` 调用轻量清理函数；保留 `GameManager.OnDestroy` 和 `mode_base_changed` 的完整清理。

- [ ] **Step 3: 运行测试并确认 GREEN**

Run: `python -m unittest features.31_fixed_point_teleport.test_fixed_point_teleport_static.FixedPointTeleportStaticTests.test_js_preserves_saved_points_across_round_lifecycle -v`

Expected: PASS。

### Task 3: 更新说明并完整验证

**Files:**
- Modify: `features/31_fixed_point_teleport/定点瞬移-简要说明.md`

- [ ] **Step 1: 更新生命周期说明**

说明同房间跨回合保留点位、回合边界取消 pending 动作、换房或关闭功能仍清点。

- [ ] **Step 2: 运行完整验证**

Run: `python -m unittest features.31_fixed_point_teleport.test_fixed_point_teleport_static -v`

Run: `node --check "features\\31_fixed_point_teleport\\script.js"`

Run: `git diff --check -- "全功能整合包2.5/game_modifier/features/31_fixed_point_teleport"`

Expected: 新增生命周期测试和现有可运行测试全部通过，JavaScript 语法正确，改动无空白错误。
