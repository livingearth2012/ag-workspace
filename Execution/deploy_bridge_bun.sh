#!/bin/bash

# Configuration
VPS_IP="187.77.3.135"
REMOTE_DIR="/home/openclaw/ally-bridge"
SERVICE_NAME="ally-bridge"

echo "--- Deploying Ally Bridge (Bun) to VPS ($VPS_IP) ---"

# Create remote directory
ssh $VPS_IP "mkdir -p $REMOTE_DIR"

# Copy files
scp ally_bridge.js package.json .env $VPS_IP:$REMOTE_DIR/

# Remote Setup
ssh $VPS_IP << EOF
    cd $REMOTE_DIR
    # Install dependencies using Bun
    /snap/bin/bun install
    
    # Setup User Systemd Service
    mkdir -p ~/.config/systemd/user/
    cat << SERVICE > ~/.config/systemd/user/$SERVICE_NAME.service
[Unit]
Description=Ally Bridge Service (Bun)
After=network.target

[Service]
WorkingDirectory=$REMOTE_DIR
ExecStart=/snap/bin/bun run ally_bridge.js
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
SERVICE

    # Reload and Start (User Mode)
    systemctl --user daemon-reload
    systemctl --user enable $SERVICE_NAME
    systemctl --user restart $SERVICE_NAME
    
    # Ensure service stays alive after logout
    loginctl enable-linger \$USER
EOF

echo "--- Deployment Complete ---"
echo "Check status with: ssh $VPS_IP 'systemctl --user status $SERVICE_NAME'"
