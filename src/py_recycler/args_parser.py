from .prompt import Prompt


def parse_parameters(params, options, short_options) -> list:
    """
    # Parses the listed parameters,
    # adds the options to the options dictionary
    # and returns a list files to be processed.
    """
    temp_prompt = Prompt()
    file_folder_param = []

    for param in params:

        if param.startswith("--"):

            try:
                key, value = param[2:].split("=", 1)
                if (value.lower() == "false" or value.lower() == "true"):
                    options[key] = (value.lower() == "true")
                else:
                    options[key] = value
            except ValueError:
                key = param[2:]
                options[key] = True

        elif param.startswith("-"):
            if (len(param[1:]) != 1):
                temp_prompt.say(f"Invalid short option format: {param}")
                exit(1)
            elif not (param[1:] in short_options.keys()):
                temp_prompt.say(f"Invalid short option: {param}")
                exit(1)
            else:
                key = short_options[param[1:]]
                options[key] = not options[key]

        else:
            file_folder_param.append(param)

    return file_folder_param
