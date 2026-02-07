# Setup manuell fortsetzen

## Problem:
Enter drücken erstellt nur eine neue Zeile - das Script wartet auf Eingabe.

## Lösung: Setup manuell fortsetzen

Am Pi-Terminal, führe diese Befehle aus:

### 1. Prüfe ob Repository bereits geklont ist:

```bash
ls -la ~/saugbot
```

Falls das Verzeichnis existiert, ist das Repository bereits geklont.

### 2. Falls nicht geklont, klone manuell:

```bash
cd ~
git clone git@github.com:jonasoschroeter-netizen/saugbot.git
```

### 3. Teste GitHub SSH-Verbindung:

```bash
ssh -T git@github.com
```

Sollte zeigen: "Hi jonasoschroeter-netizen! You've successfully authenticated..."

### 4. Gehe ins Repository:

```bash
cd ~/saugbot
```

### 5. Installiere Dependencies:

```bash
pip3 install -r requirements.txt
```

### 6. Erstelle .env Datei:

```bash
cp .env.example .env
```

### 7. Prüfe GPIO Berechtigungen:

```bash
groups
```

Falls `gpio` nicht in der Liste ist:
```bash
sudo usermod -a -G gpio pi
```

Dann neu einloggen (oder `newgrp gpio`).

## Nach dem Setup:

```bash
cd ~/saugbot
python3 src/main.py
```
