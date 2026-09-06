# ESP Player Collection and Team Filter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修复方框透视在个人竞技中错误过滤全部敌人、在 Alive 列表为空时绘制残留 Player，以及 Nano 模式玩家来源不完整的问题。

**Architecture:** 将“发现 Player 候选”和“允许绘制 Player”拆成两个阶段。GameManager 独立读取所有容器并保存来源位图，纯策略层按 GameMode、Alive 来源、Bot 新鲜度和 Neutral 队伍语义作出确定性判断，Renderer 只绘制通过当前 session、类型、生成和存活验证的候选。

**Tech Stack:** C++17、Win32/IL2CPP、MinHook、Dear ImGui、MSVC v143、Python unittest、MSBuild Release x86

---

## File map

执行命令默认从仓库根目录 `D:\trae_project\ucf1.7-modifier` 运行。

- Create: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/player_policy.h`
  - 只包含可独立测试的 GameMode、来源位图、Neutral 阵营和 Bot 新鲜度规则，不依赖 Windows、ImGui 或 IL2CPP。
- Create: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/tests/esp_player_policy_tests.cpp`
  - 直接执行纯策略矩阵，覆盖 DeathMatch、TeamDeath、Special、Nano、未知模式和 Neutral。
- Create: `04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_esp_player_collection_static.py`
  - 校验原生快照、生命周期、类型验证和 Renderer 接线，补充现有静态测试。
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/il2cpp_bridge.h`
  - 增加 GameMode、gameRoundOver 和原生 `ExpandUtil.IsSameTeam` RVA/静态字段常量。
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.h`
  - 定义容器状态、候选来源、快照接口和统一资格/阵营接口。
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.cpp`
  - 构建多来源快照、维护 Bot epoch、验证 Player 类型与生成状态、调用原生阵营规则。
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/esp_renderer.cpp`
  - 消费快照、按来源与资格绘制，并让过滤和颜色共用同一敌我结果。
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_esp_target_scope_static.py`
  - 将旧的直接队伍字段断言更新为统一 `IsEnemy` 接口断言。
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_health_bar_static.py`
  - 将旧的 Renderer 内联死亡判断断言更新为集中资格判断断言。
- Modify after successful build: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/Universal-ImGui-Hook.dll`
- Modify after successful build: `04-正式发行版/全功能整合包2.5/game_modifier/plugins/universal_hook/Universal-ImGui-Hook.dll`

不修改 2.4 发布包，不修改 WorldToScreen，不修改 UI/命名管道协议。

---

### Task 1: Add executable policy tests and pure player policy

**Files:**
- Create: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/tests/esp_player_policy_tests.cpp`
- Create: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/player_policy.h`

- [ ] **Step 1: Write the failing C++ policy test**

Create `tests/esp_player_policy_tests.cpp` with the complete matrix:

```cpp
#include "../esp/player_policy.h"
#include <cassert>

using namespace esp::policy;

int main() {
    assert(!IsSameTeamByGameRule(TEAM_BLACK_LIST, TEAM_GLOBAL_RISK));
    assert(IsSameTeamByGameRule(TEAM_BLACK_LIST, TEAM_BLACK_LIST));
    assert(IsSameTeamByGameRule(TEAM_GLOBAL_RISK, TEAM_GLOBAL_RISK));
    assert(!IsSameTeamByGameRule(TEAM_NEUTRAL, TEAM_NEUTRAL));
    assert(!IsSameTeamByGameRule(TEAM_NEUTRAL, TEAM_BLACK_LIST));
    assert(!IsSameTeamByGameRule(TEAM_GLOBAL_RISK, TEAM_NEUTRAL));

    const auto all = SourceAllPlayers;
    const auto aliveBL = SourceBLAlive;
    const auto aliveGR = SourceGRAlive;
    const auto bot = SourceBotUpdate;

    assert(IsSourceEligible(GameModeDeathMatch, all, false));
    assert(IsSourceEligible(GameModeDeathMatch, bot, true));
    assert(!IsSourceEligible(GameModeDeathMatch, bot, false));

    assert(IsSourceEligible(GameModeTeamDeath, aliveBL, false));
    assert(IsSourceEligible(GameModeTeamDeath, aliveGR, false));
    assert(!IsSourceEligible(GameModeTeamDeath, all, false));
    assert(!IsSourceEligible(GameModeTeamDeath, bot, true));

    assert(IsSourceEligible(GameModeSpecial, aliveBL, false));
    assert(!IsSourceEligible(GameModeSpecial, all, false));

    assert(IsSourceEligible(GameModeNano4, aliveGR, false));
    assert(IsSourceEligible(GameModeNano4, bot, true));
    assert(!IsSourceEligible(GameModeNano4, bot, false));
    assert(!IsSourceEligible(99, all | aliveBL | bot, true));

    assert(IsBotFresh(1000u, 1500u));
    assert(IsBotFresh(0xFFFFFF00u, 0x00000050u));
    assert(!IsBotFresh(1000u, 2001u));
    return 0;
}
```

- [ ] **Step 2: Compile the test and verify RED**

Run:

```powershell
New-Item -ItemType Directory -Force '05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\build\policy-tests' | Out-Null
cmd /c 'call D:\VS2022\Common7\Tools\VsDevCmd.bat -arch=x86 -host_arch=x64 && cl /nologo /std:c++17 /EHsc /W4 /WX /Fe:05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\build\policy-tests\esp_player_policy_tests.exe 05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\tests\esp_player_policy_tests.cpp'
```

Expected: FAIL with `fatal error C1083` because `esp/player_policy.h` does not exist.

- [ ] **Step 3: Implement the pure policy header**

Create `esp/player_policy.h`:

```cpp
#pragma once
#include <cstdint>

namespace esp::policy {

constexpr int TEAM_BLACK_LIST = 0;
constexpr int TEAM_GLOBAL_RISK = 1;
constexpr int TEAM_NEUTRAL = 2;

constexpr int GameModeTeamDeath = 0;
constexpr int GameModeDeathMatch = 1;
constexpr int GameModeSpecial = 2;
constexpr int GameModeNano3 = 3;
constexpr int GameModeNano4 = 4;
constexpr int GameModeNano6 = 5;
constexpr int GameModeNano4Terminator = 6;

enum PlayerSource : std::uint32_t {
    SourceNone       = 0,
    SourceAllPlayers = 1u << 0,
    SourceBL         = 1u << 1,
    SourceGR         = 1u << 2,
    SourceBLAlive    = 1u << 3,
    SourceGRAlive    = 1u << 4,
    SourceBotUpdate  = 1u << 5,
};

constexpr std::uint32_t BOT_FRESH_MS = 1000u;

constexpr bool HasSource(std::uint32_t sources, PlayerSource source) {
    return (sources & static_cast<std::uint32_t>(source)) != 0u;
}

constexpr bool IsNanoMode(int gameMode) {
    return gameMode >= GameModeNano3 && gameMode <= GameModeNano4Terminator;
}

constexpr bool IsKnownGameMode(int gameMode) {
    return gameMode >= GameModeTeamDeath && gameMode <= GameModeNano4Terminator;
}

constexpr bool IsSameTeamByGameRule(int localTeam, int targetTeam) {
    if (localTeam == TEAM_NEUTRAL || targetTeam == TEAM_NEUTRAL) return false;
    return localTeam == targetTeam;
}

constexpr bool IsBotFresh(std::uint32_t lastSeen, std::uint32_t now) {
    return static_cast<std::uint32_t>(now - lastSeen) <= BOT_FRESH_MS;
}

constexpr bool IsSourceEligible(int gameMode, std::uint32_t sources, bool botFresh) {
    const bool inAlive = HasSource(sources, SourceBLAlive) || HasSource(sources, SourceGRAlive);
    const bool freshBot = HasSource(sources, SourceBotUpdate) && botFresh;
    if (gameMode == GameModeDeathMatch) {
        return HasSource(sources, SourceAllPlayers) || freshBot;
    }
    if (gameMode == GameModeTeamDeath || gameMode == GameModeSpecial) {
        return inAlive;
    }
    if (IsNanoMode(gameMode)) {
        return inAlive || freshBot;
    }
    return false;
}

} // namespace esp::policy
```

- [ ] **Step 4: Compile and run the policy test**

Run the same `cl` command, then:

```powershell
& '05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\build\policy-tests\esp_player_policy_tests.exe'
if ($LASTEXITCODE -ne 0) { throw 'ESP player policy tests failed' }
```

Expected: compile exits 0 with no warnings; executable exits 0 with no output.

- [ ] **Step 5: Commit the pure policy**

```powershell
git add -- '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/player_policy.h' '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/tests/esp_player_policy_tests.cpp'
git commit -m "test: define ESP player source policy"
```

---

### Task 2: Add failing snapshot and renderer integration tests

**Files:**
- Create: `04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_esp_player_collection_static.py`
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_esp_target_scope_static.py`
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_health_bar_static.py`

- [ ] **Step 1: Create the snapshot wiring test**

Create `test_esp_player_collection_static.py`:

```python
from pathlib import Path
import unittest


SOURCE_ROOT = (
    Path(__file__).resolve().parents[5]
    / "05-正式功能"
    / "18-Universal-ESP盒子"
    / "Universal-Dear-ImGui-Hook"
)
MANAGER_H = SOURCE_ROOT / "esp" / "game_manager.h"
MANAGER_CPP = SOURCE_ROOT / "esp" / "game_manager.cpp"
RENDERER = SOURCE_ROOT / "esp" / "esp_renderer.cpp"
BRIDGE = SOURCE_ROOT / "esp" / "il2cpp_bridge.h"


class EspPlayerCollectionStaticTests(unittest.TestCase):
    def test_snapshot_preserves_container_state_and_candidate_sources(self):
        header = MANAGER_H.read_text(encoding="utf-8")
        source = MANAGER_CPP.read_text(encoding="utf-8")
        self.assertIn("enum class ContainerReadState", header)
        self.assertIn("struct PlayerCandidate", header)
        self.assertIn("struct PlayerSnapshot", header)
        self.assertIn("BuildPlayerSnapshot", header)
        for token in (
            "SourceAllPlayers", "SourceBL", "SourceGR",
            "SourceBLAlive", "SourceGRAlive", "SourceBotUpdate",
        ):
            self.assertIn(token, source)
        self.assertNotIn("if (result.empty())", source)

    def test_snapshot_reads_mode_and_round_state(self):
        source = MANAGER_CPP.read_text(encoding="utf-8")
        bridge = BRIDGE.read_text(encoding="utf-8")
        self.assertIn("GM_gameMode", bridge)
        self.assertIn("GM_gameRoundOver", bridge)
        self.assertIn("GetGameMode", source)
        self.assertIn("IsGameRoundOver", source)

    def test_render_eligibility_fails_closed(self):
        source = MANAGER_CPP.read_text(encoding="utf-8")
        self.assertIn("IsCandidateRenderable", source)
        self.assertIn("IsPlayerClassCompatible", source)
        self.assertIn("P_currentCharacter", source)
        self.assertIn("IsPlayerDead", source)

    def test_renderer_consumes_snapshot_and_shared_enemy_rule(self):
        source = RENDERER.read_text(encoding="utf-8")
        self.assertIn("BuildPlayerSnapshot", source)
        self.assertIn("IsCandidateRenderable", source)
        self.assertIn("GameManager::IsEnemy", source)
        self.assertNotIn("GetPlayerTeam(player) == GameManager::GetPlayerTeam(localPlayer)", source)

    def test_bot_supplement_is_epoch_bound_and_fresh(self):
        source = MANAGER_CPP.read_text(encoding="utf-8")
        self.assertIn("entry.epoch == s_SessionEpoch", source)
        self.assertIn("policy::IsBotFresh", source)
        self.assertIn("SourceBotUpdate", source)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Update existing static expectations before implementation**

In `test_esp_target_scope_static.py`, replace the final direct-team assertion:

```python
self.assertIn("GetPlayerTeam(player)", renderer)
```

with:

```python
self.assertIn("GameManager::IsEnemy", renderer)
self.assertNotIn("GetPlayerTeam(player) == GameManager::GetPlayerTeam(localPlayer)", renderer)
```

In `test_health_bar_static.py`, replace:

```python
self.assertIn("if (GameManager::IsPlayerDead(player)) return false;", source)
```

with:

```python
self.assertIn("IsCandidateRenderable", source)
```

- [ ] **Step 3: Run tests and verify RED**

Run from `04-正式发行版/全功能整合包2.5/game_modifier`:

```powershell
python -m unittest features.18_esp_box.test_esp_player_collection_static features.18_esp_box.test_esp_target_scope_static features.18_esp_box.test_health_bar_static -v
```

Expected: new collection tests and updated target-scope/death-filter assertions FAIL because snapshot and shared enemy APIs are not implemented; unrelated UI/health-bar tests remain PASS.

- [ ] **Step 4: Commit failing integration tests**

```powershell
git add -- '04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_esp_player_collection_static.py' '04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_esp_target_scope_static.py' '04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box/test_health_bar_static.py'
git commit -m "test: cover ESP player collection and neutral teams"
```

---

### Task 3: Build a source-aware GameManager snapshot

**Files:**
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/il2cpp_bridge.h`
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.h`
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.cpp`

- [ ] **Step 1: Add static-field and method constants**

Add to `RVAConstants` in `il2cpp_bridge.h`:

```cpp
static constexpr uintptr_t ExpandUtil_IsSameTeam = 0xAF8520;
```

Add to `OffsetConstants`:

```cpp
static constexpr uintptr_t GM_gameMode = 0x04;
static constexpr uintptr_t GM_gameRoundOver = 0x20;
```

These offsets are relative to `GameManager` static fields, not the GameManager instance.

- [ ] **Step 2: Define snapshot data types and APIs**

Include `player_policy.h` and `<cstdint>` in `game_manager.h`, then add:

```cpp
enum class ContainerReadState {
    Invalid,
    Empty,
    Valid,
};

struct PlayerCandidate {
    void* player = nullptr;
    std::uint32_t sources = policy::SourceNone;
    DWORD botLastSeenTick = 0;
    DWORD sessionEpoch = 0;
};

struct PlayerSnapshot {
    int gameMode = -1;
    bool roundOver = true;
    DWORD sessionEpoch = 0;
    ContainerReadState allPlayersState = ContainerReadState::Invalid;
    ContainerReadState blState = ContainerReadState::Invalid;
    ContainerReadState grState = ContainerReadState::Invalid;
    ContainerReadState blAliveState = ContainerReadState::Invalid;
    ContainerReadState grAliveState = ContainerReadState::Invalid;
    std::vector<PlayerCandidate> candidates;
};
```

Replace public `GetAllPlayers()`/`GetBotPlayers()` use with these APIs:

```cpp
static bool BuildPlayerSnapshot(PlayerSnapshot* outSnapshot);
static int GetGameMode();
static bool IsGameRoundOver();
static bool IsCandidateRenderable(
    const PlayerCandidate& candidate,
    const PlayerSnapshot& snapshot,
    void* localPlayer,
    DWORD now);
static bool IsEnemy(void* player, void* localPlayer);
```

Keep private helpers for container reading, merging and type validation.

- [ ] **Step 3: Return stateful container reads**

Replace the current void readers with a small internal result:

```cpp
struct PlayerContainerRead {
    ContainerReadState state = ContainerReadState::Invalid;
    std::vector<void*> players;
};
```

`ReadArrayPlayers` and `ReadListPlayers` must follow this exact state rule:

```cpp
if (container pointer/structure/count is invalid) return Invalid;
if (count == 0) return Empty;
scan elements with AddUniquePlayer;
return Valid; // even if invalid/null slots were skipped
```

Do not retain any `if (result.empty()) { ReadArrayPlayers(allPlayers) }` fallback.

- [ ] **Step 4: Read GameMode and round-over state from static fields**

Factor the existing TypeInfo/static-fields traversal into an internal helper:

```cpp
static void* GetGameManagerStaticFields();
```

Implement:

```cpp
int GameManager::GetGameMode();
bool GameManager::IsGameRoundOver();
```

Both must fail closed: unknown mode is `-1`; unreadable round state is `true`.

- [ ] **Step 5: Merge all container sources by pointer**

Implement `BuildPlayerSnapshot` so it:

1. calls `RefreshSession()` and aborts on failure;
2. reads `gameMode`, `roundOver` and `s_SessionEpoch`;
3. reads all five containers independently;
4. merges candidates with a `std::unordered_map<void*, size_t>` index;
5. ORs `policy::PlayerSource` bits for duplicates;
6. copies current-epoch Bot entries while holding `s_BotPlayersCS`;
7. stores Bot timestamp/epoch and `SourceBotUpdate` without declaring it alive;
8. limits candidate count to the union of the validated container/cache bounds.

Use an internal merge helper with this behavior:

```cpp
static void MergeCandidate(
    PlayerSnapshot& snapshot,
    std::unordered_map<void*, size_t>& index,
    void* player,
    std::uint32_t source,
    DWORD botLastSeen = 0,
    DWORD epoch = 0);
```

- [ ] **Step 6: Run the snapshot subset of tests**

Run:

```powershell
python -m unittest features.18_esp_box.test_esp_player_collection_static.EspPlayerCollectionStaticTests.test_snapshot_preserves_container_state_and_candidate_sources features.18_esp_box.test_esp_player_collection_static.EspPlayerCollectionStaticTests.test_snapshot_reads_mode_and_round_state -v
```

Expected: PASS. Renderer and renderability tests remain RED until later tasks.

- [ ] **Step 7: Compile the full DLL to catch C++ integration errors**

Run from the native source directory:

```powershell
& 'D:\VS2022\MSBuild\Current\Bin\MSBuild.exe' 'Universal-ImGui-Hook.sln' /p:Configuration=Release /p:Platform=x86 /p:OutDir='build\esp-player-filter\' /m /v:minimal
```

Expected: `Build succeeded`, zero compile/link errors, DLL created at `build/esp-player-filter/Universal-ImGui-Hook.dll`.

- [ ] **Step 8: Commit snapshot collection**

```powershell
git add -- '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/il2cpp_bridge.h' '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.h' '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.cpp'
git commit -m "feat: collect source-aware ESP player snapshots"
```

---

### Task 4: Enforce current-session render eligibility

**Files:**
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.cpp`

- [ ] **Step 1: Add Player class compatibility validation**

Implement:

```cpp
static bool IsPlayerClassCompatible(void* player, void* localPlayer) {
    void* playerKlass = nullptr;
    void* localKlass = nullptr;
    return player && localPlayer &&
           SafeReadValue<void*>(player, &playerKlass) &&
           SafeReadValue<void*>(localPlayer, &localKlass) &&
           playerKlass && playerKlass == localKlass &&
           IsValidPointer(playerKlass);
}
```

This build's dump contains one concrete `Player : Entity` class; `Bot.thisPlayer` is typed as `Player`, and no Player subclass exists. Keep the check localized so a future game build can replace it with assignability if subclasses appear.

- [ ] **Step 2: Implement fail-closed spawn validation**

Add an internal helper that requires:

```cpp
currentCharacter = player + P_currentCharacter
characterContainer = player + P_characterContainer
characterController = player + E_characterController
```

`currentCharacter` must be non-null/valid. At least one of characterContainer or characterController must be non-null/valid. Any unreadable field fails.

- [ ] **Step 3: Implement source-aware candidate eligibility**

Implement `IsCandidateRenderable` in this order:

```cpp
if (!HasActiveSession() || snapshot.roundOver) return false;
if (candidate.sessionEpoch != snapshot.sessionEpoch) return false;
if (!candidate.player || candidate.player == localPlayer) return false;
if (!IsPlayerClassCompatible(candidate.player, localPlayer)) return false;

const bool botFresh =
    policy::HasSource(candidate.sources, policy::SourceBotUpdate) &&
    candidate.sessionEpoch == s_SessionEpoch &&
    policy::IsBotFresh(candidate.botLastSeenTick, now);

if (!policy::IsSourceEligible(snapshot.gameMode, candidate.sources, botFresh)) return false;
if (IsPlayerDead(candidate.player)) return false;
if (!IsPlayerSpawned(candidate.player)) return false;
return true;
```

Container candidates must receive the current snapshot epoch during merging, not epoch zero.

- [ ] **Step 4: Tighten Bot cache eviction**

In `GetBotPlayers` replacement/snapshot-copy logic, erase entries when:

```text
entry.epoch != s_SessionEpoch
pointer/type validation fails
entry is older than the existing hard cleanup ceiling
```

The hard cleanup ceiling may remain 5000ms for memory hygiene, but only `policy::BOT_FRESH_MS` grants render eligibility to a Bot that is not in an Alive source.

Keep existing lifecycle clearing in `OnRoundStart` and `OnGameDestroy`. Ensure mode-instance/session replacement clears Bot entries before candidates are built.

- [ ] **Step 5: Run eligibility tests**

Run:

```powershell
python -m unittest features.18_esp_box.test_esp_player_collection_static.EspPlayerCollectionStaticTests.test_render_eligibility_fails_closed features.18_esp_box.test_esp_player_collection_static.EspPlayerCollectionStaticTests.test_bot_supplement_is_epoch_bound_and_fresh -v
```

Expected: PASS.

- [ ] **Step 6: Re-run policy and full native build**

Run the policy executable, then the MSBuild command from Task 3.

Expected: policy executable exits 0; Release x86 build succeeds.

- [ ] **Step 7: Commit eligibility checks**

```powershell
git add -- '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.cpp'
git commit -m "fix: reject stale and unspawned ESP players"
```

---

### Task 5: Use game team semantics in filtering and color

**Files:**
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.cpp`
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/esp_renderer.cpp`

- [ ] **Step 1: Add the safe native team-rule call**

In `game_manager.cpp`, define:

```cpp
typedef bool (__cdecl *IsSameTeamFn)(int team, int otherTeam, void* methodInfo);
```

Add an SEH-protected helper mirroring `SafeCallIsDead`. Implement `GameManager::IsEnemy`:

```cpp
static bool SafeCallIsSameTeam(
    IsSameTeamFn fn,
    int team,
    int otherTeam,
    bool* outSameTeam) {
    if (!fn || !outSameTeam) return false;
    __try {
        *outSameTeam = fn(team, otherTeam, nullptr);
        return true;
    } __except (EXCEPTION_EXECUTE_HANDLER) {
        return false;
    }
}

static void LogTeamRuleFallback() {
    static DWORD lastLogTick = 0;
    const DWORD now = GetTickCount();
    if (static_cast<DWORD>(now - lastLogTick) < config::LOG_INTERVAL) return;
    lastLogTick = now;
    DebugLog("[ESP] ExpandUtil.IsSameTeam unavailable; using verified Neutral fallback");
}

bool GameManager::IsEnemy(void* player, void* localPlayer) {
    const int playerTeam = GetPlayerTeam(player);
    const int localTeam = GetPlayerTeam(localPlayer);
    if (playerTeam < 0 || localTeam < 0) return false;

    void* base = IL2CPPBridge::GetBase();
    auto isSameTeam = base
        ? reinterpret_cast<IsSameTeamFn>(
              static_cast<char*>(base) + RVAConstants::ExpandUtil_IsSameTeam)
        : nullptr;

    bool sameTeam = true;
    if (isSameTeam && IsExecutableAddress(reinterpret_cast<void*>(isSameTeam)) &&
        SafeCallIsSameTeam(isSameTeam, localTeam, playerTeam, &sameTeam)) {
        return !sameTeam;
    }

    LogTeamRuleFallback();
    return !policy::IsSameTeamByGameRule(localTeam, playerTeam);
}
```

- [ ] **Step 2: Replace Renderer collection and filtering**

Change `ESPRenderer::Render()` to:

1. call `BuildPlayerSnapshot(&snapshot)`;
2. get localPlayer;
3. capture `DWORD now = GetTickCount()` once;
4. loop `snapshot.candidates` exactly once;
5. call `IsCandidateRenderable(candidate, snapshot, localPlayer, now)`;
6. if enemy-only is enabled, require `GameManager::IsEnemy(candidate.player, localPlayer)`;
7. call `DrawPlayerESP` only after all checks.

`SafeDrawPlayer` should accept `PlayerCandidate` and `PlayerSnapshot` or be reduced to an SEH wrapper after the centralized checks. It must not perform direct team equality.

- [ ] **Step 3: Make colors use the same enemy result**

Replace `playerTeam != localTeam` in `GetPlayerColor` with:

```cpp
const bool isEnemy = GameManager::IsEnemy(player, localPlayer);
```

Keep existing BL/GR/unknown color choices. Neutral targets in DeathMatch will use the enemy/unknown-enemy color branch instead of ally color.

- [ ] **Step 4: Add source-aware summary diagnostics**

Replace the old `fromList/fromBot/total` summary with one rate-limited record containing:

```text
mode, epoch, all/bl/gr/blAlive/grAlive states,
candidates, rejectedSource, rejectedObject, rejectedTeam, drawn
```

Do not emit per-player logs every frame. Reuse `config::LOG_INTERVAL`.

- [ ] **Step 5: Run all ESP Python tests and policy test**

Run from `04-正式发行版/全功能整合包2.5/game_modifier`:

```powershell
python -m unittest features.18_esp_box.test_esp_player_collection_static features.18_esp_box.test_esp_target_scope_static features.18_esp_box.test_health_bar_static -v
```

Then run `esp_player_policy_tests.exe`.

Expected: every Python and C++ policy test PASS; the direct equality string is absent.

- [ ] **Step 6: Build Release x86**

Run the MSBuild command from Task 3.

Expected: Build succeeded, no new warnings promoted to errors, output DLL exists.

- [ ] **Step 7: Commit renderer and team semantics**

```powershell
git add -- '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/game_manager.cpp' '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp/esp_renderer.cpp'
git commit -m "fix: apply game team rules to ESP targets"
```

---

### Task 6: Verify, package, and record the new x86 DLL

**Files:**
- Modify: `05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/Universal-ImGui-Hook.dll`
- Modify: `04-正式发行版/全功能整合包2.5/game_modifier/plugins/universal_hook/Universal-ImGui-Hook.dll`

- [ ] **Step 1: Run the complete relevant test suite**

Run:

```powershell
& '05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\build\policy-tests\esp_player_policy_tests.exe'
if ($LASTEXITCODE -ne 0) { throw 'Policy tests failed' }

Push-Location '04-正式发行版\全功能整合包2.5\game_modifier'
try {
    python -m unittest features.18_esp_box.test_esp_player_collection_static features.18_esp_box.test_esp_target_scope_static features.18_esp_box.test_health_bar_static -v
    if ($LASTEXITCODE -ne 0) { throw 'ESP Python tests failed' }
} finally {
    Pop-Location
}
```

Expected: all tests PASS.

- [ ] **Step 2: Produce an isolated verification rebuild**

Use a dedicated final output directory and `/t:Rebuild`; do not delete an existing broad build tree:

```powershell
$nativeRoot = [IO.Path]::GetFullPath('05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook')
$verifyDir = [IO.Path]::GetFullPath((Join-Path $nativeRoot 'build\esp-player-filter-final'))
if (-not $verifyDir.StartsWith($nativeRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw "Verification output escaped native project: $verifyDir"
}
New-Item -ItemType Directory -Force -LiteralPath $verifyDir | Out-Null
& 'D:\VS2022\MSBuild\Current\Bin\MSBuild.exe' (Join-Path $nativeRoot 'Universal-ImGui-Hook.sln') /t:Rebuild /p:Configuration=Release /p:Platform=x86 /p:OutDir='build\esp-player-filter-final\' /m /v:minimal
if ($LASTEXITCODE -ne 0) { throw 'Release x86 verification rebuild failed' }
```

Expected: Build succeeded and `build/esp-player-filter-final/Universal-ImGui-Hook.dll` exists.

- [ ] **Step 3: Capture hashes before packaging**

Run:

```powershell
$built = '05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\build\esp-player-filter-final\Universal-ImGui-Hook.dll'
$sourceDll = '05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\Universal-ImGui-Hook.dll'
$packageDll = '04-正式发行版\全功能整合包2.5\game_modifier\plugins\universal_hook\Universal-ImGui-Hook.dll'
Get-FileHash -Algorithm SHA256 $built,$sourceDll,$packageDll | Format-Table Path,Hash -AutoSize
```

Expected: built hash differs from the pre-fix published hash `0E042F7B74D8528DBD6324617B454245FDCF285B27A7E1E6201BB76BFACB65FC`; source and package still show the old hash before copying.

- [ ] **Step 4: Copy only the verified build to the two approved targets**

Resolve and validate all paths, require the verified build to exist, then copy only to the source DLL and 2.5 package DLL:

```powershell
$repoRoot = [IO.Path]::GetFullPath('.')
$built = [IO.Path]::GetFullPath('05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\build\esp-player-filter-final\Universal-ImGui-Hook.dll')
$sourceDll = [IO.Path]::GetFullPath('05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\Universal-ImGui-Hook.dll')
$packageDll = [IO.Path]::GetFullPath('04-正式发行版\全功能整合包2.5\game_modifier\plugins\universal_hook\Universal-ImGui-Hook.dll')
$expectedSource = [IO.Path]::GetFullPath((Join-Path $repoRoot '05-正式功能\18-Universal-ESP盒子\Universal-Dear-ImGui-Hook\Universal-ImGui-Hook.dll'))
$expectedPackage = [IO.Path]::GetFullPath((Join-Path $repoRoot '04-正式发行版\全功能整合包2.5\game_modifier\plugins\universal_hook\Universal-ImGui-Hook.dll'))
if (-not (Test-Path -LiteralPath $built -PathType Leaf)) { throw "Missing verified build: $built" }
if ($sourceDll -ne $expectedSource -or $packageDll -ne $expectedPackage) { throw 'Packaging destination mismatch' }
Copy-Item -LiteralPath $built -Destination $sourceDll -Force
Copy-Item -LiteralPath $built -Destination $packageDll -Force
```

Do not copy to `全功能整合包2.4`.

- [ ] **Step 5: Verify packaged hashes and PE architecture**

Run SHA-256 again and assert all three hashes are equal and not the old hash. Read the PE COFF Machine field and assert `0x014C` (x86) for all three DLLs:

```powershell
$oldHash = '0E042F7B74D8528DBD6324617B454245FDCF285B27A7E1E6201BB76BFACB65FC'
$dlls = @($built, $sourceDll, $packageDll)
$hashes = $dlls | ForEach-Object { (Get-FileHash -Algorithm SHA256 -LiteralPath $_).Hash }
if (($hashes | Select-Object -Unique).Count -ne 1) { throw 'Packaged DLL hashes do not match' }
if ($hashes[0] -eq $oldHash) { throw 'Verification build still has the old release hash' }

foreach ($dll in $dlls) {
    $stream = [IO.File]::OpenRead($dll)
    $reader = [IO.BinaryReader]::new($stream)
    try {
        $stream.Position = 0x3C
        $peOffset = $reader.ReadInt32()
        $stream.Position = $peOffset
        if ($reader.ReadUInt32() -ne 0x00004550) { throw "Invalid PE signature: $dll" }
        $machine = $reader.ReadUInt16()
        if ($machine -ne 0x014C) { throw ('Expected x86 PE Machine 0x014C, got 0x{0:X4}: {1}' -f $machine, $dll) }
    } finally {
        $reader.Dispose()
        $stream.Dispose()
    }
}
Write-Output "Verified SHA256=$($hashes[0]); Machine=0x014C"
```

Expected:

```text
built hash == source DLL hash == 2.5 package DLL hash
hash != 0E042F7B...
Machine == 0x014C
```

- [ ] **Step 6: Run final source and whitespace verification**

```powershell
git diff --check -- '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/esp' '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/tests' '04-正式发行版/全功能整合包2.5/game_modifier/features/18_esp_box'
git status --short
```

Expected: no whitespace errors. Inspect status and stage only files listed in this plan; preserve every unrelated user change.

- [ ] **Step 7: Commit verified binaries**

```powershell
git add -- '05-正式功能/18-Universal-ESP盒子/Universal-Dear-ImGui-Hook/Universal-ImGui-Hook.dll' '04-正式发行版/全功能整合包2.5/game_modifier/plugins/universal_hook/Universal-ImGui-Hook.dll'
git commit -m "build: package fixed ESP x86 hook"
```

- [ ] **Step 8: Report manual acceptance scenarios**

Provide the user this exact manual test matrix without claiming it was executed locally:

```text
1. 个人竞技 + 仅显示敌人：所有非本地存活玩家有框，本地玩家无框。
2. 个人竞技 + 敌人和队友：结果与仅敌人一致，因为 Neutral 玩家互为敌人。
3. 团队竞技 + 仅显示敌人：只显示敌方存活玩家。
4. 团队竞技 + 敌人和队友：显示双方存活玩家，不显示自己。
5. 回合结束/等待复活：死亡与未生成对象无框。
6. 连续换回合、换房和换模式：不出现上一 session 的残留框。
7. Nano 模式：持续活跃但未进入 allPlayers 的 Bot 仍能通过 Bot.Update 补充显示。
8. Bot 暂停功能：观察未注册 Nano Bot 是否在 1 秒后消失；若发生，仅调整补充 TTL 到 2000ms 并重新跑完整测试。
```

---

## Final verification gate

在宣布完成前必须同时满足：

- C++ policy executable exits 0;
- all three ESP Python test modules pass;
- Release x86 MSBuild succeeds;
- built/source/package DLL hashes match and differ from old release;
- all DLLs report PE Machine `0x014C`;
- `git diff --check` reports no errors;
- only plan-scoped files were staged and committed;
- WorldToScreen and 2.4 package remain unchanged.
