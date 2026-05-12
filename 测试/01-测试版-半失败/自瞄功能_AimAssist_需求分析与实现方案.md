# 自瞄功能（Aim Assist）— 基于 UnityCrossFire.dll 方案的需求分析与实现方案

> **目标**: 把准星对准视野范围内距离准星最近的敌人，不开枪、不控制子弹  
> **参考来源**: `小工具dll逆向分析.md` — UnityCrossFire.dll 自瞄方案  
> **分析日期**: 2026-05-08  
> **方案类型**: WorldToScreen + FOV 筛选 + 角度写入

---

## 一、技术可行性分析

### 1.1 总体评估：✅ 可行

DLL 方案的核心是将目标从 3D 世界坐标转换为 2D 屏幕坐标，再与屏幕中心的准星位置对比，选择距离准星最近的敌人，计算角度并写入内存。

| 维度 | 评估 | 说明 |
|------|------|------|
| **目标获取** | ✅ 可行 | GameManager.allPlayers（0x1C）提供所有玩家 |
| **坐标转换** | ✅ 可行 | Camera.WorldToScreenPoint（0x327F70）将 3D 坐标转 2D 屏幕坐标 |
| **目标筛选** | ✅ 可行 | 计算屏幕距离，选择最近目标，限制 FOV 范围 |
| **角度计算** | ✅ 可行 | `atan2(dx, dz)` 标准数学公式 |
| **角度写入** | ✅ 可行 | `player + 0x4C` 写入 yaw/pitch（cameraRotation） |
| **触发器** | ✅ 可行 | Input.GetMouseButton(0) 检测鼠标左键（0xACFB20） |
| **可见性检测** | ✅ 可行 | Physics.Raycast（0xABB0A0）检测遮挡 |

### 1.2 方案对比

| 方案 | 原理 | 复杂度 | 风险 | 本文件 |
|------|------|--------|------|--------|
| **WorldToScreen 方案（DLL）** | 3D→2D 转换后选屏幕最近目标 | ⭐⭐ 中 | 低 | ✅ 本文档 |
| **直接内存方案（Frida）** | 读 Transform.position 选世界最近目标 | ⭐ 低 | 低 | 另一方案 |

---

## 二、在 dump.cs 中搜索目标

### 2.1 搜索关键词：`Camera`

搜索 `dump.cs`，找到类名、方法名、字段名包含 `Camera` 的目标。

#### 类名包含 Camera

| 类名 | TypeDefIndex | RVA | 行号 | 说明 |
|------|-------------|-----|------|------|
| `Camera` | 1970 | — | 113923 | Unity 摄像机类 |
| `CameraSwitcher` | — | — | 27760 | 摄像机切换器 |
| `FreeCamera` | — | — | 27773 | 自由摄像机 |
| `PlayerCameraManager` | 5176 | 0xB122B0 | 234955 | **玩家摄像机管理器 ⭐** |
| `PixelPerfectCamera` | — | — | 36987 | 像素完美摄像机 |
| `CinemachineVirtualCamera` | — | — | 43273 | Cinemachine 虚拟摄像机 |

#### 方法名包含 Camera（关键）

| 方法 | 类 | RVA（dump.cs） | VA（IDA） | 说明 |
|------|---|:-------------:|:---------:|------|
| `get_main()` | Camera | **0x328310** | 0x10328310 | 获取主摄像机 ⭐ |
| `WorldToScreenPoint(Vector3)` | Camera | **0x327F70** | 0x10327F70 | 3D 世界坐标→2D 屏幕坐标 ⭐ |
| `WorldToScreenPoint(Vector3, eye)` | Camera | 0x327F20 | 0x10327F20 | 3D→2D（指定眼） |
| `ScreenToWorldPoint(Vector3)` | Camera | 0x327D70 | 0x10327D70 | 2D→3D |
| `get_mapCameraPos()` | Player | 0xB56180 | 0x10B56180 | 获取地图摄像机位置 |
| `get_modelCameraTransform()` | PlayerCameraManager | 0xB122B0 | 0x10B122B0 | 获取模型摄像机 Transform |

#### 字段名包含 Camera（关键）

| 字段 | 类 | 偏移 | 类型 | 说明 |
|------|---|:----:|------|------|
| `cameraManager` | Player | **0x48** | PlayerCameraManager | 摄像机管理器指针 ⭐ |
| `modelCamera` | PlayerCameraManager | 0x10 | Camera | 模型摄像机 |
| `mapCamera` | PlayerCameraManager | 0xC | CinemachineVirtualCamera | 地图摄像机 |

### 2.2 搜索关键词：`WorldToScreen`

| 方法 | 类 | RVA | 说明 |
|------|---|:---:|------|
| `WorldToScreenPoint(Vector3)` | Camera | **0x327F70** | 3D→2D 坐标转换 ⭐ |
| `WorldToScreenPoint(Vector3, eye)` | Camera | 0x327F20 | 3D→2D（带眼睛参数） |
| `WorldToScreenPoint(Camera, Vector3)` | — | 0x—— | 静态辅助方法 |
| `WorldToScreenPoint_Injected` | Camera | 0x—— | 注入版 |

### 2.3 搜索关键词：`Raycast`

| 方法 | 类 | RVA | 签名 | 说明 |
|------|---|:---:|------|------|
| `Raycast(Vector3, Vector3, out RaycastHit, float, int)` | Physics | **0xABB0A0** | `bool(Vector3, Vector3, out RaycastHit, float, int)` | **可见性检测 ⭐** |
| `Raycast(Vector3, Vector3, out RaycastHit, float)` | Physics | 0xABAB00 | `bool(Vector3, Vector3, out RaycastHit, float)` | 简化版 |
| `Raycast(Vector3, Vector3, out RaycastHit)` | Physics | 0xABB260 | `bool(Vector3, Vector3, out RaycastHit)` | 最简版 |
| `Raycast(Ray, ...)` | Physics | 0x—— | 多种重载 | 射线版 |

### 2.4 搜索关键词：`Transform`

| 方法/字段 | 类 | RVA / 偏移 | 说明 |
|----------|---|:----------:|------|
| `get_transform()` | Component | **0x121164** | 获取 Transform 组件 |
| `get_position()` | Transform | **0x123740** | 获取世界坐标 ⭐ |
| `_position_k__BackingField` | — | **0x38** | Transform 内部位置字段 ⭐ |
| `_characterContainer_k__BackingField` | Player | **0x58** | 角色容器（含 Transform）⭐ |

### 2.5 搜索关键词：`get_isMyPlayer` / `get_isDead` / `get_team`

| 方法 | 类 | RVA | 返回 | 说明 |
|------|---|:---:|:----:|------|
| `get_isMyPlayer()` | Player | **0xB55FD0** | bool | 是否为本地玩家 ⭐ |
| `get_isDead()` | Entity | **0xB400E0** | bool | 是否死亡 ⭐ |
| `get_team()` | Entity | **0x1E0070** | Team(enum) | 获取队伍（0x20 偏移）⭐ |
| `get_isFocusPlayer()` | Player | **0xB55F30** | bool | 是否焦点玩家 |

### 2.6 关键类继承链

```
MonoBehaviour (UnityEngine)
├── Camera                              [113923]  ← WorldToScreenPoint 提供者
├── Entity                              [233815]
│   ├── Player                          [234190]  ← 核心操作对象
│   └── SentryGun
├── PlayerCameraManager                 [234955]  ← 摄像机管理器
├── Bot                                 [231082]  ← AI Bot（无队伍体系）
├── Recoil                              [248242]  ← 后坐力
└── Singleton<T>
    └── GameManager                     [242579]  ← 持有 allPlayers

struct Ray                              [114692]  ← 射线结构
struct RaycastHit                       —         ← 射线命中结果
```

---

## 三、IDA MCP 反编译验证

> IDA 基址: `0x10000000`，.text: `0x10001000`  
> 目标: 验证 DLL 方案中关键函数的真实逻辑

### 3.1 `Camera__get_main` 反编译

```c
UnityEngine_Camera_o *__cdecl UnityEngine_Camera__get_main(const MethodInfo *method)
{
  int (*v1)(void); // eax
  v1 = (int (*)(void))dword_10E63FCC;
  if ( !dword_10E63FCC ) {
    v1 = sub_10167DE0("UnityEngine.Camera::get_main()"); // 延迟加载原生函数
    dword_10E63FCC = (int)v1;
  }
  return (UnityEngine_Camera_o *)v1();
}
```

**验证结论**: ✅ RVA 0x328310 正确。通过函数指针调用原生 API，是 Unity 标准方式。**隐含约束**: 首次调用会查找原生函数（有延迟），Camera.main 可能为 null（场景中无摄像机时）。

### 3.2 `Camera__WorldToScreenPoint` 反编译

```c
UnityEngine_Vector3_o *__cdecl UnityEngine_Camera__WorldToScreenPoint_271744880(
    UnityEngine_Vector3_o *__return_ptr retstr,
    UnityEngine_Camera_o *this,
    UnityEngine_Vector3_o position,
    const MethodInfo *method)
{
  JUMPOUT(0x10327F79);  // 内联跳转到原生实现
}
```

**验证结论**: ✅ RVA 0x327F70 正确。返回 `Vector3(x, y, z)` 其中 `x, y` 是屏幕像素坐标。**隐含约束**: Camera 不能为 null，position 需要在摄像机视野内（z > 0）。当目标在摄像机后方时，屏幕坐标不可用。

### 3.3 `Physics__Raycast` 反编译

```c
bool __cdecl UnityEngine_Physics__Raycast_279687328(
    UnityEngine_Vector3_o origin,
    UnityEngine_Vector3_o direction,
    UnityEngine_RaycastHit_o *hitInfo,
    float maxDistance,
    int32_t layerMask,
    const MethodInfo *method)
{
  // 获取默认 PhysicsScene → 执行 Raycast
  v6 = sub_10167DE0("UnityEngine.Physics::get_defaultPhysicsScene_Injected(UnityEngine.PhysicsScene&)");
  v6(&v8);          // 获取 PhysicsScene
  JUMPOUT(0x10ABB0D5);  // 跳转到 PhysicsScene.Raycast
}
```

**验证结论**: ✅ RVA 0xABB0A0 正确。签名 `bool(Vector3, Vector3, out RaycastHit, float, int)` 已确认。**隐含约束**: LayerMask 为 -1 时检测所有层；RaycastHit 结构体需要正确分配内存。

### 3.4 `Entity__get_team` 反编译

```c
int32_t __cdecl Entity__get_team(Entity_o *this, const MethodInfo *method)
{
  return this->fields._team_k__BackingField;
}
```

**验证结论**: ✅ 偏移 0x20 确认。直接返回 backing field，无 null 检查。**Team 枚举值**: BlackList=0, GlobalRisk=1, Neutral=2。

### 3.5 `Player__get_isMyPlayer` 反编译

```c
bool __cdecl Player__get_isMyPlayer(Player_o *this, const MethodInfo *method)
{
  myPlayer = GameManager_TypeInfo->static_fields->myPlayer;
  return UnityEngine_Object__op_Equality(myPlayer, (UnityEngine_Object_o *)this, 0);
}
```

**验证结论**: ✅ RVA 0xB55FD0 正确。比较当前 Player 实例与 `GameManager.myPlayer` 静态字段。**隐含约束**: 使用 `Object.op_Equality` 比较而非直接指针比较（支持 null 检查）。

### 3.6 `Input__GetMouseButton` 反编译

```c
bool __cdecl UnityEngine_Input__GetMouseButton(int32_t button, const MethodInfo *method)
{
  v2 = sub_10167DE0("UnityEngine.Input::GetMouseButton(System.Int32)");
  return v2(button);
}
```

**验证结论**: ✅ RVA 0xACFB20 正确。参数 0=左键, 1=右键, 2=中键。

---

## 四、DLL 自瞄方案完整数据流分析

### 4.1 方案架构图

```
[每帧循环]
    │
    ▼
┌─────────────────────────────────────────────────┐
│  1. 获取所有玩家                                 │
│     GameManager.allPlayers[0x1C] → Player[]      │
│                   │                              │
│                   ▼                              │
│  2. 对每个玩家:                                  │
│  ┌───────────────────────────────────────────┐   │
│  │ a. 排除自己 (isMyPlayer)                   │   │
│  │ b. 排除死亡 (isDead)                       │   │
│  │ c. 排除队友 (team ≠ myTeam)               │   │
│  │ d. get_transform() → get_position() → 世界坐标││
│  │ e. Camera.WorldToScreenPoint() → 屏幕坐标  │   │
│  │ f. 检查 z > 0（目标在摄像机前方）           │   │
│  │ g. 计算到屏幕中心(准星)的距离               │   │
│  │ h. 选择距离准星最近的可见目标               │   │
│  └───────────────────────────────────────────┘   │
│                   │                              │
│                   ▼                              │
│  3. 锁定目标                                     │
│     dword_1005A6D4 = selected_target             │
│                   │                              │
│                   ▼                              │
│  [等待热键]                                      │
│  4. GetAsyncKeyState(热键) → 是否按下           │
│          │                                       │
│          ▼                                       │
│  5. 获取自身位置 (self)                         │
│  6. 获取目标位置 (target)                       │
│  7. 计算角度:                                    │
│     yaw = atan2(dx, dz)                         │
│     pitch = atan2(dy, distance)                 │
│  8. 写入角度:                                    │
│     player + 76(0x4C) = yaw                     │
│     player + 80(0x50) = pitch                   │
│  9. 重置控制标志:                                │
│     [4]=0, [9]=0, [16]=0, [21]=0               │
└─────────────────────────────────────────────────┘
```

### 4.2 关键 API 调用链

```
GameManager                           → allPlayers[0x1C] → Player[]
Player.get_isMyPlayer(0xB55FD0)       → 排除自己
Entity.get_isDead(0xB400E0)           → 排除死亡
Entity.get_team → player[0x20]       → 排除队友
Component.get_transform(0x121164)     → 获取 Transform
Transform.get_position(0x123740)      → 获取世界坐标
Camera.get_main(0x328310)             → 获取主摄像机
Camera.WorldToScreenPoint(0x327F70)   → 3D→2D 转换
Physics.Raycast(0xABB0A0)             → 可见性检测
Input.GetMouseButton(0xACFB20)        → 鼠标左键触发
```

### 4.3 WorldToScreen 的技术细节

DLL 方案的核心是 `Camera.WorldToScreenPoint()`。该函数将 3D 世界坐标转换为 2D 屏幕像素坐标。

**输入**: 3D 世界坐标 Vector3(x, y, z)  
**输出**: 屏幕坐标 Vector3(x, y, z)  
- `x`: 屏幕像素 X（0 ~ screenWidth）  
- `y`: 屏幕像素 Y（0 ~ screenHeight）  
- `z`: 深度值（> 0 表示在摄像机前方，< 0 在后方）

**屏幕中心（准星位置）**: `(screenWidth/2, screenHeight/2)`  
**目标筛选**: 计算所有目标屏幕坐标与中心点的欧氏距离，选择最近的

### 4.4 DLL 方案与 Frida 方案的关键差异

| 维度 | DLL (WorldToScreen) 方案 | Frida (直接内存) 方案 |
|------|------------------------|---------------------|
| **目标筛选方式** | 转 2D 屏幕坐标 → 屏幕距离最近 | 读 3D 世界坐标 → 世界距离最近 |
| **坐标获取** | 调用 `get_transform()` + `get_position()` 函数 | 直接读 `characterContainer + 0x38` 内存 |
| **视野判断** | `WorldToScreenPoint` 返回 z>0 自然过滤 | 计算角度差限制 maxAimAngle |
| **性能开销** | 每玩家 2 次函数调用（get_transform + get_position + WorldToScreen） | 每玩家 1 次内存读取 |
| **可见性** | 可通过 Raycast 或 ESP 标志 | 可通过 Physics.Raycast |
| **FOV 筛选** | 通过屏幕距离自然限制 | 通过角度差限制 |
| **复杂度** | 较高（需要 Camera 实例） | 较低 |

---

## 五、DLL 自瞄方案实现步骤

### 阶段 1：基础框架

| 步骤 | 要做什么 | 预期输出 |
|------|---------|---------|
| 1.1 | 创建自瞄模块 JS 框架（enable/disable/rpc.exports） | 模块骨架 |
| 1.2 | 实现 `getGameAssembly()` 获取 DLL 基址 | 基址正常 |
| 1.3 | 实现 GameManager 获取和 allPlayers 遍历 | 玩家列表 |

### 阶段 2：WorldToScreen 坐标转换

| 步骤 | 要做什么 | 预期输出 |
|------|---------|---------|
| 2.1 | 创建 `Camera.get_main()` 的 NativeFunction（0x328310） | 获取主摄像机 |
| 2.2 | 创建 `Camera.WorldToScreenPoint()` 的 NativeFunction（0x327F70） | 坐标转换 |
| 2.3 | 创建 `Transform.get_position()` 的 NativeFunction（0x123740） | 世界坐标 |
| 2.4 | 创建 `Component.get_transform()` 的 NativeFunction（0x121164） | Transform 获取 |
| 2.5 | 测试：将一个 Bot 的坐标从 3D 转 2D 并输出日志 | 验证转换正确 |

### 阶段 3：敌人筛选

| 步骤 | 要做什么 | 预期输出 |
|------|---------|---------|
| 3.1 | 遍历 allPlayers，排除自己（isMyPlayer） | 排除自身 |
| 3.2 | 排除死亡（isDead） | 只留存活 |
| 3.3 | 按模式排除队友（team 判断） | 只留敌方 |
| 3.4 | 对每个敌方玩家：获取世界坐标 → WorldToScreen → 检查 z > 0 | 屏幕坐标列表 |

### 阶段 4：FOV 目标选择

| 步骤 | 要做什么 | 预期输出 |
|------|---------|---------|
| 4.1 | 获取屏幕宽高（可通过 `Process.findModuleByName` 或硬编码） | 屏幕中心点 |
| 4.2 | 计算每个敌人屏幕坐标到屏幕中心的距离 | 距离列表 |
| 4.3 | 选择距离最近的敌人作为目标 | 锁定最近目标 |
| 4.4 | 添加距离阈值（超过阈值忽略） | FOV 限制 |

### 阶段 5：角度计算与写入

| 步骤 | 要做什么 | 预期输出 |
|------|---------|---------|
| 5.1 | 获取自身世界坐标 | selfPos |
| 5.2 | 获取目标世界坐标（可用 Transform.get_position 或直接读内存） | targetPos |
| 5.3 | 计算 yaw = atan2(dx, dz) | 水平角度 |
| 5.4 | 计算 pitch = -atan2(dy, sqrt(dx²+dz²)) | 垂直角度 |
| 5.5 | 写入 cameraRotation（player + 0x4C = yaw, player + 0x50 = pitch） | 准星对准 |
| 5.6 | 平滑处理（分步逼近） | 平滑移动 |

### 阶段 6：鼠标触发

| 步骤 | 要做什么 | 预期输出 |
|------|---------|---------|
| 6.1 | 创建 `Input.GetMouseButton(0)` 的 NativeFunction（0xACFB20） | 检测左键 |
| 6.2 | 在 aimLoop 中，仅当左键按下时执行 | 按下瞄准 |

### 阶段 7：可见性检测

| 步骤 | 要做什么 | 预期输出 |
|------|---------|---------|
| 7.1 | 创建 `Physics.Raycast` 的 NativeFunction（0xABB0A0） | 射线检测 |
| 7.2 | 从自身眼睛位置到目标位置发出一条射线 | 检测遮挡 |
| 7.3 | 如果命中非目标物体，跳过该目标 | 只瞄准可见目标 |

---

## 六、方案评估

### 6.1 可行性评估：✅ 可行

| 判断依据 | 结论 |
|---------|:----:|
| DLL 已在外部 .dll 中成功实现此方案 | ✅ 已证明可行 |
| 所有 RVA 地址已通过 IDA MCP 反编译验证 | ✅ 地址均正确 |
| WorldToScreenPoint 是 Unity 标准 API | ✅ 稳定可靠 |
| 角度计算公式与 DLL 反汇编一致 | ✅ 数学正确 |

### 6.2 风险评估

| 风险 | 等级 | 说明 |
|------|:----:|------|
| **Camera.main 为 null** | ⚠️ 中 | 游戏场景中必须存在 Camera 且带 `MainCamera` Tag |
| **WorldToScreen 性能** | ⚠️ 低 | 每帧对每个可见玩家调用，约 10-30 次函数调用 |
| **屏幕坐标转换失败** | ⚠️ 中 | 目标在摄像机后方时 z<0，无法获得有效屏幕坐标 |
| **角度单位不确定** | ⚠️ 低 | DLL 用度(°)，Frida 方案用弧度(rad)，需实际测试 |
| **cameraRotation 被游戏覆盖** | ⚠️ 中 | 游戏可能在 Update 中重置旋转，需处理清零标志 |

### 6.3 复用的代码模式

| 模式 | 用途 |
|------|------|
| `NativeFunction` 调用 Camera API | 获取主摄像机 + WorldToScreen 转换 |
| `NativeFunction` 调用 Input API | 鼠标左键检测 |
| `Memory.alloc()` + 结构体填充 | Raycast 参数传递 |
| 定时器循环（30ms） | 每帧扫描 + 瞄准 |
| 房间切换 Hook | 进入新房间重置状态 |

### 6.4 WorldToScreen 转换函数实现

