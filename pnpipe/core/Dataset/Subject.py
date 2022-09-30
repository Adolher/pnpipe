import os


class Subject:
    def __init__(self, path, subject_id, attributes):
        self.subject_path = path
        self.subject_id = subject_id
        self.subject_attributes = attributes
        self.sessions = self.__read_sessions()

        self.is_bids = False

    def __str__(self):
        msg = """
        Participant ID: {}
        Path:           {}
        Attributes:     {}
        BIDS:           {}"""
        return msg.format(self.subject_id, self.subject_path, self.subject_attributes, self.is_bids)

    def get_subject_path(self):
        return self.subject_path

    def get_subject_id(self):
        return self.subject_id

    def get_subject_attributes(self):
        return self.subject_attributes

    def get_sessions(self):
        return self.sessions

    def get_subject_obj(self) -> object:    # ToDo: is it necessary?
        return self.__repr__()

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
