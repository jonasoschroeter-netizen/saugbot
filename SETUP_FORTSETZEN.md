# Setup-Script fortführen

## Status:
- ✅ SSH-Key zu GitHub hinzugefügt
- ✅ Setup-Script wartet auf Enter

## Nächster Schritt:

**Am Pi-Terminal:**
- Drücke **ENTER**

Das Script führt dann automatisch aus:

1. **GitHub Verbindung testen**
   - Testet ob SSH-Verbindung zu GitHub funktioniert
   - Sollte "successfully authenticated" zeigen

2. **Repository klonen**
   - Klont `git@github.com:jonasoschroeter-netizen/saugbot.git`
   - Nach `~/saugbot`

3. **Python Dependencies installieren**
   - Installiert `RPi.GPIO`
   - Installiert `python-dotenv`
   - Installiert `pytest` (optional)

4. **.env Datei erstellen**
   - Kopiert `.env.example` zu `.env`

5. **GPIO Berechtigungen prüfen**
   - Prüft ob User in `gpio` Gruppe ist

## Nach dem Setup:

```bash
cd ~/saugbot
python3 src/main.py
```

## Falls Fehler auftreten:

Sag Bescheid, dann helfe ich beim Troubleshooting!
