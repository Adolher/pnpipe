import os

import utils


class Dataset:
    def __init__(self, pattern):
        self.dataset_path = utils.get_path(pattern)
        self.dataset_description = utils.get_json(self.dataset_path, "dataset_description")
        self.raedme = utils.get_txt(self.dataset_path, "readme", "Readme", "README")
        self.changes = utils.get_txt(self.dataset_path, "changes", "Changes", "CHANGES")
        self.license = utils.get_txt(self.dataset_path, "license", "License", "LICENSE")
        self.participants = utils.get_tsv_or_json(self.dataset_path, "participants")
        self.samples_tsv = utils.get_tsv(self.dataset_path, "samples")      # ToDo: merge samples in 1 dict
        self.samples_json = utils.get_json(self.dataset_path, "samples")
        self.subjects = None

        self.is_bids = False

        self.not_to_shrink = ["ses-", ]
        self.dataset_overview, self.full_dataset = \
            self._prepare_dataset_overview(os.scandir(self.dataset_path), {}, {})

    def get_dataset_path(self):
        return self.dataset_path

    def get_dataset_description(self):
        return self.dataset_description

    def get_readme(self):
        return self.raedme

    def get_changes(self):
        return self.changes

    def get_license(self):
        return self.license

    def get_participants(self):
        return self.participants

    def get_samples(self):
        return self.samples

    def get_dataset_overview(self):
        return self.dataset_overview

    def print_dataset_overview(self, exclude):
        def print_entry(dictionary, c):
            msg = "{}{:<4}x {}"
            for data in dictionary:
                if len(dictionary[data]["content"]) == 0:
                    if not data.endswith(exclude):
                        print(msg.format(c * "  ", dictionary[data]["count"], data))
                else:
                    if not data.endswith(exclude):
                        print(msg.format(c * "  ", dictionary[data]["count"], data))
                    print_entry(dictionary[data]["content"], c+1)
        print_entry(self.dataset_overview, 0)

    def get_full_dataset(self):
        return self.full_dataset

    def print_full_dataset(self):
        pass

    def _prepare_dataset_overview(self, content, overview_dict, full_dict):
        is_dir = 0
        to_shrink = False
        for c in content:
            if c.is_file():
                name, value = utils.prepare_file(c)
                overview_dict.update({name: {}})
                full_dict.update({c.name: value})
            elif c.is_dir():
                overview_dict[c.name] = {}
                full_dict[c.name] = {}
                overview_dict[c.name], full_dict[c.name] = \
                    self._prepare_dataset_overview(os.scandir(c.path), overview_dict[c.name], full_dict[c.name])
                to_shrink = True
                for clause in self.not_to_shrink:
                    if c.name.startswith(clause):
                        to_shrink = False
                is_dir += 1
        if is_dir >= 2 and to_shrink:
            x = utils.shrink(overview_dict)
        else:
            x = overview_dict
        return x, full_dict


class Subject:
    def __init__(self):
        self.is_bids = False
