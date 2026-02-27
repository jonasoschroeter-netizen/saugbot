# Warum Multimeter 0V bei Echo zeigt – obwohl es funktioniert

## Ergebnis des Tests

- **Links:** ✅ ~29 cm
- **Rechts:** ✅ ~172 cm  
- **Front:** ❌ Kein Signal (Verkabelung prüfen)

## Warum zeigt das Multimeter 0V am Echo-Pin?

Der Echo-Puls des HC-SR04 ist nur **ca. 0,3–0,5 ms** lang.

- Ein Multimeter mittelt über Zeit → der kurze Puls geht im Mittelwert unter.
- Der Pi liest sehr schnell (Mikrosekunden) → er erkennt den Puls.
- **Fazit:** 0V am Multimeter ist normal, der Sensor funktioniert trotzdem.

## Front-Sensor (GPIO 5/6)

Nur der Front-Sensor liefert kein Signal. Prüfen:

- Trigger Pin 29 (GPIO 5) – Stecker fest?
- Echo Pin 31 (GPIO 6) – Stecker fest?
- Spannungsteiler am Echo vorhanden?
- VCC (5V) und GND am Sensor?
