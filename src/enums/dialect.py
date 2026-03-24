from enum import Enum

class SqlDialect(Enum):

    DEFAULT = 0

    POSTGRESQL = 1

def toDialect(string: str) -> SqlDialect:
    if string.casefold() == "p".casefold():
        return SqlDialect.POSTGRESQL
    else:
        return SqlDialect[string.casefold().upper()]