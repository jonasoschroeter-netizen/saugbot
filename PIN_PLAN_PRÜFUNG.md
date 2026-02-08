# 📌 Pin-Plan Prüfung

## Wichtig für zukünftige Entwicklung

**Bitte immer zuerst den Pin-Plan prüfen, bevor Code geschrieben wird!**

## Aktuelle Pin-Belegung (config.py)

### Motor Driver (L298N):
- `MOTOR_LEFT_ENABLE = 18` (PWM)
- `MOTOR_LEFT_IN1 = 23`
- `MOTOR_LEFT_IN2 = 24`
- `MOTOR_RIGHT_ENABLE = 19` (PWM)
- `MOTOR_RIGHT_IN1 = 25`
- `MOTOR_RIGHT_IN2 = 8`

### Ultraschall-Sensoren (HC-SR04):
- **Front:**
  - `ULTRASONIC_FRONT_TRIGGER = 2`
  - `ULTRASONIC_FRONT_ECHO = 3`
- **Links:**
  - `ULTRASONIC_LEFT_TRIGGER = 4`
  - `ULTRASONIC_LEFT_ECHO = 14`
- **Rechts:**
  - `ULTRASONIC_RIGHT_TRIGGER = 15`
  - `ULTRASONIC_RIGHT_ECHO = 17`

### Side Brush:
- `SIDE_BRUSH_RELAY = 27`

## Hinweis

**Die tatsächliche Verkabelung kann abweichen!**

Bitte immer:
1. ✅ Pin-Plan vom Benutzer anfordern
2. ✅ `config.py` entsprechend anpassen
3. ✅ Testen bevor Code geschrieben wird

## Pin-Plan Format

Bitte in folgendem Format angeben:
```
Motor Links:
  ENABLE: GPIO ?
  IN1: GPIO ?
  IN2: GPIO ?

Sensor Links Vorne:
  Trigger: GPIO ?
  Echo: GPIO ?
  
...
```
