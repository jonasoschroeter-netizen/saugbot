# Quick Start: Raspberry Pi Setup

## Option 1: Automatisches Setup (Empfohlen)

1. **SSH zum Raspberry Pi:**
   ```bash
   ssh pi@saugbot.local
   # Oder mit IP-Adresse: ssh pi@192.168.x.x
   # Password: 123456789
   ```

2. **Lade das Setup-Script herunter und führe es aus:**
   ```bash
   cd ~
   wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
   chmod +x setup_raspi.sh
   bash setup_raspi.sh
   ```

   **ODER** wenn das Repository bereits geklont ist:
   ```bash
   cd ~/saugbot
   chmod +x setup_raspi.sh
   bash setup_raspi.sh
   ```

Das Script führt automatisch alle Schritte aus:
- ✅ Git Installation prüfen
- ✅ SSH-Key prüfen/erstellen
- ✅ GitHub Verbindung testen
- ✅ Repository klonen/aktualisieren
- ✅ Python Dependencies installieren
- ✅ .env Datei erstellen
- ✅ GPIO Berechtigungen prüfen

## Option 2: Manuelles Setup

Falls das automatische Script nicht funktioniert, folge den Schritten in `RASPI_SETUP.md`.

## Nach dem Setup

```bash
cd ~/saugbot
python3 src/main.py
```
