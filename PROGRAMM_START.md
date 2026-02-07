# Programm starten

## Status:
- ✅ Repository geklont
- ✅ Dependencies installiert
- ✅ PYTHONPATH gesetzt
- ✅ .env Datei erstellt

## Programm starten:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/main.py
```

## Mögliche Fehler:

### 1. GPIO-Fehler (normal ohne Hardware)

Falls du Fehler wie "No module named 'RPi'" oder GPIO-Fehler siehst:
- **Das ist normal**, wenn die Hardware nicht angeschlossen ist
- Du kannst trotzdem die Logik testen

### 2. Einzelne Komponenten testen:

```bash
# Motor Control testen
python3 src/motor_control.py

# Ultraschall-Sensoren testen
python3 src/ultrasonic_sensor.py

# Side Brush testen
python3 src/side_brush.py
```

**WICHTIG:** Diese Tests bewegen die Hardware! Nur ausführen, wenn alles angeschlossen ist.

### 3. Dauerhaft PYTHONPATH setzen:

Falls du `export PYTHONPATH` jedes Mal neu setzen musst:

```bash
echo 'export PYTHONPATH=$HOME/saugbot:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

Dann funktioniert es automatisch bei jedem neuen Terminal.

## Git Workflow:

```bash
cd ~/saugbot
git add .
git commit -m "Beschreibung"
git push origin main
```

## Nächste Schritte:

1. Hardware anschließen (Motoren, Sensoren, etc.)
2. GPIO-Pins in `config.py` prüfen/anpassen
3. Programm testen
