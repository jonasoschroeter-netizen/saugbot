# 📌 Physische Pin-Nummern zu GPIO-Mapping

## Raspberry Pi Pinout (von hinten, Pin 40 beginnend):

### Rechte Seite (unten, Pin 40 = GND):

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
| 29 | GPIO 5 | Digital I/O |
| 28 | GPIO 4 | Digital I/O |
| 27 | GPIO 3 | Digital I/O |
| 26 | GPIO 2 | Digital I/O |
| 25 | GND | Masse |
| 24 | GPIO 8 | Digital I/O |
| 23 | GPIO 11 | Digital I/O |
| 22 | GPIO 25 | Digital I/O |
| 21 | GPIO 9 | Digital I/O |
| 20 | GND | Masse |

### Linke Seite (oben, Pin 1 = 3.3V):

| Physischer Pin | GPIO (BCM) | Funktion |
|----------------|------------|----------|
| 1 | 3.3V | Power |
| 2 | 5V | Power |
| 3 | GPIO 2 | Digital I/O |
| 4 | 5V | Power |
| 5 | GPIO 3 | Digital I/O |
| 6 | GND | Masse |
| 7 | GPIO 4 | Digital I/O |
| 8 | GPIO 14 | Digital I/O |
| 9 | GND | Masse |
| 10 | GPIO 15 | Digital I/O |
| 11 | GPIO 17 | Digital I/O |
| 12 | GPIO 18 | Digital I/O |
| 13 | GPIO 27 | Digital I/O |
| 14 | GND | Masse |
| 15 | GPIO 22 | Digital I/O |
| 16 | GPIO 23 | Digital I/O |
| 17 | 3.3V | Power |
| 18 | GPIO 24 | Digital I/O |
| 19 | GPIO 10 | Digital I/O |
| 20 | GND | Masse |

## Wichtig für Sensoren:

**HC-SR04 Ultraschall-Sensor benötigt:**
- **VCC**: 5V (z.B. Pin 2 oder 4)
- **GND**: Masse (z.B. Pin 6, 9, 14, 20, 25, 30, 34, 35, 39, 40)
- **Trigger**: GPIO Pin (z.B. GPIO 2, 3, 4, etc.)
- **Echo**: GPIO Pin (z.B. GPIO 14, 15, 17, etc.)

## Beispiel-Verbindung:

**Sensor 1 (z.B. Links):**
- VCC → Pin 2 (5V)
- GND → Pin 6 (GND)
- Trigger → Pin 7 (GPIO 4)
- Echo → Pin 8 (GPIO 14)

**Sensor 2 (z.B. Rechts):**
- VCC → Pin 4 (5V)
- GND → Pin 9 (GND)
- Trigger → Pin 10 (GPIO 15)
- Echo → Pin 11 (GPIO 17)

## Bitte teile mir mit:

**Welche physischen Pins hast du für jeden Sensor verwendet?**

Zum Beispiel:
- **Front Sensor:**
  - VCC → Pin ?
  - GND → Pin ?
  - Trigger → Pin ? (GPIO ?)
  - Echo → Pin ? (GPIO ?)

- **Links Sensor:**
  - VCC → Pin ?
  - GND → Pin ?
  - Trigger → Pin ? (GPIO ?)
  - Echo → Pin ? (GPIO ?)

- **Rechts Sensor:**
  - VCC → Pin ?
  - GND → Pin ?
  - Trigger → Pin ? (GPIO ?)
  - Echo → Pin ? (GPIO ?)

Dann kann ich die config.py entsprechend anpassen!
