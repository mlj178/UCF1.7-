# UnityCrossFire.dll 角色变身功能分析报告

## 1. 报告目的与范围

本报告针对 IDA Pro 当前打开的 `UnityCrossFire.dll`，只分析以下四条目标链路：

1. 玩家变身英雄
2. 玩家变身幽灵
3. Bot 变英雄
4. Bot 变幽灵

武器、弹药、移动速度、UI 绘制、聚怪等功能不在本报告范围内。

报告的用途是为后续复刻提供入口、调用关系、对象字段、角色参数和风险边界。文中将“IDA 直接证据”“已有 GameAssembly 静态分析证据”和“待动态验证的推断”分开标注。

## 2. 分析样本

| 项目 | 值 |
|---|---|
| 模块 | `UnityCrossFire.dll` |
| IDA 文件路径 | `D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire.dll` |
| ImageBase | `0x10000000` |
| Size | `0x64000` |
| FileSize | `0x5FC00` |
| MD5 | `2be82d9a5c9820a3ecc224b6b89e99b7` |
| SHA-256 | `3b5726a8ca661796c9b2904d5539d46aa0a26c24f309bf9349110251b6e50e92` |
| 架构 | x86 / 32 位 |
| 运行时关系 | Unity/IL2CPP 外部调用包装器，目标程序集为 `Assembly-CSharp` |

## 3. 总体结论

`UnityCrossFire.dll` 本身不是角色逻辑的实现主体，而是通过 IL2CPP/Mono 风格的运行时解析，取得 `Assembly-CSharp` 中方法或类型的地址，再在游戏进程中调用。

当前 DLL 可以直接确认的角色入口是：

```text
OpenMasterRole(Boolean isHero)
所属类型：NanoRoleSelect
程序集：Assembly-CSharp
```

底层类定义显示，`OpenMasterRole` 只负责打开“主角色”选择流程并设置默认选择状态；真正把 Player 更新成英雄或幽灵的代码位于 GameAssembly 的后续逻辑中。因此，复刻时不能只把 `OpenMasterRole` 当成“立即变身函数”。

当前 `UnityCrossFire.dll` 没有发现 `Bot`、`ClientData.isBot`、Bot 列表枚举或 Bot 专用变身方法名，也没有发现直接解析 `Mode_Nano4.BecomeHero` / `ModeBase_Nano.ChangeNanoGhostType` 的字符串入口。因此：

- 玩家英雄/幽灵：有明确的包装器入口和底层逻辑证据。
- Bot 英雄/幽灵：底层游戏代码具备对任意 `Player*` 执行角色更新的能力，但当前这个 DLL 没有完成目标 Bot 获取与调用链；需要另行补齐。

## 4. UnityCrossFire.dll 中的角色相关证据

### 4.1 运行时方法/类型字符串

IDA 字符串表中与角色链相关的条目：

| 地址 | 字符串 | 含义 |
|---|---|---|
| `0x100548D0` | `Void OpenMasterRole(Boolean isHero);` | 角色选择入口，带一个英雄/非英雄布尔参数 |
| `0x100548F8` | `NanoRoleSelect` | 目标类型名 |
| `0x10054908` | `Assembly-CSharp` | 目标程序集 |

相关初始化引用：

- `OpenMasterRole` 字符串操作数引用：`0x1000492E`
- `NanoRoleSelect` 字符串操作数引用：`0x10004962`
- `OpenMasterRole` 解析结果保存到全局槽位：`0x1005F704`
- `NanoRoleSelect` 相关解析/调用槽位：`0x1005F708`

### 4.2 角色动作调用点

IDA 代码中可确认的调用点：

```text
0x10005082  从 0x1005F708 取出 NanoRoleSelect 相关函数/对象获取链
0x10005090  间接调用
0x100050A2  call dword ptr [0x1005F704]
             即调用已解析的 OpenMasterRole
```

这说明 DLL 的主动作路径大致是：

```mermaid
flowchart LR
    A[UnityCrossFire.dll 动作处理] --> B[解析 Assembly-CSharp]
    B --> C[取得 NanoRoleSelect 相关对象/函数]
    C --> D[调用 OpenMasterRole bool]
    D --> E[打开主角色选择流程]
    E --> F[游戏原生选择逻辑]
    F --> G[BecomeHero 或 ChangeNanoGhostType]
```

`0x10005082` 附近的对象获取细节受当前 IDA 函数边界识别影响，建议后续在运行时断点确认第一个参数（`this`）究竟来自哪个 Player/NanoRoleSelect 实例。`0x100050A2` 的间接调用本身是直接证据。

## 5. NanoRoleSelect 对象布局

来自同版本 `GameAssembly` dump 的类定义：

```text
NanoRoleSelect +0x08  owner          Player*
NanoRoleSelect +0x0C  tableType      NanoRoleSelect.Type
NanoRoleSelect +0x10  closeTime      float
NanoRoleSelect +0x14  selection      int
NanoRoleSelect +0x18  closeWhenDead  bool
NanoRoleSelect +0x1C  Type_Listnner  delegate
```

`Player` 类中还存在：

```text
Player +0xA8  nanoRoleSelect      NanoRoleSelect*
```

这些字段是复刻时最重要的对象关系：

```text
Player* -> Player+0xA8 -> NanoRoleSelect*
NanoRoleSelect+0x08 -> owner Player*
```

实际版本若发生变化，应优先用运行时字段验证，不应只依赖固定偏移。

## 6. 玩家变身英雄

### 6.1 入口

包装器入口：

```text
NanoRoleSelect.OpenMasterRole(bool isHero)
```

GameAssembly 静态地址：

```text
RVA 0xB4ED30
VA  0x10B4ED30   （对应当前静态分析样本）
```

### 6.2 OpenMasterRole 的实际行为

GameAssembly 汇编可还原为：

```c
void NanoRoleSelect::OpenMasterRole(bool isHero)
{
    this->closeWhenDead = isHero;

    // isHero=true  -> type=2 -> Hero
    // isHero=false -> type=3 -> Terminator
    int type = (!isHero) + 2;

    this->Open(type, 5.0f);
    this->selection = 1;
}
```

关键常量：

- `5.0f`：选择流程持续时间
- `type=2`：`NanoRoleSelect.Type.Hero`
- `type=3`：`NanoRoleSelect.Type.Terminator`
- `selection=1`：默认选择项

### 6.3 英雄真正落地

`NanoRoleSelect.SelectHero` 位于：

```text
RVA 0xB4EDE0
VA  0x10B4EDE0
```

其核心逻辑是：

```text
Mode_Nano4.BecomeHero(
    this->owner,
    this->selection + 0x16,
    textTip=true
)
```

由于 `OpenMasterRole` 把 `selection` 设置为 `1`，默认英雄角色值为：

```text
1 + 0x16 = 0x17 = 23
NanoRole.MasterHumanHero = 23
```

因此玩家变英雄有两种复刻方向：

1. 复刻原生流程：取得本地玩家的 `NanoRoleSelect*`，调用 `OpenMasterRole(true)`，再让原生选择确认流程触发 `SelectHero`。
2. 直接复刻结果：取得目标 `Player*`，解析 `Mode_Nano4.BecomeHero`，传入目标 Player 和目标英雄 `NanoRole` 值。

当前 `UnityCrossFire.dll` 直接确认的是第 1 条入口；第 2 条需要新增方法解析或使用已存在的 GameAssembly 地址链。

## 7. 玩家变身幽灵

### 7.1 原生幽灵入口

`NanoRoleSelect.SelectNanoGhost` 位于：

```text
RVA 0xB4EE90
VA  0x10B4EE90
```

该函数以 `NanoRoleSelect.owner` 作为目标 Player，并根据 `selection` 转换为幽灵角色值：

| selection | 传给 ChangeNanoGhostType 的角色值 | NanoRole |
|---:|---:|---|
| `1` | `7` | `Psycho` |
| `2` | `3` | `Nurse` |
| `6` | `2` | `Hulk` |

随后调用：

```text
ModeBase_Nano.ChangeNanoGhostType(owner, role)
```

### 7.2 幽灵更新链

`ChangeNanoGhostType` 的核心行为：

```text
1. 读取 Player.nanoRole
2. 如果新旧角色不同，调用 ModeBase_Nano.UpdateNanoRole(player, newRole)
3. 如果 player.isMyPlayer 为真，播放变身出现音效
4. 对特定旧角色触发后续状态通知
```

该函数没有“只能作用于真人玩家”的硬编码判断；它接收的是一个 `Player*`。这为 Bot 变幽灵提供了底层可行性，但前提是能够取得有效的 Bot Player 指针。

## 8. Bot 变英雄 / Bot 变幽灵

### 8.1 当前 DLL 中的结论

在 `UnityCrossFire.dll` 的字符串、全局引用和已定位的角色方法解析链中，没有发现：

- `Bot` 类型解析
- `ClientData` 类型解析
- `isBot` 字段名或判断链
- `GameManager.allPlayers` / Bot 列表枚举
- `Mode_Nano4.BecomeHero` 的直接解析字符串
- `ModeBase_Nano.ChangeNanoGhostType` 的直接解析字符串
- `SelectHero` / `SelectNanoGhost` 的直接解析字符串

因此不能把当前 DLL 报告为“已经支持 Bot 变身”。准确结论是：

```text
当前 DLL 已实现/暴露主角色选择入口；
Bot 目标选择和 Bot 变身调用尚未在该 DLL 中闭合。
```

### 8.2 底层可复用性

底层 GameAssembly 的 `ChangeNanoGhostType(ModeBase_Nano*, Player*, int role)` 不检查 `isBot`，而是直接对传入 Player 执行角色更新。因此 Bot 变幽灵的复刻方案可以是：

```text
枚举目标 Bot Player*
    -> 过滤有效、存活、isBot=1 的对象
    -> 调用 ChangeNanoGhostType(modeNano, botPlayer, role)
```

英雄路径同理，应对每个 Bot Player 调用：

```text
Mode_Nano4.BecomeHero(modeNano4, botPlayer, heroRole, textTip)
```

但 Bot 英雄/幽灵的“目标 Player 枚举”和“主线程调用时机”目前不在 `UnityCrossFire.dll` 的已确认链路内，必须动态验证：

- Bot Player 是来自 `GameManager.allPlayers`，还是 Nano 模式专用列表；
- `isBot` 应从 `ClientData +0x1C` 读取，还是使用 Bot 组件/回调判断；
- 调用是否必须在 Unity 主线程；
- 角色更新是否会被回合逻辑、服务器同步或 Bot 自身回调覆盖。

### 8.3 Bot 链路建议

建议把 Bot 功能设计成独立模块，不修改现有玩家入口：

```text
PlayerRoleTransform
├── transformLocalHero()
├── transformLocalGhost(role)
├── enumerateBotPlayers()
├── transformBotHero(bot, heroRole)
└── transformBotGhost(bot, ghostRole)
```

其中 `enumerateBotPlayers()` 必须先完成目标验证，再接入角色调用。不要仅凭“Hook 返回值”判断目标 Player；已有工程经验表明，Bot 和本地玩家的返回值可能相同，应调用游戏原生 `Player.get_isMyPlayer` 或直接读取已验证的 `ClientData.isBot`。

## 9. 四条功能复刻矩阵

| 功能 | 当前 DLL 直接入口 | 底层目标 | 当前状态 | 复刻优先级 |
|---|---|---|---|---:|
| 玩家变英雄 | `OpenMasterRole(true)` | `Mode_Nano4.BecomeHero` | 入口已确认，确认动作需动态验证 | 1 |
| 玩家变幽灵 | `OpenMasterRole(false)` + 原生选择链 | `ChangeNanoGhostType` | 底层映射已确认，包装器是否自动确认需验证 | 2 |
| Bot 变英雄 | 未发现 Bot 专用入口 | `Mode_Nano4.BecomeHero(botPlayer, role)` | 当前 DLL 未闭合 | 3 |
| Bot 变幽灵 | 未发现 Bot 专用入口 | `ChangeNanoGhostType(mode, botPlayer, role)` | 底层可行，目标枚举缺失 | 4 |

## 10. 动态验证清单

后续在真实游戏房间中建议按以下顺序验证：

1. 对 `0x100050A2` 下断点，确认 `OpenMasterRole` 的第一个参数是否为 `NanoRoleSelect*`。
2. 观察 `NanoRoleSelect +0x08` 是否等于本地 `Player*`。
3. 调用 `OpenMasterRole(true)` 后，观察 `+0x0C`、`+0x10`、`+0x14`、`+0x18` 的变化。
4. 确认 `selection=1` 时是否最终进入 `SelectHero` 并得到角色值 `23`。
5. 对 `ChangeNanoGhostType` 设置断点，记录幽灵角色值与目标 Player 指针。
6. 枚举 Bot 时同时记录 `Player*`、`ClientData*`、`ClientData+0x1C` 和 `Player.nanoRole`。
7. 确认 Bot 角色更新是否被下一帧 AI/回合逻辑覆盖。
8. 确认所有角色调用是否需要主线程调度，以及退出房间时是否需要清理 Hook/缓存。

## 11. 最终复刻建议

推荐先完成“玩家英雄”和“玩家幽灵”的原生入口复刻，再单独实现 Bot 目标枚举。不要一开始直接改 `Player.nanoRole` 字段，因为原生更新链还负责模型、状态、音效和模式同步；应优先调用 `BecomeHero` / `ChangeNanoGhostType`，让游戏自身完成伴随状态更新。

对当前 DLL 的最小改造方向是：

```text
保留现有：Assembly-CSharp 解析、NanoRoleSelect 获取、OpenMasterRole 调用
新增：GameManager/Player/Bot 目标枚举
新增：Mode_Nano4.BecomeHero 解析
新增：ModeBase_Nano.ChangeNanoGhostType 解析
新增：主线程调度、目标有效性检查、房间退出清理
```

## 12. 证据等级说明

| 等级 | 本报告含义 |
|---|---|
| A | 当前 IDA 数据库中有明确字符串、交叉引用或间接调用证据 |
| B | 同版本 GameAssembly 静态汇编/`dump.cs` 已直接还原 |
| C | 基于 A+B 的复刻推断，需要运行时断点确认 |

本报告中 `OpenMasterRole` 的字符串、解析槽位和 `0x100050A2` 调用点属于 A 级；`OpenMasterRole`、`SelectHero`、`SelectNanoGhost` 和 `ChangeNanoGhostType` 的角色分流属于 B 级；Bot 目标枚举与线程调度属于 C 级。
