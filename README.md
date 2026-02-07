# Saugbot - DIY Vacuum Robot

A DIY vacuum robot built on Raspberry Pi 4 with modular Python architecture.

## 🧪 Auto-Update Test
**Test-Update um 21:30 Uhr** - Wenn du das siehst, hat Auto-Update funktioniert! ✅

## Hardware Specifications

- **Brain**: Raspberry Pi 4 (4GB)
- **Drive**: 2x High-torque DC motors (L298N Driver)
- **Peripherals**: 
  - 1x N20 Side Brush (Relay controlled)
  - 3x HC-SR04 Ultrasonic Sensors
  - Level Shifter (3.3V <-> 5V) for sensor compatibility
- **Power**: 14V Battery -> Buck Converter (5.1V for Pi)
- **LiDAR**: RPLIDAR C1 (in transit)

## Project Structure

```
saugbot/
├── src/
│   ├── main.py              # Main control script
│   ├── motor_control.py     # L298N motor driver control
│   ├── ultrasonic_sensor.py # HC-SR04 sensor handling
│   └── side_brush.py        # Side brush relay control
├── tests/
│   ├── test_motor_control.py
│   └── test_ultrasonic_sensor.py
├── config.py                # GPIO pin assignments
├── .env                     # Environment variables (not in git)
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
├── setup_git.sh            # Git setup script for Raspberry Pi
└── README.md
```

## Setup Instructions

### 1. Clone Repository on Raspberry Pi

```bash
cd ~
git clone git@github.com:jonasoschroeter-netizen/saugbot.git
cd saugbot
```

### 2. Run Setup Script (Optional)

```bash
chmod +x setup_git.sh
./setup_git.sh
```

### 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your credentials (already configured for local use)
```

### 5. GPIO Pin Configuration

All GPIO pin assignments are in `config.py`. Review and adjust if needed:
- Motor pins (L298N driver)
- Ultrasonic sensor pins (HC-SR04)
- Side brush relay pin

### 6. Test Individual Components

```bash
# Test motors
python3 src/motor_control.py

# Test ultrasonic sensors
python3 src/ultrasonic_sensor.py

# Test side brush
python3 src/side_brush.py
```

### 7. Run Main Program

```bash
python3 src/main.py
```

## Remote Development Setup

### SSH Connection from Laptop

```bash
ssh pi@saugbot.local
# Password: 123456789
```

### Git Workflow

After making changes on the Pi:

```bash
git add .
git commit -m "Description of changes"
git push origin main
```

## GPIO Pin Reference

See `config.py` for complete pin assignments. Key pins:

- **Motors**: GPIO 18, 19 (PWM), GPIO 23-25, 8 (Direction)
- **Ultrasonic**: GPIO 2-4, 14-17 (Trigger/Echo pairs)
- **Side Brush**: GPIO 27 (Relay)

## Safety Features

- Collision detection via ultrasonic sensors
- Minimum distance thresholds
- Graceful shutdown on interrupt signals
- Speed limiting for motors

## Future Enhancements

- [ ] RPLIDAR C1 integration (when hardware arrives)
- [ ] SLAM (Simultaneous Localization and Mapping)
- [ ] Web interface for remote control
- [ ] Battery monitoring
- [ ] Cleaning pattern algorithms

## Development Notes

- All sensitive data (credentials) should be in `.env` (not committed)
- GPIO cleanup is handled automatically on exit
- Use `config.py` for all hardware configuration
- Follow modular Python structure for maintainability

## License

[Add your license here]

## Author

Jonas Oschroeter (jonasoschroeter-netizen)
