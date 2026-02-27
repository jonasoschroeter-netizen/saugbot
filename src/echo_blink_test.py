#!/usr/bin/env python3
"""
Echo-Blink-Test: Zeigt ob Echo-Signal ankommt
Wenn Echo HIGH erkannt wird -> "BLINK!" in Konsole
Läuft 30 Sekunden - halte Sensor vor Gegenstand (10-50cm)
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Sensor: 1=Rechts(20/21), 2=Links(16/26), 3=Front(5/4)
SENSOR = int(sys.argv[1]) if len(sys.argv) > 1 else 1
PINS = {1: (20, 21), 2: (16, 26), 3: (5, 4)}
TRIG, ECHO = PINS.get(SENSOR, (20, 21))

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.output(TRIG, GPIO.LOW)
time.sleep(0.1)

print("=" * 50)
print("  ECHO-BLINK-TEST (30 Sekunden)")
print("=" * 50)
print(f"Teste Sensor {SENSOR} (Trigger={TRIG}, Echo={ECHO})")
print("Halte Sensor vor einen Gegenstand (10-50cm)!")
print("Bei Echo-Signal erscheint: *** ECHO! ***")
print()

blink_count = 0
end_time = time.time() + 30

while time.time() < end_time:
    # Trigger senden
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)
    
    # Schnell auf Echo prüfen (5ms Fenster)
    for _ in range(100):
        if GPIO.input(ECHO) == 1:
            blink_count += 1
            print("*** ECHO! ***", end=" ", flush=True)
            break
        time.sleep(0.00005)
    
    time.sleep(0.06)  # 60ms zwischen Messungen (HC-SR04 Min)

GPIO.cleanup()

print()
print()
print("=" * 50)
print(f"Ergebnis: {blink_count} Echo-Signale in 30 Sekunden")
if blink_count > 0:
    print("-> Sensor funktioniert! Echo kommt an.")
else:
    print("-> Kein Echo. Prüfe: VCC 5V? Spannungsteiler? Kabel?")
print("=" * 50)
