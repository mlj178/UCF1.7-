@echo off
setlocal

echo ==========================================
echo   Building Universal-ImGui-Hook.dll
echo   Using Visual Studio 2022 MSBuild
echo ==========================================
echo.

set "MSBUILD_PATH=D:\VS2022\MSBuild\Current\Bin\MSBuild.exe"
set "CONFIGURATION=Release"
set "PLATFORM=x86"
set "SLN_FILE=Universal-ImGui-Hook.sln"

if not exist "%MSBUILD_PATH%" (
    echo [ERROR] MSBuild.exe not found at %MSBUILD_PATH%
    exit /b 1
)

if not exist "%SLN_FILE%" (
    echo [ERROR] Solution file not found: %SLN_FILE%
    exit /b 1
)

echo [OK] Found MSBuild: %MSBUILD_PATH%
echo [INFO] Configuration: %CONFIGURATION%
echo [INFO] Platform: %PLATFORM%
echo [INFO] Solution: %SLN_FILE%
echo.
echo [INFO] Compiling...
echo.

"%MSBUILD_PATH%" "%SLN_FILE%" /p:Configuration=%CONFIGURATION% /p:Platform=%PLATFORM% /m /v:minimal

if errorlevel 1 (
    echo.
    echo ==========================================
    echo   [FAILED] Build failed.
    echo ==========================================
    exit /b 1
)

echo.
echo ==========================================
echo   [SUCCESS] Build completed.
echo ==========================================
echo   Output: Universal-ImGui-Hook.dll
if exist Universal-ImGui-Hook.dll (
    for %%F in (Universal-ImGui-Hook.dll) do echo   Size: %%~zF bytes
)
echo.

echo [INFO] Deploying to game_modifier...
set "TARGET_DIR=D:\trae_project\ucf1.7-modifier\04-正式发行版\全功能整合包1.7\game_modifier\plugins\universal_hook"

if exist "Universal-ImGui-Hook.dll" (
    copy /Y "Universal-ImGui-Hook.dll" "%TARGET_DIR%\"
    echo [OK] Copied Universal-ImGui-Hook.dll
)

if exist "inject.exe" (
    copy /Y "inject.exe" "%TARGET_DIR%\"
    echo [OK] Copied inject.exe
)

echo.
echo ==========================================
echo   [DEPLOY COMPLETE]
echo ==========================================
exit /b 0
