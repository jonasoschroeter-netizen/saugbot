# 🔍 Raspberry Pi im neuen WLAN finden

## Wenn du Zugriff auf den Pi hast (Monitor/Tastatur):

### Auf dem Raspberry Pi ausführen:
```bash
# Zeigt die IP-Adresse an
hostname -I

# Oder detaillierter:
ip addr show
```

Die IP-Adresse steht in der Ausgabe (z.B. `192.168.1.105`).

---

## Wenn du KEINEN Zugriff auf den Pi hast:

### Option 1: Hostname versuchen (falls mDNS funktioniert)
```bash
ping saugbot.local
```
Falls das funktioniert, kannst du dich verbinden mit:
```bash
ssh pi@saugbot.local
```

### Option 2: Router prüfen
- Öffne die Router-Oberfläche (meist `192.168.1.1` oder `192.168.0.1`)
- Gehe zu "Verbundene Geräte" / "DHCP Client List" / "LAN"
- Suche nach "saugbot" oder "raspberrypi"

### Option 3: Netzwerk-Scan (von deinem Windows-PC)
```powershell
# Alle Geräte im Netzwerk scannen
arp -a

# Oder mit nmap (falls installiert):
nmap -sn 192.168.1.0/24
```

### Option 4: WLAN-Konfiguration auf der SD-Karte ändern
Falls der Pi sich nicht verbinden kann, musst du die WLAN-Daten auf der SD-Karte anpassen:

1. SD-Karte in den PC stecken
2. In `boot` oder `bootfs` Ordner die Datei `wpa_supplicant.conf` bearbeiten
3. Neues WLAN hinzufügen:
```
country=DE
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="DEIN_NEUES_WLAN_NAME"
    psk="DEIN_WLAN_PASSWORT"
    key_mgmt=WPA-PSK
}
```

---

## Nach dem Finden der IP:

```bash
ssh pi@192.168.x.x
# Password: 123456789
```

## Wichtig für neues WLAN:
Der Hostname `saugbot.local` funktioniert nur, wenn:
- Der Pi im gleichen Netzwerk ist
- mDNS/Bonjour funktioniert (oft auf Windows nicht standardmäßig)

**Tipp:** Notiere die neue IP-Adresse und aktualisiere `IP_192.168.0.5.md` falls du sie gefunden hast!
