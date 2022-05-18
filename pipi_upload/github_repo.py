#https://www.devdungeon.com/content/working-git-repositories-python

#import gitpython
import git
import os
import sys
import shutil




#location of the local folder where the github repository will be downloaded (pulled)
local_repo = "/home/pi/pipi_reader"
#location/address of the remote github repository
github_repo = "https://github.com/TomasSpusta/pipi_reader.git"
'''
try:
    shutil.rmtree(local_repo)
except OSError as e:
    print ("Error: %s - %s." % (e.filename, e.strerror))
'''


#try to clone remote repository from github
try:
    cloned_repo = git.Repo.clone_from (github_repo, local_repo)
except Exception as error:
    #if the repository is already cloned, the folder is present on RPi,
    #error will happen, then we will try to use pull command
    #print(error)
    try:
        #initialize local repository
        repo = git.Repo(local_repo)
        repo.git.reset('--hard')
        repo.remotes.origin.pull()
    except Exception as e:
        print ("Neco sa podelalo, neexistuje repository na disku")
        print (e)
        
print("Update finished")    

