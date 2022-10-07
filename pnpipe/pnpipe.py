import json

from core.Dataset import Dataset, Subject
from core.Processor import Processor

dataset = Dataset(path="H:\\Datasets", pattern="ds004")
subject = dataset.subjects["1"]

print(type(dataset.subjects))
for subject_id, subject in dataset.subjects.items():
    print(subject_id, subject)
