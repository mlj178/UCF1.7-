# 方框透视玩家收集与阵营筛选设计

## 背景

方框透视当前存在两个相关但不同的问题：

1. `playersBL_Alive + playersGR_Alive` 为空时，代码无条件回退到 `allPlayers`。这个空结果既可能表示个人竞技按设计不使用 BL/GR 存活列表，也可能表示回合切换、无人存活、容器读取失败或 GameManager 正在销毁。将这些状态视为同一种情况，会把死亡、未生成或残留 Player 交给绘制流程。
2. “仅显示敌人”使用 `playerTeam == localTeam` 判断队友。个人竞技中所有玩家均为 `Team::Neutral (2)`，因此所有目标都被错误当成队友；游戏原生 `ExpandUtil.IsSameTeam` 明确规定任意一方为 Neutral 时均不算同队。

本设计采用已确认的方案 B：**多来源候选集合 + 来源感知的严格资格过滤 + 游戏原生阵营语义**。

## 目标

方框透视只显示满足以下全部条件的对象：

- 属于当前 GameManager、当前房间和当前回合；
- 是有效的 Player 对象；
- 不是本地玩家；
- 已生成当前角色；
- 当前存活；
- 具有可验证的 Transform、CharacterController、Bounds 或骨骼位置；
- 在“仅显示敌人”模式下，按游戏规则确认为敌人。

同时需要覆盖团队竞技、个人竞技、特殊模式和 Nano 系列模式，并保留 Nano Bot 的补漏能力。

## 非目标

- 本次不修改 WorldToScreen、DPI、Camera viewport 或交换链尺寸换算。
- 本次不重新设计 ESP UI 和命名管道协议。
- 本次不增加完全事件驱动的永久玩家注册表。
- 本次不改变方框、血条的样式和颜色配置；只统一颜色所依赖的敌我判断。

## 已确认的游戏语义

### 队伍

```text
BlackList = 0
GlobalRisk = 1
Neutral = 2
```

游戏原生 `ExpandUtil.IsSameTeam(team, otherTeam)` 的等价规则为：

```text
任意一方为 Neutral -> false
否则仅当两个队伍相等 -> true
```

因此个人竞技中的两个 Neutral 玩家互为敌人，而不是队友。

### 模式

```text
TeamDeath = 0
DeathMatch = 1
Special = 2
Nano3 = 3
Nano4 = 4
Nano6 = 5
Nano4_Terminator = 6
```

`GameManager.AddPlayer` 会在 DeathMatch 中把玩家队伍设为 Neutral。DeathMatch 不能要求玩家出现在 BL/GR Alive 列表中。

## 总体架构

处理流程拆成四层：

1. **容器读取层**：独立读取每个 GameManager 玩家容器，并区分有效空列表与读取失败。
2. **候选合并层**：合并所有来源，按 Player 指针去重，同时保留来源标记。
3. **绘制资格层**：根据模式、来源、session epoch、对象类型、生成状态和存活状态决定是否允许绘制。
4. **阵营规则层**：统一为过滤和颜色计算提供同一个 `IsSameTeam`/`IsEnemy` 结果。

容器只负责提供候选，不能单独决定绘制。

## 容器读取层

每帧分别尝试读取：

- `allPlayers`；
- `playersBL`；
- `playersGR`；
- `playersBL_Alive`；
- `playersGR_Alive`；
- 当前 session epoch 的 Bot.Update 缓存。

不再使用“Alive 合并结果为空才读取 allPlayers”的控制流。

每个容器读取结果必须保留状态：

```cpp
enum class ContainerReadState {
    Valid,
    Empty,
    Invalid,
};
```

含义：

- `Valid`：结构与数量合法，至少有一个元素；
- `Empty`：结构合法且数量为零；
- `Invalid`：指针、items、长度或内存读取失败。

`Invalid` 不能静默等同于 `Empty`。Invalid 状态只做限频诊断，本帧对依赖该容器的资格判断失败关闭。

## 候选模型

合并后的每个候选至少记录：

```text
player
fromAllPlayers
fromBL
fromGR
fromBLAlive
fromGRAlive
fromBotUpdate
botLastSeenTick
sessionEpoch
```

相同指针只产生一个候选，来源标记取并集。候选数量设置合理上限，沿用现有容器上限：数组最多 64，单个 List 最多 32，Bot 缓存最多 64。

## 模式与来源资格

### DeathMatch

DeathMatch 中 BL/GR Alive 可能按设计为空。候选满足以下任一来源条件：

- 出现在当前 GameManager 的 `allPlayers`；
- 是当前 epoch 中新鲜的 Bot.Update 补充项。

来源合格后仍需通过全部对象、生成和存活验证。`allPlayers` 不是“必然存活”的证明。

### TeamDeath 和 Special

高可信存活来源为：

- `playersBL_Alive`；
- `playersGR_Alive`。

`allPlayers`、`playersBL` 和 `playersGR` 只用于发现、去重和诊断，不能单独使候选获得绘制资格。这样可防止回合边界、死亡等待复活及未生成对象被绘制。

### Nano3、Nano4、Nano6、Nano4_Terminator

候选满足以下任一来源条件：

- 出现在 `playersBL_Alive` 或 `playersGR_Alive`；
- 是当前 epoch 中新鲜且持续有效的 Bot.Update 补充项。

Nano Bot 可能延迟进入或不完整进入 `allPlayers`，因此保留 Bot.Update 补漏。仅存在于 `allPlayers`、但既不在 Alive 列表也没有新鲜 Bot.Update 证据的对象不绘制。

### 未知模式

遇到枚举范围外的模式时失败关闭：不采用 `allPlayers` 宽松回退，只输出限频诊断。未来新增模式后显式补充策略。

## Bot 缓存和生命周期

Bot 缓存继续作为补充来源，不作为永久注册表。

- 每条记录绑定当前 `sessionEpoch`；
- `Bot.Update` 刷新 `lastSeenTick`；
- 新回合、回合结束、退出房间、模式实例变化和 GameManager OnDestroy 时清空；
- epoch 不一致的记录立即丢弃；
- 仅依赖 Bot.Update 获得资格的目标默认新鲜度为 1000ms；
- 已进入 Alive 列表的 Bot 不受补充 TTL 限制；
- 每次绘制前仍重新验证类型、存活和角色状态。

如果兼容 Bot 暂停功能的实测表明 1000ms 会导致未注册 Nano Bot 消失，可单独把补充 TTL 调整到 2000ms；不得恢复为无来源验证的永久缓存。

## Player 有效性与绘制资格

资格判断采用失败关闭，并按以下顺序执行：

1. GameManager/session 有效且未被生命周期屏障阻止；
2. 当前不处于游戏回合结束状态；
3. Player 指针及对象头可读；
4. 对象的 IL2CPP 类型是 Player 或与本地 Player 类型兼容；
5. Player 不是本地玩家；
6. 候选来源满足当前模式策略；
7. `Entity.get_isDead` 调用成功且返回 false；
8. `currentCharacter` 非空且有效；
9. `characterContainer` 或 CharacterController 至少一个有效；
10. 玩家根位置为有限值且在合理世界范围；
11. Bounds、Hitbox 或骨骼位置与玩家根位置满足距离约束；
12. WorldToScreen 成功且最终方框尺寸、比例与屏幕范围合理。

任何原生调用异常或字段读取失败均判为不可绘制，而不是默认有效。

实施前需确认真人、普通 Bot 和 Nano 角色是否共享同一 Player klass。如果存在 Player 子类，则使用 IL2CPP assignability 验证；不能用严格 klass 相等误删合法目标。

## 阵营规则层

新增单一阵营判断入口，供目标过滤和颜色选择共同使用：

```text
sameTeam = GameRules::IsSameTeam(localTeam, targetTeam)
isEnemy = !sameTeam
```

首选调用游戏原生 `ExpandUtil.IsSameTeam`（RVA `0xAF8520`）。该方法只接收两个队伍整数，避免复制分散的模式规则。

保留与游戏汇编一致的本地兜底：

```cpp
if (localTeam == Neutral || targetTeam == Neutral)
    return false;
return localTeam == targetTeam;
```

原生地址不可执行时必须记录初始化错误；不得退回旧的直接相等规则。

显示策略：

- `enemy_only`：仅绘制 `isEnemy == true` 的合格候选；
- `all_players`：绘制所有合格候选，但继续用统一的 `isEnemy` 结果选择敌我颜色；
- 两种策略始终排除本地玩家。

## 诊断设计

诊断日志保持限频，并能回答“候选从哪里来、为何未绘制”：

```text
gameMode
sessionEpoch
allPlayers / BL / GR / BLAlive / GRAlive 的读取状态和数量
Bot 缓存总数、过期数、epoch 不匹配数
候选去重后数量
按原因拒绝的数量：local、source、type、dead、unspawned、invalidTransform、projection
最终绘制数量
```

不记录高频逐帧完整对象详情；仅在异常或采样周期内记录少量指针、team、来源位图和拒绝原因。

## 测试设计

### 收集与资格

1. DeathMatch：Alive 均为空，allPlayers 含本地玩家和四个存活玩家，只绘制四个非本地玩家。
2. TeamDeath：Alive 均为空而 allPlayers 含旧对象，绘制数为零。
3. TeamDeath：Alive 含本地、队友和敌人，enemy_only 只显示敌人，all_players 显示队友和敌人。
4. Nano：Bot 不在 allPlayers，但有当前 epoch 的新鲜 Bot.Update，允许绘制。
5. Bot epoch 不匹配或超时，不允许绘制。
6. 同一 Player 出现在多个来源，只绘制一次。
7. null 槽位、异常数量和不可读容器安全失败。
8. get_isDead 调用失败、返回 true 或 currentCharacter 为空时不绘制。
9. 未知模式失败关闭。

### 阵营

覆盖 BL/GR/Neutral 的全部组合，特别验证：

- Neutral 与 Neutral 不同队；
- DeathMatch enemy_only 显示所有非本地存活 Player；
- 颜色判断与过滤使用相同结果。

### 生命周期

验证回合结束、新回合、退出、GameManager 销毁和模式实例变化均会清空或隔离旧 Bot 条目；新 session 不接受旧 epoch 候选。

### 构建与发布验证

- 运行现有 ESP 静态测试及新增逻辑测试；
- 构建 Release x86 DLL；
- 验证源工程主 DLL、构建产物和 2.5 发布包 DLL 哈希一致；
- 验证新 DLL 哈希与修改前发布 DLL 不同；
- 不触碰 2.4 发布包，除非用户另行要求回补。

## 预计改动范围

主要修改原生 ESP 源码中的：

- `esp/game_manager.h`、`esp/game_manager.cpp`：模式读取、容器快照、来源状态、Bot 生命周期；
- `esp/esp_renderer.cpp`：基于候选资格和统一阵营规则进行过滤与着色；
- 必要时增加小型内部数据结构或纯逻辑辅助函数；
- 2.5 的 ESP 测试文件；
- Release x86 DLL 及 2.5 发布包中的 `Universal-ImGui-Hook.dll`。

不进行无关重构，不修改 Frida `features/18_esp_box/script.js` 的空实现管线，不修改 UI 配置协议。

## 验收标准

1. 个人竞技选择“仅显示敌人”时，所有非本地、已生成、存活玩家正常显示。
2. 团队模式没有存活敌人时不显示幽灵框，即使 allPlayers 仍保留 Player。
3. 团队模式 enemy_only 不显示队友，all_players 显示合格队友和敌人。
4. Nano 模式不会因 allPlayers 不完整而漏掉持续活跃的 Bot。
5. 回合、房间和模式切换后不绘制上一 session 的对象。
6. 同一玩家每帧最多绘制一次。
7. 容器读取失败和原生调用异常不会导致访问违规或宽松回退。
8. 原有方框、血条开关和命名管道控制保持兼容。
