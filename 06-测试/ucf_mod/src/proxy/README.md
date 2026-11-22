# src/proxy · winhttp.dll 代理外壳

> 这个目录是 **2026-11-22 从二进制反推复原** 的源码。
> 原件（`payload/winhttp.dll`）是仓库外编的，源码没进 git，也没留 .c。

## 它是什么

游戏会 `LoadLibrary("winhttp.dll")`。把同名 DLL 放进游戏目录，Windows 的
DLL 搜索顺序会优先加载它。它做两件事：

1. **转发**：把 92 个 `WinHttp*` 导出原样转给同目录的 `winhttp_orig.dll`
   （= 系统 `winhttp.dll` 的 32 位副本）。游戏完全察觉不到。
2. **上钩**：`DllMain` 里起一个线程，`Sleep(200)` 后
   `LoadLibraryA("<游戏目录>\\ucf_mod\\ucf_mod.dll")`。失败就
   往 `<游戏目录>\\ucf_mod\\ucf_mod.log` 追加一句 `proxy: failed to load plugin`。

插件本身还要求环境变量 `UCF_MOD=1`（控制台启动游戏时注入）才工作，那是 `plugin.c` 的事。

## 复原依据

| 证据 | 内容 |
|---|---|
| COFF 符号表 | 876 条，未 strip；可见 `_DllMain@12`、`_loader@4`、`.file proxy.c` |
| 调试节 | `.debug_info` `.debug_line` `.debug_str` `.debug_frame` `.debug_aranges` 全在 |
| 导出表 | 92 条，全部是 `Forwarder RVA -- winhttp_orig.<同名>`（objdump -p 可复现） |
| 导入表 | 仅 KERNEL32 + msvcrt；proxy 用到 GetModuleFileNameA / DisableThreadLibraryCalls / CreateThread / LoadLibraryA / CreateFileA / SetFilePointer / WriteFile / CloseHandle |
| `.text` | 6144 字节，实际代码只有 DllMain + loader 两个函数 |
| 日志文字 | 从 `mov DWORD PTR [esp+0x230], imm32` 的立即数逐字节还原为 `proxy: failed to load plugin\r\n` |

**能复原到什么程度**：导出表、加载路径、Sleep 时长、日志文字、函数名都能对上；
原始变量名、注释、排版无法复原（DWARF 里没有 proxy.c 的行号表，只有 libgcc 的）。
所以这份 `proxy.c` 是"行为等价重写"，不是逐字还原。

## 怎么编

```powershell
# 默认：从 payload/winhttp.dll 取导出表 → 重建 winhttp.def → 编译 → 校验
.\build_proxy.ps1

# 也可以拿系统 winhttp 当参考（导出名一致）
.\build_proxy.ps1 -Ref 'C:\Windows\SysWOW64\winhttp.dll'
```

产物落在 `../../build/proxy/winhttp.dll`，校验通过会打印 `[OK] 导出表一致`。

## 校验（编完自己看一眼）

```powershell
& 'D:\Program Files\mingw32\bin\objdump.exe' -p '..\..\build\proxy\winhttp.dll' |
    Select-String 'Forwarder RVA'      # 应为 92 行，全部指向 winhttp_orig.*
```

## 和原件的差异

| 项 | 原件 | 复原版 |
|---|---|---|
| 大小 | 51,603 B | 51,547 B |
| 导出 | 92 个转发 → winhttp_orig.* | 92 个转发 → winhttp_orig.*（一致） |
| 导入 DLL | KERNEL32 / msvcrt | KERNEL32 / msvcrt |
| 行为 | 加载 ucf_mod.dll，失败写日志 | 同 |

**替换前请务必先在一份游戏副本上验一遍**：把 `winhttp_orig.dll` 摆好，
用控制台带 `UCF_MOD=1` 启动，确认 `ucf_mod.log` 里插件正常起来。
