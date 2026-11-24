Get-Process UnityCrossFire -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 500
$p = Start-Process -FilePath 'D:/ucf_test_level12/game/UnityCrossFire.exe' -PassThru
Write-Output ('LAUNCHED pid=' + $p.Id)
Start-Sleep -Seconds 14
& 'D:/ucf_unity/gt.ps1' -Action info
& 'D:/ucf_unity/gt.ps1' -Action snap -Out 'D:/ucf_unity/shots/01_menu.png'