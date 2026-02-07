#!/bin/bash
# Setup script for GitHub connection on Raspberry Pi
# Run this script on the Raspberry Pi after cloning the repository

echo "Setting up Git for Saugbot project..."

# Check if .env exists, if not create from example
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo ".env file created. Please review and update if needed."
fi

# Initialize git if not already initialized
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git remote add origin git@github.com:jonasoschroeter-netizen/saugbot.git
    echo "Git repository initialized and remote added."
else
    echo "Git repository already initialized."
    
    # Check if remote exists
    if ! git remote get-url origin &>/dev/null; then
        echo "Adding remote origin..."
        git remote add origin git@github.com:jonasoschroeter-netizen/saugbot.git
    else
        echo "Remote origin already configured."
    fi
fi

# Setup SSH key if needed (optional - user should do this manually)
echo ""
echo "To connect to GitHub via SSH, ensure you have:"
echo "1. Generated an SSH key: ssh-keygen -t ed25519 -C 'your_email@example.com'"
echo "2. Added it to GitHub: https://github.com/settings/keys"
echo "3. Tested connection: ssh -T git@github.com"

echo ""
echo "Setup complete!"
echo "Next steps:"
echo "1. Review config.py for GPIO pin assignments"
echo "2. Install dependencies: pip3 install -r requirements.txt"
echo "3. Test components individually before running main.py"
