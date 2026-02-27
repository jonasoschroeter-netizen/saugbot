"""
Schneller Sensor-Test - läuft 5 Messungen und beendet sich automatisch
"""
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ultrasonic_sensor import UltrasonicSensorArray
    from config import COLLISION_DISTANCE_CM
except ImportError as e:
    print(f"Fehler: {e}")
    sys.exit(1)


def format_distance(d):
    if d is None:
        return "---"
    if d < COLLISION_DISTANCE_CM:
        return f"{d:.1f}cm (GEFAHR)"
    return f"{d:.1f}cm"


def main():
    print("Sensoren testen...")
    sensors = UltrasonicSensorArray()
    time.sleep(0.3)
    
    for i in range(5):
        distances = sensors.get_all_distances()
        print(f"  Front: {format_distance(distances['front'])} | "
              f"Links: {format_distance(distances['left'])} | "
              f"Rechts: {format_distance(distances['right'])}")
        time.sleep(0.5)
    
    try:
        sensors.cleanup()
        import RPi.GPIO as GPIO
        GPIO.cleanup()
    except:
        pass
    print("Fertig!")


if __name__ == "__main__":
    main()
