"""
Direkter Sensor-Test ohne Level Shifter
⚠️ WARNUNG: Nur für kurzen Test! Dauerhaft kann der Pi beschädigt werden!
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

def test_direct_connection():
    """Test Sensor direkt ohne Level Shifter (NUR FÜR TEST!)."""
    print("=" * 60)
    print("⚠️  DIREKTER SENSOR-TEST (OHNE LEVEL SHIFTER)")
    print("=" * 60)
    print()
    print("WARNUNG: Dieser Test verbindet den Sensor direkt mit dem Pi!")
    print("Der Echo-Pin gibt 5V aus, der Pi GPIO verträgt nur 3.3V!")
    print("Nur für kurzen Test verwenden!")
    print()
    
    response = input("Möchtest du fortfahren? (ja/nein): ")
    if response.lower() != 'ja':
        print("Test abgebrochen")
        return
    
    print()
    print("Test läuft 10 Sekunden, dann wird automatisch beendet...")
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup Trigger
    GPIO.setup(ULTRASONIC_LEFT_TRIGGER, GPIO.OUT)
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
    time.sleep(0.1)
    
    # Setup Echo direkt (ohne Pull-Up/Down)
    GPIO.setup(ULTRASONIC_LEFT_ECHO, GPIO.IN)
    
    from config import SOUND_SPEED, ULTRASONIC_TIMEOUT
    
    success_count = 0
    fail_count = 0
    
    start_time = time.time()
    test_duration = 10  # 10 Sekunden
    
    try:
        while time.time() - start_time < test_duration:
            # Trigger
            GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
            
            # Wait for echo HIGH
            echo_start = None
            timeout = time.time() + ULTRASONIC_TIMEOUT
            
            while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.LOW:
                if time.time() > timeout:
                    break
                time.sleep(0.00001)
            
            if time.time() > timeout:
                fail_count += 1
                print("❌ Timeout (Echo HIGH)")
                time.sleep(0.5)
                continue
            
            echo_start = time.time()
            
            # Wait for echo LOW
            timeout = echo_start + ULTRASONIC_TIMEOUT
            echo_end = None
            
            while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.HIGH:
                if time.time() > timeout:
                    break
                echo_end = time.time()
                time.sleep(0.00001)
            
            if time.time() > timeout or echo_end is None:
                fail_count += 1
                print("❌ Timeout (Echo LOW)")
                time.sleep(0.5)
                continue
            
            # Calculate distance
            pulse_duration = echo_end - echo_start
            distance_cm = (pulse_duration * SOUND_SPEED * 100) / 2
            
            if distance_cm < 2 or distance_cm > 400:
                fail_count += 1
                print(f"⚠️  Ungültig: {distance_cm:.1f}cm")
            else:
                success_count += 1
                print(f"✅ Distanz: {distance_cm:.1f}cm")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\nTest abgebrochen")
    finally:
        GPIO.cleanup()
        print()
        print("=" * 60)
        print("Ergebnis:")
        print(f"  Erfolgreich: {success_count}")
        print(f"  Fehlgeschlagen: {fail_count}")
        print()
        
        if success_count > 0:
            print("✅ Sensor funktioniert direkt!")
            print("   → Problem ist der Level Shifter oder die Verkabelung")
        else:
            print("❌ Sensor funktioniert auch direkt nicht")
            print("   → Sensor könnte defekt sein oder falsch verkabelt")

if __name__ == "__main__":
    test_direct_connection()
