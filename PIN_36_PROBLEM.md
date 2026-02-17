# ⚠️ Pin 36 Problem

## Problem:

**Pin 36 = GPIO 16** ist bereits der **Trigger-Pin** für Sensor 2!

Ein Pin kann **nicht gleichzeitig Trigger und Echo** sein!

## Pin-Mapping (von hinten, Pin 40):

| Physischer Pin | GPIO (BCM) | Funktion |
|----------------|------------|----------|
| 40 | GND | Masse |
| 39 | GND | Masse |
| 38 | GPIO 20 | **Sensor 1 Trigger** |
| 37 | GPIO 26 | **Möglicher Echo-Pin** |
| 36 | GPIO 16 | **Sensor 2 Trigger** ⚠️ |
| 35 | GND | Masse |
| 34 | GND | Masse |
| 33 | GPIO 13 | **Möglicher Echo-Pin** |
| 32 | GPIO 12 | **Sensor 3 Trigger** |
| 31 | GPIO 6 | **Möglicher Echo-Pin** |
| 30 | GND | Masse |

## Frage:

**Meintest du vielleicht:**

- **Pin 33** = GPIO 13 (funktioniert in Tests)
- **Pin 31** = GPIO 6 (funktioniert in Tests)
- **Pin 37** = GPIO 26 (funktioniert in Tests)

Oder ist Pin 36 wirklich der Echo-Pin? Dann müsste der Trigger-Pin anders sein!

## Nächste Schritte:

1. **Prüfe nochmal:** Welcher physische Pin ist wirklich der Echo-Pin für Sensor 2?
2. **Oder teste:** Welcher Echo-Pin liefert konsistente Werte?
