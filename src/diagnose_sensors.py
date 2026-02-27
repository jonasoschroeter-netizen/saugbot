#!/usr/bin/env python3
"""
Sensor-Diagnose: Testet alle Pin-Kombinationen um herauszufinden welche Pins funktionieren
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Bekannter funktionierender Sensor (laut User)
WORKING = {'trigger': 20, 'echo': 21, 'name': 'Sensor 1 (funktioniert)'}

# Mögliche Kombinationen für die anderen 2 Sensoren
# Format: (trigger_gpio, echo_gpio, name)
COMBINATIONS = [
    # Sensor 2 (Links) - aktuelle Config
    (16, 26, 'Links: Trigger=16, Echo=26 (aktuell)'),
    # Sensor 2 - Trigger/Echo vertauscht?
    (26, 16, 'Links: Trigger=26, Echo=16 (vertauscht)'),
    # Sensor 3 (Front) - aktuelle Config  
    (5, 6, 'Front: Trigger=5, Echo=6 (aktuell)'),
    # Sensor 3 - Trigger/Echo vertauscht?
    (6, 5, 'Front: Trigger=6, Echo=5 (vertauscht)'),
    # Alternative Pins (falls Verkabelung anders)
    (13, 6, 'Alt: Trigger=13, Echo=6'),
    (6, 13, 'Alt: Trigger=6, Echo=13'),
    (13, 26, 'Alt: Trigger=13, Echo=26'),
    (26, 13, 'Alt: Trigger=26, Echo=13'),
]


def test_sensor(trigger, echo, name):
    """Teste einen Sensor, 3 Messungen."""
    try:
        GPIO.cleanup()  # Reset vor jedem Test
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(trigger, GPIO.OUT)
        GPIO.setup(echo, GPIO.IN)
        GPIO.output(trigger, GPIO.LOW)
        time.sleep(0.05)
        
        values = []
        for _ in range(3):
            GPIO.output(trigger, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(trigger, GPIO.LOW)
            
            timeout = time.time() + 0.03
            while GPIO.input(echo) == 0 and time.time() < timeout:
                pass
            start = time.time()
            while GPIO.input(echo) == 1 and time.time() < timeout:
                pass
            duration = time.time() - start
            dist = (duration * 34300) / 2
            if 2 < dist < 400:
                values.append(dist)
            time.sleep(0.1)
        
        if values:
            avg = sum(values) / len(values)
            return True, f"{avg:.1f} cm"
        return False, "Kein Echo"
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("  SENSOR-DIAGNOSE - Finde die richtigen Pins")
    print("=" * 60)
    print()
    
    # Test 1: Bekannter Sensor
    print(f"Test: {WORKING['name']} (GPIO {WORKING['trigger']}/{WORKING['echo']})")
    ok, result = test_sensor(WORKING['trigger'], WORKING['echo'], WORKING['name'])
    print(f"  -> {'OK: ' + result if ok else 'FEHLER: ' + result}")
    print()
    
    # Test 2: Andere Kombinationen
    print("Teste andere Pin-Kombinationen (5 Sekunden pro Test)...")
    print()
    
    working_combos = []
    for trigger, echo, name in COMBINATIONS:
        if (trigger, echo) == (WORKING['trigger'], WORKING['echo']):
            continue
        print(f"  {name}...", end=" ", flush=True)
        ok, result = test_sensor(trigger, echo, name)
        if ok:
            print(f"OK: {result}")
            working_combos.append((trigger, echo, name, result))
        else:
            print(f"Kein Signal")
        time.sleep(0.2)
    
    GPIO.cleanup()
    
    print()
    print("=" * 60)
    if working_combos:
        print("GEFUNDEN - Diese Kombinationen funktionieren:")
        for t, e, name, dist in working_combos:
            print(f"  {name}")
            print(f"    -> config: ULTRASONIC_*_TRIGGER = {t}, ULTRASONIC_*_ECHO = {e}")
    else:
        print("Keine weiteren funktionierenden Sensoren gefunden.")
        print()
        print("Prüfe:")
        print("  - Sind Trigger/Echo vertauscht?")
        print("  - Spannungsteiler (1k/2k) an Echo-Pins?")
        print("  - VCC (5V) und GND verbunden?")
    print("=" * 60)


if __name__ == "__main__":
    main()
