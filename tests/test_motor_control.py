"""
Unit tests for motor control module.
Note: These tests require GPIO hardware, so they may need mocking for CI/CD.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from motor_control import MotorController


class TestMotorController(unittest.TestCase):
    """Test cases for MotorController class."""
    
    @patch('motor_control.GPIO')
    def setUp(self, mock_gpio):
        """Set up test fixtures."""
        self.motor = MotorController()
    
    def test_initialization(self):
        """Test motor controller initialization."""
        self.assertTrue(self.motor.is_initialized)
    
    def test_speed_clamping(self):
        """Test speed value clamping."""
        # Test speed above max
        clamped = self.motor._clamp_speed(150)
        self.assertEqual(clamped, 100)
        
        # Test speed below min
        clamped = self.motor._clamp_speed(10)
        self.assertEqual(clamped, 30)
        
        # Test valid speed
        clamped = self.motor._clamp_speed(50)
        self.assertEqual(clamped, 50)
    
    def test_stop(self):
        """Test motor stop functionality."""
        self.motor.stop()
        # Verify motors are set to 0 speed
        # (In real implementation, would check GPIO state)


if __name__ == '__main__':
    unittest.main()
