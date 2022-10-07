

class Carrier:
    def __init__(self, name) -> None:
        self.__name = name
        self.command = self.__get_command()

    @property
    def name(self):
        return self.__name

    def __get_command(self) -> str:
        return ""
