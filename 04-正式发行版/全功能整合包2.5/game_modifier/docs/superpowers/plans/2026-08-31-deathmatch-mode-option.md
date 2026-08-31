# 个人竞技模式选项实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在整合包 2.5 的“游戏模式切换”中完整加入原生个人竞技（DeathMatch）选项。

**Architecture:** 保持现有三层声明：`panel.py` 映射界面标签，`manifest.json` 定义配置契约，`script.js` 定义运行时模式。专项测试锁定 `个人竞技 -> death_match -> gameMode 1 / weaponLimited 0`，运行时复用现有 MapAsset、Prefab、回读校验和 Neutral 出生点兼容路径。

**Tech Stack:** Python 3、unittest、JSON、CustomTkinter 配置模块、Frida JavaScript、Node.js

---

### Task 1：建立失败的三层契约测试

**Files:**
- Create: `全功能整合包2.5/game_modifier/features/27_game_mode_override/test_deathmatch_mode_option.py`
- Test: `全功能整合包2.5/game_modifier/features/27_game_mode_override/test_deathmatch_mode_option.py`

- [ ] **Step 1：新增专项测试**

```python
import importlib.util
import json
import re
import sys
import types
import unittest
from pathlib import Path

FEATURE_DIR = Path(__file__).parent
PANEL_PATH = FEATURE_DIR / "panel.py"
MANIFEST_PATH = FEATURE_DIR / "manifest.json"
SCRIPT_PATH = FEATURE_DIR / "script.js"

def load_panel_module():
    sys.modules.setdefault("customtkinter", types.SimpleNamespace())
    spec = importlib.util.spec_from_file_location("game_mode_override_panel_under_test", PANEL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class DeathmatchModeOptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.panel = load_panel_module()
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.script = SCRIPT_PATH.read_text(encoding="utf-8")
        cls.mode_control = next(
            control for control in cls.manifest["controls"]
            if control.get("key") == "mode_key"
        )

    def test_panel_exposes_personal_competition(self):
        self.assertEqual(self.panel.MODE_OPTIONS["个人竞技"], "death_match")

    def test_manifest_declares_death_match(self):
        self.assertIn("death_match", self.mode_control["values"])
        self.assertEqual(self.mode_control["display_values"]["death_match"], "个人竞技")

    def test_script_maps_death_match_to_native_mode(self):
        pattern = re.compile(
            r"death_match\s*:\s*\{\s*label\s*:\s*'个人竞技'\s*,\s*"
            r"gameMode\s*:\s*1\s*,\s*weaponLimited\s*:\s*0\s*\}",
            re.MULTILINE,
        )
        self.assertRegex(self.script, pattern)

    def test_panel_and_manifest_mode_keys_stay_in_sync(self):
        self.assertEqual(
            set(self.panel.MODE_OPTIONS.values()),
            set(self.mode_control["values"]),
        )

if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2：运行测试并确认 RED**

Run: `python -m unittest features/27_game_mode_override/test_deathmatch_mode_option.py -v`

Expected: 三个个人竞技声明测试因功能缺失而失败；测试文件本身无语法或导入错误。

### Task 2：完成最小三层实现

**Files:**
- Modify: `全功能整合包2.5/game_modifier/features/27_game_mode_override/panel.py`
- Modify: `全功能整合包2.5/game_modifier/features/27_game_mode_override/manifest.json`
- Modify: `全功能整合包2.5/game_modifier/features/27_game_mode_override/script.js`
- Test: `全功能整合包2.5/game_modifier/features/27_game_mode_override/test_deathmatch_mode_option.py`

- [ ] **Step 1：在 `MODE_OPTIONS` 的团队竞技后增加界面映射**

```python
"团队竞技": "team_death",
"个人竞技": "death_match",
"刀战": "special",
```

- [ ] **Step 2：在 manifest 的 `values` 中把 `death_match` 放在 `team_death` 后**

```json
"values": [
  "team_death",
  "death_match",
  "special",
  "nano4",
  "nano6",
  "nano4_terminator",
  "sniper",
  "handgun"
]
```

- [ ] **Step 3：在 manifest 的 `display_values` 中增加显示名称**

```json
"team_death": "团队竞技",
"death_match": "个人竞技",
"special": "刀战"
```

- [ ] **Step 4：在脚本 `MODES` 的团队竞技后增加原生模式定义**

```javascript
death_match: { label: '个人竞技', gameMode: 1, weaponLimited: 0 },
```

- [ ] **Step 5：运行专项测试并确认 GREEN**

Run: `python -m unittest features/27_game_mode_override/test_deathmatch_mode_option.py -v`

Expected: `Ran 4 tests`，`OK`。

- [ ] **Step 6：检查实现差异**

Run: `git diff --check -- features/27_game_mode_override/panel.py features/27_game_mode_override/manifest.json features/27_game_mode_override/script.js features/27_game_mode_override/test_deathmatch_mode_option.py`

Expected: exit code 0，无空白错误。

### Task 3：专项与回归验证

**Files:**
- Verify: `全功能整合包2.5/game_modifier/features/27_game_mode_override/test_deathmatch_mode_option.py`
- Verify: `全功能整合包2.5/game_modifier/features/27_game_mode_override/manifest.json`
- Verify: `全功能整合包2.5/game_modifier/features/27_game_mode_override/script.js`

- [ ] **Step 1：执行功能目录测试发现**

Run: `python -m unittest discover -s features/27_game_mode_override -p "test_*.py" -v`

Expected: 0 failures，0 errors。

- [ ] **Step 2：执行整合包 2.5 项目测试发现**

Run: `python -m unittest discover -s . -p "test_*.py" -v`

Expected: 所有可发现测试通过；任何既有环境性失败需完整记录，不能误报。

- [ ] **Step 3：验证 JSON 和模式键唯一性**

Run: `python -c "import json,pathlib; d=json.loads(pathlib.Path('features/27_game_mode_override/manifest.json').read_text(encoding='utf-8')); c=next(x for x in d['controls'] if x.get('key')=='mode_key'); assert len(c['values'])==len(set(c['values'])); assert c['display_values']['death_match']=='个人竞技'; print('MANIFEST_OK',len(c['values']))"`

Expected: `MANIFEST_OK 8`。

- [ ] **Step 4：验证 JavaScript 语法**

Run: `node --check features/27_game_mode_override/script.js`

Expected: exit code 0，无语法错误。

- [ ] **Step 5：最终差异审查**

Run: `git diff --check`，然后运行 `git status --short` 并审阅上述四个实现/测试文件的 diff。

Expected: 无意外修改，无空白错误。

### Task 4：提交实现

**Files:**
- Commit: `全功能整合包2.5/game_modifier/features/27_game_mode_override/panel.py`
- Commit: `全功能整合包2.5/game_modifier/features/27_game_mode_override/manifest.json`
- Commit: `全功能整合包2.5/game_modifier/features/27_game_mode_override/script.js`
- Commit: `全功能整合包2.5/game_modifier/features/27_game_mode_override/test_deathmatch_mode_option.py`

- [ ] **Step 1：只暂存四个实现/测试文件并提交**

```powershell
git add -- features/27_game_mode_override/panel.py features/27_game_mode_override/manifest.json features/27_game_mode_override/script.js features/27_game_mode_override/test_deathmatch_mode_option.py
git commit -m "feat: add personal competition mode option"
```

- [ ] **Step 2：确认提交内容**

Run: `git show --stat --oneline --summary HEAD`，然后运行 `git status --short`。

Expected: 新提交只包含上述四个文件，工作区没有本任务遗留的未提交实现改动。
