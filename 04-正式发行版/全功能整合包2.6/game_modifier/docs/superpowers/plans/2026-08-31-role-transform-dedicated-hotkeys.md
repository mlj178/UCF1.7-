# 角色变身专用快捷键与监听清理 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复普通快捷键重复触发，并将角色变身四项动作固定映射到 Ctrl+Q/W/E/R。

**Architecture:** `core.config` 将角色变身四项从普通下拉候选值改成专用动作映射。`HotkeyManager` 统一存储所有 `keyboard.add_hotkey` 返回的注销函数，并在重新应用和关闭时用 `keyboard.remove_hotkey` 清理。设置页只显示普通 Ctrl+1～Ctrl+5 候选项和不可编辑的专用角色快捷键。

**Tech Stack:** Python 3、CustomTkinter、keyboard、unittest、JSON。

---

### Task 1: 写出监听注销与专用映射的失败测试

**Files:**
- Modify: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`
- Modify: `全功能整合包2.5/game_modifier/core/test_native_hotkey_listener.py`
- Modify: `全功能整合包2.5/game_modifier/core/config.py`
- Modify: `全功能整合包2.5/game_modifier/core/hotkey_manager.py`

- [ ] **Step 1: 添加动作映射与注销测试**

新增断言：专用映射的键仅为 `ctrl+q`、`ctrl+w`、`ctrl+e`、`ctrl+r`，并按顺序携带 `local_hero`、`local_terminator`、`bot_hero`、`bot_terminator`。用 mock 的 `keyboard.remove_hotkey` 和两个 sentinel handle 验证 `setup_hotkeys`、`cleanup` 都会注销每个旧 handle：

```python
with mock.patch("core.hotkey_manager.keyboard.remove_hotkey") as remove_hotkey:
    manager._hotkey_handles = [first_handle, second_handle]
    manager.cleanup()
remove_hotkey.assert_has_calls([mock.call(first_handle), mock.call(second_handle)])
```

- [ ] **Step 2: 运行测试，确认失败**

Run: `python -m unittest core.test_role_transform_action_hotkeys core.test_native_hotkey_listener -v`

Expected: FAIL，当前没有角色专用映射，且当前代码调用 `handle.unhook()` 而不是 `keyboard.remove_hotkey(handle)`。

### Task 2: 修复监听清理并建立固定角色快捷键

**Files:**
- Modify: `全功能整合包2.5/game_modifier/core/config.py`
- Modify: `全功能整合包2.5/game_modifier/core/hotkey_manager.py`
- Modify: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`
- Modify: `全功能整合包2.5/game_modifier/core/test_native_hotkey_listener.py`

- [ ] **Step 1: 替换角色动作配置**

将 `ROLE_TRANSFORM_HOTKEY_ACTIONS` 替换为以快捷键为 key 的专用映射。每个值包含 `feature_id: "role_transform"`、`action: "trigger"`、对应的 `payload.action` 与显示标签；Ctrl+Q/W/E/R 不加入 `HOTKEY_POSITIONS`。

- [ ] **Step 2: 正确注销旧监听**

在 `setup_hotkeys` 和 `cleanup` 中把：

```python
handle.unhook()
```

替换为：

```python
keyboard.remove_hotkey(handle)
```

在重新注册普通功能前，循环注册专用角色动作；它们和定点瞬移专用动作都通过 `_on_dedicated_hotkey_triggered` 传递完整 payload。

- [ ] **Step 3: 清除旧的可编辑角色绑定**

在 `_load_hotkeys` 中识别 `feature_id == "role_transform"` 的动作对象，并将其置为 `None`，使历史 Ctrl+1～Ctrl+5 绑定在下次保存时从 JSON 中移除。

- [ ] **Step 4: 验证通过**

Run: `python -m unittest core.test_role_transform_action_hotkeys core.test_native_hotkey_listener -v`

Expected: PASS，旧监听被注销，Ctrl+Q/W/E/R 专用映射正确，旧普通槽位角色绑定被清除。

### Task 3: 更新设置页展示与下拉候选项

**Files:**
- Modify: `全功能整合包2.5/game_modifier/ui/settings_window.py`
- Modify: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`

- [ ] **Step 1: 添加失败测试**

测试断言设置页不再导入或遍历 `ROLE_TRANSFORM_HOTKEY_ACTIONS` 构造 Ctrl+1～Ctrl+5 候选项；断言它显示四条固定绑定文字 `Ctrl+Q`、`Ctrl+W`、`Ctrl+E`、`Ctrl+R`。

- [ ] **Step 2: 运行测试，确认失败**

Run: `python -m unittest core.test_role_transform_action_hotkeys -v`

Expected: FAIL，角色动作当前仍被加入 `option_bindings`。

- [ ] **Step 3: 最小化更新设置页**

移除角色动作加入 `option_bindings` 的循环，恢复 Ctrl+1～Ctrl+5 只列普通功能。下方新增“角色变身固定快捷键”区域，逐条读取专用映射的 label 并显示只读行。不要添加编辑控件。

- [ ] **Step 4: 验证通过**

Run: `python -m unittest core.test_role_transform_action_hotkeys -v`

Expected: PASS。

### Task 4: 回归验证

**Files:**
- Verify: `全功能整合包2.5/game_modifier/core/test_role_transform_action_hotkeys.py`
- Verify: `全功能整合包2.5/game_modifier/core/test_native_hotkey_listener.py`
- Verify: `全功能整合包2.5/game_modifier/core/test_fixed_point_teleport_hotkeys.py`
- Verify: `全功能整合包2.5/game_modifier/features/34_role_transform/test_role_transform_integration.py`

- [ ] **Step 1: 运行相关回归测试**

Run: `python -m unittest core.test_role_transform_action_hotkeys core.test_native_hotkey_listener core.test_fixed_point_teleport_hotkeys -v`

Run: `python -m unittest discover -s features/34_role_transform -p 'test_*.py' -v`

Expected: PASS；不存在旧监听残留，定点瞬移与角色变身按钮不回归。

- [ ] **Step 2: 运行语法和差异检查**

Run: `python -m py_compile core/config.py core/hotkey_manager.py ui/settings_window.py ui/app.py`

Run: `git diff --check`

Expected: 两条命令均以退出码 0 完成。
