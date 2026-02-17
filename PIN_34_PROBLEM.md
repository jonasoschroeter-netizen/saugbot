# ⚠️ Pin 34 Problem

## Problem:

**Pin 34 = GND (Masse)** - Das ist **KEIN GPIO-Pin**!

Ein Trigger-Pin **muss ein GPIO-Pin** sein, nicht GND!

## Pin-Mapping (von hinten, Pin 40):

| Physischer Pin | GPIO (BCM) | Funktion |
|----------------|------------|----------|
| 40 | GND | Masse |
| 39 | GND | Masse |
| 38 | GPIO 20 | Sensor 1 Trigger |
| 37 | GPIO 26 | **Möglicher Trigger/Echo** |
| 36 | GPIO 16 | **Möglicher Trigger** |
| 35 | GND | Masse |
| **34** | **GND** | **Masse** ⚠️ |
| 33 | GPIO 13 | **Möglicher Trigger/Echo** |
| 32 | GPIO 12 | Sensor 3 Trigger |
| 31 | GPIO 6 | **Möglicher Trigger/Echo** |
| 30 | GND | Masse |

## Frage:

**Meintest du vielleicht:**

- **Pin 33** = GPIO 13 (könnte Trigger sein)
- **Pin 35** = GND (nein, das ist auch Masse)
- **Pin 36** = GPIO 16 (könnte Trigger sein)
- **Pin 37** = GPIO 26 (könnte Trigger sein)

Oder zählst du die Pins anders? (z.B. von vorne statt von hinten?)

## Nächste Schritte:

1. **Prüfe nochmal:** Welcher physische Pin ist wirklich der Trigger für Sensor 2?
2. **Oder teste:** Welcher GPIO-Pin funktioniert als Trigger?
