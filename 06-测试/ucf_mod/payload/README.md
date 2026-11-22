# payload · 部署弹药库

> 本目录存放**部署到游戏目录**所需的全部文件。
> 这些文件在工程端原本没有副本 —— 只存在于游戏目录里，且没进 git（`06-测试/ucf_mod/.gitignore` 里有 `*.dll`）。
> 2026-11-22 从部署端一次性抢救回来，逐字节校验后入库。

## 部署时会用到的文件

| 文件 | 大小 | 用途 |
|---|---|---|
| `winhttp.dll` | 51,603 B | 代理加载器。游戏启动时被系统加载，遍历 92 个导出转发给 `winhttp_orig.dll`，并 `CreateThread` 拉起 `ucf_mod\ucf_mod.dll` |
| `ucf_mod/ucf_mod.dll` | 370,918 B | 插件本体（与 `build\ucf_mod.dll` 同一份，sha256 见 MANIFEST.json） |
| `ucf_mod/uninstall.ps1` | 2,495 B | 卸载脚本（白名单删除，不碰 markers/backup） |
| `ucf_mod/README.txt` | 6,576 B | 给最终用户的说明 |

## 只存档、**不参与部署**的文件

| 文件 | 说明 |
|---|---|
| `_rescue/level9.orig` | 192,140 B，MD5 `89c56148…`。**唯一一份未打补丁的 level9**（两份游戏目录里的 level9 都是打完补丁的 192,144 B / `b0f8db1d…`）。卸载时还原场景要用它 |
| `ucf_mod/_deploy_record_2026-11-16.json` | 2026-11-16 的部署记录，里面记的 dll 是 240,960 B 的旧版，**已过期**，只作历史留档 |

## 不在本目录、部署时才现取的

| 文件 | 来源 |
|---|---|
| `winhttp_orig.dll` | 部署时从目标机 `%WINDIR%\SysWOW64\winhttp.dll` 复制（本机实测 MD5 `2eada8c3…`，与游戏目录里那份逐字节一致）。**绝不能随包发**，各人 Windows 版本不同 |
| `ucf_mod/ucf_mod.json` | 不带。缺文件时 DLL 全部走内置默认（`src/cfg.c`），由控制台首次保存时生成 |

## 明确不属于本 mod、不要部署的

- `baselib.dll`（392,792 B）—— 导入表只有 WS2_32/KERNEL32，与 ucf_mod 无关
- `InjectDll.exe`（17,920 B）—— 字符串自述 "UnityCrossFire Cheat DLL Injector v1.0"，PDB 路径 `D:\Cscore\InjectDll\Release\`，是另一个已消失的工程留下的
- `esp_config.ini` / `imgui.ini` / `*.log` —— 运行时产物

## 注意

- `MANIFEST.json` 是脚本生成的采集清单（sha256 / 来源 / 时间），**不要手改**。
- 本目录体积约 620 KB（含 level9 存档），适合直接进 git；但 `.gitignore` 的 `*.dll` 会挡住它，需要加例外（见 `06-测试/ucf_mod/.gitignore`）。
- `winhttp.dll` 目前**只有这一份真身**。源码已丢失，2026-11-22 起在 `src/proxy/` 下复原。
