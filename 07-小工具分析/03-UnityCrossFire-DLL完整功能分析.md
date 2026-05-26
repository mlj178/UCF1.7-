# UnityCrossFire.dll 完整功能分析报告

**分析日期**: 2026-05-26  
**分析工具**: IDA Pro 9.0 + MCP  
**目标文件**: UnityCrossFire.dll  

---

## 一、DLL基本信息

### 1.1 文件元数据

| 属性 | 值 |
|------|-----|
| **文件路径** | `D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire.dll` |
| **基址** | `0x10000000` |
| **模块大小** | `0x64000` (IDB) / `0x5FC00` (文件) |
| **MD5** | `2be82d9a5c9820a3ecc224b6b89e99b7` |
| **SHA256** | `3b5726a8ca661796c9b2904d5539d46aa0a26c24f309bf9349110251b6e50e92` |
| **CRC32** | `0x8d846bf3` |
| **UI框架** | Dear ImGui 1.91.5 WIP |

### 1.2 技术架构

- **游戏引擎**: Unity (IL2CPP)
- **渲染API**: DirectX 11
- **UI框架**: Dear ImGui 1.91.5
- **编程语言**: C++ (MSVC)
- **目标平台**: Windows 32位

---

## 二、功能模块总览

### 2.1 核心功能模块

| 模块名称 | 功能描述 | 实现状态 | 关键函数 |
|---------|---------|---------|---------|
| **自瞄系统** | 自动瞄准敌人 | ✅ 完整实现 | 0x1004ad3c区域 |
| **ESP透视** | 透视显示敌人信息 | ✅ 完整实现 | sub_1002AD70 |
| **武器修改** | 武器属性修改 | ✅ 完整实现 | GiveWeapon相关 |
| **ImGui界面** | 功能菜单界面 | ✅ 完整实现 | sub_10033140等 |
| **配置系统** | 配置文件读写 | ✅ 完整实现 | esp_config.ini |
| **热键系统** | 功能快捷键 | ✅ 完整实现 | GetAsyncKeyState |

### 2.2 辅助功能模块

| 模块名称 | 功能描述 | 关键技术 |
|---------|---------|---------|
| **内存管理** | 内存分配与释放 | GlobalAlloc/GlobalFree |
| **线程管理** | 多线程支持 | CreateThread |
| **文件操作** | 配置文件读写 | std::fstream |
| **坐标转换** | 屏幕坐标转换 | ScreenToClient/ClientToScreen |

---

## 三、自瞄功能详细分析

### 3.1 功能概述

**目标**: 实现自动瞄准最近敌人，支持平滑过渡和FOV限制

**实现位置**: 未识别函数区域 `0x1004a988 ~ 0x1004bc5e`

### 3.2 实现步骤

#### 步骤1: 热键检测
- **调用函数**: `GetAsyncKeyState` @ IAT 0x10051188
- **调用位置**: 
  - 0x1004ad3c - 主热键检测
  - 0x1004b435 - 辅助热键
  - 0x1004b7a9 - 功能切换
- **实现方法**: 检测按键状态，判断是否激活自瞄

#### 步骤2: 获取游戏管理器
- **目标类**: `GameManager` (字符串 @ 0x100538e4)
- **获取方法**: 通过IL2CPP反射API获取类实例
- **关键API**:
  - `il2cpp_class_get_method_from_name` - 获取方法
  - `il2cpp_class_get_field_from_name` - 获取字段

#### 步骤3: 获取本地玩家
- **数据来源**: GameManager实例的字段
- **验证条件**:
  - 玩家对象非空
  - 玩家未死亡
  - 玩家有效状态

#### 步骤4: 遍历敌人列表
- **数据结构**: 
  - `GameManager->playersBL` (蓝队, 偏移 +0x20)
  - `GameManager->playersGR` (红队, 偏移 +0x28)
- **筛选条件**:
  - 敌人对象非空
  - 敌人 != 本地玩家
  - 敌人队伍 != 本地队伍
  - 敌人未死亡

#### 步骤5: 可见性检测
- **Unity API**: `Physics.Linecast` (字符串 @ 0x100547fc)
- **方法签名**: `Boolean Linecast(Vector3 start, Vector3 end, Int32 layerMask)`
- **实现逻辑**: 从本地玩家位置向敌人位置发射射线，检测是否有遮挡物

#### 步骤6: 获取骨骼位置
- **目标骨骼**: 胸部 (BoneIndex = 7)
- **Unity API**: `Animator.GetBoneTransform`
- **坐标获取**: `Transform.get_position` (字符串 @ 0x10054674)

#### 步骤7: 计算瞄准角度
- **算法**: 
  ```
  dx = targetPos.x - selfPos.x
  dy = targetPos.y - selfPos.y
  dz = targetPos.z - selfPos.z
  hDist = sqrt(dx*dx + dz*dz)
  
  targetYaw = atan2(dx, dz) * 180 / PI
  targetPitch = atan2(dy, hDist) * 180 / PI
  ```

#### 步骤8: 角度平滑处理
- **配置参数**: 
  - 平滑系数 @ offset +3652 (默认 8.0)
  - 平滑系数2 @ offset +3653 (默认 5.5)
- **算法**:
  ```
  newYaw = currentYaw + (targetYaw - currentYaw) * smoothing
  newPitch = currentPitch + (targetPitch - currentPitch) * smoothing
  ```

#### 步骤9: 写入角度
- **目标字段**:
  - 相机Yaw @ Player +0x4C (76)
  - 相机Pitch @ Player +0x50 (80)
- **实现**: 直接内存写入

#### 步骤10: 重置标志
- **目标**: Transform组件的相关标志位
- **偏移**: +0x10, +0x24, +0x40, +0x54

### 3.3 关键数据结构

#### PlayerController结构
```cpp
struct PlayerController {
    // +0x00 ~ +0x1F: 虚函数表 + 基类数据
    int teamID;              // +0x20 (32): 队伍ID
    // +0x24 ~ +0x47: 其他数据
    float cameraYaw;         // +0x4C (76): 相机水平旋转
    float cameraPitch;       // +0x50 (80): 相机垂直旋转
    Transform* transform;    // +0x54 (84): Transform组件
    CharacterController* cc; // +0x58 (88): 角色控制器
    // ... 其他字段
};
```

#### Vector3结构
```cpp
struct Vector3 {
    float x;  // X坐标
    float y;  // Y坐标
    float z;  // Z坐标
};
```

### 3.4 配置参数

| 参数名 | 偏移 | 默认值 | 说明 |
|--------|------|--------|------|
| AimDistance | +3656 | 12.0f | 自瞄距离限制 |
| AimFOV | +3664 | 35.0f | FOV视野限制 |
| SmoothValue1 | +3652 | 8.0f | 平滑系数1 |
| SmoothValue2 | +3653 | 5.5f | 平滑系数2 |
| SmoothValue3 | +3657 | 8.0f | 平滑系数3 |

---

## 四、ESP透视功能详细分析

### 4.1 功能概述

**目标**: 在屏幕上绘制敌人信息，包括方框、骨骼、血量等

**实现函数**: `sub_1002AD70` @ 0x1002AD70 (大小: 0x17C)

### 4.2 ESP类型

#### 4.2.1 方框ESP (BoxESP)
- **配置项**: `BoxESP=` (字符串 @ 0x1005b290)
- **绘制内容**: 
  - 2D方框包围敌人
  - 方框颜色根据队伍变化
  - 方框大小根据距离调整

#### 4.2.2 骨骼ESP (BoneESP)
- **配置项**: `BoneESP=` (字符串 @ 0x1005b298)
- **绘制内容**:
  - 头部骨骼点
  - 胸部骨骼点
  - 四肢骨骼连线
- **骨骼索引**:
  - HEAD = 0
  - NECK = 3
  - LEFT_HAND = 6
  - CHEST = 7
  - PELVIS = 10

### 4.3 实现步骤

#### 步骤1: 获取主摄像机
- **Unity API**: `Camera.get_main` (字符串 @ 0x100546c4)
- **用途**: 世界坐标转屏幕坐标

#### 步骤2: 遍历所有玩家
- **Unity API**: `Object.FindObjectsOfType` (字符串 @ 0x10054534)
- **筛选**: 同自瞄功能

#### 步骤3: 世界坐标转屏幕坐标
- **Unity API**: `Camera.WorldToScreenPoint`
- **坐标转换**:
  - ScreenToClient (IAT @ 0x10051154)
  - ClientToScreen (IAT @ 0x10051160)

#### 步骤4: 计算ESP尺寸
- **参数**: 
  - ESP大小 @ offset +3639 (默认 50.0f)
  - ESP大小2 @ offset +3640 (默认 50.0f)
  - 透明度 @ offset +3642 (默认 1.0f)

#### 步骤5: ImGui绘制
- **绘制函数**: ImGui DrawList API
- **绘制内容**:
  - 方框 (AddRect)
  - 线条 (AddLine)
  - 文字 (AddText)

### 4.4 颜色配置

| 颜色类型 | R | G | B | A | 偏移 |
|---------|---|---|---|---|------|
| 队伍1颜色 | 0.7843 | 0.7961 | 0.8157 | 1.0 | +3697~+3700 |
| 队伍2颜色 | 0.5 | 0.6 | 0.7 | 1.0 | +3701~+3704 |
| 可见敌人 | 0.2 | 0.3 | 0.4 | 0.9 | +3705~+3708 |

---

## 五、武器修改功能详细分析

### 5.1 功能概述

**目标**: 修改武器属性，实现无限弹药等功能

### 5.2 关键Unity API

#### 5.2.1 GiveWeapon
- **签名**: `Weapon GiveWeapon(Player player, Int32 weaponIndex, Boolean autoGiveUp, Boolean autoSelect)`
- **字符串地址**: 0x10054918
- **功能**: 给予玩家指定武器

#### 5.2.2 GiveWeaponByBag
- **签名**: `Weapon GiveWeaponByBag(Player player, Int32 weaponIndex)`
- **字符串地址**: 0x10054974
- **功能**: 从背包给予武器

#### 5.2.3 GetWeapon
- **签名**: `Weapon GetWeapon(Int32 weaponIndex)`
- **字符串地址**: 0x100549b0
- **功能**: 获取指定武器

#### 5.2.4 SetCurrentWeapon
- **签名**: `Void SetCurrentWeapon(Int32 slot, Weapon wpn)`
- **字符串地址**: 0x100549d8
- **功能**: 设置当前武器

### 5.3 配置项

- **WeaponID**: `WeaponID=` (字符串 @ 0x1005b310)
- **InfiniteAmmo**: `InfiniteAmmo=` (字符串 @ 0x1005b2d8)

### 5.4 实现方法

1. **获取PlayerWeapons组件**
   - 类名: `PlayerWeapons` (字符串 @ 0x10054a08)
   
2. **调用武器API**
   - 通过IL2CPP反射调用GiveWeapon等方法
   
3. **修改武器属性**
   - 弹药数量
   - 射速
   - 伤害值

---

## 六、ImGui界面功能详细分析

### 6.1 功能概述

**目标**: 提供图形化配置界面

**UI框架**: Dear ImGui 1.91.5 WIP (字符串 @ 0x10054b4c)

### 6.2 关键函数

#### 6.2.1 ImGui初始化
- **函数**: `sub_10033140` @ 0x10033140
- **功能**: 初始化ImGui上下文和风格

#### 6.2.2 ImGui新帧
- **函数**: `sub_10033260` @ 0x10033260
- **功能**: 开始新的ImGui帧

#### 6.2.3 ImGui渲染
- **函数**: `sub_10034080` @ 0x10034080
- **功能**: 结束ImGui帧并渲染

#### 6.2.4 ImGui绘制
- **函数**: `sub_1002AD70` @ 0x1002AD70
- **功能**: 绘制ESP和菜单

### 6.3 界面元素

- **主菜单**: 功能开关
- **自瞄设置**: FOV、距离、平滑度
- **ESP设置**: 颜色、透明度、类型
- **武器设置**: 武器ID、无限弹药

### 6.4 配置文件

- **文件名**: `imgui.ini` (字符串 @ 0x10054a9c)
- **日志文件**: `imgui_log.txt` (字符串 @ 0x10054aa8)

---

## 七、配置系统详细分析

### 7.1 配置文件

**文件名**: `esp_config.ini` (字符串 @ 0x1005b280)

### 7.2 配置项列表

| 配置项 | 字符串地址 | 说明 |
|--------|-----------|------|
| BoxESP | 0x1005b290 | 方框ESP开关 |
| BoneESP | 0x1005b298 | 骨骼ESP开关 |
| AimKey | 0x1005b308 | 自瞄热键 |
| WeaponID | 0x1005b310 | 武器ID |
| InfiniteAmmo | 0x1005b2d8 | 无限弹药 |

### 7.3 配置加载函数

**函数**: `sub_1004A040` @ 0x1004A040 (大小: 0x948)

**功能**:
1. 检查配置初始化标志 `byte_1005F7C9`
2. 读取配置文件
3. 设置默认值
4. 初始化颜色表

### 7.4 默认配置值

详见反编译代码中的数值初始化部分（第3.4节）

---

## 八、Unity API调用详细分析

### 8.1 Transform相关API

| API签名 | 字符串地址 | 用途 |
|---------|-----------|------|
| `Transform get_transform()` | 0x1005464c | 获取Transform组件 |
| `Vector3 get_position()` | 0x10054674 | 获取世界坐标 |
| `Void get_position_Injected(Vector3& ret)` | 0x10054698 | 获取坐标(注入版) |
| `GameObject get_gameObject()` | 0x10054798 | 获取GameObject |

### 8.2 Camera相关API

| API签名 | 字符串地址 | 用途 |
|---------|-----------|------|
| `Camera get_main()` | 0x100546c4 | 获取主摄像机 |

### 8.3 Physics相关API

| API签名 | 字符串地址 | 用途 |
|---------|-----------|------|
| `Boolean Linecast(Vector3 start, Vector3 end, Int32 layerMask)` | 0x100547fc | 射线检测 |

### 8.4 Object相关API

| API签名 | 字符串地址 | 用途 |
|---------|-----------|------|
| `Object[] FindObjectsOfType(Type type)` | 0x10054534 | 查找所有对象 |

### 8.5 IL2CPP反射API

| API名称 | 字符串地址 | 用途 |
|---------|-----------|------|
| `il2cpp_class_get_method_from_name` | 0x10053bc0 | 获取方法 |
| `il2cpp_class_get_field_from_name` | 0x10053b80 | 获取字段 |
| `il2cpp_class_get_name` | 0x10053be4 | 获取类名 |
| `il2cpp_class_get_namespace` | 0x10053c1c | 获取命名空间 |

---

## 九、导入函数分析

### 9.1 USER32导入函数

| 函数名 | IAT地址 | 用途 |
|--------|---------|------|
| **GetAsyncKeyState** | 0x10051188 | **热键检测** |
| **SetCursorPos** | 0x100511ac | 鼠标位置控制 |
| **GetCursorPos** | 0x100511a8 | 获取鼠标位置 |
| **ScreenToClient** | 0x10051154 | 屏幕坐标转换 |
| **ClientToScreen** | 0x10051160 | 客户端坐标转换 |
| **GetKeyState** | 0x1005114c | 按键状态 |
| **GetForegroundWindow** | 0x1005116c | 获取前台窗口 |
| **GetKeyNameTextA** | 0x10051144 | 按键名称 |
| **MapVirtualKeyA** | 0x10051148 | 虚拟键映射 |

### 9.2 KERNEL32导入函数

| 函数名 | IAT地址 | 用途 |
|--------|---------|------|
| CreateThread | 0x10051074 | 创建线程 |
| GlobalAlloc | 0x10051070 | 内存分配 |
| GlobalFree | 0x1005106c | 内存释放 |
| LoadLibraryA | 0x10051020 | 加载库 |
| GetProcAddress | 0x1005105c | 获取函数地址 |

---

## 十、关键函数详细分析

### 10.1 主循环函数

**函数**: `sub_10005360` @ 0x10005360 (大小: 0xEF)

**功能**:
1. 检查初始化标志 `byte_1005F73D`
2. 释放资源
3. 调用ImGui初始化 `sub_10033140`
4. 更新帧计数器

**关键代码**:
```cpp
if (byte_1005F73D) {
    // 释放资源
    ReleaseResources();
    // ImGui初始化
    sub_10033140();
    // 更新帧计数
    UpdateFrameCounter();
    byte_1005F73D = 0;
}
return RenderLoop();
```

### 10.2 配置初始化函数

**函数**: `sub_1004A040` @ 0x1004A040 (大小: 0x948)

**功能**:
1. 检查配置标志 `byte_1005F7C9`
2. 初始化所有配置默认值
3. 设置颜色表

**关键代码**:
```cpp
if (!byte_1005F7C9) {
    byte_1005F7C9 = 1;
    // 初始化配置
    result = dword_1005F76C;
    result[3639] = 1094713344;  // 50.0f
    result[3640] = 1094713344;  // 50.0f
    result[3652] = 1090519040;  // 8.0f
    // ... 更多配置
}
return result;
```

### 10.3 ImGui绘制函数

**函数**: `sub_1002AD70` @ 0x1002AD70 (大小: 0x17C)

**功能**:
1. 清空绘制数据
2. 释放资源
3. 调用绘制回调

**关键代码**:
```cpp
// 清空数据
sub_10005BB0();
sub_10005BB0(this + 3);
sub_10005BB0(this + 6);

// 释放资源
if (this[33]) {
    free(this[33]);
    this[33] = 0;
}

// 调用绘制回调
return loc_1002D770(this + 26);
```

---

## 十一、全局变量分析

### 11.1 关键全局变量

| 地址 | 名称 | 类型 | 说明 |
|------|------|------|------|
| 0x1005F6DC | dword_1005F6DC | int* | 全局上下文指针 |
| 0x1005F73D | byte_1005F73D | bool | 初始化标志 |
| 0x1005F754 | dword_1005F754 | int | DX/渲染指针 |
| 0x1005F75C | dword_1005F75C | int | ImGui上下文 |
| 0x1005F764 | dword_1005F764 | int | 纹理/资源指针 |
| 0x1005F76C | dword_1005F76C | int | **主上下文对象指针** |
| 0x1005F7C9 | byte_1005F7C9 | bool | 配置已初始化标志 |

### 11.2 主上下文对象布局

**基址**: `dword_1005F76C`

| 偏移(bytes) | 索引(int) | 类型 | 说明 |
|------------|-----------|------|------|
| +14556 | +3639 | float | ESP距离/大小 |
| +14560 | +3640 | float | ESP大小 |
| +14564 | +3641 | float | ESP参数 |
| +14568 | +3642 | float | ESP透明度 |
| +14608 | +3652 | float | 自瞄平滑系数1 |
| +14612 | +3653 | float | 自瞄平滑系数2 |
| +14624 | +3656 | float | 自瞄距离限制 |
| +14628 | +3657 | float | 自瞄平滑系数3 |
| +14656 | +3664 | float | FOV视野限制 |
| +14788 | +3697 | float | 颜色R |
| +14792 | +3698 | float | 颜色G |
| +14796 | +3699 | float | 颜色B |
| +14800 | +3700 | float | 颜色A |

---

## 十二、实现方法总结

### 12.1 核心技术

1. **IL2CPP反射**
   - 通过IL2CPP API获取Unity类和方法
   - 动态调用Unity函数

2. **内存操作**
   - 直接读写游戏内存
   - 修改玩家属性

3. **Hook技术**
   - Hook DirectX Present
   - 注入ImGui渲染

4. **坐标转换**
   - 世界坐标 → 屏幕坐标
   - 3D → 2D投影

### 12.2 实现流程

```
启动 → 配置加载 (sub_1004A040)
        ↓
    ImGui初始化 (sub_10033140)
        ↓
    进入主循环 (sub_10005360)
        ↓
    WHILE(运行) {
        ↓
        ImGui新帧 (sub_10033260)
            ↓
        热键检测 (GetAsyncKeyState)
            ↓
        自瞄更新 (0x1004ad3c区域)
            ↓
        ESP绘制 (sub_1002AD70)
            ↓
        ImGui渲染 (sub_10034080)
    }
```

---

## 十三、开发建议

### 13.1 逆向分析建议

1. **重点关注区域**:
   - 0x1004a988 ~ 0x1004bc5e (自瞄核心)
   - 0x1002AD70 (ESP绘制)
   - 0x1004A040 (配置初始化)

2. **关键字符串**:
   - GameManager
   - PlayerWeapons
   - esp_config.ini

3. **关键API**:
   - GetAsyncKeyState
   - Physics.Linecast
   - Camera.WorldToScreenPoint

### 13.2 修改建议

1. **添加新功能**:
   - 在0x1004bc5e后添加新函数
   - 使用现有的IL2CPP调用框架

2. **修改配置**:
   - 修改sub_1004A040中的默认值
   - 添加新的配置项

3. **优化性能**:
   - 减少每帧遍历次数
   - 使用对象池

---

## 十四、附录

### 14.1 关键RVA地址表

| 描述 | RVA地址 |
|------|---------|
| GetAsyncKeyState IAT | 0x10051188 |
| SetCursorPos IAT | 0x100511ac |
| sub_1002AD70 (ImGui Draw) | 0x1002AD70 |
| sub_10033140 (ImGui Init) | 0x10033140 |
| sub_10033260 (ImGui NewFrame) | 0x10033260 |
| sub_1004A040 (Config Init) | 0x1004A040 |
| GameManager 字符串 | 0x100538e4 |
| esp_config.ini 字符串 | 0x1005b280 |
| 主上下文对象指针 | 0x1005F76C |

### 14.2 GetAsyncKeyState调用点

| 地址 | 所在区域 | 用途 |
|------|---------|------|
| 0x10005778 | sub_10005360 | 主窗口消息循环 |
| 0x1004ad3c | 未识别区域 | Aimbot主循环 |
| 0x1004b435 | 未识别区域 | 辅助热键 |
| 0x1004b7a9 | 未识别区域 | 功能切换 |

---

**分析完成时间**: 2026-05-26  
**分析人员**: AI Assistant  
**工具版本**: IDA Pro 9.0 + MCP
