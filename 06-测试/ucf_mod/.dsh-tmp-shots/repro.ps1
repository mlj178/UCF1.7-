param([int]$WaitLobby = 40, [int]$WaitAfter = 40, [switch]$SkipDeploy)
$ErrorActionPreference = 'Stop'
$gd = 'D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1'
$mod = 'D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod'
$moddir = Join-Path $gd 'ucf_mod'
$src = Join-Path $mod 'build/ucf_mod.dll'
$dst = Join-Path $moddir 'ucf_mod.dll'
$log = Join-Path $moddir 'ucf_mod.log'
Add-Type -AssemblyName System.Drawing
$cs = @'
using System;
using System.Runtime.InteropServices;
public class R {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
}
'@
Add-Type -TypeDefinition $cs
[R]::SetProcessDPIAware() | Out-Null
Get-Process -Name UnityCrossFire -ErrorAction SilentlyContinue | ForEach-Object { $_.Kill(); Start-Sleep -Milliseconds 800 }
if (-not $SkipDeploy) {
  if (Test-Path $dst) { Copy-Item $dst (Join-Path $moddir ('ucf_mod.dll.bak-' + (Get-Date -Format 'HHmmss'))) -Force }
  Copy-Item $src $dst -Force
  Write-Output ('deployed ' + (Get-Item $dst).Length + ' bytes')
}
if (Test-Path $log) { Move-Item $log (Join-Path $moddir ('ucf_mod.prev_' + (Get-Date -Format 'HHmmss') + '.log')) -Force }
$env:UCF_MOD = '1'
$env:UCF_NAV_READONLY = '1'
$p = Start-Process -FilePath (Join-Path $gd 'UnityCrossFire.exe') -WorkingDirectory $gd -PassThru
Write-Output ('pid=' + $p.Id + ' waiting ' + $WaitLobby + 's for lobby')
Start-Sleep -Seconds $WaitLobby
if ($p.HasExited) { Write-Output ('game exited early code=' + $p.ExitCode) }
$h = (Get-Process -Id $p.Id).MainWindowHandle
Write-Output ('hwnd=' + $h)
$cr = New-Object R+RECT; [R]::GetClientRect($h, [ref]$cr) | Out-Null
Write-Output ('client=' + $cr.R + 'x' + $cr.B)
$cx = [int]($cr.R * 0.842); $cy = [int]($cr.B * 0.730)
$lp = [IntPtr](($cy * 65536) + $cx)
[R]::PostMessage($h, 0x0200, [IntPtr]0, $lp) | Out-Null
Start-Sleep -Milliseconds 150
[R]::PostMessage($h, 0x0201, [IntPtr]1, $lp) | Out-Null
Start-Sleep -Milliseconds 100
[R]::PostMessage($h, 0x0202, [IntPtr]0, $lp) | Out-Null
Write-Output ('posted click at client ' + $cx + ',' + $cy)
$deadline = (Get-Date).AddSeconds($WaitAfter)
$sawScene = $false
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Milliseconds 700
  if (Test-Path $log) {
    $tail = Get-Content -LiteralPath $log -Tail 500
    if ($tail -match 'scene astar=') { $sawScene = $true }
    if ($tail -match 'crash code') { Write-Output 'CRASH detected'; break }
  }
  if ($p.HasExited) { Write-Output ('process exited code=' + $p.ExitCode); break }
}
Write-Output ('sawScene=' + $sawScene + ' alive=' + (-not $p.HasExited))
if (Test-Path $log) { Get-Content -LiteralPath $log -Tail 80 | Out-String -Width 300 }
