# Web-Interface dauerhaft starten

## Option 1: Systemd (empfohlen – startet beim Boot)

Auf dem Pi ausführen:

```bash
cd ~/saugbot
git pull
chmod +x create_autostart_file.sh
./create_autostart_file.sh
```

Damit wird ein Systemd-User-Service eingerichtet. Das Web-Interface startet automatisch beim Boot und wird bei Absturz neu gestartet.

**Prüfen:**
```bash
systemctl --user status saugbot-web
```

**Im Browser:** http://saugbot.local:5000 oder http://192.168.37.207:5000

---

## Option 2: Manuell im Hintergrund

```bash
cd ~/saugbot
git pull
mkdir -p logs
pkill -f web_interface
nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &
```

Läuft bis zum nächsten Neustart.

---

## Option 3: Sofort starten (ohne Boot)

```bash
cd ~/saugbot
git pull
./create_autostart_file.sh
```

Startet den Service sofort und aktiviert ihn für zukünftige Boots.
