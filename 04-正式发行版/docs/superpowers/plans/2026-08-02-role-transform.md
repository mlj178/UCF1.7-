# 角色变身四按钮 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在单功能目录实现四个即时动作按钮，本地玩家使用游戏原生选择界面，Bot 使用游戏原生随机英雄或超级终结者逻辑。

**Architecture:** Frida RPC 只提交一次性 `pendingAction`，`ModeBase.Update` Hook 在游戏主线程消费动作并重新解析当前模式及玩家。脚本不模拟完整蓝箱回调、不缓存运行态对象，也不从 RPC 线程直接调用 Unity/游戏函数。

**Tech Stack:** Frida JavaScript、Windows x86 IL2CPP、Python 3、CustomTkinter、标准库 unittest、IDA Pro MCP。

---

### Task 1: 用失败测试固定新行为契约

**Files:**
- Modify: `05-正式功能/34-角色变身/test_role_transform_static.py`
- Test: `05-正式功能/34-角色变身/test_role_transform_static.py`

- [ ] **Step 1: Replace the old pickup-probe tests with the new contract**

测试必须覆盖：四个 action；`ModeBase_Update: 0x00AF6A00`；`pendingAction`；`NanoRoleSelect_OpenMasterRole: 0x00B4ED30`；Bot 两个随机入口；`Singleton_GameManager_get_instance: 0x004A8170`；`SingletonGameManager_get_instance_Method: 0x00E1CE64`；禁止调用完整蓝箱回调和禁止直接写 nanoRole。

```python
def test_script_queues_four_actions_for_main_thread_execution(self):
    script = SCRIPT.read_text(encoding="utf-8")
    for action in ("local_hero", "local_terminator", "bot_hero", "bot_terminator"):
        self.assertIn(action, script)
    self.assertIn("pendingAction", script)
    self.assertIn("ModeBase_Update: 0x00AF6A00", script)
    self.assertIn("function consumePendingAction", script)

def test_script_uses_native_select_and_random_routes(self):
    script = SCRIPT.read_text(encoding="utf-8")
    for token in (
        "NanoRoleSelect_OpenMasterRole: 0x00B4ED30",
        "Mode_Nano4_Terminator_BecomeRandomMasterHero: 0x00B42E90",
        "Mode_Nano4_Terminator_TryBecomeRandomMasterTerminator: 0x00B45B90",
        "Native.openMasterRole(selector, isHero",
        "Native.becomeRandomMasterHero(mode, player, 0, ptr(0))",
        "Native.tryBecomeRandomMasterTerminator(mode, player, ptr(0))",
    ):
        self.assertIn(token, script)
```

- [ ] **Step 2: Run the test and verify RED**

Run:

```powershell
python -m unittest "05-正式功能\34-角色变身\test_role_transform_static.py" -v
```

Expected: FAIL because the current script still contains the pickup probe and direct fixed-role calls.

- [ ] **Step 3: Commit only after the implementation turns the contract green**

No test-only commit is made because the feature files already contain pre-existing staged work; keep the failing test local until Tasks 2 and 3 pass.

### Task 2: Rewrite the Frida core around pending main-thread actions

**Files:**
- Modify: `05-正式功能/34-角色变身/AAAAA-role_transform_min.js`
- Test: `05-正式功能/34-角色变身/test_role_transform_static.py`

- [ ] **Step 1: Replace pickup state with the one-slot action state**

Use this runtime shape and fixed action set:

```javascript
var VALID_ACTIONS = {
    local_hero: true,
    local_terminator: true,
    bot_hero: true,
    bot_terminator: true
};

var Runtime = {
    feature_id: "role_transform",
    enabled: false,
    initialized: false,
    generation: 0,
    hooks: [],
    pendingAction: "",
    stats: {
        requests: 0,
        busy_rejections: 0,
        main_thread_consumed: 0,
        local_selector_opened: 0,
        bot_scanned: 0,
        bot_applied: 0,
        bot_skipped: 0,
        error_count: 0,
        cleanup_count: 0,
        last_request: "",
        last_completed: "",
        last_error: ""
    }
};
```

- [ ] **Step 2: Bind only the verified native functions**

Create `NativeFunction` wrappers for `ModeBase.Update`, `Mode_Nano4.get_instance3`, `NanoRoleSelect.OpenMasterRole`, both Bot random helpers, `Player.get_isMyPlayer`, `HealthData.get_isDead`, and shared `Singleton<GameManager>.get_instance`. Pass the runtime value read from `base + 0xE1CE64` as the shared generic method's `MethodInfo*`.

```javascript
Native.getGameManager = new NativeFunction(
    Runtime.base.add(RVA.Singleton_GameManager_get_instance),
    "pointer", ["pointer"], CALL_CONV
);

var methodInfo = Runtime.base.add(RVA.SingletonGameManager_get_instance_Method).readPointer();
var manager = Native.getGameManager(methodInfo);
```

- [ ] **Step 3: Implement safe local selector actions**

Resolve `GameManager.myPlayer` from TypeInfo static fields, verify `Player.get_isMyPlayer`, read `Player.nanoRoleSelect + 0xA8`, and call:

```javascript
Native.openMasterRole(selector, isHero ? 1 : 0, ptr(0));
```

Increment `local_selector_opened` only after the call returns.

- [ ] **Step 4: Implement safe Bot enumeration and random actions**

Read `GameManager.allPlayers + 0x1C` as an IL2CPP array (`max_length + 0x0C`, elements + `0x10`). Cap iteration at 64, require `ClientData.isBot`, exclude local player, require `HealthData.get_isDead == false`, then call exactly one random helper per eligible Bot.

```javascript
if (action === "bot_hero") {
    Native.becomeRandomMasterHero(mode, player, 0, ptr(0));
} else {
    Native.tryBecomeRandomMasterTerminator(mode, player, ptr(0));
}
```

- [ ] **Step 5: Attach the Update hook and expose standard RPC**

`trigger(action)` validates enabled state, action name and empty pending slot. `consumePendingAction()` clears the slot before execution. `disable()` and `cleanup()` detach hooks and clear pending state.

```javascript
Interceptor.attach(Runtime.base.add(RVA.ModeBase_Update), {
    onEnter: function () {
        if (Runtime.enabled && Runtime.pendingAction) consumePendingAction();
    }
});
```

- [ ] **Step 6: Run JavaScript syntax and static tests**

Run:

```powershell
node --check "05-正式功能\34-角色变身\AAAAA-role_transform_min.js"
python -m unittest "05-正式功能\34-角色变身\test_role_transform_static.py" -v
```

Expected: JavaScript syntax succeeds; JS contract tests pass, while any not-yet-updated UI assertions may still fail.

### Task 3: Simplify the CustomTkinter UI to four actions

**Files:**
- Modify: `05-正式功能/34-角色变身/AAAAA-role_transform_ui.py`
- Test: `05-正式功能/34-角色变身/test_role_transform_static.py`

- [ ] **Step 1: Remove probe and persistent toggle configuration**

Delete `BooleanVar`, `DEFAULT_CONFIG`, `desired_probe`, `toggle_probe`, `has_transform_target`, and role toggle rendering. Keep the background process connection, queue, RPC lock, status display, logging and safe unload behavior.

- [ ] **Step 2: Add four fixed action buttons**

Use this fixed mapping and dispatch each button through the standard `trigger` RPC:

```python
ROLE_ACTIONS = {
    "local_hero": "本地玩家：选择英雄",
    "local_terminator": "本地玩家：选择超级终结者",
    "bot_hero": "所有 Bot：随机英雄",
    "bot_terminator": "所有 Bot：随机超级终结者",
}

def trigger_action(self, action):
    if self.connected:
        self._run_rpc("trigger", action)
    else:
        self.connection_label.configure(text="等待连接游戏后执行变身...")
        self._schedule_connect()
```

On connection, call `enable` once with no configuration object.

- [ ] **Step 3: Update UI static assertions**

Assert all four labels and `trigger_action` exist; assert `toggle_probe`, `BooleanVar`, `probe_button`, and `desired_probe` do not exist.

- [ ] **Step 4: Run Python compile and the complete static suite**

Run:

```powershell
python -m py_compile "05-正式功能\34-角色变身\AAAAA-role_transform_ui.py"
python -m unittest "05-正式功能\34-角色变身\test_role_transform_static.py" -v
```

Expected: both commands exit 0 and every unittest passes.

### Task 4: Verify the whole single-feature deliverable

**Files:**
- Verify: `05-正式功能/34-角色变身/AAAAA-role_transform_min.js`
- Verify: `05-正式功能/34-角色变身/AAAAA-role_transform_ui.py`
- Verify: `05-正式功能/34-角色变身/test_role_transform_static.py`

- [ ] **Step 1: Run all automated checks from a clean command invocation**

```powershell
node --check "05-正式功能\34-角色变身\AAAAA-role_transform_min.js"
python -m py_compile "05-正式功能\34-角色变身\AAAAA-role_transform_ui.py"
python -m unittest "05-正式功能\34-角色变身\test_role_transform_static.py" -v
```

Expected: all commands exit 0.

- [ ] **Step 2: Inspect the final diff and worktree scope**

Confirm the implementation diff is limited to the three feature files plus the approved plan, and report unrelated pre-existing changes separately.

- [ ] **Step 3: Commit only the implementation scope**

```powershell
git commit --only -m "feat: implement main-thread role transform actions" -- \
  "05-正式功能/34-角色变身/AAAAA-role_transform_min.js" \
  "05-正式功能/34-角色变身/AAAAA-role_transform_ui.py" \
  "05-正式功能/34-角色变身/test_role_transform_static.py" \
  "04-正式发行版/docs/superpowers/plans/2026-08-02-role-transform.md"
```

- [ ] **Step 4: Hand off game-only acceptance checks**

Report that automated checks cannot prove in-game UI rendering or runtime pointer validity. Provide the exact four-button game test plus repeat enable/disable, death/respawn, room change and cleanup checks.
