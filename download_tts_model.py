import os
import logging
import sys
import shutil
import stat
import re

#************************************************/
#/****** Huggingface and Github Downloader ******/
#************************************************/

# Set URLs and Download directories
repo_url = "https://huggingface.co/KoljaB/XTTS_Models" # Also V2 can be found here: https://huggingface.co/coqui/XTTS-v2/
subfolder = "Lasinya" # Set the name of 'directory/model' you want to download(i.e. Lasinya, Samantha, v2.0.2) - Leave empty to download full 'repository'
local_dir = "./models/xtts"  # Replace with your desired path


# ***Initial Cleanup if already exists a '.git(hidden) directory'***
def remove_readonly(func, path, excinfo):
    os.chmod(path, stat.S_IWRITE)
    func(path)

if __name__ == "__main__":
    # Define the path to the .git folder
    git_folder_path = os.path.join(local_dir, ".git")  # Get the download directory here = place where .git is downloaded

    # Check if the .git folder exists and delete it
    if os.path.exists(git_folder_path) and os.path.isdir(git_folder_path):
        shutil.rmtree(git_folder_path, onerror=remove_readonly)
        logging.info(f"Successfully deleted directory/file: {git_folder_path}")
    else:
        logging.error(f"No need to delete .git file. It does not exist in {git_folder_path}.")


if not subfolder: # ***If 'subfolder' variable is empty(""), then download the full repo***
        
        #Get repo name with Regex (requires: 'import re')
        repo_name_pattern = r"([^\/]+$)" # source → https://stackoverflow.com/a/47942256
        repo_name = re.search(repo_name_pattern, repo_url).group(1)

        # Create path including the 'repo_name' to use it as download directory.
        repo_dir_path = os.path.join(local_dir, repo_name) 

        # Create the directory if it doesn't exist
        os.makedirs(repo_dir_path, exist_ok=True)

        logging.info(f"Downloading files to '{local_dir}'...")

        # Correct the git clone command to execute within the script
        os.system(f"git clone {repo_url} {repo_dir_path}")

        logging.info(f"Files downloaded successfully to: {local_dir}")

else: # ***If 'subfolder' variable is NOT empty, then download the especific repo***
        
         # Start setting up download folder and comparing files
        def download_subfolder(repo_url, subfolder, local_dir):
            logging.info(f"Downloading subfolder '{subfolder}' from '{repo_url}' to '{local_dir}'...")
            os.makedirs(local_dir, exist_ok=True)
            os.system(f"git init {local_dir}")
            os.system(f"cd {local_dir} && git remote add -f origin {repo_url}")
            os.system(f"cd {local_dir} && git config core.sparseCheckout true")
            with open(os.path.join(local_dir, ".git/info/sparse-checkout"), 'w') as sc:
                sc.write(subfolder)
            os.system(f"cd {local_dir} && git pull --depth=1 origin main")
            logging.info(f"Subfolder '{subfolder}' downloaded successfully to: {local_dir}")

        # Finally download the files
        download_subfolder(repo_url, subfolder, local_dir)


# ***Cleanup downloaded .git directory***

# Check if the .git folder exists and delete it
if os.path.exists(git_folder_path) and os.path.isdir(git_folder_path):
    shutil.rmtree(git_folder_path, onerror=remove_readonly)
    logging.info(f"Successfully deleted directory: {git_folder_path}")
else:
    logging.error(f"No need to delete directory {git_folder_path}, does not exist or is not a directory.")
