$ErrorActionPreference='SilentlyContinue'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$game = Split-Path -Parent $root
# 1) 还原被修改的场景
$bak = Join-Path $root 'backup\level9.orig'
if (Test-Path $bak) { Copy-Item -Force $bak (Join-Path $game 'UnityCrossFire_Data\level9'); 'level9 restored' }
# 2) 删除新增文件
Remove-Item -Force (Join-Path $game 'winhttp.dll')
Remove-Item -Force (Join-Path $game 'winhttp_orig.dll')
# 3) 删除插件目录（脚本自己也在里面，最后删）
Remove-Item -Recurse -Force $root
'uninstalled'