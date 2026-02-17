"""
Testet die aktuellen Pin-Belegungen
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("FEHLER: RPi.GPIO nicht verfügbar")
    sys.exit(1)

from config import (
    ULTRASONIC_RIGHT_TRIGGER, ULTRASONIC_RIGHT_ECHO,
    ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO,
    ULTRASONIC_FRONT_TRIGGER, ULTRASONIC_FRONT_ECHO,
)

def test_sensor(trigger_pin, echo_pin, name):
    """Testet einen Sensor."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        success_count = 0
        distances = []
        
        for _ in range(5):
            GPIO.output(trigger_pin, GPIO.LOW)
            time.sleep(0.00002)
            GPIO.output(trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(trigger_pin, GPIO.LOW)
            
            timeout = time.time() + 0.05
            echo_received = False
            while time.time() < timeout:
                if GPIO.input(echo_pin) == GPIO.HIGH:
                    echo_received = True
                    break
                time.sleep(0.00001)
            
            if echo_received:
                echo_start = time.time()
                timeout = echo_start + 0.05
                echo_end = None
                while time.time() < timeout:
                    if GPIO.input(echo_pin) == GPIO.LOW:
                        echo_end = time.time()
                        break
                    time.sleep(0.00001)
                
                if echo_end:
                    pulse_duration = echo_end - echo_start
                    distance_cm = (pulse_duration * 343 * 100) / 2
                    if 2 <= distance_cm <= 400:
                        distances.append(distance_cm)
                        success_count += 1
            
            time.sleep(0.1)
        
        GPIO.cleanup()
        
        if success_count >= 3:
            avg = sum(distances) / len(distances)
            return True, avg, success_count
        else:
            return False, None, success_count
            
    except Exception as e:
        GPIO.cleanup()
        return False, None, 0

def main():
    print("=" * 70)
    print("  TEST: Aktuelle Pin-Belegungen")
    print("=" * 70)
    print()
    
    sensors = [
        ('Rechts', ULTRASONIC_RIGHT_TRIGGER, ULTRASONIC_RIGHT_ECHO),
        ('Links', ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO),
        ('Front', ULTRASONIC_FRONT_TRIGGER, ULTRASONIC_FRONT_ECHO),
    ]
    
    print("⚠️  WICHTIG:")
    print("  - Pin 35 ist GND, kann nicht als Trigger verwendet werden!")
    print("  - Sensor 2 Trigger MUSS Pin 36 (GPIO 16) sein!")
    print()
    print("-" * 70)
    print()
    
    for name, trigger, echo in sensors:
        print(f"Teste {name} Sensor:")
        print(f"  Trigger: GPIO {trigger}")
        print(f"  Echo: GPIO {echo}")
        
        if trigger == 16:  # Sensor 2
            print(f"  ⚠️  Trigger sollte Pin 36 (GPIO 16) sein")
            print(f"     Falls Pin 35 verwendet wird → funktioniert NICHT (Pin 35 ist GND!)")
        
        works, distance, success = test_sensor(trigger, echo, name)
        
        if works:
            print(f"  ✅ FUNKTIONIERT! Distanz: {distance:.1f}cm ({success}/5 erfolgreich)")
        else:
            print(f"  ❌ Funktioniert NICHT ({success}/5 erfolgreich)")
            if trigger == 16 and success == 0:
                print(f"     → Trigger ist wahrscheinlich in Pin 35 (GND) statt Pin 36!")
        
        print()
    
    print("=" * 70)
    print("  ZUSAMMENFASSUNG:")
    print("=" * 70)
    print()
    print("Wenn Sensor 2 nicht funktioniert:")
    print("  → Trigger-Kabel von Pin 35 → Pin 36 umstecken!")
    print()
    print("Wenn Sensor 3 nicht funktioniert:")
    print("  → Trigger-Kabel von Pin 33 → Pin 32 umstecken (empfohlen)")
    print("  → Oder behalte Pin 33, aber dann Sensor 2 Echo ändern")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest abgebrochen")
        try:
            GPIO.cleanup()
        except:
            pass
