# 全模式房间人数开关 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让“全模式房间人数”只有在用户开启开关并点击“应用人数”后才写入补丁，关闭开关时立即恢复。

**Architecture:** 自定义卡片在现有滑条和按钮旁显示标准 `CTkSwitch`，开关仍走共享 `ActionRouter` 生命周期。脚本将“已启用”与“已写入补丁”分离：`enable` 仅记录开关状态，`setConfig` 仅在已启用时写补丁，`disable` 继续使用既有恢复路径。清单关闭启动恢复，防止重新连接时自动写入。

**Tech Stack:** Python 3、CustomTkinter、Frida JavaScript、`unittest` 静态回归测试。

---

### Task 1: 为显式开关行为建立失败测试

**Files:**
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`
- Test: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`

- [ ] **Step 1: 添加针对卡片、清单和脚本门控的测试**

```python
def test_panel_exposes_a_switch_and_requires_it_before_apply(self):
    text = (FEATURE_DIR / "panel.py").read_text(encoding="utf-8")
    self.assertIn("ctk.CTkSwitch", text)
    self.assertIn('callbacks["toggle"](self.feature_id)', text)
    self.assertIn('if not self.callbacks["is_enabled"](self.feature_id):', text)
    self.assertIn("请先开启功能", text)

def test_manifest_disables_startup_restore(self):
    manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))
    self.assertFalse(manifest["lifecycle"]["restore"])

def test_runtime_enable_only_arms_and_apply_requires_enabled(self):
    text = RUNTIME_JS.read_text(encoding="utf-8")
    enable_body = text.split("function enable(config)", 1)[1].split("function applyConfig(config)", 1)[0]
    apply_body = text.split("function applyConfig(config)", 1)[1].split("function disable()", 1)[0]
    self.assertNotIn("writeState(", enable_body)
    self.assertIn("enabled = true", enable_body)
    self.assertIn("if (!enabled)", apply_body)
    self.assertIn("feature_disabled", apply_body)
```

- [ ] **Step 2: 运行新增测试，确认旧实现失败**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static.RoomPlayerCountStaticTests -v`

Expected: FAIL，因为当前面板没有 `CTkSwitch`，清单的 `restore` 为 `true`，且 `enable` 会调用 `writeState`。

- [ ] **Step 3: 仅提交失败测试**

```bash
git add -- "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py"
git commit -m "test: define room player count switch lifecycle"
```

### Task 2: 实现运行时手动应用与即时恢复

**Files:**
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/script.js:340-460`
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json:15-30`
- Test: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`

- [ ] **Step 1: 让 `enable` 仅设置状态，不接触游戏内存**

```javascript
function enable(config) {
  totalPlayers = normalize(config && Object.prototype.hasOwnProperty.call(config, 'total_players') ?
    config.total_players : totalPlayers);
  enabled = true;
  log('info', '已开启；请点击“应用人数”后写入当前设置。');
  status(true);
  return successResult();
}
```

- [ ] **Step 2: 在 `applyConfig` 首行拒绝未开启的写入，保留其余现有写入与校验流程**

```javascript
if (!enabled) {
  return resultFailure('feature_disabled', '请先开启全模式房间人数功能，再点击应用人数');
}
```

删除旧的 `if (!enabled) return enable(...)` 分支，使 `writeState(...)` 仅能由已启用的 `applyConfig` 路径到达。

- [ ] **Step 3: 取消自动恢复并保留立即关闭清理**

```json
"lifecycle": {
  "cleanup": true,
  "restore": false,
  "requires_room_ready_reapply": false,
  "room_ready_retry": false,
  "room_ready_reapply_exempt_reason": "人数只在用户开启后手动点击应用人数时写入；关闭开关立即恢复补丁，重连游戏不自动重放。"
}
```

保留 `disable()` 的 `stopEntityDiagnostic()`、补丁还原、`restoreBaselineProfile()`、`status(false)` 和幂等返回逻辑。

- [ ] **Step 4: 运行同一测试，确认通过**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static.RoomPlayerCountStaticTests -v`

Expected: PASS。

- [ ] **Step 5: 提交运行时生命周期改动**

```bash
git add -- "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/script.js" "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json"
git commit -m "feat: require manual application for room player count"
```

### Task 3: 接入卡片开关并移除隐式应用

**Files:**
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/panel.py:33-164`
- Test: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`

- [ ] **Step 1: 在控制器中加入显式开关状态处理**

```python
def enabled(self):
    return bool(self.callbacks["is_enabled"](self.feature_id))

def toggle(self):
    self.cancel_pending()
    self.callbacks["toggle"](self.feature_id)
    if self.enabled():
        self.show("已开启：请点击应用人数", "#fbbf24")
    else:
        self.show("已关闭：正在恢复原始人数逻辑", "#fbbf24")
```

开关通过共享回调触发，因此关闭会调用脚本的 `disable()`；不要在面板重复实现内存恢复。

- [ ] **Step 2: 让 `apply` 先检查开关，并仅在已开启时保存/写入**

```python
if not self.callbacks["is_enabled"](self.feature_id):
    self.show("请先开启功能，再点击应用人数", "#fbbf24")
    self.log("功能未开启，未应用人数。")
    return
```

断开连接时只保存人数，并显示“未连接：人数已保存；连接后请手动点击应用人数”；删除 `enabled: True` 载荷，避免按钮绕过开关。

- [ ] **Step 3: 删除滑条的延迟/松开自动应用，增加 `CTkSwitch`**

```python
switch = ctk.CTkSwitch(top, text="", width=42, command=controller.toggle)
switch.grid(row=0, column=3, sticky="e", padx=(8, 0))
```

将 `switch` 放入返回的 `ui_handles["switch"]`，并删除 `host.after(180, self.apply)` 与 `<ButtonRelease-1>` 绑定。滑条只显示“待应用：点击应用人数后生效”。

- [ ] **Step 4: 运行静态测试，确认通过**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static.RoomPlayerCountStaticTests -v`

Expected: PASS。

- [ ] **Step 5: 提交面板改动**

```bash
git add -- "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/panel.py" "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py"
git commit -m "feat: add explicit room player count switch"
```

### Task 4: 运行完整相关验证

**Files:**
- Verify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`
- Verify: `04-正式发行版/全功能整合包2.5/game_modifier/ui/controllers/action_router.py`

- [ ] **Step 1: 运行房间人数测试和 UI 相关静态测试**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static game_modifier.ui.test_version_metadata_static -v`

Expected: 所有测试通过，且无导入错误。

- [ ] **Step 2: 检查语法和变更范围**

Run: `python -m py_compile game_modifier/features/35_room_player_count/panel.py && node --check game_modifier/features/35_room_player_count/script.js && git diff --check && git status --short`

Expected: 所有命令退出码为 0；新增变更限于规格、计划和房间人数功能文件，不包含用户的既有改动。
