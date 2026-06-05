# D3D11 Hook + IL2CPP 开发经验总结

## 📅 日期
2026-05-31

## 🎯 项目背景
- **项目**：Unity IL2CPP游戏透视功能（ESP）
- **游戏**：UnityCrossFire 1.7.1（32位，IL2CPP）
- **技术栈**：C++ DLL注入 + D3D11 Hook + ImGui + IL2CPP API

---

## 🚨 遇到的问题与解决方案

### 问题1：游戏闪退 - IL2CPP API调用约定错误

#### 🔴 现象
```
[22:04:57.292] [ESP] [IL2CPP] GetClass: calling function at 0x62CC7EB0
（之后游戏直接闪退，无后续日志）
```

#### 🔍 原因分析
**IL2CPP API使用 `__stdcall` 调用约定**，而代码中使用的是默认的 `__cdecl`。

**调用约定不匹配导致的问题：**
1. 栈不平衡
2. 参数传递错误
3. 函数返回后栈指针错误
4. 程序直接崩溃

#### ✅ 解决方案

**修改前（错误）：**
```cpp
typedef Il2CppClass* (*FnType)(const char*, const char*);
```

**修改后（正确）：**
```cpp
typedef Il2CppClass* (__stdcall *FnType)(const char*, const char*);
```

**所有IL2CPP API函数指针都需要使用 `__stdcall`：**
```cpp
、

#### 📚 知识点
- **Windows x86**：IL2CPP导出函数使用 `__stdcall`（WINAPI）
- **Windows x64**：只有一种调用约定，不需要指定
- **MinGW/GCC**：支持 `__stdcall` 关键字
- **MSVC**：支持 `__stdcall` 或 `WINAPI` 宏

---

### 问题2：游戏窗口变得非常小

#### 🔴 现象
```
[22:04:54.293] [ESP] Viewport: num=1 w=f h=f x=f y=f
```
游戏窗口变成约181x1像素，几乎看不见。

#### 🔍 原因分析

**问题链条：**
```
1. DLL注入 → Hook Present
2. RSGetViewports失败 → Viewport尺寸为0
3. ImGui使用DisplaySize(0, 0) → 窗口异常
4. Unity检测到窗口变化 → 保存到注册表
5. 注册表被修改为181x1 → 窗口变得非常小
```

**具体原因：**
1. `RSGetViewports` 返回的Viewport宽度和高度为0或异常值
2. ImGui的 `DisplaySize` 设置为错误值
3. Unity通过PlayerPrefs将错误的窗口大小保存到注册表
4. 注册表路径：`HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire`

#### ✅ 解决方案

```
**方案3：删除注册表中的错误设置**
```batch
# 删除整个键（推荐）
reg delete "HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire" /f

# 或删除特定的分辨率设置
reg delete "HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire" /v "Screenmanager Resolution Width_h182942802" /f
reg delete "HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire" /v "Screenmanager Resolution Height_h2627697771" /f
```

**方案4：手动设置正确的分辨率**

```batch
# 设置为1200x900（4:3）
reg add "HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire" /v "Screenmanager Resolution Width_h182942802" /t REG_DWORD /d 1200 /f
reg add "HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire" /v "Screenmanager Resolution Height_h2627697771" /t REG_DWORD /d 900 /f
reg add "HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire" /v "Screenmanager Fullscreen mode_h3630240806" /t REG_DWORD /d 0 /f
```

#### 📚 知识点
- **Unity PlayerPrefs**：在Windows上存储在注册表中
- **注册表路径**：`HKCU\SOFTWARE\公司名\游戏名`
- **分辨率键名**：Unity使用哈希后的键名，如 `Screenmanager Resolution Width_h182942802`
- **Viewport获取时机**：需要在D3D11设备上下文正确初始化后才能获取

---

### 问题3：重启游戏无法恢复窗口大小

#### 🔴 现象
删除游戏目录下的配置文件后，重启游戏窗口仍然很小。

#### 🔍 原因分析
**Unity的设置存储在注册表中，而不是文件中！**

- `PlayerData.dat`：游戏存档数据
- 注册表：窗口大小、音量、画质等设置

#### ✅ 解决方案
**必须删除注册表中的设置才能恢复！**

```batch
reg delete "HKCU\SOFTWARE\Alexander_GaGa\UnityCrossFire" /f
```

---