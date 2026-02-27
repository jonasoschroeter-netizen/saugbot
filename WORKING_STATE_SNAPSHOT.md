# ✅ Arbeitsstand – funktionierender Zustand

**Datum:** 27.02.2026

## Sensoren (HC-SR04)

| Sensor | Trigger | Echo | Pin |
|--------|---------|------|-----|
| Rechts | GPIO 20 | GPIO 21 | Pin 38 / 40 |
| Links | GPIO 16 | GPIO 26 | Pin 36 / 37 |
| Mitte (Front) | GPIO 5 | GPIO 6 | Pin 29 / 31 |

Alle drei Sensoren mit Spannungsteiler 1k/2k am Echo.

## Motoren (RPWM/LPWM)

| Motor | RPWM | LPWM | Pin |
|-------|------|------|-----|
| Links | GPIO 12 | GPIO 13 | Pin 32 / 33 |
| Rechts | GPIO 18 | GPIO 10 | Pin 12 / 19 |

## Web-Interface

- **URL:** http://saugbot.local:5000 oder http://192.168.37.207:5000
- **Dauerhaft:** systemd User-Service `saugbot-web`
- **Start:** `./create_autostart_file.sh`

## Wichtige Dateien

- `config.py` – Pin-Belegung
- `src/ultrasonic_sensor.py` – Sensor-Logik (70ms Pause zwischen Lesungen)
- `src/web_interface.py` – Web-Oberfläche
- `create_autostart_file.sh` – Dauerhafter Start
