<#
.SYNOPSIS
    车测：让插件自己在游戏里切图，跑完告诉你 PASS / CRASH / 超时。

.DESCRIPTION
    不依赖鼠标键盘（DSH 会话里抢不到游戏窗口前台，合成点击会落到别的窗口）。
    做法：svc 端写一个 cmd（带 UCF_AUTOTEST / UCF_MOD 环境变量）→ WMI 拉起游戏
    → 插件的 autotest.c 用 SceneManager.LoadScene(buildIndex, Single) 逐张图切
    → 每张图等 N 个 tick → 全过写 autotest.txt 并 ExitProcess(0)。
    崩了就没有 RESULT PASS，日志里会有 '!!! crash' 段（VEH 记录）。

.EXAMPLE
    .\tools\autotest.ps1 -Targets 7,10 -Settle 170
    .\tools\autotest.ps1 -Targets 7,10,7,10 -Settle 120 -NoKill
#>
param(
    [string]$Targets = '7,10',
    [int]$Settle = 120,
    [int]$Warm = 40,
    [int]$TimeoutSec = 240,
    [string]$GameDir = '',
    [switch]$NoKill
)

$ErrorActionPreference = 'Continue'
$tools = $PSScriptRoot
# 项目根：向上找 .ucfroot（和 core/ucf_paths.py 同一套约定）
$projRoot = $tools
while (-not (Test-Path -LiteralPath (Join-Path $projRoot '.ucfroot')) -and (Split-Path -Parent $projRoot) -ne $projRoot) {
    $projRoot = Split-Path -Parent $projRoot
}
# 游戏位置：命令行 > 用户配置 > 工程 tools/deploy.json（开发机兜底）
if (-not $GameDir) {
    $userCfg = Join-Path $env:LOCALAPPDATA 'UCFMod\deploy.json'
    if (Test-Path -LiteralPath $userCfg) {
        try {
            $j = Get-Content -LiteralPath $userCfg -Raw | ConvertFrom-Json
            if ($j.game_dir) { $GameDir = $j.game_dir }
        } catch { }
    }
}
if (-not $GameDir) {
    $cfg = Join-Path $tools 'deploy.json'
    if (Test-Path -LiteralPath $cfg) {
        $dep = (Get-Content -LiteralPath $cfg -Raw | ConvertFrom-Json).deploy
        if ($dep) { $GameDir = Split-Path -Parent $dep }
    }
}
if (-not $GameDir -or -not (Test-Path -LiteralPath (Join-Path $GameDir 'UnityCrossFire.exe'))) {
    throw "找不到游戏目录：$GameDir（用 -GameDir 指定，或先在控制台选游戏）"
}

# 2026-11-25：运行时状态全在工程端 run\runtime\，日志在工程端 log\；
# 游戏目录不再生成 ucf_mod\。
$logDir   = Join-Path $projRoot 'log'
$runtime  = Join-Path $projRoot 'run\runtime'
$logPath  = Join-Path $logDir 'ucf_mod.log'
$atPath   = Join-Path $logDir 'autotest.txt'
$cmdPath  = Join-Path $runtime '_autotest.cmd'
$buildDll = Join-Path $projRoot 'run\build\ucf_mod.dll'
$payloadDll = Join-Path $projRoot 'run\payload\ucf_mod\ucf_mod.dll'
$modDll = if (Test-Path -LiteralPath $buildDll) { $buildDll } else { $payloadDll }
if (-not (Test-Path -LiteralPath $modDll)) { throw "插件未编译：$buildDll / $payloadDll 都不存在" }
New-Item -ItemType Directory -Force -Path $runtime | Out-Null

if (-not $NoKill) {
    Get-Process UnityCrossFire -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 1
}
New-Item -ItemType Directory -Force -Path $logDir | Out-Null      # 工程端 log\
if (Test-Path -LiteralPath $logPath) {
    Move-Item -LiteralPath $logPath -Destination (Join-Path $logDir ('ucf_mod.prev_' + (Get-Date -Format 'HHmmss') + '.log')) -Force
}
if (Test-Path -LiteralPath $atPath) { Remove-Item -LiteralPath $atPath -Force }

# 三区：车测也把导出/测试包指到 ② 开发版，正式版 nav\ 保持只读（和 UCF 控制台一致）
$testVis = Join-Path $projRoot 'data\navdata\dev\vis'
$testPacks = Join-Path $projRoot 'data\navdata\dev\packs'

$markers = Join-Path $projRoot 'data\navdata\dev\markers'
$lines = @(
    '@echo off',
    'set UCF_MOD=1',
    ('set "UCF_MOD_DLL=' + $modDll + '"'),
    ('set "UCF_MOD_DIR=' + $runtime + '"'),
    ('set "UCF_MARKERS_DIR=' + $markers + '"'),
    ('set "UCF_EXPORT_DIR=' + $testVis + '"'),
    ('set "UCF_PACK_DIR=' + $testPacks + '"'),
    ('set "UCF_LOG_DIR=' + $logDir + '"'),
    'set UCF_NAV_READONLY=1',
    ('set UCF_AUTOTEST=' + $Targets),
    ('set UCF_AT_WARM=' + $Warm),
    ('set UCF_AT_SETTLE=' + $Settle),
    'set UCF_AT_EXIT=1',
    ('cd /d "' + $gameDir.Replace('/','\') + '"'),
    'start "" UnityCrossFire.exe'
)
Set-Content -LiteralPath $cmdPath -Value $lines -Encoding Default

$res = ([wmiclass]'Win32_Process').Create('cmd.exe /c "' + $cmdPath.Replace('/','\') + '"', $gameDir.Replace('/','\'))
if ($res.ReturnValue -ne 0) { throw "WMI launch failed: $($res.ReturnValue)" }
"launched  targets=$Targets  settle=$Settle  at $(Get-Date -Format 'HH:mm:ss')"

$deadline = (Get-Date).AddSeconds($TimeoutSec)
$state = 'timeout'
while ((Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 5
    if (Test-Path -LiteralPath $logPath) {
        $hit = Select-String -LiteralPath $logPath -Pattern 'RESULT PASS|RESULT FAIL|!!! crash' -Encoding UTF8 | Select-Object -Last 1
        if ($hit) {
            if ($hit.Line -match 'RESULT PASS') { $state = 'PASS'; break }
            if ($hit.Line -match 'RESULT FAIL') { $state = 'FAIL'; break }
            if ($hit.Line -match 'crash')        { $state = 'CRASH'; break }
        }
    }
    if (-not (Get-Process UnityCrossFire -ErrorAction SilentlyContinue) -and -not (Test-Path -LiteralPath $logPath)) { $state = 'no-game'; break }
}

"state = $state  ($(Get-Date -Format 'HH:mm:ss'))"
if (Test-Path -LiteralPath $logPath) {
    Select-String -LiteralPath $logPath -Pattern 'LOAD level|OK level|RESULT|!!! crash|vis: exported|auto-export|roots:' -Encoding UTF8 |
        ForEach-Object { $_.Line }
    if ($state -eq 'CRASH') {
        ""; '---- crash block ----'
        $all = [IO.File]::ReadAllLines($logPath, [Text.Encoding]::UTF8)
        $idx = @(); for ($i = 0; $i -lt $all.Count; $i++) { if ($all[$i] -match '!!! crash') { $idx += $i } }
        if ($idx.Count) { $s = [Math]::Max(0, $idx[-1] - 20); $all[$s..($all.Count - 1)] }
    }
}
if (Test-Path -LiteralPath $atPath) { ''; '---- autotest.txt ----'; Get-Content -LiteralPath $atPath -Encoding UTF8 }
if ($state -eq 'PASS') { exit 0 } else { exit 1 }