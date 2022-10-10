import json
import os.path


class Carrier:
    def __init__(self, name) -> None:
        self.__name = name  # ToDo: check if Carrier exists
        self.__carrier_path = None  # ToDo: search Container
        self.__command = None
        self.get_carrier_info()

    @property
    def name(self):
        return self.__name

    @property
    def carrier_path(self):
        return self.__carrier_path

    @carrier_path.setter
    def carrier_path(self, path):
        if os.path.exists(path):
            self.__carrier_path = path

    @property
    def command(self):
        return self.__command

    def get_carrier_info(self) -> None:
        path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "carrier.json")
        with open(path) as info_file:
            info = json.load(info_file)
        if self.name.title() in info.keys():
            self.carrier_path = info[self.name.title()]["path"]
            self.__command = info[self.name.title()]["command"] + f"{self.carrier_path} "
        else:
            self.__command = ""
