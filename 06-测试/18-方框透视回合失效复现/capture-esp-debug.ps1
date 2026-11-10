<#
.SYNOPSIS
    捕获本机 OutputDebugStringA 输出（等价于 Sysinternals DebugView），
    用来抓 Universal-ImGui-Hook.dll Release 版打到调试器的日志。

.DESCRIPTION
    发布版 DLL 不写 esp_debug.log（stdafx.h 里落盘代码被注释），只会
    OutputDebugStringA。DLL 每 60 帧打一行 [ESP] ...，管道命令打
    [PipeServer] State updated / State update ignored，会话变化打
    [GameManager] / [IL2CPPBridge] / [ESPData]。

    注意：DBWIN_BUFFER 每个会话只能有一个监听者。用本脚本时请关掉
    DebugView / Visual Studio 调试器，否则两边会互相抢消息。

.PARAMETER OutFile
    捕获日志路径，默认脚本同目录 esp_debug_capture.log（追加写）。

.PARAMETER Seconds
    监听秒数；0 = 一直录到 Ctrl+C。

.PARAMETER Filter
    只保留包含该子串的行（不区分大小写）；空 = 全收。

.PARAMETER EmitText
    自检用：不监听，只把这段文本 OutputDebugString 出去然后退出。

.EXAMPLE
    pwsh -File capture-esp-debug.ps1 -Seconds 600

.EXAMPLE
    pwsh -File capture-esp-debug.ps1 -Filter "ESP" -OutFile D:\esp.log
#>
[CmdletBinding()]
param(
    [string]$OutFile = '',
    [int]$Seconds = 0,
    [string]$Filter = '',
    [string]$EmitText = ''
)

Add-Type -Namespace DbWin -Name Native -MemberDefinition @'
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true, CharSet=System.Runtime.InteropServices.CharSet.Unicode)]
public static extern System.IntPtr CreateFileMapping(System.IntPtr hFile, System.IntPtr lpAttributes, uint flProtect, uint dwMaximumSizeHigh, uint dwMaximumSizeLow, string lpName);
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true)]
public static extern System.IntPtr MapViewOfFile(System.IntPtr hFileMappingObject, uint dwDesiredAccess, uint dwFileOffsetHigh, uint dwFileOffsetLow, uint dwNumberOfBytesToMap);
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true, CharSet=System.Runtime.InteropServices.CharSet.Unicode)]
public static extern System.IntPtr CreateEvent(System.IntPtr lpEventAttributes, bool bManualReset, bool bInitialState, string lpName);
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true)]
public static extern bool SetEvent(System.IntPtr hEvent);
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true)]
public static extern uint WaitForSingleObject(System.IntPtr hHandle, uint dwMilliseconds);
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true)]
public static extern bool UnmapViewOfFile(System.IntPtr lpBaseAddress);
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true)]
public static extern bool CloseHandle(System.IntPtr hObject);
[System.Runtime.InteropServices.DllImport("kernel32.dll", SetLastError=true, CharSet=System.Runtime.InteropServices.CharSet.Ansi)]
public static extern void OutputDebugStringA(string lpOutputString);
'@

if (-not $OutFile) {
    $base = if ($PSScriptRoot) { $PSScriptRoot } else { (Get-Location).Path }
    $OutFile = Join-Path $base 'esp_debug_capture.log'
}

if ($EmitText) {
    [DbWin.Native]::OutputDebugStringA($EmitText)
    return
}

$PAGE_READWRITE = 0x04
$FILE_MAP_ALL_ACCESS = 0x0002
$WAIT_OBJECT_0 = 0

$map = [DbWin.Native]::CreateFileMapping([IntPtr]::Zero, [IntPtr]::Zero, $PAGE_READWRITE, 0, 4096, 'DBWIN_BUFFER')
if ($map -eq [IntPtr]::Zero) {
    throw "CreateFileMapping(DBWIN_BUFFER) failed: $([System.ComponentModel.Win32Exception]::new([System.Runtime.InteropServices.Marshal]::GetLastWin32Error()).Message)"
}
$view = [DbWin.Native]::MapViewOfFile($map, $FILE_MAP_ALL_ACCESS, 0, 0, 4096)
if ($view -eq [IntPtr]::Zero) {
    throw "MapViewOfFile failed: $([System.ComponentModel.Win32Exception]::new([System.Runtime.InteropServices.Marshal]::GetLastWin32Error()).Message)"
}
$ready = [DbWin.Native]::CreateEvent([IntPtr]::Zero, $false, $false, 'DBWIN_BUFFER_READY')
$dataReady = [DbWin.Native]::CreateEvent([IntPtr]::Zero, $false, $false, 'DBWIN_DATA_READY')

$writer = [System.IO.StreamWriter]::new($OutFile, $true, [System.Text.Encoding]::UTF8)
$writer.AutoFlush = $true

$mode = if ($Seconds -gt 0) { "$Seconds seconds" } else { "until Ctrl+C" }
Write-Host "Capturing OutputDebugString -> $OutFile ($mode)"
if ($Filter) { Write-Host "Filter: $Filter" }

$stopAt = if ($Seconds -gt 0) { (Get-Date).AddSeconds($Seconds) } else { [datetime]::MaxValue }
$procNames = @{}
$lines = 0

try {
    while ((Get-Date) -lt $stopAt) {
        [void][DbWin.Native]::SetEvent($ready)
        if ([DbWin.Native]::WaitForSingleObject($dataReady, 500) -ne $WAIT_OBJECT_0) { continue }

        $msgPid = [System.Runtime.InteropServices.Marshal]::ReadInt32($view)
        $text = [System.Runtime.InteropServices.Marshal]::PtrToStringAnsi([IntPtr]::Add($view, 4))
        if ($null -eq $text) { $text = '' }
        $text = $text.TrimEnd([char]13, [char]10)

        if ($Filter -and ($text.IndexOf($Filter, [StringComparison]::OrdinalIgnoreCase) -lt 0)) { continue }

        if (-not $procNames.ContainsKey($msgPid)) {
            try { $procNames[$msgPid] = (Get-Process -Id $msgPid -ErrorAction Stop).ProcessName } catch { $procNames[$msgPid] = '?' }
        }
        $stamp = (Get-Date).ToString('HH:mm:ss.fff')
        $writer.WriteLine("[$stamp] [$msgPid $($procNames[$msgPid])] $text")
        $lines++
    }
}
finally {
    Write-Host "Wrote $lines lines"
    $writer.Dispose()
    [void][DbWin.Native]::UnmapViewOfFile($view)
    [void][DbWin.Native]::CloseHandle($ready)
    [void][DbWin.Native]::CloseHandle($dataReady)
    [void][DbWin.Native]::CloseHandle($map)
}
