import json

from core.Dataset import Dataset, Subject
from core.Processor import Processor
from core.Processing import Processing


def printj(dictionary):
    print(json.dumps(dictionary, indent=2))

dataset = Dataset(path="/data/pt_02682/MRI_MPILMBB_LEMON/MRI_Raw")
pro = Processor("micapipe", "singularity")
run = Processing(dataset, pro, "-proc_structural", "singularity")

for c in run.command_list:
    print(c)
