# Web Interface für Ultraschall-Sensoren

## Übersicht

Ein Web-Interface zum Testen und Einstellen der Ultraschall-Sensoren.

## Features:

- ✅ Live-Anzeige der Sensor-Distanzen (Front, Left, Right)
- ✅ Auto-Refresh (aktualisiert jede Sekunde)
- ✅ Konfiguration anpassen (Kollisions-Distanz, Minimale Distanz)
- ✅ Schönes, modernes Interface
- ✅ Funktioniert auch ohne Hardware (zeigt Fehler an)

## Installation:

### 1. Flask installieren:

Am Raspberry Pi:

```bash
cd ~/saugbot
pip3 install Flask --break-system-packages
```

### 2. Web-Interface starten:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/web_interface.py
```

### 3. Im Browser öffnen:

- **Vom Laptop:** `http://192.168.0.5:5000`
- **Vom Pi selbst:** `http://localhost:5000`

## Verwendung:

1. **Sensor-Werte anzeigen:**
   - Die drei Sensoren zeigen ihre aktuellen Distanzen in cm
   - Auto-Refresh aktualisiert automatisch jede Sekunde

2. **Konfiguration anpassen:**
   - **Kollisions-Distanz:** Abstand, bei dem Kollisionsvermeidung ausgelöst wird
   - **Minimale Distanz:** Minimale sichere Distanz
   - Klicke "Konfiguration speichern" um zu speichern

3. **Ohne Hardware:**
   - Interface zeigt "Sensoren nicht verfügbar"
   - Konfiguration kann trotzdem angepasst werden

## Dateien:

- `src/web_interface.py` - Flask Backend
- `src/templates/index.html` - Web-Interface Frontend

## API Endpoints:

- `GET /api/sensors/status` - Sensor-Status prüfen
- `GET /api/sensors/read` - Sensor-Werte lesen
- `GET /api/config/get` - Konfiguration lesen
- `POST /api/config/update` - Konfiguration speichern

## Stoppen:

Drücke `Ctrl+C` im Terminal, um das Web-Interface zu stoppen.
