# 🔧 SSH-Verbindung funktioniert nicht

## Diagnose-Ergebnis

- **Ping:** ✅ Pi ist erreichbar (192.168.37.207)
- **SSH-Port:** ✅ Verbindung wird hergestellt
- **Authentifizierung:** ❌ Permission denied (publickey,password)

## Ursache

SSH lehnt die Anmeldung ab, weil:
1. **Kein SSH-Key** auf dem Pi hinterlegt ist, ODER
2. **Passwort** wird verlangt, aber automatische Skripte können nicht eingeben

## Lösung 1: SSH-Key einrichten (empfohlen)

### Auf deinem Windows-PC (PowerShell):

```powershell
# Prüfen ob du schon einen Key hast
dir $env:USERPROFILE\.ssh\

# Falls KEIN id_ed25519.pub oder id_rsa.pub existiert, neuen Key erstellen:
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\id_ed25519 -N '""'

# Public Key anzeigen (diesen kopieren!)
cat $env:USERPROFILE\.ssh\id_ed25519.pub
```

### Auf dem Raspberry Pi (per Monitor/Tastatur oder bestehende SSH-Session):

```bash
# Ordner erstellen falls nötig
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Key hinzufügen (ersetze INHALT mit dem Output von id_ed25519.pub)
echo "ssh-ed25519 AAAA... dein-key" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Oder: Key kopieren mit ssh-copy-id (wenn du dich mit Passwort verbinden kannst):

```powershell
# Einmalig mit Passwort verbinden - Key wird automatisch kopiert
ssh-copy-id pi@192.168.37.207
# Passwort eingeben: 123456789
```

## Lösung 2: Passwort-Auth prüfen

Falls du dich manuell mit Passwort verbinden kannst:

```bash
ssh pi@192.168.37.207
# Passwort: 123456789
```

Wenn das funktioniert, liegt das Problem nur an der **automatischen** Verbindung (Skripte können kein Passwort eingeben).

## Lösung 3: SSH-Key vom Pi auf deinen PC

Falls du Zugriff auf den Pi hast (Monitor/Tastatur):

```bash
# Auf dem Pi - zeige den authorized_keys Inhalt
cat ~/.ssh/authorized_keys

# Prüfe ob SSH Passwort-Auth erlaubt
sudo grep PasswordAuthentication /etc/ssh/sshd_config
```

## Warum Cursor/AI nicht verbinden kann

Wenn du `ssh pi@saugbot.local` **manuell** in einer Konsole ausführst und das Passwort eingibst, funktioniert es. 

Die automatischen Befehle von Cursor können aber **kein Passwort eingeben** – deshalb schlägt die Verbindung fehl. Mit einem eingerichteten SSH-Key wäre keine Passworteingabe nötig.
