# 快速搜索函数位置
# 用法: .\搜索函数.ps1 "函数名关键字"

param([string]$keyword)

if (-not $keyword) {
    Write-Host "用法: .\搜索函数.ps1 '函数名关键字'"
    exit
}

$files = @(
    "GameAssembly_part1.lst",
    "GameAssembly_part2.lst", 
    "GameAssembly_part3.lst"
)

foreach ($file in $files) {
    $path = Join-Path $PSScriptRoot $file
    if (Test-Path $path) {
        $results = Select-String -Path $path -Pattern $keyword -Context 0,2 | Select-Object -First 5
        if ($results) {
            Write-Host "`n=== 找到于 $file ===" -ForegroundColor Green
            $results | ForEach-Object { Write-Host "$($_.LineNumber): $($_.Line.Trim())" }
        }
    }
}
