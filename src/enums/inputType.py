from enum import Enum, auto

class InputType(Enum):
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    TABLE_KEY = auto()
    TABLE_COLUMN = auto()
    DATE = auto()
    TIME = auto()
    TIMEDICT = auto()
    DATEDICT = auto()
    DATETIMEDICT = auto()
    LIST_STRING = auto()
