#!/bin/bash
echo "---GITHUB UPDATE---"
/usr/bin/python3 /home/bluebox/CFNano_BlueBox/bluebox_upload/after_start/github_update.py

echo "---GET MAC ADDRESS---"
/usr/bin/python3 /home/bluebox/CFNano_BlueBox/bluebox_upload/after_start/get_mac_address.py

echo "---GET TOKEN---"
/usr/bin/python3 /home/bluebox/CFNano_BlueBox/bluebox_upload/after_start/get_token.py
