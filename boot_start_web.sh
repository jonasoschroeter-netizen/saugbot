#!/bin/bash
# Boot-Script: Startet Web-Interface beim Boot
# Wird automatisch von rc.local aufgerufen (falls installiert)

# Warte bis Netzwerk bereit ist
sleep 15

cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH

# Erstelle Logs-Verzeichnis
mkdir -p ~/saugbot/logs

# Prüfe ob Web-Interface bereits läuft
if pgrep -f "web_interface.py" > /dev/null; then
    echo "$(date): Web-Interface läuft bereits" >> ~/saugbot/logs/boot.log
    exit 0
fi

# Starte Web-Interface
echo "$(date): Starte Web-Interface..." >> ~/saugbot/logs/boot.log
nohup python3 src/web_interface.py >> ~/saugbot/logs/web_interface.log 2>&1 &

sleep 3

# Prüfe ob es läuft
if pgrep -f "web_interface.py" > /dev/null; then
    echo "$(date): Web-Interface gestartet (PID: $(pgrep -f web_interface.py))" >> ~/saugbot/logs/boot.log
else
    echo "$(date): FEHLER: Web-Interface konnte nicht gestartet werden" >> ~/saugbot/logs/boot.log
fi
