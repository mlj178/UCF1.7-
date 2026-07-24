# Player Profile Editor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an independent tool that lets users edit `NickName`, `Level`, and `VipLevel` in UnityCrossFire `PlayerData.dat`.

**Architecture:** Keep file discovery and INI editing in `player_profile_service.py` so the later 2.3 package can reuse it without the standalone UI. The CustomTkinter UI only collects user input, calls the service, and shows status.

**Tech Stack:** Python standard library, CustomTkinter UI, unittest verification.

---

### Task 1: Core Service

**Files:**
- Create: `05-正式功能/34-玩家信息修改器/player_profile_service.py`
- Test: `05-正式功能/34-玩家信息修改器/test_player_profile_service.py`

- [ ] Write tests for path resolution, inserting `[Player]` before `[Inven]`, updating existing `[Player]`, and writing a `.bak` backup.
- [ ] Run `python -m unittest "05-正式功能\34-玩家信息修改器\test_player_profile_service.py" -v` and confirm it fails because the service module is missing.
- [ ] Implement `PlayerProfile`, `get_default_player_data_path`, `update_player_section_text`, `load_profile`, and `save_profile`.
- [ ] Re-run the unittest command and confirm all tests pass.

### Task 2: Standalone UI

**Files:**
- Create: `05-正式功能/34-玩家信息修改器/AAAAA-player_profile_editor_ui.py`

- [ ] Build a CustomTkinter window with NickName, Level, VipLevel inputs, detected path display, load button, save button, and log area.
- [ ] Keep all file mutation inside `player_profile_service.py`.
- [ ] Run `python -m py_compile "05-正式功能\34-玩家信息修改器\AAAAA-player_profile_editor_ui.py"`.

### Task 3: Documentation

**Files:**
- Create: `05-正式功能/34-玩家信息修改器/玩家信息修改器-简要说明.md`

- [ ] Document purpose, target path, saved fields, backup behavior, and 2.3 integration note.
- [ ] Run final verification: unittest plus py_compile for service and UI.
