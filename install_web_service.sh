#!/bin/bash
# Installiert und aktiviert den Web-Interface Service
# Wird automatisch vom Auto-Update System ausgeführt

echo "=========================================="
echo "  Web-Interface Service Installation"
echo "=========================================="
echo ""

cd ~/saugbot

# Prüfe ob Service-Datei existiert
if [ ! -f "saugbot-web.service" ]; then
    echo "FEHLER: saugbot-web.service nicht gefunden!"
    exit 1
fi

# Kopiere Service-Datei
echo "1. Kopiere Service-Datei..."
sudo cp saugbot-web.service /etc/systemd/system/
echo "   [OK] Service-Datei kopiert"

# Erstelle Logs-Verzeichnis
echo "2. Erstelle Logs-Verzeichnis..."
mkdir -p ~/saugbot/logs
echo "   [OK] Logs-Verzeichnis erstellt"

# Lade Systemd neu
echo "3. Lade Systemd neu..."
sudo systemctl daemon-reload
echo "   [OK] Systemd neu geladen"

# Aktiviere Service (startet automatisch beim Boot)
echo "4. Aktiviere Service..."
sudo systemctl enable saugbot-web.service
echo "   [OK] Service aktiviert (startet beim Boot)"

# Starte Service
echo "5. Starte Service..."
sudo systemctl start saugbot-web.service
echo "   [OK] Service gestartet"

# Warte kurz
sleep 2

# Prüfe Status
echo ""
echo "6. Service-Status:"
sudo systemctl status saugbot-web.service --no-pager -l

echo ""
echo "=========================================="
echo "  ✅ Installation abgeschlossen!"
echo "=========================================="
echo ""
echo "Web-Interface sollte jetzt laufen!"
echo "Öffne im Browser: http://192.168.0.5:5000"
echo ""
echo "Service-Befehle:"
echo "  Status prüfen:  sudo systemctl status saugbot-web.service"
echo "  Neu starten:    sudo systemctl restart saugbot-web.service"
echo "  Stoppen:       sudo systemctl stop saugbot-web.service"
echo "  Logs anzeigen: sudo journalctl -u saugbot-web.service -f"
echo ""
