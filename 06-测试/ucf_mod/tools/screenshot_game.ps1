<#
.SYNOPSIS
    抓一张游戏窗口的截图（PrintWindow，不需要窗口在前台）。

.EXAMPLE
    .\tools\screenshot_game.ps1
    .\tools\screenshot_game.ps1 -Out 'docs\shot.png'
#>
param([string]$Out = '')
$ErrorActionPreference = 'Continue'
if (-not $Out) { $Out = Join-Path $PSScriptRoot '..\_shots\game.png' }
Add-Type -AssemblyName System.Drawing
$src = @'
using System;
using System.Runtime.InteropServices;
public class UcfShot {
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L,T,R,B; }
}
'@
Add-Type -TypeDefinition $src -Language CSharp
$p = Get-Process UnityCrossFire -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $p) { throw 'game not running' }
$h = $p.MainWindowHandle
if (-not $h -or $h -eq 0) { $p.Refresh(); $h = $p.MainWindowHandle }
if (-not $h -or $h -eq 0) { throw 'no main window' }
$r = New-Object UcfShot+RECT
[void][UcfShot]::GetWindowRect($h, [ref]$r)
$w = $r.R - $r.L; $hh = $r.B - $r.T
if ($w -le 0 -or $hh -le 0) { throw 'bad rect' }
$bmp = New-Object System.Drawing.Bitmap $w, $hh
$g = [System.Drawing.Graphics]::FromImage($bmp)
$hdc = $g.GetHdc()
[void][UcfShot]::PrintWindow($h, $hdc, 2)
$g.ReleaseHdc($hdc)
$g.Dispose()
$dir = Split-Path -Parent $Out
if ($dir -and -not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
"saved $Out ($w x $hh)"