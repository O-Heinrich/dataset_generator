from enum import Enum

class SqlDialect(Enum):
    """
    Enumeration representing the available SQL-Dialects.
    The value 0 is the default value.
    """
    # Used by backend

    DEFAULT = 0

    POSTGRESQL = 1

def toDialect(string: str) -> SqlDialect:
    """
    Parses a given string to an SqlDialect in a case-insensitive manner.
    """
    if string.casefold() == "p".casefold():
        return SqlDialect.POSTGRESQL
    else:
        return SqlDialect[string.casefold().upper()]