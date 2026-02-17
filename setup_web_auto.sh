#!/bin/bash
# Automatisches Setup-Skript für Web-Interface
# Wird vom Auto-Update System nach Updates ausgeführt

cd ~/saugbot

# Prüfe ob Service bereits installiert ist
if systemctl is-enabled saugbot-web.service >/dev/null 2>&1; then
    echo "Web-Interface Service ist bereits installiert und aktiviert"
    # Service neu starten falls nötig
    sudo systemctl restart saugbot-web.service
    exit 0
fi

# Service noch nicht installiert - installiere jetzt
echo "Web-Interface Service wird installiert..."

if [ -f "install_web_service.sh" ]; then
    chmod +x install_web_service.sh
    ./install_web_service.sh
else
    echo "FEHLER: install_web_service.sh nicht gefunden!"
    exit 1
fi
