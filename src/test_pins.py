"""
Testet alle konfigurierten Pins und zeigt welche funktionieren
"""

import sys
import os
import time

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("WARNUNG: RPi.GPIO nicht verfügbar - kann nur Konfiguration anzeigen")

from config import (
    ULTRASONIC_FRONT_TRIGGER, ULTRASONIC_FRONT_ECHO,
    ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO,
    ULTRASONIC_RIGHT_TRIGGER, ULTRASONIC_RIGHT_ECHO,
)

def test_sensor(trigger_pin, echo_pin, name):
    """Testet einen einzelnen Sensor."""
    if not GPIO_AVAILABLE:
        return None, f"GPIO nicht verfügbar"
    
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup pins
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        # Send trigger
        GPIO.output(trigger_pin, GPIO.LOW)
        time.sleep(0.00002)
        GPIO.output(trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, GPIO.LOW)
        
        # Wait for echo
        timeout = time.time() + 0.03
        while GPIO.input(echo_pin) == GPIO.LOW:
            if time.time() > timeout:
                return None, "Timeout (Echo HIGH)"
            time.sleep(0.00001)
        
        echo_start = time.time()
        
        timeout = echo_start + 0.03
        while GPIO.input(echo_pin) == GPIO.HIGH:
            if time.time() > timeout:
                return None, "Timeout (Echo LOW)"
            echo_end = time.time()
            time.sleep(0.00001)
        
        if echo_start and echo_end:
            pulse_duration = echo_end - echo_start
            distance_cm = (pulse_duration * 343 * 100) / 2
            
            if 2 <= distance_cm <= 400:
                return distance_cm, "OK"
            else:
                return None, f"Ungültig: {distance_cm:.1f}cm"
        else:
            return None, "Kein Echo-Signal"
            
    except Exception as e:
        return None, f"Fehler: {e}"

def main():
    print("=" * 70)
    print("  PIN-TEST: Sensoren prüfen")
    print("=" * 70)
    print()
    
    if not GPIO_AVAILABLE:
        print("⚠️  GPIO nicht verfügbar - zeige nur Konfiguration")
        print()
        print("Konfigurierte Pins:")
        print(f"  Front:  Trigger={ULTRASONIC_FRONT_TRIGGER}, Echo={ULTRASONIC_FRONT_ECHO}")
        print(f"  Links:  Trigger={ULTRASONIC_LEFT_TRIGGER}, Echo={ULTRASONIC_LEFT_ECHO}")
        print(f"  Rechts: Trigger={ULTRASONIC_RIGHT_TRIGGER}, Echo={ULTRASONIC_RIGHT_ECHO}")
        return
    
    sensors = [
        ("Front", ULTRASONIC_FRONT_TRIGGER, ULTRASONIC_FRONT_ECHO),
        ("Links", ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO),
        ("Rechts", ULTRASONIC_RIGHT_TRIGGER, ULTRASONIC_RIGHT_ECHO),
    ]
    
    print("Teste Sensoren (3 Messungen pro Sensor)...")
    print()
    
    results = {}
    
    for name, trigger, echo in sensors:
        print(f"{name} Sensor (Trigger: GPIO {trigger}, Echo: GPIO {echo}):")
        distances = []
        errors = []
        
        for i in range(3):
            distance, status = test_sensor(trigger, echo, name)
            if distance:
                distances.append(distance)
                print(f"  Messung {i+1}: {distance:.1f} cm - {status}")
            else:
                errors.append(status)
                print(f"  Messung {i+1}: FEHLER - {status}")
            time.sleep(0.5)
        
        if distances:
            avg = sum(distances) / len(distances)
            results[name] = {
                'working': True,
                'avg_distance': avg,
                'trigger': trigger,
                'echo': echo
            }
            print(f"  ✅ Durchschnitt: {avg:.1f} cm")
        else:
            results[name] = {
                'working': False,
                'errors': errors,
                'trigger': trigger,
                'echo': echo
            }
            print(f"  ❌ Sensor funktioniert nicht")
        print()
    
    print("=" * 70)
    print("  ZUSAMMENFASSUNG:")
    print("=" * 70)
    print()
    
    for name, result in results.items():
        if result['working']:
            print(f"✅ {name}: GPIO {result['trigger']}/{result['echo']} - {result['avg_distance']:.1f} cm")
        else:
            print(f"❌ {name}: GPIO {result['trigger']}/{result['echo']} - FEHLER")
            print(f"   Fehler: {', '.join(result['errors'])}")
    
    print()
    print("=" * 70)
    
    # Cleanup
    try:
        GPIO.cleanup()
    except:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest abgebrochen")
        try:
            GPIO.cleanup()
        except:
            pass
