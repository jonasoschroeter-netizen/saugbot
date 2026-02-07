# SSH-Verbindung Problem lösen

## Problem:
SSH ist aktiviert, aber Verbindung schlägt fehl (Connection timed out).

## Prüfungen am Pi (im Terminal):

### 1. Prüfe ob SSH auf Port 22 hört:

```bash
sudo netstat -tlnp | grep :22
```

Oder:
```bash
sudo ss -tlnp | grep :22
```

Sollte zeigen: `0.0.0.0:22` oder `:::22`

### 2. Prüfe SSH-Konfiguration:

```bash
sudo nano /etc/ssh/sshd_config
```

Suche nach:
- `ListenAddress` - sollte auskommentiert sein oder `0.0.0.0`
- `Port 22` - sollte aktiv sein
- `PermitRootLogin` - kann `yes` oder `no` sein (nicht relevant für pi user)

Drücke `Ctrl+X`, dann `Y`, dann `Enter` zum Speichern.

### 3. SSH-Service neu starten:

```bash
sudo systemctl restart ssh
sudo systemctl status ssh
```

### 4. Firewall prüfen:

```bash
sudo ufw status
```

Falls aktiv, Port 22 öffnen:
```bash
sudo ufw allow 22
```

### 5. IP-Adresse prüfen:

```bash
hostname -I
```

Sollte `192.168.0.5` zeigen.

### 6. Ping-Test vom Laptop:

Vom Laptop aus (in PowerShell):
```powershell
ping 192.168.0.5
```

Sollte Antworten geben.

## Alternative: Direkt am Pi arbeiten

Falls SSH-Verbindung nicht funktioniert, kannst du alles direkt am Pi machen:

```bash
cd ~
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
chmod +x setup_raspi.sh
bash setup_raspi.sh
```

Das Setup-Script funktioniert auch direkt am Pi!
