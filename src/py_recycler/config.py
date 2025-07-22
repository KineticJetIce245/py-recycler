import urllib.request
import urllib.error
import tomllib
from .logger import Logger


def __download_config(config_location, temp_logger) -> bool:
    """
    # Downloads the configuration file from
    # the github repository and saves it as
    # 'config.toml'
    """

    url = "https://raw.githubusercontent.com/KineticJetIce245/py-recycler/refs/heads/main/config.toml"
    temp_logger.say(f"Fetching from {url}")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            with open(config_location, "wb") as f:
                f.write(response.read())
                temp_logger.say("Downloaded configuration file successfully.")
                return True
    except urllib.error.URLError as e:
        temp_logger.say(f"Failed to download configuration file: {e}")
        return False

    temp_logger.say("Failed to download configuration file.")
    return False


def load(config_location) -> dict:
    success_flag = False

    temp_logger = Logger(silent=False, log=False)

    try:
        with open(config_location, "rb") as f:
            config = tomllib.load(f)
            success_flag = True
        if (success_flag):
            return config

    except FileNotFoundError as e:
        temp_logger.say(f"Configuration file not found: {e}")
        temp_logger.say("Trying to download the configuration file...")

        if (__download_config(config_location, temp_logger)):
            with open(config_location, "rb") as f:
                config = tomllib.load(f)
                success_flag = True

    except tomllib.TOMLDecodeError as e:
        temp_logger.say(f"Configuration file is not proper toml: {e}")
    except Exception as e:
        temp_logger.say(f"Error reading configuration file: {e}")

    if (success_flag):
        return config
    else:
        temp_logger.say("Failed to load configuration file. Exiting.")
        exit(1)
