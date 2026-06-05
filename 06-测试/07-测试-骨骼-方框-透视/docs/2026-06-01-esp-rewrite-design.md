# ESP系统完全重写设计文档

**创建日期**: 2026-06-01  
**项目**: UnityCrossFire 1.7 ESP功能  
**方案**: 完全重写（参考三个开源项目）  

---

## 一、设计目标

### 1.1 核心目标
- ✅ 使用MinHook替代手动Hook（稳定、可靠）
- ✅ 添加ResizeBuffers Hook（窗口大小变化处理）
- ✅ 面向对象的IL2CPP封装（参考frida-il2cpp-bridge）
- ✅ 模块化架构（参考DX11-ImGui-Internal-Hook）
- ✅ 配置文件和热键系统

### 1.2 参考项目
1. **DX11-ImGui-Internal-Hook**: 模块化架构、命名空间设计
2. **Universal-Dear-ImGui-Hook**: 完善的Hook管理、RenderTarget处理
3. **frida-il2cpp-bridge**: 面向对象的IL2CPP封装

---

## 二、目录结构

```
m/
├── core/                      # 核心基础设施
│   ├── hook_manager.h/cpp     # MinHook封装
│   ├── logger.h/cpp           # 日志系统
│   └── config.h/cpp           # 配置管理
│
├── hook/                      # Hook模块
│   ├── d3d11_hook.h/cpp       # D3D11 Hook（Present、ResizeBuffers）
│   └── input_hook.h/cpp       # 输入Hook（WndProc）
│
├── il2cpp/                    # IL2CPP桥接
│   ├── il2cpp_api.h/cpp       # API封装
│   └── il2cpp_types.h         # 类型定义
│
├── game/                      # 游戏逻辑
│   ├── game_manager.h/cpp     # 游戏管理器
│   ├── player.h/cpp           # 玩家数据
│   └── coord_converter.h/cpp  # 坐标转换
│
├── render/                    # 渲染模块
│   ├── esp_renderer.h/cpp     # ESP渲染
│   └── menu.h/cpp             # 菜单系统
│
├── imgui/                     # ImGui库
├── minhook/                   # MinHook库
├── m.cpp                      # DLL入口
└── build.bat                  # 编译脚本
```

---

## 三、核心模块设计

### 3.1 Hook Manager（MinHook封装）

**文件**: `core/hook_manager.h`

```cpp
#pragma once
#include <Windows.h>

namespace HookManager {
    bool Initialize();
    void Shutdown();
    
    bool CreateHook(void* target, void* detour, void** original);
    bool EnableHook(void* target);
    bool DisableHook(void* target);
    bool RemoveHook(void* target);
    void EnableAllHooks();
    void DisableAllHooks();
}
```

**实现要点**：
- 使用MinHook库（`MinHook.h`）
- 统一的Hook管理接口
- 支持启用/禁用/移除Hook
- 错误检查和日志记录

---

### 3.2 Logger系统

**文件**: `core/logger.h`

```cpp
#pragma once
#include <stdio.h>

namespace Logger {
    void Initialize(const char* logPath);
    void Shutdown();
    
    void Log(const char* tag, const char* fmt, ...);
    void LogError(const char* tag, const char* fmt, ...);
    void LogWarning(const char* tag, const char* fmt, ...);
}

#define LOG(tag, fmt, ...) Logger::Log(tag, fmt, ##__VA_ARGS__)
#define LOG_ERROR(tag, fmt, ...) Logger::LogError(tag, fmt, ##__VA_ARGS__)
#define LOG_WARN(tag, fmt, ...) Logger::LogWarning(tag, fmt, ##__VA_ARGS__)
```

**特性**：
- 文件日志 + 控制台输出
- 带时间戳和标签
- 线程安全（临界区）

---

### 3.3 Config系统

**文件**: `core/config.h`

```cpp
#pragma once

struct ESPConfig {
    bool enabled = true;
    bool showBox = true;
    bool showSkeleton = false;
    bool showDistance = true;
    bool showHealth = false;
    
    int openMenuKey = VK_INSERT;      // 打开菜单热键
    int uninjectKey = VK_END;         // 卸载DLL热键
    int toggleESPKey = VK_F1;         // 开关ESP热键
    
    ImVec4 enemyColor = ImVec4(1.0f, 0.0f, 0.0f, 1.0f);     // 敌人颜色（红色）
    ImVec4 teamColor = ImVec4(0.0f, 1.0f, 0.0f, 1.0f);      // 队友颜色（绿色）
    ImVec4 visibleColor = ImVec4(1.0f, 1.0f, 0.0f, 1.0f);   // 可见颜色（黄色）
    
    float boxThickness = 1.0f;
    float skeletonThickness = 1.5f;
    float maxDistance = 500.0f;       // 最大显示距离
    
    bool LoadFromFile(const char* path);
    bool SaveToFile(const char* path);
};

extern ESPConfig g_Config;
```

**特性**：
- INI文件格式
- 热键配置
- 颜色配置
- 运行时保存/加载

---

### 3.4 D3D11 Hook

**文件**: `hook/d3d11_hook.h`

```cpp
#pragma once
#include <d3d11.h>
#include <dxgi.h>

class D3D11Hook {
public:
    static D3D11Hook& Instance();
    
    bool Initialize();
    void Shutdown();
    
private:
    D3D11Hook() = default;
    ~D3D11Hook() = default;
    
    // Hook函数
    static HRESULT WINAPI Present_Hook(IDXGISwapChain* pSwapChain, UINT SyncInterval, UINT Flags);
    static HRESULT WINAPI ResizeBuffers_Hook(IDXGISwapChain* pSwapChain, UINT BufferCount, 
                                             UINT Width, UINT Height, DXGI_FORMAT NewFormat, UINT SwapChainFlags);
    
    // 原始函数指针
    typedef HRESULT (WINAPI *Present_t)(IDXGISwapChain*, UINT, UINT);
    typedef HRESULT (WINAPI *ResizeBuffers_t)(IDXGISwapChain*, UINT, UINT, UINT, DXGI_FORMAT, UINT);
    
    static Present_t s_OriginalPresent;
    static ResizeBuffers_t s_OriginalResizeBuffers;
    
    // D3D11资源
    static ID3D11Device* s_Device;
    static ID3D11DeviceContext* s_Context;
    static ID3D11RenderTargetView* s_RTV;
    static IDXGISwapChain* s_SwapChain;
    static HWND s_hWnd;
    static bool s_Initialized;
    
    // RenderTarget管理
    static void CreateRenderTarget();
    static void CleanupRenderTarget();
    
    // ImGui初始化
    static bool InitializeImGui();
    static void RenderFrame();
};
```

**关键改进**：
- ✅ ResizeBuffers Hook（窗口大小变化处理）
- ✅ 完善的RenderTarget管理
- ✅ 单例模式
- ✅ 分离初始化和渲染

---

### 3.5 Input Hook

**文件**: `hook/input_hook.h`

```cpp
#pragma once
#include <Windows.h>

class InputHook {
public:
    static InputHook& Instance();
    
    bool Initialize(HWND hWnd);
    void Shutdown();
    
private:
    InputHook() = default;
    ~InputHook() = default;
    
    static WNDPROC s_OriginalWndProc;
    static HWND s_hWnd;
    
    static LRESULT WINAPI WndProc_Hook(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
};
```

**功能**：
- WndProc Hook
- 键盘输入处理
- 菜单开关

---

### 3.6 IL2CPP API（面向对象）

**文件**: `il2cpp/il2cpp_types.h`

```cpp
#pragma once

struct Il2CppClass;
struct MethodInfo;
struct FieldInfo;
struct Il2CppImage;
struct Il2CppAssembly;

namespace IL2CPP {
    struct Vector3 {
        float x, y, z;
    };
    
    struct Vector2 {
        float x, y;
    };
    
    class Class;
    class Method;
    class Field;
    class Object;
}
```

**文件**: `il2cpp/il2cpp_api.h`

```cpp
#pragma once
#include "il2cpp_types.h"

namespace IL2CPP {
    class API {
    public:
        static bool Initialize(HMODULE gameAssembly);
        static void Shutdown();
        
        // Domain操作
        static void* GetDomain();
        static Il2CppAssembly** GetAssemblies(size_t* count);
        static Il2CppImage* GetImage(const char* assemblyName);
        
        // Class操作
        static Il2CppClass* GetClass(const char* assemblyName, const char* namespaceName, const char* className);
        static Il2CppClass* GetClassFromObject(void* obj);
        static const char* GetClassName(Il2CppClass* klass);
        static const char* GetClassNamespace(Il2CppClass* klass);
        
        // Method操作
        static MethodInfo* GetMethod(Il2CppClass* klass, const char* methodName, int argsCount);
        static void* InvokeMethod(MethodInfo* method, void* obj, void** args);
        static const char* GetMethodName(MethodInfo* method);
        
        // Field操作
        static FieldInfo* GetField(Il2CppClass* klass, const char* fieldName);
        static int GetFieldOffset(FieldInfo* field);
        static void* GetFieldValue(void* obj, int offset);
        static void SetFieldValue(void* obj, int offset, void* value);
        
        // Object操作
        static Il2CppClass* GetObjectClass(void* obj);
        
    private:
        static HMODULE s_GameAssembly;
        
        // IL2CPP导出函数指针
        typedef void* (__stdcall *FnDomainGet)();
        typedef Il2CppAssembly** (__stdcall *FnDomainGetAssemblies)(void*, size_t*);
        typedef Il2CppClass* (__stdcall *FnClassFromName)(Il2CppImage*, const char*, const char*);
        typedef MethodInfo* (__stdcall *FnMethodFromName)(Il2CppClass*, const char*, int);
        typedef FieldInfo* (__stdcall *FnFieldFromName)(Il2CppClass*, const char*);
        typedef void* (__stdcall *FnRuntimeInvoke)(MethodInfo*, void*, void**, void**);
        typedef int (__stdcall *FnFieldGetOffset)(FieldInfo*);
        
        static FnDomainGet s_DomainGet;
        static FnDomainGetAssemblies s_DomainGetAssemblies;
        static FnClassFromName s_ClassFromName;
        static FnMethodFromName s_MethodFromName;
        static FnFieldFromName s_FieldFromName;
        static FnRuntimeInvoke s_RuntimeInvoke;
        static FnFieldGetOffset s_FieldGetOffset;
    };
    
    // 面向对象封装
    class Class {
    public:
        Class(Il2CppClass* ptr) : m_Ptr(ptr) {}
        
        const char* GetName() const;
        const char* GetNamespace() const;
        MethodInfo* GetMethod(const char* name, int argsCount);
        FieldInfo* GetField(const char* name);
        
        bool IsValid() const { return m_Ptr != nullptr; }
        Il2CppClass* GetPtr() const { return m_Ptr; }
        
    private:
        Il2CppClass* m_Ptr;
    };
    
    class Method {
    public:
        Method(MethodInfo* ptr) : m_Ptr(ptr) {}
        
        const char* GetName() const;
        void* Invoke(void* obj, void** args);
        
        bool IsValid() const { return m_Ptr != nullptr; }
        MethodInfo* GetPtr() const { return m_Ptr; }
        
    private:
        MethodInfo* m_Ptr;
    };
    
    class Field {
    public:
        Field(FieldInfo* ptr) : m_Ptr(ptr) {}
        
        int GetOffset() const;
        template<typename T>
        T GetValue(void* obj) {
            return API::GetFieldValue(obj, GetOffset());
        }
        
        bool IsValid() const { return m_Ptr != nullptr; }
        FieldInfo* GetPtr() const { return m_Ptr; }
        
    private:
        FieldInfo* m_Ptr;
    };
}
```

**关键改进**：
- ✅ 面向对象设计（Class、Method、Field封装）
- ✅ 完整的API封装
- ✅ 类型安全
- ✅ 错误检查
- ✅ `__stdcall` 调用约定

---

### 3.7 Game Manager

**文件**: `game/game_manager.h`

```cpp
#pragma once
#include "../il2cpp/il2cpp_api.h"
#include <vector>

struct PlayerData {
    void* object;
    IL2CPP::Vector3 position;
    int teamId;
    bool isAlive;
    float health;
    bool isVisible;
};

class GameManager {
public:
    static GameManager& Instance();
    
    bool Initialize();
    void Update();
    
    std::vector<PlayerData> GetAllPlayers();
    PlayerData GetLocalPlayer();
    
private:
    GameManager() = default;
    ~GameManager() = default;
    
    IL2CPP::Class m_GameManagerClass;
    IL2CPP::Method m_GetAllPlayersMethod;
    IL2CPP::Method m_GetLocalPlayerMethod;
    
    bool m_Initialized = false;
};
```

---

### 3.8 Coord Converter

**文件**: `game/coord_converter.h`

```cpp
#pragma once
#include "../il2cpp/il2cpp_api.h"

class CoordConverter {
public:
    static CoordConverter& Instance();
    
    bool Initialize();
    bool WorldToScreen(const IL2CPP::Vector3& world, IL2CPP::Vector2* screen);
    
private:
    CoordConverter() = default;
    ~CoordConverter() = default;
    
    IL2CPP::Class m_CameraClass;
    IL2CPP::Method m_WorldToScreenMethod;
    void* m_MainCamera;
    
    bool m_Initialized = false;
};
```

---

### 3.9 ESP Renderer

**文件**: `render/esp_renderer.h`

```cpp
#pragma once
#include "../game/player.h"
#include "../imgui/imgui.h"

class ESPRenderer {
public:
    static ESPRenderer& Instance();
    
    void Render();
    
private:
    ESPRenderer() = default;
    ~ESPRenderer() = default;
    
    void DrawPlayerESP(const PlayerData& player, const PlayerData& localPlayer);
    void DrawBox(const IL2CPP::Vector2& pos, float width, float height, const ImVec4& color);
    void DrawSkeleton(const std::vector<IL2CPP::Vector3>& bones);
    void DrawDistance(const IL2CPP::Vector2& pos, float distance);
    
    ImVec4 GetPlayerColor(const PlayerData& player, bool isVisible);
};
```

---

### 3.10 Menu系统

**文件**: `render/menu.h`

```cpp
#pragma once

class Menu {
public:
    static Menu& Instance();
    
    void Render();
    void Toggle() { m_Open = !m_Open; }
    bool IsOpen() const { return m_Open; }
    
private:
    Menu() = default;
    ~Menu() = default;
    
    bool m_Open = false;
    
    void RenderMainWindow();
    void RenderSettingsWindow();
};
```

---

## 四、实施计划

### 阶段1：基础设施（Day 1-2）
**任务**：
1. 创建目录结构
2. 集成MinHook库
3. 实现Hook Manager
4. 实现Logger系统
5. 实现Config系统

**验证**：
- MinHook初始化成功
- 日志文件正常输出
- 配置文件加载/保存正常

---

### 阶段2：Hook系统（Day 3）
**任务**：
1. 实现D3D11 Hook（Present、ResizeBuffers）
2. 实现Input Hook（WndProc）
3. ImGui初始化
4. RenderTarget管理

**验证**：
- Present Hook成功
- ResizeBuffers Hook成功
- ImGui正常渲染
- 窗口大小变化正常处理

---

### 阶段3：IL2CPP桥接（Day 4-5）
**任务**：
1. 实现IL2CPP API封装
2. 实现Class、Method、Field封装
3. 添加错误检查
4. 测试API调用

**验证**：
- GetClass成功
- GetMethod成功
- GetField成功
- InvokeMethod成功

---

### 阶段4：游戏逻辑（Day 6-7）
**任务**：
1. 实现GameManager
2. 实现Player数据结构
3. 实现CoordConverter
4. 测试数据获取

**验证**：
- 获取所有玩家成功
- 获取本地玩家成功
- 坐标转换成功

---

### 阶段5：渲染系统（Day 8）
**任务**：
1. 实现ESPRenderer
2. 实现Menu系统
3. 实现方框、骨骼、距离绘制
4. 颜色配置

**验证**：
- 方框绘制正常
- 骨骼绘制正常
- 距离显示正常
- 菜单交互正常

---

### 阶段6：集成测试（Day 9）
**任务**：
1. 整体集成
2. 功能测试
3. Bug修复
4. 性能优化

**验证**：
- 所有功能正常
- 无崩溃
- 性能良好

---

## 五、关键技术点

### 5.1 MinHook集成

**下载MinHook**：
- 从DX11-ImGui-Internal-Hook项目复制 `libs/MinHook` 目录
- 或从官方仓库下载：https://github.com/TsudaKageyu/minhook

**编译配置**：
- 添加MinHook源文件到编译脚本
- 或链接MinHook.lib

---

### 5.2 调用约定

**重要**：所有IL2CPP API必须使用 `__stdcall`

```cpp
// 正确
typedef Il2CppClass* (__stdcall *FnClassFromName)(Il2CppImage*, const char*, const char*);

// 错误（会导致崩溃）
typedef Il2CppClass* (__cdecl *FnClassFromName)(Il2CppImage*, const char*, const char*);
```

---

### 5.3 ResizeBuffers处理

**必须Hook ResizeBuffers**：
- 窗口大小变化时调用
- 需要清理旧的RenderTarget
- 创建新的RenderTarget
- 更新ImGui DisplaySize

---

### 5.4 错误处理

**所有API调用都需要检查**：
```cpp
Il2CppClass* klass = API::GetClass("Assembly-CSharp", "", "GameManager");
if (!klass) {
    LOG_ERROR("IL2CPP", "Failed to get GameManager class");
    return false;
}
```

---

## 六、配置文件示例

**esp_config.ini**:
```ini
[ESP]
Enabled=1
ShowBox=1
ShowSkeleton=0
ShowDistance=1
ShowHealth=0

[Hotkeys]
OpenMenu=45          ; VK_INSERT
Uninject=35          ; VK_END
ToggleESP=112        ; VK_F1

[Colors]
EnemyR=1.0
EnemyG=0.0
EnemyB=0.0
EnemyA=1.0

TeamR=0.0
TeamG=1.0
TeamB=0.0
TeamA=1.0

[Render]
BoxThickness=1.0
SkeletonThickness=1.5
MaxDistance=500.0
```

---

## 七、预期成果

### 7.1 功能完整性
- ✅ 稳定的D3D11 Hook（MinHook）
- ✅ 完善的窗口大小变化处理（ResizeBuffers）
- ✅ 面向对象的IL2CPP封装
- ✅ 模块化架构
- ✅ 配置文件支持
- ✅ 热键系统

### 7.2 代码质量
- ✅ 清晰的模块划分
- ✅ 完善的错误处理
- ✅ 详细的日志记录
- ✅ 类型安全
- ✅ 易于维护和扩展

### 7.3 性能
- ✅ 无明显性能影响
- ✅ 稳定运行
- ✅ 无内存泄漏

---

## 八、风险与应对

### 8.1 IL2CPP API变化
**风险**：不同Unity版本的IL2CPP API可能不同
**应对**：
- 添加版本检测
- 使用通用的API调用方式
- 完善的错误处理

### 8.2 游戏更新
**风险**：游戏更新可能导致偏移变化
**应对**：
- 使用IL2CPP API而非硬编码偏移
- 配置文件支持
- 日志记录便于调试

### 8.3 反作弊检测
**风险**：可能被反作弊检测
**应对**：
- 本地测试环境
- 了解反作弊机制
- 必要时添加保护

---

## 九、总结

本设计文档详细描述了ESP系统的完全重写方案，参考了三个优秀的开源项目，采用了：

1. **MinHook**：稳定可靠的Hook框架
2. **面向对象**：清晰的IL2CPP封装
3. **模块化**：易于维护和扩展的架构
4. **配置系统**：灵活的配置和热键支持

预计开发时间：**9天**

下一步：创建详细的实施计划并开始编码。
