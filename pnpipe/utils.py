import os
import json
import csv


class NothingFoundError(Exception):
    pass


def prepare_file(file):
    if "sub-" in file.name:
        splitted_name = file.name.split("_")
        name = "_".join(splitted_name[1:])
        return name, {}
    else:
        return file.name, {}


cwd = os.getcwd()


def get_path(pattern, path=None):
    global cwd
    localized_path = ""
    try:
        ds = os.scandir(path)
        path = cwd if path is None else path
        for d in ds:
            if pattern in d.name:
                localized_path = d.path
                return localized_path
            elif d.is_dir():
                localized_path = get_path(pattern, d.path)
        if cwd == path and len(localized_path) == 0:
            os.chdir("..")
            if cwd == os.getcwd():
                raise NothingFoundError
            else:
                cwd = os.getcwd()
            localized_path = get_path(pattern, os.getcwd())
    except PermissionError:
        pass
    except NothingFoundError:
        print("No dataset found")
    finally:
        return localized_path


def merge(dictionary_, list_, merged_dictionary):
    for item in list_:
        for entry in dictionary_:
            if entry.startswith(item):
                if item not in merged_dictionary.keys():
                    merged_dictionary[item] = {"count": 1, "content": {}}
                else:
                    merged_dictionary[item]["count"] += 1
                if len(dictionary_[entry]) > 0:
                    sub_list = []
                    for sub_entry in dictionary_[entry]:
                        sub_list.append(sub_entry)
                    merged_dictionary[item]["content"] = \
                        merge(dictionary_[entry], sub_list, merged_dictionary[item]["content"])

    return merged_dictionary


def shrink(dictionary):
    dir_list1 = list(dictionary.keys())
    dir_list2 = dir_list1.copy()
    shrunk = []
    for dir1 in dir_list1:
        tmp_dir_name = ""
        for dir2 in dir_list2:
            for x in range(2, min(len(dir1), len(dir2)) + 1):
                if dir1[:x] == dir2[:x]:
                    tmp_dir_name = dir1[:x]
        b = False
        for entry in shrunk:
            if tmp_dir_name.startswith(entry):
                b = True
                break
            elif entry.startswith(tmp_dir_name):
                shrunk.pop(shrunk.index(entry))
                shrunk.append(tmp_dir_name)
                b = True
                break
        if tmp_dir_name not in shrunk and not b:
            shrunk.append(tmp_dir_name)

    if len(dictionary) == len(shrunk):
        return dictionary
    else:
        shrunk_dict = {}
        shrunk_dict = merge(dictionary, shrunk, shrunk_dict)
        return shrunk_dict


def get_json(path, pattern):
    if not pattern.endswith(".json"):
        pattern += ".json"
    try:
        with open(os.path.join(path, pattern)) as json_file:
            content = json.load(json_file)
            return content
    except FileNotFoundError:
        return


def get_tsv(path, pattern):
    content = {}
    if not pattern.endswith(".tsv"):
        pattern += ".tsv"
    try:
        with open(os.path.join(path, pattern)) as tsv_file:
            y = csv.DictReader(tsv_file, delimiter="\t")
            for x in y:
                keys = list(x.keys())
                content[x.pop(keys[0])] = x
            return content
    except FileNotFoundError:
        return


def get_tsv_or_json(path, pattern):
    content = get_tsv(path, pattern) if os.path.exists(os.path.join(path, pattern + ".tsv"))\
        else get_json(path, pattern + ".json")
    return content


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
