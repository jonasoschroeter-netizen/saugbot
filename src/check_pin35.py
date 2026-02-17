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

def find_physical_pin_gpio(physical_pin):
    """Findet welcher GPIO-Pin einem physischen Pin entspricht."""
    # Standard Raspberry Pi Pinout (40-Pin Header)
    # Von hinten (Pin 40) nach vorne (Pin 1)
    pin_mapping = {
        40: None,  # GND
        39: None,  # GND
        38: 20,    # GPIO 20
        37: 26,    # GPIO 26
        36: 16,    # GPIO 16
        35: None,  # GND (Standard)
        34: None,  # GND
        33: 13,    # GPIO 13
        32: 12,    # GPIO 12
        31: 6,     # GPIO 6
        30: None,  # GND
        # ... weitere Pins
    }
    
    return pin_mapping.get(physical_pin, "UNBEKANNT")

def test_gpio_as_trigger(gpio_pin):
    """Testet ob ein GPIO-Pin als Trigger verwendet werden kann."""
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(gpio_pin, GPIO.OUT)
        GPIO.output(gpio_pin, GPIO.LOW)
        time.sleep(0.001)
        GPIO.output(gpio_pin, GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(gpio_pin, GPIO.LOW)
        
        GPIO.cleanup()
        return True
    except:
        GPIO.cleanup()
        return False

def main():
    print("=" * 70)
    print("  PIN 35 GPIO-IDENTIFIKATION")
    print("=" * 70)
    print()
    
    print("Standard Pin-Mapping sagt: Pin 35 = GND")
    print("Du sagst: Pin 35 ist kein GND")
    print()
    print("Prüfe welche GPIO-Pins in der Nähe sind...")
    print("-" * 70)
    print()
    
    # Teste alle möglichen GPIO-Pins die Pin 35 sein könnten
    possible_gpios = [16, 26, 20, 13, 12, 6, 35]  # Inkl. GPIO 35 falls vorhanden
    
    print("Teste mögliche GPIO-Pins:")
    print()
    
    working_pins = []
    
    for gpio in possible_gpios:
        if test_gpio_as_trigger(gpio):
            # Prüfe Zustand
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(gpio, GPIO.IN)
            state = GPIO.input(gpio)
            GPIO.cleanup()
            
            working_pins.append({
                'gpio': gpio,
                'state': 'HIGH' if state else 'LOW'
            })
            print(f"  ✅ GPIO {gpio}: Kann als Trigger verwendet werden (Zustand: {'HIGH' if state else 'LOW'})")
    
    print()
    print("=" * 70)
    print("  ERGEBNIS:")
    print("=" * 70)
    print()
    
    if working_pins:
        print("Funktionierende GPIO-Pins:")
        for pin_info in working_pins:
            print(f"  - GPIO {pin_info['gpio']} (Zustand: {pin_info['state']})")
        print()
        print("Um herauszufinden welcher GPIO-Pin Pin 35 ist:")
        print("  1. Prüfe physisch welche GPIO-Nummer auf dem Pin steht")
        print("  2. Oder teste jeden GPIO-Pin einzeln als Trigger")
        print()
        print("Falls Pin 35 wirklich GPIO 16 ist:")
        print("  → Dann ist Pin 36 vielleicht GPIO 26 oder ein anderer Pin")
    else:
        print("❌ Keine GPIO-Pins gefunden die als Trigger funktionieren")
    
    print()
    print("=" * 70)
    print("  NÄCHSTE SCHRITTE:")
    print("=" * 70)
    print()
    print("Teile mir mit:")
    print("  - Welcher GPIO-Pin ist Pin 35 wirklich?")
    print("  - Oder teste: python3 src/monitor_sensor.py [GPIO_PIN] [ECHO_PIN]")
    print()
    print("Dann aktualisiere ich die config.py entsprechend!")
    print()

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
