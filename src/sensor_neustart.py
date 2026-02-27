#!/usr/bin/env python3
"""
Schneller Neustart wenn Sensoren "auf einmal nicht mehr" gehen.
Stoppt alles, resetet GPIO, startet neu.
"""
import sys
import os
import time
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 1. Web-Interface stoppen
print("Stoppe Web-Interface...")
subprocess.run(["pkill", "-f", "web_interface"], capture_output=True)
time.sleep(2)

# 2. GPIO komplett zurücksetzen
print("GPIO zurücksetzen...")
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
time.sleep(1)

# 3. Sensoren testen
print("Teste Sensoren...")
from ultrasonic_sensor import UltrasonicSensorArray

sensors = UltrasonicSensorArray()
for i in range(5):
    d = sensors.get_all_distances()
    f = d['front'] or '---'
    l = d['left'] or '---'
    r = d['right'] or '---'
    print(f"  Front: {f}  Links: {l}  Rechts: {r}")
    time.sleep(1)
GPIO.cleanup()
print("Fertig.")
