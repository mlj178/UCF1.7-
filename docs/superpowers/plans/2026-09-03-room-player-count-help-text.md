# 全模式房间人数说明文字 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用无标题前缀、可在卡片内换行的说明替换房间人数卡片当前说明。

**Architecture:** 清单作为正式说明的单一来源，面板从清单读取该说明；面板默认说明与清单保持一致。将标签的 `wraplength` 调整为 250，保留现有边距、字体和操作逻辑。

**Tech Stack:** Python 3、CustomTkinter、JSON、`unittest`。

---

### Task 1: 为说明文字建立失败测试

**Files:**
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`
- Test: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`

- [ ] **Step 1: 添加说明和换行宽度测试**

```python
def test_help_text_is_short_and_wraps_inside_the_card(self):
    manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))
    panel = (FEATURE_DIR / "panel.py").read_text(encoding="utf-8")
    expected = "开启后，设置人数并点击“应用人数”。下一局生效；关闭后恢复默认人数。"

    self.assertEqual(expected, manifest["desc"])
    self.assertNotIn("功能说明：", manifest["desc"])
    self.assertIn("wraplength=250", panel)
    self.assertIn(expected, panel)
```

- [ ] **Step 2: 运行测试，确认旧说明失败**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static.RoomPlayerCountStaticTests -v`

Expected: FAIL，因为现有说明含“功能说明：”，且换行宽度为 280。

- [ ] **Step 3: 提交失败测试**

```bash
git add -- "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py"
git commit -m "test: define room player count help text bounds"
```

### Task 2: 应用简洁说明与安全换行宽度

**Files:**
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json:10`
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/panel.py:130-137`
- Test: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`

- [ ] **Step 1: 用确定的用户说明替换清单描述**

```json
"desc": "开启后，设置人数并点击“应用人数”。下一局生效；关闭后恢复默认人数。"
```

- [ ] **Step 2: 更新面板默认文本并缩短换行宽度**

```python
help_text = manifest.get(
    "desc",
    "开启后，设置人数并点击“应用人数”。下一局生效；关闭后恢复默认人数。",
)
ctk.CTkLabel(frame, text=help_text, font=("Microsoft YaHei", 12),
             text_color="#a0a0a0", wraplength=250, justify="left", anchor="w"
             ).pack(fill="x", padx=10, pady=(2, 8))
```

- [ ] **Step 3: 运行回归测试和语法检查**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static -v && python -m py_compile game_modifier/features/35_room_player_count/panel.py`

Expected: 全部测试通过，语法检查退出码为 0。

- [ ] **Step 4: 提交改动**

```bash
git add -- "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json" "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/panel.py" "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py"
git commit -m "fix: keep room player count help text inside card"
```
