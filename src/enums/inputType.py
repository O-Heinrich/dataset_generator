from enum import Enum, auto

class InputType(Enum):
    """
    Enumeration representing different types of data that can be input in the gui.
    """
    # Used by frontend

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
    FILE_PATH = auto()