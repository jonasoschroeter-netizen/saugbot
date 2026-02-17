# 🔧 SSH ohne Bildschirm aktivieren

## Problem: SSH funktioniert nicht (Connection timed out)

## Lösung 1: SSH über SD-Karte aktivieren (EINFACHSTE)

### Schritt 1: SD-Karte aus dem Raspberry Pi nehmen

### Schritt 2: SD-Karte in den Computer stecken

### Schritt 3: SSH-Datei erstellen

**Auf Windows:**
1. Öffne den Datei-Explorer
2. Gehe zur SD-Karte (z.B. `boot:` Laufwerk)
3. Erstelle eine **leere Datei** namens `ssh` (ohne Endung!)
   - Rechtsklick → Neu → Textdokument
   - Benenne um zu `ssh` (ohne .txt!)
   - Windows warnt dich - klicke "Ja"

**Oder per PowerShell:**
```powershell
# Finde das boot-Laufwerk (z.B. E:)
New-Item -Path "E:\ssh" -ItemType File
```

### Schritt 4: SD-Karte zurück in Raspberry Pi

### Schritt 5: Raspberry Pi starten

### Schritt 6: SSH-Verbindung testen

```bash
ssh pi@192.168.0.5
# Password: 123456789
```

## Lösung 2: SSH über config.txt aktivieren

Falls Lösung 1 nicht funktioniert:

1. SD-Karte in Computer
2. Öffne `config.txt` im boot-Verzeichnis
3. Füge am Ende hinzu:
   ```
   enable_uart=1
   ```
4. Speichere und starte Pi neu

## Lösung 3: WLAN-Konfiguration prüfen

Falls SSH aktiviert ist, aber Verbindung nicht funktioniert:

1. Prüfe ob Pi im gleichen Netzwerk ist
2. Prüfe Firewall-Einstellungen
3. Prüfe ob Port 22 offen ist

## Nach SSH-Aktivierung: Cron-Job installieren

```bash
ssh pi@192.168.0.5
cd ~/saugbot
git pull
chmod +x install_cron_job.sh
./install_cron_job.sh
```

## Alternative: Web-Interface manuell starten

Falls SSH funktioniert, aber Cron-Job nicht installiert werden soll:

```bash
ssh pi@192.168.0.5 "cd ~/saugbot && export PYTHONPATH=\$HOME/saugbot:\$PYTHONPATH && nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &"
```

## Schnelltest nach SSH-Aktivierung

```bash
# Teste Verbindung
ssh pi@192.168.0.5 "echo 'SSH funktioniert!'"

# Installiere Cron-Job
ssh pi@192.168.0.5 "cd ~/saugbot && git pull && chmod +x install_cron_job.sh && ./install_cron_job.sh"
```
