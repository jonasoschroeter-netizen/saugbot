# 🚀 SSH schnell aktivieren - Schritt für Schritt

## Voraussetzung: SD-Karte aus Raspberry Pi nehmen

## Methode 1: PowerShell-Script (EINFACHSTE)

1. **SD-Karte in Computer stecken**
2. **PowerShell öffnen** (als Administrator)
3. **Script ausführen:**
   ```powershell
   cd c:\Users\jonas\saugbot
   .\enable_ssh.ps1
   ```
4. **SD-Karte zurück in Raspberry Pi**
5. **Raspberry Pi starten**
6. **Warte 30 Sekunden**
7. **Teste SSH:**
   ```bash
   ssh pi@192.168.0.5
   # Password: 123456789
   ```

## Methode 2: Manuell (falls Script nicht funktioniert)

1. **SD-Karte in Computer stecken**
2. **Datei-Explorer öffnen**
3. **Gehe zum boot-Laufwerk** (z.B. `E:`)
4. **Erstelle leere Datei** namens `ssh`
   - Rechtsklick → Neu → Textdokument
   - Benenne um zu `ssh` (ohne .txt!)
   - Windows warnt - klicke "Ja"
5. **SD-Karte zurück in Raspberry Pi**
6. **Raspberry Pi starten**

## Nach SSH-Aktivierung: Web-Interface starten

```bash
# Verbinde dich per SSH
ssh pi@192.168.0.5

# Installiere Cron-Job (startet Web-Interface alle 5 Minuten)
cd ~/saugbot
git pull
chmod +x install_cron_job.sh
./install_cron_job.sh

# Oder starte Web-Interface manuell
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &
```

## Testen

Nach SSH-Aktivierung und Web-Interface-Start:

```bash
# Auf Windows:
python test_web_connection.py

# Dann Browser öffnen:
http://192.168.0.5:5000
```

## Falls SSH immer noch nicht funktioniert

1. **Prüfe ob Raspberry Pi im gleichen Netzwerk ist**
2. **Prüfe ob Port 22 blockiert ist** (Firewall)
3. **Versuche andere IP-Adresse** (falls sich geändert hat)
4. **Prüfe ob Raspberry Pi läuft** (`ping 192.168.0.5`)
