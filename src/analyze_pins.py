"""
Analysiert Pin-Zustände und hilft bei der Fehlersuche
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

# Pin-Zustände vom Diagnose-Tool
PIN_STATES = {
    2: "HIGH", 3: "HIGH", 4: "HIGH", 5: "HIGH", 6: "HIGH", 7: "HIGH",
    8: "HIGH", 9: "HIGH", 10: "HIGH", 11: "HIGH", 12: "LOW", 13: "HIGH",
    14: "HIGH", 15: "HIGH", 16: "LOW", 17: "HIGH", 18: "HIGH", 19: "HIGH",
    20: "HIGH", 21: "LOW", 22: "HIGH", 23: "HIGH", 24: "HIGH", 25: "HIGH",
    26: "HIGH", 27: "LOW"
}

def analyze_pin_states():
    """Analysiert die Pin-Zustände."""
    print("=" * 70)
    print("  PIN-ZUSTANDS-ANALYSE")
    print("=" * 70)
    print()
    
    # Funktionierender Sensor
    print("✅ FUNKTIONIERENDER SENSOR (Rechts):")
    print("-" * 70)
    print("  Trigger: GPIO 20 = HIGH (korrekt - wartet auf Signal)")
    print("  Echo:    GPIO 21 = LOW (korrekt - wartet auf Echo)")
    print()
    print("  → Dieser Sensor funktioniert korrekt!")
    print()
    
    # LOW Pins (könnten Echo-Pins sein)
    low_pins = [pin for pin, state in PIN_STATES.items() if state == "LOW"]
    print("LOW PINS (könnten Echo-Pins sein):")
    print("-" * 70)
    for pin in sorted(low_pins):
        print(f"  GPIO {pin:2}: LOW")
    print()
    print("  → Echo-Pins sollten normalerweise LOW sein")
    print("  → Sie werden HIGH wenn ein Echo-Signal kommt")
    print()
    
    # HIGH Pins (könnten Trigger-Pins sein)
    high_pins = [pin for pin, state in PIN_STATES.items() if state == "HIGH"]
    print("HIGH PINS (könnten Trigger-Pins sein):")
    print("-" * 70)
    for pin in sorted(high_pins):
        print(f"  GPIO {pin:2}: HIGH")
    print()
    print("  → Trigger-Pins können HIGH oder LOW sein")
    print()
    
    # Mögliche Sensor-Kombinationen
    print("MÖGLICHE SENSOR-KOMBINATIONEN:")
    print("-" * 70)
    print("Basierend auf den Pin-Zuständen:")
    print()
    
    # Teste LOW-Pins als Echo
    possible_sensors = []
    for echo_pin in low_pins:
        if echo_pin == 21:  # Überspringe bekannten Sensor
            continue
        for trigger_pin in high_pins:
            if trigger_pin == 20:  # Überspringe bekannten Sensor
                continue
            if trigger_pin != echo_pin:
                possible_sensors.append({
                    'trigger': trigger_pin,
                    'echo': echo_pin,
                    'reason': f'Echo={echo_pin} ist LOW (korrekt für Echo-Pin)'
                })
    
    if possible_sensors:
        print("Mögliche Sensor-Kombinationen (basierend auf Pin-Zuständen):")
        print()
        for i, sensor in enumerate(possible_sensors[:10], 1):  # Zeige erste 10
            print(f"  {i}. Trigger=GPIO {sensor['trigger']}, Echo=GPIO {sensor['echo']}")
            print(f"     → {sensor['reason']}")
        if len(possible_sensors) > 10:
            print(f"     ... und {len(possible_sensors) - 10} weitere")
        print()
        print("  ⚠️  Diese sind nur Vorschläge - müssen getestet werden!")
    else:
        print("❌ Keine offensichtlichen Sensor-Kombinationen gefunden")
    
    print()
    print("=" * 70)
    print("  DIAGNOSE:")
    print("=" * 70)
    print()
    
    print("PROBLEM:")
    print("  Nur 1 von 3 Sensoren gefunden")
    print()
    
    print("MÖGLICHE URSACHEN:")
    print("-" * 70)
    print("1. ❌ Andere Sensoren nicht angeschlossen")
    print("   → Prüfe physisch ob alle 3 Sensoren verkabelt sind")
    print()
    print("2. ❌ Andere Sensoren haben keine Stromversorgung")
    print("   → Prüfe ob alle Sensoren 5V haben")
    print("   → Prüfe ob GND korrekt angeschlossen ist")
    print()
    print("3. ❌ Echo-Pins gehen nicht über Level Shifter")
    print("   → Rechts-Sensor funktioniert (GPIO 21)")
    print("   → Andere Echo-Pins müssen auch über Level Shifter!")
    print()
    print("4. ❌ Falsche GPIO-Pins verwendet")
    print("   → Prüfe welche physischen Pins du verwendet hast")
    print("   → Vergleiche mit Pin-Mapping-Tabelle")
    print()
    
    print("NÄCHSTE SCHRITTE:")
    print("-" * 70)
    print("1. Prüfe physisch:")
    print("   - Sind alle 3 Sensoren angeschlossen?")
    print("   - Haben alle Sensoren 5V?")
    print("   - Gehen alle Echo-Pins über Level Shifter?")
    print()
    print("2. Teste mögliche Kombinationen:")
    print("   python3 src/monitor_sensor.py [TRIGGER] [ECHO]")
    print()
    print("3. Teile mir mit:")
    print("   - Welche physischen Pins hast du verwendet?")
    print("   - Welche Sensoren sind wo angeschlossen?")
    print()
    
    print("=" * 70)

def test_specific_pins():
    """Testet spezifische Pin-Kombinationen."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Mögliche Kombinationen basierend auf LOW-Pins
    low_pins = [12, 16, 21, 27]
    high_pins = [pin for pin in PIN_STATES.keys() if PIN_STATES[pin] == "HIGH"]
    
    print()
    print("=" * 70)
    print("  SCHNELLTEST: Teste mögliche Kombinationen")
    print("=" * 70)
    print()
    
    found = []
    for echo in low_pins:
        if echo == 21:  # Überspringe bekannten
            continue
        for trigger in high_pins:
            if trigger == 20:  # Überspringe bekannten
                continue
            if trigger != echo:
                # Teste schnell
                try:
                    GPIO.setup(trigger, GPIO.OUT)
                    GPIO.setup(echo, GPIO.IN)
                    
                    GPIO.output(trigger, GPIO.LOW)
                    time.sleep(0.00002)
                    GPIO.output(trigger, GPIO.HIGH)
                    time.sleep(0.00001)
                    GPIO.output(trigger, GPIO.LOW)
                    
                    timeout = time.time() + 0.05
                    echo_received = False
                    while time.time() < timeout:
                        if GPIO.input(echo) == GPIO.HIGH:
                            echo_received = True
                            break
                        time.sleep(0.00001)
                    
                    if echo_received:
                        found.append({'trigger': trigger, 'echo': echo})
                        print(f"✅ Möglicher Sensor: Trigger=GPIO {trigger}, Echo=GPIO {echo}")
                except:
                    pass
    
    GPIO.cleanup()
    
    if found:
        print()
        print(f"Gefunden: {len(found)} mögliche Sensoren")
    else:
        print()
        print("❌ Keine weiteren Sensoren gefunden")

if __name__ == "__main__":
    analyze_pin_states()
    if GPIO_AVAILABLE:
        test_specific_pins()
