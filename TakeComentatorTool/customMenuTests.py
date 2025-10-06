import os 

ignoreFolders = [".git", "Sensitive"]
# For each function, create an event check that matches the name of the event to the function you want to call.
WIPSCRIPTS_PATH = "C:\\Projekty\\Repos\\MoBu-Scripts"

files = [f for f in os.listdir() if os.path.isdir(f)]


print(files)