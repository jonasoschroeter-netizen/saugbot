# SSH am Raspberry Pi aktivieren - Schritt für Schritt

## Hardware anschließen:

1. ✅ **HDMI-Kabel** vom Pi zum Monitor/TV
2. ✅ **USB-Tastatur** anschließen
3. ✅ **Power** am Pi anschließen (falls noch nicht)

## Am Pi einloggen:

1. Pi bootet (grüne LED sollte blinken)
2. Du siehst ein Login-Prompt
3. **User:** `pi`
4. **Password:** `123456789`
   - *Hinweis: Beim Tippen siehst du nichts (normal bei Linux)*

## SSH aktivieren:

Nach dem Login, führe diese Befehle aus (einer nach dem anderen):

```bash
sudo systemctl enable ssh
```

```bash
sudo systemctl start ssh
```

```bash
sudo systemctl status ssh
```

Die letzte Zeile sollte zeigen: **"active (running)"** in grün.

## IP-Adresse prüfen:

```bash
hostname -I
```

Sollte zeigen: **192.168.0.5**

## Test von deinem Laptop:

Jetzt kannst du vom Laptop aus verbinden:

```bash
ssh pi@192.168.0.5
# Password: 123456789
```

## Setup-Script ausführen:

Nach erfolgreicher SSH-Verbindung:

```bash
cd ~
wget https://raw.githubusercontent.com/jonasoschroeter-netizen/saugbot/main/setup_raspi.sh
chmod +x setup_raspi.sh
bash setup_raspi.sh
```

Das Script führt automatisch alle Setup-Schritte aus!

## Falls Probleme:

- **"Permission denied"** → Password falsch, nochmal versuchen
- **SSH startet nicht** → Prüfe mit `sudo systemctl status ssh`
- **IP nicht gefunden** → Prüfe mit `hostname -I`
