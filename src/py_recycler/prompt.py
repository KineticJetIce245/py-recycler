class Prompt:

    def __init__(self, silent: bool = False, log: bool = False,
                 start_up: bool = True, logloc: str = None, yes: bool = False):
        self.logloc = logloc
        self.silent = silent
        self.start_up = start_up
        self.log = log
        self.yes = yes

    def __log(self, message: str):
        with open(self.logloc, 'a') as log_file:
            log_file.write(message + '\n')

    def say(self, message: str):
        if self.silent is False:
            print(message)
        if self.log is True:
            self.__log(message)

    # Always outputs to the terminal
    def startup(self, message: str):
        if self.start_up is True:
            print(message)

    def verify(self, message: str) -> bool:
        while True:
            answer = input(message)
            if (self.yes):
                return True
            elif (answer.lower() == "y" or answer.lower() == "yes"):
                return True
            elif (answer.lower() == "n" or answer.lower() == "no"):
                return False
            else:
                print("Unrecoginzed answer, please answer with 'y' or 'n'.")

    def choice(self, check_answer, message: str) -> str:
        while True:
            answer = input(message)
            if check_answer(answer):
                return answer
            else:
                print("Unrecognized answer, try again")

    def ask(self, message: str) -> str:
        return input(message)
