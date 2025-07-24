import os
import shutil
from .prompt import Prompt
from clib import recycle_api as crapi


def __resolve_path(call_path, file_path) -> dict[str]:
    """
    # This method examines the file path to determine
    # if it contains a regex pattern or wildcard.
    # If it does, it returns a dictionary mapping each
    # matching file's absolute path to its destination path.
    """
    # NOTE: Rephrased by Copilot.

    paths = {}

    if file_path == "." or file_path == "*":
        contents = os.listdir(call_path)
        for item in contents:
            destination = os.path.join(
                os.path.basename(call_path))
            paths[os.path.join(call_path, item)] = destination
    else:
        pass

    return paths


class Recycler:
    def __init__(self, call_path: str, buffer_bin_path: str, prompt: Prompt):
        self.call_path = call_path
        self.buffer_bin_path = buffer_bin_path

    def move_to_buffer_bin(self, file_path: str) -> bool:
        destinies = __resolve_path(self.call_path, file_path)

        for path in destinies.keys():
            shutil.move(path, destinies[path])
            pass

    def check_buffer_bin(self) -> list:
        pass

    def recover_from_buffer_bin(self, file_path: str, prompt: Prompt) -> bool:
        pass

    def empty_buffer_bin(self, prompt: Prompt) -> bool:
        pass

    def check_recycle_bin(self) -> list:
        pass
