# get token -> create new one, save to token data, or to config
# get sheet address
# update from github

from github_check import git_update
from network_check import get_mac_address
from web_requests import get_token 
from time import sleep
from configparser import ConfigParser
import os

#config = ConfigParser()

git_update ("/home/bluebox/pipi_reader")
#sleep (1)
get_mac_address ()
#sleep (1)
get_token ()
#sleep (1)


print (os.environ["MAC_ADDRESS"])
