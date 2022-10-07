import json

from core.Dataset import Dataset, Subject
from core.Processor import Processor


def printj(dictionary):
    print(json.dumps(dictionary, indent=2))


dataset = Dataset(path="H:\\Datasets", pattern="ds000")
subject = dataset.subjects["010003"]
pro = Processor("micapipe", "bare")
li = pro.run(dataset, subject, "-proc_rsfmri")
for lis in li:
    print(lis)
