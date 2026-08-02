# Bot 变英雄 / Bot 变幽灵链路补充报告

## 1. 结论

切换到当前 IDA 数据库的 `GameAssembly.dll` 后，Bot 两条链路均已确认存在，之前“Bot 功能不存在”的结论只适用于旧的 `UnityCrossFire.dll` 包装器，不适用于当前游戏逻辑 DLL。

当前样本：

```text
文件：D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\GameAssembly.dll
ImageBase：0x10000000
MD5：fab04426db6a014c0129ef2001530908
SHA-256：45162101da4f963e8e99ecd63873092e3f5808f00ffcfd6f2649eea68d94ee1f
架构：x86 / 32 位 IL2CPP
```

核心区别：`GameAssembly.dll` 已经包含 `Bot`、`BotAction.BA_BecomeHero`、`Bot.OnNanoRoleTableTypeChange`、`Mode_Nano4.BecomeHero` 和 `ModeBase_Nano.ChangeNanoGhostType`；因此可以直接从原生 Bot 流程复刻，而不需要猜测 Bot 是否存在。

## 2. Bot 变英雄

### 2.1 原生 AI 链路

```text
Bot 的 Action 更新
  -> BotAction.BA_BecomeHero.Update()
  -> BotAction.BA_BecomeHero.CanDo()
  -> BotAction.BA_BecomeHero.DoAction()
  ->（满足条件后，按当前 Nano4 流程进入）Mode_Nano4.BecomeHero()
  -> ModeBase_Nano.UpdateNanoRole()
  -> Player.nanoRole 更新及角色状态清理
  -> Bot.OnNanoRoleChange(oldRole, newRole)
```

关键地址：

| 函数 | VA | 作用 |
|---|---:|---|
| `BotAction.BA_BecomeHero.CanDo` | `0x10B2AC10` | 判断 Bot 是否可以变英雄 |
| `BotAction.BA_BecomeHero.DoAction` | `0x10B2ACB0` | 执行/准备变英雄动作；包含补给箱存在及随机等待逻辑 |
| `BotAction.BA_BecomeHero.Update` | `0x10B2AE40` | 周期调用 `CanDo`，通过后执行 `DoAction` |
| `Mode_Nano4.TryBecomeHero` | `0x10B46460` | 人类英雄准备流程；满足条件后调用 `BecomeHero` |
| `Mode_Nano4.BecomeHero` | `0x10B412F0` | 对指定 `Player*` 实际落地英雄角色 |
| `ModeBase_Nano.UpdateNanoRole` | `0x10AF4FF0` | 写入新角色并同步队伍/PlayerData 状态 |
| `Bot.OnNanoRoleChange` | `0x10B31760` | Bot 角色变化后的导航和动作处理 |

`CanDo` 的已确认条件：

```text
Mode_Nano4.isHeroReady == true
Bot.thisPlayer != null
Bot.thisPlayer.healthData != null
HealthData.isDead == false
Bot.thisPlayer.team == 1
```

这里的 `Bot.thisPlayer` 是目标 Bot 对应的 `Player*`，不是本地玩家占位对象。因此原生 AI 不需要重新枚举 Bot；Bot 实例本身已经保存了目标 Player。

### 2.2 英雄角色值

`NanoRoleSelect.Active` 中的英雄分支为：

```c
Mode_Nano4.BecomeHero(
    Mode_Nano4.instance3,
    nanoRoleSelect.owner,
    nanoRoleSelect.selection + 22,
    true
);
```

当前 `NanoRole` 枚举：

| selection | 角色值 | 角色 |
|---:|---:|---|
| `1` | `23` | `MasterHumanHero` |
| `2` | `24` | `MasterHunter` |
| `3` | `25` | `AsceticHero` |
| `4` | `26` | `MysticHero` |
| `5` | `27` | `MechanicHero` |

Bot 的 `tableType == Hero(2)` 随机选择 `selection=1/2/3/5`，所以原生 Bot 英雄 AI 实际覆盖 `MasterHumanHero`、`MasterHunter`、`AsceticHero` 和 `MechanicHero`，不会随机到 `MysticHero(26)`。

### 2.3 Bot 角色变化回调

`Bot.OnNanoRoleChange` 会：

1. 通过 `NanoRoleExpand.IsHuman(newRole)` 设置寻路 `traversableTags` 的第 3 位。
2. 当 `newRole == 27 (MechanicHero)` 时，创建并加入 `BotAction.Role_MechanicHero`。

因此复刻时不能只写 `Player.nanoRole=27`；必须调用原生 `BecomeHero` 或完整的 `UpdateNanoRole`，否则模型、队伍、寻路和 MechanicHero 专属 AI 可能不同步。

## 3. Bot 变幽灵

### 3.1 原生 Bot 选择链路

```text
NanoRoleSelect.tableType 变化
  -> Bot.OnNanoRoleTableTypeChange(tableType)
  -> 针对 Bot.thisPlayer.nanoRole / tableType 选择 selection
  -> StartCoroutine(Bot...InputSelect)
  -> 等待随机 0.10~0.25 秒
  -> Bot.thisPlayer.nanoRoleSelect.Select(selection)
  -> NanoRoleSelect.Active()
  -> SelectNanoGhost 分支
  -> ModeBase_Nano.ChangeNanoGhostType(mode, owner, role)
  -> ModeBase_Nano.UpdateNanoRole(mode, owner, role)
  -> Bot.OnNanoRoleChange(oldRole, newRole)
```

关键地址：

| 函数 | VA | 作用 |
|---|---:|---|
| `Bot.OnNanoRoleTableTypeChange` | `0x10B31800` | 根据角色表类型为 Bot 生成选择值 |
| `Bot...InputSelect.MoveNext` | `0x10B72C00` | 延迟后调用 `Player.nanoRoleSelect.Select(selection)` |
| `Bot...InputSelect` | `0x10B76100` | 创建协程枚举器 |
| `NanoRoleSelect.Active` | `0x10B4EAA0` | 根据 tableType/selection 分发实际变身 |
| `NanoRoleSelect.SelectNanoGhost` | `0x10B4EE90` | selection 到幽灵角色值的映射 |
| `ModeBase_Nano.ChangeNanoGhostType` | `0x10AEF790` | 对指定 Player 执行幽灵角色切换 |
| `ModeBase_Nano.UpdateNanoRole` | `0x10AF4FF0` | 统一角色状态更新 |

### 3.2 Bot 幽灵选择值

`Bot.OnNanoRoleTableTypeChange` 中，`tableType == Normal(1)` 且当前 Bot 为 `NanoGhost(1)` 时，使用 `RandomRangeInt(0,3)` 选择：

| 随机结果 | selection | 传入 ChangeNanoGhostType 的角色值 | 角色 |
|---:|---:|---:|---|
| `0` | `1` | `7` | `Psycho` |
| `1` | `2` | `3` | `Nurse` |
| `2` | `6` | `2` | `Hulk` |

`NanoRoleSelect.Active`/`SelectNanoGhost` 明确调用：

```c
selection == 1 -> ChangeNanoGhostType(mode, owner, 7);
selection == 2 -> ChangeNanoGhostType(mode, owner, 3);
selection == 6 -> ChangeNanoGhostType(mode, owner, 2);
```

### 3.3 变幽灵后的状态更新

`ChangeNanoGhostType` 不检查 `isBot`，只要求传入有效的 `Player*`。当新旧角色不同，它会进入 `UpdateNanoRole`；后者负责：

```text
读取旧 nanoRole
计算新角色所属队伍
写入 Player.nanoRole
必要时调用 Player.SetTeam
清理 Nano4 数据/纳米伤害/幽灵经验等状态
触发角色变化相关回调
```

因此 Bot 变幽灵的关键不是“找一个特殊 Bot 变身函数”，而是拿到正确的 `ModeBase_Nano*` 和 `Bot.thisPlayer`，再走原生 `ChangeNanoGhostType`。

## 4. 两条链路的复刻接口建议

如果目的是复刻原生功能，建议以以下两个逻辑接口为核心：

```c
// Bot 英雄
Mode_Nano4.BecomeHero(modeNano4, botPlayer, heroRole, false);

// Bot 幽灵
ModeBase_Nano.ChangeNanoGhostType(modeNano, botPlayer, ghostRole);
```

其中：

```text
heroRole：23/24/25/26/27；原生 Bot 随机表使用 23/24/25/27
ghostRole：7=Psycho，3=Nurse，2=Hulk
botPlayer：Bot + 0x24 的 thisPlayer 字段，或等价的 Bot.thisPlayer 属性
```

更接近原生 AI 的实现方式是：

```text
遍历有效 Bot 实例
  -> 读取 Bot.thisPlayer
  -> 过滤 null / dead
  -> 英雄：等待 isHeroReady，再调用 BecomeHero
  -> 幽灵：按 tableType 计算 selection，再调用 Select(selection)
```

不建议直接写 `Player.nanoRole`，因为会跳过 `SetTeam`、PlayerData 清理、Bot 导航标记、MechanicHero 动作和其它角色回调。

## 5. 复刻时的边界与验证点

已由当前 IDA 样本直接确认：

- Bot 类型和 `thisPlayer` 字段存在。
- Bot 英雄动作类存在，且 `CanDo` 有存活、队伍、英雄准备状态判断。
- Bot 角色表变化会启动延迟协程并调用 `nanoRoleSelect.Select`。
- 英雄与幽灵最终都接受任意有效 `Player*`，没有 `isBot` 禁止分支。
- `MechanicHero=27` 会额外添加 Bot 专属动作。

仍需动态验证：

1. `BA_BecomeHero.DoAction` 的补给箱条件与随机等待何时实际触发 `TryBecomeHero`；IDA 当前对该函数局部控制流识别不完整，但入口和结果函数均已确认。
2. 角色调用是否必须由 Unity 主线程执行。
3. 服务器/回合逻辑是否会在下一帧覆盖强制角色变化。
4. 直接调用时 `Mode_Nano4.instance3` 与 `ModeBase_Nano.instance2` 的生命周期。
5. `Bot.thisPlayer` 的字段偏移在目标构建中是否仍为 `+0x24`。

## 6. 最终判断

```text
Bot 变英雄：存在，原生入口为 BotAction.BA_BecomeHero，最终落到 Mode_Nano4.BecomeHero。
Bot 变幽灵：存在，原生入口为 Bot.OnNanoRoleTableTypeChange，最终落到 ChangeNanoGhostType。
旧 UnityCrossFire.dll：只有包装器/选择入口，未闭合 Bot 目标链。
当前 GameAssembly.dll：Bot 目标、选择、延迟协程、角色分发和状态回调均已闭合。
```
