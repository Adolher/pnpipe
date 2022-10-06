import os


class Subject:
    def __init__(self, path, subject_id, attributes):
        self.__subject_path = path
        self.__subject_id = subject_id
        self.__subject_attributes = attributes
        self.__sessions = self.__read_sessions()

        self.__is_bids = False

    def __str__(self):
        msg = """
        Participant ID: {}
        Path:           {}
        Attributes:     {}
        BIDS:           {}"""
        return msg.format(self.subject_id, self.subject_path, self.subject_attributes, self.is_bids)

    @property
    def subject_path(self):
        return self.__subject_path

    @property
    def subject_id(self):
        return self.__subject_id

    @property
    def subject_attributes(self):
        return self.__subject_attributes

    @property
    def sessions(self):
        return self.__sessions

    @property
    def is_bids(self):
        return self.__is_bids

    def __read_sessions(self):
        has_sessions = False
        sessions = {}
        content = os.listdir(self.subject_path)
        for i in content:
            if i.startswith("ses-"):
                has_sessions = True
                sessions[i] = self.__read_session(os.path.join(self.subject_path, i))
        if has_sessions:
            return sessions
        else:
            sessions["ses-01"] = self.__read_session(self.subject_path)
            return sessions

    def __read_session(self, path):
        ses_directories = {}
        content = os.listdir(path)
        for i in content:
            ses_directories[i] = os.listdir(os.path.join(path, i))
        return ses_directories
