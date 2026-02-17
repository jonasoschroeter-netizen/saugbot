# ⚠️ Pin 35 und Pin 33 Problem

## Problem:

**Pin 35 = GND (Masse)** - Das ist **KEIN GPIO-Pin**!

Ein Trigger-Pin **muss ein GPIO-Pin** sein!

## Pin-Mapping (von hinten, Pin 40):

| Physischer Pin | GPIO (BCM) | Funktion |
|----------------|------------|----------|
| 40 | GND | Masse |
| 39 | GND | Masse |
| 38 | GPIO 20 | Sensor 1 Trigger ✅ |
| 37 | GPIO 26 | - |
| 36 | GPIO 16 | **Sensor 2 Trigger (EMPFOHLEN)** ✅ |
| **35** | **GND** | **Masse** ⚠️ |
| 34 | GND | Masse |
| **33** | **GPIO 13** | **Sensor 3 Trigger** ✅ |
| 32 | GPIO 12 | **Sensor 3 Trigger (EMPFOHLEN)** ✅ |
| 31 | GPIO 6 | Sensor 3 Echo ✅ |
| 30 | GND | Masse |

## Korrektur:

### Sensor 2:
- ❌ Pin 35 (GND) - **FALSCH!**
- ✅ **Pin 36 (GPIO 16)** - **RICHTIG!**

### Sensor 3:
- ✅ Pin 33 (GPIO 13) - **KÖNNTE funktionieren**
- ✅ Pin 32 (GPIO 12) - **EMPFOHLEN** (weil Pin 33 auch als Echo verwendet werden könnte)

## Empfohlene Verkabelung:

### Sensor 2 (Links):
- **Trigger:** Pin 36 = GPIO 16 ✅
- **Echo:** Pin 33 = GPIO 13 ✅
- **GND:** Pin 34 oder 35 ✅

### Sensor 3 (Front):
- **Trigger:** Pin 32 = GPIO 12 ✅ (statt Pin 33)
- **Echo:** Pin 31 = GPIO 6 ✅
- **GND:** Pin 30 ✅

## Warum Pin 33 für Sensor 3 Trigger problematisch sein könnte:

Wenn Pin 33 (GPIO 13) als Trigger für Sensor 3 verwendet wird, kann es nicht gleichzeitig als Echo für Sensor 2 verwendet werden!

**Besser:**
- Sensor 2: Trigger=Pin 36 (GPIO 16), Echo=Pin 33 (GPIO 13)
- Sensor 3: Trigger=Pin 32 (GPIO 12), Echo=Pin 31 (GPIO 6)

## Nächste Schritte:

1. **Sensor 2 Trigger:** Pin 35 (GND) → **Pin 36 (GPIO 16)** umstecken
2. **Sensor 3 Trigger:** Pin 33 (GPIO 13) → **Pin 32 (GPIO 12)** umstecken (empfohlen)
   Oder behalte Pin 33, aber dann muss Sensor 2 Echo anders sein
