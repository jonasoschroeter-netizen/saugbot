#!/bin/bash
# Einzeltest für Sensor 1 - mit korrektem PYTHONPATH
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$HOME/saugbot/src:$PYTHONPATH

echo "=== 1. Roh-Debug (zeigt Echo-Pin Zustand) ==="
python3 src/sensor_debug_raw.py

echo ""
echo "=== 2. Sensor-Einzeltest (GPIO 20/21) ==="
python3 -c "
import sys
sys.path.insert(0, '/home/pi/saugbot/src')
from ultrasonic_sensor import UltrasonicSensor
import time
s = UltrasonicSensor(20, 21, 'Sensor1')
time.sleep(0.3)
for i in range(10):
    d = s.get_distance_cm()
    print('Messung', i+1, ':', d, 'cm')
    time.sleep(0.5)
"
