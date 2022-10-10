class Processing:
    def __init__(self, dataset, processor, command, carrier=None, executor=None):
        self.__dataset = dataset
        self.__processor = processor
        self.__carrier = carrier
        self.__command = command
        self.__executor = executor
        self.__command_list = self.__run()

    @property
    def command_list(self):
        return self.__command_list

    def __run(self) -> list:
        # print(self.__dataset.subjects["010300"].sessions.keys())
        cmd_list = list()
        for subj in self.__dataset.subjects:
            cmd_list.append(self.__processor.run(self.__dataset, self.__dataset.subjects[str(subj)], self.__command))
        return cmd_list
