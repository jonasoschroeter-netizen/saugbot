#!/usr/bin/env python3
"""
Automatisches Update-System für Saugbot
Prüft regelmäßig auf GitHub-Änderungen und aktualisiert automatisch
"""

import subprocess
import time
import os
import sys
from pathlib import Path

# Projekt-Verzeichnis
PROJECT_DIR = Path.home() / "saugbot"
GIT_BRANCH = "main"
CHECK_INTERVAL = 30  # Sekunden zwischen Checks

def run_command(cmd, cwd=None):
    """Führe Shell-Befehl aus und gib Output zurück."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or PROJECT_DIR,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def check_for_updates():
    """Prüfe ob Updates auf GitHub verfügbar sind."""
    # Hole neueste Informationen von GitHub
    success, stdout, stderr = run_command("git fetch origin")
    if not success:
        print(f"Error fetching: {stderr}")
        return False
    
    # Prüfe ob lokaler Branch hinterher ist
    success, stdout, stderr = run_command(
        f"git rev-list HEAD..origin/{GIT_BRANCH} --count"
    )
    if success and stdout.strip():
        commits_behind = int(stdout.strip())
        if commits_behind > 0:
            return True
    
    return False

def update_repository():
    """Hole Updates vom GitHub."""
    print("🔄 Updates gefunden! Starte Update...")
    
    # Stash lokale Änderungen (falls vorhanden)
    run_command("git stash")
    
    # Pull Updates
    success, stdout, stderr = run_command(f"git pull origin {GIT_BRANCH}")
    
    if success:
        print("✅ Repository erfolgreich aktualisiert!")
        print(stdout)
        return True
    else:
        print(f"❌ Fehler beim Update: {stderr}")
        return False

def restart_application():
    """Starte die Anwendung neu."""
    print("🔄 Starte Anwendung neu...")
    
    # Finde laufende Python-Prozesse (main.py oder web_interface.py)
    success, stdout, stderr = run_command(
        "pgrep -f 'python3.*(main|web_interface).py'"
    )
    
    if success and stdout.strip():
        pids = stdout.strip().split('\n')
        for pid in pids:
            try:
                os.kill(int(pid), 15)  # SIGTERM
                print(f"   Prozess {pid} beendet")
            except:
                pass
        time.sleep(2)  # Warte bis Prozesse beendet sind
    
    # Starte Anwendung neu (wird von systemd oder screen gemacht)
    # Hier nur Logging
    print("✅ Anwendung sollte neu gestartet werden")
    return True

def main():
    """Haupt-Loop für automatische Updates."""
    print("🚀 Saugbot Auto-Update System gestartet")
    print(f"📁 Projekt-Verzeichnis: {PROJECT_DIR}")
    print(f"⏱️  Prüfe alle {CHECK_INTERVAL} Sekunden auf Updates...")
    print("   (Drücke Ctrl+C zum Beenden)\n")
    
    last_update_check = 0
    
    try:
        while True:
            current_time = time.time()
            
            # Prüfe auf Updates
            if check_for_updates():
                if update_repository():
                    restart_application()
                    print(f"\n✅ Update abgeschlossen. Nächste Prüfung in {CHECK_INTERVAL} Sekunden...\n")
                else:
                    print(f"\n⚠️  Update fehlgeschlagen. Nächste Prüfung in {CHECK_INTERVAL} Sekunden...\n")
            
            # Warte bis nächste Prüfung
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Auto-Update System beendet")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
