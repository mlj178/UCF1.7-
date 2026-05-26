# UnityCrossFire.dll 技术实现详解

**文档版本**: 1.0  
**创建日期**: 2026-05-26  
**目标DLL**: UnityCrossFire.dll (MD5: 2be82d9a5c9820a3ecc224b6b89e99b7)

---

## 一、自瞄系统技术实现

### 1.1 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    自瞄系统架构                          │
├─────────────────────────────────────────────────────────┤
│  输入层: GetAsyncKeyState (热键检测)                     │
│  ↓                                                       │
│  数据层: GameManager → Player → Transform               │
│  ↓                                                       │
│  计算层: 坐标计算 → 角度计算 → 平滑处理                  │
│  ↓                                                       │
│  输出层: 内存写入 (Player +0x4C, +0x50)                 │
└─────────────────────────────────────────────────────────┘
```

### 1.2 核心实现代码分析

#### 1.2.1 热键检测实现

**位置**: 0x1004ad3c 附近

**实现逻辑**:
```cpp
// 伪代码
bool CheckAimHotkey() {
    // 调用 GetAsyncKeyState @ IAT 0x10051188
    SHORT keyState = GetAsyncKeyState(aimHotkey);
    
    // 检测最高位是否为1 (按键按下)
    if (keyState & 0x8000) {
        return true;  // 激活自瞄
    }
    
    return false;
}
```

**关键点**:
- 使用 `GetAsyncKeyState` 异步检测按键状态
- 检测最高位 (0x8000) 判断按键是否按下
- 支持自定义热键 (配置项: AimKey)

#### 1.2.2 游戏对象获取

**GameManager获取**:
```cpp
// 通过IL2CPP反射获取GameManager类
Il2CppClass* gameManagerClass = il2cpp_class_from_name(
    "Assembly-CSharp",  // 命名空间
    "GameManager"       // 类名 (字符串 @ 0x100538e4)
);

// 获取静态实例字段
FieldInfo* instanceField = il2cpp_class_get_field_from_name(
    gameManagerClass,
    "Instance"  // 单例字段名
);

// 读取实例指针
GameManager* gm = (GameManager*)il2cpp_field_static_get_value(instanceField);
```

**本地玩家获取**:
```cpp
// 从GameManager获取本地玩家
Player* GetLocalPlayer(GameManager* gm) {
    // 方法1: 通过字段偏移
    Player* localPlayer = *(Player**)(gm + LOCAL_PLAYER_OFFSET);
    
    // 方法2: 通过方法调用
    MethodInfo* getLocalPlayerMethod = il2cpp_class_get_method_from_name(
        gameManagerClass,
        "get_LocalPlayer",
        0  // 参数数量
    );
    
    Player* localPlayer = ((Player* (*)(GameManager*, MethodInfo*))getLocalPlayerMethod->methodPointer)(
        gm,
        getLocalPlayerMethod
    );
    
    // 验证玩家有效性
    if (!localPlayer) return nullptr;
    if (IsPlayerDead(localPlayer)) return nullptr;
    
    return localPlayer;
}
```

#### 1.2.3 敌人遍历与筛选

**玩家列表结构**:
```cpp
struct GameManager {
    // ... 其他字段
    PlayerList* playersBL;  // +0x20: 蓝队玩家列表
    PlayerList* playersGR;  // +0x28: 红队玩家列表
    // ... 其他字段
};

struct PlayerList {
    Player** players;      // 玩家数组指针
    int count;             // 玩家数量
};
```

**遍历实现**:
```cpp
void FindBestTarget(GameManager* gm, Player* localPlayer, Player** outTarget) {
    *outTarget = nullptr;
    float bestScore = FLT_MAX;
    
    // 遍历蓝队
    PlayerList* blueTeam = gm->playersBL;
    for (int i = 0; i < blueTeam->count; i++) {
        Player* target = blueTeam->players[i];
        if (IsValidTarget(target, localPlayer)) {
            float score = CalculateTargetScore(target, localPlayer);
            if (score < bestScore) {
                bestScore = score;
                *outTarget = target;
            }
        }
    }
    
    // 遍历红队
    PlayerList* redTeam = gm->playersGR;
    for (int i = 0; i < redTeam->count; i++) {
        Player* target = redTeam->players[i];
        if (IsValidTarget(target, localPlayer)) {
            float score = CalculateTargetScore(target, localPlayer);
            if (score < bestScore) {
                bestScore = score;
                *outTarget = target;
            }
        }
    }
}
```

**目标验证**:
```cpp
bool IsValidTarget(Player* target, Player* localPlayer) {
    // 基本检查
    if (!target) return false;
    if (target == localPlayer) return false;
    
    // 队伍检查
    if (target->teamID == localPlayer->teamID) return false;
    
    // 死亡检查
    if (IsPlayerDead(target)) return false;
    
    // 可见性检查
    if (!IsVisible(localPlayer, target)) return false;
    
    return true;
}
```

#### 1.2.4 可见性检测

**射线检测实现**:
```cpp
bool IsVisible(Player* from, Player* to) {
    // 获取位置
    Vector3 startPos = GetPosition(from);
    Vector3 endPos = GetPosition(to);
    
    // 调用 Physics.Linecast (字符串 @ 0x100547fc)
    // 签名: Boolean Linecast(Vector3 start, Vector3 end, Int32 layerMask)
    
    // 获取Physics类
    Il2CppClass* physicsClass = il2cpp_class_from_name("UnityEngine", "Physics");
    
    // 获取Linecast方法
    MethodInfo* linecastMethod = il2cpp_class_get_method_from_name(
        physicsClass,
        "Linecast",
        3  // 3个参数
    );
    
    // 调用方法
    bool hit = ((bool (*)(Vector3*, Vector3*, int, MethodInfo*))linecastMethod->methodPointer)(
        &startPos,
        &endPos,
        LAYER_MASK_DEFAULT,  // 层遮罩
        linecastMethod
    );
    
    return !hit;  // 没有碰撞 = 可见
}
```

#### 1.2.5 骨骼位置获取

**骨骼索引定义**:
```cpp
enum BoneIndex {
    HEAD       = 0,   // 头部
    NECK       = 3,   // 颈部
    LEFT_HAND  = 6,   // 左手
    CHEST      = 7,   // 胸部 (自瞄默认目标)
    PELVIS     = 10,  // 骨盆
    RIGHT_HAND = 11,  // 右手
    LEFT_FOOT  = 14,  // 左脚
    RIGHT_FOOT = 15   // 右脚
};
```

**获取骨骼位置**:
```cpp
Vector3 GetBonePosition(Player* player, int boneIndex) {
    // 获取Animator组件
    Animator* animator = GetComponent<Animator>(player);
    if (!animator) return GetPosition(player);  // 回退到中心位置
    
    // 获取骨骼Transform
    // 方法: Animator.GetBoneTransform(int boneIndex)
    MethodInfo* getBoneMethod = il2cpp_class_get_method_from_name(
        animatorClass,
        "GetBoneTransform",
        1
    );
    
    Transform* boneTransform = ((Transform* (*)(Animator*, int, MethodInfo*))getBoneMethod->methodPointer)(
        animator,
        boneIndex,
        getBoneMethod
    );
    
    if (!boneTransform) return GetPosition(player);
    
    // 获取骨骼位置
    // 方法: Transform.get_position (字符串 @ 0x10054674)
    MethodInfo* getPositionMethod = il2cpp_class_get_method_from_name(
        transformClass,
        "get_position",
        0
    );
    
    Vector3 position;
    ((void (*)(Transform*, Vector3*, MethodInfo*))getPositionMethod->methodPointer)(
        boneTransform,
        &position,
        getPositionMethod
    );
    
    return position;
}
```

#### 1.2.6 角度计算

**数学原理**:
```
给定:
- 玩家位置: (selfX, selfY, selfZ)
- 目标位置: (targetX, targetY, targetZ)

计算:
dx = targetX - selfX
dy = targetY - selfY
dz = targetZ - selfZ

水平距离: hDist = sqrt(dx² + dz²)

Yaw (水平旋转): atan2(dx, dz) * 180 / π
Pitch (垂直旋转): atan2(dy, hDist) * 180 / π
```

**代码实现**:
```cpp
void CalculateAimAngles(Vector3 selfPos, Vector3 targetPos, float* yaw, float* pitch) {
    // 计算差值
    float dx = targetPos.x - selfPos.x;
    float dy = targetPos.y - selfPos.y;
    float dz = targetPos.z - selfPos.z;
    
    // 计算水平距离
    float hDist = sqrtf(dx * dx + dz * dz);
    
    // 计算角度 (弧度转角度)
    const float RAD_TO_DEG = 180.0f / 3.14159265358979323846f;
    
    *yaw = atan2f(dx, dz) * RAD_TO_DEG;
    *pitch = atan2f(dy, hDist) * RAD_TO_DEG;
}
```

#### 1.2.7 角度平滑

**平滑算法**:
```cpp
void SmoothAngles(float* targetYaw, float* targetPitch, float currentYaw, float currentPitch, float smoothFactor) {
    // 线性插值平滑
    // 公式: new = current + (target - current) * smoothFactor
    
    *targetYaw = currentYaw + (*targetYaw - currentYaw) * smoothFactor;
    *targetPitch = currentPitch + (*targetPitch - currentPitch) * smoothFactor;
}
```

**配置参数**:
- `smoothFactor1` @ offset +3652 (默认 8.0f)
- `smoothFactor2` @ offset +3653 (默认 5.5f)
- `smoothFactor3` @ offset +3657 (默认 8.0f)

**高级平滑算法**:
```cpp
// 指数平滑
float ExponentialSmooth(float current, float target, float rate, float deltaTime) {
    return current + (target - current) * (1.0f - expf(-rate * deltaTime));
}

// 贝塞尔平滑
float BezierSmooth(float current, float target, float t) {
    // 三次贝塞尔曲线
    float t2 = t * t;
    float t3 = t2 * t;
    return current * (1 - 3*t + 3*t2 - t3) + target * t3;
}
```

#### 1.2.8 角度写入

**内存布局**:
```cpp
struct PlayerController {
    // ... 其他字段
    float cameraYaw;    // +0x4C (76): 相机水平旋转
    float cameraPitch;  // +0x50 (80): 相机垂直旋转
    // ... 其他字段
};
```

**写入实现**:
```cpp
void WriteAimAngles(Player* player, float yaw, float pitch) {
    // 直接内存写入
    *(float*)(player + 0x4C) = yaw;
    *(float*)(player + 0x50) = pitch;
    
    // 重置相关标志
    Transform* transform = *(Transform**)(player + 0x54);
    if (transform) {
        *(int*)(transform + 0x10) = 0;
        *(int*)(transform + 0x24) = 0;
        *(int*)(transform + 0x40) = 0;
        *(int*)(transform + 0x54) = 0;
    }
}
```

### 1.3 完整流程伪代码

```cpp
void Aimbot_Update() {
    // 1. 热键检测
    if (!(GetAsyncKeyState(aimHotkey) & 0x8000)) return;
    
    // 2. 获取GameManager
    GameManager* gm = GetGameManager();
    if (!gm) return;
    
    // 3. 获取本地玩家
    Player* localPlayer = GetLocalPlayer(gm);
    if (!localPlayer || IsPlayerDead(localPlayer)) return;
    
    // 4. 寻找最佳目标
    Player* target = nullptr;
    FindBestTarget(gm, localPlayer, &target);
    if (!target) return;
    
    // 5. 获取目标位置 (胸部骨骼)
    Vector3 targetPos = GetBonePosition(target, BONE_CHEST);
    Vector3 selfPos = GetPosition(localPlayer);
    
    // 6. 计算瞄准角度
    float targetYaw, targetPitch;
    CalculateAimAngles(selfPos, targetPos, &targetYaw, &targetPitch);
    
    // 7. 角度平滑
    float currentYaw = *(float*)(localPlayer + 0x4C);
    float currentPitch = *(float*)(localPlayer + 0x50);
    SmoothAngles(&targetYaw, &targetPitch, currentYaw, currentPitch, smoothFactor);
    
    // 8. 写入角度
    WriteAimAngles(localPlayer, targetYaw, targetPitch);
}
```

---

## 二、ESP透视系统技术实现

### 2.1 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    ESP系统架构                           │
├─────────────────────────────────────────────────────────┤
│  数据层: FindObjectsOfType → Player遍历                 │
│  ↓                                                       │
│  转换层: WorldToScreen → 坐标转换                       │
│  ↓                                                       │
│  计算层: 距离计算 → 尺寸计算 → 颜色选择                 │
│  ↓                                                       │
│  渲染层: ImGui DrawList → 绘制方框/骨骼/文字           │
└─────────────────────────────────────────────────────────┘
```

### 2.2 核心实现代码分析

#### 2.2.1 世界坐标转屏幕坐标

**Unity API调用**:
```cpp
Vector2 WorldToScreen(Camera* camera, Vector3 worldPos) {
    // 调用 Camera.WorldToScreenPoint
    MethodInfo* worldToScreenMethod = il2cpp_class_get_method_from_name(
        cameraClass,
        "WorldToScreenPoint",
        1
    );
    
    Vector3 screenPos;
    ((void (*)(Camera*, Vector3*, Vector3*, MethodInfo*))worldToScreenMethod->methodPointer)(
        camera,
        &worldPos,
        &screenPos,
        worldToScreenMethod
    );
    
    // 转换为客户端坐标
    Vector2 clientPos;
    clientPos.x = screenPos.x;
    clientPos.y = screenPos.y;
    
    // 使用 ScreenToClient (IAT @ 0x10051154)
    HWND hwnd = GetForegroundWindow();
    POINT pt = { (LONG)clientPos.x, (LONG)clientPos.y };
    ScreenToClient(hwnd, &pt);
    
    clientPos.x = (float)pt.x;
    clientPos.y = (float)pt.y;
    
    return clientPos;
}
```

#### 2.2.2 方框ESP绘制

**计算方框尺寸**:
```cpp
void CalculateBoxSize(Player* player, Vector2 screenPos, float* width, float* height) {
    // 获取玩家位置
    Vector3 worldPos = GetPosition(player);
    
    // 计算距离
    Vector3 localPos = GetPosition(localPlayer);
    float distance = Vector3::Distance(localPos, worldPos);
    
    // 根据距离计算尺寸
    // 配置参数: espSize @ offset +3639 (默认 50.0f)
    float baseSize = *(float*)(dword_1005F76C + 14556);  // 50.0f
    
    // 距离衰减
    float scaleFactor = baseSize / (distance * 0.1f);
    
    *width = scaleFactor;
    *height = scaleFactor * 2.0f;  // 高度是宽度的2倍
}
```

**ImGui绘制**:
```cpp
void DrawBoxESP(Player* player, Vector2 screenPos, float width, float height) {
    // 获取ImGui绘制列表
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    
    // 计算方框位置
    ImVec2 p1(screenPos.x - width/2, screenPos.y - height/2);  // 左上
    ImVec2 p2(screenPos.x + width/2, screenPos.y + height/2);  // 右下
    
    // 选择颜色 (根据队伍)
    ImVec4 color = GetTeamColor(player->teamID);
    
    // 绘制方框
    drawList->AddRect(p1, p2, ImGui::ColorConvertFloat4ToU32(color), 0.0f, 0, 2.0f);
    
    // 绘制填充 (可选)
    ImVec4 fillColor = color;
    fillColor.w = 0.3f;  // 透明度
    drawList->AddRectFilled(p1, p2, ImGui::ColorConvertFloat4ToU32(fillColor));
}
```

#### 2.2.3 骨骼ESP绘制

**骨骼连接定义**:
```cpp
struct BoneConnection {
    int fromBone;
    int toBone;
};

BoneConnection skeletonConnections[] = {
    // 头部到颈部
    { HEAD, NECK },
    
    // 颈部到胸部
    { NECK, CHEST },
    
    // 胸部到骨盆
    { CHEST, PELVIS },
    
    // 左臂
    { CHEST, LEFT_HAND },
    
    // 右臂
    { CHEST, RIGHT_HAND },
    
    // 左腿
    { PELVIS, LEFT_FOOT },
    
    // 右腿
    { PELVIS, RIGHT_FOOT }
};
```

**绘制骨骼**:
```cpp
void DrawBoneESP(Player* player) {
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    Camera* mainCamera = Camera::get_main();
    
    // 获取所有骨骼位置
    Vector2 boneScreenPos[16];
    for (int i = 0; i < 16; i++) {
        Vector3 worldPos = GetBonePosition(player, i);
        boneScreenPos[i] = WorldToScreen(mainCamera, worldPos);
    }
    
    // 绘制骨骼连线
    ImVec4 color = GetTeamColor(player->teamID);
    ImU32 colorU32 = ImGui::ColorConvertFloat4ToU32(color);
    
    for (const auto& conn : skeletonConnections) {
        Vector2 from = boneScreenPos[conn.fromBone];
        Vector2 to = boneScreenPos[conn.toBone];
        
        // 检查是否在屏幕内
        if (IsOnScreen(from) && IsOnScreen(to)) {
            drawList->AddLine(
                ImVec2(from.x, from.y),
                ImVec2(to.x, to.y),
                colorU32,
                2.0f  // 线宽
            );
        }
    }
    
    // 绘制骨骼点
    for (int i = 0; i < 16; i++) {
        if (IsOnScreen(boneScreenPos[i])) {
            drawList->AddCircleFilled(
                ImVec2(boneScreenPos[i].x, boneScreenPos[i].y),
                3.0f,  // 半径
                colorU32
            );
        }
    }
}
```

#### 2.2.4 ESP主函数

```cpp
void ESP_Update() {
    // 获取主摄像机
    Camera* mainCamera = Camera::get_main();
    if (!mainCamera) return;
    
    // 获取本地玩家
    GameManager* gm = GetGameManager();
    Player* localPlayer = GetLocalPlayer(gm);
    if (!localPlayer) return;
    
    // 查找所有玩家
    // 使用 FindObjectsOfType (字符串 @ 0x10054534)
    Il2CppClass* playerClass = il2cpp_class_from_name("Assembly-CSharp", "Player");
    MethodInfo* findMethod = il2cpp_class_get_method_from_name(
        il2cpp_class_from_name("UnityEngine", "Object"),
        "FindObjectsOfType",
        1
    );
    
    Array<Player*>* players = ((Array<Player*>* (*)(Il2CppClass*, MethodInfo*))findMethod->methodPointer)(
        playerClass,
        findMethod
    );
    
    // 遍历绘制
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    
    for (int i = 0; i < players->Length; i++) {
        Player* player = players->Items[i];
        
        // 跳过本地玩家
        if (player == localPlayer) continue;
        
        // 跳过死亡玩家
        if (IsPlayerDead(player)) continue;
        
        // 获取屏幕位置
        Vector3 worldPos = GetPosition(player);
        Vector2 screenPos = WorldToScreen(mainCamera, worldPos);
        
        // 检查是否在屏幕内
        if (!IsOnScreen(screenPos)) continue;
        
        // 绘制方框ESP
        if (IsBoxESPEnabled()) {
            float width, height;
            CalculateBoxSize(player, screenPos, &width, &height);
            DrawBoxESP(player, screenPos, width, height);
        }
        
        // 绘制骨骼ESP
        if (IsBoneESPEnabled()) {
            DrawBoneESP(player);
        }
        
        // 绘制其他信息 (血量、名字等)
        DrawPlayerInfo(player, screenPos);
    }
}
```

---

## 三、武器修改系统技术实现

### 3.1 武器API调用

#### 3.1.1 GiveWeapon实现

```cpp
Weapon* GiveWeaponToPlayer(Player* player, int weaponIndex, bool autoGiveUp, bool autoSelect) {
    // 获取PlayerWeapons类 (字符串 @ 0x10054a08)
    Il2CppClass* playerWeaponsClass = il2cpp_class_from_name("Assembly-CSharp", "PlayerWeapons");
    
    // 获取GiveWeapon方法 (字符串 @ 0x10054918)
    // 签名: Weapon GiveWeapon(Player player, Int32 weaponIndex, Boolean autoGiveUp, Boolean autoSelect)
    MethodInfo* giveWeaponMethod = il2cpp_class_get_method_from_name(
        playerWeaponsClass,
        "GiveWeapon",
        4  // 4个参数
    );
    
    // 调用方法
    Weapon* weapon = ((Weapon* (*)(Player*, int, bool, bool, MethodInfo*))giveWeaponMethod->methodPointer)(
        player,
        weaponIndex,
        autoGiveUp,
        autoSelect,
        giveWeaponMethod
    );
    
    return weapon;
}
```

#### 3.1.2 无限弹药实现

```cpp
void SetInfiniteAmmo(Player* player, bool enable) {
    // 获取当前武器
    Weapon* currentWeapon = GetCurrentWeapon(player);
    if (!currentWeapon) return;
    
    // 修改弹药字段
    // 偏移需要通过逆向分析确定
    if (enable) {
        *(int*)(currentWeapon + AMMO_CLIP_OFFSET) = 9999;      // 弹夹弹药
        *(int*)(currentWeapon + AMMO_RESERVE_OFFSET) = 9999;  // 储备弹药
    }
}

// 或者Hook弹药消耗函数
void HookAmmoConsume() {
    // 找到弹药消耗函数
    // Hook使其不减少弹药
}
```

### 3.2 武器属性修改

```cpp
struct WeaponData {
    int weaponID;          // 武器ID
    float damage;         // 伤害
    float fireRate;       // 射速
    int clipSize;         // 弹夹大小
    float reloadTime;     // 装弹时间
    float range;          // 射程
};

void ModifyWeaponAttributes(Weapon* weapon, WeaponData* data) {
    // 通过偏移直接修改
    *(float*)(weapon + DAMAGE_OFFSET) = data->damage;
    *(float*)(weapon + FIRE_RATE_OFFSET) = data->fireRate;
    *(int*)(weapon + CLIP_SIZE_OFFSET) = data->clipSize;
    *(float*)(weapon + RELOAD_TIME_OFFSET) = data->reloadTime;
    *(float*)(weapon + RANGE_OFFSET) = data->range;
}
```

---

## 四、ImGui界面系统技术实现

### 4.1 ImGui集成

#### 4.1.1 DirectX 11 Hook

```cpp
// Hook Present 函数
typedef HRESULT (__stdcall *Present_t)(IDXGISwapChain*, UINT, UINT);
Present_t originalPresent = nullptr;

HRESULT __stdcall HookedPresent(IDXGISwapChain* swapChain, UINT syncInterval, UINT flags) {
    // 初始化ImGui (仅一次)
    static bool initialized = false;
    if (!initialized) {
        ImGui_Init(swapChain);
        initialized = true;
    }
    
    // 开始新帧
    ImGui_ImplDX11_NewFrame();
    ImGui_ImplWin32_NewFrame();
    ImGui::NewFrame();
    
    // 绘制ESP
    ESP_Update();
    
    // 绘制菜单
    DrawMenu();
    
    // 结束帧
    ImGui::EndFrame();
    ImGui::Render();
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());
    
    // 调用原始Present
    return originalPresent(swapChain, syncInterval, flags);
}
```

#### 4.1.2 ImGui初始化

**函数**: `sub_10033140` @ 0x10033140

```cpp
void ImGui_Init(IDXGISwapChain* swapChain) {
    // 创建ImGui上下文
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    
    // 设置IO
    ImGuiIO& io = ImGui::GetIO();
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
    io.IniFilename = "imgui.ini";  // 字符串 @ 0x10054a9c
    io.LogFilename = "imgui_log.txt";  // 字符串 @ 0x10054aa8
    
    // 设置风格
    ImGui::StyleColorsDark();
    
    // 获取DX11设备
    ID3D11Device* device;
    swapChain->GetDevice(__uuidof(ID3D11Device), (void**)&device);
    
    // 初始化ImGui DX11
    ImGui_ImplDX11_Init(device);
    
    // 初始化ImGui Win32
    ImGui_ImplWin32_Init(hwnd);
}
```

### 4.2 菜单绘制

```cpp
void DrawMenu() {
    // 设置窗口位置和大小
    ImGui::SetNextWindowSize(ImVec2(400, 300), ImGuiCond_FirstUseEver);
    
    // 开始窗口
    ImGui::Begin("UnityCrossFire Modifier", nullptr, ImGuiWindowFlags_MenuBar);
    
    // 菜单栏
    if (ImGui::BeginMenuBar()) {
        if (ImGui::BeginMenu("File")) {
            if (ImGui::MenuItem("Save Config")) {
                SaveConfig();
            }
            if (ImGui::MenuItem("Load Config")) {
                LoadConfig();
            }
            ImGui::EndMenu();
        }
        ImGui::EndMenuBar();
    }
    
    // 自瞄设置
    if (ImGui::CollapsingHeader("Aimbot")) {
        ImGui::Checkbox("Enable", &config.aimbotEnabled);
        ImGui::SliderFloat("FOV", &config.aimFOV, 1.0f, 180.0f);
        ImGui::SliderFloat("Distance", &config.aimDistance, 1.0f, 100.0f);
        ImGui::SliderFloat("Smooth", &config.aimSmooth, 0.1f, 20.0f);
        ImGui::Combo("Target Bone", &config.targetBone, "Head\0Chest\0Pelvis\0");
    }
    
    // ESP设置
    if (ImGui::CollapsingHeader("ESP")) {
        ImGui::Checkbox("Box ESP", &config.boxESP);
        ImGui::Checkbox("Bone ESP", &config.boneESP);
        ImGui::SliderFloat("Transparency", &config.espTransparency, 0.1f, 1.0f);
        
        if (ImGui::TreeNode("Colors")) {
            ImGui::ColorEdit4("Team 1", config.team1Color);
            ImGui::ColorEdit4("Team 2", config.team2Color);
            ImGui::TreePop();
        }
    }
    
    // 武器设置
    if (ImGui::CollapsingHeader("Weapon")) {
        ImGui::Checkbox("Infinite Ammo", &config.infiniteAmmo);
        ImGui::InputInt("Weapon ID", &config.weaponID);
        if (ImGui::Button("Give Weapon")) {
            GiveWeaponToPlayer(localPlayer, config.weaponID, true, true);
        }
    }
    
    ImGui::End();
}
```

---

## 五、配置系统技术实现

### 5.1 配置文件格式

**文件**: `esp_config.ini` (字符串 @ 0x1005b280)

**格式**:
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

### 5.2 配置读写实现

```cpp
void LoadConfig() {
    // 打开配置文件
    std::ifstream file("esp_config.ini");
    if (!file.is_open()) {
        // 使用默认配置
        return;
    }
    
    std::string line;
    while (std::getline(file, line)) {
        // 解析键值对
        size_t pos = line.find('=');
        if (pos == std::string::npos) continue;
        
        std::string key = line.substr(0, pos);
        std::string value = line.substr(pos + 1);
        
        // 设置配置值
        if (key == "BoxESP") {
            config.boxESP = (value == "1");
        } else if (key == "BoneESP") {
            config.boneESP = (value == "1");
        } else if (key == "AimKey") {
            config.aimKey = std::stoi(value);
        }
        // ... 其他配置项
    }
    
    file.close();
}

void SaveConfig() {
    std::ofstream file("esp_config.ini");
    if (!file.is_open()) return;
    
    file << "[Aimbot]\n";
    file << "Enable=" << config.aimbotEnabled << "\n";
    file << "FOV=" << config.aimFOV << "\n";
    file << "Distance=" << config.aimDistance << "\n";
    file << "Smooth=" << config.aimSmooth << "\n";
    
    file << "\n[ESP]\n";
    file << "BoxESP=" << config.boxESP << "\n";
    file << "BoneESP=" << config.boneESP << "\n";
    file << "Transparency=" << config.espTransparency << "\n";
    
    file.close();
}
```

### 5.3 配置初始化

**函数**: `sub_1004A040` @ 0x1004A040

```cpp
void InitializeConfig() {
    // 检查是否已初始化
    if (byte_1005F7C9) return;
    byte_1005F7C9 = 1;
    
    // 获取配置对象
    Config* config = (Config*)dword_1005F76C;
    
    // 设置默认值
    config->espSize = 50.0f;          // offset +3639
    config->espSize2 = 50.0f;         // offset +3640
    config->espTransparency = 1.0f;   // offset +3642
    config->aimSmooth1 = 8.0f;        // offset +3652
    config->aimSmooth2 = 5.5f;        // offset +3653
    config->aimDistance = 12.0f;      // offset +3656
    config->aimSmooth3 = 8.0f;        // offset +3657
    config->aimFOV = 35.0f;           // offset +3664
    
    // 设置默认颜色
    config->team1ColorR = 0.7843f;    // offset +3697
    config->team1ColorG = 0.7961f;    // offset +3698
    config->team1ColorB = 0.8157f;    // offset +3699
    config->team1ColorA = 1.0f;       // offset +3700
    
    // ... 更多颜色配置
    
    // 尝试加载配置文件
    LoadConfig();
}
```

---

## 六、性能优化建议

### 6.1 自瞄优化

1. **空间分割**: 使用四叉树/八叉树加速目标搜索
2. **缓存机制**: 缓存玩家列表，避免每帧重新查找
3. **异步处理**: 将目标搜索放到独立线程
4. **LOD系统**: 根据距离调整更新频率

### 6.2 ESP优化

1. **视锥剔除**: 只绘制屏幕内的玩家
2. **距离剔除**: 超过一定距离不绘制
3. **批处理**: 合并绘制调用
4. **异步更新**: ESP计算和渲染分离

### 6.3 内存优化

1. **对象池**: 重用临时对象
2. **智能缓存**: 缓存IL2CPP方法指针
3. **延迟加载**: 按需加载资源

---

## 七、安全性与反检测

### 7.1 代码混淆

- 使用虚拟机保护关键代码
- 字符串加密
- 控制流平坦化

### 7.2 内存保护

- 使用VirtualProtect保护关键内存
- 避免明显的特征码
- 动态计算偏移

### 7.3 检测规避

- 避免Hook常用函数
- 使用硬件断点替代软件Hook
- 随机化更新频率

---

**文档结束**

**注意事项**:
1. 本文档仅用于技术研究和学习
2. 实际使用时需要根据游戏版本调整偏移
3. 反作弊系统可能会检测到修改行为
4. 请遵守游戏服务条款和法律法规
