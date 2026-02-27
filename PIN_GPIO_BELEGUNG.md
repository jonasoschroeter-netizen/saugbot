# Pin- und GPIO-Belegung Saugbot

## Ultraschallsensoren (HC-SR04)

| Sensor | Funktion | GPIO | Physischer Pin |
|--------|----------|------|----------------|
| **Rechts** | Trigger | 20 | Pin 38 |
| **Rechts** | Echo | 21 | Pin 40 |
| **Links** | Trigger | 16 | Pin 36 |
| **Links** | Echo | 26 | Pin 37 |
| **Mitte (Front)** | Trigger | 5 | Pin 29 |
| **Mitte (Front)** | Echo | 6 | Pin 31 |

**Wichtig:** Echo-Pins brauchen Spannungsteiler 1kΩ + 2kΩ (5V → 3.3V)!

---

## Motoren (RPWM/LPWM)

| Motor | Funktion | GPIO | Physischer Pin |
|-------|----------|------|----------------|
| **Links** | RPWM | 12 | Pin 32 |
| **Links** | LPWM | 13 | Pin 33 |
| **Rechts** | RPWM | 18 | Pin 12 |
| **Rechts** | LPWM | 10 | Pin 19 |

---

## Side Brush

| Funktion | GPIO | Physischer Pin |
|----------|------|----------------|
| Relay | 27 | Pin 13 |

---

## Übersicht nach Pin-Nummer (nur belegte Pins)

| Pin | GPIO | Belegung |
|-----|------|----------|
| 12 | 18 | Motor Rechts RPWM |
| 13 | 27 | Side Brush Relay |
| 19 | 10 | Motor Rechts LPWM |
| 29 | 5 | Sensor Mitte Trigger |
| 31 | 6 | Sensor Mitte Echo |
| 32 | 12 | Motor Links RPWM |
| 33 | 13 | Motor Links LPWM |
| 36 | 16 | Sensor Links Trigger |
| 37 | 26 | Sensor Links Echo |
| 38 | 20 | Sensor Rechts Trigger |
| 40 | 21 | Sensor Rechts Echo |

---

## Stromversorgung (5V, GND)

- **5V:** Pin 2 oder 4
- **GND:** Pin 6, 9, 14, 20, 25, 30, 34, 39

---

## Verkabelung prüfen

1. **Trigger** → Pin 38, 36, 29 (je Sensor)
2. **Echo** → Pin 40, 37, 31 (je Sensor, **mit Spannungsteiler**)
3. **VCC** → 5V (Pin 2 oder 4)
4. **GND** → GND (z.B. Pin 39)
