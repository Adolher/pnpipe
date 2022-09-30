import json

from DataSet import Dataset

ds = Dataset(path="H:\Programme\Python\pnpipe\ds000221-master")
# print(json.dumps(ds.subjects["sub-010002"].get_sessions(), indent=2))
print(json.dumps(ds.get_participants(), indent=4))
# print(json.dumps(ds.get_participants(), indent=4))
