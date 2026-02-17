# ✅ Sensor 1 gefunden!

## Gefundener Sensor:

**Trigger:** GPIO 20  
**Echo:** GPIO 21  
**Distanz:** ~151.7 cm

## Physische Pin-Nummern:

- **GPIO 20** = Physischer Pin **38**
- **GPIO 21** = Physischer Pin **40** (aber das ist GND!)

⚠️ **WICHTIG:** GPIO 21 ist normalerweise nicht verfügbar auf Raspberry Pi!  
Das könnte ein Fehler sein oder du verwendest einen speziellen Pin.

## Nächste Schritte:

### 1. Welcher Sensor ist das?

Sag mir bitte:
- **Ist das der Front-Sensor?**
- **Ist das der Links-Sensor?**
- **Ist das der Rechts-Sensor?**

### 2. Finde die anderen 2 Sensoren:

Führe das erweiterte Script aus:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/find_all_pins.py
```

Das testet alle Pin-Kombinationen gründlicher.

### 3. Prüfe Verkabelung:

- **Sind alle 3 Sensoren angeschlossen?**
- **Haben alle Sensoren Strom (5V)?**
- **Sind alle Echo-Pins über Level Shifter?**

## Temporäre config.py Anpassung:

Falls das der Links-Sensor ist, kann ich die config.py so anpassen:

```python
ULTRASONIC_LEFT_TRIGGER = 20
ULTRASONIC_LEFT_ECHO = 21
```

Aber zuerst müssen wir die anderen 2 Sensoren finden!
