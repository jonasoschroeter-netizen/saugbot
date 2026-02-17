# PowerShell-Script zum Fixen von HDMI-Problemen
# Fügt HDMI-Einstellungen zu config.txt hinzu

Write-Host "=========================================="
Write-Host "  HDMI-Fix für Raspberry Pi"
Write-Host "=========================================="
Write-Host ""

# Finde boot-Laufwerk
$bootDrive = Get-Volume | Where-Object { 
    $_.DriveType -eq 'Removable' -or 
    $_.FileSystemLabel -eq 'boot' -or
    $_.FileSystemLabel -eq 'bootfs'
} | Select-Object -First 1

if (-not $bootDrive) {
    Write-Host "FEHLER: Boot-Laufwerk nicht gefunden!"
    Write-Host ""
    Write-Host "Bitte:"
    Write-Host "1. SD-Karte aus Raspberry Pi nehmen"
    Write-Host "2. SD-Karte in Computer stecken"
    Write-Host "3. Script erneut ausführen"
    exit 1
}

$bootPath = "$($bootDrive.DriveLetter):\"
$configFile = "$bootPath\config.txt"

Write-Host "Boot-Laufwerk gefunden: $bootPath"
Write-Host ""

# Prüfe ob config.txt existiert
if (-not (Test-Path $configFile)) {
    Write-Host "FEHLER: config.txt nicht gefunden!"
    Write-Host "Bitte prüfe ob SD-Karte korrekt gemountet ist"
    exit 1
}

# Prüfe ob HDMI-Einstellungen bereits vorhanden sind
$configContent = Get-Content $configFile -Raw
if ($configContent -match "hdmi_force_hotplug") {
    Write-Host "HDMI-Einstellungen sind bereits in config.txt"
    Write-Host "Möchtest du sie überschreiben? (j/n)"
    $response = Read-Host
    if ($response -ne "j" -and $response -ne "J") {
        Write-Host "Abgebrochen"
        exit 0
    }
}

# Backup erstellen
$backupFile = "$configFile.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $configFile $backupFile
Write-Host "Backup erstellt: $backupFile"
Write-Host ""

# HDMI-Einstellungen hinzufügen
$hdmiSettings = @"

# HDMI Fix (hinzugefügt von fix_hdmi.ps1)
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
hdmi_drive=2
config_hdmi_boost=4
"@

# Entferne alte HDMI-Einstellungen (falls vorhanden)
$lines = Get-Content $configFile
$newLines = @()
$skipNext = $false
$inHdmiSection = $false

foreach ($line in $lines) {
    if ($line -match "^# HDMI Fix") {
        $inHdmiSection = $true
        $skipNext = $true
        continue
    }
    if ($inHdmiSection -and ($line -match "^hdmi_" -or $line -match "^config_hdmi")) {
        continue
    }
    if ($inHdmiSection -and $line -eq "") {
        $inHdmiSection = $false
    }
    if (-not $skipNext) {
        $newLines += $line
    }
    $skipNext = $false
}

# Füge neue HDMI-Einstellungen hinzu
$newLines += $hdmiSettings

# Schreibe config.txt neu
$newLines | Set-Content $configFile -Encoding ASCII

Write-Host "✅ config.txt aktualisiert!"
Write-Host ""
Write-Host "Hinzugefügte Einstellungen:"
Write-Host "  - hdmi_force_hotplug=1"
Write-Host "  - hdmi_group=2"
Write-Host "  - hdmi_mode=82 (1080p)"
Write-Host "  - hdmi_drive=2"
Write-Host "  - config_hdmi_boost=4"
Write-Host ""
Write-Host "=========================================="
Write-Host "  ✅ HDMI-Fix abgeschlossen!"
Write-Host "=========================================="
Write-Host ""
Write-Host "Nächste Schritte:"
Write-Host "1. SD-Karte sicher entfernen"
Write-Host "2. SD-Karte zurück in Raspberry Pi"
Write-Host "3. Raspberry Pi starten"
Write-Host "4. Bildschirm sollte jetzt Signal zeigen"
Write-Host ""
