# Raspberry Pi Status-Check

## Aktuelle Situation:
- ✅ Grüne LED hat geblinkt (Pi hat gebootet)
- ⚠️ Jetzt nur noch rote LED (Pi läuft möglicherweise nicht mehr)
- ✅ Originales Raspberry Pi Netzteil wird verwendet

## Was die LEDs bedeuten:

### Rote LED:
- **Immer an** = Power vorhanden (normal)
- **Aus** = Kein Power

### Grüne LED:
- **Blinkt** = Aktivität (Boot, Datenverkehr) - **GUT!**
- **Aus** = Keine Aktivität (Pi läuft, aber keine Daten)
- **Dauerhaft an** = Problem beim Booten

## Mögliche Ursachen für "nur noch rot":

1. **Pi ist abgestürzt/aufgehängt**
   - Lösung: Neustart (Power kurz trennen)

2. **Pi läuft, aber keine Netzwerk-Aktivität**
   - Grüne LED blinkt nur bei Datenverkehr
   - Pi könnte im Idle sein (normal)

3. **SD-Karte Problem**
   - Pi bootet nicht richtig
   - Lösung: SD-Karte prüfen

## Schnell-Check:

### 1. Pi-Neustart
```
- Power kurz trennen (5 Sekunden)
- Wieder anschließen
- Beobachte LEDs:
  * Rote LED sollte sofort an sein
  * Grüne LED sollte beim Booten blinken
```

### 2. IP-Adresse finden (wenn Pi läuft)

**Option A: Router-Interface**
- Öffne Browser: `192.168.0.1` (oder deine Router-IP)
- Login ins Router-Interface
- Suche nach "Connected Devices" / "DHCP Clients"
- Suche nach "raspberrypi" oder "saugbot"

**Option B: Monitor direkt**
- HDMI-Kabel + Monitor anschließen
- USB-Tastatur anschließen
- Am Pi einloggen (User: `pi`, Pass: `123456789`)
- IP anzeigen:
  ```bash
  hostname -I
  ```

**Option C: Netzwerk-Scan**
- Verwende Tools wie "Angry IP Scanner" oder "Advanced IP Scanner"
- Scanne 192.168.0.0/24
- Suche nach Raspberry Pi

### 3. SSH-Verbindung testen

Sobald du die IP-Adresse hast:
```bash
ssh pi@[IP-ADRESSE]
# Password: 123456789
```

## Wenn Pi nicht erreichbar ist:

1. **Power-Cycle:**
   - Power komplett trennen (30 Sekunden)
   - Wieder anschließen
   - Beobachte Boot-Sequenz

2. **SD-Karte prüfen:**
   - Ist sie richtig eingesteckt?
   - Eventuell neu flashen

3. **Monitor anschließen:**
   - Siehst du Boot-Meldungen?
   - Gibt es Fehler?

## Nächste Schritte nach erfolgreicher Verbindung:

```bash
# 1. SSH zum Pi
ssh pi@[IP-ADRESSE]

# 2. Setup-Script ausführen
cd ~
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
chmod +x setup_raspi.sh
bash setup_raspi.sh
```
