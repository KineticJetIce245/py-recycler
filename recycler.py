import os
import sys
import urllib.request
import urllib.error
import tomllib


SHORT_OPTION = {
    "r": "recovery",
    "s": "silent",
    "l": "log",
    "c": "config"
}

options = {
    "recovery": False,      # If true, entering recovery mode
    "silent": False,        # If true, no output will be printed to the console
    "log": False,           # If true, output will be written to a log file
    "config": False,        # If true, enable config mode
}


def parse_parameters(received_parm) -> list:
    """
    # Parses the listed parameters,
    # adds the options to the options dictionary
    # and returns a list files to be processed.
    """
    other_param = []
    for param in received_parm[3:]:
        if param.startswith("--"):
            key, value = param[2:].split("=", 1)
            if (value.lower() == "false" or value.lower() == "true"):
                options[key] = (value.lower() == "true")
            else:
                options[key] = value
        elif param.startswith("-"):
            if (len(param[1:]) != 1):
                print(f"Invalid short option format: {param}")
                exit(1)
            key = SHORT_OPTION[param[1:]]
            options[key] = True
        else:
            other_param.append(param)
    return other_param


def log(message: str):
    # TODO: Implement logging functionality
    pass


def say(message: str):
    if options["silent"] is False:
        print(message)
    elif options["log"] is True:
        log(message)
    else:
        pass


class Recycler:
    """
    # This class is records and load the logs
    # of the recycle bin.
    """

    __logloc: str
    __bin: str

    def __init__(self, logloc: str, bin: str):
        self.__loginfo = logloc
        self.__bin = bin
        if not os.path.exists(self.__bin):
            os.makedirs(self.__bin)

    def analyze_regex(self, call_path, file_path) -> dict[str]:
        """
        # This method examines the file path to determine
        # if it contains a regex pattern or wildcard.
        # If it does, it returns a dictionary mapping each
        # matching file's absolute path to its destination path.
        """
        # NOTE: Rephrased by Copilot.

        paths = {}

        if file_path == "." or file_path == "*":
            contents = os.listdir(call_path)
            for item in contents:
                destination = os.path.join(
                    self.__bin, os.path.basename(call_path))
                paths[os.path.join(call_path, item)] = destination
        else:
            pass

        return paths

    def recycle(self, call_path: str, file_path: str) -> bool:
        """
        # This method recycles the file at the given path.
        # Returns True if successful, False otherwise.
        """

        # Our destiny is recycle bin :P
        destinies = self.analyze_regex(call_path, file_path)

        for p in destinies.keys():
            if not os.path.exists(p):
                say(f"File / folder {p} does not exist.")
                continue
            say(f"Recycling {p} to {destinies[p]}")

        return True


def download_config(config_location) -> bool:
    """
    # Downloads the configuration file from
    # the github repository and saves it as
    # 'config.toml'
    """

    url = "https://raw.githubusercontent.com/KineticJetIce245/py-recycler/refs/heads/main/config.toml"
    say(f"Fetching from {url}")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            with open(config_location, "wb") as f:
                f.write(response.read())
                say("Downloaded configuration file successfully.")
                return True
    except urllib.error.URLError as e:
        say(f"Failed to download configuration file: {e}")
        return False

    say("Failed to download configuration file.")
    return False


def open_config(config_location) -> dict:
    success_flag = False

    try:
        with open(config_location, "rb") as f:
            config = tomllib.load(f)
            success_flag = True
        if (success_flag):
            return config
        exit(1)

    except FileNotFoundError as e:

        say(f"Configuration file not found: {e}")
        say("Trying to download the configuration file...")

        if (download_config(config_location)):
            with open(config_location, "rb") as f:
                config = tomllib.load(f)
                success_flag = True

    except tomllib.TOMLDecodeError as e:
        say(f"Configuration file is not proper toml: {e}")
    except Exception as e:
        say(f"Error reading configuration file: {e}")

    if (success_flag):
        return config
    else:
        say("Failed to load configuration file. Exiting.")
        exit(1)


def mainCycle():
    # TODO: Implement the main cycle of the program
    pass


"""
# Initialization
"""
parameters = sys.argv
"""
# From the third parameter onwards
# first parameters: .py location
# second parameters: .py folder
# thrid parameters: location where it is called
"""
if len(parameters) < 3:
    print("Error in the launch parameters, config file location missing.")
    exit(1)
config = open_config(os.path.join(parameters[1], "config.toml"))

print(parameters)

"""
# Recycle Bin Initialization
"""
if (config["path"]["under_user_profile"] is True):
    recycle_bin = os.path.join(os.path.expanduser(
        '~'), config['path']['recycle_bin'])
else:
    recycle_bin = config["path"]["recycle_bin"]

recycler = Recycler(os.path.join(parameters[1], "reclog.csv"), recycle_bin)


other_parameters = parse_parameters(parameters)
say(f"Recycle Bin Path: {recycle_bin}")
if options["recovery"]:
    say("Entering recovery mode...")
elif options["config"]:
    say("Entering config mode...")
elif len(other_parameters) > 0:
    say(f"Processing expressions: {', '.join(other_parameters)}")
    for file_path in other_parameters:
        recycler.recycle(parameters[2], file_path)
