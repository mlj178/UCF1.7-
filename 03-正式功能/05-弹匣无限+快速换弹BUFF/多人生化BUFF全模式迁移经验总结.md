# 多人生化BUFF全模式迁移经验总结

## 项目概述

将多人生化模式（Nano4 Terminator）中的回合特性BUFF（无限子弹、快速换弹）迁移到所有游戏模式中实现。

---

## 实现的功能

| 功能 | 效果 | 适用模式 |
|------|------|----------|
| 无限子弹 | 射击时弹药不减少 | 全模式 |
| 快速换弹 | 换弹速度提升2倍 | 全模式 |

---

## 核心发现

### 1. 通用BUFF字段

通过IDA反编译分析，发现以下字段定义在 `Player` 和 `PlayerWeapons` 类中，**在所有游戏模式下都有效**：

#### Player类中的通用BUFF字段

| 字段名 | 偏移 | 类型 | 说明 |
|--------|------|------|------|
| `Buff_InfinityAmmo` | 0x128 | bool | 无限子弹BUFF标志 |
| `Buff_JumpDisabled` | 0x120 | bool | 禁用跳跃BUFF |
| `Buff_CameraRotDisabled` | 0x118 | bool | 禁用相机旋转BUFF |
| `Modifier_MoveSpeedRatio` | 0x8C | PropertyModifier | 移动速度比例修改器 |

#### PlayerWeapons类中的通用Modifier字段

| 字段名 | 偏移 | 类型 | 说明 |
|--------|------|------|------|
| `Modifier_ReloadSpeed` | 0x3C | PropertyModifier | 换弹速度修改器 |
| `Modifier_KnifeRange` | 0x40 | PropertyModifier | 近战距离修改器 |
| `Modifier_KnifeSpeed` | 0x44 | PropertyModifier | 近战速度修改器 |

### 2. 为什么可以在其他模式使用？

这些字段都定义在 `Player` 和 `PlayerWeapons` 类中，这两个类是游戏的核心类，在所有模式下都存在。

**多人生化模式的限制**：
- `Mode_Nano4_Terminator` 类只在多人生化模式中存在
- `attributeAsset`、`attribute_Nano`、`attribute_Human` 等字段只在多人生化模式中有效
- `AddPropertyModifier` 方法只在多人生化模式中调用

**通用字段的优势**：
- `Player.Buff_InfinityAmmo` 是Player类的字段，所有模式都有Player
- `PlayerWeapons.Modifier_ReloadSpeed` 是PlayerWeapons类的字段，所有模式都有PlayerWeapons
- 可以直接设置这些字段，不需要依赖多人生化模式的特性系统

---

## 实现方案

### 方案对比

| 方案 | 优点 | 缺点 | 是否采用 |
|------|------|------|----------|
| 直接设置BUFF字段 | 简单直接 | 需要找到本地玩家指针 | ❌ |
| Hook get_isInfinityAmmo() | 稳定可靠 | 需要正确的RVA地址 | ✅ |
| Hook get_ReloadSpeed() | 稳定可靠 | 需要正确的RVA地址 | ✅ |

### 最终方案：Hook函数替换

#### 1. 无限子弹实现

```javascript
// PlayerWeapons.get_isInfinityAmmo (RVA 0xB17120)
var getIsInfinityAmmoAddr = base.add(0xB17120);

// 直接替换函数，始终返回1 (true)
Interceptor.replace(getIsInfinityAmmoAddr, new NativeCallback(function(self) {
    return 1;  // 无限子弹 (IL2CPP bool用int表示)
}, "int", ["pointer"]));
```

**关键点**：
- IL2CPP中bool返回值需要用int表示
- `return 1` 表示true，`return 0` 表示false
- 返回值类型必须是 `"int"`，不能是 `"bool"`

#### 2. 快速换弹实现

```javascript
// PlayerWeapons.get_ReloadSpeed (RVA 0xB170E0)
var getReloadSpeedAddr = base.add(0xB170E0);

// Player.get_isMyPlayer (RVA 0xB55FD0)
var isMyPlayerAddr = base.add(0xB55FD0);
var isMyPlayer = new NativeFunction(isMyPlayerAddr, "bool", ["pointer"]);

Interceptor.replace(getReloadSpeedAddr, new NativeCallback(function(self) {
    // PlayerWeapons + 0x8 = owner (Player)
    var owner = self.add(0x8).readPointer();
    if (!owner || owner.isNull()) {
        return RELOAD_SPEED_MULTIPLIER;
    }

    // 判断是否是本地玩家
    if (isMyPlayer(owner)) {
        return RELOAD_SPEED_MULTIPLIER;  // 快速换弹
    }

    return 1.0;  // 其他玩家返回默认值
}, "float", ["pointer"]));
```

**关键点**：
- 通过 `isMyPlayer` 判断本地玩家
- 只对本地玩家应用加速
- 其他玩家返回默认值1.0

---

## 关键技术点

### 1. IL2CPP bool返回值问题

**问题**：
```javascript
// 错误写法
Interceptor.replace(addr, new NativeCallback(function(self) {
    return true;  // 报错：expected an integer
}, "bool", ["pointer"]));
```

**正确写法**：
```javascript
// 正确写法
Interceptor.replace(addr, new NativeCallback(function(self) {
    return 1;  // IL2CPP bool用int表示
}, "int", ["pointer"]));
```

### 2. 函数RVA地址

| 函数名 | RVA | 说明 |
|--------|-----|------|
| `PlayerWeapons.get_isInfinityAmmo` | 0xB17120 | 获取是否无限子弹 |
| `PlayerWeapons.get_ReloadSpeed` | 0xB170E0 | 获取换弹速度 |
| `Player.get_isMyPlayer` | 0xB55FD0 | 判断是否是本地玩家 |

### 3. 内存偏移

| 类 | 字段 | 偏移 | 说明 |
|----|------|------|------|
| PlayerWeapons | owner | 0x8 | 玩家指针 |
| Player | wpns | 0xA0 | 武器系统指针 |
| Player | Buff_InfinityAmmo | 0x128 | 无限子弹BUFF |
| PlayerWeapons | Modifier_ReloadSpeed | 0x3C | 换弹速度修改器 |

---

## 使用方法

### 1. 注入脚本

```bash
frida -p <PID> -l infinite_ammo_rapid_reload_test.js
```

### 2. 调整参数

```javascript
var RELOAD_SPEED_MULTIPLIER = 2.0;  // 换弹速度倍数，可修改为其他值
```

### 3. 测试验证

- 进入任意游戏模式
- 射击测试无限子弹
- 换弹测试快速换弹

---

## 扩展应用

### 其他通用BUFF

基于同样的原理，可以实现以下功能：

| 功能 | 实现方式 | 偏移 |
|------|----------|------|
| 移动加速 | Hook `get_MoveSpeedRatio()` | Player.Modifier_MoveSpeedRatio (0x8C) |
| 近战加速 | Hook `get_KnifeSpeed()` | PlayerWeapons.Modifier_KnifeSpeed (0x44) |
| 近战距离 | Hook `get_KnifeRange()` | PlayerWeapons.Modifier_KnifeRange (0x40) |
| 禁用跳跃 | 设置 `Buff_JumpDisabled` | Player.Buff_JumpDisabled (0x120) |

### 代码模板

```javascript
// Hook任意getter函数的模板
var getFunctionAddr = base.add(0xXXXXXX);

Interceptor.replace(getFunctionAddr, new NativeCallback(function(self) {
    var owner = self.add(0x8).readPointer();
    if (!owner || owner.isNull()) {
        return DEFAULT_VALUE;
    }

    if (isMyPlayer(owner)) {
        return CUSTOM_VALUE;  // 本地玩家自定义值
    }

    return DEFAULT_VALUE;  // 其他玩家默认值
}, "RETURN_TYPE", ["pointer"]));
```

---

## 经验总结

### 1. 分析流程

1. **IDA反编译**：找到目标函数的RVA地址
2. **dump.cs分析**：查看类结构和字段偏移
3. **确定通用字段**：找出在所有模式下都有效的字段
4. **Hook实现**：使用Frida替换函数实现

### 2. 注意事项

- IL2CPP的bool返回值用int表示
- 需要正确判断本地玩家
- Hook函数时要注意异常处理
- 测试时要进入实际游戏模式验证

### 3. 常见问题

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| `expected an integer` | bool返回值类型错误 | 改用 `"int"` 类型，返回1或0 |
| 无限子弹无效 | Hook地址错误 | 确认RVA地址正确 |
| 快速换弹无效 | isMyPlayer判断失败 | 检查isMyPlayer函数地址 |
| 游戏崩溃 | Hook函数异常 | 添加try-catch处理 |

---

## 文件清单

| 文件 | 说明 |
|------|------|
| `infinite_ammo_rapid_reload_test.js` | 全模式无限子弹+快速换弹脚本 |
| `多人生化BUFF全模式迁移经验总结.md` | 本文档 |

---

## 更新日期

2026-05-01
