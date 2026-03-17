#!/bin/bash

# Configuration
VPS_IP="187.77.3.135"
REMOTE_DIR="~/ally-bridge"
SERVICE_NAME="ally-bridge"

echo "--- Deploying Ally Bridge to VPS ($VPS_IP) ---"

# Create remote directory
ssh $VPS_IP "mkdir -p $REMOTE_DIR"

# Copy files
scp ally_bridge.py bridge_requirements.txt .env $VPS_IP:$REMOTE_DIR/

# Remote Setup
ssh $VPS_IP << EOF
    cd $REMOTE_DIR
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r bridge_requirements.txt
    
    # Create Systemd Service File
    cat << SERVICE | sudo tee /etc/systemd/system/$SERVICE_NAME.service
[Unit]
Description=Ally Bridge Service (AG-Workspace)
After=network.target

[Service]
User=\$USER
WorkingDirectory=$REMOTE_DIR
ExecStart=$REMOTE_DIR/venv/bin/python3 ally_bridge.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE

    # Reload and Start
    sudo systemctl daemon-reload
    sudo systemctl enable $SERVICE_NAME
    sudo systemctl restart $SERVICE_NAME
EOF

echo "--- Deployment Complete ---"
echo "Check status with: ssh $VPS_IP 'sudo systemctl status $SERVICE_NAME'"
