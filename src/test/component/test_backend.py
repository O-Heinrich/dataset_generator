import unittest
from parameterized import parameterized

from faker import Faker
import random

import os
import json as j
import re
import datetime

from test.utils.test_utils import compare_trimmedFiles
from enums.dialect import SqlDialect
from backend.backend_api import generateData

BASE_PATH = "./src/test/component/" if __name__ == '__main__' else "./test/component/"
TARGET_PATH = BASE_PATH + "actual.sql"

class TestBackend(unittest.TestCase):

    def seed(self, seed=42):
        """Set Seed for random, rstr (via random) and Faker - Does not seed wonderwords"""
        Faker.seed(seed) # Faker version: 40.4.0
        random.seed(seed)

    def tearDown(self):
        if os.path.exists(TARGET_PATH):
            os.remove(TARGET_PATH)


    @parameterized.expand([
        "datetime", "datetime_dependend", "time_rounding", "datetime_parameters", "time_minmax",
        "names_addresses", "names_titles",
        "regex",
        "values",# "values_import", # TODO: values_import will fail when this is run individually, due to different relative paths
        "numbers", "numbers_dependend",
        "dependend_owntable"
    ])
    def test_seeded(self, name: str):
        """
        Takes a file with named "input_" + name + ".json" from the input_files directory as json input
        Expects a query equal to the content of "expected_" + name + ".sql" from the expected_files directory as sql output
        To generate the expected file run ./gen.ps1 with the -seed flag or ./gen.sh with the -s flag set to 42
        """
        ### given
        self.seed()
        inputPath = BASE_PATH + "input_files/input_" + name + ".json"
        expectedPath = BASE_PATH + "expected_files/expected_" + name + ".sql"
        with open(inputPath, 'r') as jsonfile:
            json = j.load(jsonfile)

        ### when
        resultPath = generateData(json=json, targetFilePath=TARGET_PATH)

        ### then
        self.assertIsNotNone(resultPath, "Did not generate a file")
        self.assertEqual(resultPath, TARGET_PATH, "Result path is not the same as the target path")
        compare_trimmedFiles(TARGET_PATH, expectedPath)

    def test_date_unseeded(self):
        ### given
        inputPath = BASE_PATH + "input_files/input_date_unseeded.json"
        with open(inputPath, 'r') as jsonfile:
            json = j.load(jsonfile)
        end = datetime.datetime.now()
        start = datetime.datetime(year=end.year-99, month=end.month, day=end.day, hour=end.hour, minute=end.minute, second=end.second)

        ### when
        resultPath = generateData(json=json, targetFilePath=TARGET_PATH)

        ### then
        self.assertIsNotNone(resultPath, "Did not generate a file")
        self.assertEqual(resultPath, TARGET_PATH, "Result path is not the same as the target path")
        with open(resultPath, 'r') as resultfile:
            results = [line.strip() for line in resultfile]
        reg = r'\(\d\d?, "(\d{4}-\d\d-\d\d)", "(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)"\)[,;]'
        for l in results[1:101]:
            self.assertRegex(l, reg, f'line {l} is not a valid line for a date and a datetime')
            matcher = re.match(reg, l)
            date_result = datetime.datetime.strptime(matcher.group(1), "%Y-%m-%d").date()
            datetime_result = datetime.datetime.strptime(matcher.group(2), "%Y-%m-%d %H:%M:%S")
            self.assertGreaterEqual(date_result, start.date())
            self.assertGreaterEqual(datetime_result, start)
            self.assertGreater(end.date(), date_result)
            self.assertGreater(end, datetime_result)


    @parameterized.expand([
        SqlDialect.DEFAULT,
        SqlDialect.POSTGRESQL
    ])
    def test_dialect_seeded(self, dialect: SqlDialect):
        ### given
        self.seed()
        inputPath = BASE_PATH + "input_files/input_general_example.json"
        expectedPath = BASE_PATH + "expected_files/expected_" + dialect.name.lower() + "_dialect.sql"
        with open(inputPath, 'r') as jsonfile:
            json = j.load(jsonfile)

        ### when
        resultPath = generateData(json=json, targetFilePath=TARGET_PATH, dialect=dialect)

        ### then
        self.assertIsNotNone(resultPath, "Did not generate a file")
        self.assertEqual(resultPath, TARGET_PATH, "Result path is not the same as the target path")
        compare_trimmedFiles(TARGET_PATH, expectedPath)


    def test_nonewline_seeded(self):
        ### given
        self.seed()
        inputPath = BASE_PATH + "input_files/input_nonewline_example.json"
        expectedPath = BASE_PATH + "expected_files/expected_nonewline.sql"
        with open(inputPath, 'r') as jsonfile:
            json = j.load(jsonfile)

        ### when
        resultPath = generateData(json=json, targetFilePath=TARGET_PATH, noNewLine=True)

        ### then
        self.assertIsNotNone(resultPath, "Did not generate a file")
        self.assertEqual(resultPath, TARGET_PATH, "Result path is not the same as the target path")
        compare_trimmedFiles(TARGET_PATH, expectedPath)

    def test_appendmode_seeded(self):
        ### given
        self.seed()
        inputPath = BASE_PATH + "input_files/input_general_example.json"
        expectedPath = BASE_PATH + "expected_files/expected_append_mode.sql"
        with open(inputPath, 'r') as jsonfile:
            json = j.load(jsonfile)
        with open(TARGET_PATH, 'x') as targetfile:
            targetfile.write("CREATE TABLE myCoolTable (unique_id, name, address, plz, town, Float, Int, Date, Time, DateTime, values, regex);")

        ### when
        resultPath = generateData(json=json, targetFilePath=TARGET_PATH, filemode='a')

        ### then
        self.assertIsNotNone(resultPath, "Did not generate a file")
        self.assertEqual(resultPath, TARGET_PATH, "Result path is not the same as the target path")
        compare_trimmedFiles(TARGET_PATH, expectedPath)

    def test_overwritemode_seeded(self):
        ### given
        self.seed()
        inputPath = BASE_PATH + "input_files/input_general_example.json"
        expectedPath = BASE_PATH + "expected_files/expected_default_dialect.sql"
        with open(inputPath, 'r') as jsonfile:
            json = j.load(jsonfile)
        with open(TARGET_PATH, 'x') as targetfile:
            targetfile.write("CREATE TABLE myCoolTable (unique_id, name, address, plz, town, Float, Int, Date, Time, DateTime, values, regex);")

        ### when
        resultPath = generateData(json=json, targetFilePath=TARGET_PATH, filemode='w')

        ### then
        self.assertIsNotNone(resultPath, "Did not generate a file")
        self.assertEqual(resultPath, TARGET_PATH, "Result path is not the same as the target path")
        compare_trimmedFiles(TARGET_PATH, expectedPath)

if __name__ == '__main__':
    unittest.main()