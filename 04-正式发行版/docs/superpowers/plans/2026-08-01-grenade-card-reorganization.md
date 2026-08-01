# Grenade Card Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Keep the existing grenade backend and split its controls into three independently usable visual cards with the required dependency behavior.

**Architecture:** Keep one grenade feature id and one Frida script to avoid duplicate hooks. Reorganize only the custom panel and preserve existing configuration keys and runtime behavior. The combined infinite-grenade/chain-throw card will enforce that chain throw cannot remain enabled when infinite grenades are disabled.

**Tech Stack:** Python, CustomTkinter, JSON manifest, existing feature configuration callbacks.

---

### Task 1: Add focused panel-structure checks

**Files:**
- Create: `game_modifier/features/26_grenade_mode/test_panel_structure.py`

- [x] **Step 1: Add checks for the three card groups, existing config keys, and dependency rule.**
- [x] **Step 2: Run the checks and confirm they fail against the current single-panel layout.**

### Task 2: Reorganize the grenade panel

**Files:**
- Modify: `game_modifier/features/26_grenade_mode/panel.py`

- [x] **Step 1: Add the shared feature-enable helper and dependency-aware toggle callbacks.**
- [x] **Step 2: Render the three cards using the existing switch, slider, select, and config helpers.**
- [x] **Step 3: Keep internal bot support switches hidden behind the 人机手雷模式 card while preserving their config keys.**

### Task 3: Preserve manifest compatibility and verify

**Files:**
- Modify: `game_modifier/features/26_grenade_mode/manifest.json` only if the existing panel metadata prevents the reorganized panel from loading.

- [x] **Step 1: Run Python syntax compilation and the focused panel/config checks.**
- [x] **Step 2: Inspect the diff to confirm no Frida script or unrelated feature was changed.**
