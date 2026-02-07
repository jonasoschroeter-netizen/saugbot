# GitHub Setup Instructions for Saugbot

## Initial Setup on Raspberry Pi

**✅ Repository ist bereits auf GitHub:** `git@github.com:jonasoschroeter-netizen/saugbot.git`  
**✅ SSH-Key wurde beim Flashing bereits hinzugefügt**

### 1. SSH to Raspberry Pi

From your laptop:
```bash
ssh pi@saugbot.local
# Password: 123456789
```

### 2. Clone Repository auf Raspberry Pi

```bash
cd ~
git clone git@github.com:jonasoschroeter-netizen/saugbot.git
cd saugbot
```

### 3. Installiere Dependencies

```bash
pip3 install -r requirements.txt
```

### 4. Erstelle .env Datei (Optional)

```bash
cp .env.example .env
# Bearbeite .env falls nötig
```

### 5. Teste SSH-Verbindung zu GitHub (Optional)

```bash
ssh -T git@github.com
# Sollte "Hi jonasoschroeter-netizen! You've successfully authenticated..." anzeigen
```

## Daily Workflow

### Making Changes and Pushing

```bash
# After making changes
git add .
git commit -m "Description of your changes"
git push origin main
```

### Example Commit Messages

```bash
git commit -m "Add collision avoidance logic"
git commit -m "Update GPIO pin assignments in config.py"
git commit -m "Fix ultrasonic sensor timeout handling"
git commit -m "Add side brush control module"
```

## Pulling Latest Changes

If working from multiple locations:

```bash
git pull origin main
```

## Troubleshooting

### If push is rejected:
```bash
# Pull latest changes first
git pull origin main --rebase
# Then push again
git push origin main
```

### If remote already exists with different URL:
```bash
git remote set-url origin git@github.com:jonasoschroeter-netizen/saugbot.git
```

### Check current remote:
```bash
git remote -v
```
