"""
# Handles application initialization:
#   1. Loads the configuration file
#   2. Parses command-line flags and applies corresponding options
#   3. Invokes src.py_recycler.core
"""
import sys
import os
from src.py_recycler import config
from src.py.recycler import core
from src.py_recycler import logger
from src.py_recycler import args_parser

SHORT_OPTION = {
    "e": "empty",
    "x": "emptyrecycle",
    "c": "config",
    "r": "recovery",
    "s": "silent",
    "l": "log",
    "b": "buffer",
}
options = {
    # Special mode (empty): not receiving any file/folder paths
    "empty": False,         # If true, empties files in buffer bin
    "emptyrecycle": False,   # If true, permernant delet files in recycle bin
    # Special mode (recovery): receiving file/folder paths in buffer bin
    "recovery": False,      # If true, recover files from the buffer bin
    # Speical mode (config): receiving configuration entries
    "config": False,        # If true, enable config mode
    # Output flags
    "silent": False,        # If true, no output will be printed to the console
    "log": False,           # If true, output will be written to a log file
    # Normal mode
    "buffer": False,         # If true, first sends files to buffer bin
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
    print("Error in the launch parameters, config file location missing.")
    exit(1)

"""
# Load configuration
# Parse command-line arguments
# Create Logger instance
"""
conf = config.load(os.path.join(input_params[1], "config.toml"))
params = args_parser.parse_parameters(input_params[3:], options, SHORT_OPTION)
permn_logger = logger.Logger(silent=options["silent"], log=options["log"],
                             config=conf["path"]["log_file"])

print(conf)
print(params)
print(options)

"""
# Run the core functionality with the provided parameters and options
"""
core.run_options(params, options, permn_logger)
