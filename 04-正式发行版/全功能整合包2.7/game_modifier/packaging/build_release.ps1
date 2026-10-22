# UCF 修改器 onedir + Inno Setup 一键构建脚本
# 对应《安装器打包规范-onedir+InnoSetup.md》§10
# 用法：在 game_modifier/ 目录下执行  powershell -ExecutionPolicy Bypass -File packaging\build_release.ps1
# 产物：release/全功能整合包<版本>.exe（安装器）+ release/SHA256.txt

$ErrorActionPreference = 'Stop'

# 1. 解析整合包目录名得到版本号
$projectDir = (Get-Location).Path
$packageFolder = Split-Path -Leaf (Split-Path -Parent $projectDir)
$versionMatch = [regex]::Match($packageFolder, '^全功能整合包(?<version>\d+(?:\.\d+)+)$')
if (-not $versionMatch.Success) {
    throw "整合包目录名不符合规则：$packageFolder；应为：全功能整合包x.x"
}
$packageVersion = $versionMatch.Groups['version'].Value
# 2.7 起发布名统一为“全功能整合包x.x”（与 spec 的 app_name、installer.iss 的 AppExeName 一致），
# 以后复制出“全功能整合包2.8”等目录时自动跟着变，无需再改这里。
$appExeName = "全功能整合包${packageVersion}"
Write-Output "[1/8] 版本号：$packageVersion"
Write-Output "[1/8] 主程序名：$appExeName"

# 2. 共享构建虚拟环境（04-正式发行版/.venv-build）
$releaseRoot = Split-Path -Parent (Split-Path -Parent $projectDir)
$buildEnv = Join-Path $releaseRoot '.venv-build'
$buildPython = Join-Path $buildEnv 'Scripts\python.exe'
if (-not (Test-Path -LiteralPath $buildPython -PathType Leaf)) {
    throw "未找到构建虚拟环境：$buildPython；请先按《32-打包发布须知.md》§三创建 .venv-build 并安装 requirements-build.txt"
}
Write-Output "[2/8] 构建Python：$buildPython"

# 3. 检测 iscc.exe
$iscc = $env:ISCC_PATH
if (-not $iscc) {
    $cmd = Get-Command iscc.exe -ErrorAction SilentlyContinue
    if ($cmd) { $iscc = $cmd.Source }
}
# Inno Setup 默认不写 PATH，这里再补几个常见安装位置，免得每次都手动设 ISCC_PATH
if (-not $iscc) {
    $isccCandidates = @(
        'C:\Program Files (x86)\Inno Setup 6\ISCC.exe',
        'C:\Program Files\Inno Setup 6\ISCC.exe',
        (Join-Path $env:ProgramFiles 'Inno Setup 6\ISCC.exe')
    )
    foreach ($candidate in $isccCandidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate -PathType Leaf)) { $iscc = $candidate; break }
    }
}
if (-not $iscc -or -not (Test-Path -LiteralPath $iscc -PathType Leaf)) {
    throw "未找到 iscc.exe；请安装 Inno Setup 6.2+ 并加入 PATH，或设置 ISCC_PATH 环境变量"
}
Write-Output "[3/8] ISCC：$iscc"

# 4. 清理旧产物
$buildDir = Join-Path $projectDir 'build_release'
$distDir = Join-Path $projectDir 'dist_release'
$releaseDir = Join-Path $projectDir 'release'
if (Test-Path $buildDir) { Remove-Item -Recurse -Force $buildDir }
if (Test-Path $distDir) { Remove-Item -Recurse -Force $distDir }
if (Test-Path $releaseDir) { Remove-Item -Recurse -Force $releaseDir }
Write-Output "[4/8] 已清理 build_release / dist_release / release"

# 5. PyInstaller onedir 构建
$specFile = Join-Path $projectDir 'game_modifier_onedir.spec'
if (-not (Test-Path -LiteralPath $specFile -PathType Leaf)) {
    throw "未找到 onedir spec：$specFile"
}
Write-Output "[5/8] PyInstaller onedir 构建中..."
& $buildPython -m PyInstaller --clean --noconfirm --workpath $buildDir --distpath $distDir $specFile
if ($LASTEXITCODE -ne 0) { throw "PyInstaller 构建失败（退出码 $LASTEXITCODE）" }

# 6. 校验 onedir 产物
$exePath = Join-Path $distDir (Join-Path $appExeName "$appExeName.exe")
if (-not (Test-Path -LiteralPath $exePath -PathType Leaf)) {
    throw "未找到 onedir 主程序：$exePath"
}
$internalDir = Join-Path $distDir (Join-Path $appExeName '_internal')
if (-not (Test-Path $internalDir -PathType Container)) {
    throw "未找到 _internal 目录：$internalDir"
}
Write-Output "[6/8] onedir 产物校验通过：$exePath"

# 7. Inno Setup 编译安装器
New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null
$issFile = Join-Path $projectDir 'packaging\installer.iss'
Write-Output "[7/8] Inno Setup 编译中..."
& $iscc "/DAppVersion=$packageVersion" $issFile
if ($LASTEXITCODE -ne 0) { throw "Inno Setup 编译失败（退出码 $LASTEXITCODE）" }

# 8. 校验安装器产物并生成 SHA256
$installerPath = Join-Path $releaseDir "${appExeName}.exe"
if (-not (Test-Path -LiteralPath $installerPath -PathType Leaf)) {
    throw "未找到安装器产物：$installerPath"
}
$hash = (Get-FileHash -LiteralPath $installerPath -Algorithm SHA256).Hash
$hashFile = Join-Path $releaseDir 'SHA256.txt'
"$hash  ${appExeName}.exe" | Out-File -Encoding utf8 -FilePath $hashFile
$readmeSource = Join-Path $projectDir 'packaging\README.txt'
if (-not (Test-Path -LiteralPath $readmeSource -PathType Leaf)) {
    throw "未找到发布说明：$readmeSource"
}
Copy-Item -LiteralPath $readmeSource -Destination (Join-Path $releaseDir 'README.txt') -Force
$disclaimerSource = Join-Path $projectDir 'packaging\免责声明.txt'
if (-not (Test-Path -LiteralPath $disclaimerSource -PathType Leaf)) {
    throw "未找到免责声明：$disclaimerSource"
}
Copy-Item -LiteralPath $disclaimerSource -Destination (Join-Path $releaseDir '免责声明.txt') -Force
# 随包分发：Q群二维码 + Win7 不可用提示。release 目录旁边也放一份，方便连同安装包一起发出去
$resourceDir = Join-Path (Split-Path -Parent $projectDir) '资源'
foreach ($extraName in @('UCF1.7Q群1095388251.jpg', 'win7用不了，只有win10和11能用.txt')) {
    $extraSource = Join-Path $resourceDir $extraName
    if (-not (Test-Path -LiteralPath $extraSource -PathType Leaf)) {
        throw "未找到附加资源：$extraSource"
    }
    Copy-Item -LiteralPath $extraSource -Destination (Join-Path $releaseDir $extraName) -Force
}
Write-Output "[8/8] 构建完成"
Write-Output ""
Write-Output "安装器：$installerPath"
Write-Output "SHA256：$hash"
