#!/bin/bash
# Start-Script für Sensor-Test Web-Interface

cd ~/saugbot

# Setze PYTHONPATH
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH

# Hole IP-Adresse
IP=$(hostname -I | awk '{print $1}')

echo "=========================================="
echo "  🤖 Saugbot Sensor Test Interface"
echo "=========================================="
echo ""
echo "🌐 Web-Interface wird gestartet..."
echo ""
echo "📱 Öffne im Browser:"
echo "   http://$IP:5000"
echo "   oder"
echo "   http://192.168.0.5:5000"
echo ""
echo "🔍 Alle 3 Sensoren werden live angezeigt:"
echo "   - Front Sensor"
echo "   - Links Sensor (Haupt-Sensor)"
echo "   - Rechts Sensor"
echo ""
echo "Drücke Ctrl+C zum Beenden"
echo "=========================================="
echo ""

# Starte Web-Interface
python3 src/web_interface.py
