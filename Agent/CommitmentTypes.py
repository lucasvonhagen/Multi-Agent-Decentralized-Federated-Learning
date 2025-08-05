
from enum import Enum, unique

@unique
class CommitmentTypes(Enum):
    TRAIN=0
    CONTRIBUTE=1
    AGGREGATE=3
    SHARE=4
    