#!/bin/bash
# Startet Web-Interface im Hintergrund (ohne Service)
# Wird automatisch vom Auto-Update System ausgeführt

cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH

# Prüfe ob Web-Interface bereits läuft
if pgrep -f "web_interface.py" > /dev/null; then
    echo "Web-Interface läuft bereits"
    exit 0
fi

# Erstelle Logs-Verzeichnis
mkdir -p ~/saugbot/logs

# Starte Web-Interface im Hintergrund
echo "Starte Web-Interface im Hintergrund..."
nohup python3 src/web_interface.py > ~/saugbot/logs/web_interface.log 2>&1 &

echo "Web-Interface gestartet (PID: $!)"
echo "Logs: ~/saugbot/logs/web_interface.log"
