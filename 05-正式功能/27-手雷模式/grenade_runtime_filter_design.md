# grenade_mode_v2_12_4_native_cleanup 说明

## 修复内容

v2.12.3 已删除旧 SmartAI 路径距离逻辑和旧距离参数，但 JS 的 `setupNatives()` 里还残留：

```text
Runtime.natives.Bot_IsPathLengthToEnemyLess =
    new NativeFunction(addrOf(RVA.Bot_IsPathLengthToEnemyLess), ...)
```

而 `RVA.Bot_IsPathLengthToEnemyLess` 已经被删除，所以开启时出现：

```text
Error: missing argument
at addrOf
at setupNatives
```

v2.12.4 已删除这段旧 Native 初始化。

## 当前状态

```text
不再初始化 Bot_IsPathLengthToEnemyLess
不再使用官方路径距离
不再使用距离安全区间
不再使用抛物线可达性
不再使用旧距离上下限/速度实验参数
```

保留：

```text
smart_grenade_ai_enabled = true
smart_grenade_require_official_visible = true
smart_grenade_recent_visible_ms = 350
canBotThrowNow()
resetBotLifeState()
```

## 文件

本版不生成 `.js.txt` 文件。
