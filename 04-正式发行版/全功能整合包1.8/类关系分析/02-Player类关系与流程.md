# Player 类关系与流程

> 目标：从穿越火线实战角度理解一名 `Player` 如何组合资料、生命、移动、视角、武器、模型、技能和复活流程。  
> 上游文档：[GameManager 类关系与流程](01-GameManager类关系与流程.md)

## 一、先用一句话理解

`Player` 是地图中真正存在的一名战斗角色。

它不是单独完成所有功能，而是一个组合中心：

- 从父类 `Entity` 继承生命、队伍、Buff、受伤和死亡基础能力。
- 使用 `ClientData` 保存进入战斗前的昵称、阵营、角色和背包资料。
- 持有 `PlayerVelocity`、`PlayerWeapons`、`PlayerSkills` 等运行时子系统。
- 持有 `CharacterModel` 表现第三人称角色和受击部位。
- 真人由 `PlayerController` 控制；Bot 则由 `Bot.thisPlayer` 指向并控制。

## 二、A：以 Player 为中心的分层预览

```mermaid
flowchart TB
    subgraph INPUT["上游：谁创建和控制 Player"]
        direction TB
        GM["GameManager<br/>创建、登记和伤害入口"]
        BOT["Bot / PlayerController<br/>AI 或真人输入"]
        MODE["ModeBase / Mode_*<br/>死亡、复活和回合规则"]
    end

    P["Player<br/>一名战场角色"]

    subgraph DATA["内部资料与战斗基础"]
        direction TB
        E["Entity<br/>生命、队伍、Buff 和死亡"]
        CD["ClientData / PlayerData<br/>房间资料和对局战绩"]
    end

    subgraph SYSTEM["下游运行时系统"]
        direction TB
        MOVE["PlayerInput / PlayerVelocity"]
        COMBAT["PlayerWeapons / PlayerSkills"]
        VIEW["CharacterModel / PlayerCameraManager"]
    end

    GM --> P
    BOT --> P
    MODE --> P
    P --> E
    P --> CD
    P --> MOVE
    P --> COMBAT
    P --> VIEW
```

### Player 持有的资料

```mermaid
flowchart TB
    P["Player<br/>战场中的角色实例"]
    CD["ClientData<br/>昵称、阵营、Bot、角色和背包资料"]
    PD["PlayerData<br/>战绩、观察模式和生化状态"]

    P -->|"clientData"| CD
    P -->|"playerData"| PD
```

### Player 持有的运行时系统

```mermaid
flowchart TB
    P["Player<br/>战场中的角色实例"]

    subgraph CONTROL["输入与移动"]
        direction TB
        PI["PlayerInput<br/>鼠标、跳跃等输入状态"]
        PV["PlayerVelocity<br/>速度、重力、冲刺和移动方向"]
    end

    subgraph COMBAT["武器与技能"]
        direction TB
        PW["PlayerWeapons<br/>武器槽和当前武器"]
        WB["WeaponBag<br/>背包配置和当前背包"]
        PS["PlayerSkills<br/>技能槽与技能使用"]
    end

    subgraph DISPLAY["角色与视角表现"]
        direction TB
        CM["CharacterModel<br/>模型、动画和受击部位"]
        PCM["PlayerCameraManager<br/>第一人称模型和 FOV"]
    end

    P -->|"input"| PI
    P -->|"velData"| PV
    P -->|"wpns"| PW
    P -->|"weaponBag"| WB
    P -->|"skills"| PS
    P -->|"currentCharacter"| CM
    P -->|"cameraManager"| PCM
```

### 最重要的认识

`Player` 是组合对象，不是单一数据结构：

```text
Player = Entity 基础战斗状态
       + ClientData 房间资料
       + PlayerData 对局统计
       + PlayerVelocity 移动速度
       + PlayerWeapons 武器系统
       + CharacterModel 角色表现
       + PlayerSkills 模式技能
```

## 三、C：分层学习地图

```mermaid
flowchart TB
    P["Player"]
    L1["第 1 层：继承基础<br/>Entity 的生命、队伍和 Buff"]
    L2["第 2 层：身份数据<br/>ClientData 与 PlayerData"]
    L3["第 3 层：运行时子系统<br/>移动、输入、武器、技能和模型"]
    L4["第 4 层：战斗生命周期<br/>创建、出生、受伤、死亡、复活、销毁"]
    L5["第 5 层：控制来源<br/>真人输入、Bot AI、模式规则"]
    L6["第 6 层：修改入口<br/>真实数据源、刷新点和清理点"]

    P --> L1
    P --> L2
    P --> L3
    P --> L4
    P --> L5
    P --> L6
```

### 3.1 第一层：Player 从 Entity 继承什么

```mermaid
flowchart TD
    E["Entity"]
    LIFE["healthData / isDead / isInvincible"]
    TEAM["team / team_Listenner"]
    MOVE["baseMoveSpeed / speedPenalty"]
    DAMAGE["damageRate / OnEntityHurt / OnEntityDeath"]
    BUFF["buffs / AddBuff / CleanAllBuff"]
    PHYSICS["characterController / characterAnimator"]
    P["Player"]

    E --> LIFE
    E --> TEAM
    E --> MOVE
    E --> DAMAGE
    E --> BUFF
    E --> PHYSICS
    P -->|"继承并覆盖部分方法"| E
```

| 功能 | 实际定义位置 | Player 如何使用 |
| --- | --- | --- |
| 队伍 | `Entity.team +0x20` | 加入 `playersBL/GR` 和敌我判断 |
| 生命 | `Entity.healthData +0x1C` | 受伤、死亡、复活 |
| 死亡状态 | `Entity.isDead` | AI、模式和 HUD 判断 |
| 移动基础值 | `Entity.baseMoveSpeed +0x0C` | `Player.GetMoveSpeed()` 继续计算 |
| 无敌 | `Entity.isInvincible +0x18` | 出生保护和 Buff |
| Buff | `Entity.buffs +0x34` | 减速、伤害倍率和无敌等 |

因此，不能只扫描 `Player` 自己声明的字段。`Player* + 0x20` 的 `team` 来自父类 `Entity`。

### 3.2 第二层：身份资料与对局统计

```mermaid
flowchart LR
    CD["ClientData<br/>进入战斗前的资料"] --> P["Player"]
    P --> PD["PlayerData<br/>进入战斗后的统计状态"]

    CD --> C1["nickName / level / vipLevel"]
    CD --> C2["joinTeam / isBot / character"]
    CD --> C3["wpnBags / itemList"]

    PD --> D1["playerID / spawnCount"]
    PD --> D2["kill / death / score / survival"]
    PD --> D3["observeMode / revengeTarget"]
    PD --> D4["nanoRole / nanoExp"]
```

区别：

| 类型 | 主要阶段 | 示例 |
| --- | --- | --- |
| `ClientData` | 房间准备和进场初始化 | 昵称、选择阵营、角色、武器背包、是否 Bot |
| `PlayerData` | 对局运行 | 击杀、死亡、分数、出生次数、观察模式 |

`Player.nickName`、`level` 和 `vipLevel` 是属性，实际会回到 `player.clientData` 读取。

### 3.3 第三层：Player 直接持有的运行时子系统

| Player 字段 | 偏移 | 指向 | 穿越火线功能 |
| --- | ---: | --- | --- |
| `cameraManager` | `0x48` | `PlayerCameraManager` | 第一人称模型、FOV、狙击镜和震屏 |
| `cameraRotation` | `0x4C` | `Vector2` | 该 Player 的横向和纵向视角角度 |
| `currentCharacter` | `0x5C` | `CharacterModel` | 当前角色模型、动画和受击部位 |
| `velData` | `0x90` | `PlayerVelocity` | 速度、冲刺、重力和移动方向 |
| `clientData` | `0x94` | `ClientData` | 玩家进场资料 |
| `playerData` | `0x98` | `PlayerData` | 对局统计和模式状态 |
| `input` | `0x9C` | `PlayerInput` | 鼠标和跳跃等输入状态 |
| `wpns` | `0xA0` | `PlayerWeapons` | 武器槽、当前武器和切枪 |
| `weaponBag` | `0xA4` | `WeaponBag` | 武器背包配置 |
| `skills` | `0xB0` | `PlayerSkills` | 生化等模式的技能 |
| `modelInfo` | `0xB4` | `PlayerMdlInfo` | 第一/第三人称模型颜色和材质 |

#### Awake 中实际创建的对象

```mermaid
flowchart TD
    AW["Player.Awake()<br/>RVA 0xB4FEF0"]
    BASE["Entity.Awake()"]
    CHAR["查找 Characters 容器"]
    VEL["new PlayerVelocity(this)<br/>写入 +0x90"]
    WPNS["new PlayerWeapons(this)<br/>写入 +0xA0"]
    SKILL["new PlayerSkills(this)<br/>写入 +0xB0"]
    NANO{"是否生化模式"}
    ROLE["创建 NanoRoleSelect"]
    N4T["Nano4T 模式创建 Nano4T_Data"]

    AW --> BASE
    BASE --> CHAR
    CHAR --> VEL
    VEL --> WPNS
    WPNS --> SKILL
    SKILL --> NANO
    NANO -->|"是"| ROLE
    ROLE --> N4T
```

IDA 直接依据：

- `0x10B4FF54` 调用 `Entity.Awake()`。
- `0x10B4FFB7` 构造 `PlayerVelocity(this)`，写入 `Player + 0x90`。
- `0x10B4FFDC` 构造 `PlayerWeapons(this)`，写入 `Player + 0xA0`。
- `0x10B50004` 构造 `PlayerSkills(this)`，写入 `Player + 0xB0`。

### 3.4 第四层：战斗生命周期

```mermaid
flowchart TD
    CREATE["GameManager.AddPlayer()<br/>实例化 Player Prefab"]
    AW["Player.Awake()<br/>创建运行时子系统"]
    DATA["GameManager.AddPlayers()<br/>写入 ClientData 和 WeaponBag"]
    CHAR["GameManager.SetCharacter()<br/>绑定 CharacterModel"]
    SPAWN["Player.Spawn()<br/>加入存活列表并进入战斗"]
    FIGHT["移动、视角、武器和技能更新"]
    HURT["Player.OnEntityHurt()"]
    DEATH["Player.OnEntityDeath()"]
    RESP["Player.Respawn(delay)"]
    DESTROY["Player.OnDestroy()<br/>离开房间或销毁对象"]

    CREATE --> AW
    AW --> DATA
    DATA --> CHAR
    CHAR --> SPAWN
    SPAWN --> FIGHT
    FIGHT --> HURT
    HURT -->|"生命仍大于 0"| FIGHT
    HURT -->|"死亡"| DEATH
    DEATH -->|"模式允许复活"| RESP
    RESP --> SPAWN
    FIGHT -->|"离开战斗场景"| DESTROY
```

### 3.5 第五层：谁在控制 Player

```mermaid
flowchart TB
    P["Player"]

    HUMAN["真人控制路径"]
    AI["Bot 控制路径"]
    RULE["规则控制路径"]

    PC["PlayerController<br/>读取按键和鼠标"]
    BOT["Bot<br/>寻敌、寻路、转向、切枪和攻击"]
    MODE["ModeBase / Mode_*<br/>出生、死亡、复活和胜负"]

    HUMAN --> PC
    PC --> P
    AI --> BOT
    BOT -->|"thisPlayer"| P
    RULE --> MODE
    MODE --> P
```

本机玩家与其他玩家使用同一个 `Player` 类。区别主要来自：

- `GameManager.myPlayer` 指向哪个 Player。
- `Player.get_isMyPlayer()` 的判断。
- `CameraManager` 当前聚焦哪个 Player。
- 真人是否有 `PlayerController` 输入控制。
- Bot Prefab 是否带有 `Bot` 组件。

### 3.6 第六层：开发时修改哪一层

```mermaid
flowchart TB
    Q["想修改 Player 相关功能"] --> TYPE{"先判断真实拥有者"}

    subgraph TARGETS["选择数据和行为所在层"]
        direction TB
        ID["昵称、等级、阵营和背包<br/><b>ClientData</b>"]
        LIFE["血量、队伍、无敌和 Buff<br/><b>Entity / HealthData</b>"]
        MOVE["移动、冲刺和重力<br/><b>PlayerVelocity / Player</b>"]
        VIEW["视角和第一人称相机<br/><b>cameraRotation / PlayerCameraManager</b>"]
        WPN["武器槽与当前武器<br/><b>PlayerWeapons / Weapon</b>"]
        MODEL["角色模型和受击部位<br/><b>CharacterModel</b>"]
        SCORE["击杀、死亡和分数<br/><b>PlayerData / Mode_*</b>"]
    end

    TYPE --> ID
    TYPE --> LIFE
    TYPE --> MOVE
    TYPE --> VIEW
    TYPE --> WPN
    TYPE --> MODEL
    TYPE --> SCORE
```

## 四、专题业务链

### 4.1 移动和视角链

```mermaid
flowchart TD
    CONTROL["PlayerController 或 Bot"]
    MOVE["MoveByLocalDirection(x, z)"]
    VEL["PlayerVelocity.Update(x, z)"]
    SPEED["GetMoveSpeed()<br/>基础速度、Buff 和武器惩罚"]
    PHYS["PhysicalUpdate()<br/>CharacterController 移动"]
    ROT["AddCameraRotation / LookAt"]
    CAM["UpdateCameraRotaion()<br/>PlayerCameraManager"]

    CONTROL --> MOVE
    MOVE --> VEL
    VEL --> SPEED
    SPEED --> PHYS
    CONTROL --> ROT
    ROT --> CAM
```

### 4.2 武器链

```mermaid
flowchart TD
    CD["ClientData.wpnBags"] --> WB["WeaponBag.LoadData()"]
    WB --> SEL["Player.SelectWeaponBag()"]
    SEL --> GIVE["GameManager.GiveWeaponByBag()"]
    GIVE --> SET["Player.SetWeapon(Weapon)"]
    SET --> PW["PlayerWeapons.SetWeapon()"]
    PW --> USE["inUse / curSlot"]
    USE --> FIRE["Weapon 开火、换弹或近战"]
```

### 4.3 角色模型链

```mermaid
flowchart TD
    CD["ClientData.character"] --> GM["GameManager.SetCharacter()"]
    GM --> MODEL["从 characterPool 获取 CharacterModel"]
    MODEL --> SET["Player.SetCharacter(model)"]
    SET --> OWNER["CharacterModel.SetOwner(Player)"]
    OWNER --> INFO["PlayerMdlInfo.AddModel()"]
    INFO --> ACTIVE["CharacterModelSetting()<br/>根据观察模式和生死切换"]
```

### 4.4 死亡和复活链

```mermaid
flowchart TD
    DMG["GameManager.TakeDamage()"] --> HURT["Player.OnEntityHurt()"]
    HURT --> DEAD{"死亡？"}
    DEAD -->|"否"| CONTINUE["继续战斗"]
    DEAD -->|"是"| DEATH["Player.OnEntityDeath()"]
    DEATH --> DROP["清地图交互和死亡掉枪"]
    DROP --> LIST["移出存活列表"]
    LIST --> RULE["Mode_* 处理击杀和复活规则"]
    RULE --> RESP["Player.Respawn(time)"]
    RESP --> SPAWN["Player.Spawn()"]
    SPAWN --> ALIVE["重新加入存活列表<br/>恢复模型、武器和出生保护"]
```

## 五、B：一名玩家的完整游戏流程

```mermaid
sequenceDiagram
    participant GM as GameManager
    participant P as Player
    participant CD as ClientData
    participant W as PlayerWeapons
    participant M as CharacterModel
    participant Mode as ModeBase / Mode_*

    GM->>P: 实例化 playerPrefab 或 botPrefab
    P->>P: Awake() 调用 Entity.Awake()
    P->>P: 创建 PlayerVelocity、PlayerWeapons、PlayerSkills
    GM->>P: 写入 clientData
    GM->>CD: Update() 派生装备能力
    GM->>P: WeaponBag.LoadData(clientData)
    GM->>M: 取得角色模型
    GM->>P: SetCharacter(model)
    Mode->>P: Spawn()
    P->>W: 选择背包和当前武器
    loop 每帧战斗
        P->>P: 输入、速度、物理、视角和 Buff 更新
        W->>GM: 武器造成 DamageEventData
        GM->>P: OnEntityHurt()
    end
    GM->>P: OnEntityDeath()
    Mode->>P: Respawn(delay)
    P->>P: Spawn()
    GM->>P: 离房时销毁
    P->>P: OnDestroy() 清理监听和父类状态
```

## 六、最重要的对象访问路径

```text
GameManager.myPlayer 或 GameManager.allPlayers[i]
└─ Player
   ├─ 继承 Entity
   │  ├─ +0x1C -> healthData
   │  └─ +0x20 -> team
   ├─ +0x48 -> cameraManager
   ├─ +0x4C -> cameraRotation
   ├─ +0x5C -> currentCharacter
   ├─ +0x90 -> velData
   ├─ +0x94 -> clientData
   ├─ +0x98 -> playerData
   ├─ +0x9C -> input
   ├─ +0xA0 -> wpns
   ├─ +0xA4 -> weaponBag
   ├─ +0xB0 -> skills
   └─ +0xB4 -> modelInfo
```

## 七、常见误解

### Player 自己有没有 `isEnemy` 字段

没有看到通用 `Player.isEnemy` 字段。团队模式通常根据继承自 `Entity` 的 `team` 比较；个人竞技和生化模式还必须结合具体 `Mode_*` 规则。

### Bot.thisPlayer 能不能替代 allPlayers

不能。`Bot.thisPlayer` 只表示某个 Bot 组件控制的 Player；真人 Player 没有 Bot 控制器。枚举全部玩家仍应从 `GameManager.allPlayers` 或阵营列表开始。

### `cameraRotation` 为什么是这个 Player 的

它是 `Player` 实例字段 `+0x4C`。从 `GameManager.myPlayer` 取得的 Player 再读取该字段，才是本机玩家视角；从敌方 Player 读取则是敌方角色自己的视角状态。

### Player 死亡后会重新 AddPlayer 吗

正常复活使用 `Respawn()` 和 `Spawn()`，不会重新创建 Player。`AddPlayer()` 主要用于初次创建参战对象。

### 为什么长期缓存 Player 地址会出问题

离开房间后 `Player.OnDestroy()` 和 `GameManager.OnDestroy()` 会执行。旧地址即使仍可读，也不再代表新房间的有效 Player。

## 八、证据索引

| 证据 | dump/IDA 位置 |
| --- | --- |
| `Player : Entity` | `dump.cs` TypeDefIndex 5171 |
| Entity 的生命和队伍字段 | `dump.cs` TypeDefIndex 5161 |
| `Player.Awake()` | RVA `0xB4FEF0` |
| 创建 `PlayerVelocity(this)` | IDA `0x10B4FFB7`，写入 `+0x90` |
| 创建 `PlayerWeapons(this)` | IDA `0x10B4FFDC`，写入 `+0xA0` |
| 创建 `PlayerSkills(this)` | IDA `0x10B50004`，写入 `+0xB0` |
| `Player.OnDestroy()` | RVA `0xB511C0` |
| `Player.OnEntityDeath()` | RVA `0xB51210` |
| `Player.OnEntityHurt()` | RVA `0xB516B0` |
| `Player.Respawn()` | RVA `0xB527A0` |
| `Player.SelectWeaponBag()` | RVA `0xB52830` |
| `Player.SetCharacter()` | RVA `0xB52AD0` |
| `Player.SetWeapon()` | RVA `0xB53650` |

## 九、读完后应该能够回答

1. Player 和 Entity 为什么要分成两个类？
2. ClientData 与 PlayerData 分别保存什么？
3. Player 的移动、武器、技能和模型分别由哪个对象负责？
4. 真人和 Bot 为什么可以使用同一个 Player 类？
5. 本机视角应该从哪个 Player 开始读取？
6. 死亡复活为什么不会重新执行 AddPlayer？
7. 修改血量、移动、武器和模型时应该分别进入哪一层？
