"""
Sensor Test Programm
Zeigt Live-Distanz eines einzelnen Sensors an
"""

import time
import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ultrasonic_sensor import UltrasonicSensor
    from config import ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO, COLLISION_DISTANCE_CM
    SENSOR_AVAILABLE = True
except ImportError as e:
    print(f"Error: Could not import sensor: {e}")
    SENSOR_AVAILABLE = False
    sys.exit(1)

def main():
    """Test einzelner Sensor mit Schwellenwert."""
    print("=" * 50)
    print("Ultraschall-Sensor Test (Links Vorne)")
    print("=" * 50)
    print(f"Schwellenwert: {COLLISION_DISTANCE_CM} cm")
    print("Drücke Ctrl+C zum Beenden\n")
    
    sensor = UltrasonicSensor(
        ULTRASONIC_LEFT_TRIGGER,
        ULTRASONIC_LEFT_ECHO,
        "Links Vorne"
    )
    
    try:
        while True:
            distance = sensor.get_distance_cm()
            
            if distance is None:
                print("❌ Keine Messung möglich")
            else:
                # Farbige Ausgabe je nach Distanz
                if distance < COLLISION_DISTANCE_CM:
                    status = "🔴 HINDERNIS!"
                    color_code = "\033[91m"  # Rot
                elif distance < COLLISION_DISTANCE_CM + 5:
                    status = "🟡 WARNUNG"
                    color_code = "\033[93m"  # Gelb
                else:
                    status = "🟢 OK"
                    color_code = "\033[92m"  # Grün
                
                reset_code = "\033[0m"
                print(f"{color_code}{status} | Distanz: {distance:6.1f} cm | Schwellenwert: {COLLISION_DISTANCE_CM} cm{reset_code}")
            
            time.sleep(0.5)  # Alle 0.5 Sekunden messen
    
    except KeyboardInterrupt:
        print("\n\nTest beendet")
    finally:
        sensor.cleanup() if hasattr(sensor, 'cleanup') else None

if __name__ == "__main__":
    main()
