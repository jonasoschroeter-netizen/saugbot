#!/bin/bash
# Auto-Start Skript für Web-Interface beim Boot
# Wird von rc.local oder crontab aufgerufen

cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH

# Warte bis Netzwerk bereit ist
sleep 10

# Prüfe ob bereits läuft
if pgrep -f "web_interface.py" > /dev/null; then
    exit 0
fi

# Erstelle Logs-Verzeichnis
mkdir -p ~/saugbot/logs

# Starte Web-Interface
nohup python3 src/web_interface.py > ~/saugbot/logs/web_interface.log 2>&1 &
