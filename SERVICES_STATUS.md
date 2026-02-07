# Services Status prüfen

## ✅ Installation erfolgreich!

Die Services sind installiert und aktiviert. Prüfe den Status:

## Status prüfen:

```bash
# Auto-Update Service
sudo systemctl status saugbot-auto-update.service

# Hauptprogramm Service
sudo systemctl status saugbot-main.service

# Web-Interface Service
sudo systemctl status saugbot-web.service
```

## Logs anzeigen:

```bash
# Auto-Update Logs
sudo journalctl -u saugbot-auto-update.service -f

# Hauptprogramm Logs
sudo journalctl -u saugbot-main.service -f

# Web-Interface Logs
sudo journalctl -u saugbot-web.service -f
```

## Wichtig:

Du hast **beide Services** aktiviert (main UND web). Das bedeutet:
- **Beide laufen parallel** (kann zu Konflikten führen)
- **Wähle EINES:**
  - Entweder `saugbot-main.service` (Hauptprogramm)
  - Oder `saugbot-web.service` (Web-Interface)

## Empfehlung:

**Für Entwicklung/Testing: Web-Interface**
```bash
sudo systemctl stop saugbot-main.service
sudo systemctl disable saugbot-main.service
sudo systemctl start saugbot-web.service
```

**Für Produktion: Hauptprogramm**
```bash
sudo systemctl stop saugbot-web.service
sudo systemctl disable saugbot-web.service
sudo systemctl start saugbot-main.service
```

## Was jetzt automatisch passiert:

✅ **Beim Booten:**
- Auto-Update startet automatisch
- Hauptprogramm/Web-Interface startet automatisch

✅ **Während des Betriebs:**
- Auto-Update prüft alle 30 Sekunden auf GitHub-Updates
- Findet Updates automatisch
- Holt sie automatisch
- Startet Programm neu

✅ **Du musst NICHTS mehr machen:**
- Code auf Laptop schreiben
- Push zu GitHub
- Pi übernimmt automatisch!

## Test:

1. **Pi neu starten:**
   ```bash
   sudo reboot
   ```

2. **Nach dem Booten prüfen:**
   ```bash
   sudo systemctl status saugbot-auto-update.service
   sudo systemctl status saugbot-main.service
   ```

3. **Sollten beide "active (running)" zeigen!**
