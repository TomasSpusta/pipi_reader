# https://www.devdungeon.com/content/working-git-repositories-python
# https://linuxconfig.org/how-to-manage-git-repositories-with-python


from datetime import datetime
import requests
import git
from lcd_display import display
from log import write_log
from log_temp import write_log_temp


def ghub_check(branch):
    display("Repo check", "", "", "", clear=True, backlight_status=True, sleep=1)

    # location of the local folder where the github repository will be downloaded (pulled)
    local_repo = "/home/bluebox/pipi_reader"

    # location/address of the remote github repository
    github_repo = "https://github.com/TomasSpusta/pipi_reader.git"

    # try to clone remote repository from github
    try:
        git.Repo.clone_from(github_repo, local_repo, branch=branch)
        write_log(4, datetime.now(), "Repo cloned")
        print("Repo cloned")

    except Exception as github_e:
        # if the repository is already cloned, the folder is present on RPi,
        # error will happen, then we will try to use pull command
        # print(error)
        git_update(local_repo)
        write_log(4, datetime.now(), "Repo updated")

    last_change = git_last_change(local_repo)
    current_version = git_version()

    display("Repo check","Repo updated",current_version,last_change,clear=True,backlight_status=True,sleep=2,   )
    log_note = "Update finished. \nVersion: %s \nLast change: %s" % (current_version,last_change,)
    write_log(4, datetime.now(), log_note)


def git_version():
    # https://api.github.com/repos/{owner}/{repo}/releases/latest
    response = requests.get(
        "https://api.github.com/repos/TomasSpusta/pipi_reader/releases/latest"
    )
    git_version = response.json()["name"]
    print(git_version)
    return str(git_version)


def git_update(local_repo):
    try:
        display("Checking software","","","",True,True,2)
        # initialize local repository
        repo = git.Repo(local_repo)
        repo.git.reset("--hard")
        repo.remotes.origin.pull()
        
        write_log_temp ("Repo update finished")
        print("Update finished")
        display("Software updated","","","",True,True,2)

    except Exception as repo_e:
        print("Problem s repository na disku")
        print(repo_e)
        write_log_temp ("Repo update error: " + str(repo_e))
        display("Repo check","Repo Update ERROR",repo_e,"",True,True,2)

def git_last_change(local_repo):
    try:
        repo = git.Repo(local_repo)
        tree = repo.tree()
        for blob in tree:
            commit = next(repo.iter_commits(paths=blob.path, max_count=1))
            date = datetime.fromtimestamp(commit.committed_date)
            if blob.path == "pipi_upload":
                last_edit_date = date
                print(blob.path, last_edit_date)
                return str(last_edit_date)
    except Exception as repo_last_e:
        print("Problem s repository na disku")
        print(repo_last_e)
        write_log(4, repo_last_e, datetime.now())
