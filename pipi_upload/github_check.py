#https://www.devdungeon.com/content/working-git-repositories-python
#https://linuxconfig.org/how-to-manage-git-repositories-with-python

#import gitpython
from datetime import datetime
import git
import LCD_display
import web_requests
from log import write_log
import config

def github_check (branch):
    LCD_display.display ("Repo check","","" ,"",clear=True, backlight_status=True, sleep=2) 
    
    #location of the local folder where the github repository will be downloaded (pulled)

    local_repo = "/home/bluebox/pipi_reader"
    
    #location/address of the remote github repository
    github_repo = "https://github.com/TomasSpusta/pipi_reader.git"
    #branch = "develop"

    #try to clone remote repository from github
    try:
        #cloned_repo = 
        git.Repo.clone_from (github_repo, local_repo, branch=branch)
        write_log(4, datetime.now(), "Repo cloned")
        print("Repo cloned")
    except Exception as github_e:
        #if the repository is already cloned, the folder is present on RPi,
        #error will happen, then we will try to use pull command
        #print(error)
        try:
            #initialize local repository
            repo = git.Repo(local_repo)
            repo.git.reset('--hard')
            repo.remotes.origin.pull()
            print("Update finished")
            web_requests.git_version ()
            write_log(4, datetime.now(), "Update finished, version: " + config.git_release )
        except Exception as repo_e:
            print ("Problem s repository na disku")
            print (repo_e)
            write_log(4, repo_e, datetime.now())
            
    LCD_display.version()


