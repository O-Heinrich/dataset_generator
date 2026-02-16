from faker import Faker
from column import Column
from helpers import stringify

from typing import Any

class SqlModel:
    def __init__(self, fake: Faker, tablename: str, columns: list[Column]):
        self.fake: Faker = fake
        self.columns: list[Column] = columns
        self.tablename: str = tablename

    def generate(self, amount: int=1) -> str:
        query = "INSERT INTO " + self.tablename + " ("
        query += ", ".join([str(c) for c in self.columns])
        query += ")\nVALUES\n"
        
        generatedData: list[Any] = [c.getListGenerator(self.fake)(amount) for c in self.columns]
        columnSortedData: list[list[Any]] = [[] for _ in range(amount)]
        for data in generatedData:
            for s, d in zip(columnSortedData, data):
                s.append(d)

        query += ",\n".join(["(" + ", ".join(map(stringify, dataset)) + ")" for dataset in columnSortedData])
        query += ";"
        return query