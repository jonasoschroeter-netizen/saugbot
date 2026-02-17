"""
Live-Monitoring für einen einzelnen Sensor
Zeigt kontinuierlich die Distanz an
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

# Sensor-Pins (kann als Parameter übergeben werden)
SENSOR_TRIGGER = 20
SENSOR_ECHO = 21

def get_distance(trigger_pin, echo_pin):
    """Misst die Distanz eines Sensors."""
    try:
        # Send trigger
        GPIO.output(trigger_pin, GPIO.LOW)
        time.sleep(0.00002)
        GPIO.output(trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(trigger_pin, GPIO.LOW)
        
        # Wait for echo HIGH
        timeout = time.time() + 0.05
        while GPIO.input(echo_pin) == GPIO.LOW:
            if time.time() > timeout:
                return None
            time.sleep(0.00001)
        
        echo_start = time.time()
        
        # Wait for echo LOW
        timeout = echo_start + 0.05
        echo_end = None
        while GPIO.input(echo_pin) == GPIO.HIGH:
            if time.time() > timeout:
                return None
            echo_end = time.time()
            time.sleep(0.00001)
        
        if echo_start and echo_end:
            pulse_duration = echo_end - echo_start
            distance_cm = (pulse_duration * 343 * 100) / 2
            
            if 2 <= distance_cm <= 400:
                return round(distance_cm, 1)
        
        return None
        
    except Exception as e:
        return None

def format_distance(distance):
    """Formatiert Distanz mit Status."""
    if distance is None:
        return "❌ ---"
    
    if distance < 10:
        return f"🔴 {distance:5.1f}cm (SEHR NAH!)"
    elif distance < 20:
        return f"🟡 {distance:5.1f}cm (NAH)"
    elif distance < 50:
        return f"🟢 {distance:5.1f}cm (OK)"
    else:
        return f"🔵 {distance:5.1f}cm (WEIT)"

def main():
    # Prüfe ob Pins als Parameter übergeben wurden
    if len(sys.argv) >= 3:
        try:
            trigger = int(sys.argv[1])
            echo = int(sys.argv[2])
            global SENSOR_TRIGGER, SENSOR_ECHO
            SENSOR_TRIGGER = trigger
            SENSOR_ECHO = echo
        except ValueError:
            print("FEHLER: Ungültige Pin-Nummern")
            print("Verwendung: python3 monitor_sensor.py [TRIGGER_PIN] [ECHO_PIN]")
            sys.exit(1)
    
    print("=" * 70)
    print("  LIVE SENSOR-MONITORING")
    print("=" * 70)
    print()
    print(f"Sensor-Konfiguration:")
    print(f"  Trigger: GPIO {SENSOR_TRIGGER}")
    print(f"  Echo:    GPIO {SENSOR_ECHO}")
    print()
    print("Drücke Ctrl+C zum Beenden")
    print()
    print("-" * 70)
    
    # GPIO Setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(SENSOR_TRIGGER, GPIO.OUT)
    GPIO.setup(SENSOR_ECHO, GPIO.IN)
    
    # Initialisiere Statistiken
    measurements = []
    successful = 0
    failed = 0
    
    try:
        while True:
            distance = get_distance(SENSOR_TRIGGER, SENSOR_ECHO)
            
            if distance is not None:
                successful += 1
                measurements.append(distance)
                if len(measurements) > 100:
                    measurements.pop(0)  # Behalte nur letzte 100 Messungen
                
                # Zeige aktuelle Messung
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] {format_distance(distance)}")
                
                # Zeige Statistik alle 10 Messungen
                if successful % 10 == 0:
                    if measurements:
                        avg = sum(measurements) / len(measurements)
                        min_dist = min(measurements)
                        max_dist = max(measurements)
                        print(f"         Statistik: Min={min_dist:.1f}cm, Avg={avg:.1f}cm, Max={max_dist:.1f}cm")
                        print()
            else:
                failed += 1
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] ❌ FEHLER - Keine Messung möglich")
            
            time.sleep(0.2)  # Alle 200ms messen
    
    except KeyboardInterrupt:
        print()
        print("-" * 70)
        print("=" * 70)
        print("  ZUSAMMENFASSUNG:")
        print("=" * 70)
        print()
        print(f"Erfolgreiche Messungen: {successful}")
        print(f"Fehlgeschlagene Messungen: {failed}")
        if measurements:
            avg = sum(measurements) / len(measurements)
            min_dist = min(measurements)
            max_dist = max(measurements)
            print()
            print(f"Distanz-Statistik:")
            print(f"  Minimum: {min_dist:.1f} cm")
            print(f"  Durchschnitt: {avg:.1f} cm")
            print(f"  Maximum: {max_dist:.1f} cm")
        print()
        print("=" * 70)
    
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
