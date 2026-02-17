# PowerShell-Script zum Aktivieren von SSH auf Raspberry Pi
# Erstellt eine ssh-Datei auf dem boot-Laufwerk

Write-Host "=========================================="
Write-Host "  SSH auf Raspberry Pi aktivieren"
Write-Host "=========================================="
Write-Host ""

# Finde boot-Laufwerk
$bootDrive = Get-Volume | Where-Object { $_.DriveType -eq 'Removable' -or $_.FileSystemLabel -eq 'boot' } | Select-Object -First 1

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

Write-Host "Boot-Laufwerk gefunden: $bootPath"
Write-Host ""

# Prüfe ob ssh-Datei bereits existiert
if (Test-Path "$bootPath\ssh") {
    Write-Host "SSH ist bereits aktiviert (ssh-Datei existiert)"
    exit 0
}

# Erstelle ssh-Datei
try {
    New-Item -Path "$bootPath\ssh" -ItemType File -Force | Out-Null
    Write-Host "✅ SSH-Datei erstellt: $bootPath\ssh"
    Write-Host ""
    Write-Host "=========================================="
    Write-Host "  ✅ SSH aktiviert!"
    Write-Host "=========================================="
    Write-Host ""
    Write-Host "Nächste Schritte:"
    Write-Host "1. SD-Karte sicher entfernen"
    Write-Host "2. SD-Karte zurück in Raspberry Pi"
    Write-Host "3. Raspberry Pi starten"
    Write-Host "4. Warte 30 Sekunden"
    Write-Host "5. Teste SSH: ssh pi@192.168.0.5"
    Write-Host ""
} catch {
    Write-Host "FEHLER: Konnte ssh-Datei nicht erstellen: $_"
    Write-Host ""
    Write-Host "Manuell erstellen:"
    Write-Host "1. Öffne Datei-Explorer"
    Write-Host "2. Gehe zu: $bootPath"
    Write-Host "3. Erstelle leere Datei namens 'ssh' (ohne Endung!)"
    exit 1
}
