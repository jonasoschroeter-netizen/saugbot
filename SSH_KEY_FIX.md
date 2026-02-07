# SSH-Key Format-Fehler beheben

## Fehler:
"Key is invalid. You must supply a key in OpenSSH public key format"

## Lösung:

Der Key muss **KOMPLETT in EINER Zeile** sein, ohne Zeilenumbrüche!

### Vollständiger Key (alles in einer Zeile):

```
ssh-ed25519 AAAAC3NzaC11ZDI1NTE5AAAAIFUFdVVKEBWosz1FRtwUpCFPuKZn/JKYWEN+qMsWCwGf saugbot-pi
```

## Wichtig beim Kopieren:

1. ✅ **Alles in einer Zeile** - keine Zeilenumbrüche!
2. ✅ **Keine Leerzeichen** am Anfang oder Ende
3. ✅ **Beginnt mit:** `ssh-ed25519`
4. ✅ **Endet mit:** `saugbot-pi`
5. ✅ **Drei Teile** durch Leerzeichen getrennt:
   - `ssh-ed25519` (Key-Typ)
   - `AAAAC3NzaC11ZDI1NTE5AAAAIFUFdVVKEBWosz1FRtwUpCFPuKZn/JKYWEN+qMsWCwGf` (Key-Daten)
   - `saugbot-pi` (Kommentar)

## Tipp:

1. Markiere den kompletten Key im Terminal
2. Kopiere mit `Ctrl+Shift+C` (oder Rechtsklick → Copy)
3. Füge in GitHub ein mit `Ctrl+V`
4. Prüfe, dass alles in einer Zeile ist

## Falls es immer noch nicht funktioniert:

Am Pi-Terminal den Key nochmal anzeigen:
```bash
cat ~/.ssh/id_ed25519.pub
```

Dann den kompletten Output kopieren.
