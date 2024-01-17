import sys
sys.path.append('pipi_upload')


from github_check import git_update
from time import sleep


git_update ("/home/bluebox/pipi_reader")
sleep (1)