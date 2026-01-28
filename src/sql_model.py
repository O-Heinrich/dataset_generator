from faker import Faker
from column import Column

class SqlModel:
    def __init__(self, fake, tablename, columns):
        if not isinstance(fake, Faker) or not isinstance(columns, list) or not all(isinstance(c, Column) for c in columns):
            raise TypeError()
        self.fake = fake
        self.columns = columns
        self.tablename = tablename

    def generate(self, amount=1):
        query = "INSERT INTO " + self.tablename + " ("
        query += ", ".join([c.name for c in self.columns])
        query += ")\nVALUES\n"
        
        generatedData = [c.getListGenerator(self.fake)(amount) for c in self.columns]
        columnSortedData = [[] for _ in range(amount)]
        for data in generatedData:
            for s, d in zip(columnSortedData, data):
                s.append(d)
        query += ",\n".join(["(" + ", ".join(map(str, dataset)) + ")" for dataset in columnSortedData])
        query += ";"
        return query