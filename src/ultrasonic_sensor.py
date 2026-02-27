"""
Ultrasonic Sensor Module for Saugbot
Handles HC-SR04 distance measurement with level shifter support.
"""

import RPi.GPIO as GPIO
import time
from config import (
    ULTRASONIC_FRONT_TRIGGER, ULTRASONIC_FRONT_ECHO,
    ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO,
    ULTRASONIC_RIGHT_TRIGGER, ULTRASONIC_RIGHT_ECHO,
    ULTRASONIC_TIMEOUT, SOUND_SPEED
)


class UltrasonicSensor:
    """Controls a single HC-SR04 ultrasonic sensor."""
    
    def __init__(self, trigger_pin, echo_pin, name="Sensor"):
        """Initialize ultrasonic sensor.
        
        Args:
            trigger_pin: GPIO pin for trigger signal
            echo_pin: GPIO pin for echo signal (via level shifter)
            name: Descriptive name for this sensor
        """
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.name = name
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup pins
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)
        
        # Initialize trigger to LOW
        GPIO.output(self.trigger_pin, GPIO.LOW)
        time.sleep(0.1)  # Allow sensor to settle
        
        print(f"{self.name} initialized (Trigger: {trigger_pin}, Echo: {echo_pin})")
    
    def get_distance_cm(self):
        """Measure distance in centimeters.
        
        Returns:
            Distance in cm, or None if measurement failed/timeout
        """
        try:
            # Send trigger pulse (10us minimum)
            GPIO.output(self.trigger_pin, GPIO.LOW)
            time.sleep(0.00002)  # Ensure LOW state (20us)
            GPIO.output(self.trigger_pin, GPIO.HIGH)
            time.sleep(0.00001)  # 10 microseconds
            GPIO.output(self.trigger_pin, GPIO.LOW)
            
            # Echo-Puls ist nur ~0.3-0.5ms - schnelles Polling (ohne sleep = schnell)
            timeout = time.time() + ULTRASONIC_TIMEOUT
            echo_start = None
            echo_end = None
            
            # Warte auf Echo HIGH
            while GPIO.input(self.echo_pin) == GPIO.LOW:
                if time.time() > timeout:
                    return None
            echo_start = time.time()
            
            # Warte auf Echo LOW, messe Dauer
            while GPIO.input(self.echo_pin) == GPIO.HIGH:
                if time.time() > timeout:
                    return None
                echo_end = time.time()
            
            if echo_start is None or echo_end is None:
                return None
            
            # Calculate distance
            pulse_duration = echo_end - echo_start
            distance_cm = (pulse_duration * SOUND_SPEED * 100) / 2
            
            # HC-SR04 range is 2-400cm, filter invalid readings
            if distance_cm < 2 or distance_cm > 400:
                return None
            
            return round(distance_cm, 1)
            
        except Exception as e:
            print(f"{self.name}: Error reading distance: {e}")
            return None
    
    def get_distance_m(self):
        """Measure distance in meters.
        
        Returns:
            Distance in meters, or None if measurement failed
        """
        distance_cm = self.get_distance_cm()
        if distance_cm is None:
            return None
        return distance_cm / 100.0


class UltrasonicSensorArray:
    """Manages all three ultrasonic sensors."""
    
    def __init__(self):
        """Initialize all three sensors."""
        self.front = UltrasonicSensor(
            ULTRASONIC_FRONT_TRIGGER,
            ULTRASONIC_FRONT_ECHO,
            "Front Sensor"
        )
        self.left = UltrasonicSensor(
            ULTRASONIC_LEFT_TRIGGER,
            ULTRASONIC_LEFT_ECHO,
            "Left Sensor"
        )
        self.right = UltrasonicSensor(
            ULTRASONIC_RIGHT_TRIGGER,
            ULTRASONIC_RIGHT_ECHO,
            "Right Sensor"
        )
    
    def get_all_distances(self):
        """Get distances from all sensors.
        
        Returns:
            Dictionary with 'front', 'left', 'right' distances in cm
        """
        # 70ms Pause zwischen Sensoren (HC-SR04 braucht min. 60ms)
        front = self.front.get_distance_cm()
        time.sleep(0.07)
        left = self.left.get_distance_cm()
        time.sleep(0.07)
        right = self.right.get_distance_cm()
        return {'front': front, 'left': left, 'right': right}
    
    def cleanup(self):
        """Clean up GPIO resources."""
        # GPIO cleanup is handled automatically, but we can add logging
        print("UltrasonicSensorArray cleaned up")


if __name__ == "__main__":
    # Test ultrasonic sensors
    sensors = UltrasonicSensorArray()
    
    try:
        print("Testing ultrasonic sensors...")
        for i in range(10):
            distances = sensors.get_all_distances()
            f = distances['front'] if distances['front'] is not None else '---'
            l = distances['left'] if distances['left'] is not None else '---'
            r = distances['right'] if distances['right'] is not None else '---'
            print(f"Front: {f} | Left: {l} | Right: {r}")
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        sensors.cleanup()
        GPIO.cleanup()
