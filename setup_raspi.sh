#!/bin/bash
# Setup Script für Raspberry Pi
# Führe dieses Script auf dem Raspberry Pi aus: bash setup_raspi.sh

set -e  # Stop bei Fehlern

echo "=========================================="
echo "Saugbot Raspberry Pi Setup"
echo "=========================================="
echo ""

# 1. Git installieren/prüfen
echo "1. Prüfe Git Installation..."
if ! command -v git &> /dev/null; then
    echo "   Git nicht gefunden. Installiere Git..."
    sudo apt update
    sudo apt install git -y
else
    echo "   ✓ Git ist installiert: $(git --version)"
fi
echo ""

# 2. Prüfe SSH-Key
echo "2. Prüfe SSH-Key..."
if [ -f ~/.ssh/id_ed25519.pub ]; then
    echo "   ✓ SSH-Key gefunden"
    echo "   Public Key:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "   Bitte stelle sicher, dass dieser Key auf GitHub hinzugefügt wurde:"
    echo "   https://github.com/settings/keys"
    echo ""
    read -p "   Ist der Key auf GitHub hinzugefügt? (j/n): " key_added
    if [ "$key_added" != "j" ]; then
        echo "   Bitte füge den Key zu GitHub hinzu und führe das Script erneut aus."
        exit 1
    fi
else
    echo "   SSH-Key nicht gefunden. Erstelle neuen Key..."
    ssh-keygen -t ed25519 -C "saugbot-pi" -f ~/.ssh/id_ed25519 -N ""
    echo "   ✓ SSH-Key erstellt"
    echo "   Public Key:"
    cat ~/.ssh/id_ed25519.pub
    echo ""
    echo "   Bitte füge diesen Key zu GitHub hinzu:"
    echo "   https://github.com/settings/keys"
    echo ""
    read -p "   Drücke Enter, wenn der Key hinzugefügt wurde..."
fi
echo ""

# 3. Teste GitHub SSH-Verbindung
echo "3. Teste GitHub SSH-Verbindung..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "   ✓ SSH-Verbindung zu GitHub funktioniert"
else
    echo "   ⚠ SSH-Verbindung fehlgeschlagen. Prüfe den Key auf GitHub."
    exit 1
fi
echo ""

# 4. Repository klonen oder aktualisieren
echo "4. Repository Setup..."
if [ -d ~/saugbot ]; then
    echo "   Repository existiert bereits. Aktualisiere..."
    cd ~/saugbot
    git pull origin main
else
    echo "   Klone Repository..."
    cd ~
    git clone git@github.com:jonasoschroeter-netizen/saugbot.git
    cd ~/saugbot
    echo "   ✓ Repository geklont"
fi
echo ""

# 5. Python und pip prüfen
echo "5. Prüfe Python Installation..."
if ! command -v python3 &> /dev/null; then
    echo "   Python3 nicht gefunden. Installiere..."
    sudo apt install python3 python3-pip -y
else
    echo "   ✓ Python3 ist installiert: $(python3 --version)"
fi

if ! command -v pip3 &> /dev/null; then
    echo "   pip3 nicht gefunden. Installiere..."
    sudo apt install python3-pip -y
else
    echo "   ✓ pip3 ist installiert: $(pip3 --version)"
fi
echo ""

# 6. Dependencies installieren
echo "6. Installiere Python Dependencies..."
pip3 install -r requirements.txt
echo "   ✓ Dependencies installiert"
echo ""

# 7. .env Datei erstellen
echo "7. Erstelle .env Datei..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   ✓ .env Datei erstellt (aus .env.example)"
else
    echo "   ✓ .env Datei existiert bereits"
fi
echo ""

# 8. GPIO Berechtigungen prüfen
echo "8. Prüfe GPIO Berechtigungen..."
if groups | grep -q gpio; then
    echo "   ✓ User ist in gpio Gruppe"
else
    echo "   Füge User zu gpio Gruppe hinzu..."
    sudo usermod -a -G gpio $USER
    echo "   ⚠ Bitte neu einloggen, damit die Änderung wirksam wird"
fi
echo ""

# 9. Zusammenfassung
echo "=========================================="
echo "Setup abgeschlossen!"
echo "=========================================="
echo ""
echo "Nächste Schritte:"
echo "1. Prüfe config.py für GPIO Pin-Zuweisungen"
echo "2. Teste einzelne Komponenten:"
echo "   python3 src/motor_control.py"
echo "   python3 src/ultrasonic_sensor.py"
echo "   python3 src/side_brush.py"
echo "3. Starte Hauptprogramm:"
echo "   python3 src/main.py"
echo ""
echo "Git Workflow:"
echo "  git add ."
echo "  git commit -m 'Beschreibung'"
echo "  git push origin main"
echo ""
