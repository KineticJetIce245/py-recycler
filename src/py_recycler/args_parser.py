from .logger import Looger


def parse_parameters(params, options, short_options) -> list:
    """
    # Parses the listed parameters,
    # adds the options to the options dictionary
    # and returns a list files to be processed.
    """
    temp_logger = Looger(silent=False, log=False)
    file_folder_param = []
    for param in params:
        if param.startswith("--"):
            key, value = param[2:].split("=", 1)
            if (value.lower() == "false" or value.lower() == "true"):
                options[key] = (value.lower() == "true")
            else:
                options[key] = value
        elif param.startswith("-"):
            if (len(param[1:]) != 1):
                temp_logger.say(f"Invalid short option format: {param}")
                exit(1)
            key = short_options[param[1:]]
            options[key] = True
        else:
            file_folder_param.append(param)
    return file_folder_param
