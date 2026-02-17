#!/bin/bash
# Erzwingt Start des Web-Interfaces
# Kann manuell ausgeführt werden oder vom Auto-Update

cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH

# Stoppe eventuell laufende Instanz
pkill -f "web_interface.py"
sleep 2

# Erstelle Logs-Verzeichnis
mkdir -p ~/saugbot/logs

# Starte Web-Interface
echo "Starte Web-Interface..."
nohup python3 src/web_interface.py > ~/saugbot/logs/web_interface.log 2>&1 &

sleep 2

# Prüfe ob es läuft
if pgrep -f "web_interface.py" > /dev/null; then
    echo "✅ Web-Interface läuft (PID: $(pgrep -f web_interface.py))"
    echo "Öffne: http://192.168.0.5:5000"
else
    echo "❌ Web-Interface konnte nicht gestartet werden"
    echo "Prüfe Logs: ~/saugbot/logs/web_interface.log"
    exit 1
fi
