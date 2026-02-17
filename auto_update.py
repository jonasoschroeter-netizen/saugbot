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
    import sys
    msg = "🔄 Updates gefunden! Starte Update...\n"
    print(msg)
    sys.stderr.write(msg)
    sys.stderr.flush()
    
    # Stash lokale Änderungen (falls vorhanden)
    run_command("git stash")
    
    # Pull Updates
    success, stdout, stderr = run_command(f"git pull origin {GIT_BRANCH}")
    
    if success:
        msg = "✅ Repository erfolgreich aktualisiert!\n"
        print(msg)
        print(stdout)
        sys.stderr.write(msg)
        sys.stderr.write(stdout)
        sys.stderr.flush()
        return True
    else:
        msg = f"❌ Fehler beim Update: {stderr}\n"
        print(msg)
        sys.stderr.write(msg)
        sys.stderr.flush()
        return False

def restart_application():
    """Starte die Anwendung neu."""
    print("🔄 Starte Anwendung neu...")
    
    # Prüfe ob Web-Interface läuft (als Prozess oder Service)
    web_running = False
    
    # Prüfe Service
    success, stdout, stderr = run_command(
        "systemctl is-active saugbot-web.service 2>/dev/null"
    )
    if success and "active" in stdout:
        web_running = True
        print("   Web-Interface Service läuft - neu starten...")
        run_command("sudo systemctl restart saugbot-web.service")
        print("   ✅ Web-Interface Service neu gestartet")
    else:
        # Prüfe ob als Prozess läuft
        success, stdout, stderr = run_command(
            "pgrep -f 'python3.*web_interface.py'"
        )
        if success and stdout.strip():
            web_running = True
            print("   Web-Interface läuft als Prozess")
    
    # Starte Web-Interface falls nicht läuft
    if not web_running:
        print("   Web-Interface läuft nicht - starte im Hintergrund...")
        start_script = PROJECT_DIR / "start_web_background.sh"
        if start_script.exists():
            success, stdout, stderr = run_command(
                f"chmod +x {start_script} && bash {start_script}"
            )
            if success:
                print("   ✅ Web-Interface im Hintergrund gestartet")
            else:
                print(f"   ⚠️  Start-Fehler: {stderr}")
        else:
            # Fallback: Direkt starten
            print("   Starte Web-Interface direkt...")
            run_command(
                f"cd {PROJECT_DIR} && export PYTHONPATH={PROJECT_DIR} && "
                f"nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &"
            )
            print("   ✅ Web-Interface gestartet")
    
    # Finde laufende Python-Prozesse (main.py) - Web-Interface nicht beenden
    success, stdout, stderr = run_command(
        "pgrep -f 'python3.*main.py'"
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
    
    print("✅ Anwendung sollte neu gestartet werden")
    return True

def ensure_web_interface_running():
    """Stelle sicher, dass Web-Interface läuft."""
    # Prüfe ob Web-Interface läuft
    success, stdout, stderr = run_command(
        "pgrep -f 'python3.*web_interface.py'"
    )
    
    if success and stdout.strip():
        # Läuft bereits
        return True
    
    # Starte Web-Interface
    print("🌐 Web-Interface läuft nicht - starte jetzt...")
    
    # Versuche zuerst force_start_web.sh (zuverlässiger)
    force_script = PROJECT_DIR / "force_start_web.sh"
    if force_script.exists():
        success, stdout, stderr = run_command(
            f"chmod +x {force_script} && bash {force_script}"
        )
        if success:
            print("   ✅ Web-Interface gestartet (force_start_web.sh)")
            time.sleep(3)  # Warte kurz
            # Prüfe nochmal
            success, stdout, stderr = run_command(
                "pgrep -f 'python3.*web_interface.py'"
            )
            if success and stdout.strip():
                return True
    
    # Fallback: Direkt starten
    print("   Versuche direkten Start...")
    run_command(
        f"cd {PROJECT_DIR} && export PYTHONPATH={PROJECT_DIR} && "
        f"mkdir -p logs && "
        f"pkill -f web_interface.py; "
        f"sleep 1; "
        f"nohup python3 src/web_interface.py > logs/web_interface.log 2>&1 &"
    )
    time.sleep(2)
    
    # Prüfe ob es jetzt läuft
    success, stdout, stderr = run_command(
        "pgrep -f 'python3.*web_interface.py'"
    )
    if success and stdout.strip():
        print("   ✅ Web-Interface gestartet (direkt)")
        return True
    else:
        print("   ⚠️  Web-Interface konnte nicht gestartet werden")
        print("   Prüfe Logs: ~/saugbot/logs/web_interface.log")
        return False

def main():
    """Haupt-Loop für automatische Updates."""
    import sys
    # Output auch nach stderr für systemd logs
    sys.stderr.write("🚀 Saugbot Auto-Update System gestartet\n")
    sys.stderr.write(f"📁 Projekt-Verzeichnis: {PROJECT_DIR}\n")
    sys.stderr.write(f"⏱️  Prüfe alle {CHECK_INTERVAL} Sekunden auf Updates...\n")
    sys.stderr.write("   (Drücke Ctrl+C zum Beenden)\n\n")
    sys.stderr.flush()
    
    print("🚀 Saugbot Auto-Update System gestartet")
    print(f"📁 Projekt-Verzeichnis: {PROJECT_DIR}")
    print(f"⏱️  Prüfe alle {CHECK_INTERVAL} Sekunden auf Updates...")
    print("   (Drücke Ctrl+C zum Beenden)\n")
    
    # Stelle sicher, dass Web-Interface beim Start läuft
    ensure_web_interface_running()
    
    last_update_check = 0
    web_check_counter = 0
    
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
            
            # Prüfe alle 60 Sekunden ob Web-Interface läuft
            web_check_counter += 1
            if web_check_counter >= (60 // CHECK_INTERVAL):  # Alle 60 Sekunden
                web_check_counter = 0
                ensure_web_interface_running()
            
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
