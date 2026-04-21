from faker import Faker
from backend.column import Column
from backend.queryCreator import createInsertQuery
from enums.datatypes import Datatype as Dt
from enums.dialect import SqlDialect as SD
from typing import Optional, Any

class TableModel:
    """Represents one table, consisting of Columns."""

    def __init__(self, fake: Faker, tablename: str, columns: dict[str, Column], amount: int, noNewlines: bool=False, dialect: SD=SD.DEFAULT):
        self.fake: Faker = fake
        self.columns: dict[str, Column] = columns
        self.tablename: str = tablename
        self.amount: int = amount
        self.primary: Optional[Column] = None
        self.foreign: list[str] = []
        requiresPrimary: bool = False
        for name, c in self.columns.items():
            if c.type == Dt.PRIMARY_KEY:
                self.primary = c
            elif c.type == Dt.FOREIGN_KEY:
                self.foreign.append(name)
            if c.type.value >= 2000 and c.metadata.foreignColumn().find(".") == -1:
                requiresPrimary = True
        if requiresPrimary and not self.primary:
            self.primary = Column("hidden_primary", Dt.PRIMARY_KEY, hidden=True)
        self.noNewlines: bool = noNewlines
        self.dialect: SD = dialect

    def generate(self) -> str:
        """Generates values for this table and passes them to queryCreator to turn them into an SQL-Query."""
        generatedValues: list[list[Any]] = []
        for _ in range(self.amount):
            key: Optional[int] = None
            fKeys: dict[str, int] = {}
            if self.primary is not None:
                key = self.primary.predictKey()
                if self.primary.hidden:
                    self.primary.getValue(self.fake, key, fKeys)
            generatedValues.append([c.getValue(self.fake, key, fKeys) for c in self.columns.values()])
        return createInsertQuery(self.tablename, self.columns.keys(), generatedValues, self.dialect, noNewLine=self.noNewlines)