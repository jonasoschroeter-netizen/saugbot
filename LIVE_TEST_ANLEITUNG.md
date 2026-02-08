# LIVE-TEST: Auto-Update beobachten

## ✅ Gute Nachricht:
Auto-Update hat bereits funktioniert! Der Commit "6b0e93d" ist auf dem Pi.

## 🧪 Neuer LIVE-TEST gestartet:

**Zeitpunkt:** Jetzt (21:32 Uhr)
**Änderung:** README.md wurde aktualisiert
**Commit:** "LIVE-TEST: Auto-Update System - [Zeit]"

## Am Raspberry Pi-Terminal:

### 1. Logs-Verzeichnis erstellen (einmalig):

```bash
cd ~/saugbot
mkdir -p logs
```

### 2. Service neu starten (für bessere Logs):

```bash
sudo systemctl restart saugbot-auto-update.service
```

### 3. Live-Logs beobachten:

```bash
sudo journalctl -u saugbot-auto-update.service -f
```

**Du solltest innerhalb von 30-60 Sekunden sehen:**
- ✅ "🚀 Saugbot Auto-Update System gestartet"
- ✅ "⏱️  Prüfe alle 30 Sekunden auf Updates..."
- ✅ "🔄 Updates gefunden! Starte Update..."
- ✅ "✅ Repository erfolgreich aktualisiert!"
- ✅ Git-Pull Output

### 4. ODER in neuem Terminal prüfen:

```bash
cd ~/saugbot
watch -n 2 'git log --oneline -1'
```

Oder einfach:
```bash
cd ~/saugbot
git log --oneline -1
```

**Sollte nach 30-60 Sekunden zeigen:**
- "LIVE-TEST: Auto-Update System - [Zeit]"

### 5. README.md prüfen:

```bash
cd ~/saugbot
tail -5 README.md
```

**Sollte zeigen:**
- "🧪 Auto-Update Test"
- "LIVE-TEST um 21:32 Uhr"

## Zeitrahmen:

- **0-30 Sekunden:** Auto-Update prüft noch nicht (nächste Prüfung)
- **30-60 Sekunden:** Auto-Update sollte Update finden und holen
- **Nach Update:** Repository ist aktualisiert

## ✅ Erfolg wenn:

- `journalctl -f` zeigt "Updates gefunden!"
- `git log` zeigt neuen "LIVE-TEST" Commit
- README.md enthält "LIVE-TEST um 21:32 Uhr"
