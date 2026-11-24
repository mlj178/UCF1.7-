param(
  [string]$Action = "snap",
  [int]$X = 0,
  [int]$Y = 0,
  [string]$Out = "D:/ucf_unity/shots/shot.png",
  [string]$ProcName = "UnityCrossFire",
  [string]$Keys = ""
)

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

if (-not ("W32" -as [type])) {
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class W32 {
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left; public int Top; public int Right; public int Bottom; }
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
    [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, IntPtr e);
    [DllImport("shcore.dll")] public static extern int SetProcessDpiAwareness(int v);
    [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
}
"@
}

try { [void][W32]::SetProcessDpiAwareness(2) } catch { try { [void][W32]::SetProcessDPIAware() } catch {} }

$proc = Get-Process -Name $ProcName -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if (-not $proc) { Write-Output "NO_WINDOW"; exit 1 }
$h = $proc.MainWindowHandle

$r = New-Object W32+RECT
[void][W32]::GetWindowRect($h, [ref]$r)
$w = $r.Right - $r.Left
$ht = $r.Bottom - $r.Top

switch ($Action) {
  "info" { Write-Output ("WINDOW " + $r.Left + "," + $r.Top + " " + $w + "x" + $ht) }
  "snap" {
    $bmp = New-Object System.Drawing.Bitmap($w, $ht)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($r.Left, $r.Top, 0, 0, $bmp.Size)
    $dir = Split-Path -Parent $Out
    if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    $bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    Write-Output ("SAVED " + $Out + " " + $w + "x" + $ht)
  }
  "click" {
    [void][W32]::SetForegroundWindow($h)
    Start-Sleep -Milliseconds 300
    [void][W32]::SetCursorPos($r.Left + $X, $r.Top + $Y)
    Start-Sleep -Milliseconds 150
    [W32]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 90
    [W32]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)
    Write-Output ("CLICKED rel " + $X + "," + $Y + " abs " + ($r.Left+$X) + "," + ($r.Top+$Y))
  }
  "move" {
    [void][W32]::SetForegroundWindow($h)
    Start-Sleep -Milliseconds 200
    [void][W32]::SetCursorPos($r.Left + $X, $r.Top + $Y)
    Write-Output ("MOVED rel " + $X + "," + $Y)
  }
  "keys" {
    [void][W32]::SetForegroundWindow($h)
    Start-Sleep -Milliseconds 300
    [System.Windows.Forms.SendKeys]::SendWait($Keys)
    Write-Output ("SENT [" + $Keys + "]")
  }
  "focus" { [void][W32]::SetForegroundWindow($h); Write-Output "FOCUSED" }
}
