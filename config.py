"""
Saugbot Configuration File
Contains all GPIO pin assignments and hardware configuration.
"""

# GPIO Pin Assignments for Motor Controllers (RPWM/LPWM - BTS7960 oder ähnlich)
# Linker Motorcontroller
MOTOR_LEFT_RPWM = 12        # GPIO 12 (Pin 32) - Rechts PWM für linken Motor
MOTOR_LEFT_LPWM = 13        # GPIO 13 (Pin 33) - Links PWM für linken Motor
# Rechter Motorcontroller
MOTOR_RIGHT_RPWM = 18       # GPIO 18 (Pin 12) - Rechts PWM für rechten Motor
MOTOR_RIGHT_LPWM = 10       # GPIO 10 (Pin 19) - Links PWM für rechten Motor

# GPIO Pin Assignments for HC-SR04 Ultrasonic Sensors
# Sensor 1: Trigger=GPIO 20 (Pin 38), Echo=GPIO 21 (Pin 40)
# Sensor 2: Trigger=GPIO 16 (Pin 36), Echo=GPIO 26 (Pin 37)
# Sensor 3 (Mitte/Front): Trigger=GPIO 5 (Pin 29), Echo=GPIO 3 (Pin 27)
ULTRASONIC_SENSOR1_TRIGGER = 20  # GPIO 20 (Pin 38) - Sensor 1 Trigger
ULTRASONIC_SENSOR1_ECHO = 21     # GPIO 21 (Pin 40) - Sensor 1 Echo (über Spannungsteiler)
ULTRASONIC_SENSOR2_TRIGGER = 16  # GPIO 16 (Pin 36) - Sensor 2 Trigger
ULTRASONIC_SENSOR2_ECHO = 26     # GPIO 26 (Pin 37) - Sensor 2 Echo (über Spannungsteiler)
ULTRASONIC_SENSOR3_TRIGGER = 5   # GPIO 5 (Pin 29) - Sensor 3 Trigger
ULTRASONIC_SENSOR3_ECHO = 3      # GPIO 3 (Pin 27) - Sensor 3 Echo (über Spannungsteiler)

# Legacy Aliases für Kompatibilität (werden auf Sensor 1, 2, 3 gemappt)
ULTRASONIC_RIGHT_TRIGGER = ULTRASONIC_SENSOR1_TRIGGER
ULTRASONIC_RIGHT_ECHO = ULTRASONIC_SENSOR1_ECHO
ULTRASONIC_LEFT_TRIGGER = ULTRASONIC_SENSOR2_TRIGGER
ULTRASONIC_LEFT_ECHO = ULTRASONIC_SENSOR2_ECHO
ULTRASONIC_FRONT_TRIGGER = ULTRASONIC_SENSOR3_TRIGGER
ULTRASONIC_FRONT_ECHO = ULTRASONIC_SENSOR3_ECHO

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
MIN_DISTANCE_CM = WARNING_DISTANCE_CM  # Alias für Kompatibilität

# Level Shifter Configuration
# Note: Level shifter is used for 3.3V <-> 5V conversion
# GPIO pins output 3.3V, sensors need 5V input
# Echo pins return 5V, need level shifting to 3.3V for Pi

# RPLIDAR C1 Configuration (for future implementation)
LIDAR_ENABLED = False        # Set to True when hardware is available

# System Configuration
HOSTNAME = "saugbot.local"
LOG_LEVEL = "INFO"           # DEBUG, INFO, WARNING, ERROR
