from enum import Enum

class Datatype(Enum):
    
    DEFAULT = 0 # Default type, for no logic

    FIRST_NAME = 1
    LAST_NAME = 2
    FULL_NAME = 3
    COMPANY_NAME = 4
    STREET = 5
    STREET_HOUSENUMBER = 6
    HOUSENUMBER = 19
    TOWN = 7
    PLZ = 8
    MONEY = 9
    INTEGER = 10
    FLOAT = 11
    DATE = 12
    TIME = 13
    DATE_TIME = 14
    VALUES = 15
    FORMAT_STRING = 16
    RANDOM_STRING = 17
    PRIMARY_KEY = 20

    # Types for fields dependend on fields from other tables. Logic accounts for these to have values >= 2000
    FOREIGN_KEY = 2001
    LOWERTHAN_DATE = 2002
    HIGHERTHAN_DATE = 2003
    LOWERTHAN_INTEGER = 2004
    HIGHERTHAN_INTEGER = 2005
    LOWERTHAN_FLOAT = 2006
    HIGHERTHAN_FLOAT = 2007