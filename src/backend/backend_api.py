from faker import Faker
from wonderwords import RandomWord
from backend.tableModel import TableModel
import os
import traceback
from exceptions.exceptions import DuplicateTablenameException
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
    API for generating SQL-Queries.
    Generates all queries according to the given json and Parameters.
    Returns the path under which the file was stored, or None on failure.
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
    """Creates and returns TableModels according to the given json."""
    tables: dict[str, TableModel] = {}
    data: list[dict[str, Any]] = sortTables(json)
    # Iterate over each table given by the data to create the TableModels
    for table in data:
        tablename: str = table["table"]
        if tablename in tables:
            raise DuplicateTablenameException()
        columns: dict[str, Column] = {}
        # Iterate over Columns for the table to create each Column
        for cName, cDesc in table["columns"].items():
            newColumn: Optional[Column]
            if isinstance(cDesc, str):
                newColumn = Column(cName, Dt[cDesc.upper()])
            elif isinstance(cDesc, dict):
                newColumn = Column(cName, Dt[cDesc["type"].upper()], cDesc)
            else:
                raise TypeError("Column description must be string or map")
            columns[newColumn.name] = newColumn
            # Check for dependend type and add a ColumnListener if necessary
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
        # Create TableModel
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
    Generates all queries according to the given tables and stores them.
    Returns the path under which the query was stored.
    """
    try:
        with open(targetPath, filemode, encoding=encoding) as file:
            if filemode == "a":
                file.write("\n\n-- The following Queries have been generated automatically using a script and appended to this file\n\n")
            for newTable in tables:
                query: str = newTable.generate()
                file.write(query)
                file.write("\n\n")
    except FileExistsError:
        print(f'File {targetPath} already exists')
        return None
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


def sortTables(tables: Union[list[dict[str, Any]], dict[str, Any]]) -> list[dict[str, Any]]:
    """Sorts a list of dictionaries representing tables such that all foreign keys are usable before transforming them to TableModels"""
    if isinstance(tables, dict):
        return [tables]
    namesToReferences: dict[str, set[str]] = {}
    for table in tables:
        tName = table.get("table")
        assert tName and isinstance(tName, str)
        namesToReferences[tName] = set()
    for table in tables:
        tName = table.get("table")
        assert tName and isinstance(tName, str)
        references: set[str] = namesToReferences[tName]
        cc = table.get("columns")
        assert cc and isinstance(cc, dict)
        columns: dict[str, Any] = cc
        for val in columns.values():
            if isinstance(val, dict):
                fc = val.get("column")
                if fc and isinstance(fc, str) and fc.find(".") > 0:
                    references.add(fc.split(".")[0])

    sortedNames: list[str] = []
    while len(sortedNames) < len(tables):
        removed: list[str] = []

        for name, references in namesToReferences.items():
            if len(references) == 0:
                removed.append(name)
                sortedNames.append(name)
        for name in removed:
            del namesToReferences[name]

        for references in namesToReferences.values():
            for name in removed:
                references.discard(name)

        if len(removed) == 0:
            raise ValueError("Cannot sort tables")
        
    sortedTables: list[dict[str, Any]] = []
    for name in sortedNames:
        for table in tables:
            if table.get("table") == name:
                sortedTables.append(table)
                break
    return sortedTables