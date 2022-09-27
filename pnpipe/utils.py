import os
import json
import csv


def prepare_file(file, *pattern):
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
                print(f"No dataset {pattern} found")
                exit(1)
            else:
                cwd = os.getcwd()
            localized_path = get_path(pattern, os.getcwd())
    except PermissionError:
        pass
    finally:
        return localized_path


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
