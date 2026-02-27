#!/usr/bin/env python3
"""
Sensor-Diagnose: Prüft ob Trigger und Echo vertauscht sind
Verwendet die gleiche Logik wie die echte Sensor-Klasse
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# WICHTIG: Web-Interface und andere Prozesse müssen beendet sein!
# pkill -f web_interface.py

from ultrasonic_sensor import UltrasonicSensor

# Alle 3 Sensoren - testen BEIDE Varianten (normal + vertauscht)
SENSORS = [
    (20, 21, 'Sensor 1 (Rechts)'),
    (16, 26, 'Sensor 2 (Links)'),
    (5, 6, 'Sensor 3 (Front)'),
]


def test_with_ultrasonic_class(trigger, echo, name, num_tests=5):
    """Nutzt die echte UltrasonicSensor-Klasse - gleiche Logik wie im Betrieb."""
    try:
        sensor = UltrasonicSensor(trigger, echo, name)
        time.sleep(0.2)  # Sensor braucht Zeit zum Einschwingen
        
        values = []
        for _ in range(num_tests):
            dist = sensor.get_distance_cm()
            if dist is not None:
                values.append(dist)
            time.sleep(0.15)
        
        try:
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        except:
            pass
            
        if values:
            avg = sum(values) / len(values)
            return True, f"{avg:.1f} cm"
        return False, "Kein Echo"
    except Exception as e:
        return False, str(e)


def main():
    config_changes = []
    
    print("=" * 65)
    print("  SENSOR-DIAGNOSE (mit echter Sensor-Logik)")
    print("=" * 65)
    print()
    print("WICHTIG: Web-Interface vorher beenden!")
    print("  pkill -f web_interface.py")
    print()
    print("Teste für jeden Sensor BEIDE Varianten:")
    print("  A) Trigger=Pin1, Echo=Pin2 (normal)")
    print("  B) Trigger=Pin2, Echo=Pin1 (vertauscht)")
    print()
    
    results = {}
    
    for pin_a, pin_b, name in SENSORS:
        print(f"--- {name} (GPIO {pin_a} / GPIO {pin_b}) ---")
        
        # Variante A
        ok_a, result_a = test_with_ultrasonic_class(pin_a, pin_b, name)
        status_a = f"OK: {result_a}" if ok_a else "Kein Signal"
        print(f"  A) Trigger={pin_a}, Echo={pin_b}: {status_a}")
        time.sleep(0.3)
        
        # Variante B (vertauscht)
        ok_b, result_b = test_with_ultrasonic_class(pin_b, pin_a, name)
        status_b = f"OK: {result_b}" if ok_b else "Kein Signal"
        print(f"  B) Trigger={pin_b}, Echo={pin_a} (VERTAUSCHT): {status_b}")
        print()
        
        if ok_a and not ok_b:
            results[name] = (pin_a, pin_b, False)
        elif ok_b and not ok_a:
            results[name] = (pin_b, pin_a, True)
        elif ok_a and ok_b:
            results[name] = (pin_a, pin_b, False)
        else:
            results[name] = None
        
        time.sleep(0.3)
    
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
            print(f"  {name}: Kein Signal")
    
    if not any(results.values()):
        print()
        print("ALLE Sensoren: Kein Signal - Mögliche Ursachen:")
        print("  1. Web-Interface läuft noch -> pkill -f web_interface.py")
        print("  2. Keine Stromversorgung (5V + GND) an den Sensoren")
        print("  3. Spannungsteiler fehlt an Echo-Pins (5V->3.3V)")
        print("  4. Falsche Pins - prüfe physische Verkabelung")
        print("  5. Mit sudo ausführen: sudo python3 src/diagnose_sensors.py")
    
    if config_changes:
        print()
        print("CONFIG.PY ÄNDERN:")
        for name, trig, echo in config_changes:
            if "Links" in name:
                print(f"  ULTRASONIC_SENSOR2_TRIGGER = {trig}")
                print(f"  ULTRASONIC_SENSOR2_ECHO = {echo}")
            elif "Front" in name:
                print(f"  ULTRASONIC_SENSOR3_TRIGGER = {trig}")
                print(f"  ULTRASONIC_SENSOR3_ECHO = {echo}")
    print("=" * 65)
    return config_changes


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--fix', action='store_true', help='config.py automatisch korrigieren')
    args = parser.parse_args()
    
    config_changes = main()
    
    if args.fix and config_changes:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(script_dir), 'config.py')
        with open(config_path, 'r') as f:
            content = f.read()
        for name, trig, echo in config_changes:
            if "Links" in name:
                content = content.replace('ULTRASONIC_SENSOR2_TRIGGER = 16', f'ULTRASONIC_SENSOR2_TRIGGER = {trig}')
                content = content.replace('ULTRASONIC_SENSOR2_ECHO = 26', f'ULTRASONIC_SENSOR2_ECHO = {echo}')
            elif "Front" in name:
                content = content.replace('ULTRASONIC_SENSOR3_TRIGGER = 5', f'ULTRASONIC_SENSOR3_TRIGGER = {trig}')
                content = content.replace('ULTRASONIC_SENSOR3_ECHO = 6', f'ULTRASONIC_SENSOR3_ECHO = {echo}')
        with open(config_path, 'w') as f:
            f.write(content)
        print("\nconfig.py wurde aktualisiert!")
