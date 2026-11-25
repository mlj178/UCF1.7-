<#
.SYNOPSIS
    重建 winhttp.dll 代理外壳（ucf_mod 的加载器）

.DESCRIPTION
    1) 从参考 DLL 的 PE 导出表重建 winhttp.def（92 个转发，全部指向 winhttp_orig.<同名>）
    2) 用 mingw32 gcc 编译 proxy.c + winhttp.def
    3) 编译产物与参考 DLL 逐一比对导出名，少一个就报错

    -Ref 默认用 payload\winhttp.dll（= 线上正在用的那份，导出表是权威）；
    也可以指向 C:\Windows\SysWOW64\winhttp.dll，导出名一致（只是那边没有转发）。

.EXAMPLE
    .\build_proxy.ps1
    .\build_proxy.ps1 -Ref 'C:\Windows\SysWOW64\winhttp.dll'
#>
param(
    [string]$Ref = '',
    [string]$OutDir = '',
    [string]$Gcc = 'D:\Program Files\mingw32\bin\gcc.exe',
    [switch]$SkipDef
)

$ErrorActionPreference = 'Stop'
$here = $PSScriptRoot
# 项目根：向上找 .ucfroot（和 core/ucf_paths.py 同一套约定）
$proj = $here
while (-not (Test-Path -LiteralPath (Join-Path $proj '.ucfroot')) -and (Split-Path -Parent $proj) -ne $proj) {
    $proj = Split-Path -Parent $proj
}

if (-not $Ref)    { $Ref = Join-Path $proj 'run\payload\winhttp.dll' }
if (-not $OutDir) { $OutDir = Join-Path $proj 'run\build\proxy' }
if (-not (Test-Path -LiteralPath $Ref)) { throw "参考 DLL 不存在：$Ref" }

function Rva2Off([uint32]$rva) {
    foreach ($s in $script:secTable) {
        $span = [Math]::Max($s.VSize, $s.RSize)
        if ($rva -ge $s.VA -and $rva -lt ($s.VA + $span)) {
            return [int]($rva - $s.VA + $s.Raw)
        }
    }
    return -1
}

function Get-ExportNames([string]$Path) {
    $b = [System.IO.File]::ReadAllBytes($Path)
    $pe = [BitConverter]::ToInt32($b, 0x3C)
    if ($b[$pe] -ne 0x50 -or $b[$pe + 1] -ne 0x45) { throw "不是 PE 文件：$Path" }
    $coff    = $pe + 4
    $nSec    = [BitConverter]::ToUInt16($b, $coff + 2)
    $optSize = [BitConverter]::ToUInt16($b, $coff + 16)
    $opt     = $coff + 20
    $magic   = [BitConverter]::ToUInt16($b, $opt)
    $dd      = if ($magic -eq 0x20b) { $opt + 112 } else { $opt + 96 }
    $expRva  = [BitConverter]::ToUInt32($b, $dd)
    if ($expRva -eq 0) { throw "该文件没有导出表：$Path" }

    $secOff = $opt + $optSize
    $secs = @()
    for ($i = 0; $i -lt $nSec; $i++) {
        $s = $secOff + $i * 40
        $secs += [pscustomobject]@{
            VA    = [BitConverter]::ToUInt32($b, $s + 12)
            VSize = [BitConverter]::ToUInt32($b, $s + 8)
            Raw   = [BitConverter]::ToUInt32($b, $s + 20)
            RSize = [BitConverter]::ToUInt32($b, $s + 16)
        }
    }
    $script:secTable = $secs

    $eo       = Rva2Off $expRva
    $nNames   = [BitConverter]::ToUInt32($b, $eo + 24)
    $namesRva = [BitConverter]::ToUInt32($b, $eo + 32)
    $names = @()
    for ($i = 0; $i -lt $nNames; $i++) {
        $nameRva = [BitConverter]::ToUInt32($b, (Rva2Off $namesRva) + $i * 4)
        $o = Rva2Off $nameRva
        $e = $o
        while ($b[$e] -ne 0) { $e++ }
        $names += [Text.Encoding]::ASCII.GetString($b, $o, $e - $o)
    }
    return $names
}

# ---- 1) 参考导出表 ----
$refNames = @(Get-ExportNames -Path $Ref)
"参考 DLL   : $Ref"
"导出数量   : $($refNames.Count)"

# ---- 2) winhttp.def ----
$defPath = Join-Path $here 'winhttp.def'
if (-not $SkipDef) {
    $lines = New-Object System.Collections.Generic.List[string]
    $lines.Add('; winhttp.def - 代理外壳的导出表（由 build_proxy.ps1 自动生成，勿手改）')
    $lines.Add("; 来源: $Ref")
    $lines.Add('; 生成: ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
    $lines.Add('LIBRARY winhttp')
    $lines.Add('EXPORTS')
    foreach ($n in $refNames) { $lines.Add("$n=winhttp_orig.$n") }
    [IO.File]::WriteAllText($defPath, ($lines -join [Environment]::NewLine), (New-Object Text.UTF8Encoding($false)))
    "已重建     : winhttp.def（$($refNames.Count) 条）"
} else {
    "跳过 def   : 使用现有 winhttp.def"
}

# ---- 3) 编译 ----
if (-not (Test-Path -LiteralPath $Gcc)) { throw "找不到 gcc：$Gcc" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$out = Join-Path $OutDir 'winhttp.dll'

Push-Location $here
try {
    $gccArgs = @('-O2', '-shared', '-o', $out, 'proxy.c', 'winhttp.def', '-static-libgcc', '-Wl,--enable-stdcall-fixup')
    & $Gcc @gccArgs 2>&1 | ForEach-Object { "  $_" }
    if ($LASTEXITCODE -ne 0) { throw "gcc 失败（exit $LASTEXITCODE）" }
} finally { Pop-Location }

$item = Get-Item -LiteralPath $out
"编译完成   : $out"
"  大小     : $($item.Length) B"
"  SHA256   : $((Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash)"

# ---- 4) 校验 ----
$newNames = @(Get-ExportNames -Path $out)
$missing = @($refNames | Where-Object { $newNames -notcontains $_ })
$extra   = @($newNames | Where-Object { $refNames -notcontains $_ })

"校验导出   : 新 $($newNames.Count) / 参考 $($refNames.Count)"
if ($missing.Count) { "  [X] 缺少: " + ($missing -join ', '); exit 2 }
if ($extra.Count)   { "  [!] 多出: " + ($extra -join ', ') }
"  [OK] 导出表一致"
