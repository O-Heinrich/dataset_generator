from faker import Faker
from wonderwords import RandomWord
from datatypes import Datatype as Dt
import nameGenerator as ng
import address_generator as ag
import numbers_generator as numg
import random
from rstr import xeger

class Column:
    nextkey = "nextkey"

    def __init__(self, name, type, metadata={}):
        if not isinstance(type, Dt) or not isinstance(metadata, dict):
            raise TypeError()
        self.name = name
        self.type = type
        self.metadata = metadata
        if type == Dt.PRIMARY_KEY and not Column.nextkey in self.metadata:
            self.metadata[Column.nextkey] = 0

    def getGenerator(self, fake):
        if not isinstance(fake, Faker):
            raise TypeError()
        min = self.metadata.get("min", 0)
        max = self.metadata.get("max")
        acc = self.metadata.get("acc", 100)

        if self.type == Dt.FIRST_NAME:
            return lambda: ng.generateFirstName(fake)
        elif self.type == Dt.LAST_NAME:
            return lambda: ng.generateLastName(fake)
        elif self.type == Dt.FULL_NAME:
            return lambda: ng.generateFullName(fake)
        elif self.type == Dt.COMPANY_NAME:
            return lambda: ag.generateCompanyName(fake)
        elif self.type == Dt.STREET:
            return lambda: ag.generateAddress(fake).street
        elif self.type == Dt.STREET_HOUSENUMBER:
            return lambda: ag.generateAddress(fake).streetHousenumber()
        elif self.type == Dt.HOUSENUMBER:
            return lambda: ag.generateAddress(fake).housenumber
        elif self.type == Dt.TOWN:
            return lambda: ag.generateAddress(fake).town
        elif self.type == Dt.PLZ:
            return lambda: ag.generateAddress(fake).plz
        elif self.type == Dt.FULL_ADDRESS:
            return lambda: ag.generateAddress(fake)
        elif self.type == Dt.MONEY:
            if max is None:
                raise ValueError("Max value is missing")
            return lambda: numg.generateFloat(min, max)
        elif self.type == Dt.INTEGER:
            if max is None:
                raise ValueError("Max value is missing")
            return lambda: random.randrange(min, max)
        elif self.type == Dt.FLOAT:
            if max is None:
                raise ValueError("Max value is missing")
            return lambda: numg.generateFloat(min, max, acc)
        elif self.type == Dt.DATE:
            return lambda: numg.generateDate(fake)
        elif self.type == Dt.TIME:
            return lambda: numg.generateTime(fake)
        elif self.type == Dt.DATE_TIME:
            return lambda: numg.generateDateTime(fake)
        elif self.type == Dt.VALUES:
            values = self.metadata.get("values")
            if values is None or not isinstance(values, list):
                raise ValueError("For Values Type there must be metadata for the values")
            return lambda: values[random.randrange(len(values))]
        elif self.type == Dt.FORMAT_STRING:
            reg = self.metadata.get("regex")
            if reg is None:
                raise ValueError("No Regex given")
            return lambda: xeger(reg)
        elif self.type == Dt.RANDOM_STRING:
            r = RandomWord()
            return lambda: r.word()
        elif self.type == Dt.PRIMARY_KEY:
            return lambda: self.getNextKeys()[0]
        elif self.type == Dt.FOREIGN_KEY:
            raise NotImplementedError()
        else:
            raise NotImplementedError()

    def getListGenerator(self, fake):
        if not isinstance(fake, Faker):
            raise TypeError()
        unique = self.metadata.get("unique", False)
        maxUniqueFailsMultiplier = self.metadata.get("mufm", 3)
        min = self.metadata.get("min", 0)
        max = self.metadata.get("max")
        acc = self.metadata.get("acc", 100)
        
        if self.type == Dt.FIRST_NAME:
            return lambda size: ng.generateFirstNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.LAST_NAME:
            return lambda size: ng.generateLastNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.FULL_NAME:
            return lambda size: ng.generateFullNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.COMPANY_NAME:
            return lambda size: ag.generateCompanyNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.STREET:
            return lambda size: [c.street for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.STREET_HOUSENUMBER:
            return lambda size: [c.streetHousenumber() for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.HOUSENUMBER:
            return lambda size: [c.housenumber for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.TOWN:
            return lambda size: [c.town for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.PLZ:
            return lambda size: [c.plz for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.FULL_ADDRESS:
            return lambda size: ag.generateAddressList(fake, size)
        elif self.type == Dt.MONEY:
            if max is None:
                raise ValueError("Max value is missing")
            return lambda size: numg.generateFloatList(size, min, max)
        elif self.type == Dt.INTEGER:
            if max is None:
                raise ValueError("Max value is missing")
            return lambda size: [random.randrange(min, max) for _ in range(size)]
        elif self.type == Dt.FLOAT:
            if max is None:
                raise ValueError("Max value is missing")
            return lambda size: numg.generateFloatList(size, min, max, acc)
        elif self.type == Dt.DATE:
            return lambda size: numg.generateDateList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.TIME:
            return lambda size: numg.generateTimeList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.DATE_TIME:
            return lambda size: numg.generateDateTimeList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.VALUES:
            values = self.metadata.get("values")
            if values is None or not isinstance(values, list):
                raise ValueError("For Values Type there must be metadata for the values")
            return lambda size: [values[random.randrange(len(values))] for _ in range(size)]
        elif self.type == Dt.FORMAT_STRING:
            reg = self.metadata.get("regex")
            if reg is None:
                raise ValueError("No Regex given")
            return lambda size: [xeger(reg) for _ in range(size)]
        elif self.type == Dt.RANDOM_STRING:
            r = RandomWord()
            return lambda size: [r.word() for _ in range(size)]
        elif self.type == Dt.PRIMARY_KEY:
            return lambda size: self.getNextKeys(size)
        elif self.type == Dt.FOREIGN_KEY:
            raise NotImplementedError()
        else:
            raise NotImplementedError()
        
    def getNextKeys(self, amount=1):
        id = self.metadata.get(Column.nextkey)
        if id is None:
            raise ValueError("No ID given")
        self.metadata[Column.nextkey] += amount
        return [i for i in range(id, id + amount)]