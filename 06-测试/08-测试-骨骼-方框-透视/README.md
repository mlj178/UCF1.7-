# ESP 项目使用指南

## 🎯 项目说明

这是一个用于 Unity IL2CPP 游戏的 ESP (Extra Sensory Perception) 外挂框架，支持：
- 方框透视
- 骨骼透视
- 距离显示
- 血量显示

## 📋 使用步骤

### 1️⃣ 编译 DLL

```powershell
cd d:\trae_project\ucf1.7-modifier\06-测试\08-测试-骨骼-方框-透视\m
.\build.bat
```

编译成功后会生成 `m.dll` (约 1.2MB)

### 2️⃣ 启动游戏

启动目标游戏 `UnityCrossFire.exe`

### 3️⃣ 注入 DLL

```powershell
cd d:\trae_project\ucf1.7-modifier\06-测试\08-测试-骨骼-方框-透视
python esp_inject.py
```

### 4️⃣ 游戏内操作

注入成功后，使用以下热键：

| 热键 | 功能 |
|------|------|
| **INSERT** | 打开/关闭菜单 |
| **F1** | 切换 ESP 开关 |
| **END** | 卸载 DLL |

### 5️⃣ 查看日志

实时查看日志：
```powershell
Get-Content d:\trae_project\ucf1.7-modifier\06-测试\08-测试-骨骼-方框-透视\m\esp_log.txt -Wait
```

## ⚙️ 配置文件

配置文件：`m\esp_config.ini`

```ini
[ESP]
Enabled=1
ShowBox=1
ShowSkeleton=0
ShowDistance=1
ShowHealth=0

[Hotkeys]
OpenMenu=45      ; VK_INSERT
Uninject=35      ; VK_END
ToggleESP=112    ; VK_F1

[Colors]
EnemyR=1.00
EnemyG=0.00
EnemyB=0.00
EnemyA=1.00

[Render]
BoxThickness=1.00
SkeletonThickness=1.50
MaxDistance=500.00
```

## 🛠️ 依赖要求

- **Python 3.x**
- **Frida**: `pip install frida`
- **psutil**: `pip install psutil`
- **MinGW32**: 用于编译 C++ 代码

## 📁 项目结构

```
m/
├── core/          # 核心基础设施
├── hook/          # D3D11 和输入 Hook
├── il2cpp/        # IL2CPP API 桥接
├── game/          # 游戏逻辑
├── render/        # ESP 渲染
├── imgui/         # ImGui 库
├── minhook/       # MinHook 库
├── m.cpp          # DLL 入口
└── build.bat      # 编译脚本
```

## ⚠️ 注意事项

1. **仅用于学习和研究目的**
2. 使用前请确保游戏已启动
3. 如遇崩溃，检查 `esp_log.txt` 日志文件
4. 首次运行会创建默认配置文件

## 🐛 故障排查

### 问题：找不到游戏进程
- 确保游戏已启动
- 检查进程名是否为 `UnityCrossFire.exe`

### 问题：DLL 加载失败
- 检查是否编译成功
- 查看日志文件中的错误信息
- 确保使用正确的 32 位编译器

### 问题：游戏崩溃
- 查看 `esp_log.txt` 中的错误日志
- 检查 IL2CPP API 是否正确初始化
- 确认游戏使用的是 IL2CPP 而非 Mono
