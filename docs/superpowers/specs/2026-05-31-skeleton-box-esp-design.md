# 骨骼与方框透视功能 - 设计文档

**创建日期**: 2026-05-31  
**目标项目**: UnityCrossFire 1.7  
**实现方式**: C++ DLL注入 + ImGui  
**功能范围**: 方框ESP（最小化验证）  

---

## 一、项目目标

### 1.1 核心目标
实现游戏内的透视功能（ESP），在屏幕上绘制方框标识敌人位置，验证整个技术流程的可行性。

### 1.2 技术选型
- **实现方式**: 基于现有m.cpp框架扩展（C++ DLL注入）
- **数据获取**: Unity IL2CPP API（与小工具一致）
- **渲染方式**: DirectX 11 Hook + ImGui
- **测试策略**: 一次性实现完整流程，代码结构分层

### 1.3 成功标准
- ✅ 能够正确获取游戏内所有玩家数据
- ✅ 能够将3D世界坐标转换为2D屏幕坐标
- ✅ 能够在屏幕上绘制方框标识敌人
- ✅ 方框颜色能区分敌我队伍
- ✅ 日志系统完善，便于调试

---

## 二、整体架构

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    ESP系统架构（分层设计）                    │
├─────────────────────────────────────────────────────────────┤
│  【渲染层】ImGui绘制                                          │
│  ├─ ESPRenderer::DrawBox() - 绘制2D方框                      │
│  └─ ESPRenderer::Render() - 主渲染循环                       │
│  ↓                                                           │
│  【转换层】坐标转换                                           │
│  ├─ CoordConverter::WorldToScreen() - 世界→屏幕坐标         │
│  └─ CoordConverter::CalculateBoxSize() - 计算方框尺寸       │
│  ↓                                                           │
│  【数据层】游戏数据获取                                       │
│  ├─ IL2CPPBridge - IL2CPP API封装                           │
│  ├─ GameManager - 游戏管理器访问                             │
│  ├─ PlayerController - 玩家控制器访问                        │
│  └─ Transform - Transform组件访问                            │
│  ↓                                                           │
│  【基础层】基础设施                                           │
│  ├─ Logger - 日志系统（已有dbg函数）                         │
│  └─ Config - 配置管理（后续扩展）                            │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 数据流向

```
游戏进程
  ↓
IL2CPP Bridge (封装API调用)
  ↓
GameManager::GetAllPlayers() (获取玩家列表)
  ↓
TransformHelper::GetPosition() (获取每个玩家位置)
  ↓
CoordConverter::WorldToScreen() (坐标转换)
  ↓
ESPRenderer::DrawBox() (ImGui绘制)
  ↓
屏幕显示
```

---

## 三、核心模块详细设计

### 3.1 数据层 - IL2CPP Bridge

**职责**: 封装IL2CPP API调用，提供类型安全的接口

**关键API地址** (来自小工具分析文档):
- `il2cpp_class_from_name` @ 字符串地址
- `il2cpp_class_get_method_from_name` @ 0x10053bc0
- `il2cpp_class_get_field_from_name` @ 0x10053b80
- `il2cpp_runtime_invoke` (需要查找)

**类设计**:
```cpp
class IL2CPPBridge {
public:
    // 初始化：获取IL2CPP导出函数地址
    static bool Initialize(HMODULE gameAssembly);
    
    // 类操作
    static Il2CppClass* GetClass(const char* namespaze, const char* className);
    static MethodInfo* GetMethod(Il2CppClass* klass, const char* methodName, int argsCount);
    static FieldInfo* GetField(Il2CppClass* klass, const char* fieldName);
    
    // 方法调用
    static void* Invoke(MethodInfo* method, void* obj, void** args);
    
    // 字段访问
    static void* GetFieldValue(void* obj, FieldInfo* field);
    
private:
    static void* s_GameAssemblyBase;
    // API函数指针
    static void* s_ClassFromName;
    static void* s_GetMethodFromName;
    static void* s_GetFieldFromName;
    static void* s_RuntimeInvoke;
};
```

**数据结构定义**:
```cpp
// Vector3 (Unity标准结构)
struct Vector3 {
    float x, y, z;
};

// Vector2 (屏幕坐标)
struct Vector2 {
    float x, y;
};

// PlayerController (基于文档偏移)
struct PlayerController {
    // +0x00 ~ +0x1F: 基类数据
    int teamID;              // +0x20 (32)
    // +0x24 ~ +0x47: 其他数据
    float cameraYaw;         // +0x4C (76)
    float cameraPitch;       // +0x50 (80)
    void* transform;         // +0x54 (84) - Transform*
    // ... 其他字段
};

// GameManager (基于文档偏移)
struct GameManager {
    void* vtable;            // +0x00
    // ...
    void* playersBL;         // +0x20 (32) - 蓝队PlayerList*
    void* playersGR;         // +0x28 (40) - 红队PlayerList*
    // ...
};
```

---

### 3.2 数据层 - GameManager访问

**职责**: 获取游戏管理器实例和玩家列表

**Unity类信息** (来自文档):
- 类名: `"GameManager"` @ 字符串地址 0x100538e4
- 命名空间: `"Assembly-CSharp"`
- 静态字段: `"Instance"` (单例)

**类设计**:
```cpp
class GameManager {
public:
    // 获取单例实例
    static void* GetInstance();
    
    // 获取本地玩家
    static void* GetLocalPlayer();
    
    // 获取所有玩家列表
    static std::vector<void*> GetAllPlayers();
    
    // 玩家验证
    static bool IsValidPlayer(void* player);
    static bool IsPlayerDead(void* player);
    static int GetPlayerTeam(void* player);
    
private:
    static void* s_Instance;
    static Il2CppClass* s_Class;
};
```

**实现要点**:
1. 通过IL2CPP反射获取GameManager类
2. 获取静态字段Instance得到单例
3. 读取playersBL和playersGR字段获取玩家列表
4. 验证玩家有效性（非空、未死亡）

---

### 3.3 数据层 - Transform访问

**职责**: 获取玩家位置和骨骼位置

**Unity API** (来自文档):
- `Transform.get_transform()` @ 字符串地址 0x1005464c
- `Transform.get_position()` @ 字符串地址 0x10054674
- `Transform.get_position_Injected()` @ 字符串地址 0x10054698

**类设计**:
```cpp
class TransformHelper {
public:
    // 获取Transform组件
    static void* GetTransform(void* player);
    
    // 获取世界坐标
    static Vector3 GetPosition(void* transform);
    
    // 获取骨骼位置 (后续扩展)
    static Vector3 GetBonePosition(void* player, int boneIndex);
    
private:
    static MethodInfo* s_GetTransformMethod;
    static MethodInfo* s_GetPositionMethod;
};
```

**实现要点**:
1. 从PlayerController +0x54偏移获取Transform指针
2. 调用get_position方法获取Vector3坐标
3. 注意处理空指针和无效对象

---

### 3.4 转换层 - 坐标转换

**职责**: 将3D世界坐标转换为2D屏幕坐标

**Unity API** (来自文档):
- `Camera.get_main` @ 字符串地址 0x100546c4
- `Camera.WorldToScreenPoint` (需要查找方法)

**Windows API** (来自文档):
- `ScreenToClient` @ IAT地址 0x10051154
- `GetForegroundWindow` @ IAT地址 0x1005116c

**类设计**:
```cpp
class CoordConverter {
public:
    // 初始化：获取主摄像机
    static bool Initialize();
    
    // 世界坐标 → 屏幕坐标
    static bool WorldToScreen(const Vector3& world, Vector2* outScreen);
    
    // 计算方框尺寸 (基于距离)
    static void CalculateBoxSize(float distance, float* width, float* height);
    
    // 判断是否在屏幕内
    static bool IsOnScreen(const Vector2& screen, float width, float height);
    
private:
    static void* s_MainCamera;
    static MethodInfo* s_WorldToScreenMethod;
};
```

**方框尺寸计算公式**:
```cpp
// 基于距离的尺寸衰减
float baseSize = Config::ESP_BASE_SIZE;  // 50.0f
float scaleFactor = baseSize / (distance * 0.1f);
*width = scaleFactor;
*height = scaleFactor * 2.0f;  // 高度是宽度的2倍 (人体比例)
```

**坐标转换流程**:
1. 调用Camera.WorldToScreenPoint转换到屏幕坐标
2. 使用ScreenToClient转换为窗口客户区坐标
3. 处理Y轴翻转（DirectX坐标系）

---

### 3.5 渲染层 - ImGui绘制

**职责**: 在屏幕上绘制ESP方框

**类设计**:
```cpp
class ESPRenderer {
public:
    // 主渲染函数 (在hkPresent中调用)
    static void Render();
    
    // 绘制单个玩家的ESP
    static void DrawPlayerESP(void* player, void* localPlayer);
    
    // 绘制2D方框
    static void DrawBox(const Vector2& center, float width, float height, 
                       const ImVec4& color, float thickness = 1.0f);
    
    // 颜色选择 (基于队伍和可见性)
    static ImVec4 GetPlayerColor(void* player, bool isVisible);
    
private:
    static bool s_Enabled;  // ESP开关
};
```

**渲染流程**:
```cpp
void ESPRenderer::Render() {
    if (!s_Enabled) return;
    
    // 1. 获取本地玩家
    void* localPlayer = GameManager::GetLocalPlayer();
    if (!localPlayer) return;
    
    // 2. 获取所有玩家
    auto players = GameManager::GetAllPlayers();
    
    // 3. 遍历绘制
    int drawnCount = 0;
    for (void* player : players) {
        // 筛选敌人
        if (!IsValidTarget(player, localPlayer)) continue;
        
        // 绘制ESP
        DrawPlayerESP(player, localPlayer);
        drawnCount++;
    }
    
    // 日志 (每60帧输出一次)
    static int frameCounter = 0;
    if (++frameCounter % 60 == 0) {
        dbg("[ESP] Players: %d, Drawn: %d", players.size(), drawnCount);
    }
}
```

**方框绘制实现**:
```cpp
void ESPRenderer::DrawBox(const Vector2& center, float w, float h, 
                          const ImVec4& color, float thickness) {
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    
    ImVec2 p1(center.x - w/2, center.y - h/2);  // 左上
    ImVec2 p2(center.x + w/2, center.y + h/2);  // 右下
    
    ImU32 col = ImGui::ColorConvertFloat4ToU32(color);
    drawList->AddRect(p1, p2, col, 0.0f, 0, thickness);
}
```

**颜色选择逻辑**:
```cpp
ImVec4 ESPRenderer::GetPlayerColor(void* player, bool isVisible) {
    int teamID = GameManager::GetPlayerTeam(player);
    
    // 根据队伍选择颜色
    if (teamID == 0) {  // 蓝队
        return isVisible ? Config::COLOR_TEAM1 : Config::COLOR_TEAM1_HIDDEN;
    } else {  // 红队
        return isVisible ? Config::COLOR_TEAM2 : Config::COLOR_TEAM2_HIDDEN;
    }
}
```

---

## 四、集成方案

### 4.1 修改m.cpp的位置

**位置1: ImGui初始化后** (g_ImGuiInit = true之后):
```cpp
if (g_ImGuiInit && !g_ESPInitialized) {
    // 初始化ESP系统
    HMODULE gameAsm = GetModuleHandleA("GameAssembly.dll");
    if (gameAsm) {
        if (IL2CPPBridge::Initialize(gameAsm)) {
            if (CoordConverter::Initialize()) {
                g_ESPInitialized = true;
                dbg("=== ESP System Initialized ===");
            }
        }
    }
}
```

**位置2: ImGui渲染循环中** (ImGui::NewFrame()之后):
```cpp
if (g_ImGuiInit && g_ESPInitialized) {
    // 渲染ESP
    ESPRenderer::Render();
}
```

**位置3: Demo窗口添加控制**:
```cpp
ImGui::Begin("ESP Demo", NULL, ImGuiWindowFlags_NoCollapse);
{
    ImGui::Checkbox("Enable ESP", &ESPRenderer::s_Enabled);
    ImGui::Separator();
    ImGui::Text("Frame: %d", (int)g_FrameCount);
    // ... 其他信息
}
ImGui::End();
```

### 4.2 新增文件结构

```
m/
├── imgui/              (已有)
├── m.cpp               (修改：添加ESP调用)
├── esp/
│   ├── il2cpp_bridge.h     (IL2CPP API封装)
│   ├── il2cpp_bridge.cpp
│   ├── game_manager.h      (GameManager访问)
│   ├── game_manager.cpp
│   ├── transform_helper.h  (Transform访问)
│   ├── transform_helper.cpp
│   ├── coord_converter.h   (坐标转换)
│   ├── coord_converter.cpp
│   ├── esp_renderer.h      (ImGui绘制)
│   ├── esp_renderer.cpp
│   └── esp_config.h        (配置常量)
└── build.bat           (修改：添加新文件编译)
```

---

## 五、错误处理与日志

### 5.1 关键检查点

每个模块初始化和关键操作都需要日志：

```cpp
// IL2CPP Bridge初始化
if (!IL2CPPBridge::Initialize(gameAsm)) {
    dbg("[ERROR] IL2CPP Bridge init failed");
    return false;
}
dbg("[OK] IL2CPP Bridge initialized");

// GameManager获取
if (!GameManager::GetInstance()) {
    dbg("[WARN] GameManager instance not found");
    return;
}
dbg("[OK] GameManager found at 0x%p", instance);

// 玩家列表获取
if (players.empty()) {
    dbg("[INFO] No players found");
    return;
}
dbg("[OK] Found %d players", players.size());

// 坐标转换失败
if (!CoordConverter::WorldToScreen(worldPos, &screenPos)) {
    dbg("[WARN] WorldToScreen failed for player at (%.2f, %.2f, %.2f)",
        worldPos.x, worldPos.y, worldPos.z);
    return;
}
```

### 5.2 性能监控

```cpp
// 每60帧输出一次性能统计
static int frameCounter = 0;
static float totalTime = 0.0f;

auto startTime = std::chrono::high_resolution_clock::now();

// ... ESP渲染逻辑 ...

auto endTime = std::chrono::high_resolution_clock::now();
float elapsed = std::chrono::duration<float>(endTime - startTime).count();
totalTime += elapsed;

if (++frameCounter % 60 == 0) {
    dbg("[ESP Perf] Avg: %.3fms, Players: %d", 
        (totalTime / 60.0f) * 1000.0f, playerCount);
    totalTime = 0.0f;
}
```

---

## 六、配置参数

### 6.1 初期硬编码配置

```cpp
namespace Config {
    // ESP基础参数
    constexpr float ESP_BASE_SIZE = 50.0f;      // 基础方框尺寸
    constexpr float BOX_THICKNESS = 1.5f;       // 方框线条粗细
    constexpr float MAX_DISTANCE = 100.0f;      // 最大显示距离
    constexpr float MIN_DISTANCE = 1.0f;        // 最小显示距离
    
    // 颜色配置 (RGBA)
    constexpr ImVec4 COLOR_TEAM1 = {0.78f, 0.80f, 0.82f, 1.0f};     // 蓝队 (可见)
    constexpr ImVec4 COLOR_TEAM2 = {0.5f, 0.6f, 0.7f, 1.0f};        // 红队 (可见)
    constexpr ImVec4 COLOR_TEAM1_HIDDEN = {0.78f, 0.80f, 0.82f, 0.5f}; // 蓝队 (不可见)
    constexpr ImVec4 COLOR_TEAM2_HIDDEN = {0.5f, 0.6f, 0.7f, 0.5f};    // 红队 (不可见)
    
    // 性能参数
    constexpr int LOG_INTERVAL = 60;  // 每60帧输出一次日志
}
```

### 6.2 后续扩展：配置文件

```ini
[ESP]
Enable=1
BaseSize=50.0
BoxThickness=1.5
MaxDistance=100.0

[Colors]
Team1R=0.78
Team1G=0.80
Team1B=0.82
Team1A=1.0

Team2R=0.5
Team2G=0.6
Team2B=0.7
Team2A=1.0
```

---

## 七、后续扩展路径

### 7.1 骨骼ESP扩展

**新增骨骼索引定义**:
```cpp
enum BoneIndex {
    HEAD       = 0,   // 头部
    NECK       = 3,   // 颈部
    LEFT_HAND  = 6,   // 左手
    CHEST      = 7,   // 胸部
    PELVIS     = 10,  // 骨盆
    RIGHT_HAND = 11,  // 右手
    LEFT_FOOT  = 14,  // 左脚
    RIGHT_FOOT = 15   // 右脚
};
```

**骨骼连接定义**:
```cpp
const int BONE_CONNECTIONS[][2] = {
    {HEAD, NECK},         // 头-颈
    {NECK, CHEST},        // 颈-胸
    {CHEST, PELVIS},      // 胸-骨盆
    {CHEST, LEFT_HAND},   // 胸-左手
    {CHEST, RIGHT_HAND},  // 胸-右手
    {PELVIS, LEFT_FOOT},  // 骨盆-左脚
    {PELVIS, RIGHT_FOOT}  // 骨盆-右脚
};
```

**绘制函数**:
```cpp
void ESPRenderer::DrawSkeleton(void* player) {
    // 获取所有骨骼位置
    std::map<int, Vector2> boneScreenPos;
    for (int bone : ALL_BONES) {
        Vector3 worldPos = TransformHelper::GetBonePosition(player, bone);
        Vector2 screenPos;
        if (CoordConverter::WorldToScreen(worldPos, &screenPos)) {
            boneScreenPos[bone] = screenPos;
        }
    }
    
    // 绘制骨骼连线
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    for (auto& conn : BONE_CONNECTIONS) {
        Vector2 p1 = boneScreenPos[conn[0]];
        Vector2 p2 = boneScreenPos[conn[1]];
        drawList->AddLine(p1, p2, color);
    }
}
```

### 7.2 血量ESP扩展

```cpp
void ESPRenderer::DrawHealthBar(void* player, const Vector2& screenPos) {
    // 获取血量
    float health = GetPlayerHealth(player);
    float maxHealth = 100.0f;
    float ratio = health / maxHealth;
    
    // 绘制血量条
    float barWidth = 50.0f;
    float barHeight = 5.0f;
    ImVec2 p1(screenPos.x - barWidth/2, screenPos.y - 30);
    ImVec2 p2(screenPos.x + barWidth/2, p1.y + barHeight);
    
    ImDrawList* drawList = ImGui::GetBackgroundDrawList();
    
    // 背景
    drawList->AddRectFilled(p1, p2, IM_COL32(0, 0, 0, 200));
    
    // 血量
    ImVec2 p3(p1.x, p1.y);
    ImVec2 p4(p1.x + barWidth * ratio, p2.y);
    ImU32 healthColor = ratio > 0.5 ? IM_COL32(0, 255, 0, 255) : 
                        ratio > 0.25 ? IM_COL32(255, 255, 0, 255) : 
                                       IM_COL32(255, 0, 0, 255);
    drawList->AddRectFilled(p3, p4, healthColor);
}
```

### 7.3 其他ESP扩展

- **距离ESP**: 显示与敌人的距离数值
- **名字ESP**: 显示敌人玩家名称
- **武器ESP**: 显示敌人当前武器
- **雷达ESP**: 小地图显示敌人位置

---

## 八、测试计划

### 8.1 单元测试（可选）

```cpp
// 测试IL2CPP Bridge
void TestIL2CPPBridge() {
    HMODULE gameAsm = GetModuleHandleA("GameAssembly.dll");
    assert(gameAsm != NULL);
    
    bool initResult = IL2CPPBridge::Initialize(gameAsm);
    assert(initResult == true);
    
    Il2CppClass* gmClass = IL2CPPBridge::GetClass("Assembly-CSharp", "GameManager");
    assert(gmClass != NULL);
    
    dbg("[TEST] IL2CPPBridge: PASS");
}

// 测试坐标转换
void TestCoordConverter() {
    Vector3 worldPos = {0, 0, 0};
    Vector2 screenPos;
    
    bool result = CoordConverter::WorldToScreen(worldPos, &screenPos);
    assert(result == true);
    
    dbg("[TEST] WorldToScreen: (%.2f, %.2f, %.2f) -> (%.2f, %.2f)",
        worldPos.x, worldPos.y, worldPos.z, screenPos.x, screenPos.y);
}
```

### 8.2 集成测试

**测试步骤**:
1. 启动游戏
2. 注入DLL（运行esp_test.py）
3. 查看日志文件确认初始化成功
4. 进入游戏房间
5. 查看是否能在敌人周围看到方框
6. 检查日志中的玩家数量和绘制数量

**预期结果**:
- 日志显示"ESP System Initialized"
- 日志显示找到玩家数量
- 游戏内能看到方框
- 方框颜色区分敌我

### 8.3 性能测试

**监控指标**:
- ESP渲染耗时（目标 < 5ms）
- 帧率影响（目标 < 5%）
- 内存占用（目标 < 10MB）

---

## 九、风险评估

### 9.1 技术风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| IL2CPP API地址变化 | 高 | 动态查找导出函数，不硬编码地址 |
| 游戏更新导致偏移失效 | 高 | 使用IL2CPP反射而非硬编码偏移 |
| ImGui渲染冲突 | 中 | 使用BackgroundDrawList避免遮挡 |
| 性能问题 | 中 | 添加距离剔除，限制绘制数量 |
| 反作弊检测 | 高 | 仅读取数据，不修改游戏内存 |

### 9.2 实现风险

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 编译环境问题 | 中 | 提供详细的编译说明 |
| 注入失败 | 中 | 完善错误日志，提供排查指南 |
| 坐标转换错误 | 中 | 详细记录转换过程，便于调试 |
| 空指针崩溃 | 高 | 所有指针访问前验证有效性 |

---

## 十、实施计划概览

### 10.1 开发阶段

1. **阶段1: 基础设施** (1-2小时)
   - 创建esp目录结构
   - 实现IL2CPP Bridge基础框架
   - 添加配置常量

2. **阶段2: 数据层** (2-3小时)
   - 实现GameManager访问
   - 实现Transform访问
   - 测试数据获取

3. **阶段3: 转换层** (1-2小时)
   - 实现坐标转换
   - 实现方框尺寸计算
   - 测试转换逻辑

4. **阶段4: 渲染层** (1-2小时)
   - 实现ImGui绘制
   - 集成到m.cpp
   - 测试完整流程

5. **阶段5: 优化与调试** (1-2小时)
   - 添加详细日志
   - 性能优化
   - 错误处理完善

### 10.2 总预估时间

**总计**: 6-11小时

---

## 十一、参考资料

### 11.1 项目内文档

- `07-小工具分析/03-UnityCrossFire-DLL完整功能分析.md`
- `07-小工具分析/04-UnityCrossFire-技术实现详解.md`
- `07-小工具分析/05-UnityCrossFire-快速参考手册.md`

### 11.2 关键地址参考

| 内容 | 地址 | 说明 |
|------|------|------|
| GameManager字符串 | 0x100538e4 | 类名 |
| get_position | 0x10054674 | Transform方法 |
| Camera.get_main | 0x100546c4 | 摄像机方法 |
| ScreenToClient | 0x10051154 | IAT函数 |

### 11.3 外部资源

- Unity IL2CPP API文档
- ImGui文档
- DirectX 11文档

---

**文档结束**

**下一步**: 调用writing-plans skill创建详细的实施计划
