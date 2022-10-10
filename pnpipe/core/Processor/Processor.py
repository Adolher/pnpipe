import os
import json

from .Carrier import Carrier


class Processor:
    def __init__(self, name, carrier="bare") -> None:
        self.__name = name
        self.__carrier = carrier
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

    def run(self, dataset, subject, command, output=None) -> list[str]:
        if output is None:
            output = []
        base = ""
        base += self.commands[self.__carrier]["arguments"]
        sessions = subject.sessions.keys()
        if "None" not in sessions:
            base += self.commands["optional_arguments"]
        command = self.commands["commands"][command]["command"]
        base += command

        if self.commands["commands"][command]["dependencies"] is not None:
            for dependency in self.commands["commands"][command]["dependencies"]:
                self.run(dataset, subject, dependency, output)

        if self.__carrier == "bare":
            if "None" not in sessions:
                for ses in sessions:
                    output.append(base.format(subject.subject_id, dataset.derivatives_path,
                                              dataset.dataset_path, ses.replace("ses-", "")))
            else:
                output.append(base.format(subject.subject_id, dataset.derivatives_path, dataset.dataset_path))
        elif self.__carrier == "singularity":
            if "None" not in sessions:
                for ses in sessions:
                    output.append(base.format(dataset.dataset_path, dataset.derivatives_path, "tmp_dir", subject.subject_id,
                                              self.commands["freesurfer_license"], ses.replace("ses-", "")))
            else:
                output.append(base.format(dataset.dataset_path, dataset.derivatives_path, "tmp_dir",
                                          self.commands["freesurfer_license"]))
        return output

    def __get_command_output(self):
        # ToDo: get output of commands with observing derivatives_directory
        pass
