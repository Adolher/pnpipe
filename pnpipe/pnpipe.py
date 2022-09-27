import json

from DataSet import Dataset

ds = Dataset("ds")
print(json.dumps(ds.subjects["sub-010002"].get_sessions(), indent=2))
# print(ds.get_subject_str("sub-010222"))
# print(json.dumps(ds.get_participants(), indent=4))
