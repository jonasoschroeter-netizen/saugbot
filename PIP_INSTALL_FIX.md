# pip3 install Fehler beheben

## Problem:
`error: externally-managed-environment`

Das ist ein Schutz in neueren Python-Versionen.

## Lösung für Raspberry Pi:

### Option 1: Mit --break-system-packages (für RPi.GPIO empfohlen)

```bash
pip3 install -r requirements.txt --break-system-packages
```

**Warum:** RPi.GPIO braucht system-level Zugriff auf GPIO, daher ist system-wide Installation hier okay.

### Option 2: Mit sudo (Alternative)

```bash
sudo pip3 install -r requirements.txt
```

### Option 3: Virtual Environment (nicht empfohlen für GPIO)

Falls du trotzdem ein venv verwenden willst:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Aber:** GPIO-Zugriff könnte dann Probleme machen.

## Empfohlene Lösung:

```bash
pip3 install -r requirements.txt --break-system-packages
```

Das installiert:
- RPi.GPIO (für GPIO-Zugriff)
- python-dotenv (für .env Dateien)
- pytest (optional, für Tests)

## Nach der Installation:

```bash
cd ~/saugbot
python3 src/main.py
```
