param([string[]]$Env = @(), [int]$Lobby = 42, [int]$Wait = 90, [switch]$SkipDeploy)
$ErrorActionPreference = 'Stop'
$gd = 'D:/BaiduNetdiskDownload/UnityCrossFire1.7.1/UnityCrossFire1.7.1'
$mod = 'D:/trae_project/ucf1.7-modifier/06-测试/ucf_mod'
$moddir = Join-Path $gd 'mod_tmpdir'
$moddir = Join-Path $gd 'ucf_mod'
$src = Join-Path $mod 'build/ucf_mod.dll'
$dst = Join-Path $moddir 'ucf_mod.dll'
$log = Join-Path $moddir 'ucf_mod.log'
$cs = @'
using System;
using System.Runtime.InteropServices;
public class X {
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, IntPtr p);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool at);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern bool GetClientRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
}
'@
Add-Type -TypeDefinition $cs
[X]::SetProcessDPIAware() | Out-Null
Get-Process -Name UnityCrossFire -ErrorAction SilentlyContinue | ForEach-Object { $_.Kill(); Start-Sleep -Milliseconds 900 }
if (-not $SkipDeploy) {
  if (Test-Path $dst) { Copy-Item $dst (Join-Path $moddir ('ucf_mod.dll.bak-' + (Get-Date -Format 'HHmmss'))) -Force }
  Copy-Item $src $dst -Force
  Write-Output ('deployed ' + (Get-Item $dst).Length + ' bytes')
}
if (Test-Path $log) { Move-Item $log (Join-Path $moddir ('ucf_mod.prev_' + (Get-Date -Format 'HHmmss') + '.log')) -Force }
$env:UCF_MOD = '1'
$env:UCF_NAV_READONLY = '1'
foreach ($e in $Env) { $kv = $e.Split('='); [Environment]::SetEnvironmentVariable($kv[0], $kv[1], 'Process') }
Write-Output ('env: ' + ($Env -join ' '))
$p = Start-Process -FilePath (Join-Path $gd 'UnityCrossFire.exe') -WorkingDirectory $gd -PassThru
Start-Sleep -Seconds $Lobby
if ($p.HasExited) { Write-Output ('exited early ' + $p.ExitCode); return }
$h = (Get-Process -Id $p.Id).MainWindowHandle
$fg = [X]::GetForegroundWindow()
$fgt = [X]::GetWindowThreadProcessId($fg, [IntPtr]::Zero)
$me = [X]::GetCurrentThreadId()
[X]::AttachThreadInput($me, $fgt, $true) | Out-Null
[X]::ShowWindow($h, 9) | Out-Null
[X]::BringWindowToTop($h) | Out-Null
[X]::SetForegroundWindow($h) | Out-Null
[X]::AttachThreadInput($me, $fgt, $false) | Out-Null
Start-Sleep -Milliseconds 700
$cr = New-Object X+RECT; [X]::GetClientRect($h, [ref]$cr) | Out-Null
$pt = New-Object X+POINT
$pt.X = [int]($cr.R * 0.842); $pt.Y = [int]($cr.B * 0.730)
[X]::ClientToScreen($h, [ref]$pt) | Out-Null
Write-Output ('click ' + $pt.X + ',' + $pt.Y + ' fg=' + [X]::GetForegroundWindow() + ' target=' + $h)
[X]::SetCursorPos($pt.X, $pt.Y) | Out-Null
Start-Sleep -Milliseconds 300
[X]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)
Start-Sleep -Milliseconds 150
[X]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)
$deadline = (Get-Date).AddSeconds($Wait)
$res = 'none'
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Milliseconds 800
  if (Test-Path $log) {
    $t = Get-Content -LiteralPath $log -Tail 200
    if ($t -match 'crash code') { $res = 'CRASH'; break }
  }
  if ($p.HasExited) { $res = 'EXIT ' + $p.ExitCode; break }
}
Write-Output ('result: ' + $res)
if (Test-Path $log) {
  $keep = Get-Content -LiteralPath $log | Where-Object { $_ -match 'ui:|compass:|crash code|access read|reg eax|PointGraph \(tick (8|16|24|32|40|48|56|64|72|80|88|96|104|112|120|128|136|144|152|160|168|176|184|192|200|208|216|224|232|240|248|256|264|272|280|288|296|304|312|320|328|336|344|352|360|368|376|384|392|400|408|416|424|432|440|448|456|464|472|480|488|496|504|512|520|528|536|544|552|560|568|576|584|592|600|608|616|624|632|640|648|656|664|672|680|688|696|704|712|720|728|736|744|752|760|768|776|784|792|800|808|816|824|832|840|848|856|864|872|880|888|896|904|912|920|928|936|944|952|960|968|976|984|992|1000)\)' -or $_ -match 'scene astar' }
  $keep | Select-Object -Last 120 | Out-String -Width 300
}
