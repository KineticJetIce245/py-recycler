class Prompt:

    def __init__(self, silent: bool = False, log: bool = False,
                 logloc: str = None, yes: bool = False):
        self.silent = silent
        self.log = log
        self.yes = yes

    def __log(self, message: str):
        # TODO: Implement logging functionality
        pass

    def say(self, message: str):
        if self.silent is False:
            print(message)
        if self.log is True:
            self.log(message)

    def prompt(self, message: str) -> str:
        # TODO: Implement prompting functionality
        pass
