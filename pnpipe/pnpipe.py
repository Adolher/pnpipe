import json

from core.Dataset.DataSet import Dataset

dataset = Dataset(pattern="ds000221")
subject = dataset.subjects["sub-010001"]

print(json.dumps(subject.get_sessions(), indent=2))
print(dataset.dataset_path)
