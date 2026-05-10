# IL2CPP 逆向的正确流程

## 前置知识：GameAssembly.dll vs Assembly-CSharp.dll

| | GameAssembly.dll | Assembly-CSharp.dll |
|------|------|------|
| 格式 | Native C++ 机器码 | .NET 托管 IL 字节码 |
| 来源 | IL2CPP 编译产物 | Unity C# 脚本编译产物 |
| 内容 | 游戏逻辑的原生代码 | 游戏逻辑的 IL 中间代码 |
| 可读性 | 极低，函数名是 sub_xxxxx | 极高，类名方法名全保留 |
| 分析工具 | IDA Pro | dnSpy / ILSpy |
| 适用场景 | IL2CPP 游戏 | Mono 游戏 |

Unity 游戏有两种编译模式：

- **Mono 模式**：产出 Assembly-CSharp.dll，用 dnSpy 直接看，类名方法名一目了然
- **IL2CPP 模式**：产出 GameAssembly.dll，必须用 IDA + dump.cs 才能还原符号

判断自己的游戏是哪种模式：如果游戏目录里有 GameAssembly.dll 且体积很大（几十MB以上），就是 IL2CPP。

---

## IL2CPP 逆向完整流程

### 第一步：从手机提取 GameAssembly.dll

GameAssembly.dll 是 IL2CPP 游戏的核心文件，包含了所有游戏逻辑的机器码。

**提取路径：**

**提取方法：**

**注意：** 安卓上的文件叫 `libil2cpp.so`，PC 上叫 `GameAssembly.dll`，本质是同一个东西，只是平台不同格式不同。

---

### 第二步：从手机提取 global-metadata.dat

这个文件存储了 IL2CPP 的所有元数据（类名、方法名、字符串等），是还原符号的关键。

**提取路径：**

**提取方法：**

**验证文件是否正确：**

- 用十六进制编辑器打开，前4个字节应该是 `AF 1B B1 FA`（global-metadata 的魔数）
- 如果前4个字节不是这个，说明被加密了，需要先解密

---

### 第三步：用 Il2CppDumper 生成 dump.cs

Il2CppDumper 会读取 GameAssembly.dll + global-metadata.dat，还原出完整的类信息，输出 dump.cs 文件。

**下载 Il2CppDumper：**

**使用方法：**

**输出文件说明：**

| 文件 | 内容 |
|------|------|
| **dump.cs** | 最重要！完整的类定义，包含类名、方法名、字段名、偏移地址 |
| script.json | 函数地址和偏移的 JSON 格式，配合 IDA 脚本使用 |
| stringliteral.json | 游戏中的字符串常量。 |

---

### 第四步：在 dump.cs 里搜到目标函数偏移，去 IDA 里跳转

**操作步骤：**

1. 在 dump.cs 里搜索你感兴趣的类名或方法名（比如搜 `OnSpecialBtnDown`）
2. 找到方法后面的偏移地址（比如 `// 0xB64240`）
3. 打开 IDA，加载 GameAssembly.dll
4. 按 **G** 键（Jump to address），输入 `base + 0xB64240`
5. IDA 会跳转到对应的汇编代码位置

**IDA 加载时的注意事项：**

- 选择 ARM64 架构（安卓）/ x64 架构（PC）。32位游戏用32位的IDA，64位游戏用64位IDA
- 等待 IDA 自动分析完成（可能需要几分钟到十几分钟）
- 分析完成后函数会自动识别出来

---

### 第五步：对照 dump.cs 看懂 IDA 里的函数

**批量重命名（进阶）：**

Il2CppDumper 输出的 `script.json` 可以配合 IDA Python 脚本批量重命名。用这个脚本ida_with_struct_py3.py。

这样 IDA 里所有函数都会自动变成可读的名字。

---

## 完整流程图

```
手机上的游戏 APK
    │
    ├── lib/arm64/libil2cpp.so          ──→  丢进 IDA 分析
    │                                         │
    └── assets/bin/Data/Managed/
        Metadata/global-metadata.dat   ──→  配合 Il2CppDumper
                                              │
                                              ↓
                                         生成 dump.cs
                                              │
                                              ↓
                                    搜索类名/方法名 → 得到偏移地址
                                              │
                                              ↓
                                    IDA 按 G 跳转到偏移地址
                                              │
                                              ↓
                                    对照 dump.cs 理解函数逻辑
                                              │
                                              ↓
                                    提取偏移 → 写 Frida 脚本 Hook
```



### Q：dump.cs 里的偏移地址和 IDA 里对不上？

- 检查 IDA 加载时选择的基址是否正确
- Il2CppDumper 输出的地址可能是 RVA（相对虚拟地址），需要加上 GameAssembly.dll 的基址
- 游戏更新后偏移会变化，需要重新提取和 dump





