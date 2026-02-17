"""
Hilft dabei, die verwendeten GPIO-Pins zu identifizieren
Testet verschiedene Pin-Kombinationen
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
    print("WARNUNG: RPi.GPIO nicht verfügbar")

# Mögliche GPIO-Pins für Sensoren (häufig verwendete)
COMMON_GPIO_PINS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

def test_pin_combination(trigger_pin, echo_pin):
    """Testet eine Trigger/Echo Pin-Kombination."""
    if not GPIO_AVAILABLE:
        return None
    
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
        
        # Wait for echo HIGH
        timeout = time.time() + 0.03
        while GPIO.input(echo_pin) == GPIO.LOW:
            if time.time() > timeout:
                return None
            time.sleep(0.00001)
        
        echo_start = time.time()
        
        # Wait for echo LOW
        timeout = echo_start + 0.03
        echo_end = None
        while GPIO.input(echo_pin) == GPIO.HIGH:
            if time.time() > timeout:
                return None
            echo_end = time.time()
            time.sleep(0.00001)
        
        if echo_start and echo_end:
            pulse_duration = echo_end - echo_start
            distance_cm = (pulse_duration * 343 * 100) / 2
            
            if 2 <= distance_cm <= 400:
                return distance_cm
        
        return None
        
    except Exception as e:
        return None

def main():
    print("=" * 70)
    print("  PIN-SUCHER: Findet funktionierende Sensor-Pins")
    print("=" * 70)
    print()
    print("Teste verschiedene Pin-Kombinationen...")
    print("Das kann einige Minuten dauern...")
    print()
    
    if not GPIO_AVAILABLE:
        print("❌ GPIO nicht verfügbar - kann nicht testen")
        return
    
    found_sensors = []
    
    # Teste alle möglichen Kombinationen
    for trigger in COMMON_GPIO_PINS:
        for echo in COMMON_GPIO_PINS:
            if trigger == echo:
                continue
            
            distance = test_pin_combination(trigger, echo)
            if distance:
                found_sensors.append({
                    'trigger': trigger,
                    'echo': echo,
                    'distance': distance
                })
                print(f"✅ Sensor gefunden: Trigger=GPIO {trigger}, Echo=GPIO {echo}, Distanz={distance:.1f}cm")
                time.sleep(0.1)
    
    GPIO.cleanup()
    
    print()
    print("=" * 70)
    print("  GEFUNDENE SENSOREN:")
    print("=" * 70)
    print()
    
    if found_sensors:
        for i, sensor in enumerate(found_sensors, 1):
            print(f"Sensor {i}:")
            print(f"  Trigger: GPIO {sensor['trigger']}")
            print(f"  Echo:    GPIO {sensor['echo']}")
            print(f"  Distanz: {sensor['distance']:.1f} cm")
            print()
        
        print("=" * 70)
        print("  Diese Pins funktionieren!")
        print("  Teile mir mit, welcher Sensor welcher ist (Front/Links/Rechts)")
        print("=" * 70)
    else:
        print("❌ Keine Sensoren gefunden")
        print()
        print("Mögliche Probleme:")
        print("  - Sensoren nicht angeschlossen")
        print("  - Falsche Stromversorgung")
        print("  - Level Shifter Problem")
        print("  - Sensoren defekt")
    
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
