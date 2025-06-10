import sys
sys.path.append('/home/bluebox/CFNano_BlueBox/bluebox_upload')


from github_check import git_update
from time import sleep


git_update ("/home/bluebox/CFNano_BlueBox")
sleep (1)