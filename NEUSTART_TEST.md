# Neustart-Test: Automatischer Start beim Booten

## 🎯 Ziel:
Prüfen ob alles automatisch beim Booten startet.

## Test-Schritte:

### 1. Pi neu starten:

```bash
sudo reboot
```

### 2. Warten bis Pi vollständig gebootet ist:

**Warte 1-2 Minuten** nach dem Booten, damit:
- Netzwerk verbindet sich
- Services starten
- Auto-Update läuft

### 3. Services Status prüfen:

```bash
# Auto-Update Service
sudo systemctl status saugbot-auto-update.service
```

**Sollte zeigen:**
- ✅ `Active: active (running)`
- ✅ `Loaded: loaded (...; enabled; ...)`
- ✅ Start-Zeit sollte nach dem Booten sein

```bash
# Web-Interface Service
sudo systemctl status saugbot-web.service
```

**Sollte zeigen:**
- ✅ `Active: active (running)`
- ✅ `Loaded: loaded (...; enabled; ...)`
- ✅ Start-Zeit sollte nach dem Booten sein

### 4. Web-Interface testen:

**Vom Laptop aus im Browser:**
- Öffne: `http://192.168.0.5:5000`

**Sollte zeigen:**
- ✅ Web-Interface lädt
- ✅ Sensor-Status wird angezeigt
- ✅ Konfiguration ist sichtbar

### 5. Auto-Update Logs prüfen:

```bash
sudo journalctl -u saugbot-auto-update.service -n 20
```

**Sollte zeigen:**
- ✅ "🚀 Saugbot Auto-Update System gestartet"
- ✅ "⏱️  Prüfe alle 30 Sekunden auf Updates..."
- ✅ Start-Zeit sollte nach dem Booten sein

### 6. Prüfe ob Auto-Update läuft:

```bash
ps aux | grep auto_update
```

**Sollte zeigen:**
- ✅ Python-Prozess läuft

### 7. Prüfe ob Web-Interface läuft:

```bash
ps aux | grep web_interface
```

**Sollte zeigen:**
- ✅ Python-Prozess läuft

## ✅ Checkliste - Alles OK wenn:

- [ ] Auto-Update Service: `active (running)` nach Booten
- [ ] Web-Interface Service: `active (running)` nach Booten
- [ ] Web-Interface erreichbar: `http://192.168.0.5:5000`
- [ ] Auto-Update Prozess läuft: `ps aux | grep auto_update`
- [ ] Web-Interface Prozess läuft: `ps aux | grep web_interface`
- [ ] Logs zeigen Start nach Booten

## ❌ Falls etwas nicht funktioniert:

### Service startet nicht automatisch:
```bash
# Prüfe ob Service enabled ist
sudo systemctl is-enabled saugbot-auto-update.service
sudo systemctl is-enabled saugbot-web.service

# Falls nicht enabled:
sudo systemctl enable saugbot-auto-update.service
sudo systemctl enable saugbot-web.service
```

### Service läuft nicht:
```bash
# Logs prüfen
sudo journalctl -u saugbot-auto-update.service -n 50
sudo journalctl -u saugbot-web.service -n 50

# Manuell starten
sudo systemctl start saugbot-auto-update.service
sudo systemctl start saugbot-web.service
```

## 🎉 Erfolg wenn:

✅ **Pi bootet** → Services starten automatisch
✅ **Web-Interface läuft** → Erreichbar im Browser
✅ **Auto-Update läuft** → Prüft regelmäßig auf Updates
✅ **Alles ohne manuelles Eingreifen!**

**Dann funktioniert der automatische Start perfekt!** 🚀
