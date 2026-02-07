# SSH am Raspberry Pi aktivieren

## Problem:
SSH-Verbindung zu 192.168.0.5 schlägt fehl - SSH ist nicht aktiviert.

## Lösung: SSH aktivieren

### Option 1: Mit Monitor (EINFACHSTE METHODE)

1. **HDMI-Kabel** vom Pi zum Monitor/TV
2. **USB-Tastatur** anschließen
3. Am Pi einloggen:
   - User: `pi`
   - Password: `123456789`
4. SSH aktivieren:
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
   sudo systemctl status ssh
   ```
5. Prüfe ob SSH läuft:
   ```bash
   sudo systemctl status ssh
   ```
   Sollte "active (running)" anzeigen.

### Option 2: SSH-Datei erstellen (Headless)

Falls du keinen Monitor hast, kannst du die SD-Karte in den Computer stecken:

1. SD-Karte aus Pi entfernen
2. In Computer/Laptop stecken
3. Im Boot-Partition eine leere Datei erstellen:
   - Dateiname: `ssh` (ohne Endung!)
   - In das `boot` Verzeichnis der SD-Karte
4. SD-Karte wieder in Pi stecken
5. Pi booten lassen

### Option 3: Raspberry Pi Imager (beim Flashing)

Falls du neu flashen musst:
- Im Raspberry Pi Imager: Settings → Enable SSH
- User/Password setzen

## Nach SSH-Aktivierung:

```bash
ssh pi@192.168.0.5
# Password: 123456789
```

## Dann Setup-Script ausführen:

```bash
cd ~
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
chmod +x setup_raspi.sh
bash setup_raspi.sh
```
