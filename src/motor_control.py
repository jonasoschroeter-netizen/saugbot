"""
Motor Control Module for Saugbot
Controls L298N driver for 2x high-torque DC motors using PWM.
"""

import RPi.GPIO as GPIO
import time
from config import (
    MOTOR_LEFT_ENABLE, MOTOR_LEFT_IN1, MOTOR_LEFT_IN2,
    MOTOR_RIGHT_ENABLE, MOTOR_RIGHT_IN1, MOTOR_RIGHT_IN2,
    MOTOR_PWM_FREQUENCY, MOTOR_MAX_SPEED, MOTOR_MIN_SPEED
)


class MotorController:
    """Controls both left and right motors via L298N driver."""
    
    def __init__(self):
        """Initialize GPIO pins and PWM for motors."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        # Setup left motor pins
        GPIO.setup(MOTOR_LEFT_ENABLE, GPIO.OUT)
        GPIO.setup(MOTOR_LEFT_IN1, GPIO.OUT)
        GPIO.setup(MOTOR_LEFT_IN2, GPIO.OUT)
        
        # Setup right motor pins
        GPIO.setup(MOTOR_RIGHT_ENABLE, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_IN1, GPIO.OUT)
        GPIO.setup(MOTOR_RIGHT_IN2, GPIO.OUT)
        
        # Initialize PWM for speed control
        self.left_pwm = GPIO.PWM(MOTOR_LEFT_ENABLE, MOTOR_PWM_FREQUENCY)
        self.right_pwm = GPIO.PWM(MOTOR_RIGHT_ENABLE, MOTOR_PWM_FREQUENCY)
        
        # Start PWM with 0% duty cycle (stopped)
        self.left_pwm.start(0)
        self.right_pwm.start(0)
        
        self.is_initialized = True
        print("MotorController initialized")
    
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
            # Forward
            GPIO.output(MOTOR_LEFT_IN1, GPIO.HIGH)
            GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
        elif speed < 0:
            # Reverse
            GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_IN2, GPIO.HIGH)
        else:
            # Stop
            GPIO.output(MOTOR_LEFT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_LEFT_IN2, GPIO.LOW)
        
        self.left_pwm.ChangeDutyCycle(clamped_speed)
    
    def _set_right_motor(self, speed):
        """Set right motor speed and direction.
        
        Args:
            speed: Speed percentage (-100 to 100, negative = reverse)
        """
        clamped_speed = self._clamp_speed(speed)
        
        if speed > 0:
            # Forward
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.HIGH)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
        elif speed < 0:
            # Reverse
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.HIGH)
        else:
            # Stop
            GPIO.output(MOTOR_RIGHT_IN1, GPIO.LOW)
            GPIO.output(MOTOR_RIGHT_IN2, GPIO.LOW)
        
        self.right_pwm.ChangeDutyCycle(clamped_speed)
    
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
        self.left_pwm.stop()
        self.right_pwm.stop()
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
