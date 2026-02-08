# 🔧 Sensor-Problem: Echo-Pin bleibt HIGH

## Problem

Der Echo-Pin des HC-SR04 Sensors bleibt dauerhaft auf HIGH und geht nie auf LOW zurück. Das bedeutet, der Sensor kann keine Distanz messen.

## Diagnose

**Symptome:**
- Echo-Pin ist HIGH am Anfang (sollte LOW sein)
- Echo wird HIGH nach Trigger (gut)
- Echo bleibt HIGH (Problem - geht nie auf LOW)

## Mögliche Ursachen

### 1. Level Shifter Problem ⚠️ (Wahrscheinlichste Ursache)

Der Echo-Pin des HC-SR04 gibt **5V** aus, aber der Raspberry Pi GPIO kann nur **3.3V** vertragen. Deshalb MUSS ein Level Shifter verwendet werden.

**Prüfen:**
- Ist der Level Shifter richtig verkabelt?
- Funktioniert der Level Shifter? (mit Multimeter testen)
- Ist der Level Shifter defekt?

**Lösung:**
- Level Shifter Verkabelung prüfen
- Level Shifter ersetzen (falls defekt)
- Richtige Pins am Level Shifter verwenden

### 2. Falsche Verkabelung

**Prüfe:**
- Echo-Pin ist an GPIO 14 angeschlossen?
- Level Shifter ist zwischen Echo und GPIO 14?
- Alle GND verbunden? (Sensor GND, Level Shifter GND, Pi GND)

### 3. Sensor defekt

**Test:**
- Anderen HC-SR04 Sensor testen
- Sensor mit Multimeter prüfen

### 4. Pull-Down Widerstand fehlt

Manche Level Shifter brauchen einen Pull-Down Widerstand am Echo-Pin.

## Lösungsversuche

### Schritt 1: Erweiterten Hardware-Test ausführen

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/sensor_hardware_test.py
```

Dieser Test zeigt:
- Echo-Pin Status über Zeit
- Ob der Pin sich ändert
- Detaillierte Hardware-Informationen

### Schritt 2: Level Shifter prüfen

**Multimeter-Test:**
1. Level Shifter ohne Sensor anschließen
2. Eingang (5V-Seite) mit Multimeter prüfen
3. Ausgang (3.3V-Seite) mit Multimeter prüfen
4. Beide Seiten sollten LOW sein wenn nichts angeschlossen ist

**Verkabelung prüfen:**
- Level Shifter HV (High Voltage) → Sensor Echo (5V)
- Level Shifter LV (Low Voltage) → GPIO 14 (3.3V)
- Level Shifter GND → GND
- Level Shifter VCC → 3.3V (für LV-Seite)

### Schritt 3: Alternative Verkabelung testen

**Option A: Direkt ohne Level Shifter (NUR FÜR TEST!)**

⚠️ **WARNUNG:** Nur für kurzen Test! Dauerhaft kann der Pi beschädigt werden!

```python
# Echo direkt an GPIO 14 (ohne Level Shifter)
# Funktioniert nur wenn Sensor 3.3V-tolerant ist (meist nicht)
```

**Option B: Spannungsteiler verwenden**

Statt Level Shifter: 2 Widerstände (10kΩ und 20kΩ) als Spannungsteiler:
- 10kΩ zwischen Echo und GPIO 14
- 20kΩ zwischen GPIO 14 und GND
- Reduziert 5V auf ~3.3V

### Schritt 4: Sensor direkt testen

**Ohne Raspberry Pi:**
- Sensor mit Arduino testen
- Sensor mit Multimeter prüfen
- Anderen Sensor testen

## Empfohlene Vorgehensweise

1. ✅ **Erweiterten Test ausführen** (`sensor_hardware_test.py`)
2. ✅ **Level Shifter Verkabelung prüfen** (siehe oben)
3. ✅ **Level Shifter mit Multimeter testen**
4. ✅ **Anderen Level Shifter testen** (falls verfügbar)
5. ✅ **Anderen Sensor testen** (falls verfügbar)

## Schnelle Lösung (wenn Level Shifter defekt)

**Spannungsteiler bauen:**
```
Sensor Echo → [10kΩ] → GPIO 14
                    ↓
                  [20kΩ]
                    ↓
                   GND
```

**Oder:**
- Neuen Level Shifter kaufen
- Anderen Level Shifter verwenden

## Nächste Schritte

Nach dem Hardware-Test:
1. Ergebnisse dokumentieren
2. Level Shifter prüfen/ersetzen
3. Sensor erneut testen
4. Bei Erfolg: Web-Interface sollte funktionieren
