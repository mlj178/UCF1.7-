# Skill Cooldown Crash Fix Implementation Plan

> **For agentic workers:** Execute the scoped changes below in the current workspace. The user explicitly requested no added test code and no DLL compilation.

**Goal:** Prevent stale or misidentified game-object pointers from being passed to `Skill_Common.EndCold`.

**Architecture:** Capture the local player only from the real `Player.get_isMyPlayer` result. Run the cooldown operation from that player's `Player.Update` callback with 200 ms throttling, and invalidate cached state on player or game-manager destruction.

**Tech Stack:** Frida JavaScript, IL2CPP native hooks.

---

### Task 1: Correct player identity and execution context

**Files:**
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/scripts/17-skill_no_cooldown.js`

- Replace `get_isMyPlayer` function replacement with a passive attach that observes its real return value.
- Remove the `get_nickName` fallback and the `isBot`-based player guess.
- Use the confirmed local player's `Player.Update` callback to invoke `EndCold` at most once every 200 ms.

### Task 2: Handle object destruction

**Files:**
- Modify: `04-正式发行版/全功能整合包1.7-修复版/game_modifier/scripts/17-skill_no_cooldown.js`

- Clear the cached player when `Player.OnDestroy` receives that player.
- Clear all runtime state when `GameManager.OnDestroy` runs.
- Reject enablement if any required hook cannot be installed.

### Task 3: Verify and document

**Files:**
- Create: `04-正式发行版/全功能整合包1.7-修复版/技能无冷却闪退修复记录.md`

- Parse the modified JavaScript with the bundled Node runtime.
- Search the final source to confirm no timer or nickname fallback remains.
- Record the changed and retained execution paths concisely.
