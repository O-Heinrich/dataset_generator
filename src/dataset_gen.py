from faker import Faker
import argparse
from tableModel import TableModel
from column import Column
from datatypes import Datatype as Dt
from wonderwords import RandomWord
import json
import exceptions
import os
import traceback
from columnListener import ColumnListener
import subprocess
import os
import platform
from dialect import SqlDialect as SD, toDialect

from typing import Optional, Union

# get python venv path
python_path: str = ""
if platform.system() == "Windows":
    scripts_path: str = os.path.join(".", "generator_venv", "Scripts", "python.exe")
    if os.path.exists(scripts_path):
        python_path = scripts_path
    else:
        python_path = os.path.join(".", "generator_venv", "bin", "python.exe")
else:
    # assume linux, don't care about mac
    python_path = os.path.join(".", "generator_venv", "bin", "python")

# type check
type_check_return_code: int = subprocess.call([python_path, "-m", "mypy", "--config-file", "./mypy.ini", "./src/"])
if type_check_return_code != 0:
    exit(type_check_return_code)

# allow parsing arguments on commmand line
parser = argparse.ArgumentParser()

parser.add_argument('-l', action="store", dest="location", default="de_DE")
parser.add_argument('-e', action="store", dest="encoding", default="utf-8")
parser.add_argument('-p', action="store", dest="jsonfile", default="example.json")
parser.add_argument('-f', action="store", dest="filepath", default="")
parser.add_argument('-a', action="store_true", dest="append", default=False)
parser.add_argument('-o', action="store_true", dest="overwrite", default=False)
parser.add_argument('-n', action="store", dest="amount", type=int, default=20)
parser.add_argument('--oneline', action="store_true", dest="noNewline", default=False)
parser.add_argument('-d', action="store", dest="sqlDialect", default="")

# get input arguments
parsed: argparse.Namespace = parser.parse_args()
localization: str = parsed.location
encoding: str = parsed.encoding
jsonPath: str = parsed.jsonfile
targetPath: str = parsed.filepath
appendMode: bool = parsed.append
overwriteMode: bool = parsed.overwrite
amount: int = parsed.amount
noNewline: bool = parsed.noNewline
sqlDialect: str = parsed.sqlDialect

# validate input arguments and create resulting objects
r = RandomWord()
targetPath = targetPath or r.word() + "_" + r.word() + "_" + r.word() + ".sql"
filemode: str = "w" if overwriteMode else "a" if appendMode else "x"
fake: Faker = Faker(localization)
dialect: SD = SD.DEFAULT
if sqlDialect:
    dialect = toDialect(sqlDialect)

tables: dict[str, TableModel] = {}
with open(jsonPath, 'r') as jsonfile:
    data: Union[list[dict], dict] = json.load(jsonfile)
    ldata: list[dict]
    if not isinstance(data, list):
        ldata = [data]
    else:
        ldata = data
    for table in ldata:
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
        newTable: TableModel = TableModel(fake, tablename, columns, table.get("amount", amount), noNewline, dialect)
        tables[tablename] = newTable

# generate datasets and write them into a file
try:
    with open(targetPath, filemode, encoding=encoding) as file:
        if filemode == "a":
            file.write("\n\n-- The following Queries have been generated automatically using a script and appended to this file\n\n")
        for newTable in tables.values():
            query: str = newTable.generate()
            file.write(query)
            if noNewline:
                file.write("\n")
            else:
                file.write("\n\n")
except Exception as e:
    print(e)
    print(traceback.format_exc())
    if filemode == "x":
        print("removing created file")
        os.remove(targetPath)
else:
    print("Successfully wrote query into", targetPath)