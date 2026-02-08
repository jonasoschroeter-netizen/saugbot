"""
Saugbot Main Control Script
Coordinates motor control, sensors, and navigation logic.
"""

import time
import signal
import sys
import importlib
from motor_control import MotorController
from ultrasonic_sensor import UltrasonicSensorArray
from side_brush import SideBrush
from config import COLLISION_DISTANCE_CM, MIN_DISTANCE_CM


class Saugbot:
    """Main robot control class."""
    
    def __init__(self):
        """Initialize all robot components."""
        print("Initializing Saugbot...")
        
        self.motor = MotorController()
        self.sensors = UltrasonicSensorArray()
        self.brush = SideBrush()
        
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        print("Saugbot initialized successfully!")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print("\nShutdown signal received...")
        self.stop()
        sys.exit(0)
    
    def start(self):
        """Start the robot."""
        self.running = True
        self.brush.start()
        print("Saugbot started!")
    
    def stop(self):
        """Stop the robot."""
        self.running = False
        self.motor.stop()
        self.brush.stop()
        print("Saugbot stopped")
    
    def check_collision(self):
        """Check if collision is imminent.
        
        Returns:
            Tuple (has_collision, direction) where direction is 'front', 'left', 'right', or None
        """
        # Reload config to get latest threshold values
        import config
        importlib.reload(config)
        from config import COLLISION_DISTANCE_CM, MIN_DISTANCE_CM
        
        distances = self.sensors.get_all_distances()
        
        # Check front collision
        if distances['front'] is not None and distances['front'] < COLLISION_DISTANCE_CM:
            return True, 'front'
        
        # Check left sensor (Links Vorne) - wichtigster Sensor
        if distances['left'] is not None and distances['left'] < COLLISION_DISTANCE_CM:
            return True, 'left'
        
        # Check right sensor (use collision distance for consistency)
        if distances['right'] is not None and distances['right'] < COLLISION_DISTANCE_CM:
            return True, 'right'
        
        return False, None
    
    def avoid_collision(self, direction):
        """Perform collision avoidance maneuver.
        
        Args:
            direction: Direction of obstacle ('front', 'left', 'right')
        """
        # Reload config to get latest threshold values
        import config
        importlib.reload(config)
        from config import COLLISION_DISTANCE_CM, MIN_DISTANCE_CM
        
        print(f"Collision detected from {direction}, avoiding...")
        
        # Stop immediately
        self.motor.stop()
        time.sleep(0.2)
        
        # Move backward slightly
        self.motor.move_backward(40)
        time.sleep(0.5)
        self.motor.stop()
        time.sleep(0.2)
        
        # Turn away from obstacle
        if direction == 'front':
            # Check which side has more space
            distances = self.sensors.get_all_distances()
            left_dist = distances['left'] if distances['left'] else 0
            right_dist = distances['right'] if distances['right'] else 0
            
            if left_dist > right_dist:
                self.motor.turn_left(50)
            else:
                self.motor.turn_right(50)
        elif direction == 'left':
            # Links vorne Sensor: Nach rechts fahren bis Gegenstand weg ist
            print("Links vorne Hindernis - fahre nach rechts...")
            max_attempts = 50  # Max 5 Sekunden (50 * 0.1s)
            attempts = 0
            while attempts < max_attempts:
                self.motor.turn_right(50)
                time.sleep(0.1)
                distances = self.sensors.get_all_distances()
                left_dist = distances['left'] if distances['left'] else 999
                if left_dist > COLLISION_DISTANCE_CM:
                    print(f"Gegenstand weg (Distanz: {left_dist}cm), fahre weiter...")
                    break
                attempts += 1
            self.motor.stop()
            return  # Früh zurückkehren, da wir bereits ausgewichen sind
        elif direction == 'right':
            self.motor.turn_left(50)
        
        time.sleep(0.8)
        self.motor.stop()
    
    def run(self):
        """Main control loop."""
        self.start()
        
        try:
            while self.running:
                # Check for collisions
                has_collision, direction = self.check_collision()
                
                if has_collision:
                    self.avoid_collision(direction)
                else:
                    # Normal forward movement
                    self.motor.move_forward(50)
                
                # Small delay to prevent excessive CPU usage
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up all resources."""
        self.stop()
        # Cleanup in richtiger Reihenfolge: zuerst brush, dann motor (GPIO.cleanup)
        self.brush.cleanup()
        self.motor.cleanup()
        self.sensors.cleanup()
        print("Saugbot cleanup complete")


if __name__ == "__main__":
    robot = Saugbot()
    robot.run()
