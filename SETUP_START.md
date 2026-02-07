# Setup starten - Befehle für Raspberry Pi

## Status:
- ✅ WLAN verbunden
- ✅ IP-Adresse: 192.168.0.5
- ✅ Internetverbindung funktioniert

## Setup-Script ausführen:

Führe diese Befehle **am Pi-Terminal** aus (einer nach dem anderen):

```bash
cd ~
```

```bash
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
```

```bash
chmod +x setup_raspi.sh
```

```bash
bash setup_raspi.sh
```

## Was das Script macht:

1. ✅ Git Installation prüfen
2. ✅ SSH-Key prüfen/erstellen
3. ✅ GitHub Verbindung testen
4. ✅ Repository klonen (`~/saugbot`)
5. ✅ Python Dependencies installieren (`pip3 install -r requirements.txt`)
6. ✅ .env Datei erstellen
7. ✅ GPIO Berechtigungen prüfen

## Nach dem Setup:

```bash
cd ~/saugbot
python3 src/main.py
```

## Git Workflow:

```bash
cd ~/saugbot
git add .
git commit -m "Beschreibung"
git push origin main
```
