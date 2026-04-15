import argparse
import json
from enums.dialect import SqlDialect as SD, toDialect
from backend.backend_api import generateData
from typing import Union
from typeCheck import typeCheck

# static type checking with mypy
typeCheck()

# allow passing arguments on commmand line
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

# parse values for filemode and sql dialect
filemode: str = "w" if overwriteMode else "a" if appendMode else "x"
dialect: SD = SD.DEFAULT
if sqlDialect:
    dialect = toDialect(sqlDialect)

# call backend api and generate queries
with open(jsonPath, 'r') as jsonfile:
    data: Union[list[dict], dict] = json.load(jsonfile)
    generateData(data, targetPath, filemode=filemode, noNewLine=noNewline, localization=localization, encoding=encoding, dialect=dialect)