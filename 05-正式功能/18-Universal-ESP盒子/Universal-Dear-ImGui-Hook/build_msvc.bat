@echo off
setlocal
rem ============================================================
rem 编译 Universal-ImGui-Hook.dll（x86 / Release）
rem 工具链：Visual Studio 2022 (MSVC v143)，见 使用教程.md 第 4 节
rem 输出：本目录 Universal-ImGui-Hook.dll
rem       （Universal-ImGui-Hook.vcxproj 的 Release|Win32 OutDir = ProjectDir）
rem 注意：游戏是 32 位（WoW64），必须用 Platform=Win32；编译后可用
rem       dumpbin /headers 确认 machine 为 14C。
rem ============================================================

set "PROJ=%~dp0Universal-ImGui-Hook.vcxproj"
set "MSBUILD=D:\VS2022\MSBuild\Current\Bin\MSBuild.exe"

if not exist "%MSBUILD%" (
    set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
    if exist "%VSWHERE%" (
        for /f "tokens=*" %%i in ('"%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild -find MSBuild\**\Bin\MSBuild.exe') do set "MSBUILD=%%i"
    )
)

if not exist "%MSBUILD%" (
    echo [ERROR] MSBuild not found. Set MSBUILD manually.
    exit /b 1
)

echo Using MSBuild: "%MSBUILD%"
"%MSBUILD%" "%PROJ%" /p:Configuration=Release /p:Platform=Win32 /m /nologo /v:minimal
if errorlevel 1 (
    echo [ERROR] Build failed.
    exit /b 1
)

echo.
echo [OK] Output: %~dp0Universal-ImGui-Hook.dll
endlocal
