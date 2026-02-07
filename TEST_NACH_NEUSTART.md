# Test nach Neustart - Alles automatisch?

## 🎯 Ziel:
Prüfen ob alles automatisch beim Booten startet.

## Schritt-für-Schritt Test:

### 1. Pi neu starten:

```bash
sudo reboot
```

### 2. Nach dem Booten (warten bis Pi vollständig gebootet ist):

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

```bash
# Web-Interface Service
sudo systemctl status saugbot-web.service
```

**Sollte zeigen:**
- ✅ `Active: active (running)`
- ✅ `Loaded: loaded (...; enabled; ...)`

### 4. Web-Interface testen:

**Vom Laptop aus im Browser:**
- Öffne: `http://192.168.0.5:5000`

**Sollte zeigen:**
- ✅ Web-Interface lädt
- ✅ Sensor-Status wird angezeigt
- ✅ Konfiguration ist sichtbar

### 5. Auto-Update testen:

**Prüfe ob Auto-Update läuft:**
```bash
ps aux | grep auto_update.py
```

**Sollte zeigen:**
- ✅ Python-Prozess läuft

**Prüfe Logs:**
```bash
sudo journalctl -u saugbot-auto-update.service -n 20
```

**Sollte zeigen:**
- ✅ "Saugbot Auto-Update System gestartet"
- ✅ "Prüfe alle 30 Sekunden auf Updates..."

### 6. Test-Update machen:

**Auf dem Laptop:**
```bash
cd C:\Users\jonas\saugbot
# Kleine Änderung machen (z.B. Kommentar in README.md)
echo "# Test Update" >> README.md
git add README.md
git commit -m "Test: Auto-Update prüfen"
git push origin main
```

**Am Pi (nach 30-60 Sekunden):**
```bash
cd ~/saugbot
git log --oneline -1
```

**Sollte zeigen:**
- ✅ Neuester Commit ist "Test: Auto-Update prüfen"
- ✅ Auto-Update hat automatisch geholt!

## ✅ Checkliste - Alles OK wenn:

- [ ] Auto-Update Service: `active (running)`
- [ ] Web-Interface Service: `active (running)`
- [ ] Web-Interface erreichbar: `http://192.168.0.5:5000`
- [ ] Auto-Update Prozess läuft: `ps aux | grep auto_update`
- [ ] Test-Update wurde automatisch geholt

## ❌ Falls etwas nicht funktioniert:

### Service läuft nicht:
```bash
# Logs prüfen
sudo journalctl -u saugbot-web.service -n 50
sudo journalctl -u saugbot-auto-update.service -n 50

# Service manuell starten
sudo systemctl start saugbot-web.service
sudo systemctl start saugbot-auto-update.service
```

### Web-Interface nicht erreichbar:
```bash
# Prüfe ob Port 5000 offen ist
sudo netstat -tlnp | grep 5000

# Prüfe ob Python-Prozess läuft
ps aux | grep web_interface.py
```

### Auto-Update holt keine Updates:
```bash
# Prüfe Logs
sudo journalctl -u saugbot-auto-update.service -f

# Manuell testen
cd ~/saugbot
git fetch origin
git status
```

## 🎉 Erfolg wenn:

✅ **Pi bootet** → Services starten automatisch
✅ **Web-Interface läuft** → Erreichbar im Browser
✅ **Auto-Update läuft** → Prüft regelmäßig auf Updates
✅ **Test-Update geholt** → Automatisch ohne manuelles Eingreifen

**Dann funktioniert alles perfekt!** 🚀
