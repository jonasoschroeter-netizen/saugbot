# 🔧 Alle Sensoren: "Kein Signal" - Checkliste

## Schritt-für-Schritt prüfen

### 1. Web-Interface und andere Prozesse beenden
```bash
pkill -f web_interface.py
pkill -f main.py
sleep 2
```
**Warum:** Andere Programme blockieren die GPIO-Pins.

### 2. Diagnose ausführen
```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/diagnose_sensors.py
```

### 3. Falls weiterhin "Kein Signal" - mit sudo versuchen
```bash
sudo python3 src/diagnose_sensors.py
```
**Warum:** GPIO-Zugriff braucht manchmal Root-Rechte.

### 4. Hardware prüfen

| Prüfung | Was prüfen |
|---------|------------|
| **5V** | Alle 3 Sensoren haben VCC an Pin 2 oder 4 (5V)? |
| **GND** | Alle 3 Sensoren haben GND an Pin 39 oder anderem GND? |
| **Spannungsteiler** | Echo-Kabel gehen durch 1kΩ + 2kΩ Spannungsteiler (5V→3.3V)? |
| **Kontakt** | Kabel sitzen fest in den Dupont-Steckern? |

### 5. Nur EINEN Sensor testen (Sensor 1 - der vorher funktionierte)
```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 -c "
from ultrasonic_sensor import UltrasonicSensor
import time
s = UltrasonicSensor(20, 21, 'Test')
for i in range(10):
    d = s.get_distance_cm()
    print(f'Messung {i+1}: {d} cm')
    time.sleep(0.5)
"
```

### 6. GPIO Berechtigungen prüfen
```bash
groups
# Sollte "gpio" enthalten. Falls nicht:
sudo usermod -a -G gpio pi
# Dann neu einloggen (SSH trennen und wieder verbinden)
```

### 7. Pin-Belegung nochmal prüfen

Deine Verkabelung laut User:
- **Sensor 1:** TRIG=Pin38 (GPIO20), ECHO=Pin40 (GPIO21)
- **Sensor 2:** TRIG=Pin36 (GPIO16), ECHO=Pin37 (GPIO26)
- **Sensor 3:** TRIG=Pin29 (GPIO5), ECHO=Pin31 (GPIO6)

Sind die Kabel wirklich so angeschlossen?
