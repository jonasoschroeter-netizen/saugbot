#!/usr/bin/env python3
"""
Low-Level Debug: Zeigt was die Echo-Pins wirklich machen
Hilft herauszufinden ob: Stromversorgung, Echo-Signal, oder Pins falsch
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Teste Sensor 1 (der vorher funktionierte)
TRIG, ECHO = 20, 21

print("=" * 60)
print("  SENSOR DEBUG - Rohdaten von GPIO")
print("=" * 60)
print(f"Trigger: GPIO {TRIG} (Pin 38)")
print(f"Echo:    GPIO {ECHO} (Pin 40)")
print()
print("Prüfe 10x: Sende Trigger, lese Echo-Pin Zustand")
print()

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(TRIG, GPIO.LOW)
time.sleep(0.1)

for i in range(10):
    # Echo vor Trigger
    echo_before = GPIO.input(ECHO)
    
    # Trigger senden
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)
    
    # Echo-Pin 50x lesen (über ~5ms)
    highs = 0
    for _ in range(50):
        if GPIO.input(ECHO) == 1:
            highs += 1
        time.sleep(0.0001)
    
    echo_after = GPIO.input(ECHO)
    
    status = "OK" if highs > 0 else "---"
    print(f"  {i+1:2}. Echo vorher={echo_before}  Hoch-Impulse={highs:2}  nachher={echo_after}  {status}")
    time.sleep(0.2)

GPIO.cleanup()

print()
print("=" * 60)
print("AUSWERTUNG:")
print("  - Hoch-Impulse > 0  = Sensor antwortet, Echo funktioniert")
print("  - Hoch-Impulse = 0  = Kein Echo-Signal")
print("    -> Prüfe: 5V+GND an Sensor? Spannungsteiler an Echo?")
print("  - Echo vorher = 1   = Pin könnte dauerhaft HIGH sein (Problem)")
print("=" * 60)
