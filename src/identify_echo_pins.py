"""
Identifiziert welcher Echo-Pin zu welchem Sensor gehört
Testet jeden Sensor einzeln mit verschiedenen Echo-Pins
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

# Bekannte Sensoren
SENSORS = [
    {'name': 'Rechts', 'trigger': 20, 'echo': 21, 'known': True},
    {'name': 'Sensor 2 (Links?)', 'trigger': 16, 'echo': None, 'known': False},
    {'name': 'Sensor 3 (Front?)', 'trigger': 12, 'echo': None, 'known': False},
]

# Mögliche Echo-Pins (die funktionieren)
POSSIBLE_ECHO_PINS = [13, 6, 26]

def get_distance(trigger_pin, echo_pin, num_tests=5):
    """Misst Distanz mehrfach und gibt Durchschnitt zurück."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        distances = []
        
        for _ in range(num_tests):
            GPIO.output(trigger_pin, GPIO.LOW)
            time.sleep(0.00002)
            GPIO.output(trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(trigger_pin, GPIO.LOW)
            
            timeout = time.time() + 0.05
            echo_high = False
            while time.time() < timeout:
                if GPIO.input(echo_pin) == GPIO.HIGH:
                    echo_high = True
                    break
                time.sleep(0.00001)
            
            if echo_high:
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
            
            time.sleep(0.1)
        
        GPIO.cleanup()
        
        if len(distances) >= 3:  # Mindestens 3 von 5 erfolgreich
            return sum(distances) / len(distances), len(distances)
        else:
            return None, len(distances)
            
    except Exception as e:
        GPIO.cleanup()
        return None, 0

def main():
    print("=" * 70)
    print("  ECHO-PIN IDENTIFIKATION")
    print("=" * 70)
    print()
    print("Teste jeden Sensor mit verschiedenen Echo-Pins")
    print("Der richtige Echo-Pin sollte konsistente Werte liefern")
    print()
    
    results = {}
    
    for sensor in SENSORS:
        if sensor['known']:
            print(f"✅ {sensor['name']}: Trigger=GPIO {sensor['trigger']}, Echo=GPIO {sensor['echo']} (bekannt)")
            continue
        
        print(f"Teste {sensor['name']}:")
        print(f"  Trigger: GPIO {sensor['trigger']}")
        print("-" * 70)
        
        sensor_results = []
        
        for echo_pin in POSSIBLE_ECHO_PINS:
            print(f"  Teste Echo=GPIO {echo_pin}...", end=" ", flush=True)
            
            distance, success_count = get_distance(sensor['trigger'], echo_pin, num_tests=5)
            
            if distance:
                print(f"✅ Distanz: {distance:.1f}cm ({success_count}/5 erfolgreich)")
                sensor_results.append({
                    'echo': echo_pin,
                    'distance': distance,
                    'success_rate': success_count,
                    'consistent': True
                })
            else:
                print(f"❌ Keine Messung ({success_count}/5 erfolgreich)")
                sensor_results.append({
                    'echo': echo_pin,
                    'distance': None,
                    'success_rate': success_count,
                    'consistent': False
                })
        
        results[sensor['name']] = sensor_results
        print()
    
    print("=" * 70)
    print("  ERGEBNIS:")
    print("=" * 70)
    print()
    
    for sensor_name, sensor_results in results.items():
        print(f"{sensor_name}:")
        print("-" * 70)
        
        # Finde beste Echo-Pin (höchste Erfolgsrate, konsistente Werte)
        best_echo = None
        best_score = 0
        
        for result in sensor_results:
            if result['consistent']:
                score = result['success_rate'] * result['distance']  # Kombiniere Erfolgsrate und Distanz
                if score > best_score:
                    best_score = score
                    best_echo = result
        
        if best_echo:
            print(f"  ✅ Empfohlener Echo-Pin: GPIO {best_echo['echo']}")
            print(f"     Distanz: {best_echo['distance']:.1f}cm")
            print(f"     Erfolgsrate: {best_echo['success_rate']}/5")
        else:
            print(f"  ❌ Kein eindeutiger Echo-Pin gefunden")
            print(f"     Prüfe physisch welche Echo-Pins verwendet werden")
        
        print()
    
    print("=" * 70)
    print("  NÄCHSTE SCHRITTE:")
    print("=" * 70)
    print()
    print("1. Prüfe physisch welche Echo-Pins verwendet werden:")
    print("   - GPIO 13 = Physischer Pin 33")
    print("   - GPIO 6  = Physischer Pin 31")
    print("   - GPIO 26 = Physischer Pin 37")
    print()
    print("2. Oder teste jeden Sensor einzeln:")
    print("   python3 src/monitor_sensor.py [TRIGGER] [ECHO]")
    print()
    print("3. Teile mir mit welcher Echo-Pin zu welchem Sensor gehört")
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
