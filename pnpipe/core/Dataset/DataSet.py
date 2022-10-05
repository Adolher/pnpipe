import os
import sys

from .Subject import Subject
from .dataset_utils import Utils


class NotSpecificError(Exception):
    def __init__(self, path, kwargs):
        self.path = ""
        for p in path:
            self.path += "\t" + p + "\n"
        self.kwargs_str = ""
        for kwarg in kwargs.keys():
            self.kwargs_str += "\t" + kwarg + " = " + kwargs[kwarg] + "\n"
        self.msg = "Found \n{} with \n{}\nPlease specify your search!"

    def __str__(self):
        return self.msg.format(self.path, self.kwargs_str)


class NoDatasetFoundError(Exception):
    def __init__(self, kwargs):
        if type(kwargs) == dict:
            self.kwargs_str = "with \""
            for kwarg in kwargs.keys():
                self.kwargs_str += kwarg + " = " + kwargs[kwarg]
        elif type(kwargs) == str:
            self.kwargs_str = "in \"" + kwargs
        self.msg = "Found no Dataset {}\"!"

    def __str__(self):
        return self.msg.format(self.kwargs_str)


class PathDoesNotExistError(Exception):
    def __init__(self, path):
        self.msg = "path = \"" + str(path) + "\" does not exist!"

    def __str__(self):
        return self.msg


class ArgsFailError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


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
        self.__dataset_path = self.__set_dataset_path(kwargs)
        self.dataset_description = self.__read_dataset_description()
        self.readme = Utils.get_txt(self.__dataset_path, "readme", "Readme", "README")
        self.changes = Utils.get_txt(self.__dataset_path, "changes", "Changes", "CHANGES")
        self.license = Utils.get_txt(self.__dataset_path, "license", "License", "LICENSE")
        self.participants = Utils.sort_dict(Utils.get_tsv_or_json(self.__dataset_path, "participants"))
        self.samples_tsv = Utils.get_tsv(self.__dataset_path, "samples")  # ToDo: merge samples in 1 dict
        self.samples_json = Utils.get_json(self.__dataset_path, "samples")

        self.subjects = self.__read_subjects()

        self.is_bids = False

    @property
    def dataset_path(self) -> str:
        return self.__dataset_path

    def __set_dataset_path(self, kwargs) -> str:
        if len(kwargs) < 1 or len(kwargs) > 2:
            raise ArgsFailError(self.arguments_msg)
        else:
            paths = Utils.scan_for_dataset_path(kwargs)
        if len(paths) == 1:
            if os.path.exists(paths[0]):
                return paths[0]
            else:
                raise PathDoesNotExistError(str(paths[0]))
        else:
            if len(paths) == 0:
                raise NoDatasetFoundError(kwargs)
            else:
                raise NotSpecificError(paths, kwargs)

    def __read_dataset_description(self):
        dataset_description = Utils.get_json(self.__dataset_path, "dataset_description")
        if dataset_description is None:
            msg = self.__dataset_path + "\nMISSING:\n\t'dataset_description.json"
            raise NoDatasetFoundError(msg)
        else:
            return dataset_description

    def __read_subjects(self):
        # ToDo: EITHER read from participants.tsv
        #       OR read from directories
        tmp_subjects = {}
        if self.participants is not None:
            for participant in self.participants:
                path = os.path.join(self.__dataset_path, participant)
                tmp_subjects[participant] = Subject(path, participant, self.participants[participant])
            return tmp_subjects
        else:
            return None

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
