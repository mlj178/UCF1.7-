# UCF 2.5 non-destructive onedir + Inno Setup release builder.
# This file is ASCII-only so Windows PowerShell can execute it without a UTF-8 BOM.

$ErrorActionPreference = 'Stop'

$projectDir = (Get-Location).Path
$packageFolder = Split-Path -Leaf (Split-Path -Parent $projectDir)
$packagePrefix = [string]::Concat([char]0x5168, [char]0x529F, [char]0x80FD, [char]0x6574, [char]0x5408, [char]0x5305)
$versionPattern = '^' + [regex]::Escape($packagePrefix) + '(?<version>\d+(?:\.\d+)+)$'
$versionMatch = [regex]::Match($packageFolder, $versionPattern)
if (-not $versionMatch.Success) {
    throw "Package directory must match the full-package version pattern: $packageFolder"
}

$packageVersion = $versionMatch.Groups['version'].Value
$modifierSuffix = [string]::Concat([char]0x4FEE, [char]0x6539, [char]0x5668)
$installerSuffix = [string]::Concat([char]0x5B89, [char]0x88C5, [char]0x5668)
$appExeName = "UCF${packageVersion}${modifierSuffix}"
$releaseRoot = Split-Path -Parent (Split-Path -Parent $projectDir)
$buildEnv = Join-Path $releaseRoot '.venv-build'
$buildPython = Join-Path $buildEnv 'Scripts\python.exe'
if (-not (Test-Path -LiteralPath $buildPython -PathType Leaf)) {
    throw "Build virtual environment was not found: $buildPython"
}

$iscc = $env:ISCC_PATH
if (-not $iscc) {
    $command = Get-Command iscc.exe -ErrorAction SilentlyContinue
    if ($command) { $iscc = $command.Source }
}
if (-not $iscc -or -not (Test-Path -LiteralPath $iscc -PathType Leaf)) {
    throw "iscc.exe was not found; install Inno Setup 6.2+ or set ISCC_PATH"
}

$tag = Get-Date -Format "yyyyMMdd-HHmmss"
$buildDir = Join-Path $projectDir "build_hidden_room_count_$tag"
$distDir = Join-Path $projectDir "dist_hidden_room_count_$tag"
$releaseDir = Join-Path $projectDir "release_hidden_room_count_$tag"
foreach ($path in @($buildDir, $distDir, $releaseDir)) {
    if (Test-Path -LiteralPath $path) {
        throw "Refusing to use an existing output directory: $path"
    }
}

Write-Output "Version: $packageVersion"
Write-Output "Build directory: $buildDir"
Write-Output "Distribution directory: $distDir"
Write-Output "Release directory: $releaseDir"

& $buildPython -m PyInstaller --clean --noconfirm --workpath $buildDir --distpath $distDir (Join-Path $projectDir 'game_modifier_onedir.spec')
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed with exit code $LASTEXITCODE" }

$exePath = Join-Path $distDir (Join-Path $appExeName "$appExeName.exe")
if (-not (Test-Path -LiteralPath $exePath -PathType Leaf)) {
    throw "The onedir executable was not found: $exePath"
}

New-Item -ItemType Directory -Path $releaseDir | Out-Null
$issFile = Join-Path $projectDir 'packaging\installer.iss'
& $iscc "/DAppVersion=$packageVersion" "/DBuildDistDir=$distDir" "/DReleaseOutputDir=$releaseDir" $issFile
if ($LASTEXITCODE -ne 0) { throw "Inno Setup failed with exit code $LASTEXITCODE" }

$installerFileName = "${appExeName}${installerSuffix}.exe"
$installerPath = Join-Path $releaseDir $installerFileName
if (-not (Test-Path -LiteralPath $installerPath -PathType Leaf)) {
    throw "The installer was not found: $installerPath"
}

$hash = (Get-FileHash -LiteralPath $installerPath -Algorithm SHA256).Hash
"$hash  $installerFileName" | Out-File -Encoding utf8 -FilePath (Join-Path $releaseDir 'SHA256.txt')
$readmeSource = Join-Path $projectDir 'packaging\README.txt'
if (Test-Path -LiteralPath $readmeSource -PathType Leaf) {
    Copy-Item -LiteralPath $readmeSource -Destination (Join-Path $releaseDir 'README.txt')
}

Write-Output "Installer: $installerPath"
Write-Output "SHA256: $hash"
