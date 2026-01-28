from faker import Faker
import argparse

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