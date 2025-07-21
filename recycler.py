import os
import sys
import urllib.request
import urllib.error
from sys import platform
import tomllib

parameters = sys.argv
print(parameters)
config_file = f"{parameters[1]}/config.toml"

options = {
    "silent": False,  # If true, no output will be printed to the console
    "writeslog": False,  # If true, output will be written to a log file
}


def log(message: str):
    pass


def say(message: str):
    if options["silent"] is False:
        print(message)
    elif options["writeslog"] is True:
        log(message)
    else:
        pass


class Config:
    """
    This class warps the configuration file
    to traceback KeyError exceptions from
    configuration file.
    """

    __entries: dict[str, str]

    def __init__(self, entries: dict[str, str]):
        self.__entries = entries

    def get(self, key: str) -> str:
        value = ""
        try:
            value = self.__entries[key]
        except KeyError as e:
            print(f"There is a configuration error, '{
                  key}' not found in configuration: {e}")
            raise e
        return value


def download_config() -> bool:
    """
    Downloads the configuration file from
    the github repository and saves it as
    'config.toml'
    """

    url = "https://raw.githubusercontent.com/KineticJetIce245/py-recycler/refs/heads/main/config.toml"
    print(f"Fetching from {url}")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            with open(config_file, "wb") as f:
                f.write(response.read())
                print("Downloaded configuration file successfully.")
                return True
    except urllib.error.URLError as e:
        print(f"Failed to download configuration file: {e}")
        return False

    print("Failed to download configuration file.")
    return False


def open_config() -> Config:
    success_flag = False

    try:
        with open(config_file, "rb") as f:
            config = Config(tomllib.load(f))
            success_flag = True
        if (success_flag):
            return config
        exit(1)

    except FileNotFoundError as e:

        print(f"Configuration file not found: {e}")
        print("Trying to download the configuration file...")

        if (download_config()):
            with open(config_file, "rb") as f:
                config = Config(tomllib.load(f))
                success_flag = True

    except tomllib.TOMLDecodeError as e:
        print(f"Configuration file is not proper toml: {e}")
    except Exception as e:
        print(f"Error reading configuration file: {e}")

    if (success_flag):
        return config
    else:
        print("Failed to load configuration file. Exiting.")
        exit(1)


"""
if (len(parameters) < 2):
    print("Option, file name, or folder name missing")
    exit(1)


print(parameters)

directory_path = f"{os.environ['USERPROFILE']}\\Recycle.Bin"
contents = os.listdir(directory_path)
for item in contents:
    print(item)

print("hello world")
"""

print(open_config())
