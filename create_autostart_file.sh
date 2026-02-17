#!/bin/bash
# Erstellt Auto-Start-Dateien die beim Boot automatisch ausgeführt werden
# Wird vom Auto-Update-System ausgeführt

cd ~/saugbot

# Erstelle .bashrc Eintrag (falls nicht vorhanden)
if ! grep -q "auto_start_web.sh" ~/.bashrc 2>/dev/null; then
    echo "" >> ~/.bashrc
    echo "# Auto-Start Web-Interface" >> ~/.bashrc
    echo "if [ -f ~/saugbot/auto_start_web.sh ]; then" >> ~/.bashrc
    echo "    ~/saugbot/auto_start_web.sh &" >> ~/.bashrc
    echo "fi" >> ~/.bashrc
    echo "✅ .bashrc aktualisiert"
fi

# Erstelle systemd user service (funktioniert ohne sudo)
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/saugbot-web.service << 'EOF'
[Unit]
Description=Saugbot Web Interface
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/pi/saugbot
Environment="PYTHONPATH=/home/pi/saugbot"
ExecStart=/usr/bin/python3 /home/pi/saugbot/src/web_interface.py
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# Aktiviere user service (funktioniert ohne sudo)
systemctl --user daemon-reload
systemctl --user enable saugbot-web.service
systemctl --user start saugbot-web.service

echo "✅ User-Service installiert und gestartet"
echo "Web-Interface sollte jetzt laufen!"
