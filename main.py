"""
# Handles application initialization:
#   1. Loads the configuration file
#   2. Parses command-line flags and applies corresponding options
#   3. Invokes src.py_recycler.core
"""
import sys
import os
from src.py_recycler import config
from src.py_recycler import core
from src.py_recycler import prompt
from src.py_recycler import args_parser
from src.py_recycler import style
from src.py_recycler import recycler

SHORT_OPTION = {
    "u": "undo",
    "h": "help",
    "e": "empty",
    "x": "emptyrecycle",
    "c": "config",
    "r": "recovery",
    "v": "view",
    "s": "silent",
    "l": "log",
    "b": "buffer",
    "y": "yes",
    "w": "regex",
}
options = {
    # Special mode (undo): undoing the last recycle operation
    "undo": False,
    # Special mode (help): displaying help message
    "help": False,
    # Special mode (empty): not receiving any file/folder paths
    "empty": False,         # If true, empties files in buffer bin
    "emptyrecycle": False,  # If true, permernant delet files in recycle bin
    # Speical mode (config): receiving configuration entries
    "config": False,        # If true, enable config mode
    # Special mode (recovery): receiving file/folder paths in buffer bin
    "recovery": False,      # If true, recover files from the buffer bin
    # Special mode (view): viewing files in buffer bin
    "view": False,
    # Output flags
    "silent": False,        # If true, no output will be printed to the console
    "log": False,           # If true, output will be written to a log file
    # Normal mode
    "buffer": False,        # If true, first sends files to buffer bin
    "yes": False,           # If true, yes will be assumed for all prompts
    "regex": False,         # If true, regex will be used for file matching
}

"""
# Initialization
# Actual parameters start from the third argument onward
# First argument: path to the script
# Second argument: script's directory
# Third argument: directory from which the script was invoked
"""
input_params = sys.argv
if len(input_params) < 3:
    print("Launch parameters do not match expectation, check 'rc.bat'.")
    exit(1)

"""
# Load configuration
# Parse command-line arguments
# Create Prompt instance
# Create Recycler instance
"""
conf = config.load(os.path.join(input_params[1], "config.toml"))
for key in conf["options"].keys():
    options[key] = conf["options"][key]

params = args_parser.parse_parameters(input_params[3:], options, SHORT_OPTION)
permn_prompt = prompt.Prompt(silent=options["silent"], log=options["log"],
                             start_up=conf["start_up"]["enable"],
                             logloc=os.path.join(
                                 input_params[1], conf["path"]["log_file"]),
                             yes=options["yes"])

permn_prompt.startup(f"{style.TCOLORS["tip"]}{
    conf["start_up"]["message"].replace("[loc]", os.path.join(input_params[1], "config.toml"))}{
    style.TCOLORS["style end"]}")

if conf["path"]["under_userprofile"]:
    buffer_bin_path = os.path.join(
        os.environ["USERPROFILE"], conf["path"]["buffer_bin"])
else:
    buffer_bin_path = conf["path"]["buffer_bin"]
recycler_options = {
    "call_path": input_params[2],
    "buffer_bin_path": buffer_bin_path,
    "prompt": permn_prompt,
    "buffer_file": os.path.join(input_params[1], conf["path"]["buffer_file"]),
    "regex": options["regex"],
}
recycler_instance = recycler.Recycler(recycler_options)

"""
# Run the core functionality with the provided parameters and options
"""
run_options = {
    "call_path": input_params[2],
    "parameters": params,
    "options": options,
    "recycler": recycler_instance,
    "conf_file": conf,
    "prompt": permn_prompt
}
# print(options)
# print(params)
core.run(run_options)
