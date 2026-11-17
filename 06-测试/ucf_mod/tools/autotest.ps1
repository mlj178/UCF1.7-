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
    [switch]$NoKill
)

$ErrorActionPreference = 'Continue'
$tools = $PSScriptRoot
$cfg = Join-Path $tools 'deploy.json'
if (-not (Test-Path -LiteralPath $cfg)) { throw "missing tools/deploy.json" }
$modDir = (Get-Content -LiteralPath $cfg -Raw | ConvertFrom-Json).deploy
$gameDir = Split-Path -Parent $modDir
$logPath = Join-Path $modDir 'ucf_mod.log'
$atPath  = Join-Path $modDir 'autotest.txt'
$cmdPath = Join-Path $modDir '_autotest.cmd'

if (-not $NoKill) {
    Get-Process UnityCrossFire -ErrorAction SilentlyContinue | Stop-Process -Force
    Start-Sleep -Seconds 1
}
if (Test-Path -LiteralPath $logPath) {
    Move-Item -LiteralPath $logPath -Destination (Join-Path $modDir ('ucf_mod.prev_' + (Get-Date -Format 'HHmmss') + '.log')) -Force
}
if (Test-Path -LiteralPath $atPath) { Remove-Item -LiteralPath $atPath -Force }

$lines = @(
    '@echo off',
    'set UCF_MOD=1',
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