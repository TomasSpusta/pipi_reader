#!/bin/bash
echo "---GITHUB UPDATE---"
/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload/init_files/github_update.py

echo "---GET MAC ADDRESS---"
/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload/init_files/get_mac_address.py

echo "---GET TOKEN---"
/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload/init_files/get_token.py
