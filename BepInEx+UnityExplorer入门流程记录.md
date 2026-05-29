# BepInEx + UnityExplorer 入门流程记录

## 一、游戏信息

### 1.1 游戏基本信息
- **游戏名称**：UnityCrossFire 1.7.1
- **游戏路径**：`D:\BaiduNetdiskDownload\UnityCrossFire1.7.1\UnityCrossFire1.7.1`
- **游戏引擎**：Unity 2020.3.30f1c1
- **游戏位数**：32位（x86）
- **游戏类型**：FPS（第一人称射击游戏）
- **运行时**：.NET 6.0.7
- **系统平台**：Windows 10 64-bit

### 1.2 游戏架构
- **脚本后端**：IL2CPP
- **核心DLL**：GameAssembly.dll
- **管理器DLL**：UnityEngine.CoreModule.dll
- **游戏程序集**：Assembly-CSharp.dll（IL2CPP互操作版本）

---

## 二、工具信息

### 2.1 BepInEx

#### 基本信息
- **工具名称**：BepInEx
- **工具版本**：6.0.0-be.755+3fab71a（预发布版）
- **GitHub地址**：https://github.com/BepInEx/BepInEx
- **下载地址**：https://github.com/BepInEx/BepInEx/releases
- **下载版本**：BepInEx-Unity.IL2CPP-win-x86-6.0.0-be.755+3fab71a
- **构建提交**：3fab71a1914132a1ce3a545caf3192da603f2258
- **下载日期**：2026-05-28

#### 版本选择
- **BepInEx 5.x**：适用于Unity Mono游戏
- **BepInEx 6.x**：适用于IL2CPP游戏（BepInEx IL2CPP）

#### 安装位置
```
UnityCrossFire1.7.1/
├── UnityCrossFire.exe
├── UnityCrossFire_Data/
├── BepInEx/              ← BepInEx文件夹
│   ├── config/           ← 配置文件
│   ├── plugins/          ← 插件文件夹
│   ├── patchers/         ← 补丁文件夹
│   ├── interop/          ← 互操作文件夹
│   └── LogOutput.log     ← 日志文件
├── doorstop_config.ini   ← 启动配置（IL2CPP）
└── winhttp.dll           ← 注入DLL
```

### 2.2 UnityExplorer

#### 基本信息
- **工具名称**：UnityExplorer
- **工具版本**：4.13.6
- **GitHub地址**：https://github.com/sinai-dev/UnityExplorer
- **下载地址**：https://github.com/sinai-dev/UnityExplorer/releases
- **下载版本**：UnityExplorer.BepInEx.Unity.IL2CPP.CoreCLR
- **下载日期**：2026-05-28
- **依赖库**：UniverseLib 1.6.2

#### 功能特性
- **对象浏览器**：查看所有GameObject、Component
- **场景浏览器**：查看场景层级结构
- **Inspector**：查看和修改对象属性
- **C#交互**：执行C#代码片段
- **反射工具**：查看类、方法、字段信息

---

## 三、安装流程

### 3.1 准备工作

#### 步骤1：确认游戏架构
```
方法1：查看游戏文件夹
- 如果有 GameAssembly.dll → IL2CPP游戏
- 如果有 Assembly-CSharp.dll → Mono游戏

方法2：使用工具检测
- 使用 CFF Explorer 或 PE-binder 查看
```

#### 步骤2：下载BepInEx
```
1. 访问 GitHub：https://github.com/BepInEx/BepInEx/releases
2. 选择对应版本：
   - IL2CPP游戏：BepInEx_UnityIL2CPP_x64_X.X.XX.X.zip
   - Mono游戏：BepInEx_UnityMono_x64_X.X.XX.X.zip
3. 下载最新稳定版
```

#### 步骤3：下载UnityExplorer
```
1. 访问 GitHub：https://github.com/sinai-dev/UnityExplorer/releases
2. 选择对应版本：
   - IL2CPP游戏：UnityExplorer.BepInEx.IL2CPP.Core.zip
   - Mono游戏：UnityExplorer.BepInEx.Mono.Core.zip
3. 下载最新版本
```

### 3.2 安装BepInEx

#### 步骤1：解压BepInEx
```
1. 将下载的BepInEx压缩包解压
2. 将解压后的文件复制到游戏根目录
   - BepInEx文件夹
   - doorstop_config.ini（IL2CPP）
   - winhttp.dll
```

#### 步骤2：首次运行
```
1. 启动游戏 UnityCrossFire.exe
2. 等待BepInEx初始化（会生成必要的文件夹和文件）
3. 关闭游戏
4. 检查 BepInEx/LogOutput.log 确认安装成功
```

### 3.3 安装UnityExplorer

#### 步骤1：解压UnityExplorer
```
1. 将下载的UnityExplorer压缩包解压
2. 找到插件DLL文件（如：UnityExplorer.BepInEx.IL2CPP.dll）
```

#### 步骤2：安装插件
```
1. 将DLL文件复制到 BepInEx/plugins/ 文件夹
2. 如果有依赖文件（如：mcs.dll），也一并复制
```

#### 步骤3：验证安装
```
1. 启动游戏
2. 按 F7 打开UnityExplorer界面（默认快捷键）
3. 如果能看到界面，说明安装成功
```

---

## 四、使用流程

### 4.1 启动游戏

#### 正常启动
```
1. 直接运行 UnityCrossFire.exe
2. BepInEx会自动注入
3. UnityExplorer会自动加载
```

#### 查看日志
```
日志位置：BepInEx/LogOutput.log
日志内容：
- BepInEx加载信息
- 插件加载信息
- 错误和警告信息
```

### 4.2 使用UnityExplorer

#### 打开界面
```
快捷键：F7（默认）
功能：
- 对象浏览器（Object Explorer）
- 场景浏览器（Scene Explorer）
- Inspector
- C#交互（REPL）
```

#### 对象浏览器
```
功能：查看所有GameObject和Component
使用：
1. 在搜索框输入对象名称
2. 点击对象查看详细信息
3. 可以修改属性值
```

#### 场景浏览器
```
功能：查看场景层级结构
使用：
1. 展开场景树
2. 选择GameObject
3. 查看其Component
```

#### Inspector
```
功能：查看和修改对象属性
使用：
1. 选择对象
2. 查看字段和属性
3. 直接修改数值
```

#### C#交互
```
功能：执行C#代码片段
示例：
// 查找对象
var obj = GameObject.Find("Player");
// 修改属性
obj.transform.position = new Vector3(0, 0, 0);
// 调用方法
obj.SetActive(false);
```

### 4.3 常用操作

#### 查找对象
```
方法1：对象浏览器搜索
方法2：场景浏览器查找
方法3：C#代码查找
  var obj = GameObject.Find("ObjectName");
  var objs = GameObject.FindGameObjectsWithTag("Tag");
```

#### 修改属性
```
方法1：Inspector直接修改
方法2：C#代码修改
  obj.GetComponent<ComponentType>().property = value;
```

#### 调用方法
```
使用C#交互：
  obj.GetComponent<ComponentType>().Method();
```



## 六、遇到的问题及解决方案

### 5.1 安装问题

#### 问题1：游戏无法启动
```
原因：
- BepInEx版本不匹配
- 游戏位数不匹配（32位/64位）

解决方案：
- 确认游戏位数（使用CFF Explorer）
- 下载对应位数的BepInEx
```

#### 问题2：UnityExplorer界面不显示
```
原因：
- 插件未正确加载
- 快捷键冲突
- 游戏架构不匹配

解决方案：
- 检查 BepInEx/LogOutput.log 是否有错误
- 尝试其他快捷键（可在配置文件修改）
- 确认下载了正确版本（IL2CPP/Mono）
```

#### 问题3：插件加载失败
```
原因：
- DLL文件缺失
- 依赖库缺失
- 版本不兼容

解决方案：
- 检查是否复制了所有文件
- 检查依赖库（如：mcs.dll）
- 更新到最新版本
```

### 5.2 使用问题

#### 问题1：找不到对象
```
原因：
- 对象名称错误
- 对象未激活
- 场景未加载

解决方案：
- 使用场景浏览器查找
- 确认对象是否激活
- 确认当前场景
```

#### 问题2：无法修改属性
```
原因：
- 属性只读
- 属性类型不匹配
- 权限问题

解决方案：
- 使用反射修改私有字段
- 确认属性类型
- 使用C#代码修改
```

#### 问题3：游戏崩溃
```
原因：
- 修改了关键数据
- 调用了错误的方法
- 内存访问错误

解决方案：
- 谨慎修改关键属性
- 备份游戏存档
- 查看日志定位问题
```

---

## 六、进阶技巧

### 6.1 自定义配置

#### BepInEx配置
```
配置文件：BepInEx/config/BepInEx.cfg
可配置项：
- 日志级别
- 插件加载顺序
- 启动参数
```

#### UnityExplorer配置
```
配置文件：BepInEx/config/sinai.dev.UnityExplorer.cfg
可配置项：
- 快捷键
- 界面样式
- 搜索选项
```

### 6.2 开发插件

#### 创建插件项目
```
1. 创建C#类库项目
2. 引用 BepInEx.dll
3. 引用 UnityEngine.dll
4. 编写插件代码
```

#### 插件模板
```csharp
using BepInEx;
using BepInEx.Logging;

[BepInPlugin("com.example.plugin", "MyPlugin", "1.0.0")]
public class MyPlugin : BaseUnityPlugin
{
    private static ManualLogSource Log;
    
    void Awake()
    {
        Log = Logger;
        Log.LogInfo("Plugin loaded!");
    }
    
    void Update()
    {
        // 插件逻辑
    }
}
```

### 6.3 与Frida配合使用

#### 信息收集
```
使用UnityExplorer：
- 查找对象名称和路径
- 查看字段偏移
- 了解对象结构

使用Frida：
- Hook方法
- 修改内存
- 实现功能
```

#### 工作流程
```
1. 使用UnityExplorer查找目标对象
2. 记录对象名称、路径、字段名
3. 使用Il2CppDumper获取RVA地址
4. 使用Frida编写Hook脚本
5. 测试验证功能
```

---

## 七、参考资源

### 7.1 官方文档
- BepInEx Wiki：https://github.com/BepInEx/BepInEx/wiki
- UnityExplorer Wiki：https://github.com/sinai-dev/UnityExplorer/wiki

### 7.2 教程资源
- BepInEx安装教程：待补充
- UnityExplorer使用教程：待补充

### 7.3 相关工具
- **Il2CppDumper**：IL2CPP逆向工具
- **dnSpy**：.NET反编译工具（Mono游戏）
- **Frida**：动态插桩工具
- **CFF Explorer**：PE文件查看工具

---

## 八、版本历史

### 8.1 工具版本记录
| 工具 | 版本 | 下载日期 | 备注 |
|------|------|---------|------|
| BepInEx | 6.0.0-be.755+3fab71a | 2026-05-28 | IL2CPP x86预发布版 |
| UnityExplorer | 4.13.6 | 2026-05-28 | BepInEx.Unity.IL2CPP.CoreCLR |
| UniverseLib | 1.6.2 | 2026-05-28 | UnityExplorer依赖库 |

### 8.2 游戏版本记录
| 游戏 | 版本 | 测试日期 | 备注 |
|------|------|---------|------|
| UnityCrossFire | 1.7.1 | 2026-05-28 | Unity 2020.3.30f1c1, IL2CPP, 32位 |

### 8.3 安装文件清单

#### BepInEx核心文件
```
BepInEx/
├── core/                          ← 核心库
│   ├── BepInEx.Core.dll
│   ├── BepInEx.Unity.IL2CPP.dll
│   ├── Il2CppInterop.Runtime.dll
│   └── ... (其他依赖)
├── interop/                       ← IL2CPP互操作程序集
│   ├── Assembly-CSharp.dll        ← 游戏主程序集
│   ├── UnityEngine.CoreModule.dll
│   └── ... (其他Unity模块)
├── plugins/                       ← 插件文件夹
│   └── sinai-dev-UnityExplorer/
│       ├── UnityExplorer.BIE.Unity.IL2CPP.CoreCLR.dll
│       ├── UniverseLib.BIE.IL2CPP.Interop.dll
│       └── data.cfg
├── config/                        ← 配置文件夹
│   ├── BepInEx.cfg
│   └── com.sinai.unityexplorer.cfg
└── LogOutput.log                  ← 日志文件
```

#### 启动配置文件
```
.doorstop_version                  ← Doorstop版本标记
winhttp.dll                        ← 注入DLL（IL2CPP）
```

---

## 九、总结

### 9.1 优点
- **可视化操作**：直观查看和修改对象
- **实时调试**：无需重启游戏即可测试
- **信息收集**：快速获取对象和字段信息
- **C#交互**：灵活执行代码片段

### 9.2 局限性
- **仅限Unity游戏**：不适用于其他引擎
- **需要注入**：可能被反作弊检测
- **性能影响**：可能影响游戏性能
- **学习曲线**：需要了解Unity架构

### 9.3 适用场景
- **逆向分析**：了解游戏结构
- **功能开发**：辅助开发修改器
- **调试测试**：快速测试修改效果
- **学习研究**：学习Unity游戏开发

### 9.4 实际测试结果

#### 安装成功确认
```
✅ BepInEx 6.0.0-be.755 启动成功
✅ UnityExplorer 4.13.6 加载成功
✅ UniverseLib 1.6.2 初始化成功
✅ IL2CPP互操作程序集生成成功
✅ 游戏正常运行，无崩溃
```

#### 日志关键信息
```
[Message: Preloader] BepInEx 6.0.0-be.755 - UnityCrossFire
[Info   :   BepInEx] Running under Unity 2020.3.30f1c1
[Info   :   BepInEx] Process bitness: 32-bit (x86)
[Info   :   BepInEx] 1 plugin to load
[Info   :   BepInEx] Loading [UnityExplorer 4.13.6]
[Message:UnityExplorer] UnityExplorer 4.13.6 initializing...
```


---

**文档创建时间**：2026-05-28
**文档版本**：v2.0
**最后更新时间**：2026-05-28
**状态**：✅ 所有信息已补充完整
