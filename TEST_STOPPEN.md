# 🛑 Test stoppen

## Monitoring-Test stoppen:

**Drücke:** `Ctrl + C`

Das beendet das Script sofort.

## Nach dem Stoppen:

Du siehst eine Zusammenfassung mit:
- Anzahl erfolgreicher Messungen
- Statistik (Min/Max/Durchschnitt)

## Diagnose-Tool starten:

```bash
cd ~/saugbot
git pull
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/diagnose_pins.py
```

Das zeigt:
- ✅ Welche Sensoren gefunden wurden
- ⚠️  Welche Pins Probleme haben
- 🔍 Warum etwas nicht funktioniert
