"""
Motor Control Module for Saugbot
Controls BTS7960 or similar motor drivers using RPWM/LPWM.
"""

import RPi.GPIO as GPIO
import time
from config import (
    MOTOR_LEFT_RPWM, MOTOR_LEFT_LPWM,
    MOTOR_RIGHT_RPWM, MOTOR_RIGHT_LPWM,
    MOTOR_PWM_FREQUENCY, MOTOR_MAX_SPEED, MOTOR_MIN_SPEED
)


class MotorController:
    """Controls both left and right motors via RPWM/LPWM motor drivers."""
    
    def __init__(self):
        """Initialize GPIO pins and PWM for motors."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup left motor pins (RPWM/LPWM)
        GPIO.setup(MOTOR_LEFT_RPWM, GPIO.OUT)
        GPIO.setup(MOTOR_LEFT_LPWM, GPIO.OUT)
        
        # Setup right motor pins (RPWM/LPWM)
        GPIO.setup(MOTOR_RIGHT_RPWM, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_LPWM, GPIO.OUT)
        
        # Initialize PWM for speed control
        self.left_rpwm = GPIO.PWM(MOTOR_LEFT_RPWM, MOTOR_PWM_FREQUENCY)
        self.left_lpwm = GPIO.PWM(MOTOR_LEFT_LPWM, MOTOR_PWM_FREQUENCY)
        self.right_rpwm = GPIO.PWM(MOTOR_RIGHT_RPWM, MOTOR_PWM_FREQUENCY)
        self.right_lpwm = GPIO.PWM(MOTOR_RIGHT_LPWM, MOTOR_PWM_FREQUENCY)
        
        # Start PWM with 0% duty cycle (stopped)
        self.left_rpwm.start(0)
        self.left_lpwm.start(0)
        self.right_rpwm.start(0)
        self.right_lpwm.start(0)
        
        self.is_initialized = True
        print("MotorController initialized (RPWM/LPWM)")
    
    def _clamp_speed(self, speed):
        """Clamp speed value between MIN and MAX."""
        return max(MOTOR_MIN_SPEED, min(MOTOR_MAX_SPEED, abs(speed)))
    
    def _set_left_motor(self, speed):
        """Set left motor speed and direction.
        
        Args:
            speed: Speed percentage (-100 to 100, negative = reverse)
        """
        clamped_speed = self._clamp_speed(speed)
        
        if speed > 0:
            # Forward: RPWM active, LPWM = 0
            self.left_rpwm.ChangeDutyCycle(clamped_speed)
            self.left_lpwm.ChangeDutyCycle(0)
        elif speed < 0:
            # Reverse: LPWM active, RPWM = 0
            self.left_rpwm.ChangeDutyCycle(0)
            self.left_lpwm.ChangeDutyCycle(clamped_speed)
        else:
            # Stop: both = 0
            self.left_rpwm.ChangeDutyCycle(0)
            self.left_lpwm.ChangeDutyCycle(0)
    
    def _set_right_motor(self, speed):
        """Set right motor speed and direction.
        
        Args:
            speed: Speed percentage (-100 to 100, negative = reverse)
        """
        clamped_speed = self._clamp_speed(speed)
        
        if speed > 0:
            # Forward: RPWM active, LPWM = 0
            self.right_rpwm.ChangeDutyCycle(clamped_speed)
            self.right_lpwm.ChangeDutyCycle(0)
        elif speed < 0:
            # Reverse: LPWM active, RPWM = 0
            self.right_rpwm.ChangeDutyCycle(0)
            self.right_lpwm.ChangeDutyCycle(clamped_speed)
        else:
            # Stop: both = 0
            self.right_rpwm.ChangeDutyCycle(0)
            self.right_lpwm.ChangeDutyCycle(0)
    
    def move_forward(self, speed=50):
        """Move robot forward.
        
        Args:
            speed: Speed percentage (0-100)
        """
        self._set_left_motor(speed)
        self._set_right_motor(speed)
    
    def move_backward(self, speed=50):
        """Move robot backward.
        
        Args:
            speed: Speed percentage (0-100)
        """
        self._set_left_motor(-speed)
        self._set_right_motor(-speed)
    
    def turn_left(self, speed=50):
        """Turn left (left motor reverse, right motor forward).
        
        Args:
            speed: Speed percentage (0-100)
        """
        self._set_left_motor(-speed)
        self._set_right_motor(speed)
    
    def turn_right(self, speed=50):
        """Turn right (left motor forward, right motor reverse).
        
        Args:
            speed: Speed percentage (0-100)
        """
        self._set_left_motor(speed)
        self._set_right_motor(-speed)
    
    def stop(self):
        """Stop both motors."""
        self._set_left_motor(0)
        self._set_right_motor(0)
    
    def cleanup(self):
        """Clean up GPIO resources."""
        self.stop()
        self.left_rpwm.stop()
        self.left_lpwm.stop()
        self.right_rpwm.stop()
        self.right_lpwm.stop()
        GPIO.cleanup()
        self.is_initialized = False
        print("MotorController cleaned up")


if __name__ == "__main__":
    # Test motor control
    motor = MotorController()
    
    try:
        print("Testing forward movement...")
        motor.move_forward(50)
        time.sleep(2)
        
        print("Testing backward movement...")
        motor.move_backward(50)
        time.sleep(2)
        
        print("Testing left turn...")
        motor.turn_left(50)
        time.sleep(2)
        
        print("Testing right turn...")
        motor.turn_right(50)
        time.sleep(2)
        
        print("Stopping...")
        motor.stop()
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        motor.cleanup()
