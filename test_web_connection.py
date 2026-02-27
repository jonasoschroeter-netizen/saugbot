"""
Test-Skript um zu prüfen ob Web-Interface erreichbar ist
Läuft auf Windows-PC und testet Verbindung zum Raspberry Pi
"""

import socket
import sys
import os

# Fix für Windows Encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warnung: requests-Bibliothek nicht installiert. HTTP-Test wird übersprungen.")
    print("Installiere mit: pip install requests")

RASPBERRY_PI_IP = "192.168.37.207"  # Oder: saugbot.local
PORT = 5000

def test_port(host, port):
    """Testet ob Port erreichbar ist."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Fehler beim Port-Test: {e}")
        return False

def test_http(host, port):
    """Testet ob HTTP-Server antwortet."""
    if not REQUESTS_AVAILABLE:
        return False
    try:
        url = f"http://{host}:{port}"
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except requests.exceptions.Timeout:
        return False
    except Exception as e:
        print(f"HTTP-Test Fehler: {e}")
        return False

def main():
    print("=" * 60)
    print("  Web-Interface Verbindungstest")
    print("=" * 60)
    print()
    
    # Test 1: Ping
    print(f"1. Teste Ping zu {RASPBERRY_PI_IP}...")
    import subprocess
    try:
        result = subprocess.run(
            ["ping", "-n", "1", RASPBERRY_PI_IP],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print("   [OK] Raspberry Pi ist erreichbar")
        else:
            print("   [FEHLER] Raspberry Pi ist NICHT erreichbar")
            print("   -> Pruefe ob Pi eingeschaltet ist und im gleichen Netzwerk")
            return
    except Exception as e:
        print(f"   [WARNUNG] Ping-Test fehlgeschlagen: {e}")
    
    print()
    
    # Test 2: Port
    print(f"2. Teste Port {PORT}...")
    if test_port(RASPBERRY_PI_IP, PORT):
        print(f"   [OK] Port {PORT} ist offen")
    else:
        print(f"   [FEHLER] Port {PORT} ist geschlossen oder nicht erreichbar")
        print("   -> Web-Interface laeuft moeglicherweise nicht")
        print("   -> Starte auf dem Pi: python3 src/web_interface.py")
        return
    
    print()
    
    # Test 3: HTTP
    if REQUESTS_AVAILABLE:
        print(f"3. Teste HTTP-Verbindung...")
        if test_http(RASPBERRY_PI_IP, PORT):
            print("   [OK] HTTP-Server antwortet")
            print()
            print("=" * 60)
            print("  [OK] ALLE TESTS BESTANDEN!")
            print("=" * 60)
            print()
            print(f"Oeffne im Browser: http://{RASPBERRY_PI_IP}:{PORT}")
        else:
            print("   [FEHLER] HTTP-Server antwortet nicht")
            print("   -> Web-Interface laeuft, aber antwortet nicht korrekt")
            print("   -> Pruefe Logs auf dem Raspberry Pi")
    else:
        print("3. HTTP-Test uebersprungen (requests nicht installiert)")
        print()
        print("=" * 60)
        print("  Port ist offen - Web-Interface sollte erreichbar sein")
        print("=" * 60)
        print()
        print(f"Oeffne im Browser: http://{RASPBERRY_PI_IP}:{PORT}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest abgebrochen")
        sys.exit(0)
