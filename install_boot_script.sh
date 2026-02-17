#!/bin/bash
# Installiert Boot-Script für Web-Interface
# Fügt Auto-Start zu rc.local hinzu

echo "=========================================="
echo "  Boot-Script Installation"
echo "=========================================="
echo ""

cd ~/saugbot

# Prüfe ob rc.local existiert
if [ ! -f /etc/rc.local ]; then
    echo "FEHLER: /etc/rc.local nicht gefunden!"
    exit 1
fi

# Prüfe ob bereits installiert
if grep -q "auto_start_web.sh" /etc/rc.local; then
    echo "Boot-Script ist bereits installiert"
    exit 0
fi

# Backup erstellen
sudo cp /etc/rc.local /etc/rc.local.backup
echo "1. Backup erstellt: /etc/rc.local.backup"

# Füge Auto-Start hinzu (vor exit 0)
sudo sed -i '/^exit 0/i /home/pi/saugbot/auto_start_web.sh &' /etc/rc.local

echo "2. Boot-Script zu rc.local hinzugefügt"
echo ""
echo "=========================================="
echo "  ✅ Installation abgeschlossen!"
echo "=========================================="
echo ""
echo "Web-Interface startet jetzt automatisch beim Boot!"
echo "Nach Neustart: http://192.168.0.5:5000"
echo ""
