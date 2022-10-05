#https://www.devdungeon.com/content/working-git-repositories-python
#https://linuxconfig.org/how-to-manage-git-repositories-with-python

#import gitpython
import git
import time
import LCD_display
from web_requests import git_release
import os
import sys
import shutil



def github_check (branch):
    #location of the local folder where the github repository will be downloaded (pulled)
    local_repo = "/home/pi/pipi_reader_develop"
    #location/address of the remote github repository
    github_repo = "https://github.com/TomasSpusta/pipi_reader.git"
    #branch = "develop"

    #try to clone remote repository from github
    try:
        #cloned_repo = 
        git.Repo.clone_from (github_repo, local_repo, branch=branch)
        print("Repo cloned")
    except Exception as error:
        #if the repository is already cloned, the folder is present on RPi,
        #error will happen, then we will try to use pull command
        #print(error)
        try:
            #initialize local repository
            repo = git.Repo(local_repo)
            repo.git.reset('--hard')
            repo.remotes.origin.pull()
            git_release ()
            print("Update finished")
        except Exception as repo_e:
            print ("Problem s repository na disku")
            print (repo_e)
            
    LCD_display.version()
    time.sleep (3) 

