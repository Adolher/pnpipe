import os

import utils


class Dataset:
    def __init__(self, pattern):
        self.dataset_path = utils.get_path(pattern)
        if self.dataset_path == "":
            exit()
        self.dataset_description = utils.get_json(self.dataset_path, "dataset_description")
        self.raedme = utils.get_txt(self.dataset_path, "readme", "Readme", "README")
        self.changes = utils.get_txt(self.dataset_path, "changes", "Changes", "CHANGES")
        self.license = utils.get_txt(self.dataset_path, "license", "License", "LICENSE")
        self.participants = utils.sort_dict(utils.get_tsv_or_json(self.dataset_path, "participants"))
        self.samples_tsv = utils.get_tsv(self.dataset_path, "samples")  # ToDo: merge samples in 1 dict
        self.samples_json = utils.get_json(self.dataset_path, "samples")
        self.subjects = self.__read_subjects()

        self.is_bids = False

    def get_dataset_path(self) -> str:
        return self.dataset_path

    def get_dataset_description(self) -> dict:
        return self.dataset_description

    def get_readme(self) -> str:
        return self.raedme

    def get_changes(self) -> str:
        return self.changes

    def get_license(self) -> str:
        return self.license

    def get_participants(self) -> dict:
        return self.participants

    def get_samples(self):
        return self.samples_tsv, self.samples_json

    def __read_subjects(self):
        tmp_subjects = {}
        for participant in self.participants:
            path = os.path.join(self.dataset_path, participant)
            tmp_subjects[participant] = Subject(path, participant, self.participants[participant])
        return tmp_subjects

    def get_subject_str(self, subject_id) -> str:
        return self.subjects[subject_id].__str__()

    def get_subject_obj(self, subject_id) -> object:
        return self.subjects[subject_id].__repr__()

    def get_subjects(self):
        return self.subjects


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

    def __read_sessions(self):
        has_sessions = False
        sessions = {}
        content = os.listdir(self.subject_path)
        for i in content:
            if i.startswith("ses-"):
                has_sessions = True
                sessions[i] = self.read_session(os.path.join(self.subject_path, i))
        if has_sessions:
            return sessions
        else:
            sessions["ses-01"] = self.read_session(self.subject_path)
            return sessions

    def read_session(self, path):
        ses_directories = {}
        content = os.listdir(path)
        for i in content:
            ses_directories[i] = os.listdir(os.path.join(path, i))
        return ses_directories
