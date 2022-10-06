import json, os

from core.Dataset.DataSet import Dataset
from core.Dataset.dataset_utils import Utils

dataset = Dataset(saved_dataset="221")
subject = dataset.subjects["sub-010001"]
print(subject.subject_attributes)
# print(json.dumps(subject.get_sessions(), indent=2))

# print(dataset.save_dataset())
# print(Utils.read_saved_datasets())
