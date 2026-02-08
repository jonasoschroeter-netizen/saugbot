# 🔍 Sensor-Einstellung und Test

## Übersicht

Du hast jetzt:
1. **Live-Distanz-Anzeige** für den Links Vorne Sensor
2. **Schwellenwert-Regler** zum Einstellen der Kollisions-Distanz
3. **Automatische Kollisionsvermeidung**: Roboter fährt nach rechts, wenn Links-Sensor anschlägt

## Web-Interface verwenden

### 1. Web-Interface starten

```bash
cd ~/saugbot
python3 src/web_interface.py
```

Oder wenn der Service läuft:
```bash
# Service sollte automatisch laufen nach Neustart
# Prüfen mit:
sudo systemctl status saugbot-web.service
```

### 2. Interface öffnen

Im Browser öffnen:
- `http://192.168.0.5:5000` (oder `http://saugbot.local:5000`)

### 3. Sensor testen

- **Große Anzeige**: Zeigt die aktuelle Distanz des Links Vorne Sensors
- **Farbcodierung**:
  - 🟢 **Grün**: OK - Distanz > Schwellenwert
  - 🟡 **Gelb**: WARNUNG - Distanz nahe Schwellenwert
  - 🔴 **Rot**: HINDERNIS - Distanz < Schwellenwert

### 4. Schwellenwert einstellen

1. **Regler verwenden**: Ziehe den Schieberegler für "Schwellenwert für Links Vorne Sensor"
2. **Wert anzeigen**: Der aktuelle Wert wird rechts neben dem Regler angezeigt
3. **Speichern**: Klicke auf "Konfiguration speichern"
4. **Automatisch aktiv**: Der Roboter verwendet den neuen Wert sofort

**Empfohlene Werte:**
- **10-15 cm**: Für enge Räume, schnelle Reaktion
- **20-25 cm**: Für normale Räume
- **30-40 cm**: Für große Räume, frühe Warnung

## Kollisionsvermeidung

### Funktionsweise

Wenn der **Links Vorne Sensor** einen Wert **unter dem Schwellenwert** misst:

1. **Roboter stoppt** sofort
2. **Fährt kurz zurück** (0.5 Sekunden)
3. **Fährt nach rechts** (rechts drehen)
4. **Prüft kontinuierlich** die Distanz
5. **Fährt weiter**, sobald Distanz > Schwellenwert

### Testen

1. Stelle einen Gegenstand **links vorne** vor den Roboter
2. Roboter sollte **sofort stoppen** und **nach rechts ausweichen**
3. Wenn Gegenstand weg ist, fährt Roboter **weiter geradeaus**

## Terminal-Test (Alternative)

Für schnelle Tests ohne Web-Interface:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/sensor_test.py
```

Zeigt:
- Live-Distanz alle 0.5 Sekunden
- Farbcodierte Warnungen
- Schwellenwert-Anzeige

## Troubleshooting

### Sensor zeigt "--"
- **Prüfe Verkabelung**: Trigger und Echo-Pins korrekt angeschlossen?
- **Prüfe Stromversorgung**: Sensor hat 5V?
- **Prüfe Level Shifter**: Echo-Pin über Level Shifter?

### Roboter reagiert nicht
- **Config neu laden**: Web-Interface → "Konfiguration speichern" klicken
- **Service neu starten**: `sudo systemctl restart saugbot-main.service`
- **Logs prüfen**: `sudo journalctl -u saugbot-main.service -f`

### Web-Interface nicht erreichbar
- **Service prüfen**: `sudo systemctl status saugbot-web.service`
- **Port prüfen**: `netstat -tuln | grep 5000`
- **Manuell starten**: `python3 src/web_interface.py`

## Nächste Schritte

1. ✅ Sensor testen und Schwellenwert einstellen
2. ✅ Kollisionsvermeidung testen
3. ⏭️ Weitere Sensoren hinzufügen (Front, Right)
4. ⏭️ Navigation-Logik erweitern
