# 📊 Sensor Pin-Belegung: Alt vs. Neu

## Vergleichstabelle

| Sensor | Funktion | **ALTE Belegung** | **NEUE Belegung** | Änderung |
|--------|----------|-------------------|-------------------|----------|
| **Sensor 1** | Trigger | GPIO 20 (Pin 38) | GPIO 20 (Pin 38) | ✅ Unverändert |
| **Sensor 1** | Echo | GPIO 21 (Pin 40) | GPIO 21 (Pin 40) | ✅ Unverändert |
| **Sensor 2** | Trigger | GPIO 13 (Pin 33) | **GPIO 16 (Pin 36)** | 🔄 **Geändert** |
| **Sensor 2** | Echo | GPIO 6 (Pin 31) | **GPIO 26 (Pin 37)** | 🔄 **Geändert** |
| **Sensor 3** | Trigger | GPIO 19 (Pin 35) | **GPIO 5 (Pin 29)** | 🔄 **Geändert** |
| **Sensor 3** | Echo | GPIO 16 (Pin 36) | GPIO 6 (Pin 31) | 🔄 **Geändert** |

## Detaillierte Übersicht

### Sensor 1 (Rechts)
| Funktion | Alt | Neu | Status |
|----------|-----|-----|--------|
| Trigger | GPIO 20 (Pin 38) | GPIO 20 (Pin 38) | ✅ Unverändert |
| Echo | GPIO 21 (Pin 40) | GPIO 21 (Pin 40) | ✅ Unverändert |
| Spannungsteiler | Ja | Ja | ✅ Unverändert |

### Sensor 2 (Links)
| Funktion | Alt | Neu | Status |
|----------|-----|-----|--------|
| Trigger | GPIO 13 (Pin 33) | **GPIO 16 (Pin 36)** | 🔄 **Geändert** |
| Echo | GPIO 6 (Pin 31) | **GPIO 26 (Pin 37)** | 🔄 **Geändert** |
| Spannungsteiler | Ja | Ja | ✅ Unverändert |

### Sensor 3 (Front)
| Funktion | Alt | Neu | Status |
|----------|-----|-----|--------|
| Trigger | GPIO 19 (Pin 35) | **GPIO 5 (Pin 29)** | 🔄 **Geändert** |
| Echo | GPIO 16 (Pin 36) | GPIO 6 (Pin 31) | 🔄 **Geändert** |
| Spannungsteiler | Ja | Ja | ✅ Unverändert |

## Zusammenfassung der Änderungen

### ✅ Unverändert:
- **Sensor 1**: Beide Pins bleiben gleich (GPIO 20/21)

### 🔄 Geändert:
- **Sensor 2 Trigger**: GPIO 13 → **GPIO 16** (Pin 33 → Pin 36)
- **Sensor 2 Echo**: GPIO 6 → **GPIO 26** (Pin 31 → Pin 37)
- **Sensor 3 Trigger**: GPIO 19 → **GPIO 5** (Pin 35 → Pin 29)
- **Sensor 3 Echo**: GPIO 16 → **GPIO 6** (Pin 36 → Pin 31)

## Physische Pin-Nummern (Raspberry Pi 40-Pin Header)

### Neue Verkabelung:
```
Sensor 1 (Rechts):
  TRIG1 → Pin 38 (GPIO 20)
  ECHO1 → Pin 40 (GPIO 21) [über Spannungsteiler 1k/2k]

Sensor 2 (Links):
  TRIG2 → Pin 36 (GPIO 16)
  ECHO2 → Pin 37 (GPIO 26) [über Spannungsteiler 1k/2k]

Sensor 3 (Front):
  TRIG3 → Pin 29 (GPIO 5)
  ECHO3 → Pin 31 (GPIO 6) [über Spannungsteiler 1k/2k]

GND → Pin 39 (oder anderer GND-Pin)
```

## Wichtige Hinweise

1. **Spannungsteiler**: Alle Echo-Pins verwenden weiterhin Spannungsteiler (1k/2k) für 5V → 3.3V Konvertierung
2. **GPIO 13**: Wird jetzt für den linken Motor (LPWM) verwendet
3. **GPIO 19**: Wird jetzt für den rechten Motor (RPWM) verwendet
4. **GPIO 16**: War vorher Sensor 3 Echo, ist jetzt Sensor 2 Trigger

## Code-Änderungen

Die `config.py` wurde aktualisiert mit:
- `ULTRASONIC_SENSOR1_TRIGGER = 20` (unverändert)
- `ULTRASONIC_SENSOR1_ECHO = 21` (unverändert)
- `ULTRASONIC_SENSOR2_TRIGGER = 16` (neu: war 13)
- `ULTRASONIC_SENSOR2_ECHO = 26` (neu: war 6)
- `ULTRASONIC_SENSOR3_TRIGGER = 5` (neu: war 19)
- `ULTRASONIC_SENSOR3_ECHO = 6` (neu: war 16)

Legacy-Aliase bleiben für Kompatibilität erhalten:
- `ULTRASONIC_RIGHT_*` → Sensor 1
- `ULTRASONIC_LEFT_*` → Sensor 2
- `ULTRASONIC_FRONT_*` → Sensor 3
