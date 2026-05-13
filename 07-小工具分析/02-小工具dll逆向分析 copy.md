# UnityCrossFire.dll 逆向完整分析 — 自瞄全流程
## IDA Pro 实时提取数据

---

## 1. DLL 基本信息（IDA 实时获取）

| 属性 | 值 |
|------|-----|
| 文件路径 | `D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1\UnityCrossFire.dll` |
| 基址 | `0x10000000` |
| 模块大小 | `0x64000` (IDB中) / `0x5FC00` (文件) |
| MD5 | `2be82d9a5c9820a3ecc224b6b89e99b7` |
| SHA256 | `3b5726a8ca661796c9b2904d5539d46aa0a26c24f309bf9349110251b6e50e92` |
| CRC32 | `0x8d846bf3` |
| UI框架 | Dear ImGui 1.91.5 WIP（字符串 `"Dear ImGui 1.91.5 WIP (19141)"` @ 0x10054b4c） |

---

## 2. 导入表（IDA 实时提取）

### USER32 — 与自瞄直接相关

| 导入函数 | 用途 | IAT 地址 |
|---------|------|---------|
| `GetAsyncKeyState` | **自瞄热键检测** | 0x10051188 |
| `SetCursorPos` | 控制鼠标位置 | 0x100511ac |
| `GetCursorPos` | 获取鼠标位置 | 0x100511a8 |
| `ScreenToClient` | 屏幕坐标→客户端坐标 | 0x10051154 |
| `ClientToScreen` | 客户端坐标→屏幕坐标 | 0x10051160 |
| `GetKeyState` | 按键状态（备用） | 0x1005114c |
| `GetForegroundWindow` | 获取前台窗口 | 0x1005116c |

### 关键说明

- `GetAsyncKeyState` 调用点（IDA xrefs）：`0x10005778`, `0x1004ad3c`, `0x1004b435`, `0x1004b7a9`
- `SetCursorPos` 调用点：自瞄写角度失败时会降级为鼠标控制
- 无 `GetKeyNameTextA` `MapVirtualKeyA` 等辅助按键映射函数

---

## 3. 关键 Unity API 字符串（IDA 字符串表）

| 地址 | 字符串 | 用途 |
|------|--------|------|
| 0x100538e4 | `"GameManager"` | 游戏管理器类名 |
| 0x1005464c | `"Transform get_transform();"` | 获取Transform组件 |
| 0x10054674 | `"Vector3 get_position();"` | 获取世界坐标 |
| 0x10054698 | `"Void get_position_Injected(Vector3& ret);"` | get_position注入版 |
| 0x100546c4 | `"Camera get_main();"` | 获取主摄像机 |
| 0x100546d8 | `"Camera"` | 摄像机类名 |
| 0x100547fc | `"Boolean Linecast(Vector3 start,Vector3 end,Int32 layerMask);"` | **可见性检测** |
| 0x10054534 | `"Object[] FindObjectsOfType(Type type);"` | 对象查找 |
| 0x10054918 | `"Weapon GiveWeapon(Player player,Int32 weaponIndex,Boolean autoGiveUp,Boolean autoSelect);"` | 武器系统 |
| 0x10054974 | `"Weapon GiveWeaponByBag(Player player,Int32 weaponIndex);"` | 武器系统 |

### 其他关键字符串

| 地址 | 字符串 |
|------|--------|
| 0x1005b280 | `"esp_config.ini"` |
| 0x1005b290 | `"BoxESP="` |
| 0x1005b298 | `"BoneESP="` |
| 0x10053c1c | `"il2cpp_class_get_namespace"` |
| 0x10054a9c | `"imgui.ini"` |
| 0x10054b4c | `"Dear ImGui 1.91.5 WIP (19141)"` |

---

## 4. 关键函数列表（IDA 函数表）

| 地址 | 名称 | 大小 | 推测用途 |
|------|------|------|---------|
| 0x10005360 | `sub_10005360` | 0xEF | **主循环/窗口过程**（含 GetAsyncKeyState @ 0x10005778） |
| 0x10005450 | `sub_10005450` | 0x40 | **窗口消息处理** WndProc |
| 0x100228B0 | `sub_100228B0` | 0x1A0 | 解码/解析工具函数 |
| 0x10022CC0 | `sub_10022CC0` | 0xBA | 处理函数 |
| 0x10022D80 | `sub_10022D80` | 0x133 | 比较/解析函数（含"1","true","type"等字符串比较） |
| 0x1002AD70 | `sub_1002AD70` | 0x17C | **ImGui 绘制函数**（原 MD sub_1002AE30） |
| 0x10033140 | `sub_10033140` | 0x11C | ImGui 初始化 |
| 0x10033260 | `sub_10033260` | 0x1BC | ImGui 新帧 |
| 0x10034080 | `sub_10034080` | 0x2F3 | ImGui 渲染结束 |
| 0x1004A040 | `sub_1004A040` | 0x948 | **初始化/配置加载**（颜色/配置常量初始化，含 esp_config.ini 读取） |
| 0x1004BC5F | `sub_1004BC5F` | 0x60 | C++ 流析构（std::ostream） |

### 未识别函数区域（IDA 未能自动识别，但包含自瞄核心代码）

| 地址范围 | 包含 | 说明 |
|---------|------|------|
| `0x10048b8c ~ 0x1004a040` | esp_config.ini 引用 @ 0x10048e89/0x10048e9f | **ESP配置读取 + 自瞄主循环初始化** |
| `0x1004a988 ~ 0x1004bc5e` | GetAsyncKeyState @ 0x1004ad3c/0x1004b435/0x1004b7a9 | **Aimbot 主循环 + 目标选择 + 角度写入** |

> 注：此 DLL 版本（MD5: 2be82d9a5c9820a3ecc224b6b89e99b7）与原始 MD 文档的版本（MD5: 0799202455e3ca7151157731be96a230）函数地址不同。原始 MD 的函数偏移在此版本中不直接对应。

---

## 5. 全局变量（IDA 分析）

| 地址 | 名称 | 推测类型 | 说明 |
|------|------|---------|------|
| 0x1005F6DC | `dword_1005F6DC` | int* | 全局上下文指针 |
| 0x1005F73D | `byte_1005F73D` | bool | 初始化标志 |
| 0x1005F754 | `dword_1005F754` | int | DX/渲染指针 |
| 0x1005F75C | `dword_1005F75C` | int | ImGui 上下文 |
| 0x1005F764 | `dword_1005F764` | int | 纹理/资源指针 |
| 0x1005F76C | `dword_1005F76C` | int | **主上下文对象指针**（含所有配置） |
| 0x1005F7C9 | `byte_1005F7C9` | bool | 配置已初始化标志 |

### `dword_1005F76C` 对象内偏移（从 sub_1004A040 分析）

从初始化函数分析出的关键偏移（`result = dword_1005F76C`）：

| 字段偏移 (bytes) | 索引 (int) | 初始化值 | 推测用途 |
|-----------------|-----------|---------|---------|
| +14556 | +3639 | 1094713344 (50.0f) | ESP 方框大小/距离 |
| +14560 | +3640 | 1094713344 (50.0f) | ESP 方框大小 |
| +14608 | +3652 | 1090519040 (8.0f) | 自瞄平滑/参数 |
| +14612 | +3653 | 1086324736 (5.5f) | 自瞄参数 |
| +14624 | +3656 | 1092616192 (12.0f) | 自瞄距离限制 |
| +14628 | +3657 | 1090519040 (8.0f) | 自瞄参数 |
| +14656 | +3664 | 1101004800 (35.0f) | FOV/视野限制 |
| +14660 | +3665 | (未初始化) | |
| +14568 | +3642 | 1065353216 (1.0f) | ESP 透明度 |
| +14640 | +3660 | (未初始化) | |
| +14788 | +3697 | 1064514355 (0.7843f) | RGB 颜色 R |
| +14792 | +3698 | 1064682127 (0.7961f) | RGB 颜色 G |
| +14796 | +3699 | 1065017672 (0.8157f) | RGB 颜色 B |
| +14800 | +3700 | 1065353216 (1.0f) | RGB 颜色 A |

---

## 6. 自瞄全流程（从IDA + 反汇编综合分析）

### 6.1 架构概览

```
启动 → sub_1004A040 (配置初始化)
        ↓
    设置 ImGui → sub_10033140
        ↓
    进入消息循环 → sub_10005360
        ↓
    WHILE(运行中) {
        ↓
        sub_10033260 (ImGui 新帧开始)
            ↓
        sub_1002AD70 (ImGui 绘制 — 菜单 + ESP + 自瞄状态)
            ↓
        ~~~ 自瞄主循环 (0x1004ad3c 附近) ~~~
            ↓
        sub_10034080 (ImGui 渲染结束 + Present)
    }
```

### 6.2 自瞄主循环伪代码（基于 GetAsyncKeyState 引用分析）

```c
// 代码位于 0x1004ad3c 附近 (未识别函数区域)
void Aimbot_Update() {
    // ━━━ Step 1: 热键检测 ━━━
    // 调用 GetAsyncKeyState @ 0x10051188
    if ((GetAsyncKeyState(aimHotkey) & 0x8000) == 0)
        return;  // 热键未按下
    
    // ━━━ Step 2: 获取 GameManager ━━━
    // "GameManager" @ 0x100538e4
    GameManager* gm = GetGameManager();
    if (!gm) return;
    
    // ━━━ Step 3: 获取本地玩家 ━━━
    Player* localPlayer = gm->getLocalPlayer();
    if (!localPlayer || localPlayer->isDead()) return;
    
    // ━━━ Step 4: 遍历敌人 ━━━
    // 从 GM->playersBL (0x20) + GM->playersGR (0x28) 获取玩家列表
    for (int i = 0; i < playerCount; i++) {
        Player* target = playerList[i];
        if (!target || target == localPlayer) continue;
        if (target->team == localPlayer->team) continue;  // 跳过友军
        if (target->isDead()) continue;
        
        // ━━━ Step 5: 可见性检测 ━━━
        // Physics.Linecast @ 0x100547fc
        if (!IsVisible(localPlayer, target)) continue;
        
        // ━━━ Step 6: 获取骨骼位置 ━━━
        // Animator.GetBoneTransform(boneIndex)
        Vector3 targetPos = GetBonePosition(target, CHEST);    // CHEST=7
        Vector3 selfPos  = GetPosition(localPlayer);
        
        // ━━━ Step 7: 计算角度 ━━━
        float dx = targetPos.x - selfPos.x;
        float dy = targetPos.y - selfPos.y;
        float dz = targetPos.z - selfPos.z;
        float hDist = sqrt(dx*dx + dz*dz);
        
        float targetYaw   = atan2(dx, dz) * 180.0f / 3.1415925f;
        float targetPitch = atan2(dy, hDist) * 180.0f / 3.1415925f;
        
        // ━━━ Step 8: 角度平滑（可选） ━━━
        if (smoothing > 0.0f) {
            float curYaw   = *(float*)(localPlayer + 76);  // +0x4C
            float curPitch = *(float*)(localPlayer + 80);  // +0x50
            targetYaw   = curYaw   + (targetYaw   - curYaw)   * smoothing;
            targetPitch = curPitch + (targetPitch - curPitch) * smoothing;
        }
        
        // ━━━ Step 9: 写入角度 ━━━
        *(float*)(localPlayer + 76) = targetYaw;    // +0x4C P_camRot
        *(float*)(localPlayer + 80) = targetPitch;  // +0x50
        
        // ━━━ Step 10: 重置标志 ━━━
        // 获取 Transform 指针 (localPlayer + 0x54)
        Transform* transform = *(Transform**)(localPlayer + 0x54);
        if (transform) {
            // v1[4]  = transform + 0x10
            // v1[9]  = transform + 0x24
            // v1[16] = transform + 0x40
            // v1[21] = transform + 0x54
            *(int*)(transform + 0x10) = 0;
            *(int*)(transform + 0x24) = 0;
            *(int*)(transform + 0x40) = 0;
            *(int*)(transform + 0x54) = 0;
        }
        
        break;  // 只锁定一个目标
    }
}
```

### 6.3 关键内存布局

```
struct PlayerController {
    // +0x00 ~ +0x1F: 虚函数表 + 未知
    int teamID;              // +0x20 (32): 队伍ID (0=观察者, 1=队1, 2=队2)
    // +0x24 ~ +0x47: 未知
    float cameraYaw;         // +0x4C (76): 相机水平旋转
    float cameraPitch;       // +0x50 (80): 相机垂直旋转
    Transform* transform;    // +0x54 (84): Transform组件指针
    CharacterController* cc; // +0x58 (88): CharacterController指针
    // ...
};

struct Vector3 {
    float x;
    float y;
    float z;
};

struct PlayerScreenData {
    float screenX;      // v47[85] = +85*4
    float screenY;      // v47[87] = +87*4
    float screenWidth;  // v47[86] = +86*4
    float screenHeight; // v47[88] = +88*4
    BYTE isVisible;     // v47[81]+1 = +81*4+1
};

// 骨骼索引 (sub_10002550)
enum BoneIndex {
    HEAD       = 0,   // 头部
    NECK       = 3,   // 颈部
    LEFT_HAND  = 6,   // 左手
    CHEST      = 7,   // 胸部
    PELVIS     = 10,  // 骨盆
    RIGHT_HAND = ?,   // 右手 (未在调用中确认)
    LEFT_FOOT  = ?,   // 左脚 (未在调用中确认)
    RIGHT_FOOT = ?,   // 右脚 (未在调用中确认)
};

// 标志重置 (DLL 3.3 反汇编原文)
// v1[4]  = Transform + 0x10
// v1[9]  = Transform + 0x24
// v1[16] = Transform + 0x40
// v1[21] = Transform + 0x54
```

---

## 7. ImGui 绘制函数 (sub_1002AD70)

地址: `0x1002AD70`, 大小: `0x17C`

此函数包含 `sub_1002AE30` 地址（原MD中为ImGui绘制方框的函数）。是 `sub_1002AD70` 的内部调用点。

---

## 8. GetAsyncKeyState 调用点汇总

IDA 显示 `GetAsyncKeyState` 在以下位置被引用：

| 引用地址 | 所在区域 | 推测用途 |
|---------|---------|---------|
| `0x10005778` | sub_10005360 附近 (0x10005360-0x1000544E) | **主窗口消息处理循环** |
| `0x1004ad3c` | 未识别函数区域 (0x1004a988~0x1004bc5e) | **Aimbot 主循环 - 热键检测** |
| `0x1004b435` | 同上区域 | **Aimbot 主循环 - 辅助热键** |
| `0x1004b7a9` | 同上区域 | **Aimbot 主循环 - 功能切换** |

`0x1004ad3c`, `0x1004b435`, `0x1004b7a9` 均位于约 0x1004a988 ~ 0x1004bc5e 的**未识别函数区域**中，这是本 DLL 的自瞄+ESP 核心功能区域。

---

## 9. 配置加载 (sub_1004A040)

地址: `0x1004A040`, 大小: `0x948`

此函数初始化所有配置默认值，包括：
- `esp_config.ini` 文件读取（`"BoxESP="`, `"BoneESP="`）
- ESP 距离/大小参数
- 自瞄参数（距离限制、FOV、平滑等）
- 颜色表（RGB 颜色浮点数组）
- 各种功能开关的默认状态

重要发现的配置偏移（基于 `dword_1005F76C` 指针）：

```
dword_1005F76C[3639]  = 50.0f     // 距离/范围参数
dword_1005F76C[3640]  = 50.0f     // 同上
dword_1005F76C[3642]  = 1.0f      // 透明度
dword_1005F76C[3652]  = 8.0f      // 自瞄参数
dword_1005F76C[3653]  = 5.5f      // 自瞄参数
dword_1005F76C[3656]  = 12.0f     // 自瞄距离限制
dword_1005F76C[3657]  = 8.0f      // 自瞄参数
dword_1005F76C[3664]  = 35.0f     // FOV 视野限制
```

---

## 10. 开发 Frida 代码需要的关键 RVA

| 描述 | 地址 |
|------|------|
| GetAsyncKeyState IAT | 0x10051188 |
| SetCursorPos IAT | 0x100511ac |
| GetCursorPos IAT | 0x100511a8 |
| ScreenToClient IAT | 0x10051154 |
| ClientToScreen IAT | 0x10051160 |
| sub_1002AD70 (ImGui Draw) | 0x1002AD70 |
| sub_10033140 (ImGui Init) | 0x10033140 |
| sub_10033260 (ImGui NewFrame) | 0x10033260 |
| sub_1004A040 (Config Init) | 0x1004A040 |
| GameManager 字符串 | 0x100538e4 |
| esp_config.ini 字符串 | 0x1005b280 |
| BoxESP= 字符串 | 0x1005b290 |
| BoneESP= 字符串 | 0x1005b298 |
| 主上下文对象指针 | 0x1005F76C |

---

## 11. Unity API 调用签名（Frida NativeFunction 使用）

```javascript
// Transform.get_transform()
// Transform* (Component* this, MethodInfo* method)
RVA 需要从 il2cpp 运行时解析或特征码搜索

// Transform.get_position()
// void (Transform* this, Vector3* out, MethodInfo* method)
RVA 需要从 il2cpp 运行时解析或特征码搜索

// Transform.get_gameObject()
// GameObject* (Transform* this, MethodInfo* method)
RVA 需要从 il2cpp 运行时解析或特征码搜索

// GameObject.GetComponent()
// void* (GameObject* this, Il2CppClass* type, MethodInfo* method)
RVA 需要从 il2cpp 运行时解析或特征码搜索

// Animator.GetBoneTransform()
// Transform* (Animator* this, int boneIndex, MethodInfo* method)
RVA 需要从 il2cpp 运行时解析或特征码搜索

// Physics.Linecast()
// bool (Vector3* start, Vector3* end, int layerMask, MethodInfo* method)
RVA 需要从 il2cpp 运行时解析或特征码搜索
```

---

## 附录：IDA 提取的原始数据

### 导入表（完整 USER32 部分）
```
GetAsyncKeyState @ 0x10051188
SetCursorPos    @ 0x100511ac
GetCursorPos    @ 0x100511a8
ScreenToClient  @ 0x10051154
ClientToScreen  @ 0x10051160
GetKeyState     @ 0x1005114c
SetCursor       @ 0x10051178
GetClientRect   @ 0x1005117c
```

### GetAsyncKeyState 完整 xref 列表
```
0x10005778 - sub_10005360 区域（主循环）
0x1004ad3c - 未识别函数区域（Aimbot主循环）
0x1004b435 - 未识别函数区域（辅助热键）
0x1004b7a9 - 未识别函数区域（功能切换）
```

---

*数据提取时间: 2026-05-09*
*提取工具: IDA Pro 9.0 via MCP*
*分析目标: UnityCrossFire.dll (MD5: 2be82d9a5c9820a3ecc224b6b89e99b7)*
