from .processor_utils import Utils


class Processor:
    def __init__(self, name):
        self.__name = name
        # ToDo: check if program exists
        # if program not exists
        # ToDo: install routine
        self.__version = Utils.get_version()
        self.__commands = Utils.get_commands(self.name)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self):
        return self.__version
