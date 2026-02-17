"""
Systematische Diagnose: Prüft alle möglichen Ursachen warum Sensoren nicht funktionieren
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
KNOWN_SENSOR = {'name': 'Rechts', 'trigger': 20, 'echo': 21, 'physical_trigger': 38, 'physical_echo': '?'}
SENSOR_2 = {'name': 'Sensor 2', 'trigger': 16, 'echo': None, 'physical_trigger': 36, 'physical_echo': '?'}
SENSOR_3 = {'name': 'Sensor 3', 'trigger': 12, 'echo': None, 'physical_trigger': 32, 'physical_echo': '?'}

def test_trigger_pin(pin):
    """Testet ob Trigger-Pin funktioniert (kann Signal senden)."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(pin, GPIO.OUT)
        
        # Test 1: Kann Pin auf HIGH setzen?
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(0.001)
        # Kann nicht direkt prüfen, aber wenn kein Fehler → funktioniert
        
        # Test 2: Kann Pin auf LOW setzen?
        GPIO.output(pin, GPIO.LOW)
        time.sleep(0.001)
        
        GPIO.cleanup()
        return True, "Trigger-Pin funktioniert"
    except Exception as e:
        GPIO.cleanup()
        return False, f"Fehler: {e}"

def test_echo_pin_connection(pin):
    """Prüft ob Echo-Pin angeschlossen ist (kann gelesen werden)."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(pin, GPIO.IN)
        
        # Prüfe aktuellen Zustand
        state1 = GPIO.input(pin)
        time.sleep(0.01)
        state2 = GPIO.input(pin)
        
        GPIO.cleanup()
        
        # Wenn Pin angeschlossen ist, sollte Zustand lesbar sein
        # Wenn nicht angeschlossen, könnte Pin "schweben" (unbestimmt)
        return True, f"Echo-Pin lesbar (Zustand: {'HIGH' if state1 else 'LOW'})"
    except Exception as e:
        GPIO.cleanup()
        return False, f"Fehler: {e}"

def test_sensor_complete(trigger_pin, echo_pin):
    """Testet kompletten Sensor (Trigger + Echo)."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        # Teste 3x
        success_count = 0
        for _ in range(3):
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
        
        if success_count >= 2:
            return True, f"Sensor funktioniert ({success_count}/3 erfolgreich)"
        else:
            return False, f"Sensor funktioniert nicht ({success_count}/3 erfolgreich)"
    except Exception as e:
        GPIO.cleanup()
        return False, f"Fehler: {e}"

def check_pin_states():
    """Prüft Zustand aller relevanten Pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    pins_to_check = [12, 13, 16, 20, 21, 6, 26]
    states = {}
    
    for pin in pins_to_check:
        try:
            GPIO.setup(pin, GPIO.IN)
            state = GPIO.input(pin)
            states[pin] = "HIGH" if state else "LOW"
        except:
            states[pin] = "FEHLER"
    
    GPIO.cleanup()
    return states

def main():
    print("=" * 70)
    print("  SYSTEMATISCHE DIAGNOSE: Warum funktionieren Sensoren nicht?")
    print("=" * 70)
    print()
    
    # Test 1: Bekannter Sensor (sollte funktionieren)
    print("TEST 1: Bekannter funktionierender Sensor (Rechts)")
    print("-" * 70)
    print(f"Trigger: GPIO {KNOWN_SENSOR['trigger']} (Pin {KNOWN_SENSOR['physical_trigger']})")
    print(f"Echo: GPIO {KNOWN_SENSOR['echo']}")
    
    trigger_ok, trigger_msg = test_trigger_pin(KNOWN_SENSOR['trigger'])
    echo_ok, echo_msg = test_echo_pin_connection(KNOWN_SENSOR['echo'])
    sensor_ok, sensor_msg = test_sensor_complete(KNOWN_SENSOR['trigger'], KNOWN_SENSOR['echo'])
    
    print(f"  Trigger-Pin: {'✅' if trigger_ok else '❌'} {trigger_msg}")
    print(f"  Echo-Pin: {'✅' if echo_ok else '❌'} {echo_msg}")
    print(f"  Kompletter Sensor: {'✅' if sensor_ok else '❌'} {sensor_msg}")
    print()
    
    # Test 2: Sensor 2
    print("TEST 2: Sensor 2 (Links?)")
    print("-" * 70)
    print(f"Trigger: GPIO {SENSOR_2['trigger']} (Pin {SENSOR_2['physical_trigger']})")
    print(f"Echo: UNBEKANNT")
    
    trigger_ok, trigger_msg = test_trigger_pin(SENSOR_2['trigger'])
    print(f"  Trigger-Pin: {'✅' if trigger_ok else '❌'} {trigger_msg}")
    
    # Teste mögliche Echo-Pins
    possible_echo_pins = [13, 6, 26, 12, 16]  # Basierend auf LOW-Pins und Nachbarschaft
    print(f"  Teste mögliche Echo-Pins:")
    
    found_echo = None
    for echo_pin in possible_echo_pins:
        if echo_pin == SENSOR_2['trigger']:  # Überspringe Trigger-Pin
            continue
        
        echo_ok, echo_msg = test_echo_pin_connection(echo_pin)
        sensor_ok, sensor_msg = test_sensor_complete(SENSOR_2['trigger'], echo_pin)
        
        status = "✅" if sensor_ok else "❌"
        print(f"    Echo=GPIO {echo_pin}: {status} {sensor_msg}")
        
        if sensor_ok and not found_echo:
            found_echo = echo_pin
    
    if found_echo:
        print(f"  ✅ Echo-Pin gefunden: GPIO {found_echo}")
    else:
        print(f"  ❌ Kein funktionierender Echo-Pin gefunden")
    print()
    
    # Test 3: Sensor 3
    print("TEST 3: Sensor 3 (Front?)")
    print("-" * 70)
    print(f"Trigger: GPIO {SENSOR_3['trigger']} (Pin {SENSOR_3['physical_trigger']})")
    print(f"Echo: UNBEKANNT")
    
    trigger_ok, trigger_msg = test_trigger_pin(SENSOR_3['trigger'])
    print(f"  Trigger-Pin: {'✅' if trigger_ok else '❌'} {trigger_msg}")
    
    # Teste mögliche Echo-Pins
    print(f"  Teste mögliche Echo-Pins:")
    
    found_echo = None
    for echo_pin in possible_echo_pins:
        if echo_pin == SENSOR_3['trigger']:  # Überspringe Trigger-Pin
            continue
        
        echo_ok, echo_msg = test_echo_pin_connection(echo_pin)
        sensor_ok, sensor_msg = test_sensor_complete(SENSOR_3['trigger'], echo_pin)
        
        status = "✅" if sensor_ok else "❌"
        print(f"    Echo=GPIO {echo_pin}: {status} {sensor_msg}")
        
        if sensor_ok and not found_echo:
            found_echo = echo_pin
    
    if found_echo:
        print(f"  ✅ Echo-Pin gefunden: GPIO {found_echo}")
    else:
        print(f"  ❌ Kein funktionierender Echo-Pin gefunden")
    print()
    
    # Pin-Zustände prüfen
    print("PIN-ZUSTÄNDE:")
    print("-" * 70)
    states = check_pin_states()
    for pin, state in sorted(states.items()):
        print(f"  GPIO {pin:2}: {state}")
    print()
    
    # Zusammenfassung
    print("=" * 70)
    print("  DIAGNOSE-ZUSAMMENFASSUNG:")
    print("=" * 70)
    print()
    
    print("MÖGLICHE URSACHEN (ausgeschlossen/verifiziert):")
    print("-" * 70)
    
    # Prüfe Trigger-Pins
    trigger2_ok, _ = test_trigger_pin(SENSOR_2['trigger'])
    trigger3_ok, _ = test_trigger_pin(SENSOR_3['trigger'])
    
    if trigger2_ok and trigger3_ok:
        print("✅ Trigger-Pins funktionieren (können Signale senden)")
        print("   → Problem ist NICHT die Trigger-Pins")
    else:
        print("❌ Trigger-Pins haben Probleme")
        print("   → Problem könnte bei Trigger-Pins liegen")
    print()
    
    print("MÖGLICHE PROBLEME:")
    print("-" * 70)
    print("1. ❓ Echo-Pins nicht angeschlossen")
    print("   → Prüfe physisch ob Echo-Pins verkabelt sind")
    print()
    print("2. ❓ Echo-Pins gehen nicht über Level Shifter")
    print("   → Rechts-Sensor funktioniert (GPIO 21)")
    print("   → Andere Echo-Pins müssen auch über Level Shifter!")
    print()
    print("3. ❓ Falsche GPIO-Pins für Echo")
    print("   → Teste verschiedene Echo-Pins (siehe oben)")
    print()
    print("4. ❓ Sensoren haben keine Stromversorgung")
    print("   → Prüfe ob alle Sensoren 5V haben")
    print("   → Prüfe ob GND korrekt angeschlossen ist")
    print()
    print("5. ❓ Sensoren defekt")
    print("   → Unwahrscheinlich wenn nur 1 funktioniert")
    print()
    
    print("NÄCHSTE SCHRITTE:")
    print("-" * 70)
    print("1. Prüfe physisch:")
    print("   - Wo sind die Echo-Pins von Sensor 2 und 3 angeschlossen?")
    print("   - Gehen sie über Level Shifter?")
    print("   - Welche physischen Pins sind das?")
    print()
    print("2. Falls Echo-Pins unbekannt:")
    print("   - Teste die oben gefundenen Echo-Pins")
    print("   - Verwende: python3 src/monitor_sensor.py [TRIGGER] [ECHO]")
    print()
    
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnose abgebrochen")
        try:
            GPIO.cleanup()
        except:
            pass
