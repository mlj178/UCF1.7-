# 热成像透视功能设计文档

**日期**: 2026-05-22  
**版本**: v1.0  
**状态**: 设计完成，待实现

---

## 1. 概述

### 1.1 目标

将装甲终结者的热成像透视技能应用到所有游戏模式，让所有玩家（human角色）都可以使用，并且可以在移动状态下使用。

### 1.2 核心需求

- ✅ 所有游戏模式下可用
- ✅ 所有角色（human）都可以使用
- ✅ 允许在移动状态下使用
- ✅ 按键触发（T键）
- ✅ 仅显示敌人
- ✅ 持续时间3秒

### 1.3 技术基础

通过IDA逆向分析发现：
- `GameManager.SetThermalVision(float duration, bool showHuman)` 是热成像的核心方法
- RVA地址：`0xB36960`
- 参数说明：
  - `duration`: 持续时间（秒）
  - `showHuman`: 是否显示人类（false = 仅显示敌人）

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────┐
│         热成像功能模块架构                │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
   ┌────▼────┐            ┌────▼────┐
   │ 按键监控 │            │ 热成像控制 │
   └────┬────┘            └────┬────┘
        │                       │
        │    ┌──────────┐       │
        └───►│ Frida JS │◄──────┘
             └────┬─────┘
                  │
        ┌─────────▼─────────┐
        │ GameManager.      │
        │ SetThermalVision  │
        └───────────────────┘
```

### 2.2 核心组件

#### **组件1：按键监控模块**

**职责**：
- 监听T键的按下事件
- 使用Windows API检测按键状态
- 触发热成像启用

**技术实现**：
```javascript
// 使用Windows API检测按键状态
var GetAsyncKeyState = Module.findExportByName("user32.dll", "GetAsyncKeyState");
var T_KEY = 0x54; // T键的虚拟键码

function isKeyPressed() {
    return GetAsyncKeyState(T_KEY) & 0x8000;
}
```

#### **组件2：热成像控制模块**

**职责**：
- 调用 `GameManager.SetThermalVision()`
- 设置持续时间参数（3秒）
- 设置显示范围参数（仅敌人）

**技术实现**：
```javascript
// GameManager.SetThermalVision 的地址
var SetThermalVision = base.add(0xB36960);

// 启用热成像（持续3秒，仅显示敌人）
function enableThermalVision() {
    SetThermalVision(3.0, 0); // duration=3秒, showHuman=false
}
```

#### **组件3：状态管理模块**

**职责**：
- 维护热成像的当前状态（启用/禁用）
- 管理按键状态（按下/松开）
- 防止重复触发

**状态机**：
```
[空闲] --按下T键--> [启用热成像] --3秒后--> [空闲]
   ↑                                        |
   └────────────────────────────────────────┘
```

---

## 3. 数据流设计

### 3.1 正常流程

```
用户按下T键
    ↓
按键监控检测到按下（50ms轮询）
    ↓
检查是否已在冷却中
    ↓ (否)
调用 GameManager.SetThermalVision(3.0, false)
    ↓
热成像效果启用（仅显示敌人）
    ↓
控制台输出: "[热成像] 已启用，持续3秒"
    ↓
等待3秒
    ↓
热成像效果自动关闭
    ↓
控制台输出: "[热成像] 已关闭"
```

### 3.2 冷却处理

```
用户按下T键
    ↓
检查是否在冷却中（距离上次启用 < 3秒）
    ↓ (是)
忽略本次按键
    ↓
控制台输出: "[热成像] 冷却中，请稍候..."
```

---

## 4. 技术实现细节

### 4.1 按键检测

**方案**：使用Windows API `GetAsyncKeyState`

**优点**：
- 性能开销小
- 不需要Hook游戏输入系统
- 实现简单可靠

**代码**：
```javascript
var GetAsyncKeyState = Module.findExportByName("user32.dll", "GetAsyncKeyState");
var T_KEY = 0x54;

function isKeyPressed() {
    try {
        return (GetAsyncKeyState(T_KEY) & 0x8000) !== 0;
    } catch(e) {
        return false;
    }
}
```

### 4.2 热成像控制

**方法签名**：
```csharp
// C# 原型
public static void SetThermalVision(float duration, bool showHuman)

// Frida NativeFunction
var SetThermalVision = new NativeFunction(
    base.add(0xB36960),
    'void',
    ['float', 'bool']
);
```

**调用方式**：
```javascript
// 启用热成像（3秒，仅敌人）
SetThermalVision(3.0, 0);

// 关闭热成像
SetThermalVision(0.0, 0);
```

### 4.3 主循环

**检测频率**：50ms

**逻辑**：
```javascript
var lastTriggerTime = 0;
var COOLDOWN = 3000; // 3秒冷却

setInterval(function() {
    var now = Date.now();
    
    // 检测T键按下
    if (isKeyPressed()) {
        // 检查冷却
        if (now - lastTriggerTime >= COOLDOWN) {
            // 启用热成像
            enableThermalVision();
            lastTriggerTime = now;
            console.log("[热成像] 已启用，持续3秒");
        }
    }
}, 50);
```

### 4.4 队友/敌人判定

**判定逻辑**（来自自瞄代码）：
```javascript
// 获取队伍信息
var myTeam = getTeam(myPlayer);
var team = getTeam(targetPlayer);

// 判定是否为敌人
var isEnemy = (myTeam === 2) || (team === 2) || (myTeam !== team);

// 说明：
// - myTeam === 2: 我在特殊队伍（如观察者）
// - team === 2: 对方在特殊队伍
// - myTeam !== team: 队伍不同（正常敌对）
```

**注意**：由于我们直接调用 `SetThermalVision(3.0, false)`，游戏内部会自动处理队友/敌人判定，我们不需要手动实现。

---

## 5. 错误处理

### 5.1 异常情况

| 异常 | 处理方式 |
|------|---------|
| GameAssembly.dll未找到 | 输出错误日志，退出脚本 |
| SetThermalVision地址无效 | 输出错误日志，禁用功能 |
| 按键检测失败 | 使用备用方案（Hook输入系统） |
| 游戏进程异常 | 自动清理资源，避免崩溃 |

### 5.2 安全检查

```javascript
function safeCall(fn, ...args) {
    try {
        return fn(...args);
    } catch(e) {
        console.log("[错误] " + e.message);
        return null;
    }
}
```

---

## 6. 用户交互

### 6.1 控制台提示

**启用时**：
```
[热成像] 已启用，持续3秒
[热成像] 按键: T | 显示: 仅敌人
```

**冷却时**：
```
[热成像] 冷却中，剩余时间: 1.5秒
```

**错误时**：
```
[热成像] 错误: GameAssembly.dll未找到
```

### 6.2 使用说明

```
========================================
      热成像透视功能 v1.0
========================================
按键: T键
持续时间: 3秒
显示范围: 仅敌人
适用模式: 所有模式
适用角色: 所有角色
移动限制: 无（可在移动中使用）
========================================
```

---

## 7. 测试计划

### 7.1 功能测试

- [ ] 团队模式下测试
- [ ] 个人竞技模式下测试
- [ ] 终结者模式下测试
- [ ] 生化模式下测试
- [ ] 移动状态下测试
- [ ] 静止状态下测试
- [ ] 冷却机制测试
- [ ] 快速连按测试

### 7.2 性能测试

- [ ] CPU占用测试
- [ ] 内存占用测试
- [ ] 帧率影响测试

### 7.3 兼容性测试

- [ ] 与其他功能同时使用
- [ ] 不同分辨率下测试
- [ ] 不同游戏版本测试

---

## 8. 实现清单

### 8.1 核心功能

- [ ] 按键检测模块
- [ ] 热成像控制模块
- [ ] 状态管理模块
- [ ] 冷却机制
- [ ] 错误处理

### 8.2 辅助功能

- [ ] 控制台提示
- [ ] 状态显示
- [ ] 调试日志

### 8.3 文档

- [ ] 使用说明
- [ ] 技术文档
- [ ] 测试报告

---

## 9. 风险评估

### 9.1 技术风险

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| SetThermalVision地址变化 | 中 | 动态查找方法地址 |
| 游戏更新导致失效 | 低 | 提供版本检测 |
| 与其他功能冲突 | 低 | 独立模块设计 |
| 性能影响 | 低 | 50ms检测频率已优化 |

### 9.2 游戏平衡风险

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| 过于强大 | 中 | 3秒持续时间限制 |
| 影响游戏体验 | 低 | 仅显示敌人 |
| 被检测风险 | 低 | 使用游戏原有功能 |

---

## 10. 未来扩展

### 10.1 可能的改进

- 可配置持续时间
- 可配置触发按键
- 可配置显示范围
- 添加UI界面
- 添加声音提示

### 10.2 高级功能

- 自动检测敌人数量
- 智能启用（敌人靠近时自动启用）
- 与其他功能联动

---

## 11. 总结

本设计方案通过直接调用游戏原有的 `GameManager.SetThermalVision` 方法，实现了热成像透视功能的全模式、全角色、移动状态下的使用。

**核心优势**：
1. 实现简单，代码量少
2. 性能开销小
3. 不破坏游戏原有逻辑
4. 易于维护和调试

**关键参数**：
- 触发按键：T键
- 持续时间：3秒
- 显示范围：仅敌人
- 检测频率：50ms

**下一步**：编写实现计划并开始编码。
