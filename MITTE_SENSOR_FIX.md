# Mitte-Sensor geht nicht – Schritt-für-Schritt

## Problem
Der mittlere Sensor (Pin 27/28, GPIO 0/1) liefert kein Signal, obwohl die Verkabelung stimmt.

## Ursache
**GPIO 0 und GPIO 1** sind Sonderpins (ID_SD/ID_SC für HAT-EEPROM). Sie haben 1,8kΩ Pull-ups und können mit Ultraschall-Sensoren Probleme machen.

---

## Lösung 1: Auf andere Pins umstecken (empfohlen)

**Neue Belegung für den Mitte-Sensor:**

| Funktion | Alt (Pin) | Neu (Pin) | GPIO |
|----------|-----------|-----------|------|
| Trigger  | 27        | **29**    | GPIO 5 |
| Echo     | 28        | **31**    | GPIO 6 |

**Schritte:**
1. Mitte-Sensor umstecken: Trigger → Pin 29, Echo → Pin 31
2. Auf dem Pi: `cd ~/saugbot && git pull`
3. In `config.py` ändern:
   ```
   ULTRASONIC_SENSOR3_TRIGGER = 5   # Pin 29
   ULTRASONIC_SENSOR3_ECHO = 6      # Pin 31
   ```
4. Oder automatisch: `python3 src/test_mitte_alternative.py` (Sensor vorher umstecken)

---

## Lösung 2: Diagnose mit aktueller Verkabelung

```bash
cd ~/saugbot
git pull
pkill -f web_interface.py
sleep 2
python3 src/diagnose_sensors.py
```

Das Script prüft:
- normale Zuordnung (Trig=27, Echo=28)
- vertauschte Zuordnung (falls Kabel vertauscht)

---

## Lösung 3: Sensor-Funktion prüfen

**Test:** Mitte-Sensor an funktionierende Pins hängen.

1. Mitte-Sensor **ab** Pin 27/28
2. Mitte-Sensor **an** Pin 38/40 (wie Rechts-Sensor)
3. `python3 src/echo_blink_test.py 1` – wenn hier Echo kommt, ist der Sensor OK
4. Dann zurück auf Pin 27/28 und Lösung 1 (Umstecken auf 29/31) nutzen

---

## Checkliste Hardware

- [ ] Sensor hat 5V (VCC) und GND
- [ ] Echo-Pin hat Spannungsteiler 1kΩ + 2kΩ (5V → 3,3V)
- [ ] Kabel sitzen fest
- [ ] Kein anderes Programm nutzt die GPIOs (Web-Interface beenden)

---

## Schnelltest: Pin 27 auf 3,3V

```bash
python3 src/pin_power_test.py
```

Multimeter: Schwarz=GND (Pin 39), Rot=Pin 27 → sollte ~3,3V zeigen.

Wenn 0V: Kabel oder Pin prüfen.
