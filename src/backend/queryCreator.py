import datetime
from enums.dialect import SqlDialect as SD
import re
from typing import Any, Iterable

def stringifyValue(any: Any, dialect: SD, sep: str=", ") -> str:
    """Turns a value into a raw string that can be part of the SQL-Query, fitting the dialect given."""
    q: str = "\"" if dialect in [SD.DEFAULT] else "'"
    if type(any) is str:
        return f'{q}{any.replace(q, f'{q}{q}')}{q}'
    elif isinstance(any, list):
        return sep.join([stringifyValue(x, dialect, sep) for x in any])
    elif isinstance(any, datetime.datetime):
        return f'{q}{any.strftime("%Y-%m-%d %H:%M:%S")}{q}'
    elif isinstance(any, datetime.date):
        return f'{q}{any.strftime("%Y-%m-%d")}{q}'
    elif isinstance(any, datetime.time):
        return f'{q}{any.strftime("%H:%M:%S")}{q}'
    else:
        return str(any)

def stringifyName(name: str, dialect: SD) -> str:
    """Turns the name of a table or column into a raw string that can be part of the SQL-Query, fitting the dialect given."""
    if dialect in [SD.POSTGRESQL]:
        reg: str = r'^[a-z\d]+$'
        return name if re.match(reg, name) else f'"{name}"'
    return name

def createInsertQuery(tableName: str, columnNames: Iterable[str], values: list[list[Any]], dialect: SD, noNewLine: bool=False) -> str:
    """
    Creates an SQL-query from given values, fitting the dialect given.
    This works independent from other logic.
    """
    # Any changes to the actual output string and dialects should happen in here or the used functions
    query: str

    if dialect in [SD.DEFAULT, SD.POSTGRESQL]:
        query = "INSERT INTO "
    else:
        raise NotImplementedError()

    query += stringifyName(tableName, dialect)

    query += " ("
    query += ", ".join([stringifyName(n, dialect) for n in columnNames])
    query += ") "

    query += "VALUES"

    query += " " if noNewLine else "\n"

    datasetStrings: list[str] = [", ".join([stringifyValue(v, dialect) for v in dv]) for dv in values]
    datasetStrings = [f'({ds})' for ds in datasetStrings]
    valuesSeperator: str = ", " if noNewLine else ",\n"
    query += valuesSeperator.join(datasetStrings)

    query += ";"
    return query