# Automatischer Start beim Booten - Setup

## 🎯 Ziel:
**Raspberry Pi startet automatisch beim Booten - du musst NICHTS mehr machen!**

## Installation (EINMALIG):

### 1. Service-Dateien kopieren:

Am Raspberry Pi:

```bash
cd ~/saugbot
git pull origin main  # Falls noch nicht gemacht
```

### 2. Services installieren:

**Option A: Auto-Update + Hauptprogramm (empfohlen):**

```bash
# Auto-Update Service
sudo cp saugbot-auto-update.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable saugbot-auto-update.service

# Hauptprogramm Service
sudo cp saugbot-main.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable saugbot-main.service
```

**Option B: Auto-Update + Web-Interface:**

```bash
# Auto-Update Service
sudo cp saugbot-auto-update.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable saugbot-auto-update.service

# Web-Interface Service
sudo cp saugbot-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable saugbot-web.service
```

### 3. Services starten:

```bash
# Auto-Update starten
sudo systemctl start saugbot-auto-update.service

# Hauptprogramm ODER Web-Interface starten
sudo systemctl start saugbot-main.service
# ODER
sudo systemctl start saugbot-web.service
```

### 4. Status prüfen:

```bash
# Status aller Services
sudo systemctl status saugbot-auto-update.service
sudo systemctl status saugbot-main.service
# ODER
sudo systemctl status saugbot-web.service
```

## ✅ Fertig!

**Jetzt passiert beim Booten automatisch:**
1. ✅ Pi bootet
2. ✅ Netzwerk verbindet sich
3. ✅ Auto-Update Service startet
4. ✅ Hauptprogramm/Web-Interface startet
5. ✅ Auto-Update prüft regelmäßig auf GitHub-Updates

## Verwendung:

### Services verwalten:

```bash
# Services starten
sudo systemctl start saugbot-auto-update.service
sudo systemctl start saugbot-main.service

# Services stoppen
sudo systemctl stop saugbot-main.service
sudo systemctl stop saugbot-auto-update.service

# Services neu starten
sudo systemctl restart saugbot-main.service

# Status prüfen
sudo systemctl status saugbot-main.service

# Logs anzeigen
sudo journalctl -u saugbot-main.service -f
sudo journalctl -u saugbot-auto-update.service -f
```

### Services deaktivieren (falls nötig):

```bash
sudo systemctl disable saugbot-main.service
sudo systemctl disable saugbot-auto-update.service
```

## Workflow (danach):

### Auf dem Laptop:
1. Code schreiben
2. `git add .`
3. `git commit -m "Beschreibung"`
4. `git push origin main`

### Auf dem Raspberry Pi:
**ABSOLUT NICHTS!** 🎉

- Pi bootet automatisch
- Services starten automatisch
- Auto-Update prüft automatisch
- Updates werden automatisch geholt
- Programm startet automatisch neu

## Wichtig:

- **Einmalig einrichten** - dann läuft alles automatisch
- **Pi kann ausgeschaltet werden** - beim Einschalten startet alles automatisch
- **Kein manuelles Eingreifen mehr nötig**

## Troubleshooting:

### Service startet nicht:
```bash
# Logs prüfen
sudo journalctl -u saugbot-main.service -n 50

# Service neu laden
sudo systemctl daemon-reload
sudo systemctl restart saugbot-main.service
```

### Service läuft nicht:
```bash
# Status prüfen
sudo systemctl status saugbot-main.service

# Manuell testen
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/main.py
```
