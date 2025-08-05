from enum import Enum, unique

@unique
class MessageTypes(Enum):
    INFORM=0
    REQUEST=1
    AGREE=2
    CFP=3
    ACCEPT=4
    REJECT=5
    PROPOSE=6

