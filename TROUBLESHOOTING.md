# Troubleshooting Guide für Saugbot

## 🔴 Problem: Rote LED am Raspberry Pi

Eine **rote LED** am Raspberry Pi bedeutet normalerweise ein **Power-Problem**:

### Mögliche Ursachen:
1. **Zu wenig Strom** - Der Pi bekommt nicht genug Power
2. **Falsche Spannung** - Buck Converter nicht richtig eingestellt
3. **Defektes Netzteil/Kabel**
4. **Zu hoher Stromverbrauch** - Peripherie zieht zu viel Strom

### Lösungen:

#### 1. Power Supply prüfen
- **Buck Converter** sollte auf **5.1V** eingestellt sein (nicht höher!)
- **Strom:** Mindestens **3A** bei 5V (Raspberry Pi 4 braucht viel Strom)
- **Kabel:** Verwende ein dickes USB-C Kabel (kurz, gute Qualität)

#### 2. Messen mit Multimeter
```
- Spannung am USB-C Port messen (sollte 5.0-5.1V sein)
- Unter Last messen (wenn Pi läuft)
- Spannung sollte nicht unter 4.75V fallen
```

#### 3. Peripherie trennen
- **Alle GPIO-Verbindungen trennen** (Motoren, Sensoren)
- Nur Pi mit Power verbinden
- Prüfe ob Pi dann bootet (grüne LED sollte blinken)

#### 4. Boot-Problem
- **SD-Karte prüfen:** Ist sie korrekt eingesteckt?
- **SD-Karte formatieren:** Falls korrupt, neu flashen
- **Andere SD-Karte testen**

### Normale LED-Zustände:
- **Rote LED:** Power vorhanden (sollte immer an sein)
- **Grüne LED:** Aktivität (sollte beim Booten blinken)
- **Beide aus:** Kein Power oder defekt

## 📡 IP-Adresse finden

### Methode 1: Router Web-Interface
1. Öffne Router-Webinterface (meist `192.168.1.1` oder `192.168.0.1`)
2. Suche nach "Connected Devices" oder "DHCP Clients"
3. Suche nach "raspberrypi" oder "saugbot"

### Methode 2: Netzwerk-Scan (Windows)
```powershell
# In PowerShell auf dem Laptop:
arp -a | findstr "192.168"
```

### Methode 3: Angry IP Scanner
- Download: https://angryip.org/
- Scanne dein Netzwerk (z.B. 192.168.1.0/24)
- Suche nach Raspberry Pi

### Methode 4: mDNS (falls aktiviert)
```bash
# Auf Windows mit WSL oder Git Bash:
ping saugbot.local
```

### Methode 5: Monitor + Tastatur direkt am Pi
```bash
# Am Pi eingeloggt:
hostname -I
# Oder:
ip addr show
```

## ✅ Was du noch brauchst - Checkliste

### Hardware (bereits vorhanden):
- ✅ Raspberry Pi 4 (4GB)
- ✅ SD-Karte mit OS
- ✅ 2x DC Motoren (L298N Driver)
- ✅ 3x HC-SR04 Ultraschall-Sensoren
- ✅ Level Shifter (3.3V <-> 5V)
- ✅ N20 Side Brush
- ✅ Relay für Side Brush
- ✅ 14V Battery
- ✅ Buck Converter
- ⏳ RPLIDAR C1 (noch in Transit)

### Software/Setup:
- ✅ GitHub Repository erstellt
- ✅ Code auf GitHub hochgeladen
- ⏳ Raspberry Pi bootet (rotes LED Problem lösen)
- ⏳ IP-Adresse finden
- ⏳ SSH-Verbindung herstellen
- ⏳ Repository auf Pi klonen
- ⏳ Dependencies installieren

### Zusätzlich benötigt (optional):
- **Multimeter** - Zum Messen der Spannung
- **Monitor + HDMI-Kabel** - Für direkten Zugriff am Pi
- **USB-Tastatur** - Falls Monitor verwendet wird
- **Netzwerk-Kabel** - Falls WLAN Probleme macht

## 🔧 Nächste Schritte

1. **Power-Problem lösen:**
   - Buck Converter auf 5.1V prüfen
   - Stromversorgung messen
   - Peripherie trennen und testen

2. **IP-Adresse finden:**
   - Router-Interface prüfen
   - Netzwerk-Scan durchführen
   - Oder Monitor direkt anschließen

3. **SSH-Verbindung testen:**
   ```bash
   ssh pi@[IP-ADRESSE]
   # Password: 123456789
   ```

4. **Setup-Script ausführen:**
   ```bash
   cd ~
   wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
   chmod +x setup_raspi.sh
   bash setup_raspi.sh
   ```

## 🆘 Wenn nichts funktioniert

### Fallback: Direkter Zugriff
1. **Monitor + HDMI** an Pi anschließen
2. **USB-Tastatur** anschließen
3. **Direkt am Pi einloggen:**
   - User: `pi`
   - Password: `123456789`
4. **IP-Adresse anzeigen:**
   ```bash
   hostname -I
   ```
5. **Von dort aus weiterarbeiten**
