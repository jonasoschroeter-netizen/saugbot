"""
Testet die spezifischen Pin-Kombinationen basierend auf physischen Pins
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

# Bekannte Verkabelung
KNOWN_SENSORS = {
    'Rechts': {'trigger': 20, 'echo': 21, 'physical': 'Pin 38/40'},
}

# Mögliche Kombinationen basierend auf physischen Pins
POSSIBLE_COMBINATIONS = [
    # Sensor 2 (Pin 36/34) - Trigger=GPIO 16
    {'name': 'Sensor 2 (Links?)', 'trigger': 16, 'echo': 13, 'physical': 'Pin 36/33'},
    {'name': 'Sensor 2 (Links?)', 'trigger': 16, 'echo': 6, 'physical': 'Pin 36/31'},
    {'name': 'Sensor 2 (Links?)', 'trigger': 16, 'echo': 26, 'physical': 'Pin 36/37'},
    
    # Sensor 3 (Pin 32/30) - Trigger=GPIO 12
    {'name': 'Sensor 3 (Front?)', 'trigger': 12, 'echo': 13, 'physical': 'Pin 32/33'},
    {'name': 'Sensor 3 (Front?)', 'trigger': 12, 'echo': 6, 'physical': 'Pin 32/31'},
    {'name': 'Sensor 3 (Front?)', 'trigger': 12, 'echo': 26, 'physical': 'Pin 32/37'},
]

def test_sensor(trigger_pin, echo_pin):
    """Testet einen Sensor."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        # Teste 3x
        success_count = 0
        distances = []
        
        for _ in range(3):
            # Send trigger
            GPIO.output(trigger_pin, GPIO.LOW)
            time.sleep(0.00002)
            GPIO.output(trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)
            GPIO.output(trigger_pin, GPIO.LOW)
            
            # Wait for echo HIGH
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
                        success_count += 1
                        distances.append(distance_cm)
            
            time.sleep(0.1)
        
        GPIO.cleanup()
        
        if success_count >= 2:
            avg_distance = sum(distances) / len(distances)
            return True, avg_distance, success_count
        else:
            return False, None, success_count
            
    except Exception as e:
        GPIO.cleanup()
        return False, None, 0

def main():
    print("=" * 70)
    print("  TESTE SPEZIFISCHE PIN-KOMBINATIONEN")
    print("=" * 70)
    print()
    
    print("Bekannte Verkabelung:")
    print("-" * 70)
    for name, sensor in KNOWN_SENSORS.items():
        print(f"✅ {name}: Trigger=GPIO {sensor['trigger']}, Echo=GPIO {sensor['echo']} ({sensor['physical']})")
    print()
    
    print("Teste mögliche Kombinationen...")
    print("-" * 70)
    print()
    
    found_sensors = []
    
    for combo in POSSIBLE_COMBINATIONS:
        print(f"Teste: {combo['name']}")
        print(f"  Trigger=GPIO {combo['trigger']}, Echo=GPIO {combo['echo']} ({combo['physical']})")
        
        works, distance, success = test_sensor(combo['trigger'], combo['echo'])
        
        if works:
            print(f"  ✅ FUNKTIONIERT! Distanz: {distance:.1f}cm ({success}/3 erfolgreich)")
            found_sensors.append({
                'name': combo['name'],
                'trigger': combo['trigger'],
                'echo': combo['echo'],
                'physical': combo['physical'],
                'distance': distance
            })
        else:
            print(f"  ❌ Funktioniert nicht ({success}/3 erfolgreich)")
        print()
    
    print("=" * 70)
    print("  ERGEBNIS:")
    print("=" * 70)
    print()
    
    if found_sensors:
        print("GEFUNDENE SENSOREN:")
        print("-" * 70)
        for sensor in KNOWN_SENSORS.items():
            print(f"✅ {sensor[0]}: Trigger=GPIO {sensor[1]['trigger']}, Echo=GPIO {sensor[1]['echo']}")
        
        for sensor in found_sensors:
            print(f"✅ {sensor['name']}: Trigger=GPIO {sensor['trigger']}, Echo=GPIO {sensor['echo']} ({sensor['physical']})")
    else:
        print("❌ Keine weiteren Sensoren gefunden")
        print()
        print("Mögliche Probleme:")
        print("  - Echo-Pins sind nicht über Level Shifter")
        print("  - Falsche GPIO-Pins")
        print("  - Sensoren haben keine Stromversorgung")
        print()
        print("Prüfe physisch:")
        print("  - Wo sind die Echo-Pins angeschlossen?")
        print("  - Gehen sie über Level Shifter?")
    
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
