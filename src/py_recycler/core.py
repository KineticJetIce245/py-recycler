from .prompt import Prompt
from .recycler import Recycler
from .config import modify


def display_help(prompt: Prompt):
    prompt.say("""Recycles files/folders to buffer bin or to recycle bin
(default depends on the \033[38;5;2mconfig.toml\033[0m file), using -b option
to reverse the option:
    rc <file/folder> [<file/folder> ...]

Sends everything in buffer bin to recycle bin, files/folders
sent to recycle bin \033[38;5;1mcan not\033[0m be recovered with this program:
    rc [-e | --empty=<true/false>]

\033[38;5;1mPERMANENTLY\033[0m deletes all files/folders in recycle bin:
    rc [-x | --emptyrecycle=<true/false>]

Modifies the config file, when no name or value is specified,
prints the current configuration, when only name is specified,
prints the value of the name, when both name and value are specified,
modifies the value of the name:
    rc [-c | --config=<true/false>] [<name> <value>]

Recovers files from buffer bin, when files/folders are not specified it
recovers last file/folder sent to buffer bin:
    rc [-r | --recovery=<true/false>] [<file/folder> ...]

Shows files in buffer bin, when files/folders are not specified, it shows all
in buffer bin:
    rc [-v | --view=<true/false>] [<file/folder> ...]

Display this help message:
    rc [-h | --help=<true/false>]

Options:
    [-s | --silent=<true/false>] [-l | --log=<true/false>] [-y | --yes=<true/false>]
    [-b | --buffer=<true/false>]""")


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

        # Case empty buffer bin
    elif (rop["options"]["empty"]):
        rop["recycler"].empty_buffer_bin()

    # Case empty recycle bin
    elif (rop["options"]["emptyrecycle"]):
        rop["recycler"].empty_recycle_bin()

    # Case recovery
    elif (rop["options"]["recovery"]):
        if rop["parameters"] is None or len(rop["parameters"]) == 0:
            rop["recycler"].recover_from_buffer_bin()
        else:
            rop["recycle"].recover_from_buffer_bin(rop["parameters"])

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
            display_help(rop["prompt"])
        else:
            for file_path in rop["parameters"]:
                if (rop["options"]["buffer"]):
                    rop["recycler"].move_to_buffer_bin(file_path)
                else:
                    rop["recycler"].move_to_recycle_bin(file_path)
