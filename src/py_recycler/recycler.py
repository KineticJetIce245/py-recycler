import os
import time
import shutil
import sqlite3
from datetime import datetime
from .prompt import Prompt
from .style import TCOLORS
from clib import recycle_api as crapi


class Recycler:
    def __init__(self, iop: dict[str, any]):
        self.call_path = iop["call_path"]
        self.buffer_bin_path = iop["buffer_bin_path"]
        self.prompt = iop["prompt"]
        self.buffer_file = iop["buffer_file"]
        self.regex = iop["regex"]
        if not os.path.exists(self.buffer_bin_path):
            os.makedirs(self.buffer_bin_path, exist_ok=True)

    def __db_initialize(self, cursor: sqlite3.Cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                base TEXT NOT NULL,
                path TEXT NOT NULL,
                time INTEGER NOT NULL
            )
        ''')  # 1 for recycled, 0 for not recycled

    def __db__test(self, cursor: sqlite3.Cursor):
        cursor.execute('''
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='bin'
        ''')
        result = cursor.fetchone()
        if not result:
            self.__db_initialize(cursor)

    def __db_log(self, name: str, path: str, time: int):
        conn = sqlite3.connect(self.buffer_file)
        cursor = conn.cursor()
        self.__db__test(cursor)
        cursor.execute('''
            INSERT INTO bin (base, path, time)
            VALUES (?, ?, ?)
        ''', (name, path, time))

        conn.commit()
        conn.close()

    def __db_read_all(self):
        conn = sqlite3.connect(self.buffer_file)
        cursor = conn.cursor()
        self.__db__test(cursor)
        cursor.execute('''
            SELECT * FROM bin
        ''')
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows

    def __db_find_from_name(self, base: str):
        conn = sqlite3.connect(self.buffer_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT path, time
            FROM bin
            WHERE base = ?
        ''', (base,))
        rows = cursor.fetchall()
        conn.commit()
        conn.close()
        return rows

    def __db_clear(self):
        conn = sqlite3.connect(self.buffer_file)
        cursor = conn.cursor()
        flag = self.prompt.verify(
            "Clearing all records in the buffer bin db, are you sure? (y/n):")
        if flag:
            cursor.execute('''
                DELETE FROM bin;
            ''')
            cursor.execute('''
                UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = 'bin';
            ''')
            conn.commit()
            cursor.execute('''
                VACUUM;
            ''')
        conn.commit()
        conn.close()

    def __resolve_path(self, file_path: str) -> dict[str]:
        destinies = {}

        if self.regex:
            pass

        elif (file_path == "." or file_path == "*" or
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
            file_path = os.path.abspath(file_path)
            if not os.path.exists(file_path):
                self.prompt.say(f"{TCOLORS["error"]}Error"
                                f"{TCOLORS["style end"]}: {TCOLORS["path"]}"
                                f"{file_path}{TCOLORS["style end"]} does not exist.")
                return {}

            timestamp = int(time.time() * 1000)
            destination = os.path.join(self.buffer_bin_path,
                                       str(timestamp),
                                       os.path.basename(file_path))
            destinies[file_path] = {
                "target": destination,
                "name": os.path.basename(file_path),
                "path": file_path,
                "time": timestamp
            }

        return destinies

    def move_to_buffer_bin(self, file_path: str):
        destinies = self.__resolve_path(file_path)
        for path in destinies.keys():
            try:
                os.makedirs(os.path.dirname(
                    destinies[path]["target"]), exist_ok=True)
                shutil.move(path, destinies[path]["target"])
                self.prompt.say(f"Moving {TCOLORS["path"]}{path}"
                                f"{TCOLORS["style end"]} to buffer bin: "
                                f"{TCOLORS["path"]}"
                                f"{destinies[path]["target"]}."
                                f"{TCOLORS["style end"]}")
                self.__db_log(
                    destinies[path]["name"],
                    destinies[path]["path"],
                    destinies[path]["time"]
                )
                self.prompt.say(
                    f"{TCOLORS["success"]}Moved {TCOLORS["path"]}"
                    f"{destinies[path]["path"]}{TCOLORS["success"]}"
                    f" to buffer bin.{TCOLORS["style end"]}")
            except Exception as e:
                self.prompt.say(f"{TCOLORS["error"]}Error moving"
                                f" {TCOLORS["path"]}{path}{TCOLORS["error"]}"
                                f" to buffer bin{TCOLORS["style end"]}: {e}")

    def move_to_recycle_bin(self, file_path: str):
        destinies = self.__resolve_path(file_path)
        self.prompt.say(
            f"{TCOLORS["warning"]}Warning{TCOLORS["style end"]}"
            ": Moving files to recycle bin can not be undone by rc command.")
        for path in destinies.keys():
            flag = self.prompt.verify(
                f"Moving {TCOLORS["path"]}{destinies[path]["path"]}"
                f"{TCOLORS["style end"]} to recycle bin, are you sure? (y/n):")
            if not flag:
                self.prompt.say(
                    f"{TCOLORS["path"]}{destinies[path]["path"]}"
                    f"{TCOLORS["style end"]} will not be moved to recycle bin.")
                continue
            try:
                crapi.recycle(destinies[path]["path"])
                self.prompt.say(
                    f"{TCOLORS["success"]}Moved {TCOLORS["path"]}"
                    f"{destinies[path]["path"]}{TCOLORS["success"]}"
                    f" to recycle bin.{TCOLORS["style end"]}")
            except Exception as e:
                print(f"{TCOLORS["error"]}Error moving {TCOLORS["path"]}"
                      f"{path}{TCOLORS["error"]}to recycle bin: {e}")

    def view_buffer_bin(self, name: str = None):
        message = ""
        if name is not None:
            result = self.__db_find_from_name(name)
            if len(result) == 0:
                self.prompt.say(f"{TCOLORS["error"]}Error{TCOLORS["style end"]}"
                                f": No file with name "
                                f"{TCOLORS["success"]}{name}"
                                f"{TCOLORS["style end"]} found in buffer bin.")
                return

            message += ("File/folder with name "
                        f"{TCOLORS["success"]}{name}{TCOLORS["style end"]}:\n")
            paths = {}
            for entry in result:
                if paths.get(entry[0]) is None:
                    paths[entry[0]] = []
                paths[entry[0]].append(
                    datetime.utcfromtimestamp(int(entry[1]/1000)).strftime(
                        '%Y-%m-%d %H:%M:%S'))
            for path in paths.keys():
                message += (f"\t Moved to buffer bin from {TCOLORS["path"]}"
                            f"{path}{TCOLORS["style end"]}:\n")
                for t in paths[path]:
                    message += f"\t\t Versions: {t}\n"
            self.prompt.say(message)
            return

        db = self.__db_read_all()
        files = {}
        for entry in db:
            if files.get(entry[1]) is None:
                files[entry[1]] = {}
            if files[entry[1]].get(entry[2]) is None:
                files[entry[1]][entry[2]] = []
            files[entry[1]][entry[2]].append(
                datetime.utcfromtimestamp(int(entry[3]/1000)).strftime(
                    '%Y-%m-%d %H:%M:%S'))

        for basename in files.keys():
            message += (f"File/folder with name {TCOLORS["success"]}"
                        f"{basename}{TCOLORS["style end"]}:\n")
            for path in files[basename].keys():
                message += (f"\t Moved to buffer bin from {TCOLORS["path"]}"
                            f"{path}{TCOLORS["style end"]}:\n")
                for t in files[basename][path]:
                    message += f"\t\t Versions: {t}\n"
        self.prompt.say(message)

    def recover_from_buffer_bin(self, file_path: str = None):
        db = self.__db_read_all()

    def empty_buffer_bin(self):
        self.__db_clear()
        contents = os.listdir(self.buffer_bin_path)
        for item in contents:
            content_path = os.path.join(self.buffer_bin_path, item)
            crapi.recycle(content_path)
        self.prompt.say(f"{TCOLORS["success"]}Emptied buffer bin."
                        f"{TCOLORS["style end"]}")

    def check_recycle_bin(self) -> list:
        print("Check recycle bin called")
