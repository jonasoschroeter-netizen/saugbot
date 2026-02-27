# 🔧 Web-Interface Start-Probleme beheben

## Problem 1: Permission denied bei auto_start_web.sh

```bash
chmod +x ~/saugbot/auto_start_web.sh
```

## Problem 2: Port 5000 bereits belegt

Alten Prozess beenden:

```bash
# Finde den Prozess auf Port 5000
sudo lsof -i :5000

# Oder: Alle web_interface Prozesse beenden
pkill -f web_interface.py

# Oder: Prozess mit PID beenden (ersetze XXXX mit der angezeigten PID)
kill XXXX
```

## Problem 3: MIN_DISTANCE_CM Fehler

✅ Bereits in config.py behoben. Führe aus:

```bash
cd ~/saugbot
git pull
```

## Kompletter Neustart des Web-Interfaces

```bash
cd ~/saugbot

# 1. Alte Prozesse beenden
pkill -f web_interface.py
sleep 2

# 2. Code aktualisieren
git pull

# 3. Script ausführbar machen
chmod +x auto_start_web.sh

# 4. Web-Interface starten
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

Dann im Browser öffnen: **http://saugbot.local:5000** oder **http://192.168.37.207:5000**
