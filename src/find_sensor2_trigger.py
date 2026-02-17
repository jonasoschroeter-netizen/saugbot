"""
Findet den richtigen Trigger-Pin für Sensor 2
Testet alle möglichen GPIO-Pins in der Nähe von Pin 34
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

# Mögliche Trigger-Pins (GPIO-Pins in der Nähe von Pin 34)
# Pin 34 ist GND, also testen wir die benachbarten GPIO-Pins
POSSIBLE_TRIGGER_PINS = [
    {'gpio': 16, 'physical': 36, 'name': 'Pin 36'},
    {'gpio': 13, 'physical': 33, 'name': 'Pin 33'},
    {'gpio': 26, 'physical': 37, 'name': 'Pin 37'},
    {'gpio': 12, 'physical': 32, 'name': 'Pin 32'},
    {'gpio': 6, 'physical': 31, 'name': 'Pin 31'},
]

# Bekannte Echo-Pins die funktionieren
KNOWN_ECHO_PINS = [13, 6, 26]

def test_trigger_pin(trigger_pin, echo_pin):
    """Testet ob Trigger-Pin funktioniert."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        success_count = 0
        
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
                success_count += 1
            
            time.sleep(0.1)
        
        GPIO.cleanup()
        
        return success_count >= 3  # Mindestens 3 von 5 erfolgreich
        
    except Exception as e:
        GPIO.cleanup()
        return False

def main():
    print("=" * 70)
    print("  SENSOR 2 TRIGGER-PIN FINDEN")
    print("=" * 70)
    print()
    print("⚠️  HINWEIS: Pin 34 ist GND (Masse), kein GPIO-Pin!")
    print("   Ein Trigger-Pin muss ein GPIO-Pin sein.")
    print()
    print("Teste mögliche Trigger-Pins in der Nähe:")
    print("-" * 70)
    print()
    
    found_combinations = []
    
    for trigger_info in POSSIBLE_TRIGGER_PINS:
        # Überspringe bekannte Trigger-Pins
        if trigger_info['gpio'] == 20:  # Sensor 1
            continue
        if trigger_info['gpio'] == 12:  # Sensor 3
            continue
        
        print(f"Teste {trigger_info['name']} (GPIO {trigger_info['gpio']}) als Trigger:")
        
        for echo_pin in KNOWN_ECHO_PINS:
            if echo_pin == trigger_info['gpio']:  # Überspringe wenn gleich
                continue
            
            works = test_trigger_pin(trigger_info['gpio'], echo_pin)
            
            if works:
                print(f"  ✅ Funktioniert mit Echo=GPIO {echo_pin}")
                found_combinations.append({
                    'trigger': trigger_info,
                    'echo': echo_pin
                })
            else:
                print(f"  ❌ Funktioniert nicht mit Echo=GPIO {echo_pin}")
        
        print()
    
    print("=" * 70)
    print("  ERGEBNIS:")
    print("=" * 70)
    print()
    
    if found_combinations:
        print("GEFUNDENE KOMBINATIONEN:")
        print("-" * 70)
        for i, combo in enumerate(found_combinations, 1):
            trigger = combo['trigger']
            echo = combo['echo']
            print(f"{i}. Trigger: {trigger['name']} (GPIO {trigger['gpio']})")
            print(f"   Echo: GPIO {echo}")
            print()
        
        # Empfehle beste Kombination
        best = found_combinations[0]
        print("=" * 70)
        print(f"  ✅ EMPFOHLENE KOMBINATION:")
        print("=" * 70)
        print(f"  Trigger: {best['trigger']['name']} = GPIO {best['trigger']['gpio']}")
        print(f"  Echo: GPIO {best['echo']}")
        print()
        print("  Teste diese Kombination:")
        print(f"  python3 src/monitor_sensor.py {best['trigger']['gpio']} {best['echo']}")
    else:
        print("❌ Keine funktionierenden Kombinationen gefunden")
        print()
        print("Prüfe:")
        print("  - Ist Pin 34 wirklich der Trigger? (Pin 34 ist GND!)")
        print("  - Welcher physische Pin ist wirklich der Trigger?")
        print("  - Zählst du die Pins von vorne statt von hinten?")
    
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
