import urllib.request
import urllib.error
import tomllib
import tomli_w
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


def modify(config_location: str, entry: str, value: str, temp_prompt: Prompt):
    """
    # Modifies the configuration file
    """
    with open(config_location, "rb") as f:
        table = tomllib.load(f)

    keys = entry.split(".")
    # HACK: Again evil recursive trick
    sub_table = table
    for i in range(len(keys) - 1):
        validity = sub_table.get(keys[i], None)
        if validity is None:
            temp_prompt.say("This entry does not exist. Creating a new entry.")
            sub_table[keys[i]] = {}
            sub_table = sub_table[keys[i]]
        else:
            sub_table = sub_table[keys[i]]
    sub_table[keys[-1]] = value

    with open("config.toml", "wb") as f:
        tomli_w.dump(table, f)
