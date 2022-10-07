import json

from core.Dataset import Dataset, Subject
from core.Processor import Processor

dataset = Dataset(path="H:\\Datasets", pattern="ds000")
subject = dataset.subjects["sub-010007"]
print(subject)
print()
micapipe = Processor("micapipe", "")
print()
ls = micapipe.run(dataset, subject, "-MPC")
for l in ls:
    print(l)
