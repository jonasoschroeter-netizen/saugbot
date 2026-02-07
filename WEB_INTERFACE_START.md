# Web-Interface starten - Schritt für Schritt

## Status:
- ✅ Hauptprogramm läuft
- ✅ Flask wird installiert
- ✅ .env Datei erstellt

## Nach Flask-Installation:

### 1. Web-Interface starten:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

### 2. Im Browser öffnen:

Vom Laptop aus:
- **http://192.168.0.5:5000**

Oder vom Pi selbst:
- **http://localhost:5000**

## Was du sehen wirst:

- **3 Sensor-Karten** mit Live-Distanzen (Front, Left, Right)
- **Status-Anzeige** (verbunden/nicht verbunden)
- **Konfigurations-Panel** zum Anpassen der Schwellenwerte
- **Auto-Refresh** Checkbox (aktualisiert jede Sekunde)

## Wichtig:

- **PYTHONPATH muss gesetzt sein** (sonst findet Python config.py nicht)
- **Hauptprogramm stoppen** (Ctrl+C), wenn du das Web-Interface startest
- **Oder:** Beide parallel laufen lassen (in verschiedenen Terminals)

## Dauerhaft PYTHONPATH setzen (optional):

Falls du `export PYTHONPATH` jedes Mal neu setzen musst:

```bash
echo 'export PYTHONPATH=$HOME/saugbot:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

Dann funktioniert es automatisch bei jedem neuen Terminal.

## Stoppen:

Drücke `Ctrl+C` im Terminal, um das Web-Interface zu stoppen.
