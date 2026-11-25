<#
.SYNOPSIS
    编译 ucf_mod.dll（可选同步到 run\payload 部署弹药库）

.EXAMPLE
    .\app\tools\build.ps1              # 只编译，产物进 run\build\
    .\app\tools\build.ps1 -Payload     # 编译并更新 run\payload\ucf_mod\ucf_mod.dll
    .\app\tools\build.ps1 -Deploy      # 旧参数，等同 -Payload（不再写游戏目录）
#>
param(
    [switch]$Payload,
    [switch]$Deploy,
    [string]$Gcc = 'D:\Program Files\mingw32\bin\gcc.exe'
)

$ErrorActionPreference = 'Stop'
$tools = $PSScriptRoot
# 项目根：向上找 .ucfroot（和 core/ucf_paths.py 同一套约定），不靠目录层级猜
$root = $tools
while (-not (Test-Path -LiteralPath (Join-Path $root '.ucfroot')) -and (Split-Path -Parent $root) -ne $root) {
    $root = Split-Path -Parent $root
}
$src   = Join-Path $root 'src'
$build = Join-Path $root 'run\build'
$sources = @('cfg.c', 'plugin.c', 'navfix.c', 'editor.c', 'autotest.c')

# ---- gcc ----
if (-not (Test-Path -LiteralPath $Gcc)) {
    $cmd = Get-Command gcc -ErrorAction SilentlyContinue
    if (-not $cmd) { throw "找不到 gcc：用 -Gcc 指定（试过 $Gcc）" }
    $Gcc = $cmd.Source
}

# ---- 版本标记 ----
$stamp = Get-Date -Format 'yyyyMMdd-HHmm'
$gitShort = ''
try { Push-Location $root; $gitShort = (git rev-parse --short HEAD 2>$null) } catch { } finally { Pop-Location }
if (-not $gitShort) { $gitShort = 'nogit' }
$name = "ucf_mod-$stamp-$gitShort.dll"
$out  = Join-Path $build $name
New-Item -ItemType Directory -Force -Path $build | Out-Null

# ---- 编译 ----
Push-Location $src
try {
    # -Werror=unused-function / unused-variable：定义了没人用的函数或变量直接编译失败。
    # 2026-11-16 的教训：plugin.c 里有个 read_config() 从没被调用，导致
    # ucf_mod.json 整个文件是死的却没人发现。用它防复发。
    # -fno-omit-frame-pointer：崩溃栈里要能看到我们自己的帧。2026-11-17 那三次闪退
    # 的日志里一个 ucf_mod 帧都没有，就是因为 -O2 把 EBP 优化掉了，人工绕了一大圈。
    & $Gcc -O2 -fno-omit-frame-pointer -shared -o $out @sources -Werror=unused-function -Werror=unused-variable -luser32 -lgdi32 -static-libgcc
    if ($LASTEXITCODE -ne 0) { throw "gcc 失败（exit $LASTEXITCODE）" }
} finally { Pop-Location }

$item = Get-Item -LiteralPath $out
$sha  = (Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash
"编译完成 : $name"
"  大小   : $($item.Length) B"
"  SHA256 : $sha"

# ---- 记录 ----
$meta = [ordered]@{
    name    = $name
    bytes   = $item.Length
    sha256  = $sha
    built   = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
    gcc     = $Gcc
    git     = $gitShort
    sources = @($sources | ForEach-Object {
        [ordered]@{ file = $_; mtime = (Get-Item -LiteralPath (Join-Path $src $_)).LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss') }
    })
}
$meta | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $build 'build.json') -Encoding UTF8
Copy-Item -LiteralPath $out -Destination (Join-Path $build 'ucf_mod.dll') -Force

# ---- 同步到 payload（可选；不再往任何游戏目录写 dll）----
if ($Payload -or $Deploy) {
    if ($Deploy -and -not $Payload) { "注意：-Deploy 已改为只更新 payload，不再写游戏目录。" }
    $pdir = Join-Path $root 'run\payload\ucf_mod'
    New-Item -ItemType Directory -Force -Path $pdir | Out-Null
    Copy-Item -LiteralPath $out -Destination (Join-Path $pdir 'ucf_mod.dll') -Force
    $live = Get-Item -LiteralPath (Join-Path $pdir 'ucf_mod.dll')
    "已更新 payload: $($live.FullName)"
    "  $($live.Length) B  sha256=$((Get-FileHash -LiteralPath $live.FullName -Algorithm SHA256).Hash.Substring(0,16))…"
    "游戏目录不写 dll；控制台启动时用 UCF_MOD_DLL 直接加载 run\build\ucf_mod.dll。"
}
