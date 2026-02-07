# GPIO-Fehler behoben - Update holen

## Problem:
Main Service schlug fehl mit: `RuntimeError: Please set pin numbering mode`

## Lösung:
GPIO Cleanup-Reihenfolge wurde behoben.

## Update holen am Raspberry Pi:

```bash
cd ~/saugbot
git pull origin main
```

## Service neu starten:

```bash
sudo systemctl restart saugbot-main.service
```

## Status prüfen:

```bash
sudo systemctl status saugbot-main.service
```

Sollte jetzt "active (running)" zeigen!

## Falls Auto-Update läuft:

Das Auto-Update sollte den Fix automatisch holen (innerhalb von 30 Sekunden).

Dann Service neu starten:
```bash
sudo systemctl restart saugbot-main.service
```
