# 📊 Sensor Live-Monitoring

## Gefundener Sensor überwachen:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/monitor_sensor.py
```

## Mit anderen Pins testen:

```bash
# Beispiel: Trigger=GPIO 20, Echo=GPIO 21
python3 src/monitor_sensor.py 20 21

# Beispiel: Trigger=GPIO 4, Echo=GPIO 14
python3 src/monitor_sensor.py 4 14
```

## Was du siehst:

- **Live-Distanz** alle 200ms
- **Farbcodierung:**
  - 🔴 Rot: < 10cm (SEHR NAH!)
  - 🟡 Gelb: 10-20cm (NAH)
  - 🟢 Grün: 20-50cm (OK)
  - 🔵 Blau: > 50cm (WEIT)
- **Statistik** alle 10 Messungen (Min/Max/Durchschnitt)

## So identifizierst du den Sensor:

1. **Starte Monitoring:**
   ```bash
   python3 src/monitor_sensor.py 20 21
   ```

2. **Bewege dich vor dem Sensor:**
   - Stelle dich **vorne** vor den Roboter → Front-Sensor?
   - Stelle dich **links vorne** → Links-Sensor?
   - Stelle dich **rechts vorne** → Rechts-Sensor?

3. **Beobachte die Werte:**
   - Wenn Distanz **kleiner wird** wenn du näher kommst → Sensor funktioniert!
   - Wenn Distanz **gleich bleibt** → Falscher Sensor oder Sensor nicht aktiv

4. **Notiere welcher Sensor es ist!**

## Beispiel-Output:

```
[14:23:45] 🟢  45.3cm (OK)
[14:23:45] 🟢  44.8cm (OK)
[14:23:46] 🟡  18.5cm (NAH)
[14:23:46] 🔴   8.2cm (SEHR NAH!)
         Statistik: Min=8.2cm, Avg=29.3cm, Max=45.3cm
```

## Nach Identifikation:

Sag mir:
- **Welcher Sensor ist GPIO 20/21?** (Front/Links/Rechts)
- Dann finden wir die anderen 2 Sensoren!
