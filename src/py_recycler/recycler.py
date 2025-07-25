import os
import time
import shutil
from .prompt import Prompt
from clib import recycle_api as crapi


class Recycler:
    def __init__(self, iop: dict[str, any]):
        self.call_path = iop["call_path"]
        self.buffer_bin_path = iop["buffer_bin_path"]
        self.prompt = iop["prompt"]
        self.buffer_file = iop["buffer_file"]

    def __resolve_path(self, file_path: str) -> dict[str]:
        """
        # This method examines the file path to determine
        # if it contains a regex pattern or wildcard.
        # If it does, it returns a dictionary mapping each
        # matching file's absolute path to its destination path.
        """
        # NOTE: Rephrased by Copilot.

        paths = {}

        if file_path == "." or file_path == "*":
            contents = os.listdir(self.call_path)
            for item in contents:
                destination = os.path.join(self.buffer_bin_path,
                                           str(int(time.time() * 1000)),
                                           os.path.basename(self.call_path))
                paths[os.path.join(self.call_path, item)] = destination

        elif file_path == "./" or file_path == ".\\":
            contents = os.listdir(self.call_path)
            for item in contents:
                destination = os.path.join(self.buffer_bin_path,
                                           str(int(time.time() * 1000)),
                                           os.path.basename(self.call_path))
                paths[os.path.join(self.call_path, item)] = destination

        else:
            # TODO: Add regex and wildcard supoort
            # TODO: Add validation for file_path
            destination = os.path.join(self.buffer_bin_path,
                                       str(int(time.time() * 1000)),
                                       file_path)
            paths[os.path.join(self.call_path, file_path)] = destination

        return paths

    def move_to_buffer_bin(self, file_path: str):
        destinies = self.__resolve_path(file_path)
        for path in destinies.keys():
            try:
                # shutil.move(path, destinies[path])
                self.prompt.say(f"Moving {path} to buffer bin: {
                                destinies[path]}")
            except Exception as e:
                self.prompt.say(f"Error moving {path} to buffer bin: {e}")

    def move_to_recycle_bin(self, file_path: str):
        print("Move to recycler bin called")

    def check_buffer_bin(self) -> list:
        print("Check buffer bin called")

    def recover_from_buffer_bin(self, file_path: str, prompt: Prompt) -> bool:
        print("Rover from buffer bin called")

    def empty_buffer_bin(self, prompt: Prompt) -> bool:
        print("Empty buffer bin called")

    def check_recycle_bin(self) -> list:
        print("Check recycle bin called")
