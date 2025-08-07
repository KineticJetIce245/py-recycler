from .prompt import Prompt
from .recycler import Recycler
from .config import modify


def display_help(prompt: Prompt):
    prompt.say("""usage:
    recycle: rc <file/folder> [<file/folder> ...]
    empty buffer bin: rc [-e | --empty=<true/false>]
    empty recycle bin: rc [-x | --emptyrecycle=<true/false>]
    modify config file: rc [-c | --config=<true/false>]
<name> <value>
    recover files from buffer bin: rc [-r | --recovery=<true/false>]
<file/folder> [<file/folder> ...]
    display help: rc [-h | --help=<true/false>]
    options: [-s | --silent=<true/false>] [-l | --log=<true/false>]
[-y | --yes=<true/false>] [-b | --buffer=<true/false>]
    """)
    pass


def mainCycle(prompt: Prompt):
    pass


def run(rop: dict[str, any]):
    """
    # This function first determines the operation mode
    # then analyzes the parameters.
    """
    conflicting_options = {
        "empty", "emptyrecycle",
        "recovery", "config", "help"
    }
    flags_received = 0
    for keys in conflicting_options:
        flags_received += rop["options"][keys]
    if (flags_received > 1):
        rop["prompt"].say("Conflicting options received.")
        exit(1)

    # Case help
    if (rop["options"]["help"]):
        display_help(rop["prompt"])

    elif (rop["options"]["undo"]):
        pass

        # Case empty buffer bin
    elif (rop["options"]["empty"]):
        rop["recycler"].empty_buffer_bin()

    # Case empty recycle bin
    elif (rop["options"]["emptyrecycle"]):
        rop["recycler"].empty_recycle_bin()

    # Case recovery
    elif (rop["options"]["recovery"]):
        rop["recycler"].recover_files(
            rop["parameters"])

    # Case view
    elif (rop["options"]["view"]):
        if len(rop["parameters"]) == 0:
            rop["recycler"].view_buffer_bin()
        else:
            for name in rop["parameters"]:
                rop["recycler"].view_buffer_bin(name)

    # Case Configuration
    elif (rop["options"]["config"]):
        if (len(rop["parameters"]) > 2):
            rop["prompt"].say(
                "Configuration mode accepts only two parameters.")
            exit(1)
        elif (len(rop["parameters"]) == 0):
            rop["prompt"].say(rop["options"])
        elif (len(rop["parameters"]) == 1):
            rop["prompt"].say(rop["options"][rop["parameters"][0]])
        else:
            modify(rop["conf_file"],
                   rop["parameters"][0], rop["parameters"][1])

    else:
        if (len(rop["parameters"]) == 0):
            mainCycle(rop["prompt"])  # launch the application mode
        else:
            for file_path in rop["parameters"]:
                if (rop["options"]["buffer"]):
                    rop["recycler"].move_to_buffer_bin(file_path)
                else:
                    rop["recycler"].move_to_recycle_bin(file_path)
