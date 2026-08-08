# UCF2.4 修改器 安装器打包规范（onedir + Inno Setup）

本文档规定 `PyInstaller onedir + Inno Setup` 安装器打包方式，作为《32-打包发布须知.md》单文件（onefile）形态的**替代发布形态**。规范参照外部项目《03-整合包1.2安装器打包规范.md》迁移而来，并按本项目（UCF 修改器）的实际技术栈与既有约定做了适配。

> 适用范围：`全功能整合包2.4/game_modifier/`。后续版本复制本目录时，版本号由整合包目录名动态解析，spec / iss / 构建脚本均无需手工改版本。

## 1. 方案目标

用户拿到一个安装器，安装后具备：

1. 自定义安装路径。
2. 桌面快捷方式、开始菜单快捷方式。
3. 系统卸载项，可从控制面板卸载。
4. 启动后无需 Python 环境即可运行 GUI。
5. 每次启动自动以管理员权限运行（满足 frida attach / DLL 注入需求）。

## 2. 与单文件版的关系

| 形态 | 工具 | 产物 | 适用场景 |
|---|---|---|---|
| 单文件（既有） | PyInstaller onefile | `UCF2.4修改器.exe` | 单文件分发，启动需自解压到 `%TEMP%` |
| 安装器（本文） | PyInstaller onedir + Inno Setup | `UCF2.4修改器安装器.exe` | 目录版，无需每次自解压，便于排查缺文件 |

两种形态**并存**，不互相替代。安装器版作为兼容备用，降低单文件自解压失败（杀软拦截 `%TEMP%` 写入、磁盘空间不足等）的风险。

## 3. 总体流程

```text
PyInstaller onedir
    └── dist_release/UCF2.4修改器/        exe + _internal/
            ↓
Inno Setup 编译 .iss
    └── release/UCF2.4修改器安装器.exe
            ↓
用户运行安装器 → 选路径 → 建快捷方式 → 启动 exe
```

## 4. 构建环境

| 项目 | 要求 |
|---|---|
| 系统 | Windows 10/11 64 位 |
| Python | 3.12 64 位（CPython 3.12.5 已验证） |
| PyInstaller | 6.20.0 |
| pyinstaller-hooks-contrib | 2026.4 |
| Inno Setup | 6.2+（需 `iscc.exe` 加入 PATH，或设置 `ISCC_PATH` 环境变量） |
| 运行依赖 | `customtkinter`、`frida`、`psutil`、`keyboard`、`pygame`、`Pillow` |

> 注意：本项目使用 `customtkinter`（非外部项目的 `imgui_bundle`），依赖收集规则不同，见 §6.2。

虚拟环境固定位置（与《32-打包发布须知.md》一致，全版本共享）：

```text
04-正式发行版/.venv-build/
```

依赖清单（锁定版本）：

```text
全功能整合包2.4/game_modifier/requirements-build.txt
```

从目标版本的 `game_modifier` 目录校准环境：

```powershell
$projectDir = (Get-Location).Path
$releaseRoot = Split-Path -Parent (Split-Path -Parent $projectDir)
$buildEnv = Join-Path $releaseRoot '.venv-build'
$buildPython = Join-Path $buildEnv 'Scripts\python.exe'

if (-not (Test-Path -LiteralPath $buildPython -PathType Leaf)) {
  py -3.12 -m venv $buildEnv
}

& $buildPython -m pip install -r (Join-Path $projectDir 'requirements-build.txt')
& $buildPython -m pip check
```

## 5. 关键差异与适配点（相对外部项目规范）

外部项目《03-整合包1.2安装器打包规范.md》的下列设定需在本项目替换：

| 外部项目设定 | 本项目适配 |
|---|---|
| UI 框架 `imgui_bundle`，需 `collect_data_files` + `collect_dynamic_libs` | UI 框架 `customtkinter`，仅需 `collect_data_files("customtkinter")` |
| AppName `整合包1.2` | AppName `UCF2.4修改器`（由目录名动态解析） |
| 安装目录英文名 `DarkStar-Trainer-1.2` | 安装目录英文名 `UCF-Trainer-2.4`（见 §8.2） |
| 用户数据 `%LOCALAPPDATA%\DarkStarSingularity\整合包1.2\` | 用户数据 `%LOCALAPPDATA%\UCFModifier\2.4\data\`（见 §7） |
| 游戏进程 `DarkStar.exe` | 游戏进程 `UnityCrossFire.exe` |
| `upx=True` | 沿用本项目约定 `upx=False`（见《32》§六） |

## 6. PyInstaller onedir 规范

### 6.1 spec 文件

复用既有 spec：

```text
全功能整合包2.4/game_modifier/game_modifier.spec
```

onefile 与 onedir 的 spec 差异仅在末尾 `EXE()` / `COLLECT()` 段。需要在现有 spec 末尾将单文件写法改为 onedir 写法（见 §6.3）。

### 6.2 必须收集的依赖

```text
customtkinter        collect_data_files（spec 已有）
frida                collect_dynamic_libs（PyInstaller 自带 hook 通常已处理，构建后用 warn-*.txt 核对）
features/*/*         作为 data 文件，保持相对路径（spec 已用 add_feature_runtime_files 收集）
资源/                微信赞赏码.png、音效1.MP3、红色图片/、红色文案/（spec 已收集）
plugins/universal_hook/   inject.exe、Universal-ImGui-Hook.dll、universal_hook.json（spec 已收集）
Tcl/Tk               spec 已从本机 Python 暂存并收集（见《32》§七）
```

> onedir 下资源直接落在 `UCF2.4修改器/_internal/`，运行时 `sys._MEIPASS` 仍可正确访问，`core/config.py` 中的 `BASE_DIR = sys._MEIPASS`、`RESOURCE_DIR`、`PLUGINS_DIR`、`FEATURES_DIR` 逻辑无需改动。

### 6.3 spec 末尾结构（onedir）

将现有 spec 末尾的 `EXE(...)` 单文件写法替换为：

```python
# onedir：EXE 不含 binaries/datas，改由 COLLECT 收集
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=app_name,
    console=False,
    strip=False,
    upx=False,          # 沿用本项目约定，见《32》§六
    uac_admin=True,     # 主 exe 每次启动弹 UAC，见 §9.1
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=app_name,
)
```

其余部分（版本解析、Tcl/Tk 暂存、资源/插件/features 收集、hiddenimports 过滤）**保持不变**，沿用《32-打包发布须知.md》的发布前阻断项要求。

### 6.4 资源路径

onedir 下 `_internal/` 即 PyInstaller 的 `sys._MEIPASS`，只读资源访问逻辑无需改动。**用户可写数据**（`data/`）的落点见 §7。

## 7. 用户数据目录策略（已确认：方案 A）

`core/config.py` 当前在 frozen 模式下：

```python
APP_DIR = os.path.dirname(sys.executable)   # onedir 主 exe 所在目录
DATA_DIR = os.path.join(APP_DIR, "data")    # 用户配置 JSON 落点
```

即 `data/`（`hotkeys.json`、`settings.json`、`weapon_hotkeys.json`、`desired_states.json`、`feature_state.json`、`user_config.json` 等）当前落在 **exe 同级目录**。

安装到 `Program Files\UCF-Trainer-2.4` 后，写入该目录需要管理员权限，且卸载时 Inno Setup 默认清空安装目录会连用户配置一起删除。因此采用**方案 A**：frozen 时把 `DATA_DIR` 重定向到 `%LOCALAPPDATA%\UCFModifier\2.4\`，安装目录不再写用户数据，卸载保留该目录。

### 7.1 config.py 改造步骤

修改 `core/config.py` 顶部 frozen 分支，把 `DATA_DIR` 重定向到用户级目录：

```python
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    BASE_DIR = sys._MEIPASS  # PyInstaller 解压目录
    RESOURCE_DIR = os.path.join(BASE_DIR, "资源")
    PLUGINS_DIR = os.path.join(BASE_DIR, "game_modifier", "plugins")
    FEATURES_DIR = os.path.join(BASE_DIR, "features")
    # 用户可写数据重定向到 %LOCALAPPDATA%，避免写 Program Files
    _local_app_data = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
    DATA_DIR = os.path.join(_local_app_data, "UCFModifier", "2.4", "data")
else:
    APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    BASE_DIR = APP_DIR
    RESOURCE_DIR = os.path.join(os.path.dirname(APP_DIR), "资源")
    PLUGINS_DIR = os.path.join(APP_DIR, "plugins")
    FEATURES_DIR = os.path.join(APP_DIR, "features")
    DATA_DIR = os.path.join(APP_DIR, "data")
```

要点：

1. 仅 frozen 模式重定向；源码运行时仍用 `APP_DIR/data`，不影响开发。
2. `2.4` 版本号建议从整合包目录名解析，避免后续版本手工改。若暂不解析，复制版本目录时务必同步修改此处字面量。
3. `os.makedirs(DATA_DIR, exist_ok=True)` 已在下方保留，首次运行自动创建。
4. 改造后需回归测试：快捷键保存/恢复、设置项持久化、武器快捷键、Nano-4T 选择、desired_state/feature_state 持久化均在 `%LOCALAPPDATA%\UCFModifier\2.4\data\` 下生效。

`logs/` 目录：按《32》§十一，正式版所有文件日志开关必须关闭，正式版**不产生** `logs/`。源码运行时才产生 `logs/`。本文按“正式版无日志文件”处理，卸载逻辑不需为 `logs/` 留保留项。

## 8. Inno Setup 安装器规范

### 8.1 脚本位置

```text
全功能整合包2.4/game_modifier/packaging/installer.iss
```

与 spec 同处 `game_modifier/` 下的 `packaging/` 子目录，便于构建脚本统一调用。

### 8.2 必备配置项

| 项 | 要求 |
|---|---|
| AppName | `全功能整合包2.4`（由目录版本动态生成，见 §8.3） |
| AppVersion | `2.4`（与 spec 的 `app_name` 版本一致） |
| DefaultDirName | 动态计算（见 §8.5），不写死 `{autopf}` |
| DefaultGroupName | `UCF修改器` |
| Compression | `lzma2/ultra64` |
| SolidCompression | `yes` |
| ArchitecturesInstallIn64BitMode | `x64` |
| PrivilegesRequired | `admin`（写 Program Files + frida attach 需要） |
| UninstallDisplayIcon | 主 exe 图标 |

安装目录名固定为英文 `UCF-Trainer-2.4`（降低中文路径风险）。AppName 仍用中文 `全功能整合包2.4` 作为显示名。

### 8.3 版本号动态生成

`installer.iss` 中的 `AppName` / `AppVersion` / `OutputBaseFilename` 不写死，由构建脚本 `build_release.ps1` 在编译前用整合包目录名解析版本号并替换占位符，或通过 ISPP 的 `#define` 传入。版本解析规则与 spec 一致：`全功能整合包(?P<version>\d+(?:\.\d+)+)`。

### 8.4 必备功能

1. 安装路径可改。
2. 桌面快捷方式（默认勾选，可取消）。
3. 开始菜单快捷方式。
4. 注册卸载项（控制面板可见）。
5. 卸载时清理安装目录内的程序文件；用户数据在 `%LOCALAPPDATA%\UCFModifier\2.4\`，卸载不删该目录。

### 8.5 默认安装路径选择逻辑

不硬编码盘符。按 `D → E → F → ...` 顺序遍历，选第一个**存在且非系统盘**的盘，都没有再回退到 `C:\Program Files`。在 `[Code]` 段实现：

```pascal
const
  InstallFolder = 'UCF-Trainer-2.4';

function GetDefaultInstallDir(Param: string): string;
var
  Drive: Char;
  Path: string;
begin
  for Drive := 'D' to 'Z' do
  begin
    if Drive <> UpCase(ExtractFileDrive(ExpandConstant('{win}'))[1]) then
    begin
      Path := Drive + ':\Program Files\' + InstallFolder;
      if DirExists(Drive + ':\') then
      begin
        Result := Path;
        Exit;
      end;
    end;
  end;
  Result := ExpandConstant('{autopf}\') + InstallFolder;
end;
```

`[Setup]` 段引用：

```text
DefaultDirName={code:GetDefaultInstallDir}
```

注意：

1. 不检查剩余空间，避免误判。
2. 用户仍可在安装界面手动改路径。
3. 回退到 C 盘时使用 `{autopf}`，尊重 32/64 位系统约定。

### 8.6 Files / Icons / Run 段要点

```text
[Files]
; onedir 产物整目录拷入，排除构建中间产物
Source: "..\dist_release\{#AppExeName}\*"; DestDir: "{app}"; \
    Flags: recursesubdirs createallsubdirs ignoreversion; \
    Excludes: "build\*,dist\*,__pycache__\*,*.spec.bak,logs\*,data\*"

[Icons]
; 快捷方式显示名用 AppName（全功能整合包2.4），exe 文件名用 AppExeName（UCF2.4修改器.exe）
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}.exe"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}.exe"; \
    Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "在桌面创建快捷方式"; GroupDescription: "附加选项:"; Flags: checkedonce

[Run]
; 安装结束不自动启动（修改器需用户主动启动并接受 UAC）
```

> 其中 `{#AppName}` = `全功能整合包2.4`（控制面板/快捷方式显示名），`{#AppExeName}` = `UCF2.4修改器`（PyInstaller 产物 exe 名），由 ISPP `#define` 从 `AppVersion` 拼接，见 §8.3。

> `Excludes` 中的 `data\*` 为防御性排除：方案 A 下 `data/` 已重定向到 `%LOCALAPPDATA%`，安装目录不预置开发者 data，首次运行由程序在 `%LOCALAPPDATA%\UCFModifier\2.4\data\` 自动创建。

### 8.7 Uninstall 段要点

方案 A 下用户数据在 `%LOCALAPPDATA%\UCFModifier\2.4\`，不在安装目录。默认卸载清空 `{app}` 即可，**不要**在 `[UninstallDelete]` 中触碰 `%LOCALAPPDATA%`：

```text
[UninstallDelete]
; 仅清理安装目录程序文件，用户配置在 %LOCALAPPDATA% 不动
Type: filesandordirs; Name: "{app}"
```

> 由于 `data/` 已重定向到 `%LOCALAPPDATA%`，安装目录内不再产生 `data/`，卸载直接清空 `{app}` 不会误删用户配置。

## 9. 主 exe 管理员权限与 UPX

### 9.1 UAC

主 exe **每次启动都弹 UAC**，强制 admin 权限。原因：

1. frida attach 游戏进程几乎必然需要 admin。
2. DLL 注入（`inject.exe` + `Universal-ImGui-Hook.dll`）需要 admin。
3. 避免“先启动 → attach 失败 → 提示重启”的二次操作。

实现：spec 的 `EXE()` 中 `uac_admin=True`（已有）。

配套要求：

1. 安装器创建的快捷方式不需要额外标记“以管理员身份运行”，exe 自带 manifest 会触发 UAC。
2. README 必须告知用户每次启动会弹 UAC，属于正常现象。
3. 安装器本身也需要 admin（写 Program Files），与主 exe 一致。

### 9.2 UPX

沿用本项目约定 `upx=False`（见《32》§六）。理由：本机未配置 UPX；对注入器类程序，额外二进制压缩不利于杀毒软件信誉判断。

## 10. 一键构建脚本

固定位置：

```text
全功能整合包2.4/game_modifier/packaging/build_release.ps1
```

脚本职责：

1. 检测 `ISCC_PATH` 环境变量或 PATH 中的 `iscc.exe`，缺失时报错退出。
2. 解析整合包目录名得到版本号，校验符合 `全功能整合包x.x` 规则。
3. 清理 `build_release/`、`dist_release/`、`release/`。
4. 用 `$buildPython`（`04-正式发行版/.venv-build`）调用 PyInstaller 构建 onedir：

```powershell
& $buildPython -m PyInstaller `
  --clean `
  --noconfirm `
  --workpath build_release `
  --distpath dist_release `
  game_modifier.spec
```

5. 校验产物 `dist_release/UCF<版本>修改器/UCF<版本>修改器.exe` 存在，且包含 `_internal/`。
6. 调用 `iscc.exe installer.iss` 编译安装器（版本号通过 ISCC 参数或占位符替换传入）。
7. 输出 `release/UCF<版本>修改器安装器.exe`。
8. 计算 SHA256，写入 `release/SHA256.txt`。

调用顺序：

```powershell
python -m PyInstaller --clean --noconfirm --workpath build_release --distpath dist_release game_modifier.spec
iscc packaging\installer.iss
```

## 11. README 模板（UAC 提示）

```text
每次启动 UCF2.4修改器.exe 会弹出 UAC 授权窗口，请点击“是”。
这是修改器连接游戏（frida attach + DLL 注入）所必需的权限，属于正常现象。

若杀毒软件报毒，系修改器含注入器与 Frida 组件所致，请加入信任后使用。
```

## 12. 发布物结构

```text
release/
├── UCF2.4修改器安装器.exe
├── README.txt
└── SHA256.txt
```

不应包含：

```text
build/  build_release/  dist/  dist_release/  *.spec.bak  __pycache__/  tests/  logs/  旧日志  data/
```

## 13. 验证清单

### 13.1 安装验证

1. 安装器能选择自定义路径。
2. 安装后开始菜单和桌面快捷方式存在。
3. 控制面板出现卸载项。
4. 安装目录包含 `UCF2.4修改器.exe` 和 `_internal/`。
5. 首次启动后在 `%LOCALAPPDATA%\UCFModifier\2.4\data\` 自动生成用户数据目录。

### 13.2 运行验证

1. 通过快捷方式启动 GUI，弹 UAC 点“是”后正常启动。
2. 中文显示正常，红色主题 Tab 图片/文案正常加载。
3. 自动检测并连接 `UnityCrossFire.exe`。
4. 各功能页开关可用（RPC 异步、状态机符合《21-整合包功能接入规范》）。
5. 快捷键保存与重启恢复正常。
6. 音效、赞赏码图片正常。

### 13.3 卸载验证

1. 控制面板卸载成功。
2. 安装目录程序文件被清理。
3. 快捷方式被清除。
4. `%LOCALAPPDATA%\UCFModifier\2.4\` 用户数据保留（卸载不清用户配置）。

### 13.4 干净机器验证

在没有 Python、没有 Inno Setup、没有项目源码的机器上：

1. 安装、启动、连接、卸载全流程通过。
2. 不弹缺 DLL、缺模块错误。

### 13.5 中文路径验证（必须实测）

1. 主 exe 从中文安装路径（如 `D:\Program Files\游戏修改器\`）启动正常。
2. frida 从中文安装目录发起 attach 连接成功。
3. 用户数据写入 `%LOCALAPPDATA%\UCFModifier\2.4\data\` 正常。

## 14. 已确认决策

迁移本规范时已确认的决策点如下，全文按此执行：

| 决策项 | 结论 | 依据 |
|---|---|---|
| D1 用户数据目录策略 | 方案 A：frozen 时重定向到 `%LOCALAPPDATA%\UCFModifier\2.4\data\`，需改 `config.py`（见 §7.1） | 安装到 Program Files 后可正常写、卸载不丢、升级不冲突 |
| D2 安装目录英文名 | `UCF-Trainer-2.4` | 降低中文路径风险，AppName 显示名仍为中文 `UCF2.4修改器` |
| D3 onedir+Inno 与 onefile 关系 | 并存 | 安装器版作为兼容备用，单文件版继续维护 |
| D4 packaging 目录位置 | `game_modifier/packaging/` | 与 spec 同处，构建脚本统一调用 |
| D5 用户数据公司级目录名 | `UCFModifier`（即 `%LOCALAPPDATA%\UCFModifier\2.4\`） | 方案 A 下 `%LOCALAPPDATA%` 的根目录名 |

## 15. 风险与处理

| 风险 | 处理 |
|---|---|
| frida attach / DLL 注入被拒绝 | 主 exe 启用 `uac_admin=True`，每次启动弹 UAC |
| 用户对每次弹 UAC 反感 | README 明确说明这是修改器正常行为 |
| 缺 DLL 或启动闪退 | 检查 onedir `_internal/` 是否完整收集 customtkinter/frida/Tcl-Tk 原生依赖 |
| 中文路径导致运行异常 | 按 §13.5 实测；hidden import 报错时单独处理 |
| 杀软误报 | onedir 误报率低于 onefile；README 提示加入信任 |
| 安装目录无写权限 | 方案 A 用户数据写入 `%LOCALAPPDATA%`；方案 B 依赖 admin 写入 |
| 默认盘符选择异常（光驱/U 盘占用 D 盘） | §8.5 逻辑只判断盘符存在，用户可手动改路径 |
| iscc 不在 PATH | 构建脚本检测 `ISCC_PATH` 环境变量，缺失时报错退出 |
| 升级覆盖安装丢用户配置 | 方案 A 配置在 `%LOCALAPPDATA%` 不受影响；方案 B 需 Inno 卸载排除 `data` |

## 16. 实测记录：便携版与安装版快捷键配置共用同一文件

### 16.1 问题

`dist_release\UCF2.4修改器`（PyInstaller onedir 便携版产物）与 `D:\Program Files\UCF-Trainer-2.4`（Inno Setup 安装版产物）两个程序的快捷键记录，读取的是哪个位置的 json 文件？初步判断两者读取的是同一个文件，但缺少依据。

### 16.2 结论

两个程序读取的是**同一个文件**：

```text
C:\Users\<用户名>\AppData\Local\UCFModifier\2.4\data\hotkeys.json
```

（本机实测路径：`C:\Users\17242\AppData\Local\UCFModifier\2.4\data\hotkeys.json`）

### 16.3 依据

`core/config.py` 第 6-21 行根据 `sys.frozen` 分流 DATA_DIR：

```python
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
    BASE_DIR = sys._MEIPASS
    ...
    # 用户可写数据重定向到 %LOCALAPPDATA%，避免写 Program Files（安装器打包规范 §7.1 方案A）
    _local_app_data = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~\\AppData\\Local")
    DATA_DIR = os.path.join(_local_app_data, "UCFModifier", "2.4", "data")
else:
    ...
    DATA_DIR = os.path.join(APP_DIR, "data")
```

第 26 行：`HOTKEYS_FILE = os.path.join(DATA_DIR, "hotkeys.json")`。

两个产物均为 PyInstaller 打包的发行版（`sys.frozen == True`），因此 `DATA_DIR` **不取决于 exe 所在位置**，统一指向 `%LOCALAPPDATA%\UCFModifier\2.4\data\`。无论从 `D:\trae_project\...\UCF2.4修改器\` 还是 `D:\Program Files\UCF-Trainer-2.4\` 启动，快捷键文件都落在上述同一位置。已确认该目录下存在 `hotkeys.json`（以及 `weapon_hotkeys.json`、`feature_state.json`、`desired_states.json`、`user_config.json` 等也共用同一位置）。

### 16.4 设计原因

代码注释已说明：把用户可写数据重定向到 `%LOCALAPPDATA%`，是为了避免向 `D:\Program Files\UCF-Trainer-2.4` 这种受保护目录写入，同时让便携版和安装版共享同一份用户配置（见 §7.1 方案 A）。
