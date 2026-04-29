# 🎮 InfiniteAmmoDLL - UnityCrossFire 游戏修改器

> **版本**: V2.0  
> **最后更新**: 2026-04-29  
> **目标游戏**: UnityCrossFire.exe (Unity IL2CPP)  
> **核心技术**: Frida 动态插桩 + Il2CppDumper 静态分析

---

## 📋 目录

1. [项目概述](#项目概述)
2. [脚本数据来源说明](#脚本数据来源说明)
3. [游戏逻辑分析](#游戏逻辑分析)
4. [四大功能模块](#四大功能模块)
5. [可执行程序清单](#可执行程序清单)
6. [使用指南](#使用指南)
7. [项目打包流程](#项目打包流程)
8. [开发挑战与解决方案](#开发挑战与解决方案)
9. [技术踩坑与经验教训](#技术踩坑与经验教训)

---

## 项目概述

本项目是一个基于 **Frida** 动态插桩框架的 Unity IL2CPP 游戏修改器，针对 UCF1.7（UnityCrossFire.exe）实现了四大核心功能：

| 功能 | 描述 | 实现方式 |
|------|------|---------|
| 🗡️ **快刀** | 刀攻击动画速度提升 3 倍 | Hook 武器动画函数 + 修改动画速度 |
| ⏱️ **全模式无限时间** | 所有游戏模式时间锁定 99:59 | Hook 回合结束逻辑 + 阻止时间流逝 |
| 🎯 **无后座力** | 消除所有枪械后坐力 | Hook 射击函数 + 清零后坐力参数 |
| 🔫 **无限子弹** | 所有武器弹药无限 | Hook 弹药消耗函数 + ObscuredInt 解密修改 |

### 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户操作界面                               │
│              (Electron + Vue3 控制台)                         │
└────────────────────────┬────────────────────────────────────┘
                         │ Electron IPC
┌────────────────────────▼────────────────────────────────────┐
│                    主进程 (Node.js)                           │
│              FridaManager + ProcessMonitor                  │
└────────────────────────┬────────────────────────────────────┘
                         │ Frida IPC
┌────────────────────────▼────────────────────────────────────┐
│                    Agent 脚本 (V8 引擎)                       │
│              combined_agent.js (4 个功能模块)                 │
└────────────────────────┬────────────────────────────────────┘
                         │ 内存操作
┌────────────────────────▼────────────────────────────────────┐
│                    游戏进程                                   │
│              UnityCrossFire.exe → GameAssembly.dll           │
└─────────────────────────────────────────────────────────────┘
```

### 核心优势

- **无需修改游戏文件**：纯内存修改，不触碰游戏文件
- **热插拔**：随时注入/卸载，无需重启游戏
- **跨版本兼容**：基于 RVA 地址，游戏更新后只需更新偏移
- **高性能**：Interceptor.replace 零性能损耗
- **易于分发**：打包为单文件 EXE，用户无需安装任何依赖

---

## 脚本数据来源说明

所有 Frida 脚本的开发依赖于 **Il2CppDumper** 对游戏 IL2CPP 程序的静态分析结果。

### 核心数据文件

| 文件 | 路径 | 用途 |
|------|------|------|
| `dump.cs` | `新建文件夹/Il2CppDumper/dump.cs` | 游戏类定义、方法签名、字段偏移、RVA 地址 |
| `script.json` | `新建文件夹/Il2CppDumper/script.json` | 方法名到绝对地址的映射表 |
| `il2cpp.h` | `新建文件夹/Il2CppDumper/il2cpp.h` | C 头文件，包含结构体定义 |
| `script.json` | `新建文件夹/Il2CppDumper/script.json` | JSON 格式的方法地址映射 |

### 数据提取流程

```
1. 从游戏目录提取 GameAssembly.dll + global-metadata.dat
   ↓
2. 运行 Il2CppDumper.exe，选择 GameAssembly.dll
   ↓
3. 生成 dump.cs、script.json、il2cpp.h 等文件
   ↓
4. 在 dump.cs 中搜索类名/方法名，获取 RVA 和字段偏移
   ↓
5. 在 script.json 中查找方法绝对地址
   ↓
6. 编写 Frida 脚本，使用 RVA + 模块基址计算绝对地址
```

### RVA 地址计算

```javascript
// Frida 脚本中的地址计算方式
var gameAssembly = Process.findModuleByName("GameAssembly.dll");
var base = gameAssembly.base;

// RVA 转绝对地址
var absoluteAddress = base.add(0xB64240);  // RVA 0xB64240

// Hook 函数
Interceptor.attach(absoluteAddress, {
    onEnter: function(args) { ... }
});
```

---

## 游戏逻辑分析

### 游戏架构

- **引擎**：Unity IL2CPP
- **核心 DLL**：GameAssembly.dll
- **进程名**：UnityCrossFire.exe
- **架构**：32 位（x86）

### 关键类继承关系

```
MonoBehaviour
    └── Component
        └── Weapon
            ├── WPN_Knife（刀武器）
            └── WPN_Gun（枪械武器）
                └── WPN_Gun.AmmoData（弹药数据）

GameManager（游戏管理器）
    └── ModeBase（模式基类）
        └── ModeBase_Nano（生化模式）

Recoil（后坐力控制器）
    └── ShootPosture（射击姿态）
```

### 核心数据结构

#### WPN_Knife（刀武器）

| 字段 | 偏移 | 类型 | 说明 |
|------|------|------|------|
| `combo1_AnimSpeed` | 0xEC | float | Combo1 轻击动画速度 |
| `data` | 0x68 | WeaponData* | 武器数据指针 |

#### WeaponData_Knife（武器数据）

| 字段 | 偏移 | 类型 | 说明 |
|------|------|------|------|
| `attackSpeed` | 0xE8 | Vector3 | 攻击速度（x=Combo1, y=Combo2, z=Bigshot） |

#### WPN_Gun.AmmoData（弹药数据）

| 字段 | 偏移 | 类型 | 说明 |
|------|------|------|------|
| `clip_encrypted` | 0x08 | ObscuredInt | 弹夹子弹（加密） |
| `clip_hiddenValue` | 0x0C | ObscuredInt | 弹夹真实值 |
| `ammo_encrypted` | 0x1C | ObscuredInt | 备用子弹（加密） |
| `ammo_hiddenValue` | 0x20 | ObscuredInt | 备用真实值 |

#### ObscuredInt（加密整数）

| 字段 | 偏移 | 类型 | 说明 |
|------|------|------|------|
| `currentCryptoKey` | 0x0 | int | 当前加密密钥 |
| `hiddenValue` | 0x4 | int | 实际存储值（XOR 加密） |
| `inited` | 0x8 | byte | 初始化标志 |
| `fakeValue` | 0xC | int | 假值（防作弊检测） |

**加密原理**：`hiddenValue = 真实值 XOR cryptoKey`

#### Recoil（后坐力）

| 字段 | 偏移 | 类型 | 说明 |
|------|------|------|------|
| `<addYaw>k__BackingField` | 0x68 | float | 后坐力 Yaw |
| `<addPitch>k__BackingField` | 0x6C | float | 后坐力 Pitch |
| `addYaw_Target` | 0x70 | float | 目标 Yaw |
| `addPitch_Target` | 0x74 | float | 目标 Pitch |

### 回合结束流程（无限时间分析）

```
游戏进行中
    ↓
触发回合结束条件（时间耗尽/分数达标/一方胜利）
    ↓
调用 CheckRoundOver()
    ↓
调用 OnTimeOut() / SoldierWin() / GhostWin()
    ↓
调用 GameManager.GameRoundEnd()
    ↓
调用 GameManager.set_gameRoundOver(true)
    ↓
回合结束，进入结算界面
```

**拦截策略**：Hook 上述所有方法，阻止执行或修改参数。

---

## 四大功能模块

### 1. 🗡️ 快刀

**脚本文件**：`快刀/speed_knife.js`

**功能**：将刀攻击动画速度提升 3 倍，使轻击和重击出刀更快。

**实现原理**：
1. Hook `WPN_Knife::PlayKnifeAttackAnim`（RVA: 0xB642B0）
2. Hook `WPN_Knife::OnSpecialBtnDown`（RVA: 0xB64240）
3. Hook `WPN_Knife::AnimSpeedSetting`（RVA: 0xB63BD0）
4. 在 Hook 回调中调用 `Animator.set_speed` 设置动画速度
5. 同时修改 `combo1_AnimSpeed`（0xEC）和 `attackSpeed`（0xE8~0xF0）

**关键地址**：
- `Animator.set_speed`：0xAA8C30
- `Weapon.get_isMyWeapon`：0xB6E1D0

**配置参数**：
```javascript
var SPEED_MULTIPLIER = 3.0;  // 速度倍数，可自定义
```

---

### 2. ⏱️ 全模式无限时间

**脚本文件**：`全模式-无限时间/time_freeze_nano_ultimate_v2.js`

**功能**：锁定所有游戏模式的时间为 99:59，阻止回合结束。

**实现原理**：
1. Hook 10 个回合结束相关方法
2. 采用两种拦截策略：
   - **空实现**：让方法什么都不做
   - **修改参数**：将 `set_gameRoundOver(true)` 改为 `false`

**Hook 方法列表**：

| 序号 | 方法 | RVA | 拦截方式 |
|------|------|-----|---------|
| 1 | `ModeBase_Nano.CheckRoundOver` | 0xAEF8A0 | 空实现 |
| 2 | `ModeBase_Nano.OnTimeOut` | 0xAF1920 | 空实现 |
| 3 | `ModeBase_Nano.SoldierWin` | 0xAF3620 | 空实现 |
| 4 | `ModeBase_Nano.GhostWin` | 0xAF0550 | 空实现 |
| 5 | `GameManager.GameRoundEnd` | 0xAFAA40 | 空实现 |
| 6 | `ModeBase.ExitGame` | 0xAEE850 | 空实现 |
| 7 | `ModeBase.RefreshNextRound` | 0xAF5C50 | 空实现 |
| 8 | `GameManager.ResetRound` | 0xAFBCA0 | 空实现 |
| 9 | `GameManager.ReturnLobby` | 0xAFBF20 | 空实现 |
| 10 | `GameManager.set_gameRoundOver` | 0xAFE420 | 修改参数 true→false |

---

### 3. 🎯 无后座力

**脚本文件**：`无后座力/no_recoil_v4_fix.js`

**功能**：消除所有枪械后坐力，射击时准心不抖动。

**实现原理**：
1. Hook `Recoil::OnGunShot`（RVA: 0xB19980）
2. 在开枪回调中清零后坐力参数：
   - `addYaw`（0x68）= 0
   - `addPitch`（0x6C）= 0
   - `addYaw_Target`（0x70）= 0
   - `addPitch_Target`（0x74）= 0
3. 使用武器缓存策略识别玩家武器（避免 Hook 敌人武器）

**关键地址**：
- `Recoil.OnGunShot`：0xB19980
- `WPN_Gun.GunShoot`：0xB624C0
- `WPN_Gun.GunShoot_NoCheck`：0xB621F0

**优化策略**：
- 不 Hook Update 函数（避免每帧调用导致掉帧）
- 只 Hook 开枪相关函数（触发频率低）
- 使用 Interceptor.replace 直接跳过 Recoil 生成

---

### 4. 🔫 无限子弹

**脚本文件**：`无限子弹/infinite_ammo_god.js`

**功能**：所有武器弹药无限，射击不消耗子弹。

**实现原理**：
1. Hook 弹药消耗相关函数
2. 解析 ObscuredInt 加密结构
3. 修改 `hiddenValue` 字段绕过加密检查
4. 使用定时器每 50ms 锁定弹药值（防止游戏恢复）

**关键地址**：
- `WPN_Gun.ammoData` 指针偏移：0xF4
- `AmmoData.clip_hiddenValue` 偏移：0x0C
- `AmmoData.ammo_hiddenValue` 偏移：0x20

**ObscuredInt 修改方法**：
```javascript
// 读取加密值
var hiddenValue = ammoData.add(0x0C).readS32();
var cryptoKey = ammoData.add(0x00).readS32();

// 计算真实值
var realValue = hiddenValue ^ cryptoKey;

// 修改为最大值（保持加密格式）
var newValue = 999 ^ cryptoKey;
ammoData.add(0x0C).writeS32(newValue);
```



## 使用指南

### 前置条件

1. **操作系统**：Windows 10/11（32 位或 64 位）
2. **游戏**：UnityCrossFire.exe 已安装并可以正常运行
3. **管理员权限**：建议以管理员权限运行修改器
4. **Frida 环境**（仅开发者需要，用户无需安装）：
   - Python 3.8+
   - frida-tools 12.0+
   - PyInstaller 6.0+

### 安装流程

#### 方式一：使用打包好的 EXE（推荐用户）

1. 下载 `dist_pkg/NoRecoilLauncher.exe`
2. 双击运行，程序会自动：
   - 检测游戏进程
   - 注入 Frida 脚本
   - 启动无后座力功能

#### 方式二：使用 Electron 控制台（完整功能）

1. 进入 `game-modifier` 目录
2. 安装依赖：
   ```bash
   npm install
   ```
3. 启动控制台：
   ```bash
   npm run dev
   ```
4. 在控制台界面中：
   - 等待检测到游戏进程
   - 点击「注入进程」
   - 开启需要的功能开关

#### 方式三：手动注入（开发者）

1. 获取游戏进程 PID：
   ```powershell
   frida-ls-devices
   frida-ps -U
   ```
2. 注入脚本：
   ```powershell
   frida -p <PID> -l 快刀/speed_knife.js
   frida -p <PID> -l 全模式-无限时间/time_freeze_nano_ultimate_v2.js
   frida -p <PID> -l 无后座力/no_recoil_v4_fix.js
   frida -p <PID> -l 无限子弹/infinite_ammo_god.js
   ```

### 操作指南

#### 快刀功能

1. 启动游戏，进入战斗
2. 注入 `speed_knife.js`
3. 使用刀攻击，观察动画速度提升
4. 如需调整速度倍数，修改脚本中的 `SPEED_MULTIPLIER` 参数

#### 无限时间功能

1. 启动游戏，进入任意模式
2. 注入 `time_freeze_nano_ultimate_v2.js`
3. 时间将锁定在当前值，不会减少
4. 回合不会结束，可以无限游玩

#### 无后座力功能

1. 启动游戏，装备任意枪械
2. 注入 `no_recoil_v4_fix.js`
3. 开枪测试，准心应保持稳定
4. 日志会显示拦截的后坐力调用次数

#### 无限子弹功能

1. 启动游戏，装备任意武器
2. 注入 `infinite_ammo_god.js`
3. 开枪测试，弹药不会减少
4. 日志会显示弹药锁定状态


## 开发挑战与解决方案

### 挑战 1：IL2CPP 加密混淆

**问题**：Unity IL2CPP 编译后的代码经过混淆，类名和方法名难以识别。

**解决方案**：
1. 使用 Il2CppDumper 提取 `dump.cs` 和 `script.json`
2. 通过方法签名和 RVA 地址定位目标函数
3. 结合游戏行为分析（开枪、扣血等）验证 Hook 位置

---

### 挑战 2：ObscuredInt 加密

**问题**：游戏使用 ActiKs ObscuredTypes 对关键数值进行加密，直接修改无效。

**解决方案**：
1. 分析 ObscuredInt 内存结构（16 字节）
2. 理解 XOR 加密原理：`hiddenValue = 真实值 XOR cryptoKey`
3. 修改 `hiddenValue` 字段而非直接修改显示值
4. 使用定时器持续锁定，防止游戏恢复原始值

---

### 挑战 3：玩家/敌人识别

**问题**：Hook 会同时影响玩家和敌人，需要区分。

**解决方案**：
1. 初期尝试调用 `Player.get_isMyPlayer` 和 `Weapon.get_isMyWeapon`
2. 发现 NativeFunction 调用不稳定后，改用**缓存策略**
3. 记录前 N 个触发 Hook 的武器指针作为玩家武器
4. 在 Hook 回调中检查指针是否在缓存中

---

### 挑战 4：性能优化

**问题**：Hook Update 函数导致严重掉帧，游戏卡顿。

**解决方案**：
1. 避免 Hook 每帧调用的函数（如 Update、LateUpdate）
2. 只 Hook 事件触发函数（如 OnGunShot、PlayKnifeAttackAnim）
3. 使用 `Interceptor.replace` 替代 `Interceptor.attach` 减少开销
4. 最小化 JS 层操作，最大化 Native 执行

---

### 挑战 5：多版本兼容

**问题**：游戏更新后 RVA 地址变化，脚本失效。

**解决方案**：
1. 所有地址基于 RVA 而非绝对地址
2. 游戏更新后只需重新运行 Il2CppDumper 获取新 RVA
3. 更新脚本中的 RVA 常量即可恢复功能
4. 维护多个版本脚本（如 infinite_bag_switch_v1~v65）

---

### 挑战 6：Frida 消息循环崩溃

**问题**：使用 `arguments.callee` 在 strict mode 下报错，导致后续功能全部丢失。

**解决方案**：
1. 移除 `'use strict'` 或使用命名函数替代 `arguments.callee`
2. 改用 `recv('toggle', onToggle)` + `function onToggle(data) { ... }` 模式
3. 确保消息循环不会因异常中断

---

## 技术踩坑与经验教训

### 坑 1：arguments.callee 在 strict mode 报错

**现象**：Agent 脚本开头的 `'use strict'` 模式下，`recv('toggle', arguments.callee)` 抛出 `TypeError`，Frida 消息循环崩溃。

**教训**：
- ❌ 永远不要在 strict mode 下使用 `arguments.callee`
- ✅ 使用命名函数：`function onToggle(data) { ... }; recv('toggle', onToggle)`

---

### 坑 2：send() 消息洪泛导致 IPC 通道阻塞

**现象**：Agent 脚本中频繁调用 `send()` 发送日志，导致 Frida IPC 通道阻塞，游戏无响应。

**教训**：
- ❌ 不要在 Hook 回调中频繁调用 `send()`
- ✅ 实现模块级日志限频（每模块最多 10 条）
- ✅ 主进程端实现时间节流（每 300ms 推送一次）

---

### 坑 3：Process.setExceptionHandler 拦截系统异常

**现象**：设置全局异常处理器后，游戏自身的异常被拦截，导致游戏崩溃。

**教训**：
- ❌ 不要设置全局异常处理器拦截游戏异常
- ✅ 让游戏自己处理异常，只在 Agent 脚本内部使用 try/catch

---

### 坑 4：setInterval 在游戏进程中运行

**现象**：在 Agent 脚本中使用 `setInterval` 定时器，导致游戏主线程阻塞。

**教训**：
- ❌ 不要在 Agent 脚本中使用长时间运行的定时器
- ✅ 如果必须使用，确保回调函数极其轻量
- ✅ 优先使用 Hook 回调而非定时器

---

### 坑 5：NativeFunction 参数类型不匹配

**现象**：调用 `Weapon.get_isMyWeapon` 时，指针类型不匹配导致返回错误结果。

**教训**：
- ❌ 不要假设 NativeFunction 的参数类型
- ✅ 仔细检查 dump.cs 中的方法签名
- ✅ 使用正确的参数类型：`["pointer", "pointer"]` 而非 `["pointer"]`

---

### 坑 6：Hook 位置选择错误

**现象**：Hook `AnimSpeedSetting` 只在切换武器时调用，挥刀时不触发。

**教训**：
- ❌ 不要只 Hook 初始化函数
- ✅ Hook 每次操作都会调用的函数（如 `PlayKnifeAttackAnim`）
- ✅ 通过日志验证 Hook 触发频率

---

### 坑 7：快刀关闭后仍然生效

**现象**：关闭快刀功能后，武器动画速度仍然很快。

**原因**：快刀修改的是武器对象的**静态属性**，值写入后永久保存在内存中。

**教训**：
- 静态属性修改需要在 disable() 时恢复原始值
- 或者接受现状（只影响玩家自己的武器）
- 动态计算值修改（如无限时间）关闭后立即失效

---

### 坑 8：DLL 注入 vs Frida 注入

**现象**：尝试使用 DLL 注入实现修改功能，但 IL2CPP 环境下难以定位函数地址。

**教训**：
- ❌ DLL 注入需要编译时链接，不适合动态修改
- ✅ Frida 注入基于运行时插桩，更灵活
- ✅ Frida 支持热插拔，无需重启游戏

---

### 经验总结

| 经验 | 说明 |
|------|------|
| **先分析后开发** | 使用 Il2CppDumper 完整分析游戏结构再编写脚本 |
| **从小处开始** | 先 Hook 单个函数验证效果，再逐步扩展 |
| **日志是关键** | 完善的日志系统能快速定位问题 |
| **性能优先** | 避免 Hook 高频函数，减少 JS 层操作 |
| **版本管理** | 维护多个版本脚本应对游戏更新 |
| **用户友好** | 打包为单文件 EXE，用户无需安装依赖 |
| **安全第一** | 只修改玩家自己的数据，不影响其他玩家 |

---

## 📚 相关文档

| 文档 | 路径 | 说明 |
|------|------|------|
| Frida 技术手册 | `Frida游戏修改技术手册.md` | 完整的技术指南 |
| 快刀开发总结 | `快刀/快刀功能开发总结.md` | 快刀功能开发过程 |
| 无限时间原理 | `全模式-无限时间/生化模式无限时间实现原理分析.md` | 时间冻结原理 |
| 无后座力文档 | `无后座力/无后坐力V4技术文档.md` | 无后座力 V4 完整文档 |
| 无限子弹方案 | `无限子弹/无限子弹成功方案.md` | 无限子弹成功方案 |
| 背包切换手册 | `全模式-无限时间/无限背包切换技术手册.md` | 背包切换技术 |

---

## ⚠️ 免责声明

本项目仅供学习和研究使用，请勿用于商业用途或破坏游戏公平性。使用本工具可能导致游戏账号封禁，请自行承担风险。

---

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。
