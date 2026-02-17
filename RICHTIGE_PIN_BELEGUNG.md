# ✅ Richtige Pin-Belegung für alle 3 Sensoren

## Problem erkannt:
- ❌ Sensor 2 Trigger → Pin 34 (GND) - **FALSCH!**
- ❌ Sensor 3 Trigger → Pin 30 (GND) - **FALSCH!**

**GND-Pins können keine Signale senden!**

## ✅ Richtige Verkabelung:

### Sensor 1 (Rechts) - BEREITS RICHTIG:
- **Trigger:** Pin 38 = GPIO 20 ✅
- **Echo:** GPIO 21 ✅
- **VCC:** Pin 2 oder 4 (5V)
- **GND:** Pin 6, 9, 14, 20, 25, 30, 34, 35, 39, 40

### Sensor 2 (Links) - KORRIGIEREN:
- **Trigger:** Pin 36 = GPIO 16 ✅ (statt Pin 34!)
- **Echo:** Pin 33 = GPIO 13 ✅ (empfohlen)
- **VCC:** Pin 2 oder 4 (5V)
- **GND:** Pin 34 ✅ (das ist richtig - GND für Masse)

### Sensor 3 (Front) - KORRIGIEREN:
- **Trigger:** Pin 32 = GPIO 12 ✅ (statt Pin 30!)
- **Echo:** Pin 31 = GPIO 6 ✅ (empfohlen)
- **VCC:** Pin 2 oder 4 (5V)
- **GND:** Pin 30 ✅ (das ist richtig - GND für Masse)

## 📌 Pin-Mapping (von hinten, Pin 40):

| Physischer Pin | GPIO (BCM) | Verwendung |
|----------------|------------|------------|
| 40 | GND | Sensor 1 GND |
| 39 | GND | - |
| 38 | GPIO 20 | **Sensor 1 Trigger** ✅ |
| 37 | GPIO 26 | - |
| 36 | GPIO 16 | **Sensor 2 Trigger** ✅ |
| 35 | GND | - |
| 34 | GND | **Sensor 2 GND** ✅ |
| 33 | GPIO 13 | **Sensor 2 Echo** ✅ |
| 32 | GPIO 12 | **Sensor 3 Trigger** ✅ |
| 31 | GPIO 6 | **Sensor 3 Echo** ✅ |
| 30 | GND | **Sensor 3 GND** ✅ |

## 🔧 Was du ändern musst:

### Sensor 2:
1. **Trigger-Kabel** von Pin 34 (GND) → **Pin 36** (GPIO 16) umstecken
2. **Echo-Kabel** → **Pin 33** (GPIO 13) stecken
3. **GND bleibt** an Pin 34 ✅

### Sensor 3:
1. **Trigger-Kabel** von Pin 30 (GND) → **Pin 32** (GPIO 12) umstecken
2. **Echo-Kabel** → **Pin 31** (GPIO 6) stecken
3. **GND bleibt** an Pin 30 ✅

## ✅ Nach der Korrektur:

Alle 3 Sensoren sollten dann funktionieren:
- Sensor 1 (Rechts): Trigger=GPIO 20, Echo=GPIO 21 ✅
- Sensor 2 (Links): Trigger=GPIO 16, Echo=GPIO 13 ✅
- Sensor 3 (Front): Trigger=GPIO 12, Echo=GPIO 6 ✅

## 🧪 Testen nach Umstecken:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/test_all_sensors.py
```

Alle 3 Sensoren sollten dann Werte anzeigen!
