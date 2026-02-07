# Automatisches Update-System - Setup

## Übersicht

Mit diesem System musst du den Raspberry Pi **NICHT mehr anfassen**! 

- ✅ Du codest auf dem Laptop
- ✅ Du pusht zu GitHub
- ✅ Der Pi holt automatisch Updates
- ✅ Das Programm startet automatisch neu

## Installation auf Raspberry Pi:

### 1. Logs-Verzeichnis erstellen:

```bash
cd ~/saugbot
mkdir -p logs
```

### 2. Auto-Update Script ausführbar machen:

```bash
chmod +x auto_update.py
chmod +x start_saugbot.sh
chmod +x start_web_interface.sh
```

### 3. Auto-Update als Systemd Service (OPTIONAL - für automatischen Start):

```bash
sudo nano /etc/systemd/system/saugbot-auto-update.service
```

Füge hinzu:
```ini
[Unit]
Description=Saugbot Auto-Update Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/saugbot
Environment="PYTHONPATH=/home/pi/saugbot"
ExecStart=/usr/bin/python3 /home/pi/saugbot/auto_update.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Dann aktivieren:
```bash
sudo systemctl daemon-reload
sudo systemctl enable saugbot-auto-update.service
sudo systemctl start saugbot-auto-update.service
```

## Verwendung:

### Option 1: Mit Start-Script (EINFACHSTE)

**Hauptprogramm starten:**
```bash
cd ~/saugbot
./start_saugbot.sh
```

**Web-Interface starten:**
```bash
cd ~/saugbot
./start_web_interface.sh
```

### Option 2: Auto-Update separat starten

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 auto_update.py
```

In einem anderen Terminal:
```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/main.py  # oder src/web_interface.py
```

## Workflow:

### Auf dem Laptop:

1. **Code schreiben/ändern**
2. **Testen (optional)**
3. **Commit und Push:**
   ```bash
   git add .
   git commit -m "Neue Funktion: ..."
   git push origin main
   ```

### Auf dem Raspberry Pi:

**NICHTS!** 🎉

- Auto-Update prüft alle 30 Sekunden
- Findet neue Commits automatisch
- Holt Updates automatisch
- Startet Programm neu (falls als Service)

## Konfiguration:

In `auto_update.py` kannst du anpassen:
- `CHECK_INTERVAL = 30` - Sekunden zwischen Checks (Standard: 30s)
- `GIT_BRANCH = "main"` - Branch zum Überwachen

## Logs prüfen:

```bash
# Auto-Update Logs
tail -f ~/saugbot/logs/auto_update.log

# Systemd Service Logs (falls als Service)
sudo journalctl -u saugbot-auto-update.service -f
```

## Stoppen:

```bash
# Auto-Update beenden
pkill -f auto_update.py

# Oder wenn als Service:
sudo systemctl stop saugbot-auto-update.service
```

## Vorteile:

✅ **Kein manuelles `git pull` mehr nötig**
✅ **Automatische Updates**
✅ **Programm startet automatisch neu**
✅ **Du codest nur auf dem Laptop**
✅ **Pi läuft autonom**

## Wichtig:

- **Erste Installation:** Einmalig `git pull` ausführen
- **Danach:** Alles automatisch!
- **Bei Problemen:** Logs prüfen
