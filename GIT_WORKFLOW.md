# Git Workflow - Wie funktioniert es?

## Aktueller Workflow (MANUELL):

### 1. Änderungen auf Laptop machen:
```bash
# Dateien bearbeiten
git add .
git commit -m "Beschreibung"
git push origin main
```

### 2. Änderungen auf Raspberry Pi holen (MANUELL):
```bash
cd ~/saugbot
git pull origin main
```

**WICHTIG:** Der Pi holt Änderungen NICHT automatisch! Du musst `git pull` manuell ausführen.

## Automatische Lösung (OPTIONAL):

Falls du möchtest, dass der Pi automatisch aktualisiert wird, gibt es mehrere Möglichkeiten:

### Option 1: Cron Job (prüft regelmäßig)

Am Pi:
```bash
crontab -e
```

Füge hinzu (prüft alle 5 Minuten):
```
*/5 * * * * cd /home/pi/saugbot && git pull origin main > /dev/null 2>&1
```

### Option 2: Webhook (sofort bei Push)

1. GitHub Webhook einrichten
2. Python-Script auf Pi, das auf Webhook hört
3. Automatisch `git pull` ausführen

### Option 3: Systemd Service (prüft beim Start)

Service erstellen, der beim Booten prüft.

## Empfehlung:

**Für Entwicklung:** Manuell `git pull` ist besser, weil:
- Du kontrollierst, wann aktualisiert wird
- Du siehst, was geändert wurde
- Keine unerwarteten Updates während Tests

**Für Produktion:** Automatische Updates können sinnvoll sein.

## Aktueller Stand:

- ✅ Du machst Änderungen auf Laptop
- ✅ Du pusht zu GitHub
- ⚠️ **Du musst am Pi `git pull` ausführen** (nicht automatisch!)

## Schneller Workflow:

**Laptop:**
```bash
git add .
git commit -m "Änderung"
git push origin main
```

**Raspberry Pi (SSH oder Terminal):**
```bash
cd ~/saugbot
git pull origin main
# Programm neu starten falls nötig
```
