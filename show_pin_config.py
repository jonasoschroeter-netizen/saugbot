"""
Zeigt die aktuelle Pin-Konfiguration aus config.py an
"""

import sys
import os

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import (
        MOTOR_LEFT_ENABLE, MOTOR_LEFT_IN1, MOTOR_LEFT_IN2,
        MOTOR_RIGHT_ENABLE, MOTOR_RIGHT_IN1, MOTOR_RIGHT_IN2,
        ULTRASONIC_FRONT_TRIGGER, ULTRASONIC_FRONT_ECHO,
        ULTRASONIC_LEFT_TRIGGER, ULTRASONIC_LEFT_ECHO,
        ULTRASONIC_RIGHT_TRIGGER, ULTRASONIC_RIGHT_ECHO,
        SIDE_BRUSH_RELAY
    )
    
    print("=" * 70)
    print("  AKTUELLE PIN-KONFIGURATION (aus config.py)")
    print("=" * 70)
    print()
    
    print("MOTOREN (L298N):")
    print("-" * 70)
    print(f"  Motor Links:")
    print(f"    ENABLE (PWM): GPIO {MOTOR_LEFT_ENABLE}")
    print(f"    IN1:          GPIO {MOTOR_LEFT_IN1}")
    print(f"    IN2:          GPIO {MOTOR_LEFT_IN2}")
    print()
    print(f"  Motor Rechts:")
    print(f"    ENABLE (PWM): GPIO {MOTOR_RIGHT_ENABLE}")
    print(f"    IN1:          GPIO {MOTOR_RIGHT_IN1}")
    print(f"    IN2:          GPIO {MOTOR_RIGHT_IN2}")
    print()
    
    print("ULTRASCHALL-SENSOREN (HC-SR04):")
    print("-" * 70)
    print(f"  Front Sensor:")
    print(f"    Trigger: GPIO {ULTRASONIC_FRONT_TRIGGER}")
    print(f"    Echo:    GPIO {ULTRASONIC_FRONT_ECHO}")
    print()
    print(f"  Links Sensor:")
    print(f"    Trigger: GPIO {ULTRASONIC_LEFT_TRIGGER}")
    print(f"    Echo:    GPIO {ULTRASONIC_LEFT_ECHO}")
    print()
    print(f"  Rechts Sensor:")
    print(f"    Trigger: GPIO {ULTRASONIC_RIGHT_TRIGGER}")
    print(f"    Echo:    GPIO {ULTRASONIC_RIGHT_ECHO}")
    print()
    
    print("SEITENBÜRSTE:")
    print("-" * 70)
    print(f"  Relay: GPIO {SIDE_BRUSH_RELAY}")
    print()
    
    print("=" * 70)
    print("  WICHTIG: Prüfe ob diese Pins mit deiner Verkabelung übereinstimmen!")
    print("=" * 70)
    
except ImportError as e:
    print(f"Fehler beim Importieren von config.py: {e}")
    print("Bitte prüfe ob config.py existiert und korrekt ist.")
    sys.exit(1)
