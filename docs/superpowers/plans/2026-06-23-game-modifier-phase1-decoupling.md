# Game Modifier Phase 1 Decoupling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract persistence and command logic out of `ui/app.py` without breaking the current CustomTkinter app.

**Architecture:** Keep the current window and event flow intact while introducing focused repositories for JSON persistence, services for Frida command dispatch, and a lightweight UI state object. `App` becomes an orchestrator that delegates persistence and command work instead of owning every concern directly.

**Tech Stack:** Python, CustomTkinter, Frida, pytest

---

### Task 1: Add tests for extracted persistence and command modules

**Files:**
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\tests\test_repositories.py`
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\tests\test_services.py`

### Task 2: Add repositories and lightweight state

**Files:**
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\core\repositories\__init__.py`
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\core\repositories\nano4t_config_repository.py`
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\core\repositories\feature_state_repository.py`
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\ui\state\__init__.py`
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\ui\state\app_state.py`

### Task 3: Add Frida command services

**Files:**
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\core\services\__init__.py`
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\core\services\feature_command_service.py`
- Create: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\core\services\weapon_giver_service.py`

### Task 4: Wire the current app to use the new modules

**Files:**
- Modify: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\game_modifier\ui\app.py`

### Task 5: Update docs and verify

**Files:**
- Modify: `D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.8\新增内容.md`
