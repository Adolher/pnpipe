import os
import csv

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
        self.__arguments_msg = \
            """
To initialize an Object of Dataset(), the following arguments MUST be specified:

        EITHER:
            dataset = Dataset(saved_dataset="pattern")
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
        self.__dataset_description = self.__read_dataset_description()
        self.__save_dataset()
        self.__readme = Utils.get_txt(self.dataset_path, "readme", "Readme", "README")
        self.__changes = Utils.get_txt(self.dataset_path, "changes", "Changes", "CHANGES")
        self.__license = Utils.get_txt(self.dataset_path, "license", "License", "LICENSE")
        self.__participants = Utils.sort_dict(Utils.get_tsv_or_json(self.dataset_path, "participants", "dict"))
        self.__samples_tsv = Utils.get_tsv(self.dataset_path, "samples", "dict")  # ToDo: merge samples in 1 dict
        self.__samples_json = Utils.get_json(self.dataset_path, "samples")
        self.__derivatives_path = None  # ToDo: get path of derivatives, look in BIDS specifications

        self.__subjects = self.__read_subjects()

        self.__is_bids = False

    @property
    def dataset_path(self) -> str:
        return self.__dataset_path

    @property
    def dataset_description(self) -> dict:
        return self.__dataset_description

    @property
    def readme(self) -> str:
        return self.__readme

    @property
    def changes(self) -> str:
        return self.__changes

    @property
    def license(self) -> str:
        return self.__license

    @property
    def participants(self) -> dict:
        return self.__participants

    @property
    def samples(self):
        return self.__samples_tsv, self.__samples_json

    @property
    def derivatives_path(self):
        return self.__derivatives_path

    @property
    def subjects(self):
        return self.__subjects

    @property
    def is_bids(self):
        return self.is_bids

    def __set_dataset_path(self, kwargs) -> str:
        if len(kwargs) < 1 or len(kwargs) > 2:
            raise ArgsFailError(self.__arguments_msg)
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
        dataset_description = Utils.get_json(self.dataset_path, "dataset_description")
        if dataset_description is None:
            msg = self.dataset_path + "\nMISSING:\n\t'dataset_description.json"
            raise NoDatasetFoundError(msg)
        else:
            return dataset_description

    def __read_subjects(self) -> dict:
        tmp_subjects = {}
        if self.participants is not None:
            for participant in self.participants:
                path = os.path.join(self.dataset_path, participant)
                participant_id = participant.replace("sub-", "")
                tmp_subjects[participant_id] = Subject(path, participant_id, self.participants[participant])
            return tmp_subjects
        else:
            for entry in os.scandir(self.dataset_path):
                if entry.is_dir() and entry.name.startswith("sub-"):
                    participant_id = entry.name.replace("sub-", "")
                    tmp_subjects[participant_id] = Subject(entry.path, participant_id)
            return tmp_subjects

    def __save_dataset(self) -> None:
        """
        Directory-Path,
        Dataset-Name ( from dataset-description.json )
        BIDS-Version ( from dataset-description.json )
        """
        ds_dir_name = self.dataset_path.split(os.sep)[-1]
        obj_to_save = [self.dataset_path, ds_dir_name,
                       self.dataset_description["Name"],
                       self.dataset_description["BIDSVersion"],
                       ]

        saved_datasets = Utils.read_saved_datasets()
        if saved_datasets is not None:
            for saved_dataset in saved_datasets:
                if obj_to_save == saved_dataset:
                    return

        path = os.path.join(os.sep.join(os.path.realpath(os.path.dirname(__file__)).split(os.sep)[:-2]), "Datasets.tsv")
        with open(path, mode="a", newline="") as ds:
            ds_writer = csv.writer(ds, delimiter="\t")
            ds_writer.writerow(obj_to_save)
