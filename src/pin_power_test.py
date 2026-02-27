#!/usr/bin/env python3
"""
PIN POWER TEST - Setzt alle Trigger-Pins auf HIGH (3.3V)
Damit kannst du mit dem Multimeter prüfen ob Strom an den Sensoren ankommt.

Verkabelung prüfen:
- Multimeter auf DC-Voltage (20V)
- Schwarzes Kabel: GND (Pin 39)
- Rotes Kabel: An TRIGGER-Pin des Sensors (oder am Pi-Pin)
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Alle Trigger-Pins (die der Pi AUSSENDET - 3.3V)
TRIGGER_PINS = [
    (20, "Sensor 1 (Rechts) - Pin 38"),
    (16, "Sensor 2 (Links) - Pin 36"),
    (5, "Sensor 3 (Front) - Pin 29"),
]

# Alle Echo-Pins (Eingang vom Sensor - Pi liest nur, sendet nicht)
ECHO_PINS = [
    (21, "Sensor 1 (Rechts) - Pin 40"),
    (26, "Sensor 2 (Links) - Pin 37"),
    (6, "Sensor 3 (Front) - Pin 31"),
]

print("=" * 60)
print("  PIN POWER TEST - Prüfe ob 3.3V an den Pins ankommt")
print("=" * 60)
print()
print("Alle TRIGGER-Pins werden jetzt auf HIGH (3.3V) gesetzt.")
print("Prüfe mit Multimeter: Schwarzes Kabel = GND (Pin 39)")
print()
print("Erwartete Spannung an jedem TRIGGER-Pin: ~3.3V")
print()

for gpio, name in TRIGGER_PINS:
    GPIO.setup(gpio, GPIO.OUT)
    GPIO.output(gpio, GPIO.HIGH)
    print(f"  GPIO {gpio:2} ({name}): HIGH = 3.3V")

print()
print("=" * 60)
print("Multimeter prüfen:")
print("  - GND (schwarz): Pin 39")
print("  - Messen (rot):  Pin 38, 36, 29 nacheinander")
print("  - Erwartung:     ~3.3V an jedem")
print()
print("Drücke Ctrl+C zum Beenden")
print("=" * 60)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nBeende...")
finally:
    for gpio, _ in TRIGGER_PINS:
        GPIO.output(gpio, GPIO.LOW)
    GPIO.cleanup()
    print("Alle Pins auf LOW. Fertig.")
