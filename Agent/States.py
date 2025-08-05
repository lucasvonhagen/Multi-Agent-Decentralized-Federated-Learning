#Defining possible states for agents
from enum import Enum, unique

@unique
class States(Enum):
    EXIT=0
    REGISTRATION=1
    DISCOVERY=2
    NEGOTIATION_FEDERATION=3
    TRAINING=4
    EVALUATION=5
    REWARDING=6
