# 全模式房间人数两行右侧布局 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让全模式房间人数卡片跨右列两行显示，滑块单独成行，并使用清晰的用户操作说明。

**Architecture:** 通过清单的 `rowspan: 2` 使用现有两列网格的右侧两个连续单元格。自定义面板把标题/开关、滑块和值、说明、操作区拆为四个纵向容器；不改变开关、手动应用或恢复逻辑。

**Tech Stack:** Python 3、CustomTkinter、JSON 清单、`unittest` 静态测试。

---

### Task 1: 为两行布局建立失败测试

**Files:**
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`
- Test: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`

- [ ] **Step 1: 添加布局和说明测试**

```python
def test_manifest_places_room_count_in_the_right_column_across_two_rows(self):
    manifest = json.loads((FEATURE_DIR / "manifest.json").read_text(encoding="utf-8"))
    self.assertEqual(2, manifest["layout"]["rowspan"])
    self.assertEqual(85, manifest["order"])

def test_panel_places_slider_on_its_own_row_with_user_facing_help(self):
    text = (FEATURE_DIR / "panel.py").read_text(encoding="utf-8")
    self.assertIn('slider_row = ctk.CTkFrame(frame, fg_color="transparent")', text)
    self.assertIn('slider_row.pack(fill="x", padx=10, pady=(2, 4))', text)
    self.assertIn("功能说明：开启后，设置总人数并点击“应用人数”。", text)
    self.assertIn("关闭功能会立即恢复默认人数。", text)
```

- [ ] **Step 2: 运行测试，确认旧布局失败**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static.RoomPlayerCountStaticTests -v`

Expected: FAIL，因为清单没有 `rowspan: 2`，且当前滑块仍在标题行。

- [ ] **Step 3: 提交失败测试**

```bash
git add -- "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py"
git commit -m "test: define room player count two-row layout"
```

### Task 2: 实现两行右侧卡片布局

**Files:**
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json:10-20`
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/panel.py:105-145`
- Test: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/test_room_player_count_static.py`

- [ ] **Step 1: 将卡片设为右列跨两行**

```json
"layout": {
  "card_type": "simple",
  "columnspan": 1,
  "rowspan": 2,
  "title_color": "#fbbf24"
}
```

保留 `order: 85`，使网格自动将它放在游戏模式切换下方、第三人称视角右侧下半格，并占据人体穿墙右侧。

- [ ] **Step 2: 将人数显示与滑块移到标题行下方的独立容器**

```python
slider_row = ctk.CTkFrame(frame, fg_color="transparent")
slider_row.pack(fill="x", padx=10, pady=(2, 4))
slider_row.grid_columnconfigure(0, weight=1)

slider = ctk.CTkSlider(slider_row, from_=2, to=100, number_of_steps=98,
                       variable=variable)
slider.grid(row=0, column=0, sticky="ew")
label = _CountLabel(slider_row, text=f"{initial}人", width=44,
                    font=("Microsoft YaHei", 11), text_color="#e0e0e0")
label.grid(row=0, column=1, sticky="e", padx=(8, 0))
```

标题行只保留名称和开关，且继续将 `switch` 返回给共享状态同步逻辑。

- [ ] **Step 3: 替换功能说明文案**

```python
ctk.CTkLabel(
    frame,
    text="功能说明：开启后，设置总人数并点击“应用人数”。人数在下一局开始时生效；关闭功能会立即恢复默认人数。",
    font=("Microsoft YaHei", 12),
    text_color="#a0a0a0",
    wraplength=280,
    justify="left",
    anchor="w",
).pack(fill="x", padx=10, pady=(2, 8))
```

- [ ] **Step 4: 运行房间人数测试并确认通过**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static.RoomPlayerCountStaticTests -v`

Expected: PASS。

- [ ] **Step 5: 提交布局实现**

```bash
git add -- "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json" "04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/panel.py"
git commit -m "feat: arrange room player count across two rows"
```

### Task 3: 语法与范围验证

**Files:**
- Verify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/panel.py`
- Verify: `04-正式发行版/全功能整合包2.5/game_modifier/features/35_room_player_count/manifest.json`

- [ ] **Step 1: 运行静态测试与 Python 语法检查**

Run: `python -m unittest game_modifier.features.35_room_player_count.test_room_player_count_static -v && python -m py_compile game_modifier/features/35_room_player_count/panel.py`

Expected: 测试全部通过，语法检查退出码为 0。

- [ ] **Step 2: 检查 JSON 和差异格式**

Run: `python -c "import json; json.load(open('game_modifier/features/35_room_player_count/manifest.json', encoding='utf-8')); print('JSON OK')" && git diff --check HEAD`

Expected: 输出 `JSON OK`，且差异格式检查退出码为 0。
