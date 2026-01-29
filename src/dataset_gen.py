from faker import Faker
import argparse
from sql_model import SqlModel
from column import Column
from datatypes import Datatype as Dt
from wonderwords import RandomWord
import json
import exceptions
import os

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
parsed = parser.parse_args()
localization = parsed.location
encoding = parsed.encoding
jsonPath = parsed.jsonfile
targetPath = parsed.filepath
appendMode = parsed.append
overwriteMode = parsed.overwrite
amount = parsed.amount

# validate input arguments and create resulting objects
r = RandomWord()
targetPath = targetPath or r.word() + "_" + r.word() + "_" + r.word() + ".sql"
filemode = "w" if overwriteMode else "a" if appendMode else "x"
fake = Faker(localization)

with open(jsonPath, 'r') as jsonfile:
    data = json.load(jsonfile)
    dbname = data["db_name"]
    columns = []
    for cName, cDesc in data["columns"].items():
        if isinstance(cDesc, str):
            columns.append(Column(cName, Dt[cDesc.upper()]))
        elif isinstance(cDesc, dict):
            columns.append(Column(cName, Dt[cDesc["type"].upper()], {k: v for k, v in cDesc.items() if k != "type"}))
        else:
            raise TypeError("Column description must be string or map")
    amount = data.get("amount", amount)

model = SqlModel(fake, dbname, columns)

# generate datasets and write them into a file
file = open(targetPath, filemode, encoding=encoding)
try:
    query = model.generate(amount)
except exceptions.TooManyUniqueFailsException as e:
    print("Failed to generate data because not enough unique values could be generated")
    file.close()
    if filemode == "x":
        print("removing created file")
        os.remove(targetPath)
except (TypeError, ValueError) as e:
    print(e)
    file.close()
    if filemode == "x":
        print("removing created file")
        os.remove(targetPath)
else:
    file.write(query)
    file.close()