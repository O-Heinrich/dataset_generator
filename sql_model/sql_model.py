from faker import Faker

class SqlModel:
    def __init__(self, fake, tablename, columns):
        if not isinstance(fake, Faker) or not isinstance(columns, list):
            raise TypeError()
        self.fake = fake
        self.columns = columns
        self.tablename = tablename

    def generate(self, amount=1):
        query = "INSERT INTO " + self.tablename + " ("
        query += ", ".join([c.name for c in self.columns])
        query += ")\nVALUES\n"
        
        pass