# 🔧 Level Shifter Problem - Lösungen

## Problem-Diagnose

Der Test zeigt:
- **Mit Pull-Down**: Echo-Pin ist LOW ✅
- **Mit Pull-Up**: Echo-Pin bleibt HIGH ❌
- **Nach Trigger**: Echo wird HIGH, bleibt aber HIGH ❌

**Bedeutung:** Der Echo-Pin ist "schwebend" (floating) - er ist nicht richtig mit dem Sensor verbunden.

## Ursache: Level Shifter Problem

Der Level Shifter funktioniert nicht richtig oder ist falsch verkabelt.

## Lösung 1: Level Shifter Verkabelung prüfen

### Richtige Verkabelung:

```
HC-SR04 Sensor:
  VCC  → 5V
  GND  → GND
  Trig → GPIO 4 (kann direkt, da 3.3V OK ist)
  Echo → Level Shifter HV (High Voltage Eingang)

Level Shifter (z.B. TXB0104 oder ähnlich):
  HV (High Voltage) → Sensor Echo (5V)
  LV (Low Voltage) → GPIO 14 (3.3V)
  GND              → GND
  VCC (LV-Seite)   → 3.3V
  VCC (HV-Seite)   → 5V (optional, manche brauchen es)
```

### Häufige Fehler:

1. **Falsche Pins am Level Shifter**
   - HV und LV vertauscht
   - Richtung falsch (bidirektional vs. unidirektional)

2. **VCC nicht angeschlossen**
   - LV-Seite braucht 3.3V
   - HV-Seite braucht manchmal 5V

3. **GND nicht verbunden**
   - Alle GND müssen verbunden sein

## Lösung 2: Spannungsteiler (Alternative)

Wenn der Level Shifter nicht funktioniert, kannst du einen **Spannungsteiler** bauen:

### Benötigt:
- 1x 10kΩ Widerstand
- 1x 20kΩ Widerstand

### Verkabelung:

```
Sensor Echo (5V) → [10kΩ] → GPIO 14 (3.3V)
                        ↓
                    [20kΩ]
                        ↓
                      GND
```

**Berechnung:**
- 10kΩ + 20kΩ = 30kΩ Gesamtwiderstand
- Spannungsteilung: 20kΩ / 30kΩ = 2/3
- 5V × (1/3) = ~1.67V am GPIO (sicher unter 3.3V)

**Oder präziser:**
- 10kΩ + 20kΩ = 30kΩ
- GPIO sieht: 5V × (20kΩ / 30kΩ) = 3.33V (knapp, aber OK)

**Besser:**
- 15kΩ + 10kΩ = 25kΩ
- GPIO sieht: 5V × (10kΩ / 25kΩ) = 2V (sicher)

## Lösung 3: Direkter Test (NUR FÜR DIAGNOSE!)

⚠️ **WARNUNG:** Nur für kurzen Test! Dauerhaft kann der Pi beschädigt werden!

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/sensor_direct_test.py
```

Dieser Test verbindet den Sensor direkt (ohne Level Shifter) für 10 Sekunden.

**Wenn das funktioniert:**
- Sensor ist OK
- Problem ist definitiv der Level Shifter

**Wenn das nicht funktioniert:**
- Sensor könnte defekt sein
- Oder Verkabelung ist falsch

## Lösung 4: Neuen Level Shifter verwenden

### Empfohlene Level Shifter:

1. **TXB0104** (4-Kanal, bidirektional)
2. **74LVC1T45** (1-Kanal, bidirektional)
3. **SparkFun Logic Level Converter** (einfach zu verwenden)

### Verkabelung TXB0104:

```
Pin 1 (VCCA) → 3.3V
Pin 2 (A1)   → GPIO 14
Pin 3 (B1)   → Sensor Echo
Pin 4 (GND)  → GND
Pin 5 (B2)   → (nicht verwendet)
Pin 6 (A2)   → (nicht verwendet)
Pin 7 (OE)   → 3.3V (Enable)
Pin 8 (VCCB) → 5V
```

## Empfohlene Vorgehensweise

1. ✅ **Direkten Test ausführen** (`sensor_direct_test.py`)
   - Wenn funktioniert → Level Shifter Problem
   - Wenn nicht funktioniert → Sensor Problem

2. ✅ **Level Shifter Verkabelung prüfen**
   - HV/LV richtig?
   - VCC angeschlossen?
   - GND verbunden?

3. ✅ **Spannungsteiler bauen** (schnelle Lösung)
   - 2 Widerstände verwenden
   - Einfacher als Level Shifter

4. ✅ **Neuen Level Shifter kaufen** (beste Lösung)
   - TXB0104 oder ähnlich
   - Professionelle Lösung

## Schnelle Lösung: Spannungsteiler

**Material:**
- 1x 10kΩ Widerstand
- 1x 20kΩ Widerstand (oder 15kΩ + 10kΩ)

**Verkabelung:**
```
Sensor Echo → [10kΩ] → GPIO 14
                  ↓
              [20kΩ]
                  ↓
                GND
```

**Das sollte sofort funktionieren!**

## Nächste Schritte

1. Führe `sensor_direct_test.py` aus
2. Wenn funktioniert: Spannungsteiler bauen oder Level Shifter reparieren
3. Wenn nicht funktioniert: Sensor prüfen/ersetzen
