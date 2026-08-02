# 32/33 功能接入整合包 2.4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将亮度调节探针和玩家信息修改器迁移为整合包 2.4 的普通功能卡片，并放入 `game_parameters_tab`。

**Architecture:** 32 号沿用 2.4 的 Frida/RPC 插件链路，以自定义普通卡片 panel 承载多个参数控件；33 号沿用同一普通卡片 UI，但通过 `plugin_feature` 动作调用本地文件 service，不连接游戏。只扩展 ActionRouter 的 payload 透传，不新建独立 UI 子系统。

**Tech Stack:** Python 3.12, CustomTkinter, Frida JavaScript RPC, JSON manifest, unittest, Node.js syntax check, PyInstaller spec.

---

### Task 1: 建立 32/33 插件目录和迁移测试

**Files:**
- Create: `全功能整合包2.4/game_modifier/features/32_brightness_probe/script.js`
- Create: `全功能整合包2.4/game_modifier/features/32_brightness_probe/test_brightness_probe_static.py`
- Create: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/player_profile_service.py`
- Create: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/test_player_profile_service.py`

- [ ] **Step 1: Copy source runtime and service into the 2.4 feature directories**

Copy the source brightness runtime unchanged as the initial migration baseline, rename it to `script.js`, and copy the player profile service and its service tests into the corresponding 2.4 directory. Do not copy standalone UI entrypoints or `pyi_tcl_runtime_hook.py`.

- [ ] **Step 2: Run the migrated tests before integration changes**

Run:

```powershell
python -m unittest "全功能整合包2.4\game_modifier\features\33_player_profile_editor\test_player_profile_service.py" -v
python -m unittest "全功能整合包2.4\game_modifier\features\32_brightness_probe\test_brightness_probe_static.py" -v
```

Expected: the player service tests pass; the brightness static test either passes or identifies source assumptions that must be changed for 2.4.

### Task 2: Add failing tests for plugin discovery and local action payloads

**Files:**
- Create: `全功能整合包2.4/game_modifier/features/32_brightness_probe/manifest.json`
- Create: `全功能整合包2.4/game_modifier/features/32_brightness_probe/feature.py`
- Create: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/manifest.json`
- Create: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/feature.py`
- Create: `全功能整合包2.4/game_modifier/features/test_feature_32_33_integration.py`
- Modify: `全功能整合包2.4/game_modifier/ui/controllers/action_router.py`

- [ ] **Step 1: Write a failing integration test for manifests**

The test must load both manifests through `ManifestLoader`, assert `feature_id`, `tab == "game_parameters_tab"`, required manifest fields, and assert that 32 declares the brightness RPC names while 33 declares local `load_profile` and `save_profile` actions with `requires_connection: false`.

- [ ] **Step 2: Run the integration test and confirm the expected failure**

Run:

```powershell
python -m unittest "全功能整合包2.4\game_modifier\features\test_feature_32_33_integration.py" -v
```

Expected: FAIL because the new manifests and plugin metadata do not yet exist.

- [ ] **Step 3: Add minimal manifests and feature classes**

Use `feature_id` values `brightness_probe` and `player_profile_editor`, set `tab` to `game_parameters_tab`, set both layouts to `card_type: wide` and `columnspan: 2`, and make 33’s actions use `type: plugin_feature` and `requires_connection: false`. Implement 33’s feature methods so `load_profile(payload)` returns loaded values and `save_profile(payload)` validates and saves through the copied service.

- [ ] **Step 4: Extend ActionRouter payload forwarding minimally**

Change `_call_plugin_feature(self, feature_id, action)` to accept `payload=None`, call plugin methods as `method(payload or {})` when the action is a local plugin action, and preserve compatibility with zero-argument plugin methods by retrying `method()` only on a `TypeError` caused by the signature. Update the call site in `action()` to pass the payload.

- [ ] **Step 5: Run the integration test and verify it passes**

Run the same unittest command. Expected: PASS with no unrelated RPC calls; 33 local actions must succeed with a temporary file and no active game connection.

### Task 3: Build the 32 brightness ordinary card

**Files:**
- Create: `全功能整合包2.4/game_modifier/features/32_brightness_probe/panel.py`
- Modify: `全功能整合包2.4/game_modifier/features/32_brightness_probe/manifest.json`
- Modify: `全功能整合包2.4/game_modifier/features/32_brightness_probe/feature.py`
- Modify: `全功能整合包2.4/game_modifier/features/32_brightness_probe/test_brightness_probe_static.py`

- [ ] **Step 1: Add failing static assertions for 2.4 RPC and panel behavior**

Assert that the script exports `setconfig`, `enable`, `applybrightness`, `resetbrightness`, `status`, and `cleanup`; the panel exposes five sliders, the post-processing switch, apply/reset buttons; and the manifest uses the 2.4 tab and config keys.

- [ ] **Step 2: Run the static test and confirm it fails for missing panel/manifest wiring**

Run:

```powershell
python -m unittest "全功能整合包2.4\game_modifier\features\32_brightness_probe\test_brightness_probe_static.py" -v
```

- [ ] **Step 3: Implement the custom ordinary-card panel**

Build a wide `customtkinter` card with five synchronized sliders, a force-post-processing switch, a status label, and apply/reset buttons. Use `callbacks["set_config"]` for individual values and `callbacks["action"]` for RPC actions. Apply must call `setconfig` followed by `applybrightness` through the existing action sequence contract; reset must call `resetbrightness`. Keep handle names in manifest for state synchronization.

- [ ] **Step 4: Make the feature metadata match the panel**

Declare defaults and ranges exactly as the source UI, include `lifecycle.restore: false`, include all RPC names, and mark apply/reset actions as requiring a connection. Keep the probe under `game_parameters_tab` with an order after existing 31.

- [ ] **Step 5: Run the brightness static test and the Python compile check**

Run:

```powershell
python -m unittest "全功能整合包2.4\game_modifier\features\32_brightness_probe\test_brightness_probe_static.py" -v
python -m compileall -q "全功能整合包2.4\game_modifier\features\32_brightness_probe"
```

Expected: PASS and exit code 0.

### Task 4: Build the 33 player profile ordinary card

**Files:**
- Create: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/panel.py`
- Modify: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/manifest.json`
- Modify: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/feature.py`
- Modify: `全功能整合包2.4/game_modifier/features/33_player_profile_editor/test_player_profile_service.py`

- [ ] **Step 1: Add failing panel/service assertions**

Add tests for the local plugin actions using a temporary `PlayerData.dat`, asserting that save does not create a backup and that invalid nickname/negative values return a validation error without modifying the file.

- [ ] **Step 2: Run the new tests and confirm they fail before panel integration**

Run:

```powershell
python -m unittest "全功能整合包2.4\game_modifier\features\33_player_profile_editor\test_player_profile_service.py" -v
```

- [ ] **Step 3: Implement the card panel**

Build a wide card with path entry, browse button, read button, nickname/level/VIP entries, save button, and status/log label. Read and save invoke the feature action callback with payloads containing `path`, `nickname`, `level`, and `vip_level`; neither action checks game connection. Display the source warning that the game may overwrite external changes while running.

- [ ] **Step 4: Verify the player profile tests**

Run the player service and integration test commands. Expected: all tests pass and no test writes to the real user profile path.

### Task 5: Update persistence records, packaging, and docs

**Files:**
- Modify: `全功能整合包2.4/game_modifier/game_modifier.spec`
- Create: `全功能整合包2.4/32-33功能接入说明.md`

- [ ] **Step 1: Add a failing packaging/discovery check**

Assert that the PyInstaller spec includes `features/32_brightness_probe` and `features/33_player_profile_editor`, and excludes standalone UI entrypoint files and test files from collected runtime assets.

- [ ] **Step 2: Update the spec and add the 2.4 integration note**

Add the two plugin directories to the same data collection mechanism used by features 30/31. Record 32 parameters as `user_config.json` values with restore disabled; record 33 as local file state with no feature switch persistence. Create `全功能整合包2.4/32-33功能接入说明.md` with usage, no-backup behavior, restart-to-apply guidance, and the manual in-game validation boundary.

- [ ] **Step 3: Run manifest, package-config, and encoding checks**

Run:

```powershell
python -m unittest discover -s "全功能整合包2.4\game_modifier\features" -p "test_*.py" -v
node --check "全功能整合包2.4\game_modifier\features\32_brightness_probe\script.js"
python -m compileall -q "全功能整合包2.4\game_modifier"
```

Expected: all tests pass, Node syntax check exits 0, and compileall exits 0.

### Task 6: Final verification

**Files:**
- Verify all files changed by Tasks 1–5.

- [ ] **Step 1: Inspect the final diff and status**

Run `git diff --stat`, `git diff --check`, and `git status --short`; confirm only the requested 2.4 feature integration, docs, and the minimal router change are present, while pre-existing user changes remain untouched.

- [ ] **Step 2: Run the complete verification suite**

Run the exact test, syntax, compile, and packaging checks from Tasks 2–5 in one fresh verification pass.

- [ ] **Step 3: Report evidence and remaining manual check**

Report test counts and exit codes. Clearly separate automated integration success from the manual in-game check required to confirm that the brightness probe changes the rendered image and that PlayerData changes persist after the game reloads.
