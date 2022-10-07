import unittest

from pnpipe.core.Dataset.DataSet import Dataset, NoDatasetFoundError, NotSpecificError, PathDoesNotExistError, ArgsFailError


class TestClassDataset(unittest.TestCase):
    success_test_list_pattern = [
        {"pattern": "ds000221-m"},
        {"pattern": "ds004259"},
    ]
    success_test_list_path_and_pattern = [
        {"pattern": "ds0", "path": "H:\\Programme"},
    ]
    success_test_list_path = [
        {"path": "H:\\Datasets\\ds000221-master"},
        {"path": "H:\\Datasets\\ds004259-main"},
    ]
    success_results = ["H:\\Datasets\\ds000221-master",
                       "H:\\Datasets\\ds004259-main",
                       "H:\\Programme\\Python\\pnpipe\\ds000221",
                       ]

    error_no_dataset_found_list_path = [
        {"path": "H:\\Datasets"},
        {"path": "H:\\Datasets\\ds004259-main\\sub-1"},
    ]
    error_no_dataset_found_list_pattern = [
        {"pattern": "ergfdfgnefdji"},
        {"pattern": "ds0000"},
    ]
    error_no_dataset_found_list_path_and_pattern = [
        {"path": "S:\\", "pattern": "ds0"},
        {"path": "H:\\Datasets\\ds004259-main\\sub-1", "pattern": "ds004259"},
    ]
    error_not_specific_list_pattern = [
        {"pattern": "ds"},
        {"pattern": "ds00"},
    ]
    error_not_specific_list_path_and_pattern = [
        {"path": "H:\\", "pattern": "ds"},
        {"path": "H:\\Datasets", "pattern": "ds00"},

    ]
    error_path_does_not_exist_list = [
        {"path": "H:\\ds000221"},
        {"path": "H:\\Datasets\\ds0004259-main"}
    ]

    def test_dataset_init_success_pattern(self):
        for test_kwargs in TestClassDataset.success_test_list_pattern:
            with self.subTest(test_kwargs):
                test_dataset = Dataset(pattern=test_kwargs["pattern"])
                self.assertIn(test_dataset.dataset_path, TestClassDataset.success_results)

    def test_dataset_init_success_path_and_pattern(self):
        for test_kwargs in TestClassDataset.success_test_list_path_and_pattern:
            with self.subTest(test_kwargs):
                test_dataset = Dataset(path=test_kwargs["path"], pattern=test_kwargs["pattern"])
                self.assertIn(test_dataset.dataset_path, TestClassDataset.success_results)

    def test_dataset_init_success_path(self):
        for test_kwargs in TestClassDataset.success_test_list_path:
            with self.subTest(test_kwargs):
                test_dataset = Dataset(path=test_kwargs["path"])
                self.assertIn(test_dataset.dataset_path, TestClassDataset.success_results)

    def test_dataset_init_error_no_dataset_found_list_path(self):
        for test_kwargs in TestClassDataset.error_no_dataset_found_list_path:
            with self.subTest(test_kwargs):
                self.assertRaises(NoDatasetFoundError, Dataset, path=test_kwargs["path"])

    def test_dataset_init_error_no_dataset_found_list_pattern(self):
        for test_kwargs in TestClassDataset.error_no_dataset_found_list_pattern:
            with self.subTest(test_kwargs):
                self.assertRaises(NoDatasetFoundError, Dataset, pattern=test_kwargs["pattern"])

    def test_dataset_init_error_no_dataset_found_list_path_and_pattern(self):
        for test_kwargs in TestClassDataset.error_no_dataset_found_list_path_and_pattern:
            with self.subTest(test_kwargs):
                self.assertRaises(NoDatasetFoundError, Dataset, path=test_kwargs["path"], pattern=test_kwargs["pattern"])

    def test_dataset_init_error_not_specific_list_pattern(self):
        for test_kwargs in TestClassDataset.error_not_specific_list_pattern:
            with self.subTest(test_kwargs):
                self.assertRaises(NotSpecificError, Dataset, pattern=test_kwargs["pattern"])

    def test_dataset_init_error_not_specific_list_path_and_pattern(self):
        for test_kwargs in TestClassDataset.error_not_specific_list_path_and_pattern:
            with self.subTest(test_kwargs):
                self.assertRaises(NotSpecificError, Dataset, path=test_kwargs["path"], pattern=test_kwargs["pattern"])

    def test_dataset_init_error_path_does_not_exist_list_path(self):
        for test_kwargs in TestClassDataset.error_path_does_not_exist_list:
            with self.subTest(test_kwargs):
                self.assertRaises(PathDoesNotExistError, Dataset, path=test_kwargs["path"])

    def test_dataset_init_error_args_fail_zero_args(self):
        self.assertRaises(ArgsFailError, Dataset)

    def test_dataset_init_error_args_fail_too_much_args(self):
        self.assertRaises(ArgsFailError, Dataset, path="H:\\", pattern="ds000", daved_dataset="ds000221")


if __name__ == '__main__':
    unittest.main(verbosity=2)
