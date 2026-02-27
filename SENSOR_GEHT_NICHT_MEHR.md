# Sensoren gehen "auf einmal nicht mehr"

## Schnell-Fix

```bash
cd ~/saugbot
git pull
python3 src/sensor_neustart.py
```

Stoppt Web-Interface, setzt GPIO zurück, testet Sensoren.

---

## Wenn das nicht hilft

**1. Pi neu starten**
```bash
sudo reboot
```
Nach dem Neustart: `systemctl --user start saugbot-web`

**2. Verkabelung prüfen**
- Stecker fest?
- 5V + GND an allen Sensoren?
- Spannungsteiler (1k/2k) an jedem Echo?

**3. Pin-Belegung (aktuell)**
| Sensor | Trigger | Echo |
|--------|---------|------|
| Rechts | Pin 38 (GPIO 20) | Pin 40 (GPIO 21) |
| Links | Pin 36 (GPIO 16) | Pin 37 (GPIO 26) |
| Mitte | Pin 29 (GPIO 5) | Pin 31 (GPIO 6) |

**4. Mit sudo testen** (falls Rechte-Problem)
```bash
sudo python3 src/test_all_sensors.py
```
