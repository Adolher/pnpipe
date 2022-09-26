import json

from DataSet import Dataset

ds = Dataset("ds")
print(ds.get_dataset_description()["Name"])
# print(json.dumps(ds.dataset_overview, indent=4))
