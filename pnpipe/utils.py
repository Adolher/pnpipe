import os
import json
import csv
import sys


def get_path(kwargs):
    cwd = os.getcwd()
    path_list = []
    visited = []
    set_path = False
    if "path" not in kwargs.keys():
        start = cwd
    else:
        start = kwargs["path"]
        set_path = True
    pattern = None if "pattern" not in kwargs.keys() else kwargs["pattern"]
    os.chdir(start)

    def search(path):
        nonlocal cwd
        nonlocal start
        nonlocal path_list
        nonlocal visited
        visited.append(path)
        try:
            ds = os.scandir(path)
            for d in ds:
                if pattern in d.name and d.path not in path_list:
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

    search(start)
    if len(path_list) == 1:
        return path_list[0]
    elif len(path_list) == 0:
        sys.exit("Found no object with pattern \"" + pattern + "\"!")
    else:
        sys.exit("Found more than 1 object with pattern \"" + pattern + "\"! Please specify your search!")
    # ToDo: exit() with number and catch it later


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


def sort_dict(dictionary):
    sorted_dictionary = {}
    keys = dictionary.keys()
    keys = sorted(keys)
    for key in keys:
        sorted_dictionary[key] = dictionary[key]
    return sorted_dictionary
