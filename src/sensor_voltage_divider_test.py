"""
Test für Sensor mit Spannungsteiler
Nach dem Bau des Spannungsteilers ausführen
"""

import sys
import os
import time

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import RPi.GPIO as GPIO
    from config import ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO, SOUND_SPEED, ULTRASONIC_TIMEOUT
    GPIO_AVAILABLE = True
except ImportError as e:
    print(f"Error: {e}")
    GPIO_AVAILABLE = False
    sys.exit(1)

def test_with_voltage_divider():
    """Test Sensor mit Spannungsteiler."""
    print("=" * 60)
    print("🔧 Sensor-Test mit Spannungsteiler")
    print("=" * 60)
    print()
    print("Verkabelung sollte sein:")
    print("  Sensor Echo → [10kΩ] → GPIO 14")
    print("                    ↓")
    print("                [20kΩ]")
    print("                    ↓")
    print("                  GND")
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup Trigger
    GPIO.setup(ULTRASONIC_LEFT_TRIGGER, GPIO.OUT)
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
    time.sleep(0.1)
    
    # Setup Echo mit Pull-Down (für Spannungsteiler)
    GPIO.setup(ULTRASONIC_LEFT_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    print("Initialer Echo-Pin Status:", "HIGH" if GPIO.input(ULTRASONIC_LEFT_ECHO) else "LOW")
    print()
    print("Starte kontinuierliche Messung...")
    print("Drücke Ctrl+C zum Beenden")
    print()
    print("-" * 60)
    
    success_count = 0
    fail_count = 0
    measurements = []
    
    try:
        while True:
            # Trigger
            GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
            time.sleep(0.00002)
            GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
            
            # Wait for echo HIGH
            echo_start = None
            timeout = time.time() + ULTRASONIC_TIMEOUT
            
            while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.LOW:
                if time.time() > timeout:
                    fail_count += 1
                    print("❌ Timeout: Echo wurde nicht HIGH")
                    time.sleep(0.5)
                    break
                time.sleep(0.00001)
            
            if time.time() > timeout:
                continue
            
            echo_start = time.time()
            
            # Wait for echo LOW
            timeout = echo_start + ULTRASONIC_TIMEOUT
            echo_end = None
            
            while GPIO.input(ULTRASONIC_LEFT_ECHO) == GPIO.HIGH:
                if time.time() > timeout:
                    fail_count += 1
                    print("❌ Timeout: Echo wurde nicht LOW")
                    time.sleep(0.5)
                    break
                echo_end = time.time()
                time.sleep(0.00001)
            
            if time.time() > timeout or echo_end is None:
                continue
            
            # Calculate distance
            pulse_duration = echo_end - echo_start
            distance_cm = (pulse_duration * SOUND_SPEED * 100) / 2
            
            if distance_cm < 2 or distance_cm > 400:
                fail_count += 1
                print(f"⚠️  Ungültig: {distance_cm:.1f}cm (außerhalb 2-400cm)")
            else:
                success_count += 1
                measurements.append(distance_cm)
                print(f"✅ Distanz: {distance_cm:.1f}cm")
            
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print()
        print("-" * 60)
        print()
        print("Test beendet")
        print()
        
        if measurements:
            avg_distance = sum(measurements) / len(measurements)
            min_distance = min(measurements)
            max_distance = max(measurements)
            
            print("=" * 60)
            print("📊 Statistik:")
            print("=" * 60)
            print(f"  Erfolgreiche Messungen: {success_count}")
            print(f"  Fehlgeschlagene Messungen: {fail_count}")
            print(f"  Durchschnittliche Distanz: {avg_distance:.1f}cm")
            print(f"  Minimale Distanz: {min_distance:.1f}cm")
            print(f"  Maximale Distanz: {max_distance:.1f}cm")
            print()
            
            if success_count > fail_count:
                print("✅ Sensor funktioniert mit Spannungsteiler!")
                print("   → Du kannst jetzt das Web-Interface verwenden")
            else:
                print("❌ Sensor funktioniert nicht richtig")
                print("   → Prüfe Verkabelung des Spannungsteilers")
        else:
            print("❌ Keine erfolgreichen Messungen")
            print("   → Prüfe Verkabelung")
    
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    test_with_voltage_divider()
