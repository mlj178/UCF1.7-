; UCF 修改器 Inno Setup 安装器脚本（onedir 形态）
; 对应《安装器打包规范-onedir+InnoSetup.md》§8
; 版本号默认取 2.5，可被 build_release.ps1 通过 /DAppVersion=x.x 覆盖。
; 编译：iscc /DAppVersion=2.5 packaging\installer.iss

#ifndef AppVersion
  #define AppVersion "2.5"
#endif
#ifndef BuildDistDir
  #define BuildDistDir "..\dist_release"
#endif
#ifndef ReleaseOutputDir
  #define ReleaseOutputDir "..\release"
#endif
#define AppName "全功能整合包" + AppVersion
#define AppExeName "UCF" + AppVersion + "修改器"
#define InstallFolder "UCF-Trainer-" + AppVersion

[Setup]
; AppName 为控制面板显示名（中文），AppExeName 为 PyInstaller 产物 exe 名
AppName={#AppName}
AppVersion={#AppVersion}
DefaultDirName={code:GetDefaultInstallDir}
DefaultGroupName=UCF修改器
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
ArchitecturesAllowed=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#AppExeName}.exe
; 产物输出到 game_modifier 同级的 release/（脚本从 packaging/ 调用，故 ..\release）
OutputDir={#ReleaseOutputDir}
OutputBaseFilename={#AppExeName}安装器
DisableProgramGroupPage=yes
WizardStyle=modern

[Languages]
; Inno Setup 6.7.3 官方语言包不含简体中文 ISL（位于 Unofficial 目录）。
; 当前用默认英文界面；AppName/快捷方式/Tasks 描述中的中文仍可正常显示（Unicode 版本）。
; 如需中文界面，从 https://github.com/jrsoftware/issrc 下载 ChineseSimplified.isl
; 放入 packaging/ 后改回：Name: "chinesesimp"; MessagesFile: "ChineseSimplified.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "在桌面创建快捷方式"; GroupDescription: "附加选项:"; Flags: checkedonce

[Files]
; onedir 产物整目录拷入，排除构建中间产物与开发者 data
Source: "{#BuildDistDir}\{#AppExeName}\*"; DestDir: "{app}"; \
    Flags: recursesubdirs createallsubdirs ignoreversion; \
    Excludes: "build\*,dist\*,__pycache__\*,*.spec.bak,logs\*,data\*"

[Icons]
Name: "{group}\{#AppName}"; Filename: "{app}\{#AppExeName}.exe"
Name: "{commondesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}.exe"; Tasks: desktopicon

[Run]
; 安装结束不自动启动（修改器需用户主动启动并接受 UAC）

[UninstallDelete]
; 仅清理安装目录程序文件，用户配置在 %LOCALAPPDATA%\UCFModifier 不动（方案A）
Type: filesandordirs; Name: "{app}"

[Code]
const
  InstallFolder = '{#InstallFolder}';

function GetDefaultInstallDir(Param: string): string;
var
  DriveCode: Integer;
  Drive: Char;
  SysDrive: string;
  Path: string;
begin
  // 优先 D、E、F... 非系统盘（68='D'，90='Z'）
  SysDrive := Uppercase(ExtractFileDrive(ExpandConstant('{win}')));  // e.g. 'C:'
  for DriveCode := 68 to 90 do
  begin
    Drive := Chr(DriveCode);
    if (Length(SysDrive) > 0) and (Drive <> SysDrive[1]) then
    begin
      Path := Drive + ':\Program Files\' + InstallFolder;
      if DirExists(Drive + ':\') then
      begin
        Result := Path;
        Exit;
      end;
    end;
  end;
  // 回退 C 盘
  Result := ExpandConstant('{autopf}\') + InstallFolder;
end;
