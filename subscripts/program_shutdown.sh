# https://unix.stackexchange.com/questions/645914/running-a-sudo-command-automatically-on-startup

sudo mkdir -p /opt

# Create the shutdown script
sudo tee /opt/mystartup.sh > /dev/null << 'EOF'
#!/bin/bash
shutdown 01:30
EOF

# Set permissions
sudo chmod 755 /opt/mystartup.sh

# Create systemd service
sudo tee /etc/systemd/system/mystartup.service > /dev/null << 'EOF'
[Unit]
Description=Set automatic shutdown

[Service]
Type=oneshot
ExecStart=/opt/mystartup.sh

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable mystartup.service
sudo systemctl start mystartup.service