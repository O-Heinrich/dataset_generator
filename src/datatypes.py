from enum import Enum

class Datatype(Enum):
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
    FOREIGN_KEY = 21 # UNSUPPORTED

    # Types for multiple dependend fields. Logic accounts for these to have values >= 1000
    ASCENDING = 1001