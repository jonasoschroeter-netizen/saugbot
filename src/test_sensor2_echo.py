"""
Testet Sensor 2 mit verschiedenen Echo-Pins um den richtigen zu finden
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

# Sensor 2 Konfiguration
SENSOR_2_TRIGGER = 16  # Pin 36

# Mögliche Echo-Pins (basierend auf physischen Pins in der Nähe)
POSSIBLE_ECHO_PINS = [
    {'gpio': 13, 'physical': 33, 'name': 'Pin 33'},
    {'gpio': 6, 'physical': 31, 'name': 'Pin 31'},
    {'gpio': 26, 'physical': 37, 'name': 'Pin 37'},
]

def test_echo_pin(trigger_pin, echo_pin, num_tests=10):
    """Testet einen Echo-Pin ausführlich."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        distances = []
        success_count = 0
        
        print(f"  Teste {num_tests} Messungen...")
        
        for i in range(num_tests):
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
                        success_count += 1
                        if (i + 1) % 5 == 0:
                            print(f"    Messung {i+1}: {distance_cm:.1f}cm")
            
            time.sleep(0.1)
        
        GPIO.cleanup()
        
        if len(distances) >= 5:
            avg = sum(distances) / len(distances)
            min_dist = min(distances)
            max_dist = max(distances)
            variance = sum((d - avg) ** 2 for d in distances) / len(distances)
            std_dev = variance ** 0.5
            
            return {
                'success': True,
                'avg_distance': avg,
                'min_distance': min_dist,
                'max_distance': max_dist,
                'std_deviation': std_dev,
                'success_rate': success_count,
                'consistency': 'gut' if std_dev < 5 else 'ok' if std_dev < 10 else 'schlecht'
            }
        else:
            return {
                'success': False,
                'success_rate': success_count,
                'reason': f'Nur {success_count}/{num_tests} erfolgreich'
            }
            
    except Exception as e:
        GPIO.cleanup()
        return {
            'success': False,
            'reason': f'Fehler: {e}'
        }

def main():
    print("=" * 70)
    print("  SENSOR 2 ECHO-PIN IDENTIFIKATION")
    print("=" * 70)
    print()
    print(f"Sensor 2: Trigger=GPIO {SENSOR_2_TRIGGER} (Pin 36)")
    print()
    print("⚠️  HINWEIS: Pin 36 ist GPIO 16 = Trigger-Pin!")
    print("   Ein Pin kann nicht gleichzeitig Trigger und Echo sein.")
    print()
    print("Teste mögliche Echo-Pins in der Nähe:")
    print("-" * 70)
    print()
    
    results = []
    
    for echo_info in POSSIBLE_ECHO_PINS:
        print(f"Teste {echo_info['name']} (GPIO {echo_info['gpio']}):")
        result = test_echo_pin(SENSOR_2_TRIGGER, echo_info['gpio'], num_tests=10)
        
        if result['success']:
            print(f"  ✅ FUNKTIONIERT!")
            print(f"     Durchschnitt: {result['avg_distance']:.1f}cm")
            print(f"     Min: {result['min_distance']:.1f}cm, Max: {result['max_distance']:.1f}cm")
            print(f"     Standardabweichung: {result['std_deviation']:.2f}cm ({result['consistency']})")
            print(f"     Erfolgsrate: {result['success_rate']}/10")
            results.append({
                'echo_info': echo_info,
                'result': result
            })
        else:
            print(f"  ❌ Funktioniert nicht: {result.get('reason', 'Unbekannt')}")
        print()
    
    print("=" * 70)
    print("  ERGEBNIS:")
    print("=" * 70)
    print()
    
    if results:
        # Sortiere nach Konsistenz (niedrigste Standardabweichung = beste)
        results.sort(key=lambda x: x['result']['std_deviation'])
        
        print("GEFUNDENE ECHO-PINS (sortiert nach Konsistenz):")
        print("-" * 70)
        for i, res in enumerate(results, 1):
            echo = res['echo_info']
            r = res['result']
            print(f"{i}. {echo['name']} (GPIO {echo['gpio']}):")
            print(f"   Distanz: {r['avg_distance']:.1f}cm")
            print(f"   Konsistenz: {r['consistency']} (StdDev: {r['std_deviation']:.2f}cm)")
            print(f"   Erfolgsrate: {r['success_rate']}/10")
            print()
        
        best = results[0]
        print("=" * 70)
        print(f"  ✅ EMPFOHLENER ECHO-PIN:")
        print("=" * 70)
        print(f"  {best['echo_info']['name']} = GPIO {best['echo_info']['gpio']}")
        print(f"  Distanz: {best['result']['avg_distance']:.1f}cm")
        print(f"  Konsistenz: {best['result']['consistency']}")
        print()
    else:
        print("❌ Keine funktionierenden Echo-Pins gefunden")
        print()
        print("Prüfe:")
        print("  - Ist der Echo-Pin wirklich Pin 36?")
        print("  - Geht der Echo-Pin über Level Shifter?")
        print("  - Hat der Sensor Stromversorgung?")
    
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
