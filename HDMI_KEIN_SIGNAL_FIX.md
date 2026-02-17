# 🔧 HDMI kein Signal - Lösung

## Problem: Bildschirm zeigt kein Signal vom Raspberry Pi

## Häufige Ursachen und Lösungen:

### 1. Falsche HDMI-Einstellungen (HÄUFIGSTE URSACHE)

**Lösung: SD-Karte konfigurieren**

1. **SD-Karte aus Raspberry Pi nehmen**
2. **SD-Karte in Computer stecken**
3. **Öffne `config.txt` im boot-Verzeichnis**
4. **Füge am Ende hinzu:**

```
# HDMI Force
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
hdmi_drive=2
config_hdmi_boost=4
```

**Oder für 1080p:**
```
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
hdmi_drive=2
```

**Oder für 4K:**
```
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_drive=2
hdmi_cvt=3840 2160 60 6 0 0 0
```

5. **Speichere und starte Pi neu**

### 2. Falscher HDMI-Port (Raspberry Pi 4)

**Raspberry Pi 4 hat 2 HDMI-Ports:**
- **HDMI 0** (näher am USB-C)
- **HDMI 1** (weiter weg)

**Lösung:** Versuche beide Ports!

### 3. Stromversorgung

**Problem:** Pi hat nicht genug Strom

**Lösung:**
- Verwende originales Netzteil (mindestens 5V, 3A)
- Prüfe ob rote LED leuchtet (Power)
- Prüfe ob grüne LED blinkt (SD-Karte wird gelesen)

### 4. SD-Karte-Problem

**Problem:** SD-Karte ist defekt oder nicht richtig formatiert

**Lösung:**
- Prüfe ob grüne LED blinkt (zeigt SD-Karten-Aktivität)
- Versuche andere SD-Karte
- Formatiere SD-Karte neu und installiere Raspberry Pi OS neu

### 5. HDMI-Kabel-Problem

**Lösung:**
- Versuche anderes HDMI-Kabel
- Prüfe ob Kabel funktioniert (mit anderem Gerät testen)

### 6. Bildschirm-Problem

**Lösung:**
- Versuche anderen Bildschirm
- Prüfe ob Bildschirm funktioniert (mit anderem Gerät testen)

## Schnellste Lösung: config.txt anpassen

### Schritt 1: SD-Karte in Computer

### Schritt 2: config.txt öffnen

**Im boot-Verzeichnis der SD-Karte**

### Schritt 3: Füge hinzu (am Ende der Datei):

```
# HDMI Fix
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
hdmi_drive=2
config_hdmi_boost=4
```

### Schritt 4: Speichere und starte Pi neu

## Alternative: Minimal config.txt

Falls das nicht funktioniert, versuche:

```
hdmi_safe=1
```

Dies aktiviert den "Safe Mode" für HDMI.

## Debugging: Prüfe ob Pi läuft

Auch wenn kein Bildschirm-Signal ist, kannst du prüfen ob der Pi läuft:

```bash
# Ping testen
ping 192.168.0.5

# Ports prüfen
python check_services.py
```

Falls Ping funktioniert, läuft der Pi - nur HDMI funktioniert nicht.

## Nach HDMI-Fix: Web-Interface starten

Sobald du Bildschirm-Signal hast:

1. **Öffne Terminal auf dem Pi**
2. **Führe aus:**
   ```bash
   cd ~/saugbot
   git pull
   chmod +x install_rc_local.sh boot_start_web.sh
   ./install_rc_local.sh
   ```

Oder starte Web-Interface manuell:
```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &
```

## Nächste Schritte:

1. **SD-Karte in Computer stecken**
2. **config.txt anpassen** (siehe oben)
3. **SD-Karte zurück in Pi**
4. **Pi starten**
5. **Bildschirm sollte jetzt Signal zeigen**

Falls es immer noch nicht funktioniert, prüfe:
- Stromversorgung (rote LED leuchtet?)
- SD-Karte (grüne LED blinkt?)
- HDMI-Kabel (funktioniert mit anderem Gerät?)
