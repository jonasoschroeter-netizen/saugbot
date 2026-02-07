# Router Session-Problem lösen

## Fehler: "Web GUI support a single session only"

Dieser Fehler bedeutet, dass bereits eine andere Browser-Sitzung oder ein anderes Gerät im Router-Interface eingeloggt ist.

## Lösungen:

### Lösung 1: Andere Browser-Tabs schließen
1. Schließe **alle anderen Browser-Tabs** mit dem Router-Interface
2. Warte 1-2 Minuten
3. Versuche es erneut: `http://192.168.0.1`

### Lösung 2: Andere Geräte prüfen
- Prüfe, ob jemand anderes im Router-Interface eingeloggt ist
- Oder ob du es auf einem anderen Gerät (Handy, Tablet) geöffnet hast

### Lösung 3: Browser-Cache leeren
1. Drücke `Ctrl + Shift + Delete`
2. Wähle "Cookies und Cache"
3. Lösche die Daten
4. Versuche es erneut

### Lösung 4: Inkognito/Private Modus
1. Öffne Browser im **Inkognito-Modus** (Ctrl + Shift + N)
2. Gehe zu: `http://192.168.0.1`

### Lösung 5: Router neu starten (wenn nichts hilft)
- Router kurz vom Strom trennen (30 Sekunden)
- Wieder anschließen
- Warten bis Router vollständig gebootet ist
- Dann erneut versuchen

## Alternative: IP direkt am Pi finden

Falls das Router-Interface nicht funktioniert, verwende die **Monitor-Methode**:

1. **HDMI-Kabel** vom Pi zum Monitor/TV
2. **USB-Tastatur** anschließen
3. Am Pi einloggen: `pi` / `123456789`
4. IP anzeigen:
   ```bash
   hostname -I
   ```

## Nachdem du die IP hast:

```bash
ssh pi@[IP-ADRESSE]
# Password: 123456789
```
