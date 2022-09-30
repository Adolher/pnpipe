import os
import sys

from .Subject import Subject
from .dataset_utils import Utils


class Dataset:
    def __init__(self, **kwargs):
        self.arguments_msg = \
            """
To initialize an Object of Dataset(), the following arguments MUST be specified:

        EITHER:
            dataset = Dataset(dataset_json="<dataset name>.json")
        OR:
            EITHER:
                dataset = Dataset(path="x:\\path\\to\\dataset-directory-name")  (Windows)
                dataset = Dataset(path="/path/to/dataset-directory-name")       (Linux)
            OR:
                dataset = Dataset(pattern="ds000221")
                    # search on WHOLE STORAGE for a directory with "ds000221" in directory-name
                    # if 1 directory is found: return the directory-path
                    # if nothing found: sys.exit()
                    # if >1 found: sys.exit()
            OR:
                dataset = Dataset(path="X:\\path", pattern="ds000221")  (Windows)
                dataset = Dataset(path="/path", pattern="ds000221")     (linux)
                    # search in SPECIFIED PATH for a directory with "ds000221" in directory-name
                    # if 1 directory is found: return the directory-path
                    # if nothing found: sys.exit()
                    # if >1 found: sys.exit()
        """

        self.dataset_path = self.__set_dataset_path(kwargs)
        self.dataset_description = self.__read_dataset_description()
        self.readme = Utils.get_txt(self.dataset_path, "readme", "Readme", "README")
        self.changes = Utils.get_txt(self.dataset_path, "changes", "Changes", "CHANGES")
        self.license = Utils.get_txt(self.dataset_path, "license", "License", "LICENSE")
        self.participants = Utils.sort_dict(Utils.get_tsv_or_json(self.dataset_path, "participants"))
        self.samples_tsv = Utils.get_tsv(self.dataset_path, "samples")  # ToDo: merge samples in 1 dict
        self.samples_json = Utils.get_json(self.dataset_path, "samples")

        self.subjects = self.__read_subjects()

        self.is_bids = False

    def __set_dataset_path(self, kwargs):
        if len(kwargs) == 0:
            sys.exit(self.arguments_msg)
            # ToDo: exit() with number and catch it in UI
        else:
            paths = Utils.get_dataset_path(kwargs)
        if len(paths) == 1:
            if os.path.exists(paths[0]):
                return paths[0]
            else:
                sys.exit("path = \"" + str(paths[0]) + "\" does not exist!")
                # ToDo: exit() with number and catch it in UI
        else:
            kwargs_str = "\n"
            for kwarg in kwargs.keys():
                kwargs_str += "\t" + kwarg + " = " + kwargs[kwarg] + "\n"
            if len(paths) == 0:
                sys.exit("Found no object with \"" + str(kwargs) + "\"!")
                # ToDo: exit() with number and catch it in UI
            else:
                paths_string = "\n"
                for p in paths:
                    paths_string += "\t" + p + "\n"
                sys.exit("Found " + paths_string + " with" + kwargs_str + "\nPlease specify your search!")
                # ToDo: exit() with number and catch it in UI

    def __read_dataset_description(self):
        dataset_description = Utils.get_json(self.dataset_path, "dataset_description")
        if dataset_description is None:
            sys.exit("In " + self.dataset_path + " is no Dataset!\nMISSING:\n\t'dataset_description.json")
            # ToDo: exit() with number and catch it in UI
        else:
            return dataset_description

    def __read_subjects(self):
        # ToDo: EITHER read from participants.tsv
        #       OR read from directories
        tmp_subjects = {}
        if self.participants is not None:
            for participant in self.participants:
                path = os.path.join(self.dataset_path, participant)
                tmp_subjects[participant] = Subject(path, participant, self.participants[participant])
            return tmp_subjects
        else:
            return None

    def get_dataset_path(self) -> str:
        return self.dataset_path

    def get_dataset_description(self) -> dict:
        return self.dataset_description

    def get_readme(self) -> str:
        return self.readme

    def get_changes(self) -> str:
        return self.changes

    def get_license(self) -> str:
        return self.license

    def get_participants(self) -> dict:
        return self.participants

    def get_samples(self):
        return self.samples_tsv, self.samples_json

    def get_subjects(self):
        return self.subjects
