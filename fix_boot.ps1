# PowerShell-Script zum Fixen von Boot-Problemen
# Fügt Boot-Fix-Einstellungen zu config.txt hinzu

Write-Host "=========================================="
Write-Host "  Boot-Fix für Raspberry Pi"
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

# Backup erstellen
$backupFile = "$configFile.backup.$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $configFile $backupFile
Write-Host "Backup erstellt: $backupFile"
Write-Host ""

# Boot-Fix-Einstellungen
$bootFixSettings = @"

# Boot-Fix (hinzugefügt von fix_boot.ps1)
# HDMI-Fix
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
hdmi_drive=2
hdmi_ignore_edid=0xa5000080
hdmi_blanking=0

# UART für Debugging
enable_uart=1
"@

# Entferne alte Boot-Fix-Einstellungen (falls vorhanden)
$lines = Get-Content $configFile
$newLines = @()
$inBootFixSection = $false

foreach ($line in $lines) {
    if ($line -match "^# Boot-Fix") {
        $inBootFixSection = $true
        continue
    }
    if ($inBootFixSection -and ($line -match "^hdmi_" -or $line -match "^enable_uart" -or $line -match "^config_hdmi")) {
        continue
    }
    if ($inBootFixSection -and $line -eq "" -and ($lines[$lines.IndexOf($line) + 1] -notmatch "^hdmi_" -and $lines[$lines.IndexOf($line) + 1] -notmatch "^enable_uart")) {
        $inBootFixSection = $false
    }
    if (-not $inBootFixSection) {
        $newLines += $line
    }
}

# Füge neue Boot-Fix-Einstellungen hinzu
$newLines += $bootFixSettings

# Schreibe config.txt neu
$newLines | Set-Content $configFile -Encoding ASCII

Write-Host "✅ config.txt aktualisiert!"
Write-Host ""
Write-Host "Hinzugefügte Einstellungen:"
Write-Host "  - hdmi_force_hotplug=1 (HDMI erzwingen)"
Write-Host "  - hdmi_mode=82 (1080p)"
Write-Host "  - hdmi_ignore_edid=0xa5000080 (EDID ignorieren)"
Write-Host "  - hdmi_blanking=0 (Bildschirm-Sleep deaktivieren)"
Write-Host "  - enable_uart=1 (UART für Debugging)"
Write-Host ""
Write-Host "=========================================="
Write-Host "  ✅ Boot-Fix abgeschlossen!"
Write-Host "=========================================="
Write-Host ""
Write-Host "Nächste Schritte:"
Write-Host "1. SD-Karte sicher entfernen"
Write-Host "2. SD-Karte zurück in Raspberry Pi"
Write-Host "3. Raspberry Pi starten"
Write-Host "4. Bildschirm sollte jetzt stabil bleiben"
Write-Host ""
Write-Host "Falls Bildschirm immer noch weg geht:"
Write-Host "- Prüfe ob Pi läuft: ping 192.168.0.5"
Write-Host "- Falls Pi läuft: SSH aktivieren und Web-Interface starten"
Write-Host ""
