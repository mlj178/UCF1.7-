# GameManager 类完整分析与修改指南

> 适用版本：当前 `UnityCrossFire 1.7.1` 的 `GameAssembly.dll`  
> 主要依据：`Il2CppDumper/dump.cs`、IDA 导出汇编、IDA MCP 反编译  
> 分析角度：Unity 生命周期 + 穿越火线对局逻辑 + CE/Frida 修改实践

关系图与流程版：

- [GameManager 类关系与流程](类关系分析/01-GameManager类关系与流程.md)
- [穿越火线核心类总览](类关系分析/00-穿越火线核心类总览.md)

---

## 一、GameManager 在游戏中的职责

`GameManager : Singleton<GameManager>` 是一局穿越火线比赛的核心管理器。

从游戏流程看，它主要负责：

```text
进入战斗场景
→ 创建 GameManager 单例
→ 加载武器资源和对象池
→ 根据房间 ClientData 创建所有 Player/Bot
→ 保存双方玩家列表和存活列表
→ 管理伤害、击杀和回合结束事件
→ 提供武器、角色模型和玩家查询功能
→ 离开房间时清理静态引用和事件
```

它不是所有游戏逻辑的唯一管理器：

| 游戏功能 | 主要类 |
|---|---|
| 本局玩家、武器、伤害、回合入口 | `GameManager` |
| 具体比赛规则、比分和倒计时 | `ModeBase` 及其子类 |
| 出生点 | `MapManager` |
| 玩家生命、队伍、移动、武器包 | `Player` / `Entity` / `PlayerWeapons` |
| 房间配置和 ClientData | `UI_GameRoom` / `ClientData` |
| Bot 行为 | `Bot` |
| 摄像机 | `CameraManager` |

因此，修改 `GameManager` 的字段不一定等于修改完整游戏规则。很多值只是入口、缓存或列表，真正状态可能由其他类持续维护。

本版本 `dump.cs` 中的 GameManager 清单：

| `dump.cs` 分类 | 数量 | 进一步拆分或例外 |
|---|---:|---|
| `Fields` | 42 | 27 个静态字段 + 15 个实例字段 |
| `Properties` | 8 | 全部为静态属性 |
| `Methods` | 58 | 包含 10 个属性 getter/setter、20 个事件 add/remove、5 个生命周期/构造方法、23 个业务方法 |
| 公开字段 | 26 | 包含普通数据字段和公开 Delegate 字段 |
| 私有字段 | 16 | 包含 2 个编译器生成的 backing field 和多个私有 Delegate |
| 编译器生成 backing field | 2 | `<ace>k__BackingField`、`<gameRoundOver>k__BackingField` |
| Delegate 类型字段 | 17 | `DamageEvent`、`DeathEvent`、`SpecialKillChecker`、`Action` |
| 嵌套 Delegate 类型 | 3 | `DamageEvent`、`DeathEvent`、`SpecialKillChecker` |
| 回合重置协程编译类 | 1 | `<RestRoundCoroutine>d__88`，不属于 GameManager 本体的 58 个方法 |

说明：

- `Fields=42` 是字段总数，不能再与“静态字段 + 实例字段”并列相加。
- `Properties=8` 在 IL2CPP 中还会生成对应的 getter/setter 方法，这些访问器已经包含在 `Methods=58` 内。
- 嵌套 Delegate 和协程状态机是独立生成类型，不计入 GameManager 本体字段、属性和方法数量。

---

## 二、读取偏移时最容易犯的错误

### 静态字段偏移和实例字段偏移不是同一个基址

实例字段：

```text
GameManager 实例地址 + 字段偏移
```

静态字段：

```text
GameManager_TypeInfo
→ Il2CppClass.static_fields
→ 静态字段偏移
```

例如：

```text
allPlayers = GameManager实例 + 0x1C
myPlayer   = GameManager静态字段区 + 0x00
gameMode   = GameManager静态字段区 + 0x04
```

不能使用：

```text
GameManager实例 + 0x04
```

去读取 `gameMode`。实例 `+0x04` 属于 IL2CPP 对象头，不是该静态字段。

### `dump.cs` 中相同偏移不代表冲突

例如：

```text
实例字段 playerPrefab = 0x0C
静态字段 revengeEnable = 0x0C
```

它们属于两个不同的内存区域。

---

## 三、如何获取当前 GameManager

### 推荐方式：调用单例 getter

```text
Singleton<GameManager>.get_instance()
共享函数 RVA：0x4A8170
GameManager MethodInfo RVA：0xE1CE64
```

这个 getter 是泛型共享实现，必须传入 `Singleton<GameManager>` 对应的 `MethodInfo`。IDA 显示它通过 `method->klass -> rgctx_data` 确定泛型参数，最后返回 `Singleton<GameManager>` 静态字段中的实例。

### 其他方式

| 方式 | 适用情况 | 风险 |
|---|---|---|
| Hook `GameManager.Awake(this)` 保存 `this` | 需要稳定监听房间创建 | 离房必须在 `OnDestroy` 清空 |
| Hook `GameManager.Start(this)` | 玩家即将创建时 | 进入 Start 前资源可能还没准备好 |
| 从 `Singleton<GameManager>` 静态 instance 读取 | CE/原生 DLL | 需要正确解析泛型类静态字段 |
| `FindObjectOfType<GameManager>()` | Unity 托管代码 | 较慢，切场景时可能为空 |

### 不推荐方式

不要长期缓存跨房间使用的 `GameManager*`。Unity 销毁对象后，旧地址可能仍可读，但已经不是当前房间对象。

推荐生命周期：

```text
GameManager.Awake/Start → 保存当前实例
GameManager.OnDestroy   → 清空实例、Player 和所有派生缓存
```

---

## 四、修改价值等级

| 等级 | 含义 |
|---|---|
| S | 修改功能的重要入口，值得重点研究 |
| A | 很有用，但需要正确对象、参数或生命周期 |
| B | 可用于状态读取、事件监听或辅助功能 |
| C | 内部资源、缓存或低频功能 |
| D | 不建议直接改，容易无效或破坏状态 |

写入策略：

| 标记 | 含义 |
|---|---|
| 直接读取 | 通常可以安全读取 |
| 条件写入 | 可以写，但可能被游戏重新覆盖 |
| Hook 推荐 | 修改生产者或调用链比反复写字段可靠 |
| 不建议写 | 引用、集合或事件对象不能随便填裸地址 |

---

## 五、全部静态字段

静态字段偏移基址均为 `GameManager_TypeInfo->static_fields`。

### 5.1 模式、本地玩家和回合状态

| 字段 | 偏移 | 穿越火线中的作用 | 实际来源 / 主要写入者 | 价值与修改建议 |
|---|---:|---|---|---|
| `myPlayer` | `0x00` | 当前本地玩家的 `Player` 对象。自瞄、武器、摄像机和本地事件的重要入口 | `AddPlayers()` 遍历 `ClientData`，当前项等于 `ClientData.mine` 时写入；`OnDestroy()` 清零 | S。主要读取，不建议替换 |
| `gameMode` | `0x04` | 当前比赛模式：团队竞技、个人竞技、特殊战、生化模式等 | 房间创建/加载阶段写入；`get_isNanoMode()`、`AddPlayer()`、`GetWeapon()` 等读取 | S。可条件写入，但战斗中改值不会重建 Mode、队伍、UI |
| `weaponLimited` | `0x08` | 房间武器限制：无限制、刀战、手枪、狙击 | 房间配置阶段写入；`GetWeapon()` 每次取得武器时读取并过滤 | A。可写，可能被房间初始化覆盖 |
| `revengeEnable` | `0x0C` | 是否允许击杀事件产生“复仇”判定 | 房间/模式配置写入；`DeathEventBroadcast()` 相关击杀逻辑读取 | B。可写，但不等于直接制造复仇或加分 |
| `gameModePrefab` | `0x10` | 当前模式逻辑预制体 | 房间加载阶段选择；`GameManager.Awake()` 读取并 `Instantiate` | A。应在 `Awake()` 前修改，战斗中替换不会自动重建 Mode |
| `<ace>k__BackingField` | `0x14` | 属性 `ace` 的实际存储位置，即当前 Ace/MVP 候选玩家 | `set_ace()` / `TryGetAce()` 更新；`OnDestroy()` 清零 | B。会随击杀数据重新计算 |
| `WpnDictionary` | `0x18` | `weaponIndex -> Weapon` 武器模板字典 | `.cctor()` 创建空字典；`LoadWeapon()` 填充；`GetWeapon()`、`GetWpnData()` 读取 | S。读取或修改字典内容，勿替换为裸地址 |
| `WpnDataDictionary` | `0x1C` | `weaponIndex -> WeaponData` 武器配置字典 | `.cctor()` 创建；`LoadWeapon()` 填充；武器查询逻辑读取 | S。适合修改模板数据 |
| `<gameRoundOver>k__BackingField` | `0x20` | 属性 `gameRoundOver` 的实际存储位置 | `GameRoundEnd()` 写 `true`；回合重置流程恢复；`OnDestroy()` 结束整局生命周期 | A。应修改触发条件，避免只循环写最终标记 |
| `dropWpnRecycleTime` | `0x68` | 掉落武器回收到对象池前的时间 | `.cctor()` 明确初始化为 `10.0f`；掉落武器回收逻辑读取 | B。可改，最好在掉落计时开始前写入 |

### `myPlayer` 赋值与清空的直接依据

`AddPlayers()` 中：

```text
0x10AF9F14  读取 ClientData.mine
0x10AF9F7B  cmp esi, [ebp-14h]
            当前遍历 ClientData == ClientData.mine 才进入本地玩家分支
0x10AF9FA6  取得 GameManager.static_fields
0x10AF9FAB  mov [eax], edi
            static_fields + 0x00 = 当前新建 Player
```

其中：

```text
esi = 当前 ClientData
edi = AddPlayer() 返回的 Player
[eax] = GameManager 静态字段偏移 0x00，也就是 myPlayer
```

`OnDestroy()` 中：

```text
0x10AFB74D  mov eax, [GameManager_TypeInfo + 0x5C]
            eax = GameManager.static_fields
0x10AFB753  mov dword ptr [eax], 0
            static_fields + 0x00 = null
```

因此更准确的结论是：

```text
AddPlayers() 只在当前 ClientData == ClientData.mine 时设置 myPlayer；
GameManager.OnDestroy() 在离开/销毁本局 GameManager 时清空 myPlayer。
```

#### `gameMode` 枚举

| 值 | 模式 | 穿越火线含义 |
|---:|---|---|
| 0 | `TeamDeath` | 团队竞技 |
| 1 | `DeathMatch` | 个人竞技 |
| 2 | `Special` | 特殊战 |
| 3 | `Nano3` | 生化模式之一 |
| 4 | `Nano4` | 生化模式之一 |
| 5 | `Nano6` | 生化模式之一 |
| 6 | `Nano4_Terminator` | 多人终结者模式 |

#### 为什么修改 `gameMode` 后看起来没有反应

`gameMode` 只是模式标识，真正的模式对象在 `GameManager.Awake()` 中依据 `gameModePrefab` 实例化。队伍也已经在 `AddPlayer()` 中分配。

在房间运行中只改 `gameMode`：

```text
不会自动替换 ModeBase 子类
不会重新分配 Player.team
不会重建 HUD
不会重置出生点
不会重新绑定模式事件
```

正确方向是修改房间创建阶段的数据，或者在新场景加载前同时配置 `gameMode` 与 `gameModePrefab`。

### 5.2 武器字典

静态构造函数 `.cctor()` 创建两个空字典，`Awake()` 再调用 `LoadWeapon(weaponAsset)` 加载内容。

如果过早调用 `GetWeapon()` 或 `GiveWeapon()`：

```text
WpnDictionary 可能仍为空
weaponPool 可能尚未初始化
GameManager.instance 可能为 null
```

这会表现为返回空、调用无反应或异常。

### 5.3 伤害与死亡事件

| 字段 | 偏移 | 功能 | 实际来源 / 主要写入者 | 价值与修改建议 |
|---|---:|---|---|---|
| `DamageEvent_InvalidCheck_Observers` | `0x24` | 伤害合法性检查阶段 | 各系统调用 `add_DamageEvent_InvalidCheck_Observers()` 注册；`TakeDamage()` 调用；`OnDestroy()` 清空 | S。通过 add/remove 或 Hook 使用 |
| `DamageEvent_PreCal_Observers` | `0x28` | 伤害正式计算前 | `add_DamageEvent_PreCal_Observers()` 维护；`TakeDamage()` 伤害链读取 | S。可修改 `ref DamageEventData` |
| `DamageEvent_PostCal_Observers` | `0x2C` | 伤害计算后、最终处理前 | `add_DamageEvent_PostCal_Observers()` 维护；`TakeDamage()` 读取 | S。适合观察最终计算或二次调整 |
| `DamageEvent_Post_Observers` | `0x30` | 伤害流程完成后的广播 | 游戏系统直接赋/组合公开 Delegate；`TakeDamage()` 后段读取；`OnDestroy()` 清空 | A。适合记录 |
| `DeathEvent_Observers` | `0x34` | 通用死亡事件 | Mode/HUD/统计系统注册；`DeathEventBroadcast()` 调用；`OnDestroy()` 清空 | A。可监听所有击杀 |
| `DeathEvent_ForGameRule` | `0x38` | 比赛规则专用死亡事件 | 当前 `ModeBase` 子类注册；`DeathEventBroadcast()` 调用 | S。影响比分、复活和胜负，不能随意清空 |
| `firstAndLastKillChecker` | `0x3C` | 判断首杀、最后一杀 | 模式规则设置；`DeathEventBroadcast()` 调用 | B。直接替换必须构造正确 Delegate |
| `MyPlayerCasueDamageEvent_Observers` | `0x50` | 本地玩家造成伤害 | 对应 add/remove 维护；`TakeDamage()` 根据攻击者是否为 myPlayer 调用 | A。适合命中记录 |
| `MyPlayerGetDamageEvent_Observers` | `0x54` | 本地玩家受到伤害 | 对应 add/remove 维护；受害者为 myPlayer 时调用 | A。适合受击触发 |
| `MyPlayerKillEvent_Observers` | `0x58` | 本地玩家击杀别人 | 对应 add/remove 维护；`DeathEventBroadcast()` 调用 | A。适合击杀触发 |
| `MyPlayerDeathEvent_Observers` | `0x5C` | 本地玩家死亡 | 对应 add/remove 维护；`DeathEventBroadcast()` 调用 | A。适合死亡清理 |

`TakeDamage(DamageEventData)` 会从合法性检查事件开始执行。事件委托通常接收结构体引用，因此 CE 直接调用时必须构造完整参数，不能只调用函数地址而不准备 `DamageEventData`。

### 5.4 玩家和回合事件

| 字段 | 偏移 | 功能 | 实际来源 / 主要写入者 | 价值与修改建议 |
|---|---:|---|---|---|
| `NewPlayerJoinEvent_Observers` | `0x40` | 新 Player 对象创建并加入本局 | add/remove 维护；`AddPlayers()` 每创建并初始化一个 Player 后调用 | A。适合更新玩家缓存 |
| `PlayerSpawnEvent_Observers` | `0x44` | 任意玩家出生/复活 | 外部系统注册；`Player.Spawn()` 调用；`OnDestroy()` 清空 | S。比 `AddPlayer` 更适合监听复活 |
| `MyPlayerJoinEvent_Observers` | `0x48` | 本地 Player 首次加入 | add/remove 维护；`AddPlayers()` 的本地 ClientData 分支调用 | A。适合取得 myPlayer |
| `MyPlayerSpawnEvent_Observers` | `0x4C` | 本地玩家出生/复活 | 外部系统注册；`Player.Spawn()` 在 isMyPlayer 条件下调用 | S。适合重新应用功能 |
| `NewGameRoundStart_Observer` | `0x60` | 新回合开始 | 模式、地图、HUD 系统注册；`ResetRound` 协程调用 | S。适合回合重置 |
| `GetGrenadeFromBag_Observer` | `0x64` | 从背包取得投掷武器时触发 | add/remove 维护；`GiveWeaponByBag()` 在手雷槽条件下调用 | B。只在对应路径触发 |

### 为什么直接改 Observer 字段危险

这些字段是 IL2CPP 委托对象指针，不是普通开关：

```text
委托对象
→ target
→ method_ptr
→ invoke_impl
→ method metadata
```

向字段写 `1`、写任意函数地址或清空游戏规则委托，都可能导致崩溃或规则失效。应调用对应的 `add_...` / `remove_...` 方法，或 Hook 广播函数。

---

## 六、全部实例字段

实例字段偏移基址为当前 `GameManager*`。

### 6.1 玩家与 Bot

| 字段 | 偏移 | 穿越火线中的作用 | 实际来源 / 主要写入者 | 价值与修改建议 |
|---|---:|---|---|---|
| `playerPrefab` | `0x0C` | 真人/本地 Player 创建时使用的预制体 | Unity 场景或 Prefab 序列化字段注入；`AddPlayer(isBot=false)` 读取 | A。可读取，不建议战斗中替换 |
| `botPrefab` | `0x10` | Bot Player 创建时使用的预制体 | Unity 场景或 Prefab 序列化字段注入；`AddPlayer(isBot=true)` 读取 | A。替换对象必须兼容原 Bot/Player 组件 |
| `entityBL_Alive` | `0x14` | 潜伏者阵营所有存活 `Entity`，可能包含 Player 以外实体 | `.ctor()` 创建空 List；Entity 出生/死亡流程动态增删 | A。适合读取，列表内容会持续变化 |
| `entityGR_Alive` | `0x18` | 保卫者阵营所有存活 `Entity` | `.ctor()` 创建；Entity 出生/死亡流程动态维护 | A。同上 |
| `allPlayers` | `0x1C` | 固定长度 30 的 Player 槽位数组 | `.ctor()` 创建 `new Player[30]`；`AddPlayer()` 写入空槽 | S。重要入口，不建议直接改数组长度或槽位 |
| `playersBL` | `0x20` | 潜伏者全部 Player 列表 | `.ctor()` 创建；`AddPlayer()`/Player 初始化按队伍加入 | S。适合阵营功能 |
| `playersBL_Alive` | `0x24` | 潜伏者存活 Player 列表 | `.ctor()` 创建；`Player.Spawn()`、死亡流程维护 | S。读取存活状态，注意事件时间差 |
| `playersGR` | `0x28` | 保卫者全部 Player 列表 | `.ctor()` 创建；`AddPlayer()`/Player 初始化按队伍加入 | S。适合阵营功能 |
| `playersGR_Alive` | `0x2C` | 保卫者存活 Player 列表 | `.ctor()` 创建；`Player.Spawn()`、死亡流程维护 | S。同上 |

IDA 确认构造函数创建：

```text
allPlayers = new Player[30]
playersBL / playersBL_Alive = new List<Player>()
playersGR / playersGR_Alive = new List<Player>()
entityBL_Alive / entityGR_Alive = new List<Entity>()
```

#### 能否修改这些列表

技术上可以，但不推荐直接修改 `_size`、`_items` 或数组指针。

原因：

- Player 内部仍保存自己的队伍和索引；
- ModeBase、记分板、出生逻辑可能持有相同 Player；
- Unity GC 需要写屏障；
- 列表会被出生、死亡和回合重置逻辑继续维护；
- 从列表删掉 Player 不等于销毁角色。

可靠方式是 Hook 正常的加入、出生、死亡或销毁流程，再维护自己的独立缓存。

### 6.2 武器和角色资源

| 字段 | 偏移 | 作用 | 实际来源 / 主要写入者 | 价值与修改建议 |
|---|---:|---|---|---|
| `weaponAsset` | `0x30` | 房间可使用的武器资源集合 | Unity Inspector/Prefab 序列化注入；`Awake()` 读取并调用 `LoadWeapon()` | S。适合查询资源 |
| `characterAsset` | `0x34` | 角色模型资源集合 | Unity Inspector/Prefab 序列化注入；`SetCharacter()` 读取 | A。可用于查角色 Prefab |
| `characterPool` | `0x38` | 角色模型对象池 | `Awake()` 使用 GameManager Transform 创建 `NameKeyPool` 后写入 | A。私有运行时对象，不要写裸指针 |
| `weaponPool` | `0x3C` | 武器实例对象池 | `Awake()` 创建 `NameKeyPool`；`GetWeapon()` 读取、复用和登记武器 | S。修改其内部结构风险高 |

### 6.3 回收对象和摄像机辅助

| 字段 | 偏移 | 作用 | 实际来源 / 主要写入者 | 价值与修改建议 |
|---|---:|---|---|---|
| `recyclableObjects` | `0x40` | 本回合需要统一回收的对象，如掉落物和临时对象 | `.ctor()` 创建；`AddRecyclableObject()`、`RemoveRecyclableObject()`、`ClearRecyclableObject()` 维护 | B。使用原方法，不要直接破坏 List |
| `playerCameraChanger` | `0x44` | 玩家镜头切换相关内部计数/索引 | 构造时默认为 0；具体写入链在当前重点反编译中尚未完全确认 | C。标记为“需要运行时写断点验证”，不凭字段名强行解释 |

---

## 七、全部属性

| 属性 | Getter/Setter RVA | 实际来源 | 用途 | 可否修改 |
|---|---|---|---|---|
| `myJoinTeam` | `0xAFDAE0` | `ClientData.mine.joinTeam` | 本地玩家加入的阵营 | 只读属性；应修改 ClientData 来源或 Player.team |
| `isNanoMode` | `0xAFDA80` | `gameMode` 是否在 3~6 | 判断生化模式 | 只读计算值，不能单独修改 |
| `playerCount_BL` | `0xAFDB40` | `playersBL.Count` | 潜伏者总人数 | 只读计算值 |
| `alivePlayerCount_BL` | `0xAFD930` | `playersBL_Alive.Count` | 潜伏者存活人数 | 只读计算值 |
| `playerCount_GR` | `0xAFDBC0` | `playersGR.Count` | 保卫者总人数 | 只读计算值 |
| `alivePlayerCount_GR` | `0xAFD9B0` | `playersGR_Alive.Count` | 保卫者存活人数 | 只读计算值 |
| `ace` | get `0xAFD8E0`, set `0xAFE3C0` | 静态 backing field | 当前 MVP/Ace | Setter 私有，且会被 `TryGetAce()` 更新 |
| `gameRoundOver` | get `0xAFDA30`, set `0xAFE420` | 静态 backing field | 回合结束标记 | Setter 私有，回合流程会重写 |

### 属性对应的全部实际方法名

| 实际方法 | RVA | 说明 |
|---|---:|---|
| `get_myJoinTeam()` | `0xAFDAE0` | 返回 `ClientData.mine.joinTeam` |
| `get_isNanoMode()` | `0xAFDA80` | 判断 `gameMode` 是否在 3~6 |
| `get_playerCount_BL()` | `0xAFDB40` | 返回 `playersBL.Count` |
| `get_alivePlayerCount_BL()` | `0xAFD930` | 返回 `playersBL_Alive.Count` |
| `get_playerCount_GR()` | `0xAFDBC0` | 返回 `playersGR.Count` |
| `get_alivePlayerCount_GR()` | `0xAFD9B0` | 返回 `playersGR_Alive.Count` |
| `get_ace()` | `0xAFD8E0` | 读取 Ace backing field |
| `set_ace(Player)` | `0xAFE3C0` | 写入 Ace backing field，源码访问级别为 private |
| `get_gameRoundOver()` | `0xAFDA30` | 读取回合结束标记 |
| `set_gameRoundOver(bool)` | `0xAFE420` | 写入回合结束标记，源码访问级别为 private |

### 为什么改人数属性没有反应

人数属性没有独立存储值：

```text
get_playerCount_BL()
→ GameManager.instance.playersBL
→ List<Player>.Count
```

CE 找到 getter 返回的数字后修改，只是在改寄存器结果或临时显示值，下一次 getter 会重新读取 List 的 `_size`。

如果修改 List `_size`：

- 记分板可能短暂变化；
- 实际 Player 不会创建或销毁；
- 遍历可能访问垃圾指针；
- 下一次列表操作可能恢复或崩溃。

---

## 八、全部事件注册方法

这些方法本质上使用 `Delegate.Combine` 或 `Delegate.Remove` 修改事件链。

| 方法 | RVA | 功能 |
|---|---:|---|
| `add_DamageEvent_InvalidCheck_Observers` | `0xAFD160` | 注册伤害合法性检查 |
| `remove_DamageEvent_InvalidCheck_Observers` | `0xAFDC40` | 注销伤害合法性检查 |
| `add_DamageEvent_PreCal_Observers` | `0xAFD2E0` | 注册伤害计算前事件 |
| `remove_DamageEvent_PreCal_Observers` | `0xAFDDC0` | 注销伤害计算前事件 |
| `add_DamageEvent_PostCal_Observers` | `0xAFD220` | 注册伤害计算后事件 |
| `remove_DamageEvent_PostCal_Observers` | `0xAFDD00` | 注销伤害计算后事件 |
| `add_NewPlayerJoinEvent_Observers` | `0xAFD820` | 注册新玩家加入事件 |
| `remove_NewPlayerJoinEvent_Observers` | `0xAFE300` | 注销新玩家加入事件 |
| `add_MyPlayerJoinEvent_Observers` | `0xAFD6A0` | 注册本地玩家加入事件 |
| `remove_MyPlayerJoinEvent_Observers` | `0xAFE180` | 注销本地玩家加入事件 |
| `add_MyPlayerCasueDamageEvent_Observers` | `0xAFD460` | 注册本地玩家造成伤害事件 |
| `remove_MyPlayerCasueDamageEvent_Observers` | `0xAFDF40` | 注销本地玩家造成伤害事件 |
| `add_MyPlayerGetDamageEvent_Observers` | `0xAFD5E0` | 注册本地玩家受伤事件 |
| `remove_MyPlayerGetDamageEvent_Observers` | `0xAFE0C0` | 注销本地玩家受伤事件 |
| `add_MyPlayerKillEvent_Observers` | `0xAFD760` | 注册本地玩家击杀事件 |
| `remove_MyPlayerKillEvent_Observers` | `0xAFE240` | 注销本地玩家击杀事件 |
| `add_MyPlayerDeathEvent_Observers` | `0xAFD520` | 注册本地玩家死亡事件 |
| `remove_MyPlayerDeathEvent_Observers` | `0xAFE000` | 注销本地玩家死亡事件 |
| `add_GetGrenadeFromBag_Observer` | `0xAFD3A0` | 注册取得投掷武器事件 |
| `remove_GetGrenadeFromBag_Observer` | `0xAFDE80` | 注销取得投掷武器事件 |

注意：`DamageEvent_Post_Observers`、`DeathEvent_Observers`、`DeathEvent_ForGameRule`、`PlayerSpawnEvent_Observers`、`MyPlayerSpawnEvent_Observers` 和 `NewGameRoundStart_Observer` 在 `dump.cs` 中是公开委托字段，没有对应的 GameManager add/remove 包装方法。

原生脚本若要订阅事件，需要正确创建 IL2CPP Delegate。通常直接 Hook 事件广播点更简单、更稳定。

---

## 九、嵌套委托与回合协程类

### 9.1 `GameManager.DamageEvent`

```csharp
void Invoke(ref DamageEventData data)
```

关键点是 `ref`：观察者接收同一份伤害结构体地址，可以修改后续流程使用的数据。原生 Hook 时必须按指针处理，不能误认为是普通返回值事件。

### 9.2 `GameManager.DeathEvent`

```csharp
void Invoke(DeathEventData data)
```

用于广播攻击者、死亡者、爆头、穿墙、武器、复仇和特殊击杀等信息。

### 9.3 `GameManager.SpecialKillChecker`

```csharp
SpecialKillType Invoke(Entity killer, Entity dead)
```

根据攻击者和死亡者返回：

```text
None
FirstKill
LastKill
```

### 9.4 `GameManager.<RestRoundCoroutine>d__88`

这是 C# 编译器为：

```csharp
IEnumerator RestRoundCoroutine(float delay)
```

生成的状态机类。重要成员：

| 成员 | 偏移/RVA | 作用 |
|---|---|---|
| `<>1__state` | `0x08` | 协程当前执行阶段 |
| `<>2__current` | `0x0C` | 当前 yield 对象 |
| `delay` | `0x10` | 回合重置延迟 |
| `MoveNext()` | `0xB71440` | 执行协程的实际回合重置逻辑 |
| `IEnumerator.Reset()` | `0xB71510` | 状态机 Reset 接口 |

通常应调用 `ResetRound(delay)` 让 Unity 启动协程，不应手工创建或修改状态机字段。

---

## 十、全部普通方法总表

### 10.1 Unity 生命周期和初始化

| 方法 | RVA | 穿越火线中的功能 | 主要调用者 / 前置依赖 | 修改价值 |
|---|---:|---|---|---|
| `Awake()` | `0xAFA250` | 设置 Singleton，加载武器，创建角色池和武器池，实例化模式 Prefab | Unity 场景加载自动调用；依赖序列化的 Asset、Prefab 和有效 GameObject | S |
| `Start()` | `0xAFC160` | `ResetRound(0)` 后进入 `AddPlayers()` | Unity 在 Awake 后自动调用；依赖房间 ClientData 已准备 | S |
| `OnDestroy()` | `0xAFB6F0` | 清空单例、本地玩家、Ace 和所有事件委托 | Unity 销毁场景对象时调用 | S |
| `.ctor()` | `0xAFCFB0` | 创建玩家列表、存活列表、30 槽数组和回收列表 | IL2CPP 创建 GameManager 对象时调用 | B |
| `.cctor()` | `0xAFCEF0` | 创建武器字典并设置掉落武器回收时间为 10 秒 | IL2CPP 首次使用类型前自动执行一次 | B |
| `Test()` | `0xAFC890` | 游戏内部测试/调试逻辑 | 调用入口及完整意图需要运行时验证 | C |

### 10.2 玩家、Bot、角色与队伍

| 方法 | RVA | 穿越火线中的功能 | 主要调用者 / 实际数据来源 | 调用建议 |
|---|---:|---|---|---|
| `AddPlayers()` | `0xAF9DE0` | 遍历房间 `ClientData`，批量创建所有 Player/Bot，设置 `myPlayer`、角色和武器包 | `Start()` 调用；玩家信息来自 `UI_GameRoom` 的 `List<ClientData>` | S，通常不应重复主动调用 |
| `AddPlayer(bool isBot, Team team)` | `0xAF9A90` | 实例化单个 Player/Bot，分配模式队伍，写入 `allPlayers` | `AddPlayers()` 调用；依赖 `playerPrefab/botPrefab`、当前 `gameMode` 和空槽 | S，需要有效 `this` |
| `GetSparePlayerIndex()` | `0xAFACE0` | 在 `allPlayers[30]` 中寻找第一个空槽 | 读取 `GameManager.instance.allPlayers` | A，可安全查询 |
| `SetCharacter(Player, string)` | `0xAFBFD0` | 从角色资源/对象池取得模型并绑定给 Player | `AddPlayers()` 和生化角色切换调用；依赖 `characterAsset/characterPool` | A，需要合法 IL2CPP 字符串 |
| `GetCharacter(string)` | `0xAFABC0` | 按角色名取得角色模型 | `SetCharacter()` 内部辅助；来源为角色资源和对象池 | B，私有辅助方法 |
| `TryGetAce(Player)` | `0xAFCD00` | 按击杀/死亡数据判断并更新 Ace | `Player.UpdateAce()` 调用；比较记分板击杀/死亡数据 | B |

### 10.3 武器

| 方法 | RVA | 穿越火线中的功能 | 主要调用者 / 实际数据来源 | 调用建议 |
|---|---:|---|---|---|
| `LoadWeapon(WeaponAsset)` | `0xAFB4B0` | 把武器资源加载进两个静态字典 | `Awake()` 调用；来源为实例字段 `weaponAsset` | S，只应在资源有效时调用 |
| `GetWeapon(int)` | `0xAFADB0` | 从武器池取实例；没有则从模板实例化，并应用模式/武器限制 | `GiveWeapon()`、地图枪等调用；依赖 `weaponPool`、`WpnDictionary`、`gameMode`、`weaponLimited` | S |
| `GiveWeapon(Player,int,bool,bool)` | `0xAFB390` | 给 Player 设置武器所有者，可丢弃旧槽位并自动切换 | 补给箱、修改器等调用；内部使用 `GetWeapon()` 和 `Player.wpns` | S |
| `GiveWeaponByBag(Player,int)` | `0xAFB2A0` | 背包路径给武器，内部调用 `GiveWeapon(false,false)`，手雷槽会广播事件 | `Player.SelectWeaponBag()` 调用；武器 ID 来自 WeaponBag | A |
| `GetWpnData(int,out WeaponData)` | `0xAFB130` | 从字典取得武器配置 | HUD/背包和查询代码调用；读取武器字典中的 Weapon.data | A |
| `GetWpnName(int)` | `0xAFB1F0` | 根据武器 ID 获取名称 | 击杀信息、UI 等查询；数据来自武器配置 | B |

### 10.4 伤害、击杀和特效

| 方法 | RVA | 穿越火线中的功能 | 主要调用者 / 实际数据来源 | 调用建议 |
|---|---:|---|---|---|
| `TakeDamage(DamageEventData)` | `0xAFC1C0` | 完整伤害总入口：检查、计算、扣血、特效、死亡广播 | 武器命中流程调用；数据来自攻击者、受害者和武器生成的 `DamageEventData` | S，不适合 CE 无参数调用 |
| `PlayHitFxAndSnd(...)` | `0xAFB970` | 播放命中特效和声音 | `TakeDamage()` 后段调用；依赖受害者、命中点和资源名称 | C，需要完整参数 |
| `DeathEventBroadcast(DeathEventData)` | `0xAFA400` | 处理并广播击杀、复仇、首杀/末杀、本地玩家事件和规则事件 | `TakeDamage()` 在确认死亡后调用；输入来自真实死亡结果 | S，不建议伪造不完整结构体 |

### 10.5 回合、场景和对象池

| 方法 | RVA | 穿越火线中的功能 | 主要调用者 / 实际数据来源 | 调用建议 |
|---|---:|---|---|---|
| `ResetRound(float delay=0)` | `0xAFBCA0` | 启动回合重置协程，清理对象并发出新回合事件 | `Start()` 和模式规则调用；依赖当前 GameManager 与 Unity Coroutine | S，调用后改变整局状态 |
| `RestRoundCoroutine(float)` | `0xAFBEC0` | 延时执行 ResetRound 的实际步骤 | 仅由 `ResetRound()` 创建并启动；状态保存在编译器状态机 | B，不建议直接调用 |
| `GameRoundEnd()` | `0xAFAA40` | 设置 `gameRoundOver=true` 并处理回合结束状态 | `ModeBase` 子类胜负条件调用 | S |
| `ReturnLobby()` | `0xAFBF20` | 加载大厅场景并处理控制器状态 | `ModeBase.ExitGame()` 调用；依赖 Unity SceneManager | A，调用会退出战斗 |
| `AddRecyclableObject(obj)` | `0xAFA1C0` | 将临时对象加入本回合回收列表 | 掉落物/临时实体创建时调用 | B |
| `RemoveRecyclableObject(obj)` | `0xAFBC10` | 从回收列表移除对象 | 对象自行回收或销毁时调用 | B |
| `ClearRecyclableObject()` | `0xAFA370` | 回收/清空所有登记对象 | `ResetRound()` 等清场流程调用 | B |

---

## 十一、继承自 Singleton<GameManager> 的方法

这些方法虽然不在 GameManager 本体方法表中，但 GameManager 会使用。

| 方法 | 共享 RVA | 功能 |
|---|---:|---|
| `Singleton<GameManager>.get_instance()` | `0x4A8170` | 获取当前单例 |
| `Singleton<GameManager>.Awake()` | `0x4A7C30` | 设置单例 instance |
| `Singleton<GameManager>.OnDestroy()` | `0x4A7FA0` | 清理单例 instance |
| `Singleton<GameManager>.SetVisible(bool)` | `0x4A8030` | 设置该 GameObject 可见/激活相关状态 |

泛型共享方法必须使用正确 `MethodInfo`。只调用 RVA 而把 MethodInfo 传 `0`，可能在方法读取 `method->klass` 时崩溃。

### 11.1 `<instance>k__BackingField` 是什么

`dump.cs` 中 `Singleton<T>` 的定义包含：

```csharp
private static T <instance>k__BackingField;
public static T instance { get; set; }
```

这是 C# **自动属性的编译器生成后台字段**。

开发者原始代码通常类似：

```csharp
public static T instance { get; private set; }
```

C# 编译器需要一个真实字段保存属性值，于是自动生成：

```text
<instance>k__BackingField
```

名称拆解：

| 部分 | 含义 |
|---|---|
| `<instance>` | 这个字段属于名为 `instance` 的属性 |
| `k__BackingField` | 编译器约定：这是属性的后台存储字段 |
| `static T` | 每个封闭泛型 Singleton 类型保存自己的实例 |

对本游戏来说：

```text
Singleton<GameManager>      有自己的 instance
Singleton<CameraManager>    有自己的 instance
Singleton<MapManager>       有自己的 instance
```

虽然 IL2CPP 可能共享同一个 getter 本机代码 RVA，但必须通过不同 `MethodInfo` 找到对应泛型类型的静态字段。

`GameManager.myPlayer` 与它不是同一个东西：

| 字段 | 保存内容 |
|---|---|
| `Singleton<GameManager>.<instance>k__BackingField` | 当前 `GameManager` 对象 |
| `GameManager.myPlayer` | 当前本地玩家 `Player` 对象 |

生命周期：

```text
Singleton<GameManager>.Awake()
→ <instance>k__BackingField = 当前 GameManager this

Singleton<GameManager>.OnDestroy()
→ <instance>k__BackingField = null
```

`<ace>k__BackingField` 和 `<gameRoundOver>k__BackingField` 原理相同，分别是 `ace`、`gameRoundOver` 属性的真实存储字段。

修改建议：

- 读取 Singleton 实例时，优先调用 `get_instance()`。
- 不要把 `<instance>k__BackingField` 改成任意地址。
- 写错会使所有通过 Singleton 取得 GameManager 的方法访问错误对象。
- 场景切换时旧 GameManager 会销毁，不能把旧 instance 强行写回。

---

## 十二、玩家与 Bot 管理重点分析

### 12.1 `AddPlayers()` 的真实作用

调用关系：

```text
GameManager.Start()
→ ResetRound(0)
→ AddPlayers()
→ 遍历 UI_GameRoom 中的 ClientData
→ AddPlayer(clientData.isBot, clientData.joinTeam)
→ ClientData.Update()
→ Player.clientData = 当前 ClientData
→ 加载 WeaponBag
→ 如果是 ClientData.mine：
   GameManager.myPlayer = 当前 Player
   CameraManager.SetFocusPlayer(myPlayer)
→ SetCharacter()
→ NewPlayerJoinEvent
```

所以 `AddPlayers()` 不是“刷新玩家列表”的普通方法，而是房间初始化阶段的批量构建流程。

重复主动调用可能：

- 重复创建 Player；
- 占用新的 `allPlayers` 槽；
- 重复加载角色和武器；
- 覆盖 `myPlayer`；
- 造成记分板、事件和对象池状态不一致。

### 12.2 `AddPlayer()` 与复活的区别

`AddPlayer()`：

```text
创建新的 Player GameObject
→ 取得 Player 组件
→ 设置队伍
→ 写入 allPlayers 空槽
→ 设置 Player 索引
```

普通死亡复活：

```text
Mode_DeathMatch/Mode_TeamDeath.DeathEvent
→ Player.Respawn()
→ 延时
→ Player.Spawn()
```

复活复用原来的 `Player`，不会重新执行 `AddPlayer()`。

监听复活应使用：

- `Player.Spawn()`；
- `PlayerSpawnEvent_Observers`；
- `MyPlayerSpawnEvent_Observers`。

### 12.3 模式如何改变队伍

IDA 中 `AddPlayer()` 的实际队伍分配：

```text
GameMode 3~6 → 强制 team = 1
GameMode 1   → 强制 team = 2
其他模式     → 使用传入 team
```

个人竞技 `team=2` 表示中立。敌我逻辑需要先排除自己，再把其他中立 Player 当作敌人。

### 12.4 获取所有 Player 的建议

```text
基础来源：
allPlayers + playersBL + playersGR

特殊 Bot 补充：
Bot.Update() -> Bot.thisPlayer

最终：
按 Player 指针去重
```

不要只读 `playersBL/playersGR` 后假定特殊模式没有遗漏，也不要只用 `Bot.thisPlayer` 代替真人玩家集合。

---

## 十三、武器功能重点分析

### 13.1 `GiveWeapon()` 为什么 CE 调用后没有反应

函数签名：

```csharp
Weapon GiveWeapon(
    Player player,
    int weaponIndex,
    bool autoGiveUp,
    bool autoSelect
)
```

必须同时满足：

1. `player` 是当前房间有效的 `Player*`；
2. `weaponIndex >= 0`；
3. `LoadWeapon()` 已填充 `WpnDictionary`；
4. `GetWeapon()` 没有被 `weaponLimited` 或模式限制拦截；
5. Player 的 `wpns` 已初始化；
6. 调用约定和参数顺序正确；
7. IL2CPP 隐藏参数 `MethodInfo*` 正确，或者该函数路径允许传空；
8. 若希望立即切枪，`autoSelect=true`。

内部流程：

```text
GetWeapon(weaponIndex)
→ 可选：丢弃目标槽旧武器
→ Weapon.SetOwner(player)
→ 可选：PlayerWeapons.Select(targetSlot)
```

`autoSelect=false` 时，武器可能已经给到 Player，但当前手持武器不变，看起来像“没有反应”。

### 13.2 `GetWeapon()` 不是简单查字典

它会：

- 优先从 `weaponPool` 按名称取可复用对象；
- 再从 `WpnDictionary` 查模板；
- 检查武器模式限制；
- 实例化 GameObject；
- 调用武器虚函数 `Init()`；
- 设置对象池；
- 调用 `OnSelectedFromWeaponPool()`。

所以直接调用需要主线程、有效 Unity 对象和完整房间环境。

### 13.3 修改 WeaponData 和修改 Weapon 实例的区别

| 对象 | 含义 | 修改效果 |
|---|---|---|
| `WpnDataDictionary[id]` | 武器配置模板 | 可能影响之后创建/初始化的武器 |
| `WpnDictionary[id]` | 武器模板/Prefab 组件 | 影响从模板生成的实例 |
| Player 当前 `Weapon` | 正在使用的实例 | 立即影响当前武器，但换枪/重生可能丢失 |

想让功能跨换枪、复活保持，应在 `PlayerWeapons.Select`、`Player.Spawn` 或武器初始化点重新应用。

---

## 十四、伤害与击杀重点分析

### 14.1 `TakeDamage()` 是完整业务入口

`TakeDamage(DamageEventData data)` 不是无参方法。`DamageEventData` 至少包含：

```text
攻击者
受害者
伤害值/类型
命中位置
命中标签
武器信息
流程状态
```

它还会调用多个 Observer，部分 Observer 可以修改结构体。

用 CE 直接执行函数地址但没有构造参数时：

- 函数可能读取到随机攻击者/受害者；
- `data.type` 可能导致流程提前结束；
- Unity 对象检查失败；
- 事件把伤害改回去；
- 最终没有扣血；
- 严重时崩溃。

如果目标只是修改伤害，优先方案：

1. Hook `DamageEvent_PreCal_Observers` 前后的伤害数据；
2. Hook `TakeDamage()` 并修改传入结构体；
3. 修改武器攻击数据的生产源；
4. 不建议伪造一次完整 `TakeDamage()` 调用。

### 14.2 伤害阶段

可按以下逻辑理解：

```text
InvalidCheck
→ 判断伤害是否允许
→ PreCal
→ 计算护甲、爆头、距离等
→ PostCal
→ 应用生命值
→ 命中特效和声音
→ Post
→ 如果死亡则 DeathEventBroadcast
```

不同阶段适合的功能：

| 需求 | 推荐阶段 |
|---|---|
| 无敌、禁止伤害 | InvalidCheck 或生命扣除前 |
| 伤害倍率 | PreCal |
| 记录最终伤害 | PostCal/Post |
| 自动触发击杀逻辑 | 不建议伪造，使用真实死亡流程 |

---

## 十五、回合、模式与胜负重点分析

### 15.1 `GameRoundEnd()`

IDA 已确认它首先执行：

```text
gameRoundOver = true
```

随后处理玩家/回合结束状态。

只把 `gameRoundOver` 改成 `false` 不等于恢复比赛，因为：

- ModeBase 可能已停止计时；
- 玩家控制可能已关闭；
- HUD 可能已显示结果；
- 回合结束事件已经广播；
- 下一回合协程可能已经启动。

要阻止结束，应 Hook 调用 `GameRoundEnd()` 的规则条件，而不是结束后反复写 `false`。

### 15.2 `ResetRound(delay)`

它通过协程延时执行，可能包含：

- 清理临时对象；
- 重置回合状态；
- 重新出生玩家；
- 发送 `NewGameRoundStart_Observer`；
- 恢复 `gameRoundOver`；
- 重置模式数据。

CE 调用时必须按静态方法调用约定传入 `float delay`。把它当无参方法调用，栈中的随机值可能被解释成延迟时间。

### 15.3 `ReturnLobby()`

IDA 显示它会调用 Unity：

```text
SceneManager.LoadScene(...)
```

这是场景切换方法。调用成功后当前 GameManager 会销毁，所有旧 Player/GameManager 指针都必须失效。

---

## 十六、特效、对象池与场景生命周期

### 对象池为什么会让修改看起来恢复

武器和角色不一定每次创建新对象：

```text
对象使用结束
→ 回到 NameKeyPool/ObjectPool
→ 下次取出
→ Init/OnSelectedFromWeaponPool 重新初始化
```

如果只修改某个实例字段：

- 回收到池时可能被重置；
- 再次取出时 Init 会覆盖；
- 换枪后拿到的是另一个实例。

跨实例修改应针对：

- `WeaponData` 模板；
- `Weapon.Init()`；
- `Weapon.OnSelectedFromWeaponPool()`；
- `PlayerWeapons.Select()`。

### `OnDestroy()` 清理范围

IDA 确认 `GameManager.OnDestroy()` 会清空：

- Singleton instance；
- `myPlayer`；
- `ace`；
- 所有伤害、死亡、加入、出生、回合和手雷 Observer。

因此，跨房间缓存这些指针或委托都会失效。脚本必须在新房间重新获取和安装。

---

## 十七、CE 主动调用无反应的常见原因

### 原因 1：把实例方法当静态方法

例如：

```csharp
Player AddPlayer(bool isBot, Team team)
```

真实本机参数包含：

```text
GameManager* this
bool isBot
Team team
MethodInfo* method
```

缺少 `this` 时函数无法访问 Prefab、列表和对象池。

### 原因 2：把有隐藏参数的方法当真正无参

IL2CPP 方法通常还有：

```text
MethodInfo* method
```

泛型共享函数尤其依赖它。`Singleton<GameManager>.get_instance()` 的实现会读取 `method->klass`，不能随便传空。

### 原因 3：调用时机不对

| 时机 | 可能缺少的内容 |
|---|---|
| `Awake` 前 | Singleton、对象池、武器资源 |
| `Start/AddPlayers` 前 | `myPlayer`、Player、ClientData 绑定 |
| 玩家死亡期间 | `wpns`、Character、Transform 的有效状态 |
| `OnDestroy` 后 | 整个房间对象已经失效 |

### 原因 4：方法只发事件，没有观察者

部分方法的效果依赖 Observer。若当前模式没有注册对应委托，调用可能只执行空检查，看不到画面变化。

### 原因 5：方法只改变后台数据

例如给武器但没有 `autoSelect`，当前画面不切枪；修改 Ace 但记分板没有刷新；修改模式值但模式 Prefab 已创建。

### 原因 6：调用线程错误

涉及以下 Unity API 的方法通常应在 Unity 主线程执行：

- `Instantiate`；
- `LoadScene`；
- `Transform`；
- `GameObject`；
- `Component.GetComponent`；
- 对象池和模型切换。

从 CE 任意线程直接调用可能无效、卡死或崩溃。

### 原因 7：参数类型构造错误

常见错误：

- 把普通 ASCII 地址当作 `System.String*`；
- 把整数当作 `Player*`；
- 结构体按值/按引用传递错误；
- `bool` 宽度、浮点参数或栈对齐错误；
- x86 调用约定错误。

---

## 十八、字段修改后恢复原值的原因

### 18.1 修改的是计算结果，不是数据源

```text
playerCount_BL ← playersBL.Count
isNanoMode     ← gameMode 范围判断
myJoinTeam     ← ClientData.mine.joinTeam
```

应修改右侧数据源或 Hook getter。

### 18.2 每帧、每次事件或每回合重新赋值

常见覆盖点：

| 字段/状态 | 可能覆盖来源 |
|---|---|
| `myPlayer` | `AddPlayers()`、`OnDestroy()` |
| `gameRoundOver` | `GameRoundEnd()`、`ResetRound()` |
| `ace` | `TryGetAce()`、回合清理 |
| 存活列表 | `Player.Spawn()`、死亡事件 |
| 当前武器 | `PlayerWeapons.Select()`、复活和背包加载 |
| 角色模型 | `SetCharacter()`、生化角色切换 |
| `gameMode` | 房间加载/场景初始化数据 |

### 18.3 修改了模板，但当前实例已经创建

修改 `WeaponData` 模板后，当前手中的 Weapon 可能已经复制了相关数值。需要重新初始化、换枪或同时修改实例。

### 18.4 修改了实例，但对象池重新初始化

换枪、掉落、拾取、复活后，游戏可能从对象池取得新实例，并恢复模板值。

### 18.5 写入了错误的字段区

最常见的是：

- 把静态偏移加到 GameManager 实例；
- 把实例偏移加到 `static_fields`；
- 把 List 对象地址当作数据数组；
- 忘记 Unity/IL2CPP 对象头。

### 18.6 Unity 假 null

Unity 对象原生部分被销毁后，托管指针可能非零，但 `UnityEngine.Object.op_Implicit` 会返回 false。仅判断地址非零不够。

---

## 十九、推荐修改策略

### 玩家和 Bot

```text
GameManager.Awake/Start 获取实例
→ allPlayers + playersBL + playersGR
→ Bot.thisPlayer 补充
→ 指针去重
→ Player.get_isMyPlayer / Entity.get_team / Entity.get_isDead
→ Player.OnDestroy 或 GameManager.OnDestroy 清理
```

### 武器

```text
读取 WpnDataDictionary
→ 找到目标 WeaponData
→ 决定修改模板还是当前实例
→ 在 PlayerWeapons.Select / Player.Spawn 重新应用
```

### 回合

```text
找到 ModeBase 中触发 GameRoundEnd/ResetRound 的条件
→ Hook 条件或计时器
→ 不要只反复写 gameRoundOver
```

### 伤害

```text
Hook TakeDamage
→ 在正确阶段修改 DamageEventData
→ 保留原始事件和死亡广播
```

### 生命周期

```text
进入房间：重新取得所有单例和 Player
离开房间：清空所有裸指针、缓存和延迟任务
新回合：重新验证 Player/Weapon/Character
```

---

## 二十、运行时验证模板

对于任何“改了无效”的字段，按以下顺序记录：

```text
1. 修改前的值
2. 写入后的立即值
3. 下一帧的值
4. 触发换枪/复活/新回合后的值
5. 哪个函数第一次把值改回
```

判断结果：

| 现象 | 结论 |
|---|---|
| 写入后立即没变 | 地址、类型、保护或字段区错误 |
| 立即变化，下一帧恢复 | Update/事件持续覆盖 |
| 一直变化但游戏没反应 | 改的是缓存、显示值或未被使用的副本 |
| 换枪/复活后恢复 | 实例被替换或初始化函数覆盖 |
| 新房间失效 | 使用了旧 GameManager/Player 指针 |

推荐 Hook 写入监控点：

- 对目标地址设置写入断点；
- 找到第一个覆盖写入者；
- 追踪其上游数据来源；
- 优先修改生产者，而不是无限循环写最终字段。

---

## 二十一、最值得用于修改功能的成员

| 优先级 | 成员 | 适合开发的功能 |
|---:|---|---|
| 1 | `myPlayer` | 本地武器、位置、队伍、摄像机、生命 |
| 2 | `allPlayers`、`playersBL/GR` | 自瞄、ESP、聚怪、全员状态 |
| 3 | `PlayerSpawnEvent_Observers`、`MyPlayerSpawnEvent_Observers` | 复活后重新应用功能 |
| 4 | `WpnDictionary`、`WpnDataDictionary` | 武器数据、武器生成 |
| 5 | `GiveWeapon()`、`GetWeapon()` | 主动给武器和对象池研究 |
| 6 | `TakeDamage()` 和伤害阶段 Observer | 无敌、伤害倍率、命中记录 |
| 7 | `NewGameRoundStart_Observer`、`ResetRound()` | 回合功能和状态重置 |
| 8 | `gameMode`、`isNanoMode` | 模式判断，不建议战斗中单独切换 |
| 9 | `SetCharacter()` | 角色模型、生化角色切换研究 |
| 10 | `OnDestroy()` | 防止跨房间旧指针崩溃 |

---

## 二十二、完整结论

```text
GameManager 是本局玩家、武器、伤害事件和回合生命周期的总入口，
但许多字段只是列表、缓存、模板或事件引用。

字段可以写入，不代表游戏会使用这个值；
方法可以调用，不代表当前对象、参数、线程和生命周期满足条件。

遇到“调用无反应”时，先检查：
this、MethodInfo、参数、主线程、Singleton、资源加载和观察者。

遇到“字段恢复原值”时，先找：
哪个 Update、Spawn、Select、ResetRound 或对象池初始化重新写入。

最可靠的修改方式通常是：
找到真实数据生产者或生命周期事件进行 Hook，
而不是只修改最终缓存字段，或者把有参数的 IL2CPP 方法当作无参函数调用。
```

---

## 二十三、分析其他类时可复用的提示词

把下面的 `[类名]`、游戏名称和输出路径替换后，可以直接使用：

```text
请分析 Unity IL2CPP 游戏中的 `[类名]` 类。

资料位置：
1. dump.cs：
   D:\trae_project\ucf1.7-modifier\01-游戏逆向分析-相关信息\Il2CppDumper\dump.cs
2. IDA 导出汇编：
   D:\trae_project\ucf1.7-modifier\01-游戏逆向分析-相关信息\IDA-汇编代码\IDA导出-分割
3. 如果需要，可以连接 IDA MCP，对重点方法进行反编译、查看调用者和被调用方法。

游戏是 Unity IL2CPP 的穿越火线。
请从 Unity 生命周期、穿越火线实际游戏逻辑和 CE/Frida 修改角度分析。

请生成一个新的 Markdown 文档，不要覆盖原文档。

文档要求：

1. 在文档开头统计该类：
   - Fields 总数
   - 静态字段数量
   - 实例字段数量
   - public/private/protected 字段数量
   - Properties 数量
   - Methods 数量
   - 属性访问器、事件 add/remove、生命周期方法、业务方法数量
   - 嵌套 Delegate、枚举、结构体、协程状态机等例外类型

2. 全部成员必须列出，不能省略：
   - 全部静态字段
   - 全部实例字段
   - 全部属性
   - 全部方法
   - 全部事件和 Delegate
   - 编译器生成的 backing field 和协程状态机

3. 字段表至少包含：
   - 字段名
   - 类型
   - 静态/实例
   - 偏移
   - 穿越火线中的实际作用
   - 实际来源
   - 初始化方法
   - 主要读取者
   - 主要写入者/覆盖者
   - 是否可以读取
   - 是否可以修改
   - 修改后是否会被覆盖
   - 推荐修改方式
   - 风险
   - 结论依据

4. 属性表至少包含：
   - 属性名
   - getter/setter RVA
   - 实际数据来源
   - 是否只是计算值
   - backing field
   - 主要调用者
   - 修改数据源的方法

5. 方法表至少包含：
   - 方法签名
   - RVA
   - 静态/实例
   - 参数和返回值
   - 主要调用者
   - 主要被调用方法
   - 前置条件
   - 实际副作用
   - 能否使用 CE/Frida 主动调用
   - 正确 this、MethodInfo 和线程要求
   - 调用无反应的可能原因
   - 崩溃风险

6. 对修改游戏有价值的成员深入分析：
   - 给出完整调用链
   - 说明何时创建、何时更新、何时销毁
   - 说明字段为什么可能被游戏覆盖
   - 说明修改模板、缓存和实时实例的区别
   - 说明推荐 Hook 点

7. 不重要的成员也必须保留，用一句话说明用途。

8. 证据等级必须标记：
   - IDA 已确认
   - dump.cs 已确认
   - 根据调用关系推断

输出路径：
创建新的md文档


如果你不清楚怎么去设计，或者不知道输出哪些信息，你可以来问我，或者通过问我的方式去了解我的需求。
```
方便我学习了解熟悉游戏结构和信息
