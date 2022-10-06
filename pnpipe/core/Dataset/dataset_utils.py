import os
import json
import csv


class Utils:
    @staticmethod
    def scan_for_dataset_path(kwargs):
        def search(path):
            nonlocal cwd
            nonlocal start
            nonlocal path_list
            nonlocal visited
            visited.append(path)
            try:
                ds = os.scandir(path)
                for d in ds:
                    if pattern in d.name and d.is_dir():
                        path_list.append(d.path)
                    elif d.is_dir() and d.path not in visited and not d.name.startswith("."):
                        search(d.path)  # ToDo: don't search visited directories
                if start == path and not set_path:
                    if os.getcwd() == "/" or os.getcwd().endswith(":\\"):
                        return
                    else:
                        os.chdir("..")
                        start = os.getcwd()
                        search(start)
            except PermissionError:
                pass

        path_list = []
        if "saved_dataset" in kwargs.keys():
            searched_dataset = kwargs["saved_dataset"]
            saved_datasets = Utils.read_saved_datasets()
            if saved_datasets is not None:
                for saved_dataset in saved_datasets:
                    if searched_dataset.lower() in saved_dataset[1].lower()\
                            or searched_dataset.lower() in saved_dataset[2].lower():
                        path_list.append(saved_dataset[0])
            else:
                path_list = Utils.scan_for_dataset_path({"pattern":searched_dataset})
        elif len(kwargs.keys()) == 1 and "path" in kwargs.keys():
            path_list.append(kwargs["path"])
        else:
            cwd = os.getcwd()
            visited = []
            set_path = False
            if "path" not in kwargs.keys():
                start = cwd
            else:
                start = kwargs["path"]
                set_path = True
            pattern = None if "pattern" not in kwargs.keys() else kwargs["pattern"]
            os.chdir(start)

            search(start)
        return path_list

    @staticmethod
    def read_saved_datasets():
        path = os.sep.join(os.path.realpath(os.path.dirname(__file__)).split(os.sep)[:-2])
        pattern = "Datasets.tsv"
        ds_list = Utils.get_tsv(path, pattern, "list")
        return ds_list

    @staticmethod
    def get_json(path, pattern):
        if not pattern.endswith(".json"):
            pattern += ".json"
        try:
            with open(os.path.join(path, pattern)) as json_file:
                content = json.load(json_file)
                return content
        except FileNotFoundError:
            return None

    @staticmethod
    def get_tsv(path, pattern, out):
        content = {}
        if not pattern.endswith(".tsv"):
            pattern += ".tsv"
        try:
            if out == "dict":
                with open(os.path.join(path, pattern)) as tsv_file:
                    y = csv.DictReader(tsv_file, delimiter="\t")
                    for x in y:
                        keys = list(x.keys())
                        content[x.pop(keys[0])] = x
                    return content
            elif out == "list":
                with open(os.path.join(path, pattern), mode="r") as ds:
                    dataset_list = []
                    ds_reader = csv.reader(ds, delimiter="\t")
                    for row in ds_reader:
                        dataset_list.append(row)
                return dataset_list
        except FileNotFoundError:
            return None

    @staticmethod
    def get_tsv_or_json(path, pattern, out):
        content = Utils.get_tsv(path, pattern, out) if os.path.exists(os.path.join(path, pattern + ".tsv")) \
            else Utils.get_json(path, pattern + ".json")
        return content

    @staticmethod
    def get_txt(path, *pattern):
        content = None
        for p in pattern:
            try:
                with open(os.path.join(path, p)) as txt_file:
                    content = txt_file.read()
                    return content
            except FileNotFoundError:
                p += ".txt"
                try:
                    with open(os.path.join(path, p)) as txt_file:
                        content = txt_file.read()
                        return content
                except FileNotFoundError:
                    pass
        if content is None:
            return content

    @staticmethod
    def sort_dict(dictionary):
        if dictionary is not None:
            sorted_dictionary = {}
            keys = dictionary.keys()
            keys = sorted(keys)
            for key in keys:
                sorted_dictionary[key] = dictionary[key]
            return sorted_dictionary
        else:
            return None
