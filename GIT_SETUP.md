# GitHub Setup Instructions for Saugbot

## Initial Setup on Raspberry Pi

### 1. SSH to Raspberry Pi

From your laptop:
```bash
ssh pi@saugbot.local
# Password: 123456789
```

### 2. Navigate to Home Directory and Clone Repository

```bash
cd ~
git clone git@github.com:jonasoschroeter-netizen/saugbot.git
cd saugbot
```

**Note**: If the repository doesn't exist yet on GitHub, create it first on GitHub.com, then clone it.

### 3. If Repository Already Exists Locally

If you already have the code locally and need to connect to GitHub:

```bash
cd ~/saugbot  # or wherever your project is
git init
git remote add origin git@github.com:jonasoschroeter-netizen/saugbot.git
```

### 4. Setup SSH Key for GitHub (if not already done)

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Display public key to add to GitHub
cat ~/.ssh/id_ed25519.pub
```

Then:
1. Copy the output
2. Go to https://github.com/settings/keys
3. Click "New SSH key"
4. Paste the key and save

Test connection:
```bash
ssh -T git@github.com
```

### 5. Initial Commit and Push

```bash
# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Saugbot project structure with motor control, sensors, and main control loop"

# Push to GitHub (if main branch)
git push -u origin main

# OR if using master branch
git branch -M main  # Rename to main if needed
git push -u origin main
```

## Daily Workflow

### Making Changes and Pushing

```bash
# After making changes
git add .
git commit -m "Description of your changes"
git push origin main
```

### Example Commit Messages

```bash
git commit -m "Add collision avoidance logic"
git commit -m "Update GPIO pin assignments in config.py"
git commit -m "Fix ultrasonic sensor timeout handling"
git commit -m "Add side brush control module"
```

## Pulling Latest Changes

If working from multiple locations:

```bash
git pull origin main
```

## Troubleshooting

### If push is rejected:
```bash
# Pull latest changes first
git pull origin main --rebase
# Then push again
git push origin main
```

### If remote already exists with different URL:
```bash
git remote set-url origin git@github.com:jonasoschroeter-netizen/saugbot.git
```

### Check current remote:
```bash
git remote -v
```
