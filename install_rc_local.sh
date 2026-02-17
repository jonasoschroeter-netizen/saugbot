#!/bin/bash
# Installiert Boot-Script in rc.local
# Wird vom Auto-Update-System ausgeführt

echo "Installiere Boot-Script in rc.local..."

# Prüfe ob rc.local existiert
if [ ! -f /etc/rc.local ]; then
    echo "FEHLER: /etc/rc.local nicht gefunden!"
    exit 1
fi

# Prüfe ob bereits installiert
if grep -q "boot_start_web.sh" /etc/rc.local; then
    echo "Boot-Script ist bereits in rc.local installiert"
    exit 0
fi

# Backup erstellen
sudo cp /etc/rc.local /etc/rc.local.backup.$(date +%Y%m%d_%H%M%S)

# Füge Boot-Script hinzu (vor exit 0)
# Verwende sed mit sudo
sudo sed -i '/^exit 0/i /home/pi/saugbot/boot_start_web.sh &' /etc/rc.local

echo "✅ Boot-Script zu rc.local hinzugefügt"
echo "Web-Interface startet jetzt automatisch beim Boot!"
