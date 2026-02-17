# 🔍 Sensoren schnell testen

## Auf dem Raspberry Pi ausführen:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/test_pins.py
```

## Oder alle Sensoren testen:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/test_all_sensors.py
```

## Falls Datei nicht gefunden:

```bash
# Prüfe ob Datei existiert:
ls -la src/test_pins.py

# Falls nicht, hole Updates:
cd ~/saugbot
git pull origin main
```
