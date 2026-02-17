# 🔄 Lösung nach Neustart

## Nach dem Neustart

Das Auto-Update-System sollte jetzt:
1. ✅ Beim Boot automatisch starten (falls als Service installiert)
2. ✅ Die neuesten Updates holen
3. ✅ Das Boot-Script in rc.local installieren
4. ✅ Das Web-Interface starten

## Was passiert beim nächsten Neustart:

1. **Raspberry Pi bootet**
2. **rc.local wird ausgeführt** (falls Boot-Script installiert)
3. **boot_start_web.sh wird ausgeführt**
4. **Web-Interface startet automatisch**

## Testen:

**Warte 1-2 Minuten** nach dem Neustart, dann:

```bash
python test_web_connection.py
```

Falls es funktioniert:
```
http://192.168.0.5:5000
```

## Falls es immer noch nicht funktioniert:

Das Problem ist wahrscheinlich, dass:
1. **Auto-Update läuft nicht** beim Boot
2. **rc.local benötigt sudo** (kann nicht automatisch installiert werden)
3. **Boot-Script hat einen Fehler**

## Lösung: Einmalig SSH aktivieren

Falls du einmalig Zugriff bekommst (z.B. SD-Karte):

1. **SSH aktivieren** (siehe `SSH_AKTIVIEREN_OHNE_BILDSCHIRM.md`)
2. **Boot-Script installieren:**
   ```bash
   ssh pi@192.168.0.5
   cd ~/saugbot
   git pull
   chmod +x install_rc_local.sh boot_start_web.sh
   ./install_rc_local.sh
   ```
3. **Oder Web-Interface manuell starten:**
   ```bash
   ssh pi@192.168.0.5 "cd ~/saugbot && export PYTHONPATH=\$HOME/saugbot:\$PYTHONPATH && nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &"
   ```

## Alternative: Sensoren direkt testen

Falls Web-Interface nicht funktioniert, teste Sensoren direkt:

```bash
ssh pi@192.168.0.5 "cd ~/saugbot && export PYTHONPATH=\$HOME/saugbot:\$PYTHONPATH && python3 src/test_all_sensors.py"
```

Zeigt alle 3 Sensoren im Terminal an.
