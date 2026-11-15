# 42-路点体检（修改器功能 + 独立启动界面）

**这不是 DLL 插件**：只有你主动打开它才生效，关掉就停止并还原。
同源文件同时放在：

- 实际生效位置：`04-正式发行版/全功能整合包2.8/game_modifier/features/42_waypoint_probe/`
- 本目录：同一份源码副本（script.js / manifest.json / feature.py / panel.py）

## 两种启动方式

### 1）独立界面（不用开修改器，推荐调试用）

双击本目录的 `启动路点体检.bat`，或：

```bat
python AAAAA-waypoint_probe_ui.py
```

- 界面自己 attach `UnityCrossFire.exe`，加载同目录的 `script.js`（和修改器里跑的是同一份脚本，不存在两份实现）；
- 游戏没开时会显示「等待游戏启动...」，开了自动连上；
- 关窗口会先调用 `cleanup`（还原队伍/无敌）再 detach，不会残留状态；
- 「保存日志」会把完整日志（含 `PROBE|EDGES` 逐边数据）落盘到 `logs/`。

> `.bat` 必须保持**纯 ASCII + CRLF**。之前写成 UTF-8 带中文、又加 `chcp 65001`，
> cmd 按 936 码页预解析，把后面的 `python "AAAAA-..."` 行切成碎片，启动直接失败
> （`'??动' is not recognized`）。中文提示一律放进 Python 窗口，别写进 bat。

界面上的控件和修改器卡片一一对应，另外多了 **采样间隔滑块**、**PASS/BLOCK/GAP/STEP/STEEP 计数面板**、**EDGES 明细开关**。

### 2）修改器功能卡片

启动修改器 → 「游戏测试」页 → 「路点体检」卡片（见下）。

## 面板上有什么

| 控件 | 作用 |
| --- | --- |
| 总开关 | 功能开关；关掉会停止所有定时器并**还原**改过的队伍/无敌 |
| 停战（同队 + 无敌） | bot 之间不再互相锁定、打不死；只关战斗不动移动 |
| 跟随我（每个阵营 1 个） | 每个阵营挑一个 bot，把它“敌人”字段指向你，让它自己寻路跟过来 |
| 人机采样 | 定时记录 bot 所在节点，跨节点时记一条边 |
| 跑一次物理探针 | 按人机体积沿每条边扫，判定 PASS/BLOCK/GAP/STEP/STEEP |

## 日志：自动写盘（不用点保存）

界面一启动就在本目录 `logs/` 下开一个文件，**每一行都实时 flush 到磁盘**：

```
logs/waypoint-probe-ui-20261115-211204.log
[21:12:04] === 路点体检 UI 启动 2026-11-15 21:12:04 ===
[21:12:05] 已加载 script.js
[21:12:13] SELFTEST|ok=true|...
[21:12:19] === 退出 ===
```

- 界面上隐藏的 `PROBE|EDGES` 明细也照样写进文件；
- Python 异常、Tk 回调异常都会被 `sys.excepthook` / `report_callback_exception` 抓住写成 `[Python 异常] <traceback>`；
- 点「打开日志目录」直接跳过去；「另存日志」是手动复制一份。

## 日志格式（修改器里也从同一套 log 事件出来）

脚本通过 `log` 事件写进修改器日志，关键行前缀：

```
PROBE|SUMMARY|total=1391|pass=1300|block=61|gap=20|step=8|drop=0|steep=2|nodes=786
PROBE|EDGES|i,j,ax,ay,az,bx,by,bz,dist,verdict,gmax,block,gap;...（每行最多 20 条）
FOLLOW|i=0|team=0|dist=8.4|moved=1.7
WALK|bot=0|x=..|y=..|z=..|node=321
TRACE|bot=0|321>322|linked=1
my_team=1
pacify bots=29 changed=12
```

- `PROBE|EDGES` 是完整逐边数据，可以直接用脚本切分做 CSV；
- `TRACE ... linked=0` 表示 bot 跨到了图上不相邻的节点（瞬移/重生/漏边）。

## 测试流程

1. 启动游戏并**进入一张地图**（大厅里 `AstarPath.active` 是空的，探针会返回 `no_point_graph`）；
2. 启动独立界面（或修改器卡片）；
3. 先开总开关 → 开「停战」，确认 bot 不再互相打；
4. 开「跟随我」，看日志 `FOLLOW` 行的 `moved` 是否 > 0；
5. 点「跑一次物理探针」（约 1~3 秒卡一下）；
6. 走几分钟后看日志；关总开关会自动还原队伍/无敌。

## 2026-11-15 真机验证记录

在游戏进程里跑通了 attach → load → `enable` → `status` → `disable`，日志出现 `native ready`，说明
NativeFunction 全部构造成功（含射线 thunk）。过程中修掉两个真 bug：

| 现象 | 原因 | 修法 |
| --- | --- | --- |
| `enable` 返回 `initNative: not a function` | Frida 17 删除了 `Module.getExportByName` | 加 `resolveExport()`：先 `mod.getExportByName`，再退到 `Module.getGlobalExportByName` |
| 调射线时 access violation（0x51ec8b55） | thunk 用 `add esp,0x24` 收栈，实际参数是 10 个 dword（2×Vector3+ptr+float+int+MethodInfo）= 0x28 | 改成 `add esp,0x28`（已按 IDA 反编译的签名核对过每个参数的 `[ebp+off]`） |

仍未验证：真实命中结果（需要进图才有地面）。进图后点探针看 `PROBE|SUMMARY` 是否输出、`pass` 是否占多数。

## 2026-11-15 第二轮修复（"一直报错"）

真机上复现到的报错是 `pacify: access violation accessing 0xba`，**每秒 10 条**一直刷。根因不是逻辑，是拿脏指针去解引用：

| 问题 | 原因 | 修法 |
| --- | --- | --- |
| 对局外类指针是垃圾（读到 `0x20003043`、`0xbc8df08b`） | `*Bot_TypeInfo` 这类静态槽要等类初始化（进对局）才有值，菜单里是脏数据 | 改用 il2cpp 反射按名字找类：`il2cpp_domain_get` → `domain_get_assemblies` → `assembly_get_image` → `class_from_name`，程序集一加载就能找到；TypeInfo RVA 只当兜底 |
| 每个定时器 tick 都抛异常刷屏 | `pacifyOnce` 每 100ms 跑一次，一次异常一条 error | 所有解引用套 `safe()`+`isPtr()`；没玩家也没人机时只 `noteOnce` 提示一句就返回；同一错误 3 秒内只记一次 |
| `klassName` 永远读不出来 | `readUtf8String(64)` 会越过字符串末尾读到未映射内存而抛异常 | 改成读到 \0 为止（`readUtf8String()`），并校验名称是合法标识符 |

菜单里现在的自检输出（ok=true，零错误）：

```
SELFTEST|ok=true|native=ready|astarpath=null|pointgraph=null|assemblies=51 images|
astar_class=0x10b62ff8/AstarPath|bot_class=0x10cfd0f8/Bot|player_class=0x11106398/Player|
gm_class=0x110faaf8/GameManager|gm_static=0x22201ee0|myplayer=null|bots=0|players=0|
il2cpp_api=Object->0x79edb48/name=Object|raycast=skipped(no_map)
```

大厅里 `astarpath=null`、`raycast=skipped(no_map)` 是正常的（没有导航图就没有地图数据）；
开「停战」只会打印一次 `当前没有玩家/人机（应该还没进入对局）`，不再刷错误。

## 2026-11-15 第三轮：射线 thunk 的真 bug

上一版手写的 x86 thunk 里最后一步是 `FF 15 <目标地址>`，也就是 **`call dword ptr [目标地址]`** —
它把目标函数的头 4 个字节当成函数指针去调用：

- 调 `Physics.Raycast` 时读到的是它自己的序言 `55 8B EC 51` → 崩在 `0x51ec8b55`；
- 用测试桩验证时同样崩在测试桩的头 4 个字节。

改成 `B8 <目标地址>`（`mov eax, imm32`）+`FF D0`（`call eax`）后，用一个"把栈上 10 个 dword
抄进缓冲区"的测试桩做了单元验证，参数布局完全正确：

```
栈上实测: 3f800000 40000000 40400000 3e800000 bf800000 3f000000 <hit> 41480000 7 0
期望:     origin.x origin.y origin.z dir.x   dir.y   dir.z   hit  12.5f    mask method
```

另外给探针加了前置检查：如果 `Physics.Raycast` 本身调用失败，直接
`PROBE|ABORT|...` 中止，不再把整张图判成 1391 条 GAP 骗自己。

## 2026-11-15 第四轮：停战/跟随为什么完全没反应

根因就一句话：**人机一个都没找到**。日志里那条 `follow picked 0 bot(s), teams=` 就是证据。

`Object.FindObjectsOfType(Type, bool)` 的第一个参数要的是 **System.Type 托管对象**，
脚本之前塞的是 `il2cpp_class_get_type()` 返回的 `Il2CppType*` ——类型对不上，
函数每次返回空数组，于是：

- 停战：拿不到 bot，一个字段都没写；
- 跟随：`pickFollowers()` 永远挑出 0 个。

修法：加 `il2cpp_type_get_object(Il2CppType*)` 转成 System.Type 再传；顺便让按名字找类时
多试几个命名空间（`Camera` 在 `UnityEngine` 里，只查全局命名空间会找不到）。

**可验证的证据**（菜单里跑自检，不需要进对局）：

```
修复前: cameras=0
修复后: cameras=1     ← FindObjectsOfType 真的能取到对象了
```

顺带修掉两个"看着对、其实没用"的地方：

| 功能 | 之前 | 现在 |
| --- | --- | --- |
| 停战 | 只改 `Entity.team`/`isInvincible`，人机照样开火 | 只开停战时直接写 `Bot.stopAllBot`（静态 +0xC，24-人机暂停 同款开关，实测	extbf{可写}）；另外仍保持同队+无敌 |
| 跟随 | 只写 `Bot.tryFindEnemy`（0x2C） | 真正驱动 AI 的是 `Bot.enemyInfo`（BotEnemyInfo 对象，Bot+0x28）：写 `enemy`(+0xC)、`isPlayer`(+0x18)、`enemyPos`(+0x1C)、`distance`(+0x28)、`findTime/lastLostTime/nextCheckVisibleTime`，50ms 刷一次；同时把 `nextAttackTime` 推到 1e9 让它不开枪 |

注意：**停战 + 跟随同时开时以跟随为准**（`stopAllBot` 会把 AI 一起冻住，就没法走过来），
这时停战靠同队 + 无敌 + 禁止开火实现。

## 2026-11-15 第五轮：IDA 里查清了停战/跟随为什么"毫无效果"

反编译（IDA，GameAssembly.dll base 0x10000000）看到三件关键事实：

1. **`Bot.get_isStopped` 就是 `Bot.stopAllBot != 0`**（0x10B34080）：
   ```
   if (!v2->static_fields->stopAllBot) return 0; else return 1;
   ```
   `Bot.Update`（0x10B33370）里 `Move()` → `BotEnemyInfo.Update()` → **`if (!get_isStopped())` 才做寻路/打人**。
   所以 `stopAllBot` 一写就把人机整个冻住。上一版只在"停战且没开跟随"时才写它，
   你两个开关一起开 → 这条最有效的路径等于没走。

2. **人机挑敌人只看阵营存活列表**（`<FindAttackTarget>g__GetAttackTargetList` 0x10B32CD0）：
   ```
   if (thisPlayer->team) return GameManager.entityBL_Alive; else return entityGR_Alive;
   ```
   就是 `GameManager` 的 0x14 / 0x18 两个 `List<Entity>`。

3. **只有 `Entity.SetTeam` 才会维护这两个列表**（0x10B3F940）：
   ```
   this->klass->vtable._8_RemoveFromTeamList(...,0);
   this->_team_k__BackingField = newTeam;
   this->klass->vtable._9_AddToTeamList(...,0);
   if (!isDead) this->klass->vtable._9_AddToTeamList(...,1);
   ```
   之前直接写 `Entity.team`（+0x20）字段，列表根本没动 → 人机眼里目标一个没少，照打不误。

### 这一版的做法

| 功能 | 实现 |
| --- | --- |
| 停火 | `Interceptor.replace(Bot.CheckAttackTarget, 0x00B2DD80)`：换成空函数，人机不再选敌、不开火，但 `Update/Move` 照跑（跟随才走得动）。安装时校验入口首字节是 `55 8B EC`，关功能时 `Interceptor.revert` |
| 只开停战 | 额外写 `Bot.stopAllBot = true`（人机整体站住，最稳） |
| 跟随 | 每 50ms 写 `Bot.enemyInfo`（enemy/isPlayer/enemyPos/distance/findTime/lastLostTime/nextCheckVisibleTime），并把 `nextAttackTime` 推到 1e9 让它别开枪；跟随者选定后固定，不再每 2 秒重挑（避免"并队"后把自己阵营也选进去） |
| 诊断 | `FOLLOW` 行末尾加了 `own=`：1 表示 `enemyInfo.enemy` 此刻确实指向你（写进去没被 AI 覆盖），0 表示被游戏改回去了 |

实测（菜单里，enable → 2 秒 → disable）：hook 安装/撤销都成功，`errors=0`，进程存活。

## 2026-11-15 第六轮：加"谁都掉不了血"

上一次真机日志（21:40）其实已经证明跟随在动：

```
[21:40:29] follow picked 1 bot(s), teams=1
[21:40:30] FOLLOW|i=0|team=1|dist=107.62|moved=0.00|own=1
[21:40:31] FOLLOW|i=0|team=1|dist=101.20|moved=5.48|own=1
```

`own=1` = 我们写的 `enemyInfo.enemy` 没被 AI 覆盖；距离 107 → 101 在缩短（它在往你这边走，
只是从 100 米外跑过来要十几秒）。

"停战还是打" 的残余问题在于：`Bot.CheckAttackTarget` 只挡住"重新选敌"，
已经锁上目标的人机照样能扣扳机。所以这一版再加一道底层闸：

```
Interceptor.replace(HealthData.Hurt, 0x00AE45B0)   // 谁都掉不了血
```

`HealthData.Hurt(int)`（0x10AE45B0，签名 `void Hurt(HealthData* this, int value, MethodInfo*)`）是所有伤害的入口，
换成空函数后不管谁开枪、谁砍人，血量都不会变 → 人机之间打不死、你也死不了。

现在停战 = 两条：
1. `Bot.CheckAttackTarget` 接管 → 人机不再选敌/开火；
2. `HealthData.Hurt` 接管 → 就算开了枪也扣不了血（兜底）。

实测（菜单里 enable → 2s → disable）：两个 hook 安装、撤销都成功，`errors=0`，进程存活。

## 2026-11-15 第七轮：查到反作弊在还原我们的补丁 + 性能重做

### 1. 为什么"接管函数"没效果（还偶尔卡死/崩）

上一版用 `Interceptor.replace` 接管了 `Bot.CheckAttackTarget` 和 `HealthData.Hurt`。实测发现：

```
接管后再撤销，入口字节变成了：
Bot.CheckAttackTarget @ 0x6457dd80 : e9 7f 27 ec 9c ...  -> jmp 0x1440504 (unknown)
HealthData.Hurt      @ 0x645345b0 : e9 4f c0 f0 9c ...  -> jmp 0x1440604 (unknown)
几分钟后再看（我们什么都没做）：
Bot.CheckAttackTarget : 55 8b ec 51 80 3d ...   ← 被游戏自己还原了
```

这个游戏带 **CodeStage Anti-Cheat Toolkit**（dump.cs 里一堆 `ObscuredBool/ObscuredInt`），
它会把改过的函数入口还原、还会保留一段 `jmp` 到失效地址——这时候人机一调这个函数就崩。

**结论：这个功能里彻底不做代码 patch。** 现在全部是"数据写入"，反作弊不校验数据：

| 作用 | 手段（纯数据） |
| --- | --- |
| 冻结人机行为 | `Bot.stopAllBot`（静态 +0xC）——游戏自己的 AI 总闸，`Bot.get_isStopped` 每帧读它 |
| 跟随 | `Bot.enemyInfo`(+0x28 → BotEnemyInfo)：`enemy`(+0xC) / `isPlayer`(+0x18) / `enemyPos`(+0x1C) / `distance`(+0x28) / `findTime`(+0x10) / `lastLostTime`(+0x14) / `nextCheckVisibleTime`(+0x48) |
| 不开火 | `Bot.nextAttackTime`(+0x3C) = 1e9 |
| 不死 | `Entity.isInvincible`(+0x18) |

### 2. 人机都有哪些行为决策（IDA + dump.cs）

`Bot.Update`（0x10B33370）每帧的顺序：

```
Move()                        ← 永远执行（按 path 走）
BotEnemyInfo.Update()         ← 更新目标距离/可见性
武器 BotControl(bot)          ← 开火/挥刀（武器类的虚函数，slot 39）
if (!get_isStopped()) {       ← Bot.stopAllBot 为真就整段跳过
    PathSetting()             ← seeker 算路
    CheckAttackTarget()       ← 选敌/决定攻击
    UseWeapon() / UseSkill() / UpdateAction() / JumpCheck() / TryCrouch() ...
}
```

也就是说：**`Bot.stopAllBot = true` 一开，除了 `Move()` 之外所有决策都被游戏自己跳过了**
（不寻敌、不开火、不巡逻、不用技能、不跳不蹲）。

### 3. 加载时机

- 每个 Bot 在 `Awake()` 建自己的 `enemyInfo` 对象，`stopAllBot` 是**静态字段**；
- 决策判断是**每帧读**，所以不需要"进房间之前清空配置"——进房前写、进房后写都生效；
- 我们的定时器每 200~300ms 重新写一遍，覆盖回合切换/重生。

### 4. 性能（上一版卡的原因）

| 原来 | 现在 |
| --- | --- |
| 跟随 50ms、停战 100ms 各调一次 `Object.FindObjectsOfType`（每次扫全场景） | **1 秒一次**，结果缓存 |
| 采样时每个 bot 重读 786 个节点的坐标（15×786×3 次读） | 节点坐标**只读一次**缓存起来 |
| 每个 bot 每 200ms 都算最近节点 + 每换节点写一条 TRACE | 只算"动过"的 bot，最多 8 个；TRACE 只在 `linked=0` 或每 20 条写一次 |
| 停战 100ms / 跟随 50ms | 200ms / 100ms |

## 实现要点

- 点图：`AstarPath.active`（`AstarPath_TypeInfo=0xE2544C`，static+0x0C）→ `data`(+0x10) → `graphs`(+0x20)，取节点数最多的图；
- 节点：`nodes`(+0xE8)/`nodeCount`(+0xEC)，位置 `Int3` 在 +0x14（1/1000 m），边在 `PointNode.connections`(+0x20)，步长 12；
- 射线：`Physics.Raycast`(0xABB0A0) 是 Vector3 传值的重载，Frida 不能直接按值传结构，所以脚本里用一段自己拼的 x86 thunk（`buildRaycastStub`）把指针参数展开成按值参数；
- bot：`Bot_TypeInfo`(0xE25F44) + `Object.FindObjectsOfType`(0x4E9620)；字段 `thisPlayer` 0x24、`tryFindEnemy` 0x2C、`faceToEnemy` 0x30、两个计时器 0x38/0x3C；
- 队伍/无敌：`Entity.team` 0x20、`Entity.isInvincible` 0x18；本地玩家取 `GameManager.myPlayer`（static+0），取不到就用 `Player.get_isMyPlayer`(0xB55FD0) 兜底。
