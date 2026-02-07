# Raspberry Pi Setup Checkliste für Saugbot

## ✅ Was bereits erledigt ist:
- Raspberry Pi OS installiert
- SSH beim Flashing eingerichtet
- Hostname: `saugbot.local`
- User: `pi`, Password: `123456789`

## 📋 Was noch zu tun ist:

### 1. Git installieren (falls nicht vorhanden)

```bash
# SSH zum Raspberry Pi
ssh pi@saugbot.local

# Prüfe ob Git installiert ist
git --version

# Falls nicht installiert:
sudo apt update
sudo apt install git -y
```

### 2. SSH-Key zu GitHub hinzufügen (falls noch nicht geschehen)

```bash
# Prüfe ob SSH-Key existiert
ls -la ~/.ssh/

# Falls kein Key vorhanden, erstelle einen:
ssh-keygen -t ed25519 -C "saugbot-pi"
cat ~/.ssh/id_ed25519.pub

# Kopiere den Output und füge ihn zu GitHub hinzu:
# https://github.com/settings/keys
```

**Hinweis:** Wenn SSH beim Flashing bereits eingerichtet wurde, sollte der Key bereits existieren. Prüfe einfach mit `cat ~/.ssh/id_ed25519.pub`

### 3. Repository klonen

```bash
cd ~
git clone git@github.com:jonasoschroeter-netizen/saugbot.git
cd saugbot
```

### 4. Python Dependencies installieren

```bash
# Prüfe Python Version (sollte 3.x sein)
python3 --version

# Installiere pip falls nötig
sudo apt install python3-pip -y

# Installiere Projekt-Dependencies
pip3 install -r requirements.txt
```

### 5. .env Datei erstellen (optional)

```bash
cp .env.example .env
# Bearbeite .env falls nötig
nano .env
```

### 6. GPIO Berechtigungen prüfen

```bash
# Prüfe ob User in gpio Gruppe ist
groups

# Falls nicht, füge User hinzu (normalerweise nicht nötig bei Standard-Installation)
sudo usermod -a -G gpio pi
# Dann neu einloggen
```

### 7. Test der Komponenten

```bash
# Teste Motor Control (VORSICHT: Motoren werden sich bewegen!)
python3 src/motor_control.py

# Teste Ultraschall-Sensoren
python3 src/ultrasonic_sensor.py

# Teste Side Brush
python3 src/side_brush.py
```

## 🚀 Hauptprogramm starten

```bash
python3 src/main.py
```

## 📝 Git Workflow auf dem Pi

```bash
# Änderungen hinzufügen
git add .

# Commit erstellen
git commit -m "Beschreibung der Änderungen"

# Zu GitHub pushen
git push origin main

# Neueste Änderungen vom Laptop holen
git pull origin main
```

## ⚠️ Wichtige Hinweise

1. **GPIO Pins prüfen:** Stelle sicher, dass die Pin-Zuweisungen in `config.py` mit deiner Hardware übereinstimmen
2. **Power Supply:** Stelle sicher, dass der Buck Converter korrekt auf 5.1V eingestellt ist
3. **Level Shifter:** Die HC-SR04 Sensoren benötigen den Level Shifter für 3.3V/5V Konvertierung
4. **LiDAR:** RPLIDAR C1 ist noch nicht implementiert (kommt später)

## 🔧 Troubleshooting

### Git funktioniert nicht:
```bash
# Prüfe SSH-Verbindung
ssh -T git@github.com

# Falls Fehler, prüfe SSH-Key
cat ~/.ssh/id_ed25519.pub
```

### Python Module nicht gefunden:
```bash
# Installiere fehlende Module
pip3 install RPi.GPIO python-dotenv
```

### GPIO Permission Denied:
```bash
# Füge User zu gpio Gruppe hinzu
sudo usermod -a -G gpio pi
# Neu einloggen erforderlich
```
