# 🔧 Links & Front Sensoren reparieren

## Situation
- **Rechts** (GPIO 20/21): ✅ Funktioniert
- **Links** (GPIO 16/26): ❌ Keine Werte
- **Front** (GPIO 5/6): ❌ Keine Werte

## Schritt 1: Diagnose ausführen

Auf dem Raspberry Pi:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/diagnose_sensors.py
```

Das Script testet verschiedene Pin-Kombinationen und zeigt, welche funktionieren.

## Schritt 2: Mögliche Ursachen prüfen

### Verkabelung prüfen (Links & Front):

| Sensor | Trigger Pin | Echo Pin | Spannungsteiler? |
|--------|-------------|----------|------------------|
| Links | Pin 36 (GPIO 16) | Pin 37 (GPIO 26) | Echo: 1k/2k |
| Front | Pin 29 (GPIO 5) | Pin 31 (GPIO 6) | Echo: 1k/2k |

### Häufige Fehler:
1. **Trigger und Echo vertauscht** – Kabel tauschen
2. **Kein Spannungsteiler** – Echo liefert 5V, Pi verträgt nur 3.3V
3. **VCC/GND** – Beide Sensoren brauchen 5V und GND

## Schritt 3: Wenn Diagnose andere Pins findet

Wenn das Diagnose-Script z.B. meldet "Trigger=13, Echo=6 funktioniert", dann in `config.py` ändern:

```python
# Für Links (wenn z.B. 13/6 funktioniert):
ULTRASONIC_SENSOR2_TRIGGER = 13
ULTRASONIC_SENSOR2_ECHO = 6
```

## Schritt 4: Sensor-Anzeige tauschen (optional)

Wenn der funktionierende Sensor **physisch in der Mitte** sitzt, aber als "Rechts" angezeigt wird:

In `config.py` die Zeilen für FRONT und RIGHT tauschen – dann zeigt "Front" die Werte des mittleren Sensors.
