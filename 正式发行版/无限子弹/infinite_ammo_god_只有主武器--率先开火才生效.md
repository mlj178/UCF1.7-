# ✅ 无限子弹成功方案 - 完整记录

## 📋 最终成功方案

### 使用的脚本
**文件名**: `infinite_ammo_god.js`

**使用方法**:
```powershell
cd D:\trae_project\InfiniteAmmoDLL
frida -p <PID> -l infinite_ammo_god.js
```

---

## 🔍 核心发现

### 1. 游戏架构
- **引擎**: Unity IL2CPP
- **程序集**: `GameAssembly.dll`
- **基地址**: 动态加载（Frida 自动获取）

### 2. 关键类结构

#### WPN_Gun 类（武器基类）
```
WPN_Gun 对象结构:
  0x000 - 0x0F0: 其他数据
  0x0F4: ammoData 指针 (指向 AmmoData 对象)
  0x0F8 - 0x0FC: 其他数据
```

#### AmmoData 结构（弹药数据）
```
AmmoData 对象:
  0x00: 类型指针
  0x04: 填充
  0x08: clip_encrypted (ObscuredInt 加密值)
  0x0C: clip_hiddenValue (ObscuredInt 真实加密值) ← 修改这里！
  0x10: clip_inited
  0x14 - 0x18: 填充
  0x1C: ammo_encrypted (ObscuredInt 加密值)
  0x20: ammo_hiddenValue (ObscuredInt 真实加密值) ← 修改这里！
  0x24: ammo_inited
```

### 3. ObscuredInt 加密结构
```
ObscuredInt (16 字节):
  0x0: currentCryptoKey (4 字节)
  0x4: hiddenValue (4 字节) ← 实际存储的值
  0x8: inited (1 字节)
  0xC: fakeValue (4 字节)
  0x10: fakeValueActive (1 字节)
```

**加密原理**:
- `hiddenValue = 真实值 XOR cryptoKey`
- 每次读取时：`真实值 = hiddenValue XOR currentCryptoKey`
- 直接修改 `hiddenValue` 可以绕过加密检查

---

## 🎯 关键内存地址

### Cheat Engine 手动修改方案

#### 步骤 1: 找到玩家的枪指针
1. 打开 CE，附加到 `UnityCrossFire.exe`
2. 搜索类型：**Pointer** (指针)
3. 第一次扫描：值 = `0` (或未知值)
4. 在游戏中开枪
5. 再次扫描：值 **改变** 的
6. 重复直到找到 **WPN_Gun 对象指针**

#### 步骤 2: 找到 ammoData 指针
```
WPN_Gun 地址 + 0xF4 = ammoData 指针
```
例如：
- WPN_Gun = `0x45EDC2E0`
- ammoData = `0x45EDC2E0 + 0xF4` → 读取这个地址的指针值 → 得到 `0x45E92240`

#### 步骤 3: 修改弹药值
```
ammoData + 0x0C = 弹夹子弹加密值
ammoData + 0x20 = 备用子弹加密值
```

**修改方法**:
1. 在 CE 中添加地址：`[ ammoData 地址 + 0x0C ]`
2. 类型：**4 Bytes**
3. 值：修改为当前值（保持不变）
4. 添加地址：`[ ammoData 地址 + 0x20 ]`
5. 值：修改为当前值

**关键点**: 必须**每帧都修改**，否则游戏会恢复！

---

## 💻 Frida 自动化方案

### 完整脚本代码
```javascript
// infinite_ammo_god.js
console.log("[*] === GOD MODE Infinite Ammo ===");

(function() {
    var gameAssembly = Process.findModuleByName("GameAssembly.dll");
    
    var playerGun = null;
    var targetClip = 9999;
    var targetAmmo = 9999;

    // Hook 开火函数识别玩家枪支
    var fireFunctions = [0xB67AF0, 0xB62730, 0xB621F0, 0xAEA6B0];

    for (var i = 0; i < fireFunctions.length; i++) {
        var addr = gameAssembly.base.add(fireFunctions[i]);
        
        Interceptor.attach(addr, {
            onEnter: function(args) {
                var thisPtr = args[0];
                
                if (thisPtr === null || thisPtr.isNull()) return;

                if (playerGun === null) {
                    playerGun = thisPtr;
                    console.log("[+] Player gun: " + playerGun);
                    
                    var ammoDataPtr = thisPtr.add(0xF4).readPointer();
                    if (!ammoDataPtr.isNull()) {
                        targetClip = ammoDataPtr.add(0x0C).readInt();
                        targetAmmo = ammoDataPtr.add(0x20).readInt();
                        console.log("[*] Target clip_h: " + targetClip);
                        console.log("[*] Target ammo_h: " + targetAmmo);
                    }
                }
            }
        });
    }

    // 每 50ms 强制锁定弹药值
    setInterval(function() {
        if (playerGun !== null) {
            try {
                var ammoDataPtr = playerGun.add(0xF4).readPointer();
                if (!ammoDataPtr.isNull()) {
                    ammoDataPtr.add(0x0C).writeInt(targetClip);
                    ammoDataPtr.add(0x20).writeInt(targetAmmo);
                }
            } catch (e) {}
        }
    }, 50);

    console.log("[+] Continuous lock enabled!");
})();
```

---

## 🔧 开火函数地址列表

以下函数在开枪时会被调用（可用于识别玩家枪支）：

| 函数名 | RVA 地址 | 说明 |
|--------|---------|------|
| `Weapon.Fire` | `0xB67AF0` | 基类开火函数 |
| `WPN_Gun.GunShoot` | `0xB62730` | 武器开火 |
| `WPN_Gun.GunShoot_NoCheck` | `0xB621F0` | 无检查开火 |
| `WPN_Gun.Shoot` | `0xAEA6B0` | 射击函数 |

---

## 📊 实际内存示例

### 玩家的枪（实战数据）
```
WPN_Gun 地址：0x45EDC2E0
ammoData 指针：0x45E92240 (读取 0x45EDC2E0+0xF4 得到)

AmmoData 内容:
  0x00: 0x0F616BF8 (类型指针)
  0x04: 0x00000000
  0x08: 0x0006C81C (444444) - clip_encrypted
  0x0C: 0x0006C83E (444478) - clip_hiddenValue ← 修改这个！
  0x10: 0x00000001
  0x14: 0x00000000
  0x18: 0x00000000
  0x1C: 0x0006C81C (444444) - ammo_encrypted
  0x20: 0x0006C890 (444560) - ammo_hiddenValue ← 修改这个！
  0x24: 0x00000001
```

---

## ⚠️ 失败方案总结

### 方案 1: Hook ConsumeAmmo (0xB61140)
**失败原因**: 这个函数只是**检查**弹药，不**减少**弹药

### 方案 2: 只恢复一次
**失败原因**: 游戏有**持续检测**，必须每帧恢复

### 方案 3: 修改加密值而不是 hiddenValue
**失败原因**: ObscuredInt 读取的是 `hiddenValue XOR cryptoKey`，必须修改 hiddenValue

---

## ✅ 成功关键

1. **找对地方**: `AmmoData` 对象的 `0x0C` 和 `0x20` 偏移
2. **持续锁定**: 每 50ms 强制写入一次（比游戏更新快）
3. **识别玩家枪支**: Hook 开火函数，第一把被调用的就是玩家的枪
4. **保持原值**: 使用当前加密值作为目标值，不会触发反作弊

---

## 🎮 使用步骤

### Frida 方案（推荐）
```powershell
# 1. 启动游戏
# 2. 进入游戏对局
# 3. 打开 PowerShell
cd D:\trae_project\InfiniteAmmoDLL

# 4. 查找游戏进程 ID
Get-Process UnityCrossFire

# 5. 注入脚本（替换 PID）
frida -p <PID> -l infinite_ammo_god.js

# 6. 回到游戏开枪 - 无限子弹生效！
```

### Cheat Engine 方案（手动）
1. CE 附加进程
2. 搜索 WPN_Gun 指针（参考上文）
3. 计算 ammoData 地址 = `WPN_Gun + 0xF4`
4. 添加两个地址到 CE 列表：
   - `[[WPN_Gun]+0xF4]+0x0C`
   - `[[WPN_Gun]+0xF4]+0x20`
5. 锁定这两个值为当前值
6. 开枪测试

---

## 📝 备注

- **加密值会变化**: 每次游戏启动加密密钥都不同，不能用固定值
- **Bot 干扰**: 游戏中 Bot 的枪也会调用开火函数，要识别玩家枪支
- **反作弊**: 修改幅度不要太大，保持原始加密值最安全

---

## 📂 相关文件

所有脚本位于：`D:\trae_project\InfiniteAmmoDLL\`

| 文件名 | 说明 | 状态 |
|--------|------|------|
| `infinite_ammo_god.js` | 上帝模式（成功✅） | ✅ 可用 |
| `infinite_ammo_working.js` | 恢复弹药（测试用） | ⚠️ 不完整 |
| `find_real_fire_function.js` | 查找开火函数 | 🔧 调试用 |
| `dump_gun_once.js` | 内存转储 | 🔧 调试用 |

---

**生成时间**: 2026-04-22  
**游戏版本**: UnityCrossFire 1.7.1  
**Frida 版本**: 17.9.1
