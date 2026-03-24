from faker import Faker
from wonderwords import RandomWord
from backend.tableModel import TableModel
import os
import traceback
import exceptions.exceptions as exceptions
from backend.column import Column
from enums.datatypes import Datatype as Dt
from backend.columnListener import ColumnListener
from enums.dialect import SqlDialect as SD

from typing import Any, Union, Optional

def generateData(
        json: Union[list[dict[str, Any]], dict[str, Any]], # json input according to documentation
        targetFilePath: Optional[str]=None, # Filepath where the query will be written. Generates a random filename if None
        filemode: str="x", # Mode in which to write the file
        noNewLine: bool=False, # Currently not implemented
        localization: str="de_DE", # localization according to https://faker.readthedocs.io/en/master/#localization
        encoding: str="utf-8", # encoding in which to write the file
        dialect: SD=SD.DEFAULT
) -> Optional[str]:
    """
    API for generating SQL-Queries
    Generates all queries according to the given json and Parameters
    Returns the path under which the file was stored, or None on failure
    """
    r: RandomWord = RandomWord()
    targetPath: str = targetFilePath or r.word() + "_" + r.word() + "_" + r.word() + ".sql"
    fake: Faker = Faker(localization)

    tables: dict[str, TableModel] = createTables(json, fake, noNewLine=noNewLine, dialect=dialect)
    return generateAndWriteQueries(list(tables.values()), targetPath, filemode=filemode, encoding=encoding)

def createTables(
        json: Union[list[dict[str, Any]], dict[str, Any]],
        fake: Faker,
        amount: int=20,
        noNewLine: bool=False,
        dialect: SD=SD.DEFAULT
        ) -> dict[str, TableModel]:
    """
    Creates and returns tableModels according to the given json
    """
    tables: dict[str, TableModel] = {}
    data: list[dict[str, Any]]
    if not isinstance(json, list):
        data = [json]
    else:
        data = json
    for table in data:
        tablename: str = table["table"]
        if tablename in tables:
            raise exceptions.DuplicateTablenameException()
        columns: dict[str, Column] = {}
        for cName, cDesc in table["columns"].items():
            newColumn: Optional[Column]
            if isinstance(cDesc, str):
                newColumn = Column(cName, Dt[cDesc.upper()])
            elif isinstance(cDesc, dict):
                newColumn = Column(cName, Dt[cDesc["type"].upper()], cDesc)
            else:
                raise TypeError("Column description must be string or map")
            columns[newColumn.name] = newColumn
            if newColumn.type.value >= 2000:
                if not isinstance(cDesc, dict):
                    raise TypeError("Column description must be map for dependent types")
                split: list[str] = str(newColumn.metadata.foreignColumn()).split(".")
                listener = ColumnListener()
                if len(split) == 1:
                    columns[split[0]].addListener(listener)
                    newColumn.ownTable = True
                elif len(split) == 2:
                    tables[split[0]].columns[split[1]].addListener(listener)
                else:
                    raise KeyError()
                newColumn.listenTo(listener)
        newTable: TableModel = TableModel(fake, tablename, columns, table.get("amount", amount), noNewLine, dialect)
        tables[tablename] = newTable
    return tables
    

def generateAndWriteQueries(
        tables: list[TableModel],
        targetPath: str,
        filemode: str="x",
        encoding: str="utf-8"
                            ) -> Optional[str]:
    """
    Generates all queries according to the given tables and stores them
    Returns the path under which the query was stored
    """
    try:
        with open(targetPath, filemode, encoding=encoding) as file:
            if filemode == "a":
                file.write("\n\n-- The following Queries have been generated automatically using a script and appended to this file\n\n")
            for newTable in tables:
                query: str = newTable.generate()
                file.write(query)
                file.write("\n\n")
    except Exception as e:
        print(e)
        print(traceback.format_exc())
        if filemode == "x":
            print("removing created file")
            os.remove(targetPath)
        return None
    else:
        print("Successfully wrote query into", targetPath)
    return targetPath