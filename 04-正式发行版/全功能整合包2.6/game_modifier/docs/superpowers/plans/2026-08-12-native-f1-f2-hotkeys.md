# Native F1/F2 Hotkeys Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 使用 Windows `RegisterHotKey` 让点位2的 F1/F2 在游戏前台时可触发。

**Architecture:** 新增专用 Win32 消息线程管理系统热键；现有 `HotkeyManager` 负责选择原生注册或 `keyboard` 回退，并继续把动作投递到 Tk 主线程。F1/F2 不再保留 Tk 局部绑定，避免重复触发。

**Tech Stack:** Python 3、ctypes、Win32 User32、threading、unittest

---

### Task 1: 原生热键组件

**Files:**
- Create: `core/native_hotkey_listener.py`
- Create: `core/test_native_hotkey_listener.py`

- [x] 写失败测试，覆盖 F1/F2 注册、WM_HOTKEY 分派、失败结果和 UnregisterHotKey 清理。
- [x] 运行测试并确认因组件不存在而失败。
- [x] 实现专用消息线程、`MOD_NOREPEAT` 注册和可停止生命周期。
- [x] 运行测试并确认通过。

### Task 2: 接入 HotkeyManager

**Files:**
- Modify: `core/hotkey_manager.py`
- Modify: `core/test_native_hotkey_listener.py`
- Modify: `ui/app.py`

- [x] 写失败测试，确认原生注册成功的 F1/F2不再调用 `keyboard.add_hotkey`，失败键才回退。
- [x] 运行测试并确认旧管理器不满足行为。
- [x] 接入原生监听器并在重新设置/关闭时停止。
- [x] 从 Tk 映射删除 F1/F2，保留 Alt+1/Alt+2。
- [x] 运行测试并确认通过。

### Task 3: 验证

**Files:**
- Verify: all files above and existing shortcut regression tests

- [x] 运行原生组件、快捷键映射和定点瞬移文档测试。
- [x] 运行 Python 编译和差异检查。
- [x] 在 Windows 上执行原生 F1/F2注册/解除探测。
- [ ] 用户重启修改器后在游戏前台进行人工测试。
