import unittest
import itertools

from pnpipe.core.Dataset.DataSet import Dataset, NoDatasetFoundError, NotSpecificError, PathDoesNotExistError, ArgsFailError


class MyTestCase(unittest.TestCase):
    success_test_list = [
        {},
        {"pattern": "ds000221"},
        {"pattern": "ds0", "path": "H:\\Programme"},
        {"path": "H:\\Programme\\Python\\pnpipe\\ds000221-master"},
    ]
    no_dataset_found_error_list = [
        {"path": "H:\\Programme"},
        {"pattern": "ergfdfgnefdji"},
    ]
    not_specific_error_list = [
        {"pattern": "ds"},
    ]
    path_does_not_exist_error_list = [
        {"path": "H:\\Programme\\Python\\pipe\\ds000221-master"},
    ]

    test_list = itertools.chain(success_test_list, no_dataset_found_error_list, not_specific_error_list, path_does_not_exist_error_list)

    def test_dataset_init(self):
        for test_kwargs in MyTestCase.test_list:
            with self.subTest(test_kwargs):
                if len(test_kwargs.keys()) == 1:
                    if "pattern" in test_kwargs.keys():
                        if test_kwargs in MyTestCase.no_dataset_found_error_list:
                            self.assertRaises(NoDatasetFoundError, Dataset, pattern=test_kwargs["pattern"])
                        elif test_kwargs in MyTestCase.not_specific_error_list:
                            self.assertRaises(NotSpecificError, Dataset, pattern=test_kwargs["pattern"])
                        else:
                            test_dataset = Dataset(pattern=test_kwargs["pattern"])
                            self.assertEqual(test_dataset.dataset_path, "H:\\Programme\\Python\\pnpipe\\ds000221-master")
                    elif "path" in test_kwargs.keys():
                        if test_kwargs in MyTestCase.path_does_not_exist_error_list:
                            self.assertRaises(PathDoesNotExistError, Dataset, path=test_kwargs["path"])
                        elif test_kwargs in MyTestCase.no_dataset_found_error_list:
                            self.assertRaises(NoDatasetFoundError, Dataset, path=test_kwargs["path"])
                        else:
                            test_dataset = Dataset(path=test_kwargs["path"])
                            self.assertEqual(test_dataset.dataset_path, "H:\\Programme\\Python\\pnpipe\\ds000221-master")
                elif len(test_kwargs.keys()) == 2:
                    test_dataset = Dataset(pattern=test_kwargs["pattern"], path=test_kwargs["path"])
                    self.assertEqual(test_dataset.dataset_path, "H:\\Programme\\Python\\pnpipe\\ds000221-master")
                else:
                    self.assertRaises(ArgsFailError, Dataset)


if __name__ == '__main__':
    unittest.main()
