"""
Test-Programm für alle 3 Ultraschallsensoren
Zeigt kontinuierlich die Distanzen aller Sensoren an
"""

import time
import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ultrasonic_sensor import UltrasonicSensorArray
    from config import COLLISION_DISTANCE_CM
    SENSOR_AVAILABLE = True
except ImportError as e:
    print(f"Fehler: Konnte Sensoren nicht importieren: {e}")
    SENSOR_AVAILABLE = False
    sys.exit(1)


def format_distance(distance):
    """Formatiert Distanz mit Status-Icon."""
    if distance is None:
        return "❌ ---"
    
    if distance < COLLISION_DISTANCE_CM:
        return f"🔴 {distance:5.1f}cm"
    elif distance < COLLISION_DISTANCE_CM + 5:
        return f"🟡 {distance:5.1f}cm"
    else:
        return f"🟢 {distance:5.1f}cm"


def main():
    """Testet alle 3 Sensoren kontinuierlich."""
    print("=" * 70)
    print("  ULTRASCHALL-SENSOREN TEST - Alle 3 Sensoren")
    print("=" * 70)
    print(f"Schwellenwert für Kollision: {COLLISION_DISTANCE_CM} cm")
    print("Drücke Ctrl+C zum Beenden\n")
    
    # Initialisiere alle Sensoren
    print("Initialisiere Sensoren...")
    sensors = UltrasonicSensorArray()
    print("✅ Alle Sensoren initialisiert!\n")
    
    # Kurze Pause für Sensor-Stabilisierung
    time.sleep(0.5)
    
    try:
        iteration = 0
        while True:
            iteration += 1
            
            # Lese alle Sensoren aus
            distances = sensors.get_all_distances()
            
            # Ausgabe mit Zeitstempel
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] Messung #{iteration}")
            print(f"  Front:  {format_distance(distances['front'])}")
            print(f"  Links:  {format_distance(distances['left'])}")
            print(f"  Rechts: {format_distance(distances['right'])}")
            print()
            
            # Statistik anzeigen (alle 10 Messungen)
            if iteration % 10 == 0:
                print("-" * 70)
                print("  Statistik (letzte 10 Messungen):")
                print(f"  Front:  {distances['front']:.1f}cm | "
                      f"Links: {distances['left']:.1f}cm | "
                      f"Rechts: {distances['right']:.1f}cm")
                print("-" * 70)
                print()
            
            # Warte 0.5 Sekunden bis zur nächsten Messung
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("Test beendet")
        print("=" * 70)
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        try:
            sensors.cleanup()
            import RPi.GPIO as GPIO
            GPIO.cleanup()
        except:
            pass


if __name__ == "__main__":
    main()
