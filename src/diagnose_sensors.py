#!/usr/bin/env python3
"""
Sensor-Diagnose: Prüft ob Trigger und Echo vertauscht sind
Testet BEIDE Varianten (normal + vertauscht) für jeden Sensor
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Alle 3 Sensoren mit Pin A und Pin B (wir testen beide Richtungen)
# Format: (pin_a, pin_b, sensor_name)
SENSORS = [
    (20, 21, 'Sensor 1 (Rechts)'),   # Pin 38, 40
    (16, 26, 'Sensor 2 (Links)'),    # Pin 36, 37
    (5, 6, 'Sensor 3 (Front)'),      # Pin 29, 31
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
    config_changes = []
    
    print("=" * 65)
    print("  TRIGGER/ECHO PRÜFUNG - Sind die Kabel vertauscht?")
    print("=" * 65)
    print()
    print("Teste für jeden Sensor BEIDE Varianten:")
    print("  A) Trigger=Pin1, Echo=Pin2 (normal)")
    print("  B) Trigger=Pin2, Echo=Pin1 (vertauscht)")
    print()
    
    results = {}
    
    for pin_a, pin_b, name in SENSORS:
        print(f"--- {name} (Pin {pin_a} / Pin {pin_b}) ---")
        
        # Variante A: Trigger=A, Echo=B
        ok_a, result_a = test_sensor(pin_a, pin_b, name)
        status_a = f"OK: {result_a}" if ok_a else "Kein Signal"
        print(f"  A) Trigger={pin_a}, Echo={pin_b}: {status_a}")
        time.sleep(0.2)
        
        # Variante B: Trigger=B, Echo=A (vertauscht)
        ok_b, result_b = test_sensor(pin_b, pin_a, name)
        status_b = f"OK: {result_b}" if ok_b else "Kein Signal"
        print(f"  B) Trigger={pin_b}, Echo={pin_a} (VERTAUSCHT): {status_b}")
        print()
        
        if ok_a and not ok_b:
            results[name] = (pin_a, pin_b, False)  # Normal ist richtig
        elif ok_b and not ok_a:
            results[name] = (pin_b, pin_a, True)   # Vertauscht ist richtig!
        elif ok_a and ok_b:
            results[name] = (pin_a, pin_b, False)   # Beide OK, nimm normal
        else:
            results[name] = None  # Keiner funktioniert
        
        time.sleep(0.2)
    
    GPIO.cleanup()
    
    print("=" * 65)
    print("  ERGEBNIS")
    print("=" * 65)
    
    for name, res in results.items():
        if res:
            trig, echo, was_swapped = res
            if was_swapped:
                print(f"  {name}: VERTAUSCHT! -> Trigger={trig}, Echo={echo}")
                config_changes.append((name, trig, echo))
            else:
                print(f"  {name}: OK (richtig verkabelt)")
        else:
            print(f"  {name}: Kein Signal - Verkabelung prüfen!")
    
    if config_changes:
        print()
        print("CONFIG.PY ÄNDERN - Diese Zeilen anpassen:")
        print()
        for name, trig, echo in config_changes:
            if "Rechts" in name or "1" in name:
                print(f"  ULTRASONIC_SENSOR1_TRIGGER = {trig}")
                print(f"  ULTRASONIC_SENSOR1_ECHO = {echo}")
            elif "Links" in name or "2" in name:
                print(f"  ULTRASONIC_SENSOR2_TRIGGER = {trig}")
                print(f"  ULTRASONIC_SENSOR2_ECHO = {echo}")
            elif "Front" in name or "3" in name:
                print(f"  ULTRASONIC_SENSOR3_TRIGGER = {trig}")
                print(f"  ULTRASONIC_SENSOR3_ECHO = {echo}")
    print("=" * 65)
    return config_changes


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Prüft ob Trigger/Echo vertauscht sind')
    parser.add_argument('--fix', action='store_true', help='config.py automatisch korrigieren')
    args = parser.parse_args()
    
    config_changes = main()
    
    if args.fix and config_changes:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(script_dir), 'config.py')
        with open(config_path, 'r') as f:
            content = f.read()
        for name, trig, echo in config_changes:
            if "Links" in name or "2" in name:
                content = content.replace('ULTRASONIC_SENSOR2_TRIGGER = 16', f'ULTRASONIC_SENSOR2_TRIGGER = {trig}')
                content = content.replace('ULTRASONIC_SENSOR2_ECHO = 26', f'ULTRASONIC_SENSOR2_ECHO = {echo}')
            elif "Front" in name or "3" in name:
                content = content.replace('ULTRASONIC_SENSOR3_TRIGGER = 5', f'ULTRASONIC_SENSOR3_TRIGGER = {trig}')
                content = content.replace('ULTRASONIC_SENSOR3_ECHO = 6', f'ULTRASONIC_SENSOR3_ECHO = {echo}')
        with open(config_path, 'w') as f:
            f.write(content)
        print("\nconfig.py wurde aktualisiert!")
