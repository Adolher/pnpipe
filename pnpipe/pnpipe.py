import json

from DataSet import Dataset

ds = Dataset("ds")
ds.print_dataset_overview("json")
# print(json.dumps(ds.dataset_overview, indent=4))
