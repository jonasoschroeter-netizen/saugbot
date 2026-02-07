"""
Web Interface für Saugbot
Ermöglicht Testen und Einstellen der Ultraschall-Sensoren
"""

from flask import Flask, render_template, jsonify, request
import json
import os
import sys

# Add parent directory to path for config import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ultrasonic_sensor import UltrasonicSensorArray
    from config import COLLISION_DISTANCE_CM, MIN_DISTANCE_CM
    SENSORS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import sensors: {e}")
    SENSORS_AVAILABLE = False

app = Flask(__name__)

# Global sensor instance
sensors = None

def init_sensors():
    """Initialize sensors if available."""
    global sensors
    if SENSORS_AVAILABLE:
        try:
            sensors = UltrasonicSensorArray()
            return True
        except Exception as e:
            print(f"Error initializing sensors: {e}")
            return False
    return False

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/sensors/status')
def sensor_status():
    """Get sensor status."""
    if not SENSORS_AVAILABLE:
        return jsonify({
            'available': False,
            'error': 'Sensors not available (hardware not connected or import error)'
        })
    
    if sensors is None:
        initialized = init_sensors()
        if not initialized:
            return jsonify({
                'available': False,
                'error': 'Could not initialize sensors'
            })
    
    return jsonify({
        'available': True,
        'sensors': {
            'front': {'name': 'Front Sensor', 'enabled': True},
            'left': {'name': 'Left Sensor', 'enabled': True},
            'right': {'name': 'Right Sensor', 'enabled': True}
        }
    })

@app.route('/api/sensors/read')
def read_sensors():
    """Read all sensor values."""
    if not SENSORS_AVAILABLE or sensors is None:
        return jsonify({
            'success': False,
            'error': 'Sensors not available'
        })
    
    try:
        distances = sensors.get_all_distances()
        return jsonify({
            'success': True,
            'distances': {
                'front': distances['front'],
                'left': distances['left'],
                'right': distances['right']
            },
            'unit': 'cm'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/config/get')
def get_config():
    """Get current configuration values."""
    try:
        from config import COLLISION_DISTANCE_CM, MIN_DISTANCE_CM
        return jsonify({
            'success': True,
            'config': {
                'collision_distance_cm': COLLISION_DISTANCE_CM,
                'min_distance_cm': MIN_DISTANCE_CM
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/config/update', methods=['POST'])
def update_config():
    """Update configuration values."""
    try:
        data = request.json
        collision_distance = data.get('collision_distance_cm')
        min_distance = data.get('min_distance_cm')
        
        # Read current config.py
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.py')
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Update values
        import re
        if collision_distance is not None:
            content = re.sub(
                r'COLLISION_DISTANCE_CM\s*=\s*\d+',
                f'COLLISION_DISTANCE_CM = {collision_distance}',
                content
            )
        if min_distance is not None:
            content = re.sub(
                r'MIN_DISTANCE_CM\s*=\s*\d+',
                f'MIN_DISTANCE_CM = {min_distance}',
                content
            )
        
        # Write back
        with open(config_path, 'w') as f:
            f.write(content)
        
        return jsonify({
            'success': True,
            'message': 'Configuration updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("Starting Saugbot Web Interface...")
    print("Open http://raspberrypi.local:5000 or http://192.168.0.5:5000 in your browser")
    app.run(host='0.0.0.0', port=5000, debug=True)
