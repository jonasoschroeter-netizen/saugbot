# 🧪 Sensoren testen – Kurzanleitung

## Voraussetzungen
- Raspberry Pi ist eingeschaltet und im WLAN
- Sensoren sind verkabelt (siehe `SENSOR_PIN_VERGLEICH.md`)
- Code ist aktuell: `git pull` auf dem Pi

## 1. Per SSH verbinden

```bash
ssh pi@saugbot.local
# Password: 123456789
```

## 2. Sensoren testen

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/test_all_sensors.py
```

## 3. Was du sehen solltest

- **🟢** = Alles OK (Distanz > 9 cm)
- **🟡** = Warnung (4–9 cm)
- **🔴** = Kollisionsgefahr (< 4 cm)
- **❌** = Sensor liefert keine Werte (Verkabelung prüfen!)

## 4. Beenden

`Ctrl+C` drücken

## Aktuelle Pin-Belegung (config.py)

| Sensor | Trigger | Echo |
|--------|---------|------|
| Rechts | GPIO 20 (Pin 38) | GPIO 21 (Pin 40) |
| Links | GPIO 16 (Pin 36) | GPIO 26 (Pin 37) |
| Front | GPIO 5 (Pin 29) | GPIO 6 (Pin 31) |

## Bei Problemen

- **Alle ❌**: Stromversorgung (5V) und GND prüfen
- **Einzelner Sensor ❌**: Trigger/Echo-Pins und Spannungsteiler prüfen
- **Unrealistische Werte**: Spannungsteiler (1k/2k) prüfen
