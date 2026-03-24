from faker import Faker
from backend.column import Column
from backend.helpers import createInsertQuery
from enums.datatypes import Datatype as Dt
from enums.dialect import SqlDialect as SD

from typing import Optional, Any

class TableModel:
    def __init__(self, fake: Faker, tablename: str, columns: dict[str, Column], amount: int, noNewlines: bool=False, dialect: SD=SD.DEFAULT):
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
        self.dialect: SD = dialect

    def generate(self) -> str:
        generatedValues: list[list[Any]] = []
        for _ in range(self.amount):
            key: Optional[int] = None
            if self.primary is not None:
                key = self.columns[self.primary].predictKey()
            fKeys: dict[str, int] = {}
            generatedValues.append([c.getValue(self.fake, key, fKeys) for c in self.columns.values()])
        return createInsertQuery(self.tablename, [n for n in self.columns.keys()], generatedValues, self.dialect, noNewLine=self.noNewlines)