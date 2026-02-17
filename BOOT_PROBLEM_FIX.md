# 🔧 Raspberry Pi Boot-Problem: Loading Screen dann weg

## Problem: Loading Screen erscheint, dann schwarzer Bildschirm

## Mögliche Ursachen:

### 1. System bootet, aber HDMI geht aus (HÄUFIGSTE)

**Lösung:** HDMI-Signal erzwingen

Füge zu `config.txt` hinzu:
```
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
hdmi_drive=2
hdmi_ignore_edid=0xa5000080
```

### 2. System stürzt beim Boot ab

**Lösung:** Boot-Logs prüfen

Füge zu `config.txt` hinzu:
```
enable_uart=1
```

Dann kannst du per USB-Serial die Boot-Logs sehen.

### 3. Display-Timeouts

**Lösung:** Bildschirm-Sleep deaktivieren

Füge zu `config.txt` hinzu:
```
hdmi_blanking=0
hdmi_ignore_edid=0xa5000080
```

### 4. Falsche Auflösung

**Lösung:** Safe Mode aktivieren

Füge zu `config.txt` hinzu:
```
hdmi_safe=1
```

## Schnellste Lösung: config.txt komplett anpassen

### Schritt 1: SD-Karte in Computer

### Schritt 2: config.txt öffnen

### Schritt 3: Füge am Ende hinzu:

```
# Boot-Fix
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=82
hdmi_drive=2
hdmi_ignore_edid=0xa5000080
hdmi_blanking=0
enable_uart=1
```

### Schritt 4: Speichere und starte Pi neu

## Alternative: Minimal config.txt

Falls das nicht funktioniert, versuche:

```
hdmi_safe=1
enable_uart=1
```

## Prüfe ob Pi läuft (auch ohne Bildschirm)

Auch wenn der Bildschirm schwarz ist, kann der Pi laufen:

```bash
# Ping testen
ping 192.168.0.5

# Ports prüfen
python check_services.py
```

Falls Ping funktioniert, läuft der Pi - nur der Bildschirm zeigt nichts.

## Debugging: Boot-Logs sehen

### Option 1: USB-Serial

1. **USB-to-Serial Kabel** an Pi anschließen
2. **Putty öffnen** (Windows)
3. **COM-Port wählen** (z.B. COM3)
4. **Baudrate: 115200**
5. **Pi starten** - Logs erscheinen im Terminal

### Option 2: SSH (falls aktiviert)

Falls SSH funktioniert:
```bash
ssh pi@192.168.0.5
dmesg | tail -50
journalctl -b
```

## Häufige Boot-Fehler:

### "Failed to start" Fehler

Prüfe welche Services fehlschlagen:
```bash
systemctl --failed
```

### Speicher-Problem

Prüfe Speicher:
```bash
df -h
```

### SD-Karte-Problem

Prüfe SD-Karte:
```bash
dmesg | grep -i "mmc\|sdcard"
```

## Nach Fix: Web-Interface starten

Sobald der Pi stabil bootet:

```bash
cd ~/saugbot
git pull
chmod +x install_rc_local.sh boot_start_web.sh
./install_rc_local.sh
```

Oder manuell:
```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &
```

## Nächste Schritte:

1. **config.txt anpassen** (siehe oben)
2. **Pi starten**
3. **Prüfe ob Pi läuft** (`ping 192.168.0.5`)
4. **Falls Pi läuft:** SSH aktivieren und Web-Interface starten
