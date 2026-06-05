param(
    [string]$LogPath = "D:\trae_project\Universal-Dear-ImGui-Hook\esp_debug.log",
    [int]$Tail = 2000
)

if (-not (Test-Path -LiteralPath $LogPath)) {
    Write-Host "[ERROR] Log file not found: $LogPath"
    exit 1
}

try {
    $lines = Get-Content -LiteralPath $LogPath -Tail $Tail -ErrorAction Stop
} catch {
    Write-Host "[ERROR] Failed to read log: $($_.Exception.Message)"
    exit 1
}

function Count-Matches([string]$Pattern) {
    return @($lines | Select-String -Pattern $Pattern).Count
}

$signals = [ordered]@{
    "Bridge initialized"       = Count-Matches "\[IL2CPPBridge\] Initialized successfully"
    "GM waiting"               = Count-Matches "GameManager not available|GameManager unavailable|not available yet"
    "GM session changes"       = Count-Matches "GameManager instance changed"
    "Session clears"           = Count-Matches "Clearing session state"
    "Player list reads"        = Count-Matches "\[GameManager\] Got [0-9]+ unique players"
    "Dead=true samples"        = Count-Matches "IsPlayerDead\(.*\) = 1"
    "Dead=false samples"       = Count-Matches "IsPlayerDead\(.*\) = 0"
    "ESP draw summaries"       = Count-Matches "\[ESP\] Players:"
    "Rejected bad positions"   = Count-Matches "Rejected .* position"
    "Draw access violations"   = Count-Matches "DrawPlayerESP access violation"
}

Write-Host "ESP runtime log summary"
Write-Host "Log: $LogPath"
Write-Host "Lines inspected: $($lines.Count)"
Write-Host ""

foreach ($key in $signals.Keys) {
    "{0,-24} {1}" -f $key, $signals[$key]
}

Write-Host ""
Write-Host "Interpretation:"
Write-Host "- Pre-room injection is healthy if GM waiting appears without a crash."
Write-Host "- Leaving-room handling is healthy if session clears appear when exiting, without a crash."
Write-Host "- Death filtering has evidence when Dead=true samples appear and ESP draw continues."
Write-Host "- Position filtering has evidence when Rejected bad positions appears."
Write-Host "- Draw access violations should stay 0; if nonzero, the SEH guard prevented a frame-breaking crash."
