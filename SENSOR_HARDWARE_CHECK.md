# 🔌 Sensor Hardware-Checkliste

## Wenn ALLE Sensoren "Kein Signal" zeigen

### 1. Roh-Debug ausführen (zeigt ob Echo-Pin reagiert)
```bash
cd ~/saugbot
git pull
python3 src/sensor_debug_raw.py
```

**Ergebnis:**
- **Hoch-Impulse > 0** → Sensor antwortet, Problem liegt woanders
- **Hoch-Impulse = 0** → Kein Echo-Signal, siehe unten

### 2. Stromversorgung prüfen

| Anschluss | Wo hin | Prüfen |
|-----------|--------|--------|
| **VCC** | Pin 2 oder 4 (5V) | Multimeter: 5V zwischen VCC und GND? |
| **GND** | Pin 6, 9, 14, 20, 25, 30, 34, 39, 40 | Kontinuität zu Pi-GND? |
| **Trigger** | GPIO-Pins | Pi sendet 3.3V - reicht für HC-SR04 |
| **Echo** | Über Spannungsteiler! | 5V vom Sensor → 3.3V für Pi |

### 3. Spannungsteiler (wichtig!)

HC-SR04 Echo gibt **5V** aus. Raspberry Pi verträgt nur **3.3V**.

**Lösung:** 1kΩ + 2kΩ Spannungsteiler:
```
Sensor ECHO ---[1kΩ]---+---[2kΩ]--- GND
                       |
                       +--- zu Pi GPIO (Echo-Pin)
```
Ergebnis: ~3.3V am Pi

**Ohne Spannungsteiler:** Pi kann beschädigt werden oder liest falsch!

### 4. HC-SR04 Pinbelegung (von vorne)
```
  [VCC] [TRIG] [ECHO] [GND]
```

### 5. Falsche Pins?

Falls die Verkabelung ANDERS ist als in config.py, alle Kombinationen testen:
- Sensor 1: Pins 38/40 oder 36/37 oder 29/31?
- Welche physischen Pins sind wirklich belegt?

### 6. Sensor defekt?

Einen Sensor an bekannte funktionierende Pins (20/21) anschließen und testen.
