# IP-Adresse gefunden!

## Mögliche IP-Adresse: **192.168.0.2**

Im Netzwerk-Diagramm ist "saugbot" sichtbar und in der ARP-Tabelle gibt es eine IP **192.168.0.2** ohne Hostname.

### Status:
- ✅ Ping funktioniert (Gerät antwortet)
- ⚠️ SSH-Verbindung wird abgelehnt

### Mögliche Gründe:
1. SSH ist auf dem Pi nicht aktiviert
2. Es ist ein anderes Gerät (nicht der Pi)
3. Pi läuft, aber SSH-Service ist nicht gestartet

## Lösungen:

### Option 1: Router-Interface prüfen
- Gehe zu: `192.168.0.1` (compalhub.home)
- Suche nach "saugbot" in der Geräteliste
- Dort sollte die korrekte IP-Adresse stehen

### Option 2: Monitor direkt am Pi
- HDMI + Monitor anschließen
- USB-Tastatur anschließen
- Am Pi einloggen: `pi` / `123456789`
- IP anzeigen:
  ```bash
  hostname -I
  ```

### Option 3: SSH auf Pi aktivieren (falls deaktiviert)
Am Pi (mit Monitor):
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

## Nachdem du die IP hast:

```bash
ssh pi@[IP-ADRESSE]
# Password: 123456789
```

Dann Setup-Script ausführen:
```bash
cd ~
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
chmod +x setup_raspi.sh
bash setup_raspi.sh
```
