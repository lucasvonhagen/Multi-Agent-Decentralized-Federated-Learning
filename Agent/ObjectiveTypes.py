from enum import Enum, unique

@unique
class ObjectiveTypes(Enum):
    PROFIT=0
    IMPROVED_ACCURACY=1
    CONTRIBUTE=2
