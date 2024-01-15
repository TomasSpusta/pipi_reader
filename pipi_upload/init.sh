#!/bin/bash
echo "---GITHUB UPDATE---"
/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload/github_update.py

echo "---GET MAC ADDRESS---"
/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload/get_mac_address.py

echo "---GET TOKEN---"
#/usr/bin/python3 /home/bluebox/pipi_reader/pipi_upload/get_token.py
