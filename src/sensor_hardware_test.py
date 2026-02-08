"""
Erweiterter Hardware-Test für Ultraschall-Sensor
Prüft Verkabelung und Level Shifter
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

def test_echo_pin():
    """Test Echo-Pin direkt."""
    print("=" * 60)
    print("Echo-Pin Hardware-Test")
    print("=" * 60)
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup Echo-Pin als INPUT mit Pull-Down
    GPIO.setup(ULTRASONIC_LEFT_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    print(f"Echo-Pin (GPIO {ULTRASONIC_LEFT_ECHO}) als INPUT mit Pull-Down konfiguriert")
    print()
    
    print("Prüfe Echo-Pin Status (10 Sekunden):")
    for i in range(20):
        state = GPIO.input(ULTRASONIC_LEFT_ECHO)
        print(f"  {i*0.5:.1f}s: {'HIGH' if state else 'LOW'}")
        time.sleep(0.5)
    
    print()
    print("⚠️  Wenn Echo-Pin dauerhaft HIGH ist:")
    print("   → Level Shifter könnte defekt sein")
    print("   → Echo-Pin könnte falsch angeschlossen sein")
    print("   → Sensor könnte defekt sein")
    print()
    
    GPIO.cleanup()

def test_trigger_pin():
    """Test Trigger-Pin."""
    print("=" * 60)
    print("Trigger-Pin Test")
    print("=" * 60)
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    GPIO.setup(ULTRASONIC_LEFT_TRIGGER, GPIO.OUT)
    
    print(f"Trigger-Pin (GPIO {ULTRASONIC_LEFT_TRIGGER}) als OUTPUT konfiguriert")
    print()
    
    print("Sende 5 Trigger-Pulse (jeweils 10µs HIGH):")
    for i in range(5):
        GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
        time.sleep(0.00002)
        GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
        print(f"  Pulse {i+1} gesendet")
        time.sleep(0.1)
    
    print()
    print("✅ Trigger-Pin funktioniert (wenn kein Fehler)")
    print()
    
    GPIO.cleanup()

def test_with_pull_up():
    """Test mit Pull-Up statt Pull-Down."""
    print("=" * 60)
    print("Test mit Pull-Up Widerstand")
    print("=" * 60)
    print()
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    
    # Setup Trigger
    GPIO.setup(ULTRASONIC_LEFT_TRIGGER, GPIO.OUT)
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
    time.sleep(0.1)
    
    # Setup Echo mit Pull-Up
    GPIO.setup(ULTRASONIC_LEFT_ECHO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    print("Echo-Pin mit Pull-Up konfiguriert")
    print("Initialer Zustand:", "HIGH" if GPIO.input(ULTRASONIC_LEFT_ECHO) else "LOW")
    print()
    
    # Send trigger
    print("Sende Trigger...")
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(ULTRASONIC_LEFT_TRIGGER, GPIO.LOW)
    
    # Monitor echo
    print("Überwache Echo-Pin (2 Sekunden):")
    states = []
    for i in range(40):
        state = GPIO.input(ULTRASONIC_LEFT_ECHO)
        states.append(state)
        if i % 10 == 0:
            print(f"  {i*0.05:.2f}s: {'HIGH' if state else 'LOW'}")
        time.sleep(0.05)
    
    high_count = sum(states)
    print()
    print(f"Ergebnis: {high_count}/40 Messungen waren HIGH")
    
    if high_count == 40:
        print("❌ Echo-Pin bleibt dauerhaft HIGH")
        print("   → Hardware-Problem wahrscheinlich")
    elif high_count == 0:
        print("❌ Echo-Pin bleibt dauerhaft LOW")
        print("   → Sensor reagiert nicht")
    else:
        print("✅ Echo-Pin ändert Zustand")
        print("   → Sensor könnte funktionieren")
    
    GPIO.cleanup()

def main():
    """Hauptfunktion."""
    print()
    print("🔧 Erweiterter Hardware-Test für HC-SR04 Sensor")
    print()
    
    print("WICHTIG: Prüfe zuerst die Verkabelung!")
    print()
    print("Verkabelung sollte sein:")
    print("  - VCC → 5V")
    print("  - GND → GND")
    print("  - Trig → GPIO 4 (über Level Shifter oder direkt)")
    print("  - Echo → GPIO 14 (MUSS über Level Shifter: 5V → 3.3V)")
    print()
    
    input("Drücke Enter zum Fortfahren...")
    print()
    
    # Test 1: Echo-Pin Status
    test_echo_pin()
    print()
    
    # Test 2: Trigger-Pin
    test_trigger_pin()
    print()
    
    # Test 3: Mit Pull-Up
    test_with_pull_up()
    print()
    
    print("=" * 60)
    print("Zusammenfassung")
    print("=" * 60)
    print()
    print("Wenn Echo-Pin dauerhaft HIGH bleibt:")
    print("  1. Prüfe Level Shifter Verkabelung")
    print("  2. Prüfe ob Level Shifter funktioniert (mit Multimeter)")
    print("  3. Teste Sensor ohne Level Shifter (VORSICHT: nur 3.3V Echo!)")
    print("  4. Teste mit anderem Sensor (falls verfügbar)")
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest abgebrochen")
        GPIO.cleanup()
    except Exception as e:
        print(f"\n\nFehler: {e}")
        import traceback
        traceback.print_exc()
        GPIO.cleanup()
