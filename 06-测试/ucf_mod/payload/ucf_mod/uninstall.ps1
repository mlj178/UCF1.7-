# UCF 插件卸载 —— 默认只移除「部署物」，不动导航数据与工程源码
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
$deployFiles = @('ucf_mod.dll', 'ucf_mod.json', 'ucf_mod.log', 'collect.flag')
$deployDirs  = @('vis')
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
Get-ChildItem -LiteralPath $root -File -Force | Where-Object { $_.Name -like 'ucf_mod.log.prev*' } |
    ForEach-Object { Remove-Checked $_.FullName '日志轮转' }
foreach ($d in $deployDirs) { Remove-Checked (Join-Path $root $d) '采集输出' }

# 4) 可选：删数据
if ($Purge) {
    foreach ($d in $dataDirs) { Remove-Checked (Join-Path $root $d) '导航数据' }
    "  已 -Purge：nav/markers/maps/backup 一并删除"
} else {
    "  已保留：$root\markers  backup（要彻底清掉请加 -Purge）"
}

if (-not $DryRun) { "卸载完成。" }
