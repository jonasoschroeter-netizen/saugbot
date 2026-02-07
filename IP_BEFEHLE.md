# IP-Adresse am Raspberry Pi finden - Alternative Befehle

## Problem:
`hostname -I` gibt keine Ausgabe (schwarze Zeile).

## Alternative Befehle:

### 1. IP-Adresse mit `ip` Befehl:

```bash
ip addr show
```

Oder kürzer:
```bash
ip a
```

Suche nach der Zeile mit `inet 192.168.0.5` (oder ähnlich).

### 2. IP-Adresse mit `ifconfig` (falls installiert):

```bash
ifconfig
```

Oder nur WLAN:
```bash
ifconfig wlan0
```

### 3. IP-Adresse aus Router-Info:

Du weißt bereits aus dem Router-Interface:
- **IP-Adresse: 192.168.0.5** ✅

Das ist die korrekte IP-Adresse!

## Wichtig:

Die IP-Adresse ist: **192.168.0.5**

Du kannst direkt mit dem Setup fortfahren, auch wenn `hostname -I` nichts zeigt.

## Setup ausführen:

```bash
cd ~
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
chmod +x setup_raspi.sh
bash setup_raspi.sh
```
