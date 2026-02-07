# Quick Start: Automatisches Update-System

## 🎯 Ziel:
**Du codest nur auf dem Laptop, der Pi holt automatisch Updates!**

## Installation auf Raspberry Pi (EINMALIG):

### 1. Updates holen:
```bash
cd ~/saugbot
git pull origin main
```

### 2. Logs-Verzeichnis erstellen:
```bash
mkdir -p logs
```

### 3. Scripts ausführbar machen:
```bash
chmod +x auto_update.py
chmod +x start_saugbot.sh
chmod +x start_web_interface.sh
```

## Verwendung:

### Hauptprogramm mit Auto-Update starten:
```bash
cd ~/saugbot
./start_saugbot.sh
```

### Web-Interface mit Auto-Update starten:
```bash
cd ~/saugbot
./start_web_interface.sh
```

## Workflow (danach):

### Auf dem Laptop:
1. Code schreiben
2. `git add .`
3. `git commit -m "Beschreibung"`
4. `git push origin main`

### Auf dem Raspberry Pi:
**NICHTS!** 🎉

- Auto-Update prüft alle 30 Sekunden
- Findet Updates automatisch
- Holt sie automatisch
- Startet Programm neu

## Fertig! 🚀

Jetzt musst du den Pi nicht mehr anfassen - alles läuft automatisch!
