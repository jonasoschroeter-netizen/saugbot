"""
Side Brush Control Module for Saugbot
Controls N20 side brush via relay.
"""

import RPi.GPIO as GPIO
import time
from config import SIDE_BRUSH_RELAY


class SideBrush:
    """Controls the side brush motor via relay."""
    
    def __init__(self):
        """Initialize relay pin for side brush."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(SIDE_BRUSH_RELAY, GPIO.OUT)
        GPIO.output(SIDE_BRUSH_RELAY, GPIO.LOW)  # Relay OFF initially
        
        self.is_running = False
        print("SideBrush initialized")
    
    def start(self):
        """Start the side brush."""
        GPIO.output(SIDE_BRUSH_RELAY, GPIO.HIGH)
        self.is_running = True
        print("Side brush started")
    
    def stop(self):
        """Stop the side brush."""
        GPIO.output(SIDE_BRUSH_RELAY, GPIO.LOW)
        self.is_running = False
        print("Side brush stopped")
    
    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop()
        print("SideBrush cleaned up")


if __name__ == "__main__":
    # Test side brush
    brush = SideBrush()
    
    try:
        print("Starting side brush...")
        brush.start()
        time.sleep(5)
        
        print("Stopping side brush...")
        brush.stop()
    
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        brush.cleanup()
        GPIO.cleanup()
