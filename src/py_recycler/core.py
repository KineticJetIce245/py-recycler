from .prompt import Prompt
from .recycler import Recycler
from .config import modify


def display_help(prompt: Prompt):
    pass


def run(run_options: dict[str, any]):
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
        flags_received += run_options.options[keys]
    if (flags_received > 1):
        run_options.prompt.say("Conflicting options received.")
        exit(1)

    # Case help
    if (run_options.options["help"]):
        display_help(run_options.prompt)

    # Case empty buffer bin
    elif (run_options.options["empty"]):
        run_options.recycler.empty_buffer_bin(run_options.prompt)

    # Case empty recycle bin
    elif (run_options.options["emptyrecycle"]):
        run_options.recycler.empty_recycle_bin(run_options.prompt)

    # Case recovery
    elif (run_options.options["recovery"]):
        run_options.recycler.recover_files(
            run_options.params, run_options.prompt)

    # Case Configuration
    elif (run_options.options["config"]):
        if (len(run_options.parameters) > 2):
            run_options.prompt.say(
                "Configuration mode accepts only two parameters.")
            exit(1)
        modify(run_options.conf_file,
               run_options.params[0], run_options.params[1])

    else:
        if (len(run_options.params) == 0):
            mainCycle(run_options.prompt)
        else:
            pass


def mainCycle(prompt: Prompt):
    pass
