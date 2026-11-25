# UCF 插件卸载 —— 默认只移除「部署物」，不动导航数据与工程源码
#
# 2026-11-25 起：新部署不再把本脚本放进游戏目录。卸载请用控制台「部署」页，
# 或 python app\tabs\deploy\deploy_mod.py --game-exe "D:\...\UnityCrossFire.exe" --uninstall。
# 本脚本只留作 2026-11-25 之前旧部署的手工清理。
#
#   默认：还原 level9 → 删加载器 → 删 dll/配置/日志/vis
#   保留：markers\ backup\（蹲守点 + level9 还原点；nav\ maps\ 已于 2026-11-21 清空）
#   -Purge  ：连 markers/backup 一起删（谨慎）
#   -DryRun ：只列出将要删除的东西，不执行
#
# 注意：2026-11-16 之前的旧版脚本会 Remove-Item -Recurse 整个 ucf_mod 目录，
#       等于把源码和导航数据一起删掉。本版已改为白名单删除。

param([switch]$Purge, [switch]$DryRun)

$ErrorActionPreference = 'SilentlyContinue'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$game = Split-Path -Parent $root

$loaders     = @('winhttp.dll', 'winhttp_orig.dll')                 # 游戏根
$deployFiles = @('ucf_mod.dll', 'ucf_mod.json', 'ucf_navcmd.txt', 'collect.flag')
$deployDirs  = @('vis', 'log')          # vis：旧采集输出；log：2026-11-23 起的日志目录
# 旧部署（2026-11-23 之前）把日志写在 ucf_mod\ 根目录，卸载时一并清掉
$legacyLogs  = @('ucf_mod.log', 'autotest.txt', 'player_marks.txt')
$dataDirs    = @('markers', 'backup')                                # 仅 -Purge 才删

function Remove-Checked($path, $what) {
    if (Test-Path -LiteralPath $path) {
        if ($DryRun) { "  [dry] 将删除 $what : $path" }
        else { Remove-Item -LiteralPath $path -Recurse -Force; "  已删除 $what : $path" }
    }
}

"== UCF 插件卸载 =="
if ($DryRun) { "（干跑模式：只列出，不执行）" }

# 1) 还原被修改的场景
$bak = Join-Path $root 'backup\level9.orig'
$lvl = Join-Path $game 'UnityCrossFire_Data\level9'
if (Test-Path -LiteralPath $bak) {
    if ($DryRun) { "  [dry] 将还原场景 level9" }
    else { Copy-Item -Force -LiteralPath $bak -Destination $lvl; "  已还原 level9" }
} else {
    "  !! backup\level9.orig 不存在，跳过场景还原"
}

# 2) 删加载器（游戏根）
foreach ($f in $loaders) { Remove-Checked (Join-Path $game $f) '加载器' }

# 3) 删部署物
foreach ($f in $deployFiles) { Remove-Checked (Join-Path $root $f) '部署文件' }
foreach ($d in $deployDirs) { Remove-Checked (Join-Path $root $d) '日志/采集输出' }
foreach ($f in $legacyLogs) { Remove-Checked (Join-Path $root $f) '旧日志（兼容）' }
Get-ChildItem -LiteralPath $root -File -Force |
    Where-Object { $_.Name -like 'ucf_mod.log.prev*' -or $_.Name -like 'ucf_mod.prev_*.log' } |
    ForEach-Object { Remove-Checked $_.FullName '旧日志轮转（兼容）' }

# 4) 可选：删数据
if ($Purge) {
    foreach ($d in $dataDirs) { Remove-Checked (Join-Path $root $d) '导航数据' }
    "  已 -Purge：nav/markers/maps/backup 一并删除"
} else {
    "  已保留：$root\markers  backup（要彻底清掉请加 -Purge）"
}

if (-not $DryRun) { "卸载完成。" }
