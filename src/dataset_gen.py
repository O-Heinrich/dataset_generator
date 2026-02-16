from faker import Faker
import argparse
from sql_model import SqlModel
from column import Column
from datatypes import Datatype as Dt
from wonderwords import RandomWord
import json
import exceptions
import os
import traceback
import subprocess
import os
import platform

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

# get input arguments
parsed: argparse.Namespace = parser.parse_args()
localization: str = parsed.location
encoding: str = parsed.encoding
jsonPath: str = parsed.jsonfile
targetPath: str = parsed.filepath
appendMode: str = parsed.append
overwriteMode: str = parsed.overwrite
amount: int = parsed.amount

# validate input arguments and create resulting objects
r = RandomWord()
targetPath = targetPath or r.word() + "_" + r.word() + "_" + r.word() + ".sql"
filemode = "w" if overwriteMode else "a" if appendMode else "x"
fake = Faker(localization)

with open(jsonPath, 'r') as jsonfile:
    data = json.load(jsonfile)
    dbname: str = data["db_name"]
    columns: list[Column] = []
    for cName, cDesc in data["columns"].items():
        if isinstance(cDesc, str):
            columns.append(Column(cName, Dt[cDesc.upper()]))
        elif isinstance(cDesc, dict):
            columns.append(Column(cName, Dt[cDesc["type"].upper()], {k: v for k, v in cDesc.items() if k != "type"}))
        else:
            raise TypeError("Column description must be string or map")
    amount = data.get("amount", amount)

model: SqlModel = SqlModel(fake, dbname, columns)

# generate datasets and write them into a file
try: 
    with open(targetPath, filemode, encoding=encoding) as file:
        query: str = model.generate(amount)
        file.write(query)
except (exceptions.TooManyUniqueFailsException, TypeError, ValueError) as e:
    print(e)
    #print(traceback.format_exc())
    if filemode == "x":
        print("removing created file")
        os.remove(targetPath)