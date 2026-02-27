# 🔌 Sensor Spannungsprüfung mit Multimeter

## Erwartete Spannungen

| Pin | Funktion | Ruhezustand | Bei Aktivität |
|-----|----------|-------------|---------------|
| **Trigger** | Pi → Sensor | 0V (LOW) | 3.3V (HIGH) für 10µs |
| **Echo** | Sensor → Pi | 0V (LOW) | 5V vom Sensor → 3.3V nach Spannungsteiler |

## Trigger-Pins (Pi sendet 3.3V)

| Sensor | GPIO | Physischer Pin | Erwartung bei HIGH |
|--------|------|----------------|---------------------|
| Sensor 1 | 20 | Pin 38 | **~3.3V** |
| Sensor 2 | 16 | Pin 36 | **~3.3V** |
| Sensor 3 | 5 | Pin 29 | **~3.3V** |

## Echo-Pins (Sensor sendet, Pi liest)

| Sensor | GPIO | Physischer Pin | Erwartung |
|--------|------|----------------|-----------|
| Sensor 1 | 21 | Pin 40 | 0V idle, ~3.3V wenn Echo (nach Spannungsteiler) |
| Sensor 2 | 26 | Pin 37 | 0V idle, ~3.3V wenn Echo |
| Sensor 3 | 6 | Pin 31 | 0V idle, ~3.3V wenn Echo |

**Wichtig:** Echo kommt vom Sensor (5V) → Spannungsteiler 1k/2k → ~3.3V am Pi

## Test-Script: Alle Trigger auf 3.3V

```bash
cd ~/saugbot
python3 src/pin_power_test.py
```

Das Script setzt alle 3 Trigger-Pins dauerhaft auf HIGH (3.3V).

**Mit Multimeter prüfen:**
1. Multimeter: DC Voltage, 20V Bereich
2. Schwarz (COM): Pin 39 (GND)
3. Rot (V): Pin 38, dann 36, dann 29
4. Erwartung: **~3.3V** an jedem Pin

Wenn 0V → Kabel oder Pin falsch.

## HC-SR04 Sensor-Anschlüsse (von vorne)

```
  [VCC] [TRIG] [ECHO] [GND]
   5V    3.3V   5V→3.3V  0V
```

- **VCC:** Muss 5V haben (Pin 2 oder 4)
- **GND:** Muss 0V haben (Pin 39)
- **TRIG:** Erhält 3.3V vom Pi (reicht für HC-SR04)
- **ECHO:** Gibt 5V aus → Spannungsteiler → 3.3V zum Pi
