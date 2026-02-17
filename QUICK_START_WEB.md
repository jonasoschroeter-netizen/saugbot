# 🚀 Web-Interface schnell starten

## Problem: Port 5000 ist geschlossen - Web-Interface läuft nicht

## Lösung: Web-Interface auf Raspberry Pi starten

### Option 1: Direkt auf dem Raspberry Pi (mit Monitor/Tastatur)

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

### Option 2: Mit dem Start-Skript

```bash
cd ~/saugbot
chmod +x start_sensor_test.sh
./start_sensor_test.sh
```

### Option 3: Als Hintergrund-Prozess (damit es weiterläuft)

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
nohup python3 src/web_interface.py > web_interface.log 2>&1 &
```

Dann im Browser öffnen: **http://192.168.0.5:5000**

### Option 4: Service starten (falls installiert)

```bash
sudo systemctl start saugbot-web.service
sudo systemctl status saugbot-web.service
```

## Nach dem Start

Öffne im Browser:
- **http://192.168.0.5:5000**
- oder **http://saugbot.local:5000**

Du solltest dann sehen:
- ✅ Front Sensor
- ✅ Links Sensor (große Anzeige)
- ✅ Rechts Sensor
- ✅ Live-Updates alle 1 Sekunde

## Falls es nicht funktioniert

1. **Prüfe ob Python läuft:**
   ```bash
   python3 --version
   ```

2. **Prüfe ob Dependencies installiert sind:**
   ```bash
   cd ~/saugbot
   pip3 install -r requirements.txt
   ```

3. **Prüfe ob Port bereits belegt ist:**
   ```bash
   sudo lsof -i :5000
   # Falls belegt, beende Prozess:
   sudo kill -9 [PID]
   ```

4. **Prüfe Logs:**
   ```bash
   tail -f web_interface.log
   ```

## Schnelltest ohne Web-Interface

Falls Web-Interface Probleme macht, teste Sensoren direkt:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/test_all_sensors.py
```

Zeigt alle 3 Sensoren im Terminal an.
