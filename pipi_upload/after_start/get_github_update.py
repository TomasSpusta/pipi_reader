import sys
sys.path.append('/home/bluebox/pipi_reader/pipi_upload')


from github_check import git_update
from time import sleep


git_update ("/home/bluebox/pipi_reader")
sleep (1)