# 高跳空中移动只读探针 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe` 创建一个自动等待游戏进程、只读附加并生成结构化日志的 Frida 诊断工具。

**Architecture:** 使用一个 Python 启动器枚举本地进程并附加唯一的 `UnityCrossFire` 目标；它将一个只读 JavaScript 观察脚本加载到该会话。Python 端把来自脚本的结构化事件写入 JSONL，并在结束时从已记录数据生成摘要 JSON；JavaScript 端只安装观察 Hook 和读取状态字段。

**Tech Stack:** Python 3、Frida Python API、Frida JavaScript API、unittest、JSON Lines。

---

## File Structure

- `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.py` — 命令行入口、进程等待/附加、日志写入与会话摘要。
- `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.js` — 仅在目标游戏内执行的只读 Hook 与字段快照。
- `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py` — 不附加真实进程的 Python 单元测试。
- `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\README.md` — 使用步骤、只读承诺、2.4/2.5 测试流程与日志说明。
- `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\logs\` — 运行时自动创建的 JSONL 与摘要文件；不纳入版本控制。

### Task 1: 建立可测试的日志命名与摘要统计

**Files:**
- Create: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py`
- Create: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.py`

- [ ] **Step 1: Write the failing test**

```python
from gravity_airmove_probe import SessionSummary, build_log_paths


def test_build_log_paths_separates_label_and_timestamp(tmp_path):
    events_path, summary_path = build_log_paths(tmp_path, "2.5", "20260902_180000")
    assert events_path.name == "gravity_airmove_2.5_20260902_180000.jsonl"
    assert summary_path.name == "gravity_airmove_2.5_20260902_180000_summary.json"


def test_summary_counts_airborne_and_horizontal_motion_samples():
    summary = SessionSummary(label="2.5")
    summary.observe({"type": "player_snapshot", "grounded": False})
    summary.observe({"type": "controller_move", "vector_readable": True})
    summary.observe({"type": "probe_error", "message": "sample"})
    assert summary.to_dict()["airborne_samples"] == 1
    assert summary.to_dict()["readable_horizontal_moves"] == 1
    assert summary.to_dict()["errors"] == 1
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: FAIL because `gravity_airmove_probe` does not exist.

- [ ] **Step 3: Write minimal implementation**

Implement `build_log_paths(directory, label, timestamp)` with strict labels `2.4` and `2.5`, and a `SessionSummary` dataclass that counts only `player_snapshot`, readable `controller_move`, and `probe_error` events. `to_dict()` must include the label and counters.

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: PASS for both tests.

### Task 2: 实现自动等待、只读附加与事件落盘

**Files:**
- Modify: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py`
- Modify: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.py`
- Create: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.js`

- [ ] **Step 1: Write the failing test**

```python
from gravity_airmove_probe import choose_target


def test_choose_target_returns_only_unitycrossfire_process():
    processes = [
        {"pid": 100, "name": "UCF2.4修改器.exe"},
        {"pid": 200, "name": "UnityCrossFire.exe"},
    ]
    assert choose_target(processes) == {"pid": 200, "name": "UnityCrossFire.exe"}


def test_choose_target_rejects_ambiguous_game_processes():
    processes = [
        {"pid": 200, "name": "UnityCrossFire.exe"},
        {"pid": 201, "name": "UnityCrossFire-Test.exe"},
    ]
    assert choose_target(processes) is None
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: FAIL because `choose_target` does not exist.

- [ ] **Step 3: Write minimal implementation**

Implement `choose_target` as a case-insensitive name match for `unitycrossfire`, returning a target only when exactly one process matches. The command-line entry point must poll once per second, log `waiting_for_game`, attach through `frida.get_local_device().attach(pid)`, load the JavaScript source, and write every script `send` payload as one JSON object per JSONL line. It must detach in `finally` and write the summary JSON even after Ctrl+C or attach failure.

The JavaScript must use `Process.findModuleByName('GameAssembly.dll')`; if missing, it emits a `probe_error` event and installs nothing. It may only use `Interceptor.attach`, pointer/read methods, `send`, timers, and `console`-free helpers. It must not contain `write`, `replace`, `NativeCallback`, or calls to the modifier RPC interface.

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: PASS for all four tests.

### Task 3: 实现最小只读移动观测

**Files:**
- Modify: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.js`
- Modify: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path


def test_probe_script_has_only_readonly_operations():
    source = Path(__file__).with_name("gravity_airmove_probe.js").read_text(encoding="utf-8").lower()
    assert "interceptor.attach" in source
    assert "readu8" in source
    assert "readfloat" in source
    assert ".write" not in source
    assert "interceptor.replace" not in source
    assert "nativecallback" not in source
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: FAIL until the observation script provides the required read-only primitives.

- [ ] **Step 3: Write minimal implementation**

Attach read-only hooks at `GameAssembly.base + 0xB50A00` and `GameAssembly.base + 0xAB8210`. Capture a local-player candidate only after calling the existing `Player.get_isMyPlayer` function at `base + 0xB55FD0` returns true; never call game movement functions.

For the captured player, sample no more than every 100 ms: `+0x70` as unsigned byte, `+0x88` as float, and pointer `+0x90` then its `+0x10` float. For `CharacterController.Move`, attempt X/Y/Z reads only after `args[1]` is confirmed readable as 12 bytes; otherwise emit an unreadable move event with the raw argument address. Rate-limit move events to one each 50 ms. All memory reads must be wrapped in `try/catch` and emit `probe_error` rather than throw.

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: PASS, proving the probe source contains only its allowed observation mechanisms.

### Task 4: 写入使用说明并进行离线验证

**Files:**
- Create: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\README.md`
- Modify: `D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path


def test_readme_documents_two_version_comparison_workflow():
    text = Path(__file__).with_name("README.md").read_text(encoding="utf-8")
    assert "2.4" in text
    assert "2.5" in text
    assert "只读" in text
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: FAIL because `README.md` does not exist.

- [ ] **Step 3: Write minimal implementation**

Document the exact commands:

```powershell
python .\gravity_airmove_probe.py --label 2.4
python .\gravity_airmove_probe.py --label 2.5
```

Document the identical reproduction sequence for both versions: only enable high jump, walk on ground, jump, hold W, hold A, hold S, hold D, land, stop the probe. Include the log location and state that missing `controller_move` events are evidence rather than an automatic failure.

- [ ] **Step 4: Run test to verify it passes**

Run:

```powershell
python -m unittest D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\test_gravity_airmove_probe.py -v
```

Expected: PASS for all tests.

- [ ] **Step 5: Perform static safety verification**

Run:

```powershell
Select-String -LiteralPath D:\trae_project\ucf1.7-modifier\06-测试\gravity_airmove_probe\gravity_airmove_probe.js -Pattern 'write|replace|NativeCallback|rpc' -CaseSensitive:$false
```

Expected: no matches.

