# WLAN am Raspberry Pi verbinden

## Problem:
- `wlan0` zeigt `NO-CARRIER, DOWN`
- Keine Internetverbindung
- `wget` schlägt fehl

## Lösung: WLAN aktivieren und verbinden

### Option 1: WLAN mit `raspi-config` konfigurieren

```bash
sudo raspi-config
```

Dann:
1. Gehe zu: **"System Options"** → **"Wireless LAN"**
2. Wähle dein WLAN-Netzwerk (SSID: `KabelBox-43D8`)
3. Gebe das WLAN-Passwort ein
4. Speichere und beende

### Option 2: WLAN manuell mit `nmcli` (falls NetworkManager installiert)

```bash
sudo nmcli device wifi list
```

```bash
sudo nmcli device wifi connect "KabelBox-43D8" password "DEIN_WLAN_PASSWORT"
```

### Option 3: WLAN mit `wpa_supplicant` konfigurieren

```bash
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
```

Füge am Ende hinzu:
```
network={
    ssid="KabelBox-43D8"
    psk="DEIN_WLAN_PASSWORT"
}
```

Dann:
```bash
sudo wpa_cli -i wlan0 reconfigure
```

Oder Pi neu starten:
```bash
sudo reboot
```

### Option 4: WLAN-Status prüfen

```bash
sudo iwconfig wlan0
```

```bash
sudo iwlist wlan0 scan | grep -i "KabelBox"
```

## Nach WLAN-Verbindung:

Prüfe ob WLAN verbunden ist:
```bash
ip addr show wlan0
```

Sollte zeigen: `inet 192.168.0.5` (oder ähnlich)

Dann Setup-Script ausführen:
```bash
cd ~
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
chmod +x setup_raspi.sh
bash setup_raspi.sh
```

## Falls WLAN-Passwort nicht bekannt:

- Prüfe Router-Interface
- Oder Router-Aufkleber
- SSID: `KabelBox-43D8` (5 GHz)
