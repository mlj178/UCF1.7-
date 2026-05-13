# Unity游戏反作弊开发技术文档
## 基于UnityCrossFire.dll分析

---

## 目录

1. [DLL基本信息](#1-dll基本信息)
2. [技术架构概述](#2-技术架构概述)
3. [核心功能实现原理](#3-核心功能实现原理)
   - 3.1 方框透视(ESP Box)
   - 3.2 骨骼透视(ESP Skeleton)
   - 3.3 自瞄功能(Aimbot)
4. [关键数据识别方法](#4-关键数据识别方法)
   - 4.1 识别电脑BOT
   - 4.2 识别阵营/队伍
   - 4.3 识别坐标位置
5. [准星移动实现](#5-准星移动实现)
6. [反作弊检测策略](#6-反作弊检测策略)
7. [防御建议](#7-防御建议)

---

## 1. DLL基本信息

| 属性 | 值 |
|------|-----|
| 文件名 | UnityCrossFire.dll |
| 文件大小 | 0x5AE00 (372,224 字节) |
| 基址 | 0x10000000 |
| MD5 | 0799202455e3ca7151157731be96a230 |
| 游戏引擎 | Unity (IL2CPP) |
| UI框架 | Dear ImGui 1.91.5 WIP |

---

## 2. 技术架构概述

### 2.1 IL2CPP反射机制

该DLL使用IL2CPP API进行游戏数据访问：

```c
// 关键IL2CPP函数
il2cpp_domain_get()                    // 获取IL2CPP域
il2cpp_domain_assembly_open()          // 打开程序集
il2cpp_class_from_name()               // 通过命名空间+类名获取类
il2cpp_class_get_methods()             // 获取类方法
il2cpp_class_get_fields()              // 获取类字段
il2cpp_object_new()                    // 创建对象实例
```

### 2.2 关键Unity API调用

从字符串分析可见使用的Unity API：

```csharp
// 对象查找
Object[] FindObjectsOfType(Type type);

// Transform相关
Transform get_transform();
Vector3 get_position();

// Camera相关
Camera get_main();

// Physics相关
Boolean Raycast(Vector3 origin, Vector3 direction, RaycastHit& hitInfo, Single maxDistance, Int32 layerMask);
Boolean Linecast(Vector3 start, Vector3 end, Int32 layerMask);

// GameObject相关
GameObject get_gameObject();
Int32 get_layer();
```

### 2.3 关键导入函数

| 模块 | 关键函数 | 用途 |
|------|----------|------|
| USER32 | `GetAsyncKeyState` | 检测按键状态(自瞄热键) |
| USER32 | `SetCursorPos` | 控制鼠标位置 |
| USER32 | `GetCursorPos` | 获取鼠标位置 |
| USER32 | `ScreenToClient` | 屏幕坐标转客户端坐标 |
| USER32 | `ClientToScreen` | 客户端坐标转屏幕坐标 |

---

## 3. 核心功能实现原理

### 3.1 方框透视(ESP Box)

#### 实现流程

```
┌─────────────────────────────────────────────────────────────┐
│                    ESP Box 实现流程                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 获取GameManager实例                                     │
│     └─> sub_10002850("GameManager")                         │
│                                                             │
│  2. 遍历玩家列表(最多30个)                                   │
│     └─> while(v43 < 30)                                     │
│                                                             │
│  3. 对每个玩家调用处理函数                                   │
│     └─> sub_100022D0(player, player_count, LODWORD(v2))     │
│        - 获取玩家Transform                                  │
│        - 获取玩家位置坐标                                   │
│                                                             │
│  4. WorldToScreen转换                                       │
│     └─> sub_10001330(camera, player_transform)              │
│        - 3D世界坐标 → 2D屏幕坐标                            │
│                                                             │
│  5. 检查可见性标志                                          │
│     └─> if(byte_1005A0D8 && BYTE1(v47[81]) && v47[1] > 0)   │
│        - byte_1005A0D8: ESP开关标志                         │
│        - BYTE1(v47[81]): 玩家是否可见                       │
│        - v47[1]: 玩家数量                                   │
│                                                             │
│  6. 绘制方框                                                │
│     └─> sub_1002AE30(x, y, color, width, height)            │
│        - 使用ImGui绘制                                    │
│        - 根据队伍不同设置不同颜色                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 关键代码分析 (sub_100052A0)

```c
// 获取GameManager
v1 = sub_10002850("GameManager");
if (v1) {
    v1 = v1[7];  // 获取玩家列表
    if (v1) {
        v46 = v1[4];  // 玩家数量
        if (v46 != 0.0) {
            dword_1005A76C = (int)v1;
            v42 = v1 + 5;  // 玩家数组起始
            v43 = 1;
            
            // 遍历最多30个玩家
            while (1) {
                v4 = *v3;  // 当前玩家对象
                if (!v4 || !*(_DWORD *)(v4 + 96))
                    break;
                
                // 处理玩家数据
                memset(v47, 0, sizeof(v47));
                sub_100022D0(v4, *(_DWORD *)(v4 + 96), LODWORD(v2));
                sub_10001330(LODWORD(v2), v4);  // WorldToScreen
                
                // 检查ESP开关和可见性
                if (byte_1005A0D8 && BYTE1(v47[81]) && v47[1] > 0) {
                    // 计算方框坐标
                    v35[0] = *(float *)&v47[86] - 0.49f;  // 左上X
                    v35[1] = *(float *)&v47[88] - 0.49f;  // 左上Y
                    v34[0] = *(float *)&v47[85] + 0.5f;   // 右下X
                    v34[1] = *(float *)&v47[87] + 0.5f;   // 右下Y
                    
                    // 绘制方框
                    sub_1002AE30(x, y, color, 1, 1065353216);
                }
            }
        }
    }
}
```

#### 内存布局推测

```c
struct PlayerData {
    // offset 0-95: 未知数据
    void* transform;        // +96: Transform对象
    // ...
    int team;               // +32: 队伍ID
    // ...
    float screenX;          // +85*4: 屏幕X坐标
    float screenY;          // +87*4: 屏幕Y坐标
    float screenWidth;      // +86*4: 屏幕宽度
    float screenHeight;     // +88*4: 屏幕高度
    byte isVisible;         // +81*4+1: 可见性标志
    int playerCount;        // +1*4: 玩家数量
};
```

---

### 3.2 骨骼透视(ESP Skeleton)

#### 实现流程

```
┌─────────────────────────────────────────────────────────────┐
│                  ESP Skeleton 实现流程                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 检查骨骼ESP开关                                         │
│     └─> if(byte_1005A0D9 && v47[1] > 0)                     │
│                                                             │
│  2. 获取骨骼节点坐标                                        │
│     └─> sub_10002550(bone_index, type, context)             │
│        - bone_index: 骨骼索引                               │
│          * 0: 头部                                          │
│          * 3: 颈部                                          │
│          * 7: 胸部                                          │
│          * 10: 骨盆                                         │
│          * 6: 左手/右手                                     │
│                                                             │
│  3. WorldToScreen转换每个骨骼点                             │
│     └─> 每个骨骼点从3D转2D                                  │
│                                                             │
│  4. 连接骨骼点绘制线条                                      │
│     └─> 使用ImGui绘制线段连接各个骨骼点                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 骨骼索引映射

```c
// 从代码分析可见的骨骼索引调用
sub_10002550(0, 3, v5);    // 骨骼0 (头部)
sub_10002550(3, 7, v12);   // 骨骼3 (颈部->胸部)
sub_10002550(10, 6, v13);  // 骨骼10 (骨盆->手)

// 典型Unity游戏骨骼层次
enum BoneIndex {
    HEAD = 0,        // 头部
    NECK = 3,        // 颈部
    CHEST = 7,       // 胸部
    PELVIS = 10,     // 骨盆
    LEFT_HAND = 6,   // 左手
    RIGHT_HAND = ?,  // 右手
    LEFT_FOOT = ?,   // 左脚
    RIGHT_FOOT = ?,  // 右脚
};
```

---

### 3.3 自瞄功能(Aimbot)

#### 实现流程

```
┌─────────────────────────────────────────────────────────────┐
│                    Aimbot 实现流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 检测自瞄热键                                            │
│     └─> GetAsyncKeyState(uCode)                             │
│        - 检查特定按键是否按下                               │
│        - 返回值 < 0 表示按键按下                            │
│                                                             │
│  2. 获取目标玩家信息                                        │
│     └─> if(dword_1005A6D4)  // 当前锁定目标                 │
│         if(dword_1005A6D8)  // 自瞄开关标志                 │
│                                                             │
│  3. 获取目标位置                                            │
│     └─> v1 = *(_DWORD **)(dword_1005A6D4 + 84)              │
│        - +84偏移处存储目标Transform                         │
│                                                             │
│  4. 计算角度                                                │
│     └─> dword_1005A6E8(&v44, dword_1005A6C8)                │
│        - 获取目标世界坐标                                   │
│                                                             │
│  5. 获取自身位置                                            │
│     └─> v23 = dword_1005A6E4()                              │
│        v24 = dword_1005A6DC(v23)                            │
│        dword_1005A6E8(&v50, v24)                            │
│                                                             │
│  6. 计算Yaw(水平角度)                                       │
│     └─> v46 = targetX - selfX                               │
│        v41 = targetZ - selfZ                                │
│        v44 = atan2(v46, v41)                                │
│        yaw = v44 * 180.0 / 3.1415925                        │
│                                                             │
│  7. 计算Pitch(垂直角度)                                     │
│     └─> distance = sqrt(v46^2 + v41^2)                      │
│        heightDiff = targetY - selfY                         │
│        v44 = atan2(heightDiff, distance)                    │
│        pitch = v44 * 180.0 / 3.1415925                      │
│                                                             │
│  8. 写入角度到游戏内存                                      │
│     └─> *(float *)(target + 76) = yaw                       │
│        *(float *)(target + 80) = pitch                      │
│        target[4] = 0    // 重置某些标志                     │
│        target[9] = 0                                        │
│        target[21] = 0                                       │
│        target[16] = 0                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 关键代码分析

```c
// 检测自瞄热键
LOWORD(v1) = GetAsyncKeyState(uCode);
if ((__int16)v1 < 0) {  // 按键按下
    v21 = dword_1005A6D4;  // 当前锁定目标
    if (dword_1005A6D4) {
        if (dword_1005A6D8) {  // 自瞄开关
            v1 = *(_DWORD **)(dword_1005A6D4 + 84);  // 获取目标Transform
            v43 = (int)v1;
            if (v1) {
                // 获取目标位置
                dword_1005A6E8(&v44, dword_1005A6C8);
                
                // 获取自身位置
                v22 = dword_1005A6DC;
                v23 = dword_1005A6E4();
                v24 = v22(v23);
                dword_1005A6E8(&v50, v24);
                
                // 计算差值
                v46 = *(float *)&v39 - *((float *)&v50 + 1);  // X差值
                v41 = v40 - *((float *)&v50 + 3);             // Z差值
                
                // 计算Yaw
                v44 = atan2(v46, v41);
                *(float *)&v42 = (float)(v44 * 180.0) / 3.1415925;
                
                // 计算Pitch
                v39 = *((float *)&v39 + 1) - *((float *)&v50 + 2);  // Y差值
                v26 = sqrt(v46*v46 + v41*v41);  // 水平距离
                v44 = atan2(v39, v26);
                
                // 写入角度
                *(float *)(v21 + 76) = *(float *)&v42;   // Yaw
                *(float *)(v21 + 80) = (float)(v44 * 180.0) / 3.1415925;  // Pitch
                
                // 重置标志
                v1[4] = 0;
                v1[9] = 0;
                v1[21] = 0;
                v1[16] = 0;
            }
        }
    }
}
```

#### 角度计算数学原理

```c
// Yaw (水平旋转角度)
// 使用atan2计算从自身到目标的水平角度
yaw = atan2(target.x - self.x, target.z - self.z) * 180 / PI

// Pitch (垂直俯仰角度)  
// 计算从自身到目标的垂直角度
horizontal_distance = sqrt((target.x - self.x)^2 + (target.z - self.z)^2)
pitch = atan2(target.y - self.y, horizontal_distance) * 180 / PI

// 坐标系统 (Unity左手坐标系)
// X: 左右方向
// Y: 上下方向  
// Z: 前后方向
```

---

## 4. 关键数据识别方法

### 4.1 识别电脑BOT

#### 检测方法

```c
struct PlayerInfo {
    // 方法1: 通过玩家数据结构中的BOT标志
    byte isBot;  // 某个偏移处的标志位
    
    // 方法2: 通过行为特征
    - 移动模式固定
    - 反应时间恒定
    - 名称包含特定前缀
    
    // 方法3: 通过游戏内部标志
    - GameManager中的玩家类型字段
    - 特定偏移处的值区分真人/BOT
};
```

#### 反作弊检测策略

```c
// 检测异常的玩家数据访问模式
bool DetectBotReading() {
    // 1. 监控对GameManager的访问
    // 2. 检测是否读取了BOT标识字段
    // 3. 分析访问频率是否异常
    
    if (access_pattern == "rapid_iteration") {
        // 正常玩家不会每帧遍历所有BOT
        return SUSPICIOUS;
    }
}
```

---

### 4.2 识别阵营/队伍

#### 内存布局分析

```c
// 从代码分析: v7 == 2 || v7 != *(_DWORD *)(v47[0] + 32)
// 推测队伍信息存储在 +32 偏移处

struct PlayerData {
    // ...
    int teamID;           // +32: 队伍标识
    // teamID == 1: 队伍1 (如保卫者)
    // teamID == 2: 队伍2 (如潜伏者)
    // teamID == 0: 观察者/BOT
    // ...
};
```

#### 队伍判断逻辑

```c
// 代码中的队伍判断
v7 = *(_DWORD *)(v47[2] + 32);  // 当前玩家队伍
if (v7 == 2 || v7 != *(_DWORD *)(v47[0] + 32)) {
    v8 = 1.0;  // 敌方, 高亮显示
} else {
    v8 = 0.0;  // 友方, 不显示或不同颜色
}

// 颜色设置
if (v8 >= 0.0) {
    // 敌方颜色 (红色系)
    color = (int)((fminf(1.0, v8) * 255.0) + 0.5) | 0xFF00FF00;
} else {
    // 友方颜色 (绿色系)
    color = -16711936;  // 0xFF00FF00
}
```

#### 反作弊检测策略

```c
// 检测队伍信息读取
bool DetectTeamInfoAbuse() {
    // 1. 监控对+32偏移的访问
    // 2. 检测是否只针对敌方玩家进行额外处理
    // 3. 分析是否利用队伍信息进行不公平渲染
}
```

---

### 4.3 识别坐标位置

#### 坐标获取流程

```
┌─────────────────────────────────────────────────────────────┐
│                  坐标获取流程                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 获取玩家Transform组件                                   │
│     └─> player_transform = player->get_transform()          │
│                                                             │
│  2. 获取世界坐标                                            │
│     └─> Vector3 position = transform->get_position()        │
│        或                                                   │
│     └─> transform->get_position_Injected(&ret)              │
│                                                             │
│  3. WorldToScreen转换                                       │
│     └─> Camera.main->WorldToScreenPoint(position)           │
│        或使用内部函数 sub_10001330()                        │
│                                                             │
│  4. 屏幕坐标处理                                            │
│     └─> screen_x = position.x / screen_width                │
│        screen_y = position.y / screen_height                │
│                                                             │
│  5. 坐标归一化                                              │
│     └─> 转换为0-1范围的归一化坐标                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 坐标数据结构

```c
// Unity Vector3 结构
struct Vector3 {
    float x;  // 左右
    float y;  // 上下
    float z;  // 前后
};

// 屏幕坐标转换
struct ScreenPoint {
    float x;  // 像素X
    float y;  // 像素Y
    float z;  // 深度值
};

// 从代码分析的坐标存储
struct PlayerScreenData {
    float screenX;      // v47[85]
    float screenY;      // v47[87]
    float screenWidth;  // v47[86]
    float screenHeight; // v47[88]
};
```

#### WorldToScreen实现原理

```c
// 简化的WorldToScreen算法
Vector3 WorldToScreen(Vector3 worldPos, Matrix4x4 viewProjMatrix, int screenWidth, int screenHeight) {
    // 1. 乘以视图投影矩阵
    Vector4 clipPos = viewProjMatrix * Vector4(worldPos, 1.0f);
    
    // 2. 透视除法
    Vector3 ndcPos = Vector3(clipPos.x, clipPos.y, clipPos.z) / clipPos.w;
    
    // 3. 转换到屏幕坐标
    ScreenPoint screen;
    screen.x = (ndcPos.x * 0.5f + 0.5f) * screenWidth;
    screen.y = (1.0f - (ndcPos.y * 0.5f + 0.5f)) * screenHeight;
    screen.z = ndcPos.z;
    
    return screen;
}
```

---

## 5. 准星移动实现

### 5.1 鼠标控制方法

```c
// 方法1: SetCursorPos (直接设置鼠标位置)
SetCursorPos(screen_x, screen_y);

// 方法2: 修改游戏视角角度 (代码中使用的方法)
// 直接写入Yaw/Pitch到游戏内存
*(float *)(playerController + 76) = targetYaw;
*(float *)(playerController + 80) = targetPitch;
```

### 5.2 自瞄完整流程

```
┌─────────────────────────────────────────────────────────────┐
│                    完整自瞄流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [输入] 热键检测                                             │
│     │                                                        │
│     ▼                                                        │
│  [选择] 目标选择逻辑                                         │
│     ├─> 遍历所有可见敌方玩家                                │
│     ├─> 计算距离准星的角度距离                              │
│     └─> 选择角度最近的玩家                                  │
│                                                             │
│  [计算] 角度计算                                             │
│     ├─> 获取自身位置 (World Position)                       │
│     ├─> 获取目标位置 (World Position)                       │
│     ├─> 计算Yaw = atan2(dx, dz) * 180/PI                    │
│     └─> 计算Pitch = atan2(dy, distance) * 180/PI            │
│                                                             │
│  [平滑] 角度平滑 (可选)                                      │
│     ├─> smoothYaw = currentYaw + (targetYaw - currentYaw) * factor │
│     └─> smoothPitch = currentPitch + (targetPitch - currentPitch) * factor │
│                                                             │
│  [输出] 写入角度                                             │
│     ├─> 写入PlayerController内存                            │
│     ├─> offset+76: Yaw                                     │
│     └─> offset+80: Pitch                                   │
│                                                             │
│  [重置] 清除标志                                             │
│     ├─> offset+4: 0                                        │
│     ├─> offset+9: 0                                        │
│     ├─> offset+16: 0                                       │
│     └─> offset+21: 0                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 代码实现

```c
// 自瞄核心代码
void Aimbot_Update() {
    // 1. 检查热键
    if (GetAsyncKeyState(AIM_KEY) < 0) {
        // 2. 检查是否有锁定目标
        if (lockedTarget && aimbotEnabled) {
            // 3. 获取目标Transform
            Transform* targetTransform = *(Transform**)(lockedTarget + 84);
            if (targetTransform) {
                // 4. 获取目标位置
                Vector3 targetPos = GetPosition(targetTransform);
                
                // 5. 获取自身位置
                Vector3 selfPos = GetSelfPosition();
                
                // 6. 计算差值
                float dx = targetPos.x - selfPos.x;
                float dy = targetPos.y - selfPos.y;
                float dz = targetPos.z - selfPos.z;
                
                // 7. 计算Yaw
                float yaw = atan2f(dx, dz) * 180.0f / 3.1415925f;
                
                // 8. 计算Pitch
                float horizontalDist = sqrtf(dx*dx + dz*dz);
                float pitch = atan2f(dy, horizontalDist) * 180.0f / 3.1415925f;
                
                // 9. 写入角度
                *(float*)(lockedTarget + 76) = yaw;
                *(float*)(lockedTarget + 80) = pitch;
                
                // 10. 重置标志
                *(int*)(lockedTarget + 16) = 0;
                *(int*)(lockedTarget + 36) = 0;
                *(int*)(lockedTarget + 64) = 0;
                *(int*)(lockedTarget + 84) = 0;
            }
        }
    }
}
```

---

## 6. 反作弊检测策略

### 6.1 内存访问监控

```c
// 检测异常的内存访问模式
class MemoryAccessMonitor {
    // 1. 监控对关键游戏对象的访问
    - GameManager访问频率
    - 玩家列表遍历速度
    - Transform组件读取模式
    
    // 2. 检测异常行为
    - 每帧遍历所有玩家(正常游戏不需要)
    - 只读取敌方玩家信息
    - 频繁的WorldToScreen调用
    
    // 3. 内存完整性检查
    - 关键数据校验和
    - 指针有效性验证
    - 内存页保护
};
```

### 6.2 行为分析检测

```c
// 检测作弊行为特征
class BehaviorAnalyzer {
    // 1. 视角变化检测
    - 检测视角突变(自瞄特征)
    - 分析视角移动平滑度
    - 检测超人类反应速度
    
    // 2. 瞄准模式分析
    - 统计爆头率异常
    - 分析瞄准时间分布
    - 检测预瞄行为
    
    // 3. 信息利用检测
    - 检测是否"知道"墙后敌人位置
    - 分析移动路径是否透视导向
    - 统计异常击杀(穿墙等)
};
```

### 6.3 代码完整性验证

```c
// 检测DLL注入和代码修改
class IntegrityChecker {
    // 1. 模块验证
    - 扫描已加载模块列表
    - 验证模块签名
    - 检测未知DLL
    
    // 2. 代码段校验
    - 计算关键函数哈希
    - 检测代码段修改
    - 验证导入表完整性
    
    // 3. 运行时检测
    - 检测调试器存在
    - 验证关键指针
    - 检查API钩子
};
```

### 6.4 具体检测点

```c
// 针对该DLL的检测点

// 1. 检测IL2CPP API滥用
bool DetectIL2CPPAbuse() {
    // 监控以下函数的调用频率
    - il2cpp_class_from_name("GameManager")
    - il2cpp_class_get_methods()
    - FindObjectsOfType()
    
    // 正常游戏不会频繁调用这些
}

// 2. 检测ImGui使用
bool DetectImGui() {
    // 扫描内存中的ImGui特征
    - "Dear ImGui" 字符串
    - ImGui窗口类
    - ImGui渲染循环
}

// 3. 检测异常按键监控
bool DetectKeyStateMonitoring() {
    // 监控GetAsyncKeyState调用
    // 检测是否监控非游戏相关按键
}

// 4. 检测视角写入
bool DetectAimbotWrite() {
    // 监控对PlayerController角度字段的写入
    // 检测非输入设备导致的视角变化
}
```

---

## 7. 防御建议

### 7.1 代码层面

```c
// 1. 加密关键数据
class EncryptedPlayerData {
    // 加密队伍、位置等敏感信息
    // 运行时解密,使用后立即清除
};

// 2. 添加数据校验
class ValidatedData {
    // 对关键数据添加校验和
    // 定期验证数据完整性
};

// 3. 混淆IL2CPP符号
// 使用IL2CPP代码混淆
// 重命名关键类和方法
```

### 7.2 架构层面

```c
// 1. 服务器验证
// 关键计算在服务器进行
// 客户端只负责渲染
// 验证客户端提交的角度合理性

// 2. 信息隐藏
// 只发送可见玩家信息
// 使用战争迷雾机制
// 延迟同步位置信息

// 3. 反调试
// 检测调试器存在
// 使用VM保护
// 添加时间检测反调试
```

### 7.3 运行时保护

```c
// 1. 内存保护
- 对关键数据页设置保护
- 使用API监控内存访问
- 检测异常读取模式

// 2. 行为监控
- 客户端收集行为数据
- 服务器分析异常模式
- 机器学习检测作弊

// 3. 定期扫描
- 扫描进程模块
- 验证文件完整性
- 检测已知作弊特征
```

---

## 附录

### A. 关键内存偏移总结

| 偏移 | 类型 | 说明 |
|------|------|------|
| +32 | int | 队伍ID |
| +76 | float | Yaw角度 |
| +80 | float | Pitch角度 |
| +84 | Transform* | Transform指针 |
| +96 | 未知 | 玩家数据标志 |

### B. 关键全局变量

| 变量 | 地址 | 说明 |
|------|------|------|
| byte_1005A0D8 | 0x1005A0D8 | ESP开关 |
| byte_1005A0D9 | 0x1005A0D9 | 骨骼ESP开关 |
| dword_1005A6D4 | 0x1005A6D4 | 当前锁定目标 |
| dword_1005A6D8 | 0x1005A6D8 | 自瞄开关 |

### C. 关键函数地址

| 函数 | 地址 | 功能 |
|------|------|------|
| sub_10002850 | 0x10002850 | 获取GameManager |
| sub_100022D0 | 0x100022D0 | 处理玩家数据 |
| sub_10001330 | 0x10001330 | WorldToScreen |
| sub_10002550 | 0x10002550 | 获取骨骼坐标 |
| sub_100052A0 | 0x100052A0 | ESP/Aimbot主循环 |
| sub_1002AE30 | 0x1002AE30 | ImGui绘制 |

---

## 免责声明

本文档仅用于**反作弊开发学习**和**游戏安全研究**目的。

- 不得用于开发或使用游戏作弊软件
- 不得用于破坏游戏公平性
- 遵守相关法律法规和游戏服务条款
- 游戏安全研究应在合法授权范围内进行

---

*文档生成时间: 2026-05-04*
*分析目标: UnityCrossFire.dll (MD5: 0799202455e3ca7151157731be96a230)*
