from .prompt import Prompt
from .recycler import Recycler
from .config import modify


def display_help(prompt: Prompt):
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

    # Case empty buffer bin
    elif (rop["options"]["empty"]):
        rop["recycler"].empty_buffer_bin(rop["prompt"])

    # Case empty recycle bin
    elif (rop["options"]["emptyrecycle"]):
        rop["recycler"].empty_recycle_bin(rop["prompt"])

    # Case recovery
    elif (rop["options"]["recovery"]):
        rop["recycler"].recover_files(
            rop["parameters"], rop["prompt"])

    # Case Configuration
    elif (rop["options"]["config"]):
        if (len(rop["parameters"]) > 2):
            rop["prompt"].say(
                "Configuration mode accepts only two parameters.")
            exit(1)
        modify(rop["conf_file"],
               rop["parameters"][0], rop["parameters"][1])

    else:
        if (len(rop["parameters"]) == 0):
            mainCycle(rop["prompt"])  # launch the application mode
        else:
            pass
