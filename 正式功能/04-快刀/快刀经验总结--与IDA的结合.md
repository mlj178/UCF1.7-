# UnityCrossFire 快刀功能开发完整总结

## 1. 目标与背景

- **游戏**：Unity IL2CPP 引擎 FPS 游戏  
- **目标**：通过 Frida 动态修改内存，使玩家出刀动画速度大幅提升，且不影响其他玩家（人机）。  
- **关键 DLL**：`GameAssembly.dll`  
- **攻击类型**：轻击第一段（Combo1）、轻击第二段（Combo2）、重击（Bigshot）

---

## 2. 数据结构回顾

### 2.1 武器类继承链
`WPN_Knife` → `Weapon`

### 2.2 关键速度字段

| 字段                  | 所在结构                               | 偏移        | 说明                           |
| --------------------- | -------------------------------------- | ----------- | ------------------------------ |
| `combo1_AnimSpeed`    | `WPN_Knife` 实例                       | `0xEC`      | 轻击第一段动画速度（直接有效） |
| `attackSpeed.x`       | `WeaponData_Knife`（通过 `data` 指针） | `data+0xE8` | 轻击第一段备选（未采用）       |
| `attackSpeed.y`       | 同上                                   | `data+0xEC` | 轻击第二段速度                 |
| `attackSpeed.z`       | 同上                                   | `data+0xF0` | 重击速度                       |
| `Modifier_KnifeSpeed` | `PlayerWeapons`                        | `0x44`      | 玩家专属的刀速乘数，影响所有段 |

- **data 指针路径**：`WPN_Knife` 实例 `+0x68` → 读取 `WeaponData_Knife` 对象。

### 2.3 玩家武器判断

游戏内置函数 `Weapon.get_isMyWeapon()`（RVA `0xB6E1D0`）可判断武器是否属于本地玩家；`Player.get_isMyPlayer()`（RVA `0xB55FD0`）判断 `Player` 实例。

---

## 3. 版本演进与错误分析

### 3.1 V5 – 双速度直接写入（问题版本）

**V5 核心逻辑**：

```javascript
// Hook OnSpecialBtnDown, PlayKnifeAttackAnim, AnimSpeedSetting
function setAllSpeeds(weaponPtr, source) {
    // 轻击：直接写 combo1_AnimSpeed (0xEC)
    weaponPtr.add(0xEC).writeFloat(SPEED_MULTIPLIER);
    // 重击：通过 data 指针写 attackSpeed.z (0xF0)
    var dataPtr = weaponPtr.add(0x68).readPointer();
    dataPtr.add(0xF0).writeFloat(SPEED_MULTIPLIER);
}

// 每 16ms 定时器强制刷新所有已缓存武器
setInterval(function() {
    for (var key in playerWeapons) {
        setAllSpeeds(ptr(key), "TIMER");
    }
}, 16);
```

#### V5 的三大错误

**错误1：玩家武器判定依赖前两把缓存，导致第三把刀无效**

```javascript
var MAX_PLAYER_WEAPONS = 2;
function isPlayerWeapon(weaponPtr) {
    if (playerWeapons[key]) return true;
    if (playerWeaponCount < MAX_PLAYER_WEAPONS) {
        playerWeapons[key] = true;
        playerWeaponCount++;
        return true;
    }
    return false; // 第三个武器直接被拒！
}
```
- 游戏中可能同时存在多个武器实例（不同背包或丢弃的刀），只缓存前两个会导致切换背包后新的刀无法被识别为玩家武器，因而失效。  
- 日志表现：只有前两把刀速度被修改，第三把刀还原。

**错误2：16ms 定时器高频写入，造成严重卡顿且仅在团队模式“能用”**

- 每 16 毫秒遍历所有缓存武器写入速度，会产生大量内存访问和异常捕获开销，导致游戏帧率下降。  
- 在特殊模式（个人竞技、生化）中，武器对象生命周期或实例布局可能不同，定时器反复对可能的无效指针写入，引发更多异常或逻辑错误，从而表现为“其他模式无法使用，卡顿严重”。

**错误3：速度倍数过高时数值越界，刀速被重置**

- 代码中没有对写入值做范围限制，当 `SPEED_MULTIPLIER` 设为 20 时，直接写入 `20.0`。  
- 游戏内部可能存在最大有效值检查（例如 `>15.0` 视为非法），导致动画速度被强制恢复为默认值。  
- 用户反馈：倍速 20 挥几刀失效，13 也几秒后失效。这通常是因为游戏某个校验点将速度钳制回正常范围，而 V5 的定时器可能还在反复写入，但 Hook 触发时机不对，导致最终被覆盖。

---

### 3.2 V11 – 全背包+三段加速，但人机也被加速

**V11 改进点**：

- 移除定时器，全部改为事件驱动（Hook 触发时修改）。
- 使用 `Weapon.get_isMyWeapon()` 实时判断玩家武器，不再缓存，从而支持所有背包。
- 同时修改轻击第一段 `combo1_AnimSpeed`（0xEC），并通过 `data` 指针修改 `attackSpeed.y` 和 `attackSpeed.z` 以实现轻击第二段和重击加速。

```javascript
function hook(addr, name) {
    Interceptor.attach(addr, {
        onEnter(args) {
            var self = args[0];
            if (isMyWeapon(self, ptr(0))) { // 判断是否玩家武器
                setCombo1Speed(self, name);
                setAttackSegmentSpeeds(self);
            }
        }
    });
}
```

**V11 的新问题：人机的刀也变快了**

- 根源在于 `isMyWeapon(self, ptr(0))` 的判断逻辑。  
  该函数签名是 `bool get_isMyWeapon(void *weapon, void *player)`。V11 传入 `ptr(0)` 作为第二个参数，这可能在某些情况下错误地返回 `true`（例如当 player 为 null 时，函数内部比较宽松），导致人机武器也被当成玩家武器修改。
- 此外，`setAttackSegmentSpeeds` 中修改的是 `WeaponData_Knife` 对象，而 `data` 指针可能是**共享**的（同一刀型的 WeaponData 可能被多个武器实例引用），一旦修改，所有使用相同数据的刀（包括人机）都会受影响。

**V11 代码中的共享修改证据**：

```javascript
function setAttackSegmentSpeeds(weaponPtr) {
    var dataPtr = weaponPtr.add(0x68).readPointer();
    // 修改 data + 0xEC (attackSpeed.y) 和 data + 0xF0 (attackSpeed.z)
    dataPtr.add(0xEC).writeFloat(SPEED);
    dataPtr.add(0xF0).writeFloat(SPEED);
}
```
- 这里直接写入了 WeaponData 对象，而这个对象可能是全局的，导致人机刀速也被修改。

---

### 3.3 V16 – 终极方案：替换 `get_KnifeSpeed`，仅玩家生效

**V16 核心思路**（来自方案5分析文档）：  

通过 IDA 反编译 `PlayKnifeAttackAnim` 发现，所有攻击段的**最终速度 = `PlayerWeapons.KnifeSpeed` × 各段基础速度**。  
`PlayerWeapons` 是**每个玩家独立**的对象，其中的 `Modifier_KnifeSpeed`（偏移 `0x44`）是一个乘数修饰符。只需要让本地玩家的 `get_KnifeSpeed` 返回加速后的值，就能实现：

- 轻击、重击全部加速
- 只影响玩家自己
- 不影响人机
- 切换背包自动有效
- 退出房间自动失效

**V16 实现方式**：使用 Frida 的 `Interceptor.replace` 替换原 `PlayerWeapons.get_KnifeSpeed` 函数为一个 `NativeCallback`，在回调中判断所属玩家是否为本地玩家。

```javascript
var isMyPlayer = new NativeFunction(isMyPlayerAddr, "bool", ["pointer"]);
var originalGetKnifeSpeed = new NativeFunction(getKnifeSpeedAddr, "float", ["pointer"]);

Interceptor.replace(getKnifeSpeedAddr, new NativeCallback(function(self) {
    var owner = self.add(0x8).readPointer(); // PlayerWeapons + 0x8 = owner (Player)
    if (owner && !owner.isNull() && isMyPlayer(owner)) {
        return SPEED; // 本地玩家返回高倍速
    }
    return originalGetKnifeSpeed(self); // 其他玩家调用原函数
}, "float", ["pointer"]));
```

- `PlayerWeapons` 实例通过 `+0x8` 获得所属的 `Player` 指针。
- `Player.get_isMyPlayer` 准确判断是否本地玩家。
- 对于非本地玩家，调用原始 `get_KnifeSpeed`，保证其速度不变。

**V16 的优势**：
- **零性能损耗**：没有定时器，只在读取刀速时触发，且函数替换属于原生调用，开销极低。
- **精确作用域**：直接修改计算因子，不会误伤共享的 `WeaponData`，因此人机完全不受影响。
- **全模式通用**：与模式无关，只要游戏用到 `PlayerWeapons` 计算刀速就生效。
- **安全上限**：如果速度倍率过高触发游戏内部钳制，依然是返回 `SPEED`，但游戏可将其钳制在合法上限，不会导致失效（只需将 SPEED 设为上限值即可，例如 13.0）。

**为什么 V16 能解决 V11 的人机问题？**

因为 V11 修改的是 `WPN_Knife` 实例字段或共享的 `WeaponData`，而 V16 修改的是 `PlayerWeapons` 的返回值，这是**每个玩家独立的逻辑**，不会跨实例污染。

---

## 4. 三个分析文档的整合要点

### 4.1 快刀方案5分析（PlayerWeapons.KnifeSpeed 发现过程）

- **关键发现**：通过 IDA 反编译 `PlayKnifeAttackAnim`，看到了 `v31 = sub_10B170A0(v22)` 即 `get_KnifeSpeed()`，并与 `v28` 相乘得到最终速度。
- **结论**：`PlayerWeapons.Modifier_KnifeSpeed`（0x44）是玩家专用的乘数，修改它即可优雅实现快刀。
- **该发现直接催生了 V16 方案**。

### 4.2 快刀功能开发总结（从 dump.cs 到 V5）

- 明确了攻击类型枚举、类继承、关键字段偏移。
- 记录了 V5 的双路径写入（combo1 实例字段 + data 指针 attackSpeed.z），并指出了只有前两把刀有效、倍速过高失效等问题。
- 为后续改进提供了数据基础。

### 4.3 快刀 Frida 开发总结（V11 开发经验）

- 总结了 V10/V11 中 `get_isMyWeapon` 和移除定时器的改进。
- 指出了 `attackSpeed.y` 对应轻击第二段，`attackSpeed.z` 对应重击。
- 强调了定时器危害和实时判断的重要性。

这三个文档分别对应“**发现关键字段** → **暴力实现与踩坑** → **优化到事件驱动但仍有缺陷**”的过程，最终由 V16 收敛到最优解。

---

## 5. 最终偏移与函数速查表

### 表1：关键函数 RVA

| 函数名                          | RVA      | 作用                             |
| ------------------------------- | -------- | -------------------------------- |
| `PlayerWeapons.get_KnifeSpeed`  | 0xB170A0 | 返回当前背包刀速乘数             |
| `Player.get_isMyPlayer`         | 0xB55FD0 | 判断是否本地玩家                 |
| `Weapon.get_isMyWeapon`         | 0xB6E1D0 | 判断武器是否属于玩家（已弃用）   |
| `WPN_Knife.OnSpecialBtnDown`    | 0xB64240 | 按下攻击键                       |
| `WPN_Knife.PlayKnifeAttackAnim` | 0xB642B0 | 播放攻击动画（速度计算发生于此） |
| `WPN_Knife.AnimSpeedSetting`    | 0xB63BD0 | 设置动画速度                     |

### 表2：关键字段偏移

| 字段                  | 所在类             | 偏移 | 类型             | 说明                          |
| --------------------- | ------------------ | ---- | ---------------- | ----------------------------- |
| `combo1_AnimSpeed`    | `WPN_Knife`        | 0xEC | float            | 仅影响轻击第一段              |
| `data`                | `Weapon`           | 0x68 | pointer          | 指向 WeaponData               |
| `attackSpeed.x`       | `WeaponData_Knife` | 0xE8 | float            | Combo1 基础速度（未单独使用） |
| `attackSpeed.y`       | `WeaponData_Knife` | 0xEC | float            | Combo2 基础速度               |
| `attackSpeed.z`       | `WeaponData_Knife` | 0xF0 | float            | Bigshot 基础速度              |
| `Modifier_KnifeSpeed` | `PlayerWeapons`    | 0x44 | PropertyModifier | 刀速乘数，V16 核心            |
| `owner`               | `PlayerWeapons`    | 0x8  | pointer          | 指向所属 Player               |

> 注：V16 不再需要直接操作 `WPN_Knife` 或 `WeaponData` 的任何字段，只需替换 `get_KnifeSpeed` 即可。

---

## 6. 总结与经验

1. **从修改实例字段到修改玩家属性乘数**  
   - 修改武器实例字段/共享数据容易误伤他人，且需要复杂的事件管理。  
   - 修改 `PlayerWeapons.get_KnifeSpeed` 返回值是更上层的、玩家隔离的优雅方案。
2. **动态替换优于被动 Hook**  
   - V16 的 `Interceptor.replace` 直接替换函数实现，无需在多个 Hook 点重复写入，也没有定时器开销。
3. **游戏内部 clamp 是速度上限的硬限制**  
   - 倍数不能无限大，合理上限约 13~14，超过会被游戏钳制回默认，因此 V16 只需设定一个稳定上限即可。

**最终推荐脚本**：`speed_knife_v16.js`，替换 `get_KnifeSpeed`，全模式、全背包、仅玩家生效，无卡顿，无需重复注入。







快刀倍速20的话，打几刀人物的手臂和刀就失效了。可能超出范围了。必须切换武器才能再次看到手臂。

  尝试最多就是13是上限，14就不行了。
13也不行了，挥刀几秒钟就消失了，游戏帧率可能是60，需要解锁60帧率

