import os
import json

from .Carrier import Carrier


class Processor:
    def __init__(self, name, carrier) -> None:
        self.__name = name
        self.carrier = Carrier(carrier)
        # ToDo: check if program exists
        # if program not exists
        # ToDo: install routine
        self.__version = self.__get_version()
        self.__command_list = []
        self.__commands = self.__get_commands()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    def __get_version(self) -> str:
        version = "XX.XX.XX"
        return version

    @property
    def command_list(self) -> list:
        return self.__command_list

    @property
    def commands(self):
        return self.__commands

    def __get_commands(self) -> dict:
        # ToDo: investigate commands without human input
        path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "commands.json")
        with open(path) as commands_file:
            commands = json.load(commands_file)
        for command in commands[self.name]["commands"].keys():
            self.__command_list.append(command)
        return commands[self.name]

    def run(self, dataset, subject, command, cl=[]) -> list[str]:
        base = self.commands["arguments"]
        command = self.commands["commands"][command]["command"]
        base += command

        if self.commands["commands"][command]["dependencies"] is not None:
            for dependency in self.commands["commands"][command]["dependencies"]:
                self.run(dataset, subject, dependency)

        cl.append(base.format(subject.subject_id, dataset.derivatives_path, dataset.dataset_path))
        return cl

    def __get_command_output(self):
        # ToDo: get output of commands with observing derivatives_directory
        pass
