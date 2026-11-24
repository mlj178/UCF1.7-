$ErrorActionPreference='Continue'
Get-Process UnityCrossFire -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Milliseconds 800
Start-Process -FilePath 'D:/ucf_test_level12/game/UnityCrossFire.exe' | Out-Null
Write-Output 'launched'
Start-Sleep -Seconds 15
& 'D:/ucf_unity/gt.ps1' -Action click -X 474 -Y 392 | Out-Null
Start-Sleep -Milliseconds 1200
& 'D:/ucf_unity/gt.ps1' -Action click -X 390 -Y 485 | Out-Null
Start-Sleep -Milliseconds 1200
& 'D:/ucf_unity/gt.ps1' -Action snap -Out 'D:/ucf_unity/shots/T0_room.png' | Out-Null
& 'D:/ucf_unity/gt.ps1' -Action click -X 1171 -Y 664 | Out-Null
Start-Sleep -Seconds 10
& 'D:/ucf_unity/gt.ps1' -Action snap -Out 'D:/ucf_unity/shots/T1_10s.png' | Out-Null
Start-Sleep -Seconds 10
& 'D:/ucf_unity/gt.ps1' -Action snap -Out 'D:/ucf_unity/shots/T2_20s.png' | Out-Null
Write-Output 'done'