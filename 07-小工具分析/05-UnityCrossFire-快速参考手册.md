# UnityCrossFire.dll 快速参考手册

**版本**: 1.0  
**日期**: 2026-05-26  
**DLL**: UnityCrossFire.dll (MD5: 2be82d9a5c9820a3ecc224b6b89e99b7)

---

## 一、关键地址速查表

### 1.1 函数地址

| 功能 | 地址 | 大小 | 说明 |
|------|------|------|------|
| 主循环 | 0x10005360 | 0xEF | 主消息循环 |
| 窗口过程 | 0x10005450 | 0x40 | WndProc |
| ImGui初始化 | 0x10033140 | 0x11C | ImGui上下文初始化 |
| ImGui新帧 | 0x10033260 | 0x1BC | 开始新帧 |
| ImGui渲染 | 0x10034080 | 0x2F3 | 渲染结束 |
| ImGui绘制 | 0x1002AD70 | 0x17C | ESP+菜单绘制 |
| 配置初始化 | 0x1004A040 | 0x948 | 加载配置+设置默认值 |
| 解析工具 | 0x100228B0 | 0x1A0 | 数据解析 |
| 处理函数 | 0x10022CC0 | 0xBA | 通用处理 |
| 比较函数 | 0x10022D80 | 0x133 | 字符串比较 |

### 1.2 IAT地址 (导入函数)

| 函数 | IAT地址 | 模块 | 用途 |
|------|---------|------|------|
| **GetAsyncKeyState** | 0x10051188 | USER32 | **热键检测** |
| **SetCursorPos** | 0x100511ac | USER32 | 鼠标控制 |
| **GetCursorPos** | 0x100511a8 | USER32 | 获取鼠标位置 |
| **ScreenToClient** | 0x10051154 | USER32 | 坐标转换 |
| **ClientToScreen** | 0x10051160 | USER32 | 坐标转换 |
| GetKeyState | 0x1005114c | USER32 | 按键状态 |
| GetForegroundWindow | 0x1005116c | USER32 | 前台窗口 |
| CreateThread | 0x10051074 | KERNEL32 | 创建线程 |
| GlobalAlloc | 0x10051070 | KERNEL32 | 内存分配 |
| GlobalFree | 0x1005106c | KERNEL32 | 内存释放 |
| LoadLibraryA | 0x10051020 | KERNEL32 | 加载DLL |
| GetProcAddress | 0x1005105c | KERNEL32 | 获取函数 |

### 1.3 全局变量地址

| 变量 | 地址 | 类型 | 说明 |
|------|------|------|------|
| dword_1005F6DC | 0x1005F6DC | int* | 全局上下文 |
| byte_1005F73D | 0x1005F73D | bool | 初始化标志 |
| dword_1005F754 | 0x1005F754 | int | DX渲染指针 |
| dword_1005F75C | 0x1005F75C | int | ImGui上下文 |
| dword_1005F764 | 0x1005F764 | int | 纹理资源 |
| **dword_1005F76C** | **0x1005F76C** | **int** | **主配置对象** |
| byte_1005F7C9 | 0x1005F7C9 | bool | 配置已初始化 |

### 1.4 字符串地址

| 字符串 | 地址 | 用途 |
|--------|------|------|
| "GameManager" | 0x100538e4 | 游戏管理器类名 |
| "PlayerWeapons" | 0x10054a08 | 武器管理类名 |
| "Camera" | 0x100546d8 | 摄像机类名 |
| "esp_config.ini" | 0x1005b280 | 配置文件名 |
| "imgui.ini" | 0x10054a9c | ImGui配置 |
| "imgui_log.txt" | 0x10054aa8 | ImGui日志 |
| "Dear ImGui 1.91.5 WIP (19141)" | 0x10054b4c | ImGui版本 |
| "BoxESP=" | 0x1005b290 | 方框ESP配置项 |
| "BoneESP=" | 0x1005b298 | 骨骼ESP配置项 |
| "AimKey=" | 0x1005b308 | 自瞄热键配置项 |
| "WeaponID=" | 0x1005b310 | 武器ID配置项 |
| "InfiniteAmmo=" | 0x1005b2d8 | 无限弹药配置项 |

---

## 二、Unity API字符串速查表

### 2.1 Transform相关

| API签名 | 地址 | 用途 |
|---------|------|------|
| `Transform get_transform()` | 0x1005464c | 获取Transform |
| `Vector3 get_position()` | 0x10054674 | 获取位置 |
| `Void get_position_Injected(Vector3& ret)` | 0x10054698 | 获取位置(注入) |
| `GameObject get_gameObject()` | 0x10054798 | 获取GameObject |
| `Int32 get_layer()` | 0x100547e8 | 获取层 |
| `Collider get_collider()` | 0x10054770 | 获取碰撞体 |

### 2.2 Camera相关

| API签名 | 地址 | 用途 |
|---------|------|------|
| `Camera get_main()` | 0x100546c4 | 获取主摄像机 |

### 2.3 Physics相关

| API签名 | 地址 | 用途 |
|---------|------|------|
| `Boolean Linecast(Vector3 start, Vector3 end, Int32 layerMask)` | 0x100547fc | 射线检测 |

### 2.4 Object相关

| API签名 | 地址 | 用途 |
|---------|------|------|
| `Object[] FindObjectsOfType(Type type)` | 0x10054534 | 查找对象 |

### 2.5 Weapon相关

| API签名 | 地址 | 用途 |
|---------|------|------|
| `Weapon GiveWeapon(Player, Int32, Boolean, Boolean)` | 0x10054918 | 给予武器 |
| `Weapon GiveWeaponByBag(Player, Int32)` | 0x10054974 | 从背包给予 |
| `Weapon GetWeapon(Int32)` | 0x100549b0 | 获取武器 |
| `Void SetCurrentWeapon(Int32, Weapon)` | 0x100549d8 | 设置当前武器 |

---

## 三、IL2CPP反射API速查表

| API名称 | 地址 | 用途 |
|---------|------|------|
| `il2cpp_class_get_method_from_name` | 0x10053bc0 | 获取方法 |
| `il2cpp_class_get_field_from_name` | 0x10053b80 | 获取字段 |
| `il2cpp_class_get_name` | 0x10053be4 | 获取类名 |
| `il2cpp_class_get_namespace` | 0x10053c1c | 获取命名空间 |
| `il2cpp_class_get_methods` | 0x10053ba4 | 获取方法列表 |
| `il2cpp_class_get_fields` | 0x10053aec | 获取字段列表 |
| `il2cpp_class_get_parent` | 0x10053c38 | 获取父类 |
| `il2cpp_method_get_name` | 0x10054080 | 获取方法名 |
| `il2cpp_field_get_name` | 0x10053ef8 | 获取字段名 |
| `il2cpp_field_get_offset` | 0x10053f28 | 获取字段偏移 |

---

## 四、数据结构偏移速查表

### 4.1 PlayerController结构

| 字段 | 偏移 | 类型 | 说明 |
|------|------|------|------|
| teamID | +0x20 (32) | int | 队伍ID |
| cameraYaw | +0x4C (76) | float | 相机水平旋转 |
| cameraPitch | +0x50 (80) | float | 相机垂直旋转 |
| transform | +0x54 (84) | Transform* | Transform组件 |
| characterController | +0x58 (88) | CC* | 角色控制器 |

### 4.2 GameManager结构

| 字段 | 偏移 | 类型 | 说明 |
|------|------|------|------|
| playersBL | +0x20 (32) | PlayerList* | 蓝队玩家列表 |
| playersGR | +0x28 (40) | PlayerList* | 红队玩家列表 |

### 4.3 配置对象 (dword_1005F76C)

| 参数 | 偏移(bytes) | 索引(int) | 默认值 | 说明 |
|------|------------|-----------|--------|------|
| ESP距离 | +14556 | +3639 | 50.0f | ESP大小/距离 |
| ESP大小 | +14560 | +3640 | 50.0f | ESP大小 |
| ESP透明度 | +14568 | +3642 | 1.0f | ESP透明度 |
| 平滑系数1 | +14608 | +3652 | 8.0f | 自瞄平滑 |
| 平滑系数2 | +14612 | +3653 | 5.5f | 自瞄平滑 |
| 自瞄距离 | +14624 | +3656 | 12.0f | 自瞄距离限制 |
| 平滑系数3 | +14628 | +3657 | 8.0f | 自瞄平滑 |
| FOV限制 | +14656 | +3664 | 35.0f | FOV视野限制 |
| 颜色R | +14788 | +3697 | 0.7843f | 队伍1颜色R |
| 颜色G | +14792 | +3698 | 0.7961f | 队伍1颜色G |
| 颜色B | +14796 | +3699 | 0.8157f | 队伍1颜色B |
| 颜色A | +14800 | +3700 | 1.0f | 队伍1颜色A |

### 4.4 骨骼索引

| 骨骼 | 索引 | 说明 |
|------|------|------|
| HEAD | 0 | 头部 |
| NECK | 3 | 颈部 |
| LEFT_HAND | 6 | 左手 |
| CHEST | 7 | 胸部 (自瞄默认) |
| PELVIS | 10 | 骨盆 |

---

## 五、GetAsyncKeyState调用点

| 地址 | 区域 | 用途 |
|------|------|------|
| 0x10005778 | sub_10005360 | 主窗口消息循环 |
| 0x1004ad3c | 未识别区域 | **Aimbot主循环** |
| 0x1004b435 | 未识别区域 | 辅助热键 |
| 0x1004b7a9 | 未识别区域 | 功能切换 |

**未识别函数区域**: `0x1004a988 ~ 0x1004bc5e` (自瞄核心代码)

---

## 六、功能模块速查

### 6.1 自瞄功能

**实现位置**: 0x1004a988 ~ 0x1004bc5e

**实现步骤**:
1. 热键检测 (GetAsyncKeyState @ 0x1004ad3c)
2. 获取GameManager (字符串 @ 0x100538e4)
3. 获取本地玩家
4. 遍历敌人列表
5. 可见性检测 (Linecast @ 0x100547fc)
6. 获取骨骼位置 (CHEST = 7)
7. 计算瞄准角度
8. 角度平滑处理
9. 写入角度 (Player +0x4C, +0x50)
10. 重置标志

**配置参数**:
- FOV: 35.0f (offset +3664)
- 距离: 12.0f (offset +3656)
- 平滑: 8.0f / 5.5f (offset +3652 / +3653)

### 6.2 ESP功能

**实现函数**: sub_1002AD70 @ 0x1002AD70

**ESP类型**:
- BoxESP (方框ESP) - 配置项 @ 0x1005b290
- BoneESP (骨骼ESP) - 配置项 @ 0x1005b298

**实现步骤**:
1. 获取主摄像机 (Camera.get_main @ 0x100546c4)
2. 遍历所有玩家 (FindObjectsOfType @ 0x10054534)
3. 世界坐标转屏幕坐标
4. 计算ESP尺寸
5. ImGui绘制

### 6.3 武器修改

**关键API**:
- GiveWeapon @ 0x10054918
- GiveWeaponByBag @ 0x10054974
- GetWeapon @ 0x100549b0
- SetCurrentWeapon @ 0x100549d8

**配置项**:
- WeaponID @ 0x1005b310
- InfiniteAmmo @ 0x1005b2d8

### 6.4 ImGui界面

**关键函数**:
- 初始化: sub_10033140 @ 0x10033140
- 新帧: sub_10033260 @ 0x10033260
- 渲染: sub_10034080 @ 0x10034080
- 绘制: sub_1002AD70 @ 0x1002AD70

**配置文件**:
- imgui.ini @ 0x10054a9c
- imgui_log.txt @ 0x10054aa8

---

## 七、配置文件格式

**文件**: esp_config.ini

```ini
[Aimbot]
Enable=1
FOV=35.0
Distance=12.0
Smooth=8.0
TargetBone=7

[ESP]
BoxESP=1
BoneESP=1
Transparency=1.0

[Weapon]
InfiniteAmmo=0
WeaponID=0

[Colors]
Team1R=0.7843
Team1G=0.7961
Team1B=0.8157
Team1A=1.0
```

---

## 八、开发调试速查

### 8.1 断点设置建议

| 地址 | 条件 | 说明 |
|------|------|------|
| 0x1004ad3c | GetAsyncKeyState调用 | 自瞄激活检测 |
| 0x10051188 | IAT读取 | 热键状态获取 |
| 0x1004A040 | 函数入口 | 配置初始化 |
| 0x1002AD70 | 函数入口 | ESP绘制 |

### 8.2 内存监控建议

| 地址 | 大小 | 说明 |
|------|------|------|
| 0x1005F76C | 4 | 主配置对象指针 |
| 0x1005F73D | 1 | 初始化标志 |
| 0x1005F7C9 | 1 | 配置初始化标志 |

### 8.3 日志输出建议

```cpp
// 关键日志点
printf("[Aimbot] Hotkey detected at 0x%08X\n", 0x1004ad3c);
printf("[ESP] Drawing at 0x%08X\n", 0x1002AD70);
printf("[Config] Loading from 0x%08X\n", 0x1004A040);
```

---

## 九、常见问题速查

### 9.1 地址偏移问题

**问题**: 不同版本DLL地址不同  
**解决**: 使用RVA (相对虚拟地址) = 地址 - 基址

**示例**:
- 基址: 0x10000000
- 函数地址: 0x1004A040
- RVA: 0x4A040

### 9.2 字符串编码问题

**问题**: Unicode字符串处理  
**解决**: 使用MultiByteToWideChar / WideCharToMultiByte

### 9.3 IL2CPP版本问题

**问题**: 不同Unity版本IL2CPP API不同  
**解决**: 动态检测Unity版本，选择对应API

---

## 十、性能优化速查

### 10.1 自瞄优化

- 使用空间分割加速目标搜索
- 缓存玩家列表避免重复查找
- 异步处理目标搜索
- LOD系统降低远距离更新频率

### 10.2 ESP优化

- 视锥剔除只绘制屏幕内对象
- 距离剔除跳过远距离对象
- 批处理合并绘制调用
- 异步更新分离计算和渲染

### 10.3 内存优化

- 对象池重用临时对象
- 智能缓存IL2CPP方法指针
- 延迟加载按需加载资源

---

**文档结束**

**使用建议**:
1. 优先使用RVA地址而非绝对地址
2. 根据实际游戏版本调整偏移
3. 使用调试器验证关键地址
4. 定期更新配置文件
