import datetime
from dialect import SqlDialect as SD
import re

from typing import Any;

def stringifyValue(any: Any, dialect: SD, sep: str=", ") -> str:
    q: str = "\"" if dialect in [SD.DEFAULT] else "'"
    if type(any) is str:
        return f'{q}{any.replace(q, f'{q}{q}')}{q}'
    elif isinstance(any, list):
        return sep.join([stringifyValue(x, dialect, sep) for x in any])
    elif isinstance(any, datetime.date):
        return f'{q}{any.strftime("%Y-%m-%d")}{q}'
    else:
        return str(any)

def stringifyName(name: str, dialect: SD) -> str:
    if dialect in [SD.POSTGRESQL]:
        reg: str = r'^[a-z\d]+$'
        return name if re.match(reg, name) else f'"{name}"'
    return name

def createInsertQuery(tableName: str, columnNames: list[str], values: list[list[Any]], dialect: SD, noNewLine: bool=False) -> str:
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