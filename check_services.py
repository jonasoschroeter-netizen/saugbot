"""
Prüft welche Services auf dem Raspberry Pi erreichbar sind
"""

import socket

RASPBERRY_PI_IP = "192.168.37.207"  # Oder: saugbot.local

# Bekannte Ports
PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    5000: "Web-Interface",
    5900: "VNC",
    3389: "RDP",
    8080: "HTTP Alternative",
    8000: "HTTP Alternative 2",
}

def check_port(host, port, timeout=2):
    """Prüft ob Port offen ist."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def main():
    print("=" * 60)
    print("  Raspberry Pi Service-Check")
    print("=" * 60)
    print()
    print(f"Prüfe IP: {RASPBERRY_PI_IP}")
    print()
    
    open_ports = []
    
    for port, name in PORTS.items():
        is_open = check_port(RASPBERRY_PI_IP, port)
        status = "[OFFEN]" if is_open else "[GESCHLOSSEN]"
        print(f"{name:20} Port {port:5} {status}")
        if is_open:
            open_ports.append((port, name))
    
    print()
    print("=" * 60)
    
    if open_ports:
        print("  Erreichbare Services:")
        for port, name in open_ports:
            print(f"  - {name} auf Port {port}")
        print()
        print("  Moegliche Zugriffswege:")
        if any(p[0] == 22 for p in open_ports):
            print("  ✅ SSH aktiviert - kannst dich verbinden!")
        if any(p[0] == 80 or p[0] == 8080 or p[0] == 8000 for p in open_ports):
            print("  ✅ Web-Server laeuft - pruefe im Browser")
        if any(p[0] == 5900 for p in open_ports):
            print("  ✅ VNC aktiviert - kannst dich verbinden!")
    else:
        print("  Keine erreichbaren Services gefunden")
        print()
        print("  Moegliche Loesungen:")
        print("  1. Auto-Update-System sollte Web-Interface starten")
        print("  2. SSH aktivieren (benoetigt physischen Zugriff)")
        print("  3. Warte auf naechsten Auto-Update-Check (30 Sekunden)")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
