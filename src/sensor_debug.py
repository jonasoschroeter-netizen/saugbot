"""
Sensor Debug Tool
Testet einzelne Sensoren mit detaillierter Ausgabe
"""

import sys
import os
import time

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import RPi.GPIO as GPIO
    from config import ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO
    GPIO_AVAILABLE = True
except ImportError as e:
    print(f"Error: {e}")
    GPIO_AVAILABLE = False
    sys.exit(1)

def test_pins():
    """Test GPIO pins directly."""
    print("=" * 60)
    print("GPIO Pin Test für Links Vorne Sensor")
    print("=" * 60)
    print(f"Trigger Pin: GPIO {ULTRASONIC_LEFT_TRIGGER} (BCM)")
    print(f"Echo Pin: GPIO {ULTRASONIC_LEFT_ECHO} (BCM)")
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup pins
    GPIO.setup(ULTRASONIC_LEFT_TRIGGER, GPIO.OUT)
    GPIO.setup(ULTRASONIC_LEFT_ECHO, GPIO.IN)
    
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
    time.sleep(0.1)
    
    print("1. Prüfe Echo-Pin Status (sollte LOW sein):")
    echo_state = GPIO.input(ULTRASONIC_LEFT_ECHO)
    print(f"   Echo Pin: {'HIGH' if echo_state else 'LOW'}")
    print()
    
    print("2. Sende Trigger-Puls...")
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
    print("   Trigger gesendet")
    print()
    
    print("3. Warte auf Echo HIGH...")
    start_wait = time.time()
    timeout = start_wait + 0.1  # 100ms timeout
    
    while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.LOW:
        if time.time() > timeout:
            print("   ❌ Timeout: Echo Pin wurde nicht HIGH")
            print("   → Prüfe Verkabelung und Level Shifter!")
            GPIO.cleanup()
            return False
        time.sleep(0.001)
    
    echo_high_time = time.time()
    wait_duration = echo_high_time - start_wait
    print(f"   ✅ Echo wurde HIGH nach {wait_duration*1000:.2f}ms")
    print()
    
    print("4. Warte auf Echo LOW...")
    start_high = time.time()
    timeout = start_high + 0.1
    
    while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.HIGH:
        if time.time() > timeout:
            print("   ❌ Timeout: Echo Pin wurde nicht LOW")
            print("   → Möglicherweise falsche Verkabelung oder Sensor defekt")
            GPIO.cleanup()
            return False
        time.sleep(0.001)
    
    echo_low_time = time.time()
    pulse_duration = echo_low_time - start_high
    print(f"   ✅ Echo wurde LOW nach {pulse_duration*1000:.2f}ms")
    print()
    
    # Calculate distance
    from config import SOUND_SPEED
    distance_cm = (pulse_duration * SOUND_SPEED * 100) / 2
    
    print("5. Berechnung:")
    print(f"   Puls-Dauer: {pulse_duration*1000:.2f}ms")
    print(f"   Distanz: {distance_cm:.1f}cm")
    print()
    
    if distance_cm < 2 or distance_cm > 400:
        print("   ⚠️  Distanz außerhalb des gültigen Bereichs (2-400cm)")
    else:
        print("   ✅ Messung erfolgreich!")
    
    GPIO.cleanup()
    return True

def continuous_test():
    """Kontinuierlicher Test."""
    print("=" * 60)
    print("Kontinuierlicher Sensor-Test")
    print("Drücke Ctrl+C zum Beenden")
    print("=" * 60)
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(ULTRASONIC_LEFT_TRIGGER, GPIO.OUT)
    GPIO.setup(ULTRASONIC_LEFT_ECHO, GPIO.IN)
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
    time.sleep(0.1)
    
    from config import SOUND_SPEED, ULTRASONIC_TIMEOUT
    
    try:
        while True:
            # Trigger
            GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
            
            # Wait for echo HIGH
            start_time = time.time()
            timeout = start_time + ULTRASONIC_TIMEOUT
            
            while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.LOW:
                if time.time() > timeout:
                    print("❌ Timeout (Echo HIGH)")
                    time.sleep(0.5)
                    continue
                time.sleep(0.00001)
            
            echo_start = time.time()
            
            # Wait for echo LOW
            timeout = echo_start + ULTRASONIC_TIMEOUT
            
            while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.HIGH:
                if time.time() > timeout:
                    print("❌ Timeout (Echo LOW)")
                    time.sleep(0.5)
                    continue
                echo_end = time.time()
                time.sleep(0.00001)
            
            pulse_duration = echo_end - echo_start
            distance_cm = (pulse_duration * SOUND_SPEED * 100) / 2
            
            if distance_cm < 2 or distance_cm > 400:
                print(f"⚠️  Ungültig: {distance_cm:.1f}cm")
            else:
                print(f"✅ Distanz: {distance_cm:.1f}cm")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\nTest beendet")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Sensor Debug Tool')
    parser.add_argument('--continuous', '-c', action='store_true', 
                       help='Kontinuierlicher Test')
    args = parser.parse_args()
    
    if args.continuous:
        continuous_test()
    else:
        test_pins()
        print()
        print("Für kontinuierlichen Test: python3 sensor_debug.py --continuous")
