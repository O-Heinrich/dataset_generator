from faker import Faker
import argparse
from sql_model import SqlModel
from column import Column
from datatypes import Datatype as Dt

# allow parsing arguments on commmand line
parser = argparse.ArgumentParser()

parser.add_argument('-l', action="store", dest="location", default="de_DE")
parser.add_argument('-p', action="store", dest="jsonfile", default="")
parser.add_argument('-f', action="store", dest="filepath", default="")
parser.add_argument('-a', action="store_true", dest="append", default=False)

parsed = parser.parse_args()
localization = parsed.location
jsonPath = parsed.jsonfile
targetPath = parsed.filepath
# TODO: validate path
appendMode = parsed.append

fake = Faker(localization)

columns = [
    Column("id", Dt.PRIMARY_KEY),
    Column("value", Dt.INTEGER, {"max":100}),
    Column("name", Dt.FULL_NAME),
    Column("date", Dt.DATE),
    Column("plz", Dt.PLZ)
]

model = SqlModel(fake, "dbname", columns)

file = open("test.txt", "w")
query = model.generate(20)
file.write(query)
file.close()