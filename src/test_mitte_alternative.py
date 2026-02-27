#!/usr/bin/env python3
"""
Mitte-Sensor auf ALTERNATIVEN Pins testen.
GPIO 0/1 (Pin 27/28) sind Sonderpins - können Probleme machen.

Wenn du den Mitte-Sensor TEMPORÄR umsteckst:
  Trigger: Pin 29 (GPIO 5)
  Echo:    Pin 31 (GPIO 6)

... und dieses Script läuft -> Sensor ist OK, Problem sind GPIO 0/1.
Dann dauerhaft umstecken und config anpassen.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Web-Interface vorher beenden!
# pkill -f web_interface.py

from ultrasonic_sensor import UltrasonicSensor

# Aktuelle Pins (GPIO 0/1)
CURRENT = (0, 1)
# Alternative Pins (GPIO 5/6) - normale GPIOs, zuverlässiger
ALTERNATIVE = (5, 6)

def test_sensor(trigger, echo, name, num=10):
    try:
        sensor = UltrasonicSensor(trigger, echo, name)
        time.sleep(0.2)
        ok = 0
        for _ in range(num):
            d = sensor.get_distance_cm()
            if d is not None:
                ok += 1
                print(f"  {d:.1f} cm", end=" ")
            else:
                print("---", end=" ")
            time.sleep(0.1)
        print()
        return ok
    except Exception as e:
        print(f"  Fehler: {e}")
        return 0
    finally:
        try:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        except:
            pass

def main():
    print("=" * 60)
    print("  MITTE-SENSOR: Aktuell vs. Alternative Pins")
    print("=" * 60)
    print()
    print("Aktuell: Pin 27 (GPIO 0) = Trigger, Pin 28 (GPIO 1) = Echo")
    print("Alternative: Pin 29 (GPIO 5) = Trigger, Pin 31 (GPIO 6) = Echo")
    print()
    print("WICHTIG: pkill -f web_interface.py vorher!")
    print()
    
    print("--- Test AKTUELL (Pin 27/28, GPIO 0/1) ---")
    ok1 = test_sensor(*CURRENT, "Mitte aktuell")
    time.sleep(0.5)
    
    print()
    print("--- Test ALTERNATIVE (Pin 29/31, GPIO 5/6) ---")
    print("(Mitte-Sensor temporär umstecken: Trig->29, Echo->31)")
    ok2 = test_sensor(*ALTERNATIVE, "Mitte alternative")
    
    print()
    print("=" * 60)
    if ok2 > ok1 and ok2 > 0:
        print("ALTERNATIVE funktioniert besser!")
        print("-> Mitte-Sensor dauerhaft umstecken auf Pin 29/31")
        print("-> config.py wird angepasst...")
        # Config anpassen
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config.py')
        with open(config_path, 'r') as f:
            c = f.read()
        c = c.replace('ULTRASONIC_SENSOR3_TRIGGER = 0', 'ULTRASONIC_SENSOR3_TRIGGER = 5')
        c = c.replace('ULTRASONIC_SENSOR3_ECHO = 1', 'ULTRASONIC_SENSOR3_ECHO = 6')
        c = c.replace('Trigger=GPIO 0 (Pin 27), Echo=GPIO 1 (Pin 28)', 'Trigger=GPIO 5 (Pin 29), Echo=GPIO 6 (Pin 31)')
        with open(config_path, 'w') as f:
            f.write(c)
        print("   config.py aktualisiert!")
    elif ok1 > 0:
        print("Aktuell funktioniert - Verkabelung prüfen")
    else:
        print("Beide: Kein Signal. Prüfen:")
        print("  - 5V + GND am Sensor?")
        print("  - Spannungsteiler 1k/2k am Echo?")
        print("  - Sensor defekt? (mit funktionierendem Sensor tauschen)")
    print("=" * 60)

if __name__ == "__main__":
    main()
