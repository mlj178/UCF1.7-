# Hide Room Player Count and Non-destructive Release Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Hide the 2.5 room-player-count card without removing its implementation, then build a separately named EXE installer without altering prior release artifacts.

**Architecture:** The feature manifest declares that its UI is not visible. The shared card builder respects that declaration before allocating grid space, while plugin discovery and runtime code remain unchanged. A dedicated packaging script uses timestamped build, distribution, and installer output folders; the Inno Setup script accepts optional source/output directory defines while retaining its current defaults.

**Tech Stack:** Python 3 `unittest`, CustomTkinter plugin UI, PowerShell, PyInstaller, Inno Setup.

---

### Task 1: Add and verify the UI visibility contract

**Files:**
- Modify: `全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`
- Modify: `全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json`
- Modify: `全功能整合包2.5/game_modifier/ui/pages/plugin_feature_page.py`

- [ ] **Step 1: Write the failing tests**

```python
def test_manifest_marks_room_count_as_not_visible_in_ui(self):
    manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))
    self.assertFalse(manifest["ui"]["visible"])

def test_plugin_page_skips_features_explicitly_hidden_from_ui(self):
    page = FEATURE_DIR.parents[2] / "ui" / "pages" / "plugin_feature_page.py"
    self.assertIn('if manifest.get("ui", {}).get("visible", True) is False:', page.read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run the test and verify it fails**

Run: `python -m unittest features.35_room_player_count.test_room_player_count_static -v`

Expected: failure because the manifest has no `ui.visible` property and the shared page has no visibility guard.

- [ ] **Step 3: Write the minimal implementation**

```json
"ui": { "visible": false }
```

```python
if manifest.get("ui", {}).get("visible", True) is False:
    continue
```

- [ ] **Step 4: Run the test and verify it passes**

Run: `python -m unittest features.35_room_player_count.test_room_player_count_static -v`

Expected: all room-player-count static tests pass.

### Task 2: Add a non-destructive installer build path

**Files:**
- Modify: `全功能整合包2.5/game_modifier/packaging/test_build_release_static.py`
- Modify: `全功能整合包2.5/game_modifier/packaging/installer.iss`
- Create: `全功能整合包2.5/game_modifier/packaging/build_release_non_destructive.ps1`

- [ ] **Step 1: Write failing static tests**

```python
def test_installer_accepts_overridable_build_and_release_directories(self):
    self.assertIn('#ifndef BuildDistDir', INSTALLER_SCRIPT)
    self.assertIn('#ifndef ReleaseOutputDir', INSTALLER_SCRIPT)

def test_non_destructive_builder_uses_timestamped_output_and_never_removes_prior_release_dirs(self):
    self.assertIn('Get-Date -Format "yyyyMMdd-HHmmss"', text)
    self.assertNotIn('Remove-Item', text)
```

- [ ] **Step 2: Run the packaging static test and verify it fails**

Run: `python -m unittest packaging.test_build_release_static -v`

Expected: failure because neither optional installer defines nor the dedicated script exist.

- [ ] **Step 3: Implement optional installer paths and the dedicated builder**

The Inno script keeps `..\\dist_release` and `..\\release` as defaults but uses `BuildDistDir` and `ReleaseOutputDir` when supplied. The new PowerShell script creates timestamped `build_hidden_room_count_*`, `dist_hidden_room_count_*`, and `release_hidden_room_count_*` folders, invokes PyInstaller and Inno Setup with those paths, and emits SHA-256 and README alongside the installer. It must never call `Remove-Item`.

- [ ] **Step 4: Run the packaging static test and verify it passes**

Run: `python -m unittest packaging.test_build_release_static -v`

Expected: all packaging static tests pass.

### Task 3: Build and inspect the isolated installer output

**Files:**
- Verify: generated timestamped `release_hidden_room_count_*` folder and installer

- [ ] **Step 1: Run the dedicated builder**

Run: `powershell -ExecutionPolicy Bypass -File packaging\\build_release_non_destructive.ps1`

Expected: PyInstaller and Inno Setup both exit zero; an installer, SHA256.txt, and README.txt exist in a new timestamped release directory.

- [ ] **Step 2: Verify packaged UI data**

Run: inspect `_internal/features/35_room_player_count/manifest.json` and `_internal/ui/pages/plugin_feature_page.py` in the new timestamped distribution output.

Expected: manifest has `ui.visible: false`; shared builder has the visibility guard; `script.js`, `panel.py`, and `feature.py` are present.

- [ ] **Step 3: Verify prior artifacts were preserved**

Run: compare existence and hashes/timestamps of pre-existing `release/UCF2.5修改器安装器.exe` and `dist_release/UCF2.5修改器` before and after build.

Expected: existing paths remain present and unchanged; only timestamped paths were created.
