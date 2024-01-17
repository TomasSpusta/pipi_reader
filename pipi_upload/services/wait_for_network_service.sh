#https://raspberrypi.stackexchange.com/questions/78991/running-a-script-after-an-internet-connection-is-established

#!/bin/bash

echo "---Started---"


# Create or edit wait_network.service using a temporary file
echo "---Creating service---"
sudo tee /etc/systemd/system/wait_network.service.tmp > /dev/null <<EOF

[Unit]
Description=Wait for Network Service
#Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=bluebox
WorkingDirectory=/home/bluebox/pipi_reader/pipi_upload
ExecStart=/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload//after_start/get_github_update.py
ExecStart=/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload//after_start/get_mac_address.py
ExecStart=/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload//after_start/get_token.py
ExecStart=/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload/loading.py

[Install]
WantedBy=multi-user.target
WantedBy=network-online.service
EOF

# Move the temporary file to the final location
sudo mv /etc/systemd/system/wait_network.service.tmp /etc/systemd/system/wait_network.service

# Reload systemd to apply changes
sudo systemctl daemon-reload

# Optional: Display the content of the created/edited service file
echo "---Content of wait_network.service:---"
sudo cat /etc/systemd/system/wait_network.service

#Activate service
echo "---Activating service:---"
sudo systemctl enable wait_network.service
sudo systemctl start wait_network.service

# Check new service status
#echo "---Service status:---"
sudo systemctl status wait_network.service

#Reboot service
#sudo systemctl reboot
echo "Wait for reboot - sudo systemctl reboot"
