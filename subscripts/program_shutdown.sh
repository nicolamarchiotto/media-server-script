# https://unix.stackexchange.com/questions/645914/running-a-sudo-command-automatically-on-startup

sudo touch /usr/local/sbin/mystartup.sh 
sudo echo -e "#!/bin/bash\nsudo shutdown 01:30" > /usr/local/sbin/mystartup.sh 
sudo chmod 0700 /usr/local/sbin/mystartup.sh 
sudo touch /etc/systemd/system/mystartup.service
sudo echo -e "[Unit]\nDescription=Set automatic shutdown\n[Service]\nExecStart=/usr/local/sbin/mystartup.sh\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/mystartup.service
sudo systemctl start mystartup.service
sudo systemctl enable mystartup.service
sudo systemctl daemon-reload