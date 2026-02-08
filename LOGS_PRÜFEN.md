# Auto-Update Logs prüfen

## Problem:
`journalctl` zeigt nur Start-Eintrag, keine weiteren Logs.

## Lösung: Logs auf verschiedene Weise prüfen

### 1. Log-Datei direkt lesen:

```bash
tail -f ~/saugbot/logs/auto_update.log
```

Falls die Datei nicht existiert:
```bash
ls -la ~/saugbot/logs/
mkdir -p ~/saugbot/logs  # Falls Verzeichnis fehlt
```

### 2. Prüfe ob Script läuft:

```bash
ps aux | grep auto_update
```

Sollte Python-Prozess zeigen.

### 3. Prüfe direkt ob Update geholt wurde:

```bash
cd ~/saugbot
git log --oneline -1
```

**Sollte zeigen:**
- "TEST: Auto-Update System - 21:27:12" (oder neuerer Commit)

### 4. README.md prüfen:

```bash
cd ~/saugbot
tail -5 README.md
```

**Sollte zeigen:**
- "🧪 Auto-Update Test"
- "Test-Update um 21:30 Uhr"

### 5. Service Status prüfen:

```bash
sudo systemctl status saugbot-auto-update.service
```

### 6. Manuell testen ob Update verfügbar:

```bash
cd ~/saugbot
git fetch origin
git status
```

Falls "Your branch is behind" → Update wurde noch nicht geholt
Falls "Your branch is up to date" → Update wurde bereits geholt

## Nach Verbesserung (nächster Pull):

Das Script schreibt jetzt auch in systemd logs. Nach `git pull` und Service-Neustart:

```bash
sudo systemctl restart saugbot-auto-update.service
sudo journalctl -u saugbot-auto-update.service -f
```

Dann solltest du mehr Logs sehen!
