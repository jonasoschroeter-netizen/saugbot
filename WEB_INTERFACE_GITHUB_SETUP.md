# 🌐 Web-Interface über GitHub aktivieren

## Problem: Raspberry Pi ist verbaut, kann nicht direkt zugreifen

## Lösung: Über GitHub und Auto-Update

### Schritt 1: Dateien auf GitHub pushen

```bash
cd c:\Users\jonas\saugbot
git add .
git commit -m "Web-Interface Service Setup - automatischer Start"
git push origin main
```

### Schritt 2: Auf Raspberry Pi (einmalig per SSH oder wenn möglich)

**Falls du einmalig SSH-Zugriff hast:**

```bash
ssh pi@192.168.0.5
cd ~/saugbot
git pull origin main
chmod +x install_web_service.sh
./install_web_service.sh
```

**Falls Auto-Update bereits läuft:**

Der Raspberry Pi holt automatisch die Updates. Dann musst du nur noch den Service installieren.

### Schritt 3: Service installieren (einmalig)

**Option A: Wenn du SSH-Zugriff hast:**

```bash
ssh pi@192.168.0.5 "cd ~/saugbot && chmod +x install_web_service.sh && ./install_web_service.sh"
```

**Option B: Wenn Auto-Update läuft, aber Service noch nicht installiert:**

Du musst den Service einmalig installieren. Falls das nicht geht, können wir einen Workaround machen:

### Alternative: Auto-Start ohne Service

Falls Service-Installation nicht möglich ist, können wir das Web-Interface über `rc.local` oder `crontab` starten.

## Schritt 4: Prüfen ob es funktioniert

Nach dem Push und Service-Installation:

1. **Warte 30-60 Sekunden** (Auto-Update prüft alle 30 Sekunden)
2. **Teste Verbindung:**
   ```bash
   python test_web_connection.py
   ```
3. **Öffne im Browser:**
   ```
   http://192.168.0.5:5000
   ```

## Automatischer Workflow (nach einmaliger Installation)

1. ✅ **Du codest auf dem Laptop**
2. ✅ **Du pusht zu GitHub:** `git push origin main`
3. ✅ **Raspberry Pi holt automatisch Updates** (alle 30 Sekunden)
4. ✅ **Service startet automatisch neu** (wenn als Service installiert)
5. ✅ **Web-Interface läuft automatisch**

## Service-Befehle (falls du später SSH-Zugriff bekommst)

```bash
# Status prüfen
sudo systemctl status saugbot-web.service

# Neu starten
sudo systemctl restart saugbot-web.service

# Logs anzeigen
sudo journalctl -u saugbot-web.service -f

# Stoppen
sudo systemctl stop saugbot-web.service

# Deaktivieren (startet nicht mehr beim Boot)
sudo systemctl disable saugbot-web.service
```

## Falls Service nicht installiert werden kann

### Alternative 1: Auto-Start über rc.local

Falls Service nicht geht, können wir `rc.local` verwenden:

```bash
# Auf dem Pi (einmalig):
sudo nano /etc/rc.local

# Vor "exit 0" hinzufügen:
cd /home/pi/saugbot
export PYTHONPATH=/home/pi/saugbot
nohup python3 src/web_interface.py > /home/pi/saugbot/logs/web_interface.log 2>&1 &

exit 0
```

### Alternative 2: Crontab @reboot

```bash
# Auf dem Pi:
crontab -e

# Hinzufügen:
@reboot cd /home/pi/saugbot && export PYTHONPATH=/home/pi/saugbot && python3 src/web_interface.py > /home/pi/saugbot/logs/web_interface.log 2>&1 &
```

## Nächste Schritte

1. **Pushe die Dateien zu GitHub**
2. **Warte 30-60 Sekunden**
3. **Teste die Verbindung mit `test_web_connection.py`**
4. **Öffne http://192.168.0.5:5000 im Browser**

Falls es nicht funktioniert, müssen wir den Service einmalig installieren (per SSH oder wenn du Zugriff bekommst).
