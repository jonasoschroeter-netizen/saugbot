# Web-Interface nicht erreichbar - Lösung

## Problem: Website ist nicht aufrufbar

### Schritt 1: Raspberry Pi erreichbar?

Prüfe ob der Raspberry Pi erreichbar ist:

```bash
ping 192.168.0.5
```

Falls nicht erreichbar:
- Prüfe ob Raspberry Pi eingeschaltet ist
- Prüfe ob Raspberry Pi im gleichen Netzwerk ist
- Prüfe ob IP-Adresse sich geändert hat: `hostname -I` auf dem Pi

### Schritt 2: Web-Interface starten

**Direkt auf dem Raspberry Pi (mit Monitor/Tastatur):**

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

**Oder per SSH (falls SSH funktioniert):**

```bash
ssh pi@192.168.0.5
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

### Schritt 3: Port prüfen

Auf dem Raspberry Pi:

```bash
# Prüfe ob Port 5000 belegt ist
sudo netstat -tuln | grep 5000

# Prüfe ob Firewall Port blockiert
sudo ufw status
```

Falls Firewall aktiv:
```bash
sudo ufw allow 5000
```

### Schritt 4: Service prüfen

Falls der Service läuft:

```bash
# Service Status prüfen
sudo systemctl status saugbot-web.service

# Service neu starten
sudo systemctl restart saugbot-web.service

# Service Logs anzeigen
sudo journalctl -u saugbot-web.service -f
```

### Schritt 5: Manuell starten (ohne Service)

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH

# Stoppe eventuell laufende Instanz
pkill -f web_interface.py

# Starte neu
python3 src/web_interface.py
```

### Schritt 6: IP-Adresse prüfen

Falls 192.168.0.5 nicht funktioniert, finde die aktuelle IP:

```bash
# Auf dem Raspberry Pi:
hostname -I
```

Dann verwende diese IP im Browser: `http://[NEUE_IP]:5000`

### Schritt 7: Alternative - Lokaler Test

Falls Web-Interface nicht startet, teste Sensoren direkt:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/test_all_sensors.py
```

## Häufige Fehler

### Fehler: "Address already in use"
```bash
# Finde Prozess auf Port 5000
sudo lsof -i :5000
# Beende Prozess
sudo kill -9 [PID]
```

### Fehler: "Module not found"
```bash
# Installiere Dependencies
cd ~/saugbot
pip3 install -r requirements.txt
```

### Fehler: "Permission denied" (GPIO)
```bash
# Füge User zur gpio Gruppe hinzu
sudo usermod -a -G gpio pi
# Logge dich neu ein
```

## Schnellstart (wenn alles funktioniert)

```bash
cd ~/saugbot
chmod +x start_sensor_test.sh
./start_sensor_test.sh
```

Dann im Browser öffnen: `http://192.168.0.5:5000`
