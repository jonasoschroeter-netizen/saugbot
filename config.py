"""
Saugbot Configuration File
Contains all GPIO pin assignments and hardware configuration.
"""

# GPIO Pin Assignments for L298N Motor Driver
MOTOR_LEFT_ENABLE = 18      # PWM pin for left motor speed
MOTOR_LEFT_IN1 = 23         # Left motor direction pin 1
MOTOR_LEFT_IN2 = 24         # Left motor direction pin 2
MOTOR_RIGHT_ENABLE = 19     # PWM pin for right motor speed
MOTOR_RIGHT_IN1 = 25        # Right motor direction pin 1
MOTOR_RIGHT_IN2 = 8         # Right motor direction pin 2

# GPIO Pin Assignments for HC-SR04 Ultrasonic Sensors
# Sensor 1 (Rechts): Trigger=GPIO 20, Echo=GPIO 21
# Sensor 2 (Links): Trigger=GPIO 19 (MISO), Echo=GPIO 16 (Chip Enable-C2)
# Sensor 3 (Front): Trigger=GPIO 13 (PWM), Echo=GPIO 6
ULTRASONIC_FRONT_TRIGGER = 13   # GPIO 13 (PWM) - Sensor 3 Trigger
ULTRASONIC_FRONT_ECHO = 6       # GPIO 6 - Sensor 3 Echo
ULTRASONIC_LEFT_TRIGGER = 19    # GPIO 19 (MISO) - Sensor 2 Trigger
ULTRASONIC_LEFT_ECHO = 16       # GPIO 16 (Chip Enable-C2) - Sensor 2 Echo
ULTRASONIC_RIGHT_TRIGGER = 20  # GPIO 20 - Sensor 1 Trigger
ULTRASONIC_RIGHT_ECHO = 21     # GPIO 21 - Sensor 1 Echo

# GPIO Pin Assignment for N20 Side Brush Relay
SIDE_BRUSH_RELAY = 27

# Motor Configuration
MOTOR_PWM_FREQUENCY = 1000   # PWM frequency in Hz
MOTOR_MAX_SPEED = 100        # Maximum speed percentage (0-100)
MOTOR_MIN_SPEED = 30         # Minimum speed percentage (0-100)

# Ultrasonic Sensor Configuration
ULTRASONIC_TIMEOUT = 0.03    # Timeout in seconds (30ms for ~5m max range)
SOUND_SPEED = 343            # Speed of sound in m/s at 20°C

# Safety Thresholds
WARNING_DISTANCE_CM = 4      # Distance for warning (orange) in cm
COLLISION_DISTANCE_CM = 2    # Distance for collision danger (red) in cm - triggers avoidance

# Level Shifter Configuration
# Note: Level shifter is used for 3.3V <-> 5V conversion
# GPIO pins output 3.3V, sensors need 5V input
# Echo pins return 5V, need level shifting to 3.3V for Pi

# RPLIDAR C1 Configuration (for future implementation)
LIDAR_ENABLED = False        # Set to True when hardware is available

# System Configuration
HOSTNAME = "saugbot.local"
LOG_LEVEL = "INFO"           # DEBUG, INFO, WARNING, ERROR
