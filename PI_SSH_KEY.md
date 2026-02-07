# Raspberry Pi SSH-Key zu GitHub hinzufügen

## SSH-Key vom Raspberry Pi:

```
ssh-ed25519 AAAAC3NzaC11ZDI1NTE5AAAAIFUFdVVKEBWosz1FRtwUpCFPuKZn/JKYWEN+qMsWCwGf saugbot-pi
```

## Schritte:

1. **Öffne GitHub SSH Settings:**
   - Gehe zu: https://github.com/settings/keys
   - Oder: GitHub → Settings → SSH and GPG keys

2. **Klicke auf "New SSH key"**

3. **Fülle das Formular aus:**
   - **Title:** `Saugbot Raspberry Pi` (oder ein anderer Name)
   - **Key type:** `Authentication Key` (Standard)
   - **Key:** Füge den kompletten Key ein:
     ```
     ssh-ed25519 AAAAC3NzaC11ZDI1NTE5AAAAIFUFdVVKEBWosz1FRtwUpCFPuKZn/JKYWEN+qMsWCwGf saugbot-pi
     ```
     **Wichtig:** Alles in einer Zeile kopieren!

4. **Klicke auf "Add SSH key"**

5. **Am Pi-Terminal:**
   - Drücke **Enter** um fortzufahren
   - Das Script testet dann die GitHub-Verbindung

## Nach dem Hinzufügen:

Das Setup-Script führt automatisch weiter:
- ✅ GitHub Verbindung testen
- ✅ Repository klonen
- ✅ Dependencies installieren
- ✅ .env Datei erstellen
- ✅ GPIO Berechtigungen prüfen
