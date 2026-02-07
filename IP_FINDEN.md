# IP-Adresse des Raspberry Pis finden

## Router-Login (falls du die Daten hast)

### Standard Router-Login-Daten (häufig):
- **Benutzername:** `admin` oder `Administrator` oder leer lassen
- **Kennwort:** `admin` oder `password` oder leer lassen
- **Oder:** Steht auf einem Aufkleber am Router

### Falls du die Router-Daten nicht hast:
→ **Überspringe den Router** und nutze die anderen Methoden unten!

## Alternative Methoden (OHNE Router-Login):

### Methode 1: Monitor direkt am Pi (EINFACHSTE METHODE)

1. **HDMI-Kabel** vom Pi zum Monitor/TV
2. **USB-Tastatur** anschließen
3. Am Pi einloggen:
   - User: `pi`
   - Password: `123456789`
4. IP-Adresse anzeigen:
   ```bash
   hostname -I
   ```
   Oder:
   ```bash
   ip addr show | grep "inet "
   ```

### Methode 2: Netzwerk-Scan Tool (Windows)

**Angry IP Scanner** (kostenlos):
1. Download: https://angryip.org/download/
2. Installieren
3. Scanne: `192.168.0.1` bis `192.168.0.254`
4. Suche nach "raspberrypi" oder "saugbot" in der Liste

**Advanced IP Scanner** (auch kostenlos):
1. Download: https://www.advanced-ip-scanner.com/
2. Installieren
3. Scanne dein Netzwerk
4. Suche nach Raspberry Pi

### Methode 3: PowerShell-Scan (auf diesem Laptop)

Führe diesen Befehl aus (kann etwas dauern):
```powershell
1..254 | ForEach-Object {
    $ip = "192.168.0.$_"
    $result = Test-Connection -ComputerName $ip -Count 1 -Quiet -ErrorAction SilentlyContinue
    if ($result) {
        Write-Host "Erreichbar: $ip"
        try {
            $hostname = [System.Net.Dns]::GetHostEntry($ip).HostName
            Write-Host "  Hostname: $hostname"
        } catch {}
    }
}
```

### Methode 4: mDNS / Bonjour (falls aktiviert)

```bash
# In PowerShell oder CMD:
ping saugbot.local
```

Falls das funktioniert, zeigt es die IP-Adresse.

## Nachdem du die IP hast:

```bash
ssh pi@[IP-ADRESSE]
# Password: 123456789
```

## Schnellste Lösung:

**Monitor + HDMI + Tastatur** ist am schnellsten:
- Direkt am Pi: `hostname -I`
- Fertig! 🎯
