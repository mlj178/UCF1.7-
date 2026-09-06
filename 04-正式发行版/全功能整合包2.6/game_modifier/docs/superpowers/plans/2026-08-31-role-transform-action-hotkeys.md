# 角色变身动作快捷键 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让角色变身的四个按钮可以作为独立选项绑定到 Ctrl+1～Ctrl+5，并在按键时执行原按钮动作。

**Architecture:** 在 `core.config` 定义角色变身动作的稳定绑定对象。设置页将普通功能 ID 和该对象共同展示、按唯一绑定键去重；热键管理器保存两种值，应用层把对象的 payload 原样交给现有动作控制器。

**Tech Stack:** Python 3、CustomTkinter、keyboard、unittest、JSON。

---

### Task 1: 添加动作绑定的失败测试

**Files:**
- Create: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`
- Modify: `全功能整合包2.5/game_modifier/core/config.py`
- Modify: `全功能整合包2.5/game_modifier/core/hotkey_manager.py`
- Modify: `全功能整合包2.5/game_modifier/ui/settings_window.py`
- Modify: `全功能整合包2.5/game_modifier/ui/app.py`

- [ ] **Step 1: 创建测试文件**

在新测试中加载配置、热键管理器和应用方法。测试必须断言四项动作及其 payload：

```python
self.assertEqual(
    {"local_hero", "local_terminator", "bot_hero", "bot_terminator"},
    {item["payload"]["action"] for item in ROLE_TRANSFORM_HOTKEY_ACTIONS},
)
```

也必须用假动作控制器断言 `_on_hotkey_toggle` 对以下绑定发起精确调用：

```python
binding = {
    "feature_id": "role_transform",
    "action": "trigger",
    "payload": {"action": "bot_terminator"},
}
# expected: trigger_feature_action("role_transform", "trigger", {"action": "bot_terminator"})
```

- [ ] **Step 2: 运行失败测试**

Run: `python -m unittest core.test_role_transform_action_hotkeys -v`

Expected: FAIL，原因是动作定义和 payload 分派尚不存在。

### Task 2: 实现兼容的动作绑定与热键分派

**Files:**
- Modify: `全功能整合包2.5/game_modifier/core/config.py`
- Modify: `全功能整合包2.5/game_modifier/core/hotkey_manager.py`
- Modify: `全功能整合包2.5/game_modifier/ui/app.py`
- Modify: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`

- [ ] **Step 1: 定义四个可绑定动作**

在 `config.py` 添加 `ROLE_TRANSFORM_HOTKEY_ACTIONS`。每项采用如下结构，另三项只替换 label 与 `payload.action`：

```python
{
    "label": "本地玩家：选择英雄",
    "feature_id": "role_transform",
    "action": "trigger",
    "payload": {"action": "local_hero"},
}
```

- [ ] **Step 2: 允许热键配置保存动作对象**

在 `hotkey_manager.py` 增加识别动作对象的辅助逻辑。`_load_hotkeys` 仅将字符串功能 ID 与 `HOTKEY_EXCLUDED` 比较，完整动作对象保留。`set_hotkey` 的重复清理根据稳定绑定键执行：字符串用自身，角色动作用 `role_transform:<payload.action>`。现有 `hotkeys.json` 的字符串读取和保存格式不变。

- [ ] **Step 3: 转交 payload**

在 `ui/app.py` 的 `_on_hotkey_toggle` 字典分支中复制可选 `payload` 并调用：

```python
self._feature_controller.trigger_feature_action(feature_id, action, payload)
```

没有 payload 的固定定点瞬移绑定仍传 `None`，保持 F1、F2、Alt+1、Alt+2 的原有行为。

- [ ] **Step 4: 验证测试通过**

Run: `python -m unittest core.test_role_transform_action_hotkeys -v`

Expected: PASS。

### Task 3: 在 Ctrl+1～Ctrl+5 的下拉框提供动作选项

**Files:**
- Modify: `全功能整合包2.5/game_modifier/ui/settings_window.py`
- Modify: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`

- [ ] **Step 1: 扩展测试**

测试设置窗口源代码引用 `ROLE_TRANSFORM_HOTKEY_ACTIONS` 和 `binding_key`，并确认四个中文名称会作为候选项。测试还应确认同一具体动作不能重复绑定，但四个不同动作可以同时占用不同 Ctrl 槽位。

- [ ] **Step 2: 运行失败测试**

Run: `python -m unittest core.test_role_transform_action_hotkeys -v`

Expected: FAIL，设置页尚未构建角色动作候选项。

- [ ] **Step 3: 修改候选项和去重逻辑**

在 `settings_window.py` 导入动作定义，建立“显示名 → 绑定值”映射。普通功能映射到字符串，角色动作映射到字典副本。`binding_key(binding)` 对字符串返回自身，对动作对象返回 `role_transform:<payload.action>`。使用该键计算可用候选项和处理选项变化。五个 Ctrl 槽位共享候选项；固定快捷键区域完全不改。

- [ ] **Step 4: 验证测试通过**

Run: `python -m unittest core.test_role_transform_action_hotkeys -v`

Expected: PASS。

### Task 4: 完整回归验证

**Files:**
- Verify: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`
- Verify: `全功能整合包2.5/game_modifier/core/test_fixed_point_teleport_hotkeys.py`
- Verify: `全功能整合包2.5/game_modifier/features/34_role_transform/test_role_transform_integration.py`

- [ ] **Step 1: 运行功能回归测试**

Run: `python -m unittest core.test_role_transform_action_hotkeys core.test_fixed_point_teleport_hotkeys features.34_role_transform.test_role_transform_integration -v`

Expected: PASS，四个角色动作的 payload 正确，定点瞬移固定快捷键和原有角色按钮不回归。

- [ ] **Step 2: 运行语法与差异检查**

Run: `python -m py_compile core/config.py core/hotkey_manager.py ui/settings_window.py ui/app.py`

Expected: 无输出且退出码为 0。

Run: `git diff --check`

Expected: 无空白错误。
