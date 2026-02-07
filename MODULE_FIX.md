# ModuleNotFoundError: No module named 'config' - Lösung

## Problem:
`ModuleNotFoundError: No module named 'config'`

Das liegt daran, dass `config.py` im Root-Verzeichnis liegt, aber Python es nicht findet.

## Lösung 1: PYTHONPATH setzen (EINFACHSTE)

Am Pi-Terminal:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/main.py
```

## Lösung 2: Von Root-Verzeichnis aus ausführen

```bash
cd ~/saugbot
python3 -m src.main
```

## Lösung 3: Dauerhaft PYTHONPATH setzen

Füge zu `~/.bashrc` hinzu:

```bash
echo 'export PYTHONPATH=$HOME/saugbot:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

Dann:
```bash
cd ~/saugbot
python3 src/main.py
```

## Lösung 4: Script anpassen (falls nötig)

Falls nichts funktioniert, können wir die Imports in den Python-Dateien anpassen.

## Empfohlene Lösung:

```bash
cd ~/saugbot
export PYTHONPATH=$HOME/saugbot:$PYTHONPATH
python3 src/main.py
```

Das sollte funktionieren!
