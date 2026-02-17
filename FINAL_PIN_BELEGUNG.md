# ✅ Finale Pin-Belegung - ALLE SENSOREN

## Komplette Verkabelung:

### Sensor 1 (Rechts):
- **Trigger:** GPIO 20
- **Echo:** GPIO 21
- **Status:** ✅ Funktioniert

### Sensor 2 (Links):
- **Trigger:** GPIO 19 (MISO)
- **Echo:** GPIO 16 (Chip Enable-C2)
- **Status:** ✅ Konfiguriert

### Sensor 3 (Front):
- **Trigger:** GPIO 13 (PWM)
- **Echo:** GPIO 6
- **Status:** ✅ Konfiguriert

## Testen:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/test_all_sensors.py
```

Alle 3 Sensoren sollten jetzt funktionieren!

## Web-Interface:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

Dann im Browser: `http://192.168.0.5:5000`

Alle 3 Sensoren werden live angezeigt!
