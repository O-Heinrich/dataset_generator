from enum import Enum

class Datatype(Enum):
    """
    Enumeration representing datatypes of table columns.
    The value 0 is the default value and dependend types do have values greater or equal 2000.
    """
    # Used by both backend and frontend
    
    DEFAULT = 0 # Default type, for no logic

    PRIMARY_KEY = 1

    FIRST_NAME = 51
    LAST_NAME = 52
    FULL_NAME = 53
    COMPANY_NAME = 54

    STREET = 101
    HOUSENUMBER = 102
    STREET_HOUSENUMBER = 103
    TOWN = 104
    PLZ = 105

    INTEGER = 151
    FLOAT = 152
    MONEY = 153

    DATE = 201
    TIME = 202
    DATE_TIME = 203

    VALUES = 251
    CYCLING_VALUES = 252
    SHUFFLED_VALUES = 253

    FORMAT_STRING = 1001
    RANDOM_STRING = 1002
    COUNTING = 1003

    # Types for fields dependend on fields from other tables. Logic accounts for these to have values >= 2000
    FOREIGN_KEY = 2001

    LOWERTHAN_INTEGER = 2051
    HIGHERTHAN_INTEGER = 2052
    LOWERTHAN_FLOAT = 2053
    HIGHERTHAN_FLOAT = 2054

    LOWERTHAN_DATE = 2101
    HIGHERTHAN_DATE = 2102
    LOWERTHAN_TIME = 2103
    HIGHERTHAN_TIME = 2104
    LOWERTHAN_DATETIME = 2105
    HIGHERTHAN_DATETIME = 2106