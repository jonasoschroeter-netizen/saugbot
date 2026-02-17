"""
Diagnose-Tool: Testet alle GPIO-Pins und zeigt welche Signale ankommen
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

# Alle verfügbaren GPIO-Pins
ALL_GPIO_PINS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

def test_pin_as_trigger(trigger_pin, echo_pin):
    """Testet ob Trigger-Pin funktioniert."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(trigger_pin, GPIO.OUT)
        GPIO.setup(echo_pin, GPIO.IN)
        
        # Test 1: Trigger senden
        GPIO.output(trigger_pin, GPIO.LOW)
        time.sleep(0.00002)
        GPIO.output(trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, GPIO.LOW)
        
        # Test 2: Echo lesen
        timeout = time.time() + 0.05
        echo_high = False
        echo_low = False
        
        # Warte auf Echo HIGH
        start_time = time.time()
        while time.time() < timeout:
            if GPIO.input(echo_pin) == GPIO.HIGH:
                echo_high = True
                break
            time.sleep(0.00001)
        
        if echo_high:
            # Warte auf Echo LOW
            timeout = time.time() + 0.05
            while time.time() < timeout:
                if GPIO.input(echo_pin) == GPIO.LOW:
                    echo_low = True
                    break
                time.sleep(0.00001)
        
        if echo_high and echo_low:
            return True, "OK"
        elif echo_high:
            return False, "Echo HIGH aber kein LOW"
        else:
            return False, "Kein Echo HIGH"
            
    except Exception as e:
        return False, f"Fehler: {e}"

def check_pin_state(pin):
    """Prüft den aktuellen Zustand eines Pins."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin, GPIO.IN)
        state = GPIO.input(pin)
        return "HIGH" if state else "LOW"
    except:
        return "FEHLER"

def main():
    print("=" * 70)
    print("  GPIO PIN-DIAGNOSE")
    print("=" * 70)
    print()
    print("Teste alle GPIO-Pins...")
    print("Drücke Ctrl+C zum Beenden")
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Bekannter funktionierender Sensor
    KNOWN_TRIGGER = 20
    KNOWN_ECHO = 21
    
    print(f"Bekannter funktionierender Sensor: Trigger=GPIO {KNOWN_TRIGGER}, Echo=GPIO {KNOWN_ECHO} (Rechts)")
    print()
    print("-" * 70)
    
    # Teste alle Pin-Kombinationen
    found_sensors = []
    problem_pins = []
    
    # Berechne Gesamtanzahl der Tests
    total_combinations = 0
    for trigger in ALL_GPIO_PINS:
        for echo in ALL_GPIO_PINS:
            if trigger == echo:
                continue
            if trigger == KNOWN_TRIGGER and echo == KNOWN_ECHO:
                continue
            total_combinations += 1
    
    print("Teste Pin-Kombinationen...")
    print(f"Gesamt: {total_combinations} Kombinationen")
    print()
    
    start_time = time.time()
    tested = 0
    
    for trigger in ALL_GPIO_PINS:
        for echo in ALL_GPIO_PINS:
            if trigger == echo:
                continue
            
            # Überspringe bekannten Sensor
            if trigger == KNOWN_TRIGGER and echo == KNOWN_ECHO:
                continue
            
            tested += 1
            progress = (tested / total_combinations) * 100
            elapsed = time.time() - start_time
            if tested > 0:
                avg_time = elapsed / tested
                remaining = (total_combinations - tested) * avg_time
            else:
                remaining = 0
            
            # Fortschrittsanzeige
            bar_length = 50
            filled = int(bar_length * progress / 100)
            bar = "█" * filled + "░" * (bar_length - filled)
            
            print(f"\r[{bar}] {progress:5.1f}% | {tested}/{total_combinations} | ⏱️  ~{int(remaining)}s verbleibend", end="", flush=True)
            
            # Teste mehrmals
            success_count = 0
            for _ in range(3):
                works, message = test_pin_as_trigger(trigger, echo)
                if works:
                    success_count += 1
                time.sleep(0.1)
            
            if success_count >= 2:  # Mindestens 2 von 3 erfolgreich
                found_sensors.append({
                    'trigger': trigger,
                    'echo': echo,
                    'success_rate': success_count
                })
                print(f"\n✅ Sensor gefunden: Trigger=GPIO {trigger}, Echo=GPIO {echo} ({success_count}/3 erfolgreich)")
            elif success_count == 1:
                # Teilweise funktionierend - könnte ein Problem sein
                problem_pins.append({
                    'trigger': trigger,
                    'echo': echo,
                    'issue': 'Unzuverlässig (nur 1/3 erfolgreich)'
                })
    
    # Finale Fortschrittsanzeige
    print(f"\r[{'█' * bar_length}] 100.0% | {total_combinations}/{total_combinations} | ✅ Fertig!        ")
    print()
    
    GPIO.cleanup()
    
    print()
    print("=" * 70)
    print("  DIAGNOSE-ERGEBNIS:")
    print("=" * 70)
    print()
    
    print("GEFUNDENE SENSOREN:")
    print("-" * 70)
    print(f"✅ Rechts Sensor: Trigger=GPIO {KNOWN_TRIGGER}, Echo=GPIO {KNOWN_ECHO}")
    
    if found_sensors:
        for i, sensor in enumerate(found_sensors, 1):
            print(f"✅ Sensor {i}: Trigger=GPIO {sensor['trigger']}, Echo=GPIO {sensor['echo']}")
    else:
        print("❌ Keine weiteren Sensoren gefunden")
    
    print()
    
    if problem_pins:
        print("PROBLEM-PINS (unzuverlässig):")
        print("-" * 70)
        for pin in problem_pins:
            print(f"⚠️  Trigger=GPIO {pin['trigger']}, Echo=GPIO {pin['echo']}: {pin['issue']}")
        print()
    
    print("MÖGLICHE PROBLEME:")
    print("-" * 70)
    
    if len(found_sensors) < 2:
        print("❌ Nur 1 Sensor gefunden (Rechts)")
        print()
        print("Mögliche Ursachen:")
        print("  1. Andere Sensoren nicht angeschlossen")
        print("  2. Andere Sensoren haben keine Stromversorgung (5V)")
        print("  3. Andere Sensoren verwenden andere GPIO-Pins")
        print("  4. Echo-Pins gehen nicht über Level Shifter")
        print("  5. Falsche Verkabelung")
        print()
        print("Prüfe:")
        print("  - Sind alle 3 Sensoren physisch angeschlossen?")
        print("  - Haben alle Sensoren 5V Strom?")
        print("  - Gehen alle Echo-Pins über Level Shifter?")
        print("  - Welche physischen Pins hast du verwendet?")
    
    print()
    print("=" * 70)
    
    # Zeige Pin-Zustände
    print()
    print("AKTUELLE PIN-ZUSTÄNDE (als Input):")
    print("-" * 70)
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    for pin in ALL_GPIO_PINS:
        try:
            GPIO.setup(pin, GPIO.IN)
            state = GPIO.input(pin)
            state_str = "HIGH" if state else "LOW"
            print(f"GPIO {pin:2}: {state_str}")
        except:
            print(f"GPIO {pin:2}: FEHLER")
    
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnose abgebrochen")
        try:
            GPIO.cleanup()
        except:
            pass
