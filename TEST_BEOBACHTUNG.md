# Test-Beobachtung am Raspberry Pi

## 🧪 Test-Update wurde gesendet!

**Zeitpunkt:** Jetzt
**Änderung:** README.md wurde aktualisiert
**Commit:** "TEST: Auto-Update System - [Zeit]"

## Was du am Pi-Terminal sehen solltest:

### Option 1: Auto-Update Logs live beobachten:

```bash
sudo journalctl -u saugbot-auto-update.service -f
```

**Du solltest sehen:**
- ✅ "🔄 Updates gefunden! Starte Update..."
- ✅ "✅ Repository erfolgreich aktualisiert!"
- ✅ Git-Pull Output
- ✅ "✅ Update abgeschlossen. Nächste Prüfung in 30 Sekunden..."

### Option 2: Repository direkt prüfen:

```bash
cd ~/saugbot
git log --oneline -1
```

**Sollte zeigen:**
- ✅ Neuester Commit: "TEST: Auto-Update System - [Zeit]"

### Option 3: README.md prüfen:

```bash
cd ~/saugbot
tail -5 README.md
```

**Sollte zeigen:**
- ✅ "🧪 Auto-Update Test"
- ✅ "Test-Update um 21:30 Uhr" (oder aktuelle Zeit)

## Zeitrahmen:

- **0-30 Sekunden:** Auto-Update prüft noch nicht (nächste Prüfung)
- **30-60 Sekunden:** Auto-Update sollte Update finden und holen
- **Nach Update:** Repository ist aktualisiert

## Falls nichts passiert:

```bash
# Prüfe ob Auto-Update läuft
sudo systemctl status saugbot-auto-update.service

# Prüfe Logs
sudo journalctl -u saugbot-auto-update.service -n 50

# Manuell prüfen
cd ~/saugbot
git fetch origin
git status
```

## ✅ Erfolg wenn:

- Auto-Update Logs zeigen "Updates gefunden"
- `git log` zeigt neuen Commit
- README.md enthält Test-Text
