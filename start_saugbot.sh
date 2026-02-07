#!/bin/bash
# Start-Script für Saugbot mit Auto-Update

cd ~/saugbot

# Setze PYTHONPATH
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH

# Starte Auto-Update im Hintergrund
echo "🚀 Starte Auto-Update System..."
python3 auto_update.py > ~/saugbot/logs/auto_update.log 2>&1 &
AUTO_UPDATE_PID=$!
echo "   Auto-Update PID: $AUTO_UPDATE_PID"

# Starte Hauptprogramm
echo "🤖 Starte Saugbot..."
python3 src/main.py

# Wenn Hauptprogramm beendet wird, beende auch Auto-Update
kill $AUTO_UPDATE_PID 2>/dev/null
