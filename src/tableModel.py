from faker import Faker
from column import Column
from helpers import stringify
from datatypes import Datatype as Dt

from typing import Optional

class TableModel:
    def __init__(self, fake: Faker, tablename: str, columns: dict[str, Column], amount: int, noNewlines: bool=False):
        self.fake: Faker = fake
        self.columns: dict[str, Column] = columns
        self.tablename: str = tablename
        self.amount: int = amount
        self.primary: Optional[str] = None
        self.foreign: list[str] = []
        for name, c in self.columns.items():
            if c.type == Dt.PRIMARY_KEY:
                self.primary = name
            elif c.type == Dt.FOREIGN_KEY:
                self.foreign.append(name)
        self.noNewlines: bool = noNewlines

    def generate(self) -> str:
        query: str = "INSERT INTO " + self.tablename + " ("
        query += ", ".join(self.columns.keys())
        query += ") VALUES\n"
        
        generatedValues: list[str] = []
        for _ in range(self.amount):
            newValue: str = "("
            key: Optional[int] = None
            if self.primary is not None:
                key = self.columns[self.primary].predictKey()
            fKeys: dict[str, int] = {}
            newValue += ", ".join([stringify(c.getValue(self.fake, key, fKeys)) for c in self.columns.values()])
            newValue += ")"
            generatedValues.append(newValue)
        sep: str = ",\n"
        if self.noNewlines:
            sep = ", "
        query += sep.join(generatedValues)
        query += ";"
        return query