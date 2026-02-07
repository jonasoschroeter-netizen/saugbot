# Automatischer Start beim Booten - Quick Setup

## 🎯 Antwort: JA, nach einmaliger Einrichtung!

**Nach dem Setup startet alles automatisch beim Booten!**

## Einmalige Installation am Raspberry Pi:

### 1. Updates holen:
```bash
cd ~/saugbot
git pull origin main
```

### 2. Services installieren:

**Für Hauptprogramm:**
```bash
sudo cp saugbot-auto-update.service /etc/systemd/system/
sudo cp saugbot-main.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable saugbot-auto-update.service
sudo systemctl enable saugbot-main.service
sudo systemctl start saugbot-auto-update.service
sudo systemctl start saugbot-main.service
```

**Für Web-Interface:**
```bash
sudo cp saugbot-auto-update.service /etc/systemd/system/
sudo cp saugbot-web.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable saugbot-auto-update.service
sudo systemctl enable saugbot-web.service
sudo systemctl start saugbot-auto-update.service
sudo systemctl start saugbot-web.service
```

## ✅ Fertig!

**Jetzt beim Booten:**
1. ✅ Pi startet
2. ✅ Auto-Update startet automatisch
3. ✅ Hauptprogramm/Web-Interface startet automatisch
4. ✅ Alles läuft ohne manuelles Eingreifen!

## Danach:

- **Pi ausschalten** → OK
- **Pi einschalten** → Alles startet automatisch! 🚀
- **Du codest auf Laptop** → Push zu GitHub
- **Pi holt Updates automatisch** → Kein Eingreifen nötig!
