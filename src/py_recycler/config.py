import urllib.request
import urllib.error
import tomllib
from .prompt import Prompt


def __download_config(config_location: str, temp_prompt: Prompt) -> bool:
    """
    # Downloads the configuration file from
    # the github repository and saves it as
    # 'config.toml'
    """

    url = "https://raw.githubusercontent.com/KineticJetIce245/py-recycler/refs/heads/main/config.toml"
    temp_prompt.say(f"Fetching from {url}")
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            with open(config_location, "wb") as f:
                f.write(response.read())
                temp_prompt.say("Downloaded configuration file successfully.")
                return True

    except Exception as e:
        temp_prompt.say(f"Failed to download configuration file: {e}")
        return False

    temp_prompt.say("Failed to download configuration file.")
    return False


def load(config_location: str) -> dict:
    """
    # Loads the configuration file,
    # In case where the configuration file
    # is not found, it calls method to
    # download the configuration file
    # from github.
    """
    success_flag = False
    temp_prompt = Prompt()

    try:
        with open(config_location, "rb") as f:
            config = tomllib.load(f)
            success_flag = True

        if (success_flag):
            return config

    except FileNotFoundError as e:
        temp_prompt.say(f"Configuration file not found: {e}")
        temp_prompt.say("Trying to download the configuration file...")

        if (__download_config(config_location, temp_prompt)):
            with open(config_location, "rb") as f:
                config = tomllib.load(f)
                success_flag = True

    except tomllib.TOMLDecodeError as e:
        temp_prompt.say(f"Configuration file is not proper toml: {e}")

    except Exception as e:
        temp_prompt.say(f"Error reading configuration file: {e}")

    if (success_flag):
        return config
    else:
        temp_prompt.say("Failed to load configuration file. Exiting.")
        exit(1)


def modify(config_location: str, entry: str, value: str) -> bool:
    pass
