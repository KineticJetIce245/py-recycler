import os
import time
import shutil
import sqlite3
from .prompt import Prompt
from clib import recycle_api as crapi


class Recycler:
    def __init__(self, iop: dict[str, any]):
        self.call_path = iop["call_path"]
        self.buffer_bin_path = iop["buffer_bin_path"]
        self.prompt = iop["prompt"]
        self.buffer_file = iop["buffer_file"]
        print(self.buffer_file)

    def __initialize_db(self, cursor: sqlite3.Cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base TEXT NOT NULL,
                path TEXT NOT NULL,
                time InTEGER NOT NULL
            )
        ''')

    def __log_to_sql(self, name: str, path: str, time: int):
        conn = sqlite3.connect(self.buffer_file)
        cursor = conn.cursor()
        # look for the table named bin,
        cursor.execute('''
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='bin'
        ''')
        result = cursor.fetchone()
        if not result:
            self.__initialize_db(cursor)

        cursor.execute('''
            INSERT INTO bin (base, path, time)
            VALUES (?, ?, ?)
        ''', (name, path, time))

        conn.commit()
        conn.close()

    def __resolve_path(self, file_path: str) -> dict[str]:
        """
        # This method examines the file path to determine
        # if it contains a regex pattern or wildcard.
        # If it does, it returns a dictionary mapping each
        # matching file's absolute path to its destination path.
        """
        # NOTE: Rephrased by Copilot.

        destinies = {}

        if (file_path == "." or file_path == "*" or
                file_path == "./" or file_path == ".\\"):

            contents = os.listdir(self.call_path)
            timestamp = int(time.time() * 1000)
            for item in contents:
                destination = os.path.join(self.buffer_bin_path,
                                           str(timestamp),
                                           os.path.basename(self.call_path),
                                           item)
                destinies[os.path.join(self.call_path, item)] = {
                    "target": destination,
                    "name": item,
                    "path": os.path.join(self.call_path, item),
                    "time": timestamp
                }

        else:
            timestamp = int(time.time() * 1000)
            destination = os.path.join(self.buffer_bin_path,
                                       str(timestamp),
                                       file_path)
            destinies[os.path.join(self.call_path, file_path)] = [
                destination, timestamp]

        return destinies

    def move_to_buffer_bin(self, file_path: str):
        destinies = self.__resolve_path(file_path)
        for path in destinies.keys():
            try:
                os.makedirs(os.path.dirname(
                    destinies[path]["target"]), exist_ok=True)
                shutil.move(path, destinies[path]["target"])
                self.prompt.say(f"Moving {path} to buffer bin: {
                                destinies[path]}")
                self.__log_to_sql(
                    destinies[path]["name"],
                    destinies[path]["path"],
                    destinies[path]["time"]
                )
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
