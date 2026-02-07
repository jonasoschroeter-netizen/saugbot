"""
Unit tests for ultrasonic sensor module.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ultrasonic_sensor import UltrasonicSensor, UltrasonicSensorArray


class TestUltrasonicSensor(unittest.TestCase):
    """Test cases for UltrasonicSensor class."""
    
    @patch('ultrasonic_sensor.GPIO')
    def setUp(self, mock_gpio):
        """Set up test fixtures."""
        self.sensor = UltrasonicSensor(2, 3, "Test Sensor")
    
    def test_initialization(self):
        """Test sensor initialization."""
        self.assertEqual(self.sensor.trigger_pin, 2)
        self.assertEqual(self.sensor.echo_pin, 3)
        self.assertEqual(self.sensor.name, "Test Sensor")


if __name__ == '__main__':
    unittest.main()
