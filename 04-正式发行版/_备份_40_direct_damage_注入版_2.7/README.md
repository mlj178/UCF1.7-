# 备份：40_direct_damage 注入版（已退役）

备份时间：2026-10-16
原因：`features/40_direct_damage` 切换到 **C 路线（根治版）**，注入链路整体下线。

## 为什么要退役

旧版的常规枪械走的是「**自己合成 `DamageEventData` + 调 `GameManager.TakeDamage` +
`Interceptor.replace` 跳过原函数**」。原函数的后半截（击杀提示 / 模式记账 /
`GameManager.DeathEventBroadcast` / `ModeBase_Nano.RespawnPlayer` 复活调度）
因此从未跑过，表现就是：

- 目标「扣了血但死亡流程没走完」→ **躺尸不复活**；
- 战场上一个目标卡住不复活，只能靠脚本自己补。

于是又加了 `death_fix_broadcast`（补发死亡广播）和 `death_fix_respawn`
（6 秒后还死着就手动 `RespawnPlayer`）去兜底 —— 这就是"越界"：
**我们去做了游戏自己该做的事，然后为了收拾自己造成的烂摊子，又写了第二层逻辑。**

后来新增的 `gun_ray_redirect`（原生射线接管：只掰射线方向、原函数照常跑完）
其实已经是不越界的正解，注入路径退化成"射线接管失败时的补刀"，
但补刀 + 兜底仍然留着，并先后引发两个线上问题：

1. 近战武器打死的生化幽灵会被脚本"复活"（兜底把**所有**死亡都登记了观察窗口）；
2. 新回合倒计时里冒出上一回合的幽灵（观察窗口跨回合存活，而当时一个回合钩子都没挂）。

## C 路线做了什么

直接删掉整条注入链路，死亡与复活完全交还游戏：

- 保留并作为**唯一**枪械实现：原生射线接管（`gun_ray_redirect`）；
- 保留：弹体追踪（`homing`，本来就不注入伤害）；
- 删除：`applyDamage` / `directDamage` / `buildEventDwords` / `callGameManagerTakeDamage` /
  `callPlayerHurt` / `callEntityHurt` / `skipOriginalFromOnEnter` /
  `installGunHookReplace`（`Interceptor.replace`）/
  `clearTargetInvincibility`（不再清目标的复活无敌）；
- 删除：`death_fix_broadcast` / `death_fix_respawn` / `death_diag` 全家 /
  `installDeathDiagnostics` / `installPipelineProbes` / `installRaiseProbe` /
  `watchDeath` / `checkDeathWatch` / `registerDeathWatch` / `deathRescueTick` /
  回合边界钩子（`GameRoundEnd` / `NewGameRoundStart` / `OnDestroy`）；
- 删除：整张 `DamageEventData` / `DeathEventData` 偏移表与对应 RVA。

代码量：`script.js` 4983 行 / 269 KB → 2454 行 / 118 KB；142 个函数 → 保留 77、重写 11、删除 50。

## 本目录内容

| 路径 | 说明 |
|---|---|
| `40_direct_damage/` | 退役那一刻的 `features/40_direct_damage` 全量副本（`script.js` 等 7 个文件） |
| `05-正式功能-40-开火直伤/` | 退役那一刻的 `05-正式功能/40-开火直伤` 副本（含旧版 `开火直伤-简要说明.md`） |
| `06-测试-death-diag-stub/` | 旧版死亡链离线冒烟桩 `smoke_death_diag.js`（只对旧脚本有意义，已从 `06-测试` 移出） |
| `05-正式功能-40-开火直伤/AAAAA-direct_damage_ui.py` | 旧版的 05 本地调试 UI（含它的 `logs/`）。它的状态面板专为注入链路而写：显示「伤害次数 / HP 对照 / wpnIndex 底板 / 死亡广播 / 清无敌 / 管线计数」，并会下发已删除的 `damage_entry`。**当前版本没有这些量**，所以随旧版一起移出活动目录。 |

## 想回去对照 / 恢复时注意

1. 这份代码**不要再放回 `features/`**（目录扫描按 `features/*/manifest.json`，放回去会被加载）；
2. 恢复注入版 = 重新引入第 1、2 个已修 bug 的成因，除非同时把死亡兜底一起恢复；
3. 当前版本的边界由 `features/40_direct_damage/test_c_route_static.py`（静态）和
   `06-测试/c-route-stub/smoke_c_route.js`（运行时）守着，恢复注入前先看这两个测试为什么存在。

## 附：调试 UI 为什么也一起退役

`AAAAA-direct_damage_ui.py` 的状态面板整块是为注入链路写的：

- 显示 `damage_applied` / `hp_checks` / `hp_dropped` / `template_captured` /
  `death_in`→`death_out` / `invincible_cleared` / `pipeline_*` —— 这些计数器
  在当前版本里**全部不存在**；
- 它的下拉框会下发 `config.damage_entry`，而当前 `updateConfig` 故意忽略该键，
  等于一个点了没反应的开关。

留着它就是一个"看起来能用、数字全是 0"的陷阱，所以随旧版一起移出。
当前版本的排错入口在 `features/40_direct_damage` 的 RPC 里（`logs` / `snapshot` / `status`），
状态字段以 `getStatus()` 返回的为准。
