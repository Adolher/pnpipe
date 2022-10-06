

class Utils:
    @staticmethod
    def get_version() -> str:
        version = ""
        return version

    @staticmethod
    def get_commands(processor_name) -> dict:
        """
        :param: processor_name: Name of the processing Software
        :return:
        {
            "<command>":
            {
                "command": "<command>",
                "arguments": ["<argument> {<>}, ]",
                "optional_arguments": "[<optional_argument> {<>}, ]",
            }
        }
        """
        # ToDo: read commands from commands.json
        # ToDo: investigate commands without human input
        # ToDo: get output of commands with observing derivatives_directory
        return {}
