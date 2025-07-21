import os
import sys
from sys import platform
import tomllib


def extract_config() -> dict:
    success_flag = False

    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
        success_flag = True

    if (success_flag):
        return config
    else:
        print("Configuration file not found or invalid.")


parameters = sys.argv
if (len(parameters) < 2):
    print("[Error from py-recyler] option, file name, or folder name missing")
    exit(1)


print(parameters)

directory_path = f"{os.environ['USERPROFILE']}\Recycle.Bin"
contents = os.listdir(directory_path)
for item in contents:
    print(item)
