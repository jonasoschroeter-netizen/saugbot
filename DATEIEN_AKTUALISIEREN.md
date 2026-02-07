# Dateien vom GitHub aktualisieren

## Problem:
`web_interface.py` wurde nicht gefunden - die neuen Dateien sind noch nicht auf dem Pi.

## Lösung:

### Am Raspberry Pi:

```bash
cd ~/saugbot
git pull origin main
```

Das lädt alle neuen Dateien vom GitHub Repository herunter:
- `src/web_interface.py`
- `src/templates/index.html`
- `requirements.txt` (mit Flask)
- etc.

### Dann Web-Interface starten:

```bash
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

### Falls git pull Fehler gibt:

Prüfe ob alles committed ist:
```bash
git status
```

Falls es lokale Änderungen gibt:
```bash
git stash
git pull origin main
```

## Alternative: Dateien manuell kopieren

Falls git pull nicht funktioniert, können die Dateien auch manuell vom Laptop auf den Pi kopiert werden (z.B. per SCP oder direkt am Pi erstellen).
