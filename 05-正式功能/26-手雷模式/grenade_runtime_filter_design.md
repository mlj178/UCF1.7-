# grenade_mode_v2_12_8_final_clean_ui 说明

## 基准

```text
grenade_mode_v2_12_7_safe_give_argfix_ctk.zip
```

## 本版目标

最终版清理，不再继续优化功能。

```text
删除/隐藏观察类 UI 选项
删除/隐藏测试验证类 UI 入口
默认关闭观察日志
保留 v2.12.7 已验证成功的扔雷主链路
```

## UI 删除/隐藏内容

已从界面移除：

```text
查看状态按钮
VirtualGrenadeMode观察
Bot手雷行为观察
Bot攻击入口观察
Bot AI观察/测试/触发调试行
GiveWeapon过滤调试开关
旧入口重定向提示
大量历史观察说明文案
```

## 保留核心功能

仍然保留：

```text
锁999
保护当前手雷对象 Remove
运行时参数即时同步
Bot手雷模式
Bot.UseWeapon 投掷驱动
VirtualBotControl 接管
禁止 Bot 原枪械开火
无手雷也不放行开枪
统一投掷许可层
出生保护
目标稳定
首次额外延迟
复活重置
多 key Grenade 缓存
主动补发普通 Grenade
GiveWeapon 参数修复
```

## 默认配置变化

观察日志默认关闭：

```text
virtual_grenade_observer_enabled = false
virtual_grenade_observer_verbose = false
bot_grenade_behavior_observer_enabled = false
bot_attack_observer_enabled = false
bot_ai_probe_enabled = false
bot_ai_probe_verbose = false
observe_set_current_weapon = false
```

内部稳定链路仍然开启：

```text
bot_ai_hook_drive_enabled = true
bot_ai_checkattack_drive_enabled = true
bot_ai_camerarotation_drive_enabled = true
bot_ai_trysettarget_drive_enabled = false
bot_ai_hook_drive_require_target = true
bot_ai_hook_drive_cooldown_ms = 1000

virtual_grenade_giveweapon_enabled = true
bot_grenade_active_give_enabled = true
bot_grenade_mode_enabled = true
bot_throw_drive_enabled = true
virtual_botcontrol_enabled = true
```

## 最终原则

```text
界面只保留最终功能控制。
观察/测试/验证不再暴露给用户。
底层扔雷主链路不删除，避免影响已验证成功的 v2.12.7 行为。
```

## 文件

本版不生成 `.js.txt` 文件。
