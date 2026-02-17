#!/bin/bash
# Installiert Cron-Job für Web-Interface
# Startet Web-Interface alle 5 Minuten, falls es nicht läuft

echo "=========================================="
echo "  Cron-Job Installation"
echo "=========================================="
echo ""

cd ~/saugbot

# Prüfe ob bereits installiert
if crontab -l 2>/dev/null | grep -q "force_start_web.sh"; then
    echo "Cron-Job ist bereits installiert"
    exit 0
fi

# Erstelle temporäre Crontab
TEMP_CRON=$(mktemp)
crontab -l 2>/dev/null > "$TEMP_CRON"

# Füge Cron-Job hinzu (alle 5 Minuten)
echo "*/5 * * * * /home/pi/saugbot/force_start_web.sh >> /home/pi/saugbot/logs/cron_web.log 2>&1" >> "$TEMP_CRON"

# Installiere neue Crontab
crontab "$TEMP_CRON"
rm "$TEMP_CRON"

echo "Cron-Job installiert: Startet Web-Interface alle 5 Minuten"
echo ""
echo "=========================================="
echo "  ✅ Installation abgeschlossen!"
echo "=========================================="
echo ""
echo "Web-Interface wird alle 5 Minuten geprüft und gestartet!"
echo ""
