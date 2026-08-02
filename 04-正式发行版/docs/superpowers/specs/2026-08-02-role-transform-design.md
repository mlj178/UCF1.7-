# 角色变身按钮设计

## 目标

在 `05-正式功能/34-角色变身/` 实现四个即时动作按钮：

| 按钮 | 目标 | 角色决定方式 |
| --- | --- | --- |
| 本地玩家：选择英雄 | 本地玩家 | 打开游戏原生英雄选择界面，由玩家选择 |
| 本地玩家：选择超级终结者 | 本地玩家 | 打开游戏原生超级终结者选择界面，由玩家选择 |
| 所有 Bot：随机英雄 | 当前存活 Bot | 调用游戏原生随机英雄逻辑 |
| 所有 Bot：随机超级终结者 | 当前存活 Bot | 调用游戏原生随机超级终结者逻辑 |

按钮不要求地图上存在箱子，不生成或回收实体箱子，也不附带蓝箱的经验、弹药、回血、Buff 或层数效果。

## 已确认的游戏链路

### 真实蓝箱链路

`dump.cs` 和 IDA Pro MCP 已确认：

```text
SupplyBox.Type.Blue = 2

SupplyBox.OnTriggerStay                         RVA 0xB217E0
  -> SupplyBox.CanPickUp
  -> RecyclableObject.TryRecycle
  -> ModeBase_Nano.instance2
  -> 虚函数槽 49 OnPlayerPickUpSupplyBox
  -> Mode_Nano4_Terminator.OnPlayerPickUpSupplyBox
                                                 RVA 0xB444B0
```

完整蓝箱回调还会处理经验、弹药、回血、Buff、箱子层数、当前阵营和角色状态，因此本功能不直接调用完整拾箱回调。

### 本地玩家选择链路

`Player.nanoRoleSelect` 位于 `Player + 0xA8`。原生选择入口是：

```text
NanoRoleSelect.OpenMasterRole(bool isHero)       RVA 0xB4ED30
```

该方法调用 `Open(type, 5.0)`，打开游戏原生选择界面五秒。

英雄路径：

```text
OpenMasterRole(true)
  -> NanoRoleSelect.Type.Hero = 2
  -> 玩家选择 1..5
  -> NanoRoleSelect.SelectHero                    RVA 0xB4EDE0
  -> role = selection + 22                        角色 23..27
  -> Mode_Nano4.BecomeHero                        RVA 0xB412F0
```

超级终结者路径：

```text
OpenMasterRole(false)
  -> NanoRoleSelect.Type.Terminator = 3
  -> 玩家选择 1..5
  -> NanoRoleSelect.SelectTerminator              RVA 0xB4EF90
  -> role = selection + 12                        角色 13..17
  -> Mode_Nano4.BecomeMasterTerminator            RVA 0xB41580
```

### Bot 随机链路

Bot 英雄使用原生随机入口：

```text
Mode_Nano4_Terminator.BecomeRandomMasterHero
                                                 RVA 0xB42E90
  -> 游戏原生随机算法
  -> Mode_Nano4.BecomeHero
```

Bot 超级终结者使用原生随机入口：

```text
Mode_Nano4_Terminator.TryBecomeRandomMasterTerminator
                                                 RVA 0xB45B90
  -> UnityEngine.Random.RandomRangeInt(0, 5)
  -> 角色 13..17
  -> Mode_Nano4.BecomeMasterTerminator
```

本功能不在 JavaScript 中复制随机算法，以游戏原生结果为准。

## 方案选择

### 未采用：调用完整蓝箱回调

该方式最接近真实拾箱，但会产生本功能明确排除的附带奖励和状态变化。

### 未采用：从 Frida RPC 线程直接调用游戏函数

现有代码采用该方式。它虽然短，但会从非游戏主线程触碰选择界面、玩家对象和模式对象，存在卡死或闪退风险，也违反项目生命周期规范。

### 采用：RPC 提交动作，游戏主线程消费

`trigger(action)` 只写入一次性 pending 动作。脚本 Hook `ModeBase.Update`（RVA `0xAF6A00`），在下一帧游戏主线程重新解析当前对象并执行动作。

## 运行架构

```text
CustomTkinter 按钮
  -> trigger(action) RPC
  -> Runtime.pendingAction
  -> ModeBase.Update Hook（游戏主线程）
  -> 取出并立即清空 pendingAction
  -> 重新取得 Mode_Nano4、GameManager 和目标玩家
  -> 执行对应的原生选择或随机变身入口
  -> 更新 Runtime.stats 和日志
```

允许的动作固定为：

```text
local_hero
local_terminator
bot_hero
bot_terminator
```

若已有动作尚未消费，新请求返回“动作处理中”，不得覆盖或累积动作。

## 对象解析与目标筛选

每次消费动作时重新解析对象，不跨帧、跨房间缓存 `Player*`、`Mode_Nano4*` 或 `GameManager*`。

- 当前模式：`Mode_Nano4.get_instance3`，RVA `0xB467A0`。
- 本地玩家：`GameManager` TypeInfo 静态字段中的 `myPlayer`。
- GameManager 实例：调用 `Singleton<GameManager>.get_instance` 的共享泛型实现 RVA `0x4A8170`，并传入全局 `Method$Singleton_GameManager__get_instance__`（RVA `0xE1CE64`）在运行时保存的真实 `MethodInfo*`。
- 玩家数组：`GameManager.allPlayers + 0x1C`。
- Bot 身份：`Player.clientData + 0x94 -> ClientData.isBot + 0x1C`。
- 本地身份复核：`Player.get_isMyPlayer`，RVA `0xB55FD0`。

Bot 批量动作只处理按钮点击时存在、指针有效、身份明确且存活的 Bot。死亡或正在重生的 Bot 跳过，避免向未来重生事件注册延迟变身。

## 生命周期

核心脚本保留单一 `Runtime`，包含：

```text
feature_id
enabled
initialized
generation
hooks
pendingAction
stats
```

- `enable`：安装一次 `ModeBase.Update` Hook，并启用动作处理。
- `trigger`：校验动作名和当前状态，只提交 pending，不调用运行态游戏函数。
- `disable`：停止处理、清空 pending、移除 Hook、递增 generation。
- `cleanup`：可重复执行；效果与完整 disable 相同，并增加 cleanup 统计。
- `status`：返回结构化状态、pending、最后动作、成功/跳过计数、Bot 扫描结果和最后错误。
- `setConfig`：为标准 RPC 兼容保留；本功能没有持久布尔开关，不接受会改变四个动作语义的配置。

动作在当前帧无法执行时立即失败并丢弃，不跨房间等待。这样可避免在大厅点击后进入房间突然变身。

## UI

保留现有 CustomTkinter 测试 UI 的后台连接、消息队列、RPC 锁、日志和安全卸载结构，删除补给箱探测开关和四个 BooleanVar 配置。

界面固定显示：

```text
本地玩家：选择英雄
本地玩家：选择超级终结者
所有 Bot：随机英雄
所有 Bot：随机超级终结者
读取状态
```

按钮只调用 `trigger(action)`；游戏内角色选择由原生 UI 完成。

## 错误处理与可观测性

以下情况只记录失败，不调用变身函数：

- 功能未启用或 Hook 尚未安装；
- 当前不是有效的 `Mode_Nano4`；
- 本地玩家、`nanoRoleSelect`、GameManager 或玩家数组为空；
- Bot 指针无效、不是 Bot、已死亡或正在重生；
- 动作名无效或已有 pending 动作。

`status()` 至少提供：pending 动作、最后请求、最后完成动作、主线程消费次数、本地选择界面打开次数、Bot 扫描/成功/跳过数量、错误数量和最后错误。

## 测试与验收

自动验证：

- `node --check` 验证核心 JavaScript 语法；
- `python -m py_compile` 验证 CustomTkinter UI；
- 标准库静态测试验证四个动作、pending 主线程链、关键 RVA、标准 RPC、可重复 cleanup，以及代码中不存在完整蓝箱回调调用和直接写 `Player.nanoRole`。

游戏内验收：

1. 本地英雄按钮打开原生英雄选择界面，可选择角色 23..27。
2. 本地超级终结者按钮打开原生终结者选择界面，可选择角色 13..17。
3. Bot 英雄按钮对所有存活 Bot 使用原生随机英雄入口。
4. Bot 超级终结者按钮对所有存活 Bot 使用原生随机超级终结者入口。
5. 四条路径均不生成/回收箱子，不增加箱子层数、经验、弹药、回血或 Buff。
6. 快速重复点击不会覆盖或重复执行 pending 动作。
7. 反复 enable/disable、死亡/重生、切房间、退出游戏和重复 cleanup 不使用旧指针且不崩溃。

## 交付范围

本轮只修复或重写：

```text
05-正式功能/34-角色变身/AAAAA-role_transform_min.js
05-正式功能/34-角色变身/AAAAA-role_transform_ui.py
05-正式功能/34-角色变身/test_role_transform_static.py
```

先完成单功能验证，不接入正式整合包，不修改其他功能。
