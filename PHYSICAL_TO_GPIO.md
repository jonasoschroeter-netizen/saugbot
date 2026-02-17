# 📌 Physische Pin-Nummern zu GPIO-Mapping

## Deine Verkabelung:

### Rechter Sensor:
- **Pin 40** = GND (Masse)
- **Pin 38** = GPIO 20 (Trigger)
- **Echo:** GPIO 21 (gefunden durch Test)

### Sensor 2 (wahrscheinlich Links):
- **Pin 36** = GPIO 16
- **Pin 34** = GND (Masse)
- **Vermutung:** Trigger=GPIO 16, Echo=?

### Sensor 3 (wahrscheinlich Front):
- **Pin 32** = GPIO 12
- **Pin 30** = GND (Masse)
- **Vermutung:** Trigger=GPIO 12, Echo=?

## Pin-Mapping (von hinten, Pin 40):

| Physischer Pin | GPIO (BCM) | Funktion |
|----------------|------------|----------|
| 40 | GND | Masse |
| 39 | GND | Masse |
| 38 | GPIO 20 | Digital I/O |
| 37 | GPIO 26 | Digital I/O |
| 36 | GPIO 16 | Digital I/O |
| 35 | GND | Masse |
| 34 | GND | Masse |
| 33 | GPIO 13 | Digital I/O |
| 32 | GPIO 12 | Digital I/O |
| 31 | GPIO 6 | Digital I/O |
| 30 | GND | Masse |

## WICHTIG: Echo-Pins fehlen!

Du hast nur Trigger und GND angegeben. Die **Echo-Pins** müssen auch angeschlossen sein!

**HC-SR04 Sensor benötigt:**
- VCC (5V)
- GND (Masse)
- **Trigger** (GPIO Pin)
- **Echo** (GPIO Pin über Level Shifter)

## Frage:

**Wo sind die Echo-Pins angeschlossen?**

Für jeden Sensor brauchen wir:
- Trigger-Pin (hast du angegeben)
- Echo-Pin (fehlt noch!)

## Mögliche Echo-Pins:

Basierend auf den LOW-Pins könnten die Echo-Pins sein:
- GPIO 12 (Pin 32) - aber das ist schon Trigger für Sensor 3?
- GPIO 16 (Pin 36) - aber das ist schon Trigger für Sensor 2?
- GPIO 13 (Pin 33) - könnte Echo für Sensor 2 sein
- GPIO 6 (Pin 31) - könnte Echo für Sensor 3 sein

## Nächste Schritte:

1. **Prüfe physisch:** Wo sind die Echo-Pins angeschlossen?
2. **Teste mögliche Kombinationen:**
   - Sensor 2: Trigger=GPIO 16, Echo=GPIO 13?
   - Sensor 3: Trigger=GPIO 12, Echo=GPIO 6?
