# 角色变身接入整合包 2.5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将角色变身四个即时动作作为独立内嵌卡片接入整合包 2.5 的“多人生化”页。

**Architecture:** 新插件 `features/34_role_transform` 自包含 Frida 脚本、manifest、插件壳和 UI 卡片。按钮通过通用 `callbacks["action"]` 调用 `trigger(action)`；`trigger` 首次调用时惰性安装 `ModeBase.Update` Hook，再由游戏主线程消费一次性动作。插件只使用现有 `special_inline_card` 扩展点，不修改 Buff、决战回合或中心文件。

**Tech Stack:** Python 3、CustomTkinter、Frida JavaScript、JSON manifest、标准库 unittest、Node.js 语法检查。

---

## 文件职责

- `features/34_role_transform/script.js`：角色变身游戏逻辑、惰性初始化、主线程动作队列和标准 RPC。
- `features/34_role_transform/manifest.json`：插件发现、页签位置、四个动作、RPC 和生命周期声明。
- `features/34_role_transform/feature.py`：最小 `PluginFeatureBase` 插件壳。
- `features/34_role_transform/panel.py`：四按钮内嵌卡片，只使用通用 callbacks。
- `features/34_role_transform/events.py`：空的功能级事件入口。
- `features/34_role_transform/test_role_transform_integration.py`：接入契约与源码静态测试。
- `02-开发规范/20-整合包接入/22-功能开关与参数持久化记录.md`：记录四个按钮不持久化、不自动重放。

### Task 1: 用失败测试固定插件契约

**Files:**
- Create: `全功能整合包2.5/game_modifier/features/34_role_transform/test_role_transform_integration.py`

- [ ] **Step 1: 创建失败测试**

测试读取同目录文件并断言：manifest 使用 `role_transform`、`nano4t_tab`、`special_inline_card`、四个 `trigger` payload、`restore=false`；panel 只通过 `callbacks["action"]`；JS 保留四个动作、主线程 pending 队列和关键 RVA，并支持按钮首次调用时初始化。

```python
class RoleTransformIntegrationTests(unittest.TestCase):
    def test_manifest_declares_inline_one_shot_actions(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual("role_transform", manifest["feature_id"])
        self.assertEqual("nano4t_tab", manifest["tab"])
        self.assertEqual("special_inline_card", manifest["ui"]["mode"])
        self.assertFalse(manifest["lifecycle"]["restore"])
        self.assertFalse(manifest["state"]["sync_enabled_from_config"])
        self.assertEqual(
            {"local_hero", "local_terminator", "bot_hero", "bot_terminator"},
            {item["payload"]["action"] for item in manifest["controls"]},
        )

    def test_trigger_lazy_enables_before_queueing(self):
        script = SCRIPT.read_text(encoding="utf-8")
        body = script.split("function queueAction", 1)[1].split("function status", 1)[0]
        self.assertIn("enableFeature()", body)
        self.assertIn("Runtime.pendingAction = action", body)
```

- [ ] **Step 2: 运行测试确认 RED**

Run: `python -m unittest "features\34_role_transform\test_role_transform_integration.py" -v`

Expected: FAIL，因为插件目录与文件尚不存在。

### Task 2: 建立插件壳并完整复制核心 JS

**Files:**
- Create: `全功能整合包2.5/game_modifier/features/34_role_transform/__init__.py`
- Create: `全功能整合包2.5/game_modifier/features/34_role_transform/feature.py`
- Create: `全功能整合包2.5/game_modifier/features/34_role_transform/events.py`
- Create: `全功能整合包2.5/game_modifier/features/34_role_transform/script.js`

- [ ] **Step 1: 创建最小 Python 插件壳**

```python
# feature.py
from core.plugin.plugin_base import PluginFeatureBase


class PluginFeature(PluginFeatureBase):
    pass
```

```python
# events.py
def handle_event(context, event, payload):
    """角色变身当前不消费插件事件。"""
    return None
```

- [ ] **Step 2: 将单功能 JS 完整复制为 script.js**

源：`05-正式功能/34-角色变身/AAAAA-role_transform_min.js`

目标：`全功能整合包2.5/game_modifier/features/34_role_transform/script.js`

复制后先校验内容哈希一致，再进行 Task 3 的最小适配。

- [ ] **Step 3: 运行源码契约测试**

Run: `node --check features/34_role_transform/script.js`

Expected: PASS。

### Task 3: 适配一次性按钮的惰性初始化

**Files:**
- Modify: `全功能整合包2.5/game_modifier/features/34_role_transform/script.js`
- Test: `全功能整合包2.5/game_modifier/features/34_role_transform/test_role_transform_integration.py`

- [ ] **Step 1: 修改 queueAction，使首次按钮调用自动初始化**

在动作名校验后执行惰性 enable；失败时保留结构化 rejected 状态：

```javascript
function queueAction(actionOrPayload) {
    var action = typeof actionOrPayload === 'string'
        ? actionOrPayload
        : actionOrPayload && actionOrPayload.action;
    if (!VALID_ACTIONS[action]) {
        reject('unknown action: ' + action);
        return status();
    }
    if (!Runtime.enabled || !Runtime.initialized) {
        enableFeature();
    }
    if (!Runtime.enabled || !Runtime.initialized) {
        reject('feature initialization failed');
        return status();
    }
    if (Runtime.pendingAction) {
        reject('another action is pending');
        return status();
    }
    Runtime.pendingAction = action;
    Runtime.stats.requests += 1;
    Runtime.stats.last_action = action;
    Runtime.stats.last_result = 'queued';
    return status();
}
```

- [ ] **Step 2: 让 cleanup 接受整合包 payload**

```javascript
function cleanupFeature(_payload) {
    Runtime.stats.cleanup_count += 1;
    resetRuntime('cleanup');
    return status();
}
```

- [ ] **Step 3: 运行 JS 与测试确认 GREEN**

Run: `node --check features/34_role_transform/script.js`

Run: `python -m unittest "features\34_role_transform\test_role_transform_integration.py" -v`

Expected: 与 JS 相关的测试通过；manifest/panel 测试仍因文件缺失失败。

### Task 4: 创建 manifest 和四按钮内嵌卡片

**Files:**
- Create: `全功能整合包2.5/game_modifier/features/34_role_transform/manifest.json`
- Create: `全功能整合包2.5/game_modifier/features/34_role_transform/panel.py`
- Test: `全功能整合包2.5/game_modifier/features/34_role_transform/test_role_transform_integration.py`

- [ ] **Step 1: 创建 manifest**

关键声明如下；四个 controls 均调用同一个 RPC `trigger`，以 payload 区分动作：

```json
{
  "feature_id": "role_transform",
  "canonical_id": "role_transform",
  "display_name": "角色变身",
  "category": "special",
  "tab": "nano4t_tab",
  "tab_title": "多人生化",
  "tab_order": 40,
  "order": 60,
  "script": "script.js",
  "runtime": {"type": "plugin_script"},
  "ui": {"mode": "special_inline_card"},
  "layout": {"card_type": "wide", "columnspan": 2, "title_color": "#A855F7"},
  "controls": [
    {"type": "button", "action": "trigger", "label": "本地玩家：选择英雄", "payload": {"action": "local_hero"}},
    {"type": "button", "action": "trigger", "label": "本地玩家：选择超级终结者", "payload": {"action": "local_terminator"}},
    {"type": "button", "action": "trigger", "label": "所有 Bot：随机英雄", "payload": {"action": "bot_hero"}},
    {"type": "button", "action": "trigger", "label": "所有 Bot：随机超级终结者", "payload": {"action": "bot_terminator"}}
  ],
  "config": {},
  "rpc": ["enable", "disable", "status", "cleanup", "trigger", "setConfig", "set_config", "setconfig"],
  "actions": {"trigger": {"type": "rpc", "requires_connection": true}},
  "lifecycle": {"cleanup": true, "restore": false, "requires_room_ready_reapply": false, "room_ready_retry": false, "room_ready_reapply_exempt_reason": "四个按钮都是用户手动触发的一次性动作；无有效房间时本次失败，不跨房间重放。"},
  "state": {"sync_enabled_from_config": false}
}
```

- [ ] **Step 2: 创建 panel.py**

panel 从 manifest 读取按钮，闭包固定 payload，并只走通用 action callback：

```python
def run_action(control):
    action = control.get("action", "trigger")
    payload = dict(control.get("payload") or {})
    return callbacks["action"](feature_id, action, payload)
```

使用透明 `CTkFrame`、标题、两列按钮和说明文本；返回四个按钮 handle，不访问 App 私有字段，不 import Frida 管理器。

- [ ] **Step 3: 运行完整插件测试**

Run: `python -m unittest "features\34_role_transform\test_role_transform_integration.py" -v`

Expected: PASS。

### Task 5: 更新持久化记录并验证插件发现

**Files:**
- Modify: `02-开发规范/20-整合包接入/22-功能开关与参数持久化记录.md`
- Test: `全功能整合包2.5/game_modifier/features/34_role_transform/test_role_transform_integration.py`

- [ ] **Step 1: 在“多人生化”表格新增记录**

```markdown
| 34-角色变身 | 四个变身按钮 | 不记录动作或参数 | 不恢复 | 一次性动作，仅在用户点击时执行；无有效多人生化房间时失败，不跨房间重放。 |
```

- [ ] **Step 2: 验证 manifest loader 能发现新插件**

增加测试：调用 `ManifestLoader(ROOT.parent).load()` 扫描项目 features 路径，断言 `role_transform` 存在且 `_plugin_dir` 指向 `34_role_transform`。

- [ ] **Step 3: 运行插件发现与全套静态测试**

Run: `python -m unittest "features\34_role_transform\test_role_transform_integration.py" -v`

Expected: PASS。

### Task 6: 完整验证与范围审计

**Files:**
- Verify: `全功能整合包2.5/game_modifier/features/34_role_transform/*`
- Verify: `02-开发规范/20-整合包接入/22-功能开关与参数持久化记录.md`

- [ ] **Step 1: 运行语法与单元测试**

Run: `node --check features/34_role_transform/script.js`

Run: `python -m py_compile features/34_role_transform/feature.py features/34_role_transform/panel.py features/34_role_transform/events.py features/34_role_transform/test_role_transform_integration.py`

Run: `python -m unittest "features\34_role_transform\test_role_transform_integration.py" -v`

Expected: 所有命令退出码 0。

- [ ] **Step 2: 运行项目相关插件测试**

Run: `python -m unittest discover -s features -p "test_*.py" -v`

Expected: 全部通过；若发现与本功能无关的既有失败，记录准确用例和错误，不修改无关功能。

- [ ] **Step 3: 审计 Git 范围**

Run: `git diff --check`

Run: `git status --short`

Expected: 本功能新增仅位于 `34_role_transform`；开发规范仅新增一行；`15_nano4t`、`19_battle_round` 和中心文件没有因本功能发生变化。用户原有未提交改动保持原样。

- [ ] **Step 4: 交付游戏内验收清单**

在游戏中确认：卡片出现在“多人生化”页且不影响 Buff/决战回合；四个按钮分别执行正确动作；快速重复点击不会覆盖 pending；切房、断线、退出清理后不重放旧动作且不崩溃。
