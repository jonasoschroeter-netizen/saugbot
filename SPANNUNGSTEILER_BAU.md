# 🔧 Spannungsteiler für HC-SR04 Echo-Pin

## Problem

Der HC-SR04 Echo-Pin gibt **5V** aus, aber der Raspberry Pi GPIO verträgt nur **3.3V**. Ein Spannungsteiler reduziert die Spannung sicher.

## Material

- **1x 10kΩ Widerstand** (braun-schwarz-orange)
- **1x 20kΩ Widerstand** (rot-schwarz-orange)
- **Lötkolben + Lötzinn** (oder Steckbrett für Test)

## Verkabelung

### Schaltplan:

```
HC-SR04 Echo (5V)
    │
    ├───[10kΩ]───→ GPIO 14 (Raspberry Pi)
    │
    └───[20kΩ]───→ GND
```

### Schritt-für-Schritt:

1. **10kΩ Widerstand:**
   - Ein Ende → HC-SR04 Echo-Pin
   - Anderes Ende → GPIO 14 (Raspberry Pi)

2. **20kΩ Widerstand:**
   - Ein Ende → Verbindung zwischen 10kΩ und GPIO 14
   - Anderes Ende → GND (Raspberry Pi GND)

3. **Prüfen:**
   - Alle Verbindungen fest?
   - GND richtig verbunden?
   - Keine Kurzschlüsse?

## Berechnung

**Spannungsteilung:**
- Gesamtwiderstand: 10kΩ + 20kΩ = 30kΩ
- Spannung am GPIO: 5V × (20kΩ / 30kΩ) = 3.33V

**Sicherheit:**
- GPIO Maximum: 3.3V
- Tatsächliche Spannung: ~3.33V (knapp, aber OK)
- Mit Toleranzen: ~3.0V - 3.6V (sicher)

**Alternative (sicherer):**
- 15kΩ + 10kΩ = 25kΩ
- Spannung: 5V × (10kΩ / 25kΩ) = 2.0V (sehr sicher)

## Test nach dem Bau

### 1. Hardware prüfen

**Mit Multimeter:**
- Spannung zwischen GPIO 14 und GND messen
- Sollte ~0V sein wenn Sensor nicht aktiv
- Sollte ~2-3V sein wenn Sensor Echo sendet

### 2. Software-Test

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/sensor_voltage_divider_test.py
```

**Erwartetes Ergebnis:**
- ✅ Distanz-Werte werden angezeigt
- ✅ Werte ändern sich wenn du dich näherst/entfernst
- ✅ Keine Timeout-Fehler

### 3. Web-Interface testen

```bash
# Web-Interface sollte automatisch laufen
# Oder manuell starten:
python3 src/web_interface.py
```

Dann im Browser: `http://192.168.0.5:5000`

## Troubleshooting

### Problem: Immer noch Timeout

**Prüfe:**
1. Spannungsteiler richtig verkabelt?
2. Widerstände haben richtige Werte? (mit Multimeter prüfen)
3. GND richtig verbunden?
4. GPIO 14 richtig angeschlossen?

**Test:**
```bash
# Echo-Pin Status prüfen
python3 src/sensor_hardware_test.py
```

### Problem: Falsche Distanz-Werte

**Mögliche Ursachen:**
- Widerstände haben falsche Werte
- Spannungsteiler nicht richtig verkabelt
- Sensor hat Störungen

**Lösung:**
- Widerstände mit Multimeter prüfen
- Verkabelung nochmal prüfen
- Andere Widerstände testen

### Problem: Sensor reagiert nicht

**Prüfe:**
1. Sensor hat 5V?
2. Trigger-Pin funktioniert? (GPIO 4)
3. GND verbunden?
4. Sensor LED leuchtet?

## Alternative Widerstandswerte

Wenn du andere Widerstände hast:

| R1 | R2 | Spannung am GPIO | Sicherheit |
|----|----|------------------|------------|
| 10kΩ | 20kΩ | 3.33V | ⚠️ Knapp |
| 15kΩ | 10kΩ | 2.0V | ✅ Sehr sicher |
| 12kΩ | 18kΩ | 3.0V | ✅ Sicher |
| 8kΩ | 12kΩ | 3.0V | ✅ Sicher |

**Formel:** `V_out = V_in × (R2 / (R1 + R2))`

## Nächste Schritte

1. ✅ Spannungsteiler bauen
2. ✅ Hardware-Test ausführen (`sensor_voltage_divider_test.py`)
3. ✅ Web-Interface testen
4. ✅ Roboter-Logik testen

## Wichtig

- **Spannungsteiler reduziert nur die Spannung**
- **Trigger-Pin kann direkt angeschlossen werden** (3.3V ist OK)
- **VCC muss 5V bleiben** (Sensor braucht 5V)
- **GND muss verbunden sein**
