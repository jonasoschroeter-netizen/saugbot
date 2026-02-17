# 📌 Pin 35 Information

## Standard Raspberry Pi Pinout:

**Pin 35 = GND (Masse)** bei den meisten Raspberry Pi Modellen

## Aber:

Du sagst Pin 35 ist **kein GND**. Das könnte bedeuten:

1. **Anderes Pi-Modell:** Manche Pi-Modelle haben andere Pin-Belegungen
2. **Andere Pin-Nummerierung:** Vielleicht zählst du die Pins anders?
3. **HAT/Shield:** Ein aufgestecktes Board könnte Pins umbelegt haben

## Prüfe Pin 35:

Führe dieses Script aus:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/check_pin35.py
```

Das zeigt:
- Ob Pin 35 als GPIO verwendet werden kann
- Welcher Zustand Pin 35 hat
- Ob es als Trigger verwendet werden kann

## Falls Pin 35 wirklich ein GPIO-Pin ist:

Dann teile mir mit:
- **Welcher GPIO-Pin ist Pin 35?** (z.B. GPIO 16, GPIO 26, etc.)
- Dann aktualisiere ich die config.py entsprechend

## Alternative Pin-Mappings:

Falls du ein **Raspberry Pi Zero** oder anderes Modell verwendest:
- Pin-Belegungen können abweichen
- Prüfe die Dokumentation deines Pi-Modells

## Nächste Schritte:

1. **Prüfe Pin 35:** Führe `check_pin35.py` aus
2. **Teile mir mit:** Welcher GPIO-Pin ist Pin 35?
3. **Dann:** Aktualisiere ich die config.py
