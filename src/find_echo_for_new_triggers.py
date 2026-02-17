"""
Findet die Echo-Pins für Sensor 2 (Trigger=GPIO 19) und Sensor 3 (Trigger=GPIO 13)
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

# Bekannte Trigger-Pins
SENSOR_2_TRIGGER = 19  # GPIO 19 (MISO)
SENSOR_3_TRIGGER = 13  # GPIO 13 (PWM)

# Mögliche Echo-Pins (alle verfügbaren GPIO-Pins)
POSSIBLE_ECHO_PINS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27]

def test_sensor(trigger_pin, echo_pin, num_tests=5):
    """Testet einen Sensor."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        success_count = 0
        distances = []
        
        for _ in range(num_tests):
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
        
        if len(distances) >= 3:
            avg = sum(distances) / len(distances)
            return True, avg, success_count
        else:
            return False, None, success_count
            
    except Exception as e:
        GPIO.cleanup()
        return False, None, 0

def main():
    print("=" * 70)
    print("  ECHO-PIN FINDEN FÜR NEUE TRIGGER-PINS")
    print("=" * 70)
    print()
    print("Bekannte Trigger-Pins:")
    print(f"  Sensor 2 (Links): GPIO {SENSOR_2_TRIGGER} (MISO)")
    print(f"  Sensor 3 (Front): GPIO {SENSOR_3_TRIGGER} (PWM)")
    print()
    print("⚠️  WICHTIG: GPIO 13 ist jetzt Sensor 3 Trigger!")
    print("   → Kann nicht mehr als Echo für Sensor 2 verwendet werden!")
    print()
    print("Teste mögliche Echo-Pins...")
    print("-" * 70)
    print()
    
    # Entferne bekannte Trigger-Pins aus Echo-Liste
    echo_pins_to_test = [p for p in POSSIBLE_ECHO_PINS if p not in [SENSOR_2_TRIGGER, SENSOR_3_TRIGGER, 20, 21]]
    
    sensors = [
        {'name': 'Sensor 2 (Links)', 'trigger': SENSOR_2_TRIGGER},
        {'name': 'Sensor 3 (Front)', 'trigger': SENSOR_3_TRIGGER},
    ]
    
    results = {}
    
    for sensor in sensors:
        print(f"Teste {sensor['name']}:")
        print(f"  Trigger: GPIO {sensor['trigger']}")
        print()
        
        sensor_results = []
        
        for echo_pin in echo_pins_to_test:
            print(f"  Teste Echo=GPIO {echo_pin}...", end=" ", flush=True)
            
            works, distance, success = test_sensor(sensor['trigger'], echo_pin, num_tests=5)
            
            if works:
                print(f"✅ Distanz: {distance:.1f}cm ({success}/5)")
                sensor_results.append({
                    'echo': echo_pin,
                    'distance': distance,
                    'success_rate': success
                })
            else:
                print(f"❌ ({success}/5)")
            
            time.sleep(0.1)
        
        results[sensor['name']] = sensor_results
        print()
    
    print("=" * 70)
    print("  ERGEBNIS:")
    print("=" * 70)
    print()
    
    for sensor_name, sensor_results in results.items():
        print(f"{sensor_name}:")
        print("-" * 70)
        
        if sensor_results:
            # Sortiere nach Erfolgsrate
            sensor_results.sort(key=lambda x: x['success_rate'], reverse=True)
            
            print("Gefundene Echo-Pins:")
            for i, res in enumerate(sensor_results[:5], 1):  # Zeige beste 5
                print(f"  {i}. GPIO {res['echo']}: {res['distance']:.1f}cm ({res['success_rate']}/5 erfolgreich)")
            
            best = sensor_results[0]
            print()
            print(f"✅ Empfohlener Echo-Pin: GPIO {best['echo']}")
            print(f"   Distanz: {best['distance']:.1f}cm")
            print(f"   Erfolgsrate: {best['success_rate']}/5")
        else:
            print("❌ Keine funktionierenden Echo-Pins gefunden")
            print("   Prüfe:")
            print("   - Ist Echo-Pin angeschlossen?")
            print("   - Geht Echo-Pin über Level Shifter?")
            print("   - Hat Sensor Stromversorgung?")
        
        print()
    
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest abgebrochen")
        try:
            GPIO.cleanup()
        except:
            pass
