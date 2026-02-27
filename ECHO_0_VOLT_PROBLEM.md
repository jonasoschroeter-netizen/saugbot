# 🔧 Echo-Pins zeigen 0V - Diagnose

## Das Problem
Echo-Pins (40, 37, 31) haben überall 0V.

## Mögliche Ursachen

### 1. Echo-Puls ist sehr kurz (~0,3 ms)
Der HC-SR04 sendet nur **0,3–0,5 ms** lang 5V auf Echo. Ein Multimeter zeigt oft den **Mittelwert** → 0V, weil der Puls so kurz ist.

**Test:** Script laufen lassen, das ständig triggert – dann kurz vor einen Gegenstand (10–30 cm) halten und schauen, ob das Multimeter kurz etwas anzeigt.

### 2. Spannungsteiler falsch verkabelt
```
RICHTIG:
Sensor ECHO (5V) ---[1kΩ]---+---[2kΩ]--- GND
                            |
                            +--- zu Pi GPIO (Pin 40, 37, 31)

FALSCH (häufig):
- Echo direkt an Pi (OHNE Teiler) → Pi könnte Schaden nehmen!
- Teiler-Ausgang nicht am Pi angeschlossen
- 1k und 2k vertauscht
```

### 3. Sensor hat keine Stromversorgung
- **VCC:** Muss 5V haben (Pin 2 oder 4)
- **GND:** Muss 0V haben (Pin 39)

**Prüfen:** Am Sensor zwischen VCC und GND messen → sollte 5V sein.

### 4. Echo-Kabel nicht verbunden
- Ist das Echo-Kabel vom Sensor am richtigen Pi-Pin?
- Sensor 1 Echo → Pin 40
- Sensor 2 Echo → Pin 37  
- Sensor 3 Echo → Pin 31

### 5. Sensor defekt oder kein Echo
- Sensor muss auf einen Gegenstand zeigen (5 cm – 4 m)
- Ohne Reflexion bleibt Echo dauerhaft 0V

## Nächste Schritte

1. **VCC am Sensor prüfen:** Zwischen VCC und GND des Sensors → 5V?
2. **Spannungsteiler prüfen:** Schaltung und Anschlüsse kontrollieren
3. **Echo direkt am Sensor messen:** Vor dem Spannungsteiler – kommt dort 5V an?
4. **LED-Test:** Script nutzen, das eine LED blinken lässt, wenn Echo erkannt wird
