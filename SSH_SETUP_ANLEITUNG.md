# SSH-Key zu GitHub hinzufügen - Anleitung

## Dein SSH-Key:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAx2Au4sTbnrEQOi5hv6xTl7CrSzB+/ds5mN+bIqaRqC saugbot-laptop
```

## Schritte:

1. **Kopiere den kompletten Key oben** (alles in einer Zeile, beginnt mit `ssh-ed25519`)

2. **Gehe zu GitHub SSH Settings:**
   - Öffne: https://github.com/settings/keys
   - Oder: GitHub → Settings → SSH and GPG keys

3. **Klicke auf "New SSH key"**

4. **Fülle das Formular aus:**
   - **Title:** `Saugbot Laptop` (oder ein anderer Name)
   - **Key type:** `Authentication Key` (Standard)
   - **Key:** Füge den kompletten Key ein (alles in einer Zeile)

5. **Klicke auf "Add SSH key"**

6. **Teste die Verbindung:**
   ```bash
   ssh -T git@github.com
   ```
   
   Du solltest sehen: `Hi jonasoschroeter-netizen! You've successfully authenticated...`

## Nach dem Hinzufügen:

Das Repository ist bereits auf SSH konfiguriert. Du kannst jetzt direkt pushen:

```bash
cd C:\Users\jonas\saugbot
git push origin main
```
