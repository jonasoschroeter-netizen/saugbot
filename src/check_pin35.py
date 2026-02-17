"""
Prüft welcher GPIO-Pin Pin 35 wirklich ist
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    print("FEHLER: RPi.GPIO nicht verfügbar")
    sys.exit(1)

def check_pin(pin_number):
    """Prüft einen GPIO-Pin."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(pin_number, GPIO.IN)
        state = GPIO.input(pin_number)
        
        GPIO.cleanup()
        
        return True, "HIGH" if state else "LOW"
    except Exception as e:
        GPIO.cleanup()
        return False, str(e)

def main():
    print("=" * 70)
    print("  PIN 35 PRÜFUNG")
    print("=" * 70)
    print()
    
    # Standard Pin-Mapping (kann je nach Pi-Modell variieren)
    print("Standard Pin-Mapping (Raspberry Pi 4/3):")
    print("-" * 70)
    print("Pin 35 = GND (Masse)")
    print()
    
    # Prüfe mögliche GPIO-Pins die Pin 35 sein könnten
    # Basierend auf verschiedenen Pi-Modellen
    possible_pins = {
        35: "Standard: GND",
        16: "GPIO 16 (könnte Pin 36 sein)",
        26: "GPIO 26 (könnte Pin 37 sein)",
        20: "GPIO 20 (könnte Pin 38 sein)",
    }
    
    print("Prüfe Pin 35...")
    print("-" * 70)
    
    # Versuche Pin 35 als GPIO zu verwenden
    # Wenn es GND ist, sollte das fehlschlagen
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Versuche Pin 35 als GPIO zu konfigurieren
        # Wenn es GND ist, sollte das problematisch sein
        GPIO.setup(35, GPIO.IN)
        state = GPIO.input(35)
        
        print(f"✅ Pin 35 kann als GPIO verwendet werden!")
        print(f"   Zustand: {'HIGH' if state else 'LOW'}")
        print(f"   → Pin 35 ist GPIO 35 (oder ein anderer GPIO-Pin)")
        
        GPIO.cleanup()
        
        # Teste ob es als Output funktioniert
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(35, GPIO.OUT)
        GPIO.output(35, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(35, GPIO.LOW)
        GPIO.cleanup()
        
        print(f"   → Kann als Output verwendet werden (Trigger möglich)")
        print()
        print("=" * 70)
        print("  ERGEBNIS:")
        print("=" * 70)
        print()
        print("✅ Pin 35 ist ein GPIO-Pin!")
        print("   → Kann als Trigger verwendet werden")
        print()
        print("⚠️  HINWEIS: Das ist ungewöhnlich!")
        print("   Standard Raspberry Pi Pinout zeigt Pin 35 als GND")
        print("   Vielleicht verwendest du:")
        print("   - Ein anderes Pi-Modell")
        print("   - Eine andere Pin-Nummerierung")
        print("   - Ein HAT/Shield das Pins umbelegt")
        
    except Exception as e:
        print(f"❌ Pin 35 kann nicht als GPIO verwendet werden")
        print(f"   Fehler: {e}")
        print(f"   → Pin 35 ist wahrscheinlich GND (wie erwartet)")
        print()
        print("=" * 70)
        print("  LÖSUNG:")
        print("=" * 70)
        print()
        print("Falls Pin 35 wirklich GND ist:")
        print("  → Sensor 2 Trigger muss Pin 36 (GPIO 16) sein")
        print()
        print("Falls Pin 35 wirklich ein GPIO-Pin ist:")
        print("  → Teile mir mit welcher GPIO-Pin das ist")
        print("  → Dann aktualisiere ich die config.py")
    
    print()
    print("=" * 70)

if __name__ == "__main__":
    import time
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest abgebrochen")
        try:
            GPIO.cleanup()
        except:
            pass
